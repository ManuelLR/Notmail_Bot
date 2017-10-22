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
class User:
    def __init__(self, id, accounts):
        self.id = id
        self.accounts = accounts

    def add_account(self, account):
        self.accounts.append(account)

    def update_account(self, account):
        i = 0
        for acc in self.accounts:
            if acc.name == account.name:
                self.accounts[i] = account
                break
            i = i + 1

    def remove_account(self, account):
        i = 0
        for acc in self.accounts:
            if acc.name == account.name:
                self.accounts.pop(i)
                break
            i = i + 1
