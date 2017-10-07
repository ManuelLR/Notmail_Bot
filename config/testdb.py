import os

from repository.repository import DBC
from repository.Account import Account, parseAccountsToJson

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

#Test User

account1 = Account('Gmail','test@gmail.com','mypass',None)
account2 = Account('Outlook','test@outlook.com','mypass',25)
accounts = [account1,account2]
db.insertUser('123456789',accounts)
User = db.searchUser('123456789')
print('\n['+User.getId()+']\nAccounts: '+str(parseAccountsToJson(User.getAccounts())))
db.removeUser('123456789')

#Test Accounts

account3 = Account('Gmail','test@gmail.com','mypass',None)
account4 = Account('Outlook','test@outlook.com','mypass',25)
accounts = [account3]
db.insertUser('123456789',accounts)
User1 = db.searchUser('123456789')
print('\n['+User1.getId()+']\nAccounts: '+str(parseAccountsToJson(User1.getAccounts())))
db.addAccountToUser(User,account4)
User1 = db.searchUser('123456789')
print('\n['+User1.getId()+']\nAccounts: '+str(parseAccountsToJson(User1.getAccounts())))
account4 = Account('Outlook','test@outlook.com','mypass',35)
db.updateAccountOfUser(User,account4)
User1 = db.searchUser('123456789')
print('\n['+User1.getId()+']\nAccounts: '+str(parseAccountsToJson(User1.getAccounts())))
db.removeAccountOfUser(User,account4)
User1 = db.searchUser('123456789')
print('\n['+User1.getId()+']\nAccounts: '+str(parseAccountsToJson(User1.getAccounts())))
db.removeUser('123456789')