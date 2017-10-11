import os

from repository.repository import DBC
from repository.Account import Account, parseAccountsToJson

db = DBC(os.path.join('..','config', 'tmail-bot.json'))

#Test Accounts

account1 = Account('Gmail','test@gmail.com','mypass',None)
account2 = Account('Outlook','test@outlook.com','mypass',25)
accounts = [account1,account2]
db.insertUser('123456789',accounts)
User = db.searchUser('123456789')
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