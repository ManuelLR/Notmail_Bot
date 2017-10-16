import logging
import os
from configparser import ConfigParser

from repository.repository import DBC
from config.loadConfig import get_config

refresh_inbox = 3 * 5


class UserContent:
    def __init__(self):
        self.messages = dict()

    def add_email(self, smtp_server, smtp_server_port, from_email, from_pwd, refresh_time=refresh_inbox):
        self.messages[from_email] = MessageContent(smtp_server, smtp_server_port, from_email, from_pwd, refresh_time=refresh_time)


class MessageContent:
    def __init__(self, smtp_server, smtp_server_port, from_email, from_pwd, refresh_time=refresh_inbox):
        self.smtp_server = smtp_server
        self.smtp_server_port = smtp_server_port
        self.from_email = from_email
        self.from_pwd = from_pwd
        self.refresh_time = refresh_time


def insert(key, value):
#    db.set(key, value)
    logging.error("Not implemented")


def get_all():

    # Retrieve configuration from Database (Do not forgot run "PopulateDatabase" first)
    db = DBC()
    email_server = db.search_email_server('Test', 'SMTP')
    smtp_server = email_server.host
    smtp_server_port = email_server.port
    user = db.search_user(get_config().telegram_admin_user_id)
    from_email = user.accounts[0].username
    from_pwd = user.accounts[0].password

    admin_id = user.id

    u_content = UserContent()
    u_content.add_email(smtp_server, smtp_server_port, from_email, from_pwd)
    result = {
        admin_id: u_content
    }
    # return None
    return result


def get(key):
    return None


def get_message_content(user, email):
#    return db.get(user)[email]
    config = ConfigParser()
    config.read(os.path.join('config', 'myconfig.ini'))
    smtp_server = config['email test']['SMTP_SERVER']
    smtp_server_port = config['email test']['SMTP_SERVER_PORT']
    from_email = config['email test']['FROM_EMAIL']
    from_pwd = config['email test']['FROM_PWD']
    admin_id = config['Telegram']['ADMIN_ID']
    result = MessageContent(smtp_server, smtp_server_port, from_email, from_pwd)
    return result
    # return None


def set_last_message_time(user, email, time):
    logging.error("Not implemented")

Emails = dict()


def get_emails_servers():
    return Emails


def add_email_server(key, value):
    Emails[key] = value
