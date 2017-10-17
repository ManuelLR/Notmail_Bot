import os

from repository.repository import DBC
from repository.account import Account, parse_accounts_to_json

# Test DATABASE utils

db = DBC(os.path.join('..', 'config', 'tmail-bot.json'))

# Test User

account1 = Account('Gmail', 'test@gmail.com', 'mypass', 'test.com', 465, None)
account2 = Account('Outlook', 'test@outlook.com', 'mypass', 'test.com', 465, 25)
accounts = [account1, account2]
db.insert_user('123456789', accounts)
User = db.search_user('123456789')
print('\n[' + User.id + ']\nAccounts: ' + str(parse_accounts_to_json(User.accounts)))
db.remove_user('123456789')
