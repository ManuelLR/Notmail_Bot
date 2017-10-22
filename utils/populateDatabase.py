# Copyright 2017 by Notmail Bot contributors. All rights reserved.
#
# This file is part of Notmail Bot.
#
#     Notmail Bot is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Notmail Bot is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Notmail Bot.  If not, see <http:#www.gnu.org/licenses/>.
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
                      config['email test']['SMTP_SERVER'],config['email test']['SMTP_SERVER_PORT'], 'IMAP',180)
    db.insert_user(config['Telegram']['ADMIN_ID'], [account])



populateDatabase()
