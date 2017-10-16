def parseAccountsToJson(accounts):
    json = []
    for acc in accounts:
        account = {}
        account['name'] = acc.name
        account['username'] = acc.username
        account['password'] = acc.password
        account['refresh_time'] = acc.refresh_time
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
        self.name = name
        self.username = username
        self.password = password
        if refresh_time==None:
            self.refresh_time = 3 * 5
        else:
            self.refresh_time = refresh_time