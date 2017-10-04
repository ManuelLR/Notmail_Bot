from tinydb import TinyDB, Query

class DBC:
    def __init__(self, path=None):
        if path is None:
            self.__db = TinyDB('config' + '/' + 'tmail-bot.json')
        else:
            self.__db = TinyDB(path)

    def getTable(self, tableName):
        return self.__db.table(tableName)

    def insertSMTPServer(self, name, host, port):
        SMTPServers = self.__db.table('SMTPServers')
        SMTPServers.insert({'name':name,'host':host,'port':port})
        return SMTPServer(name, host, port)

    def searchSMTPServer(self, name):
        SMTPServers = self.__db.table('SMTPServers')
        query = Query()
        search = SMTPServers.search(query.name == name)
        result = eval(str(search))
        smtpServer = SMTPServer(name, result['host'], result['port'])
        return smtpServer

    def updateSMTPServer(self, smtpServer):
        SMTPServers = self.__db.table('SMTPServers')
        query = Query()
        search = SMTPServers.search({'host':smtpServer.host,'port':smtpServer.port}, query.name == smtpServer.name)
        result = eval(str(search))
        smtpServer = SMTPServer(result['name'], result['host'], result['port'])
        return smtpServer

    def removeSMTPServer(self, name):
        SMTPServers = self.__db.table('SMTPServers')
        query = Query()
        SMTPServers.remove(query.name == name)

    def insertUser(self, id, accounts):
        Users = self.__db.table('Users')
        Users.insert({'id': id, 'accounts':[accounts]})
        return SMTPServer(id, accounts)

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

class SMTPServer:
    def __init__(self, name, host, port):
        self.__name = name
        self.__host = host
        self.__port = port

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

