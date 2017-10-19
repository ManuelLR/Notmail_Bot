import imaplib
import logging
import os, sys
import email as email_lib
from email.header import decode_header

imaplib._MAXLINE = 100000

class Message:
    def __init__(self, msg, flags=None):
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
                if isinstance(input_mod, bytes):
                    result = input_mod.decode()
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

    def get_body(self, format='text'):
        maintype = self.msg.get_content_maintype()
        if maintype == 'multipart':
            for part in self.msg.get_payload():
                if part.get_content_maintype() == format:
                    return part.get_payload(decode=True).decode("utf-8")
        elif maintype == 'text':
            return self.msg.get_payload()


class Folder:
    def __init__(self, raw_folder):
        split1 = raw_folder.decode().split(' \"/\"')
        name = split1[1].replace(' \"', '').replace('\"', '')
        self.flags = split1[0]
        self.name = name


def connect(smtp_server, smtp_port, email, password):
    mail = imaplib.IMAP4_SSL(smtp_server, smtp_port)
    mail.login(email, password)
    return mail


def get_email_by_uid(mail, folder, uid):
    mail.select(folder, readonly=True)
    typ, data = mail.uid('FETCH', uid, '(FLAGS RFC822)')
    # typ, data = mail.uid('FETCH', uid, '(RFC822)')
    if typ != "OK" or len(data) < 2:
        logging.debug("Error retrieving :" + str(folder) + "  __@" + str(uid))
        return

    return Message(data[0], data[1])


# Sorted from oldest(0) to newest(-1)
def get_uid_list(mail, folder):
    mail.select(folder, readonly=True)  # Don't mark message as read

    try:
        type, data = mail.uid('search', None, "ALL")  # search and return uids instead
        #            type, data = mail.search(None, 'UnSeen')
        mail_uids = data[0].split()

        return mail_uids, None

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        logging.error(e)
        return [], e


def change_flags(mail, folder, email_uid, flag, put_or_quit):
    mail.select(folder, readonly=False)

    if put_or_quit not in ['+', '-']:
        logging.fatal("Incorrect flag!")

    # logging.info(email_uid + ':' + put_or_quit + ':' + flag)
    # mail.select(folder)
    logging.info(email_uid)
    typ, data = mail.uid('STORE', email_uid, put_or_quit+'FLAGS', '\\'+flag)
    logging.info(data)
    if typ != 'OK':
        logging.error("Failed to apply " + str(put_or_quit) + "FLAGS " + flag)


def edit_flag_modified(mail, folder, email_uid, flag, put_or_quit):
    if put_or_quit not in ['+', '-']:
        logging.fatal("Incorrect flag!")

    # logging.info(email_uid + ':' + put_or_quit + ':' + flag)
    mail.select(folder, readonly=False)
    logging.info("In edit_flag_modified")
    logging.info(email_uid)
    typ, data = mail.uid('STORE', email_uid, put_or_quit + 'FLAGS', flag)
    logging.info(data)
    if typ != 'OK':
        logging.error("Failed to apply " + str(put_or_quit) + "FLAGS " + flag)
    mail.select(folder, readonly=False)


def get_folders(mail):
    typ, data = mail.list('""', '*')
    result = []
    if typ != "OK":
        logging.error("Failed to list the folders")
        return None
    for mbox in data:
        result.append(Folder(mbox))

    return result


def add_message_to_folder(mail, uid, destination_folder):
    result = mail.uid('COPY', uid, destination_folder)
    if result != "OK":
        logging.error("Failed to move message to folder")
        raise TypeError


def remove_message_from_folder(mail, uid, folder):
    return edit_flag_modified(mail, folder="Inbox", email_uid=uid, flag="\\Deleted", put_or_quit='+')



