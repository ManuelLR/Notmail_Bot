import logging

refresh_inbox = 3 * 5


class UserContent:
    def __init__(self):
        self.messages = []

    def add_email(self, smtp_server, smtp_server_port, from_email, from_pwd, refresh_time=refresh_inbox):
        self.messages.append(MessageContent(smtp_server, smtp_server_port, from_email, from_pwd, refresh_time=refresh_time))


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
    return None


def get(key):
    return None


def get_message_content(user, email):
#    return db.get(user)[email]
    return None


def set_last_message_time(user, email, time):
    logging.error("Not implemented")
