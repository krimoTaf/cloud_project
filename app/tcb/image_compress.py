import os
from PIL import Image
from flask import current_app


# compress downloaded image
def compress_img(image_file, quality = 70):

    image = Image.open(os.path.join(current_app.config['TEMP'], image_file))

    image.save(os.path.join(current_app.config['TEMP'], image_file), image.format, optimize = True, quality = quality)
    