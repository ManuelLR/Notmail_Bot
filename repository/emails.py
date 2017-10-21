
Emails = dict()


def get_emails_servers():
    return Emails


def add_email_server(key, value):
    Emails[key] = value
