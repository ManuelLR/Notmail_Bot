from tinydb import TinyDB, Query

class DBC:
    def __init__(self, path=None):
        if path is None:
            self.__db = TinyDB('config' + '/' + 'db.json')
        else:
            self.__db = TinyDB(path)

    def getTable(self, tableName):
        return self.__db.table(tableName)

    def searchSMTPServer(self, name):
        SMTPServers = self.__db.table('SMTPServers')
        query = Query()
        search = SMTPServers.search(query.name == name)
        result = eval(str(search))
        smtpServer = SMTPServer(name, result['host'], result['port'])
        return smtpServer

    def insertSMTPServer(self, name, host, port):
        SMTPServers = self.__db.table('SMTPServers')
        SMTPServers.insert({'name':name,'host':host,'port':port})
        return SMTPServer(name, host, port)

    def updateSMTPServer(self, smtpServer):
        pass

    def removeSMTPServer(self, name):
        pass

    def searchUser(self, id):
        pass

    def insertUser(self, id, accounts):
        pass

    def updateUser(self, user):
        pass

    def removeUser(self, id):
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
