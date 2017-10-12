import os

from repository.repository import DBC
from repository.Account import Account, parseAccountsToJson

#Test DATABASE utils

db = DBC(os.path.join('..','config', 'tmail-bot.json'))


#Test User

account1 = Account('Gmail','test@gmail.com','mypass',None)
account2 = Account('Outlook','test@outlook.com','mypass',25)
accounts = [account1,account2]
db.insertUser('123456789',accounts)
User = db.searchUser('123456789')
print('\n['+User.getId()+']\nAccounts: '+str(parseAccountsToJson(User.getAccounts())))
db.removeUser('123456789')