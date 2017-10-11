import os

from repository.repository import DBC

#Test DATABASE utils

db = DBC(os.path.join('..','config', 'tmail-bot.json'))

#Test EmailServer

db.insertEmailServer('Gmail','smtp.gmail.com',465,'SMTP')
EmailServer = db.searchEmailServer('Gmail','SMTP')
print('\n['+EmailServer.getName()+']\nHost: '+EmailServer.getHost()+'\nPort: '+str(EmailServer.getPort())+
      '\nProtocol: '+EmailServer.getProtocol())
EmailServer.setPort(468)
db.updateEmailServer(EmailServer)
EmailServer = db.searchEmailServer('Gmail','SMTP')
print('\n['+EmailServer.getName()+']\nHost: '+EmailServer.getHost()+'\nPort: '+str(EmailServer.getPort())+
      '\nProtocol: ' + EmailServer.getProtocol())
db.removeEmailServer('Gmail','SMTP')
