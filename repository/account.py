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
from config.loadConfig import get_config


def parse_accounts_to_json(accounts):
    json = []
    for acc in accounts:
        account = {'name': acc.name, 'username': acc.username, 'password': acc.password, 'host': acc.host,
                   'port': acc.port, 'protocol': acc.protocol, 'refresh_time': acc.refresh_time}
        json.append(account)
    return json


def parse_json_to_accounts(accounts):
    result = []
    for acc in accounts:
        account = Account(acc['name'],acc['username'],acc['password'], acc['host'], acc['port'],
                          acc['protocol'], acc['refresh_time'])
        result.append(account)
    return result


class Account:
    def __init__(self, name, username, password, host, port, protocol, refresh_time=None):
        self.name = name
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.protocol = protocol
        if refresh_time is None:
            self.refresh_time = get_config().default_refresh_inbox
        else:
            self.refresh_time = refresh_time
