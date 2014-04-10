import sqlite3

db = sqlite3.connect('images.sqlite')
db.execute('CREATE TABLE IF NOT EXISTS image_store (i INTEGER PRIMARY KEY, image BLOB, name nvarchar(32), desc nvarchar(128))');
db.commit()
db.close()

def insertToDB(data, file_name, file_desc):
    db = sqlite3.connect('images.sqlite')
    db.text_factory = bytes

    # grab whatever it is you want to put in the database
    r = data
    name = file_name
    desc = file_desc 

    # insert!
    db.execute('INSERT INTO image_store (image, name, desc) VALUES (?, ?, ?)', (r, name, desc,))
    db.commit()
