import configparser
from tinydb import TinyDB, Query
from utils.database import DBC, EmailServer, User, Account

#Test DATABASE utils

db = DBC()

#Test EmailServer

db.insertEmailServer('Gmail','smtp.gmail.com',465,'SMTP')
EmailServer = db.searchEmailServer('Gmail','SMTP')
print('['+EmailServer.getName()+']\nHost: '+EmailServer.getHost()+'\nPort: '+str(EmailServer.getPort())+
      '\nProtocol: '+EmailServer.getProtocol())
EmailServer.setPort(468)
db.updateEmailServer(EmailServer)
EmailServer = db.searchEmailServer('Gmail','SMTP')
print('['+EmailServer.getName()+']\nHost: '+EmailServer.getHost()+'\nPort: '+str(EmailServer.getPort())+
      '\nProtocol: ' + EmailServer.getProtocol())
db.removeEmailServer('Gmail','SMTP')
