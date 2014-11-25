# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, IntegerField
from flask_wtf.file import FileField, FileAllowed


class PersonalInfoForm(Form):
    image = FileField('image', validators=[FileAllowed(['jpg', 'png', 'bmp', 'gif'])])
    user_id = IntegerField('user_id')
    nickname = StringField('nickname')
    signature = StringField('signature')