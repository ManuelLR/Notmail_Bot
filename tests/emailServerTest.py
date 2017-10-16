import os

from repository.repository import DBC

#Test DATABASE utils

db = DBC(os.path.join('..','config', 'tmail-bot.json'))

#Test EmailServer

db.insertEmailServer('Gmail','smtp.gmail.com',465,'SMTP')
EmailServer = db.searchEmailServer('Gmail','SMTP')
print('\n['+EmailServer.name+']\nHost: '+EmailServer.host+'\nPort: '+str(EmailServer.port)+
      '\nProtocol: '+EmailServer.protocol)
EmailServer.port = 468
db.updateEmailServer(EmailServer)
EmailServer = db.searchEmailServer('Gmail','SMTP')
print('\n['+EmailServer.name+']\nHost: '+EmailServer.host+'\nPort: '+str(EmailServer.port)+
      '\nProtocol: ' + EmailServer.protocol)
db.removeEmailServer('Gmail','SMTP')
