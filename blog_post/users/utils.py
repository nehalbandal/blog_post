import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from blog_post import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')  # Senders email address
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender=EMAIL_ADDRESS, recipients=[user.email])
    msg.body = '''To reset your password, visit the following link: {}
    \nIf you did not make this request then simply ignore this email and no changes will be made.
    \nThis link is valid only for 30 minutes.
    '''.format(url_for('users.reset_token', token=token, _external=True))
    # _external=True means get absolute URL. There are Jinja2 templates for these messages.
    mail.send(msg)
