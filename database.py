from tinydb import TinyDB
from os.path import exists

def init_db():
    if exists('data.jspn') == False:
        db = TinyDB('data.json')
        db.insert({'like': 0, 'dislike': 0})

def get_data():
    if exists('data.json') == False:
        init_db()
    db = TinyDB('data.json')
    return db.all()[0]

def update_data(text):
    if exists('data.json') == False:
        init_db()
    db = TinyDB('data.json')

    if text == 'like':
        db.update({'like': int(db.all()[0]['like']) + 1})
    if text == 'dislike':
        db.update({'dislike': int(db.all()[0]['dislike']) + 1})


