class User:
    def __init__(self, id, accounts):
        self.id = id
        self.accounts = accounts

    def addAccount(self, account):
        self.accounts.append(account)

    def updateAccount(self, account):
        i = 0
        for acc in self.accounts:
            if acc.name == account.name:
                self.accounts[i] = account
                break
            i = i + 1

    def removeAccount(self, account):
        i = 0
        for acc in self.accounts:
            if acc.name == account.name:
                self.accounts.pop(i)
                break
            i = i + 1