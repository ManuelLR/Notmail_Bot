import os

from repository.repository import DBC

#Test DATABASE utils

db = DBC(os.path.join('..','config', 'tmail-bot.json'))

#Test EmailServer

db.insert_email_server('Gmail', 'smtp.gmail.com', 465, 'SMTP')
EmailServer = db.search_email_server('Gmail', 'SMTP')
print('\n['+EmailServer.name+']\nHost: '+EmailServer.host+'\nPort: '+str(EmailServer.port)+
      '\nProtocol: '+EmailServer.protocol)
EmailServer.port = 468
db.update_email_server(EmailServer)
EmailServer = db.search_email_server('Gmail', 'SMTP')
print('\n['+EmailServer.name+']\nHost: '+EmailServer.host+'\nPort: '+str(EmailServer.port)+
      '\nProtocol: ' + EmailServer.protocol)
db.remove_email_server('Gmail', 'SMTP')
