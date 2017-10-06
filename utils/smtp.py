import imaplib
import logging
import os, sys
import email.utils as email_util
import email as email


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
            msg = email.message_from_bytes(response_part[1])
            # msg = email.message_from_string(response_part[1].decode('utf-8'))
            email_subject = msg['subject']
            email_date = msg['date']
            # email_from = msg['from']
            logging.debug('(' + str(id) + ')-[' + email_date + ']______Subject : ' + email_subject[:30] + '')
            return msg


def read_emails(mail, folder, lastScan):
    logging.debug("Checking emails from account: " )  # + mail.from_email)
    unread = []
    try:
        mail.select('inbox')
        type, data = mail.search(None, 'ALL')
#            type, data = mail.search(None, 'UnSeen')
        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id, first_email_id, -1):
            msg = get_email(mail, str(i))
            msg_date = email_util.parsedate_to_datetime(msg['date'])
            if msg_date <= lastScan:
                break
            else:
                unread.append(msg)

        if len(unread) > 0:
            logging.debug("There are " + str(len(unread)) + " news emails !")
            lastScan = email_util.parsedate_to_datetime(unread[0]['date'])
        else:
            logging.debug("No news emails !")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        logging.error(e)

    return lastScan, unread
