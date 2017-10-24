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
from repository.account import Account, parse_accounts_to_json

# Test DATABASE utils

db = DBC(os.path.join('..', 'config', 'tmail-bot.json'))

# Test User

account1 = Account('Gmail', 'test@gmail.com', 'mypass', 'test.com', 465, 'IMAP', 15)
account2 = Account('Outlook', 'test@outlook.com', 'mypass', 'test.com', 465, 'IMAP', 25)
accounts = [account1, account2]
db.insert_user('123456789', accounts)
User = db.search_user('123456789')
print('\n[' + User.id + ']\nAccounts: ' + str(parse_accounts_to_json(User.accounts)))
db.remove_user('123456789')