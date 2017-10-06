import repository.emails as email_repo
import utils.smtp as email_util
import sched
import time
import logging
import datetime
import pytz
import email
from email.header import decode_header


scheduler = sched.scheduler(time.time, time.sleep)

# refresh_inbox = 3 * 60
refresh_inbox = 3 * 5
Bot_2 = None
Emails = dict()


def init_email_service(bot):
    global Bot_2
    Bot_2 = bot
    email_repo_all = email_repo.get_all()

    if not email_repo_all:
        return

    for user, u_content in email_repo_all.items():
        for email, m_content in u_content.messages.items():
            Emails[email] = EmailServer(user, email)
            Emails[email].check()


class EmailServer:
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
        logging.debug("Reconnecting account: " + self.__user)
        message_content = email_repo.get_message_content(self.__user, self.__email)
        self.mail = email_util.connect(message_content.smtp_server, message_content.smtp_server_port,
                               message_content.from_email, message_content.from_pwd)

    def check(self):
        logging.debug("Checking account: " + self.__user)
        if not self.__check_alive():
            self.__connect()

        self.read_email_from_gmail()
        scheduler.enter(refresh_inbox, 1, self.check)
        scheduler.run()

    def read_email_from_gmail(self):
        self.lastScan, unread = email_util.read_emails(self.mail, 'inbox', self.lastScan)

        for m in unread:
            send_telegram(m)

    def get_email(self, id):
        if not self.__check_alive():
            self.__connect()
        return email_util.get_email(self.mail, id)

    def get_email_uid(self, uid):
        if not self.__check_alive():
            self.__connect()
        return email_util.get_email_uid(self.mail, uid)

    def __check_alive(self):
        try:
            status = self.mail.noop()[0]
            # logging.debug("Connection status: " + str(status))
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
