import os
from tinydb import TinyDB, Query
from repository.EmailServer import EmailServer
from repository.User import User
from repository.Account import parseAccountsToJson,parseJsonToAccounts

class DBC:
    def __init__(self, path=None):
        if path is None:
            self.db = TinyDB(os.path.join('config', 'tmail-bot.json'))
        else:
            self.db = TinyDB(path)

    def getTable(self, tableName):
        return self.db.table(tableName)

    def purge(self):
        self.db.purge_tables()

    def insertEmailServer(self, name, host, port, protocol):
        EmailServers = self.db.table('EmailServers')
        EmailServers.insert({'name':name,'host':host,'port':port,'protocol':protocol})
        return EmailServer(name, host, port, protocol)

    def searchEmailServer(self, name, protocol):
        EmailServers = self.db.table('EmailServers')
        query = Query()
        search = EmailServers.search(query.name == name and query.protocol == protocol)
        result = eval(str(search))[0] #We suposse that names + protocol will be unique
        emailServer = EmailServer(name, result['host'], result['port'], result['protocol'])
        return emailServer

    def updateEmailServer(self, emailServer):
        EmailServers = self.db.table('EmailServers')
        query = Query()
        EmailServers.update({'host':emailServer.host,'port':emailServer.port},
                                    query.name == emailServer.name and query.protocol == emailServer.protocol)

    def removeEmailServer(self, name, protocol):
        EmailServers = self.db.table('EmailServers')
        query = Query()
        EmailServers.remove(query.name == name and query.protocol == protocol)

    def insertUser(self, id, accounts):
        Users = self.db.table('Users')
        Users.insert({'id': id, 'accounts':parseAccountsToJson(accounts)})
        return User(id, accounts)

    def searchUser(self, id):
        Users = self.db.table('Users')
        query = Query()
        search = Users.search(query.id == id)
        result = eval(str(search))[0]
        user = User(id, parseJsonToAccounts(result['accounts']))
        return user

    def updateUser(self, user):
        Users = self.db.table('Users')
        query = Query()
        Users.update({'id': user.id, 'accounts':parseAccountsToJson(user.accounts)},
                                    query.id == user.id)

    def removeUser(self, id):
        Users = self.db.table('Users')
        query = Query()
        Users.remove(query.id == id)

    def getAccountsOfUser(self, user):
        user = self.searchUser(user.id)
        return user.accounts

    def addAccountToUser(self, user, account):
        user = self.searchUser(user.id)
        user.addAccount(account)
        self.updateUser(user)

    def updateAccountOfUser(self, user, account):
        user = self.searchUser(user.id)
        user.updateAccount(account)
        self.updateUser(user)

    def removeAccountOfUser(self, user, account):
        user = self.searchUser(user.id)
        user.removeAccount(account)
        self.updateUser(user)

    def getEmailServerOfAccount(self, account, protocol):
        emailServer = self.searchEmailServer(account.name, protocol)
        return emailServer