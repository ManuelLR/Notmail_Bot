import sched
import time
import imaplib
import email
import smtplib
import logging
import datetime

import os, sys
import pytz
import configparser
from email.header import decode_header



scheduler = sched.scheduler(time.time, time.sleep)

refresh_inbox = 3 * 60
# refresh_inbox = 3 * 5
SMTP_SERVER = None
SMTP_SERVER_PORT = None
FROM_EMAIL = None
FROM_PWD = None

Emails = dict()
Bot_2 = None


def init_2(bot):
    global Bot_2
    Bot_2 = bot

    email_check()


def email_check():
#    global SMTP_SERVER, SMTP_SERVER_PORT, FROM_EMAIL, FROM_PWD
    Config = configparser.ConfigParser()
    Config.read('config' + '/' + 'myconfig.ini')
    SMTP_SERVER = Config.get("email test", "SMTP_SERVER")
    SMTP_SERVER_PORT = Config.get("email test", "SMTP_SERVER_PORT")
    FROM_EMAIL = Config.get("email test", "FROM_EMAIL")
    FROM_PWD = Config.get("email test", "FROM_PWD")

    if FROM_EMAIL in Emails and Emails[FROM_EMAIL].check_alive():
        email = Emails[FROM_EMAIL]
    else:
        email = Email(SMTP_SERVER, SMTP_SERVER_PORT, FROM_EMAIL, FROM_PWD)
        Emails[FROM_EMAIL] = email

    email.read_email_from_gmail()
    scheduler.enter(refresh_inbox, 1, email_check)
    scheduler.run()


def send_telegram(msg):
    Config = configparser.ConfigParser()
    Config.read('config' + '/' + 'myconfig.ini')
    id_user = Config.get("Telegram", "ADMIN_ID")
    email_date = email.utils.parsedate_to_datetime(msg['date'])
    email_from_, encoding = decode_header(msg['from'])[0]
    try:
        email_from = email_from_.decode('utf-8')
    except:
        email_from = str(email_from_)
    email_subject_, encoding = decode_header(msg['subject'])[0]
    try:
        email_subject = email_subject_.decode('utf-8')
    except:
        email_subject = str(email_subject_)

    logging.error(id_user)
    Bot_2.send_message(chat_id=id_user, parse_mode="Markdown",
                       text="*"+email_subject + "*\n[" + email_from + "]\n(_" + str(email_date)+"_)")


class Email:
    def __init__(self, smtp_server, smtp_port, email, password, last_message_time=None):
        self.__smtp_server = smtp_server
        self.__smtp_port = smtp_port
        self.__email = email
        self.__password = password
        if last_message_time is None:
            timezone = pytz.timezone('Europe/Madrid')
    #        self.lastScan = datetime.datetime.now(timezone) - datetime.timedelta(days=2)
            self.lastScan = datetime.datetime.now(timezone) - datetime.timedelta(minutes=15)
        else:
            self.lastScan = last_message_time

        self.mail = imaplib.IMAP4_SSL(self.__smtp_server, self.__smtp_port)
        self.mail.login(self.__email, self.__password)

    def read_email_from_gmail(self):
        logging.debug("Checking emails from account: " + self.__email)
        unread = []
        try:
            self.mail.select('inbox')
            type, data = self.mail.search(None, 'ALL')
#            type, data = mail.search(None, 'UnSeen')
            mail_ids = data[0]

            id_list = mail_ids.split()
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])

            for i in range(latest_email_id, first_email_id, -1):
                msg = self.get_email(str(i))
                msg_date = email.utils.parsedate_to_datetime(msg['date'])
                if msg_date <= self.lastScan:
                    break
                else:
                    unread.append(msg)
                    send_telegram(msg)

            if len(unread) > 0:
                logging.debug("There are " + str(len(unread)) + " news emails !")
                self.lastScan = email.utils.parsedate_to_datetime(unread[0]['date'])
            else:
                logging.debug("No news emails !")

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            logging.error(e)

    def get_email(self, id):
        typ, data = self.mail.fetch(id, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                # msg = email.message_from_string(response_part[1].decode('utf-8'))
                email_subject = msg['subject']
                email_date = msg['date']
                # email_from = msg['from']
                logging.debug('(' + str(id) + ')-[' + email_date + ']______Subject : ' + email_subject[:30] + '')
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

    def check_alive(self):
        try:
            status = self.mail.noop()[0]
            logging.debug("Connection status: " + str(status))
        except:  # smtplib.SMTPServerDisconnected
            status = -1
        return True if status == "OK" else False
