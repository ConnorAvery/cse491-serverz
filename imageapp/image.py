# image handling API

import sqlite3

def add_image_metadata(data, name, desc):
    img = {'data' : data}
    img['name'] = name
    img['desc'] = desc
    return img

def add_image(data):
    images.append(data)
    return len(images)

def get_image(num):
    img = images[num]
    return img['data']

def get_latest_image():
    img = images[0]
    return img['data']

def get_latest_name():
    img = images[len(images) - 1]
    return img['name']

def get_latest_desc():
    img = images[len(images) - 1]
    return img['desc']


db = sqlite3.connect('images.sqlite')
db.text_factory = bytes
c = db.cursor()
c.execute('SELECT image, name, desc FROM image_store')
images = []
rows = c.fetchall()
for row in rows:
    add_image(row[0])
    add_image_metadata(row[0], row[1], row[2])
