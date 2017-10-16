from commands.email import send_msg
import repository.emails as email_repo
import repository.repository as repository
from config.loadConfig import get_config
import utils.imap as imap_util
import sched
import time
import logging


scheduler = sched.scheduler(time.time, time.sleep)

# refresh_inbox = 3 * 60
refresh_inbox = 3 * 5
Bot_2 = None


def init_email_service(bot):
    global Bot_2
    Bot_2 = bot
    email_repo_all = email_repo.get_all()

    if not email_repo_all:
        return

    for user, u_content in email_repo_all.items():
        for email, m_content in u_content.messages.items():
            email_repo.add_email_server(email, EmailServer(user, email, "SMTP", {'inbox': None}))
            email_repo.get_emails_servers()[email].check('inbox')


class EmailServer:
    def __init__(self, id_user, email, protocol, folder_last_message_uid):
        self.__user = id_user
        self.__email = email
        self.__protocol = protocol

        self.__connect()

        self.folder_last_message_uid = dict()
        for folder, uid in folder_last_message_uid.items():
            if uid is not None:
                self.folder_last_message_uid[folder] = uid
                continue
            uids, err = imap_util.get_uid_list(self.mail, folder)
            if err is not None:
                logging.error("Error reading folder: " + str(err))
                continue
            self.folder_last_message_uid[folder] = int(uids[-2])  # for debug
            # self.folder_last_message_uid[folder] = int(uids[-1])

    def __connect(self):
        logging.debug("Reconnecting account: " + self.__user)
        db = repository.DBC(get_config().db_path)
        account = db.get_accounts_of_user(db.search_user(get_config().telegram_admin_user_id))[0]
        email_server = db.search_email_server(account.name, self.__protocol)
        # message_content = email_repo.get_message_content(self.__user, self.__email)
        self.mail = imap_util.connect(email_server.host, email_server.port,
                                      account.username, account.password)
        self.mail.select('inbox')

    def check(self, folder):
        logging.debug("Checking account: " + self.__email + ":/" + folder)
        if not self.__check_alive():
            self.__connect()

        self.read_email_from_gmail(folder)
        scheduler.enter(refresh_inbox, 1, self.check, kwargs={'folder': folder})
        scheduler.run()

    def read_email_from_gmail(self, folder):
        uids, err = imap_util.get_uid_list(self.mail, 'inbox')
        logging.info("Emails in folder: " + str(len(uids)))
        if len(uids) < 1:
            return
        most_recent_uid = int(uids[-1])

        if most_recent_uid == self.folder_last_message_uid[folder]:
            return

        uids_truncated = []
        for uid in reversed(uids):
            if int(uid) <= self.folder_last_message_uid[folder]:
                break
            uids_truncated.append(uid)

        for uid in reversed(uids_truncated):
            send_msg(Bot_2, self.__user, self.__email, folder, uid)
        self.folder_last_message_uid[folder] = most_recent_uid

    def mark_as_read(self, folder, uid, mark_as_read=True):
        if not self.__check_alive():
            self.__connect()
        put_or_quit = '+'
        if not mark_as_read:
            put_or_quit = '-'
        imap_util.change_flags(self.mail, folder, uid, flag='Seen', put_or_quit=put_or_quit)

    def __get_uid_list(self, folder):
        return imap_util.get_uid_list(self.mail, folder)

    def get_email_by_uid(self, folder, uid):
        if not self.__check_alive():
            self.__connect()
        return imap_util.get_email_by_uid(self.mail, folder, uid)

    def __check_alive(self):
        try:
            status = self.mail.noop()[0]
        except:  # smtplib.SMTPServerDisconnected
            status = -1
        return True if status == "OK" else False

    def add_to_folder(self, uid, folder):
        if not self.__check_alive():
            self.__connect()
        try:
            imap_util.add_message_to_folder(self.mail, uid, folder)
        except:
            logging.error("Failed adding to folder")

    def delete_from_folder(self, uid, folder):
        if not self.__check_alive():
            self.__connect()
        try:
            imap_util.remove_message_from_folder(self.mail, uid, folder)
        except Exception as e:
            logging.error("Failed removing from folder")
            logging.error(e)

    def get_folders(self):
        if not self.__check_alive():
            self.__connect()
        return imap_util.get_folders(self.mail)
