from tinydb import TinyDB, Query
import os


def parseAccountsToJson(accounts):
    json = []
    for acc in accounts:
        account = {}
        account['name'] = acc.getName()
        account['username'] = acc.getUsername()
        account['password'] = acc.getPassword()
        account['refresh_time'] = acc.getRefresh_Time()
        json.append(account)
    return json

def parseJsonToAccounts(accounts):
    result = []
    for acc in accounts:
        account = Account(acc['name'],acc['username'],acc['password'],acc['refresh_time'])
        result.append(account)
    return result

class DBC:
    def __init__(self, path=None):
        if path is None:
            self.__db = TinyDB(os.path.join('..', 'config', 'tmail-bot.json'))
        else:
            self.__db = TinyDB(path)

    def getTable(self, tableName):
        return self.__db.table(tableName)

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


class EmailServer:
    def __init__(self, name, host, port, protocol):
        self.__name = name
        self.__host = host
        self.__port = port
        self.__protocol = protocol

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def getHost(self):
        return self.__host

    def setHost(self, host):
        self.__host = host

    def getPort(self):
        return self.__port

    def setPort(self, port):
        self.__port = port

    def getProtocol(self):
        return self.__protocol

    def setProtocol(self, protocol):
        self.__protocol = protocol

class User:
    def __init__(self, id, accounts):
        self.__id = id
        self.__accounts = accounts

    def getId(self):
        return self.__id

    def getAccounts(self):
        return self.__accounts

    def addAccount(self, account):
        self.__accounts.append(account)

    def updateAccount(self, account):
        i = 0
        for acc in self.__accounts:
            if acc.getName() == account.getName():
                self.__accounts[i] = account
                break
            i = i + 1

    def removeAccount(self, account):
        i = 0
        for acc in self.__accounts:
            if acc.getName() == account.getName():
                self.__accounts.pop(i)
                break
            i = i + 1

class Account:
    def __init__(self, name, username, password, refresh_time=None):
        self.__name = name
        self.__username = username
        self.__password = password
        if refresh_time==None:
            self.__refresh_time = 3 * 5
        else:
            self.__refresh_time = refresh_time

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def getUsername(self):
        return self.__name

    def setUsername(self, username):
        self.__username = username

    def getPassword(self):
        return self.__password

    def setPassword(self, password):
        self.__password = password

    def getRefresh_Time(self):
        return self.__refresh_time

    def setRefresh_Time(self, refresh_time):
        self.__refresh_time = refresh_time

