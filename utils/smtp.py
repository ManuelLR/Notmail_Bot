import imaplib
import logging

def connect(smtp_server, smtp_port, email, password):
    mail = imaplib.IMAP4_SSL(smtp_server, smtp_port)
    mail.login(email, password)
    return mail


def get_email(mail, id):
    typ, data = mail.fetch(id, '(RFC822)')
    return process_mails(mail, data)


def get_email_uid(mail, uid):
    typ, data = mail.fetch(uid, 'UID')
    return process_mails(mail, data)


def process_mails(mail, data):
    for response_part in data:
        if isinstance(response_part, tuple):
            msg = mail.message_from_bytes(response_part[1])
            # msg = email.message_from_string(response_part[1].decode('utf-8'))
            email_subject = msg['subject']
            email_date = msg['date']
            # email_from = msg['from']
            logging.debug('(' + str(id) + ')-[' + email_date + ']______Subject : ' + email_subject[:30] + '')
            return msg