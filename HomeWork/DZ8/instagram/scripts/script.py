from pymongo import MongoClient


def subscribers(id):
    client = MongoClient('localhost', 27017)
    base = client['instagram']
    db = base[id]

    items = db.find({'status': 'subscriber'})
    for item in items:
        print(item)


def subscriptions(id):
    client = MongoClient('localhost', 27017)
    base = client['instagram']
    db = base[id]

    items = db.find({'status': 'subscription'})
    for item in items:
        print(item)


if __name__ == '__main__':
    subscribers('3688525371')
    subscriptions('3688525371')
