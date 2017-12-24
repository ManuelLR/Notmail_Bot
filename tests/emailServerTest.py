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

from repository.repository import DBC

#Test DATABASE utils

db = DBC(os.path.join('..','config', 'tmail-bot.json'))

#Test EmailServer

db.insert_email_server('Gmail', 'smtp.gmail.com', 465, 'SMTP')
EmailServer = db.search_email_server('Gmail', 'IMAP')
print('\n['+EmailServer.name+']\nHost: '+EmailServer.host+'\nPort: '+str(EmailServer.port)+
      '\nProtocol: '+EmailServer.protocol)
EmailServer.port = 468
db.update_email_server(EmailServer)
EmailServer = db.search_email_server('Gmail', 'IMAP')
print('\n['+EmailServer.name+']\nHost: '+EmailServer.host+'\nPort: '+str(EmailServer.port)+
      '\nProtocol: ' + EmailServer.protocol)
db.remove_email_server('Gmail', 'IMAP')
