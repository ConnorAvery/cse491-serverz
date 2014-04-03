# image handling API

import sqlite3

def add_image(data):
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0
    print image_num
    images[image_num] = data
    return image_num

def get_image(num):
    return images[num]

def get_latest_image():
    image_num = max(images.keys())
    return images[0]

db = sqlite3.connect('images.sqlite')
db.text_factory = bytes
c = db.cursor()
c.execute('SELECT image FROM image_store')
images = {}
rows = c.fetchall()
for row in rows:
    add_image(row[0])
