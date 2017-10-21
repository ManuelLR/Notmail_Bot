import os
from configparser import ConfigParser

from repository.repository import DBC
from repository.account import Account

def populateDatabase():

    # Insert Default Servers
    db = DBC(os.path.join('..', 'config', 'tmail-bot.json'))
    db.purge()
    db.insert_email_server('GMAIL','imap.gmail.com', '993', 'IMAP')
    db.insert_email_server('GMAIL', 'smtp.gmail.com', '465', 'SMTP')
    db.insert_email_server('OUTLOOK', 'pop3.live.com', '995', 'POP3')
    db.insert_email_server('OUTLOOK', 'smtp.live.com', '587', 'SMTP')

    #Insert Test Config

    config = ConfigParser()
    config.read(os.path.join('..', 'config', 'myconfig.ini'))
    db.insert_email_server('Test', config['email test']['SMTP_SERVER'], config['email test']['SMTP_SERVER_PORT']
                           , 'SMTP')
    account = Account('Test',config['email test']['FROM_EMAIL'],config['email test']['FROM_PWD'],
                      config['email test']['SMTP_SERVER'],config['email test']['SMTP_SERVER_PORT'], 'SMTP',None)
    db.insert_user(config['Telegram']['ADMIN_ID'], [account])



populateDatabase()
