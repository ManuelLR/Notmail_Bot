# Copyright 2017 by Notmail Bot contributors. All rights reserved.
#
# This file is part of Notmail Bot.
#
#     Notmail Bot is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Notmail Bot is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Notmail Bot.  If not, see <http:#www.gnu.org/licenses/>.
import imaplib
import logging
import os, sys
import email as email_lib
from email.header import decode_header
from bs4 import BeautifulSoup
import re

imaplib._MAXLINE = 100000

class Message:
    def __init__(self, email, uid, folders, msg, flags=None):
        self.email = email
        self.uid = uid
        self.folders = folders
        self.msg = email_lib.message_from_bytes(msg[1])
        try:
            self.flags = imaplib.ParseFlags(flags)
        except:
            self.flags = None

    @staticmethod
    def __fix_string(input):
        res = ""
        for input_mod, encoding in decode_header(input):
            try:
                is_bytes = isinstance(input_mod, bytes)
                if is_bytes and (encoding is None or "unknown" in encoding):
                    result = input_mod.decode()
                elif is_bytes and encoding is not None:
                    result = input_mod.decode(encoding=encoding)
                elif isinstance(input_mod, str):
                    result = input_mod
                else:
                    result = input_mod.decode(encoding)
            except AttributeError as ae:
                result = str(input_mod)
                pass
            except Exception as e:
                logging.error(e)
                logging.error(str(input_mod))
                result = str(input_mod)
            res = res + result + " "
        return res

    def get_header(self, property):
        return self.__fix_string(self.msg[property])

    def get_flag(self, property=None):
        if not property or not self.flags:
            return False
        return bytes("\\" + property, 'utf-8') in self.flags

    def get_body(self):
        maintype = self.msg.get_content_maintype()
        if maintype == 'multipart':
            html_body = None
            for part in self.msg.get_payload():
                if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
                    return Message.__decode_body_from_part_message(part)
                elif part.get_content_maintype() == 'text' and part.get_content_subtype() == 'html':
                    html_body = part
                elif part.get_content_maintype() == 'multipart':
                    for part_in in part.get_payload():
                        if part_in.get_content_maintype() == 'text' and part_in.get_content_subtype() == 'plain':
                            return Message.__decode_body_from_part_message(part_in)
                        elif part.get_content_maintype() == 'text' and part_in.get_content_subtype() == 'html':
                            html_body = part
            else:
                if html_body is not None:
                    return Message.__decode_body_from_part_message(html_body, is_html=True)
                else:
                    return "😥🙃 no compatible format found"

        elif maintype == 'text':
            return Message.__decode_body_from_part_message(self.msg, is_html=self.msg.get_content_subtype()!="plain")

    @staticmethod
    def __decode_body_from_part_message(part_msg, is_html=False, del_double_new_line=False):
        encode = part_msg.get_content_charset(failobj="utf-8")
        if not is_html:
            text_decode = part_msg.get_payload(decode=True).decode(encoding=encode)
        else:
            text = re.sub(" ?\r?\n\<\/", "</", part_msg.get_payload(decode=True).decode(encoding=encode))
            soup = BeautifulSoup(text)
            for script in soup(["script", "style"]):
                script.extract()
            text_decode = soup.get_text()

        if del_double_new_line:
            # break into lines and remove leading and trailing space on each
            lines = (line for line in text_decode.splitlines())
#            lines = (line.strip() for line in text_decode.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase for line in lines for phrase in line.split("  "))
#            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            res = '\n'.join(chunk for chunk in chunks)
        else:
            res = re.sub(" ?\r?\n[\r?\n ?]+", "\n\n", text_decode.strip())

        return res


class Folder:
    def __init__(self, raw_folder):
        split1 = raw_folder.decode().split(' \"/\"')
        name = split1[1].replace(' \"', '').replace('\"', '')
        self.flags = split1[0]
        self.name = name


def connect(imap_server, imap_port, email, password):
    mail = imaplib.IMAP4_SSL(imap_server, imap_port)
    mail.login(email, password)
    mail.user = email
    return mail


def get_email_by_uid(mail, folder, uid):
    mail.select(folder, readonly=True)
    typ, data = mail.uid('FETCH', uid, '(FLAGS RFC822)')
    # typ, data = mail.uid('FETCH', uid, '(RFC822)')
    if typ != "OK" or len(data) < 2:
        logging.debug("Error retrieving :" + str(folder) + "  __@" + str(uid))
        return

    return Message(mail.user, uid, [folder], data[0], data[1])


# Sorted from oldest(0) to newest(-1)
def get_uid_list(mail, folder):
    mail.select(folder, readonly=True)  # Don't mark message as read

    try:
        type, data = mail.uid('search', None, "ALL")  # search and return uids instead
        # type, data = mail.search(None, 'UnSeen')
        mail_uids = data[0].split()

        return mail_uids, None

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error(exc_type, fname, exc_tb.tb_lineno)
        logging.error(e)
        return [], e


def change_flags(mail, folder, email_uid, flag, put_or_quit):
    if put_or_quit not in ['+', '-']:
        logging.fatal("Incorrect flag!")

    mail.select(folder, readonly=False)
    typ, data = mail.uid('STORE', email_uid, put_or_quit+'FLAGS', '\\'+flag)
    if typ != 'OK':
        logging.info(email_uid + ':' + put_or_quit + ':' + flag)
        logging.info(data)
        logging.error("Failed to apply " + str(put_or_quit) + "FLAGS " + flag)


def edit_flag_modified(mail, folder, email_uid, flag, put_or_quit):
    if put_or_quit not in ['+', '-']:
        logging.fatal("Incorrect flag!")

    mail.select(folder, readonly=False)
    typ, data = mail.uid('STORE', email_uid, put_or_quit + 'FLAGS', flag)
    if typ != 'OK':
        logging.info(email_uid + ':' + put_or_quit + ':' + flag)
        logging.info(data)
        logging.error("Failed to apply " + str(put_or_quit) + "FLAGS " + flag)
    # mail.select(folder, readonly=False)


def get_folders(mail):
    typ, data = mail.list('""', '*')
    result = []
    if typ != "OK":
        logging.error("Failed to list the folders")
        return None
    for mbox in data:
        result.append(Folder(mbox))

    return result


def add_message_to_folder(mail, uid, origin_folder, destination_folder):
    mail.select(origin_folder, readonly=False)
    result = mail.uid('COPY', uid, destination_folder)
    if result != "OK":
        logging.error("Failed to move message to folder")
        raise TypeError


def remove_message_from_folder(mail, uid, folder):
    return edit_flag_modified(mail, folder="Inbox", email_uid=uid, flag="\\Deleted", put_or_quit='+')



