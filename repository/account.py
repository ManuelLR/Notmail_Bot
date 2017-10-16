def parse_accounts_to_json(accounts):
    json = []
    for acc in accounts:
        account = {'name': acc.name, 'username': acc.username, 'password': acc.password,
                   'refresh_time': acc.refresh_time}
        json.append(account)
    return json


def parse_json_to_accounts(accounts):
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
        if refresh_time is None:
            self.refresh_time = 3 * 5
        else:
            self.refresh_time = refresh_time
