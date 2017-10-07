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
        return self.__username

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