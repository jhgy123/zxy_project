from django.core.mail import send_mail
from django.http import HttpResponse
from django.template import loader

from ZXY.settings import EMAIL_HOST_USER, SERVER_HOST, SERVER_PORT


def send_email_activate(teachername, receive, u_token):
    subject = "智学云（ZXY）用户激活"  # subject, message, from_email 和 recipient_list
    message = ""
    data = {
        'teacher_name': teachername,
        'activate_url': 'http://{}:{}/zxy/activate/?u_token={}'.format(SERVER_HOST, SERVER_PORT, u_token)

    }
    html_message = loader.get_template('activate.html').render(data)
    from_email = EMAIL_HOST_USER
    recipient_list = [receive,]
    send_mail(subject=subject, message='', html_message=html_message, from_email=from_email, recipient_list=recipient_list)


def send_email_reset_t(teachername, receive, u_token1, u_token2):
    subject = "智学云（ZXY）用户密码重置"  # subject, message, from_email 和 recipient_list
    message = ""
    data = {
        'teacher_name': teachername,
        'reset_url': 'http://{}:{}/zxy/resetteacher/?u_token1={}&u_token2={}'.format(SERVER_HOST, SERVER_PORT, u_token1, u_token2)

    }
    html_message = loader.get_template('reset_t.html').render(data)
    from_email = EMAIL_HOST_USER
    recipient_list = [receive,]
    send_mail(subject=subject, message='', html_message=html_message, from_email=from_email, recipient_list=recipient_list)


def send_email_reset_s(studentname, receive, u_token1, u_token2):
    subject = "智学云（ZXY）用户密码重置"  # subject, message, from_email 和 recipient_list
    message = ""
    data = {
        'student_name': studentname,
        'reset_url': 'http://{}:{}/zxy/resetstudent/?u_token1={}&u_token2={}'.format(SERVER_HOST, SERVER_PORT, u_token1, u_token2)

    }
    html_message = loader.get_template('reset_s.html').render(data)
    from_email = EMAIL_HOST_USER
    recipient_list = [receive,]
    send_mail(subject=subject, message='', html_message=html_message, from_email=from_email, recipient_list=recipient_list)
