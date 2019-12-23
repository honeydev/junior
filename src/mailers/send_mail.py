from flask import current_app as junior_app
from flask import render_template
from flask_mail import Mail, Message


def send_mail_for_aprove(user):
    msg = Message(
        'Подтвердите регистрацию на JUNIOR, пройдя по ссылке',
        sender=junior_app.config['ADMINS'][0],
        recipients=[user.email],
    )

    msg.html = render_template(
        'user/email_aprove.html',
        user=user,
        token=user.get_token_for_mail_aproved(),
    )
    mail = Mail(junior_app)
    mail.send(msg)
    return True
