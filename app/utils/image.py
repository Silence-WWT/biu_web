# -*- coding: utf-8 -*-
import os
from base64 import b64decode
from cStringIO import StringIO
from hashlib import md5
from uuid import uuid4

from PIL import Image
from flask import current_app


def generate_dir_path(user_id):
    return '%s/user_%s/' % (user_id % 100, md5(str(user_id)).hexdigest())


def upload_image(user_id, image_base64_string):
    path = current_app.config['IMAGE_DIR']
    relative_path = generate_dir_path(user_id)
    dir_path = os.path.join(path, relative_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    image_name = uuid4().hex
    image_path = os.path.join(dir_path, image_name)
    try:
        image = Image.open(StringIO(b64decode(image_base64_string)))
    except:
        return False
    image.save(image_path, image.format, quality=75)
    return relative_path + image_name
