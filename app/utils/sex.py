from flask import current_app


def sex_isvalid(sex):
    return current_app.config['SEX_FEMALE'] <= sex <= current_app.config['SEX_UNKNOWN']