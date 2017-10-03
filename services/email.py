import repository.emails as email_repo
import utils.email as email_util
import sched
import time
import logging
import datetime
import pytz
import email
from email.header import decode_header
import os, sys


scheduler = sched.scheduler(time.time, time.sleep)

# refresh_inbox = 3 * 60
refresh_inbox = 3 * 5
Bot_2 = None
Emails = dict()


def init_2(bot):
    global Bot_2
    Bot_2 = bot
    email_repo_all = email_repo.get_all()

    if not email_repo_all:
        return

    for user, u_content in email_repo_all.items():
        for email, m_content in u_content.items():
            Emails[email] = Email(user, email)


class Email:
    def __init__(self, id_user, email, last_message_time=None):
        self.__user = id_user
        self.__email = email
        if last_message_time is None:
            timezone = pytz.timezone('Europe/Madrid')
    #        self.lastScan = datetime.datetime.now(timezone) - datetime.timedelta(days=2)
            self.lastScan = datetime.datetime.now(timezone) - datetime.timedelta(minutes=15)
        else:
            self.lastScan = last_message_time

        self.__connect()

    def __connect(self):
        message_content = email_repo.get_message_content(self.user, self.email)
        self.mail = email_util(message_content.smtp_server, message_content.smtp_port,
                               message_content.email, message_content.password)

    def check(self):
        if not self.__check_alive():
            self.__connect()

        self.read_email_from_gmail()
        scheduler.enter(self.refresh_time, 1, self.check())
        scheduler.run()

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
        return email_util.get_email(self.mail, id)

    def get_email_uid(self, uid):
        return email_util.get_email_uid(self.mail, id)

    def __check_alive(self):
        try:
            status = self.mail.noop()[0]
            logging.debug("Connection status: " + str(status))
        except:  # smtplib.SMTPServerDisconnected
            status = -1
        return True if status == "OK" else False


def send_telegram(msg, id_user):
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
    msg_send = Bot_2.send_message(chat_id=id_user, parse_mode="Markdown",
                       text="*"+email_subject + "*\n[" + email_from + "]\n(_" + str(email_date)+"_)")
    return msg_send is not None
