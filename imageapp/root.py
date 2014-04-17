import quixote
from quixote.directory import Directory, export, subdir

from . import html, db, image

class RootDirectory(Directory):
    _q_exports = []

    @export(name='') # this makes it public.
    def index(self):
        return html.render('index.html')

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        file_name = request.form['name']
        file_desc = request.form['desc']
        
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))

        
        img = image.add_image_metadata(data, file_name, file_desc)
        image.add_image(img)
        db.text_factory = bytes
        db.insertToDB(data, file_name, file_desc);

        return quixote.redirect('./')

    @export(name='image')
    def image(self):
        return html.render('image.html')

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        response.set_content_type('image/jpg')
        img = image.get_latest_image()
        return img

    @export(name='image_name')
    def image_raw(self):
        response = quixote.get_response()
        response.set_content_type('text/plain')
        img = image.get_latest_name()
        return img
    
    @export(name='image_desc')
    def image_raw(self):
        response = quixote.get_response()
        response.set_content_type('text/plain')
        img = image.get_latest_desc()
        return img
    
    @export(name='body.jpg')
    def body_jpg(self):
        data = html.get_image('body.jpg')
        return data

    @export(name='content.jpg')
    def content_jpg(self):
        data = html.get_image('content.jpg')
        return data

    @export(name='footer.gif')
    def footer_gif(self):
        data = html.get_image('footer.gif')
        return data

    @export(name='header.jpg')
    def header_jpg(self):
        data = html.get_image('header.jpg')
        return data

    @export(name='menubottom.jpg')
    def menubottom_jpg(self):
        data = html.get_image('menubottom.jpg')
        return data

    @export(name='menuhover.gif')
    def menuhover_gif(self):
        data = html.get_image('menuhover.gif')
        return data

