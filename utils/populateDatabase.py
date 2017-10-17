import os
from configparser import ConfigParser

from repository.repository import DBC
from repository.account import Account

def populateDatabase():
    db = DBC(os.path.join('..','config', 'tmail-bot.json'))
    db.purge()
    config = ConfigParser()
    config.read(os.path.join('..', 'config', 'myconfig.ini'))
    db.insert_email_server('Test', config['email test']['SMTP_SERVER'], config['email test']['SMTP_SERVER_PORT'], 'SMTP')
    account = Account('Test',config['email test']['FROM_EMAIL'],config['email test']['FROM_PWD'],
                      config['email test']['SMTP_SERVER_PORT'], 'SMTP',None)
    db.insert_user(config['Telegram']['ADMIN_ID'], [account])

populateDatabase()
