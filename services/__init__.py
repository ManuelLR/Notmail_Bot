
bot = None
emailsServices = dict()

def get_bot():
    return bot

def set_bot(inp):
    global bot
    bot = inp


def get_emails_servers():
    return emailsServices

def get_email_server(inp):
    return emailsServices[inp]

def add_email_server(key, value):
    emailsServices[key] = value

