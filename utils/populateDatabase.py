import os
from configparser import ConfigParser
from utils.database import Account, DBC

def populateDatabase():
    db = DBC(os.path.join('..','config', 'tmail-bot.json'))
    db.purge()
    config = ConfigParser()
    config.read(os.path.join('..', 'config', 'myconfig.ini'))
    db.insertEmailServer('Test',config['email test']['SMTP_SERVER'],config['email test']['SMTP_SERVER_PORT'],'SMTP')
    account = Account('Test',config['email test']['FROM_EMAIL'],config['email test']['FROM_PWD'],None)
    db.insertUser(config['Telegram']['ADMIN_ID'],[account])

populateDatabase()
