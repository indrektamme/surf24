import os, time
from PIL import Image #pip install PIL
from flask import url_for, current_app

def add_ad_pic(pic_upload, ad_id):
    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    secondsSinceEpoch = str(time.time())
    storage_filename = str(ad_id) + '_' + secondsSinceEpoch + '.' + ext_type
    filepath = os.path.join(current_app.root_path, 'static', 'ad_pics', storage_filename)
    output_size = (200,200)
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)
    return storage_filename
