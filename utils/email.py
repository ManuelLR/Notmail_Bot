import sched
import time
import imaplib
import email
import smtplib
import logging
import datetime
import pytz
import configparser

scheduler = sched.scheduler(time.time, time.sleep)

# refresh_inbox = 3 * 60
refresh_inbox = 3 * 5
SMTP_SERVER = None
SMTP_SERVER_PORT = None
FROM_EMAIL = None
FROM_PWD = None


def email_check():
#    global SMTP_SERVER, SMTP_SERVER_PORT, FROM_EMAIL, FROM_PWD
    Config = configparser.ConfigParser()
    Config.read('config' + '/' + 'myconfig.ini')
    SMTP_SERVER = Config.get("email test", "SMTP_SERVER")
    SMTP_SERVER_PORT = Config.get("email test", "SMTP_SERVER_PORT")
    FROM_EMAIL = Config.get("email test", "FROM_EMAIL")
    FROM_PWD = Config.get("email test", "FROM_PWD")

    email = Email(SMTP_SERVER, SMTP_SERVER_PORT, FROM_EMAIL, FROM_PWD)
    email.read_email_from_gmail()
    scheduler.enter(refresh_inbox, 1, email_check)
    scheduler.run()


class Email:
    def __init__(self, smtp_server, smtp_port, email, password, last_message_time=None):
        self.__smtp_server = smtp_server
        self.__smtp_port = smtp_port
        self.__email = email
        self.__password = password
        if last_message_time is None:
            timezone = pytz.timezone('Europe/Madrid')
    #        self.__lastScan = None
            self.__lastScan = datetime.datetime.now(timezone) - datetime.timedelta(minutes=15)
        else:
            self.__lastScan = last_message_time

        self.mail = imaplib.IMAP4_SSL(self.__smtp_server, self.__smtp_port)
        self.mail.login(self.__email, self.__password)
        self.mail.select('inbox')

    def read_email_from_gmail(self):
        try:
            type, data = self.mail.search(None, 'ALL')
#            type, data = mail.search(None, 'UnSeen')
            mail_ids = data[0]

            id_list = mail_ids.split()
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])

            for i in range(latest_email_id, first_email_id, -1):
                print("_______" + str(i))
                msg = self.get_email(str(i))
                msg_date = email.utils.parsedate_to_datetime(msg['date'])
                if msg_date < self.__lastScan:
                    self.__lastScan = msg_date
                    break

        except Exception as e:
            logging.error(e)

    def get_email(self, id):
        typ, data = self.mail.fetch(id, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                # msg = email.message_from_bytes(response_part[1])
                msg = email.message_from_string(response_part[1].decode('utf-8'))
                email_subject = msg['subject']
                email_date = msg['date']
                email_from = msg['from']
                print('From : ' + email_from + '_________[' + email_date + ']')
                print('Subject : ' + email_subject + '\n')
                return msg

    def get_email_uid(self, uid):
        typ, data = self.mail.fetch(uid, 'UID')
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_subject = msg['subject']
                email_from = msg['from']
                print('From : ' + email_from + '')
                print('Subject : ' + email_subject + '\n')
