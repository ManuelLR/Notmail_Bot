import configparser
from tinydb import TinyDB, Query

SMTP_SERVER = None
SMTP_SERVER_PORT = None
FROM_EMAIL = None
FROM_PWD = None



#    global SMTP_SERVER, SMTP_SERVER_PORT, FROM_EMAIL, FROM_PWD
Config = configparser.ConfigParser()
Config.read('myconfig.ini')
SMTP_SERVER = Config.get("email test", "SMTP_SERVER")
SMTP_SERVER_PORT = Config.get("email test", "SMTP_SERVER_PORT")
FROM_EMAIL = Config.get("email test", "FROM_EMAIL")
FROM_PWD = Config.get("email test", "FROM_PWD")

#DB configuration
db = TinyDB('db.json')
users = db.table('Users')
#Only uncoment if you want to insert a new row
#users.insert({'id':'1234567890','accounts':[{'gmail':{'username':FROM_EMAIL,'password':FROM_PWD}}]})
User = Query()
result  = users.search(User.id == '1234567890')
print(eval(str(result[0]))['accounts'][0])