import pickedb

db = pickedb.load('config/tmail-bot.db', False)


def insert(key, value):
    db.set(key, value)


def get_all():
    return db.getAll()


def get(key):
    return db.get(key)
