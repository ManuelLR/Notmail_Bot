import os
from tinydb import TinyDB, Query
from repository.EmailServer import EmailServer
from repository.User import User
from repository.Account import parseAccountsToJson,parseJsonToAccounts

class DBC:
    def __init__(self, path=None):
        if path is None:
            self.__db = TinyDB(os.path.join('config', 'tmail-bot.json'))
        else:
            self.__db = TinyDB(path)

    def getTable(self, tableName):
        return self.__db.table(tableName)

    def purge(self):
        self.__db.purge_tables()

    def insertEmailServer(self, name, host, port, protocol):
        EmailServers = self.__db.table('EmailServers')
        EmailServers.insert({'name':name,'host':host,'port':port,'protocol':protocol})
        return EmailServer(name, host, port, protocol)

    def searchEmailServer(self, name, protocol):
        EmailServers = self.__db.table('EmailServers')
        query = Query()
        search = EmailServers.search(query.name == name and query.protocol == protocol)
        result = eval(str(search))[0] #We suposse that names + protocol will be unique
        emailServer = EmailServer(name, result['host'], result['port'], result['protocol'])
        return emailServer

    def updateEmailServer(self, emailServer):
        EmailServers = self.__db.table('EmailServers')
        query = Query()
        EmailServers.update({'host':emailServer.getHost(),'port':emailServer.getPort()},
                                    query.name == emailServer.getName() and query.protocol == emailServer.getProtocol())

    def removeEmailServer(self, name, protocol):
        EmailServers = self.__db.table('EmailServers')
        query = Query()
        EmailServers.remove(query.name == name and query.protocol == protocol)

    def insertUser(self, id, accounts):
        Users = self.__db.table('Users')
        Users.insert({'id': id, 'accounts':parseAccountsToJson(accounts)})
        return User(id, accounts)

    def searchUser(self, id):
        Users = self.__db.table('Users')
        query = Query()
        search = Users.search(query.id == id)
        result = eval(str(search))[0]
        user = User(id, parseJsonToAccounts(result['accounts']))
        return user

    def updateUser(self, user):
        Users = self.__db.table('Users')
        query = Query()
        Users.update({'id': user.getId(), 'accounts':parseAccountsToJson(user.getAccounts())},
                                    query.id == user.getId())

    def removeUser(self, id):
        Users = self.__db.table('Users')
        query = Query()
        Users.remove(query.id == id)

    def getAccountsOfUser(self, user):
        user = self.searchUser(user.getId())
        return user.getAccounts()

    def addAccountToUser(self, user, account):
        user = self.searchUser(user.getId())
        user.addAccount(account)
        self.updateUser(user)

    def updateAccountOfUser(self, user, account):
        user = self.searchUser(user.getId())
        user.updateAccount(account)
        self.updateUser(user)

    def removeAccountOfUser(self, user, account):
        user = self.searchUser(user.getId())
        user.removeAccount(account)
        self.updateUser(user)

    def getEmailServerOfAccount(self, account, protocol):
        emailServer = self.searchEmailServer(account.getName(), protocol)
        return emailServer