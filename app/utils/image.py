# -*- coding: utf-8 -*-
import os
import requests
from base64 import b64decode
from cStringIO import StringIO
from hashlib import md5
from uuid import uuid4

from PIL import Image
from flask import current_app


def generate_dir_path(user_id):
    return '%s/user_%s/' % (user_id % 100, md5(str(user_id)).hexdigest())


def upload_image(user_id, image_string, is_base64=True):
    path = current_app.config['IMAGE_DIR']
    relative_path = generate_dir_path(user_id)
    dir_path = os.path.join(path, relative_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    image_name = uuid4().hex
    image_path = os.path.join(dir_path, image_name)
    try:
        if is_base64:
            image_string = b64decode(image_string)
        image = Image.open(StringIO(image_string))
    except:
        return ''
    image.save(image_path, image.format, quality=75)
    return relative_path + image_name


def get_image_from_url(user_id, image_url):
    if not image_url:
        image_string = ''
    else:
        try:
            resp = requests.get(image_url)
            image_string = resp.content
        except:
            image_string = ''
    if image_string:
        image_path = upload_image(user_id, image_string, False)
    else:
        image_path = ''
    return image_path