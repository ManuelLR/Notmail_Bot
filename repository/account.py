def parse_accounts_to_json(accounts):
    json = []
    for acc in accounts:
        account = {'name': acc.name, 'username': acc.username, 'password': acc.password, 'host': acc.host,
                   'port': acc.port, 'protocol': acc.protocol, 'refresh_time': acc.refresh_time}
        json.append(account)
    return json


def parse_json_to_accounts(accounts):
    result = []
    for acc in accounts:
        account = Account(acc['name'],acc['username'],acc['password'], acc['host'], acc['port'],
                          acc['protocol'], acc['refresh_time'])
        result.append(account)
    return result


class Account:
    def __init__(self, name, username, password, host, port, protocol, refresh_time=None):
        self.name = name
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.protocol = protocol
        if refresh_time is None:
            self.refresh_time = 3 * 5
        else:
            self.refresh_time = refresh_time
