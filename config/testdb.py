import configparser
from tinydb import TinyDB, Query
from utils.database import DBC, SMTPServer, User, Account

#Test DATABASE utils

db = DBC()

#Test SMTPServer

db.insertSMTPServer('Gmail','smtp.gmail.com',465)
SMTPServer = db.searchSMTPServer('Gmail')
print('['+SMTPServer.getName()+']\nHost: '+SMTPServer.getHost()+'\nPort: '+str(SMTPServer.getPort()))
SMTPServer.setPort(468)
db.updateSMTPServer(SMTPServer)
SMTPServer = db.searchSMTPServer('Gmail')
print('['+SMTPServer.getName()+']\nHost: '+SMTPServer.getHost()+'\nPort: '+str(SMTPServer.getPort()))
db.removeSMTPServer('Gmail')
