import os
import random
import pyshorteners
from flask import current_app
from flask import (
    Blueprint, g, request, jsonify, current_app
)



from tcb.db import get_db
from tcb.upload_s3 import upload_S3

from tcb.image_compress import compress_img

from werkzeug.utils import secure_filename

bp = Blueprint('upload_file', __name__)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@bp.route('/upload_file', methods=('POST',))
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return ('No file part')
        file = request.files['file']
            
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
           return ('No file !')
        
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            old_name = filename

            # add some random to image name
            filename = str('_'+str(random.getrandbits(16))+'.').join(filename.split('.'))

            file.save(os.path.join(os.path.join(current_app.config['TEMP'], filename)))

            # compresse image
            compress_img(filename, 75)
            
            #upload to S3 images bucket
            upload_S3(filename, "tcb-cloud", "images/"+g.user['username']+"/"+filename)

            link_to_S3 = current_app.config['AWS_S3_LINK']+"images/"+g.user['username']+"/"+filename

            short_link = pyshorteners.Shortener().tinyurl.short(link_to_S3)

            db = get_db()

            with db:
                with db.cursor() as curs:
                    curs.execute(
                        'INSERT INTO image (name, link, user_id)'
                        ' VALUES (%s, %s, %s)',
                        (old_name, short_link, g.user['id'])
                    )



            resp = jsonify({"success": True, "link": short_link})

            return resp
        

    return ""