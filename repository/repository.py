import os
from tinydb import TinyDB, Query
from repository.email_server import EmailServer
from repository.user import User
from repository.account import parse_accounts_to_json, parse_json_to_accounts


class DBC:
    def __init__(self, path=None):
        if path is None:
            self.db = TinyDB(os.path.join('config', 'tmail-bot.json'))
        else:
            self.db = TinyDB(path)

    def get_table(self, table_name):
        return self.db.table(table_name)

    def purge(self):
        self.db.purge_tables()

    def insert_email_server(self, name, host, port, protocol):
        email_servers = self.db.table('EmailServers')
        email_servers.insert({'name': name, 'host': host, 'port': port, 'protocol': protocol})
        return EmailServer(name, host, port, protocol)

    def search_email_server(self, name, protocol):
        email_servers = self.db.table('EmailServers')
        query = Query()
        search = email_servers.search(query.name == name and query.protocol == protocol)
        result = eval(str(search))[0]  # We suppose that names + protocol will be unique
        email_server = EmailServer(name, result['host'], result['port'], result['protocol'])
        return email_server

    def update_email_server(self, email_server):
        email_servers = self.db.table('EmailServers')
        query = Query()
        email_servers.update({'host': email_server.host, 'port': email_server.port},
                             query.name == email_server.name and query.protocol == email_server.protocol)

    def remove_email_server(self, name, protocol):
        email_servers = self.db.table('EmailServers')
        query = Query()
        email_servers.remove(query.name == name and query.protocol == protocol)

    def insert_user(self, id, accounts):
        users = self.db.table('Users')
        users.insert({'id': id, 'accounts': parse_accounts_to_json(accounts)})
        return User(id, accounts)

    def search_user(self, id):
        users = self.db.table('Users')
        query = Query()
        search = users.search(query.id == id)
        result = eval(str(search))[0]
        user = User(id, parse_json_to_accounts(result['accounts']))
        return user

    def update_user(self, user):
        users = self.db.table('Users')
        query = Query()
        users.update({'id': user.id, 'accounts': parse_accounts_to_json(user.accounts)},
                     query.id == user.id)

    def get_all_users(self):
        users = self.db.table('Users')
        res = []
        for a in users.all():
            res.append(User(a['id'], a['accounts']))
        return res

    def remove_user(self, user_id):
        users = self.db.table('Users')
        query = Query()
        users.remove(query.id == user_id)

    def get_accounts_of_user(self, user):
        user = self.search_user(user.id)
        return user.accounts

    def add_account_to_user(self, user, account):
        user = self.search_user(user.id)
        user.add_account(account)
        self.update_user(user)

    def update_account_of_user(self, user, account):
        user = self.search_user(user.id)
        user.update_account(account)
        self.update_user(user)

    def remove_account_of_user(self, user, account):
        user = self.search_user(user.id)
        user.remove_account(account)
        self.update_user(user)

    def get_email_server_of_account(self, account, protocol):
        email_server = self.search_email_server(account.name, protocol)
        return email_server
