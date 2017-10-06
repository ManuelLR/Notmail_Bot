import imaplib
import logging
import os, sys
import email.utils as email_util
import email as email
from email.header import decode_header
from urllib.parse import unquote

class Message:
    def __init__(self, msg):
        self.msg = msg

    @staticmethod
    def __fix_string(input):
        res = ""
        for input_mod, encoding in decode_header(input):
            try:
                if isinstance(input_mod, bytes):
                    result = input_mod.decode()
                else:
                    result = input_mod.decode(encoding)
            except:
                result = str(input_mod)
            res = res + result + " "
        return res

    def get_header(self, property):
        return self.__fix_string(self.msg[property])

    def get_body(self, format='text'):
        maintype = self.msg.get_content_maintype()
        if maintype == 'multipart':
            for part in self.msg.get_payload():
                if part.get_content_maintype() == format:
                    return part.get_payload(decode=True).decode("utf-8")
        elif maintype == 'text':
            return self.msg.get_payload()


def connect(smtp_server, smtp_port, email, password):
    mail = imaplib.IMAP4_SSL(smtp_server, smtp_port)
    mail.login(email, password)
    return mail


def get_email_by_uid(mail, uid):
    typ, data = mail.uid('FETCH', uid, '(RFC822)')
    return process_mails(mail, data)


def process_mails(mail, data):
    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            # msg = email.message_from_string(response_part[1].decode())
            email_subject = msg['subject']

            email_date = msg['date']
            # email_from = msg['from']
            logging.debug('(' + str(id) + ')-[' + email_date + ']______Subject : ' + email_subject[:30] + '')
            return msg


# Sorted from oldest(0) to newest(-1)
def get_uid_list(mail, folder):
    try:
        # mail.select('inbox')
        mail.select(folder, readonly=True)  # Don't mark message as read
        # mail.select('[Gmail]/All Mail', readonly=True)  # Don't mark message as read

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

