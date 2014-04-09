import sqlite3

db = sqlite3.connect('images.sqlite')
db.execute('CREATE TABLE IF NOT EXISTS image_store (i INTEGER PRIMARY KEY, image BLOB)');
db.commit()
db.close()

def insertToDB(data):
    db = sqlite3.connect('images.sqlite')
    db.text_factory = bytes

    # grab whatever it is you want to put in the database
    r = data

    # insert!
    db.execute('INSERT INTO image_store (image) VALUES (?)', (r,))
    db.commit()

    
