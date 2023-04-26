import os
import random
import requests

from flask import current_app

from tcb.image_compress import compress_img


# download image
def download_avatar(gender, name="avatar"):

    if gender:
    
        # genrate avatar authomaticly
        url = "https://xsgames.co/randomusers/avatar.php?g="+gender

        name = name+"_"+str(random.getrandbits(128)) if name == "avatar" else name

        req = requests.get(url)
        ext = '.' + req.headers['content-type'].split('/')[1]
        img_data = req.content

        with open(os.path.join(current_app.config['TEMP'], name+ext), 'wb') as handler:
            handler.write(img_data)

            
        # compresse image
        compress_img(name+ext, 75)
        
        return name+ext
    
    return False




