# -*- coding: utf-8 -*-
import os
from hashlib import md5
from uuid import uuid4

from flask import current_app


IMAGE_EXTS = ['jpg', 'png', 'bmp', 'gif']


def generate_dir_path(user_id):
    return '%s/user_%s/' % (user_id % 100, md5(str(user_id)).hexdigest())


def valid_image(name):
    ext = name.rsplit('.', 1)[-1]
    return ext in IMAGE_EXTS


def upload_image(user_id, image):
    path = current_app.config['IMAGE_DIR']
    relative_path = generate_dir_path(user_id)
    dir_path = os.path.join(path, relative_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    ext = image.filename.rsplit('.', 1)[-1]
    image_name = uuid4().hex + '.' + ext
    image_path = os.path.join(dir_path, image_name)
    image.save(image_path)
    return relative_path + image_name
