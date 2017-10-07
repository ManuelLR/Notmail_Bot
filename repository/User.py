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