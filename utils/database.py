from tinydb import TinyDB, Query
import os


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
        search = EmailServers.search(query.name == name)
        result = eval(str(search))[0] #We suposse that names + protocol will be unique
        emailServer = EmailServer(name, result['host'], result['port'], result['protocol'])
        return emailServer

    def updateEmailServer(self, EmailServer):
        EmailServers = self.__db.table('EmailServers')
        query = Query()
        EmailServers.update({'host':EmailServer.getHost(),'port':EmailServer.getPort()},
                                    query.name == EmailServer.getName() and query.protocol == EmailServer.getProtocol())

    def removeEmailServer(self, name, protocol):
        EmailServers = self.__db.table('EmailServers')
        query = Query()
        EmailServers.remove(query.name == name and query.protocol == protocol)

    def insertUser(self, id, accounts):
        Users = self.__db.table('Users')
        Users.insert({'id': id, 'accounts':[accounts]})
        return EmailServer(id, accounts)

    def searchUser(self, id):
        Users = self.__db.table('Users')
        query = Query()
        search = Users.search(query.id == id)
        result = eval(str(search))
        user = User(id, result['accounts'])
        return user

    def removeUser(self, id):
        Users = self.__db.table('Users')
        query = Query()
        Users.remove(query.id == id)

    def getAccountsOfUser(self, user):
        pass

    def addAccountToUser(self, user, account):
        pass

    def updateAccountOfUser(self, user, account):
        pass

    def removeAccountOfUser(self, user, account):
        pass


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

