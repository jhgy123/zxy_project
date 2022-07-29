import uuid

# from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.urls import reverse
from ratelimit.decorators import ratelimit
# import ratelimit
from App.models import ZXYteacher, ZXYstudent
from App.views_helper import send_email_activate, send_email_reset_t, send_email_reset_s


def index(request):
    data = {}
    return render(request, 'index.html', context=data)

def register_teacher(request):
    if request.method == "GET":
        data = {}
        return render(request, 'register_teacher.html', context=data)

    elif request.method == "POST":
        teachername = request.POST.get("teachername")
        teacherid = request.POST.get("teacherid")
        teacheremail = request.POST.get("teacheremail")
        teacherpaw = request.POST.get("teacherpaw")

        password = make_password(teacherpaw)

        teacher = ZXYteacher()
        teacher.t_name = teachername
        teacher.t_id = teacherid
        teacher.t_email = teacheremail
        teacher.t_password = password
        teacher.save()
        u_token = uuid.uuid4().hex
        cache.set(u_token, teacher.t_id, timeout=60*60*24)
        send_email_activate(teachername, teacheremail, u_token)
        return redirect(reverse("zxy:login_teacher"))


#用户登录次数限制
@ratelimit(key='post:teacherid', rate='10/24h', method=['POST',], block=True)
def login_teacher(request):
    if request.method == "GET":
        data = {}
        return render(request, 'login_teacher.html', context=data)
    elif request.method == "POST":
        tid = request.POST.get('teacherid')
        tpaw = request.POST.get('teacherpaw')
        teachers = ZXYteacher.objects.filter(t_id=tid)
        # data = {
        #     "status": 902,
        #     "msg": "user error or password error"
        # }
        if teachers.exists():
            teacher = teachers.first()
            if check_password(tpaw, teacher.t_password):
                if teacher.is_active:
                    teachername = teacher.t_name
                    request.session['teachername'] = teachername
                    return redirect(reverse("zxy:teacher_home"))
                else:
                    return render(request, 'unactivated_error.html')

        return render(request, 'login_error_t.html')


def activate(request):
    u_token = request.GET.get('u_token')
    teacher_id = cache.get(u_token)
    if teacher_id:
        teachers = ZXYteacher.objects.filter(t_id=teacher_id)
        teacher = teachers.first()
        teacher.is_active = True
        teacher.save()
        data = {
            "title": "激活成功提示",
            "content": "您的账号激活成功，快前往登录页面去使用吧"
        }
        return render(request, 'notice.html', context=data)
    data = {
        "title": "激活失败提示",
        "content": "激活链接已失效，请重新激活该账号"
    }
    return render(request, 'activation_failed.html', context=data)


#用户激活次数限制
@ratelimit(key='post:teacherid', rate='2/24h', method=['POST',], block=True)
def reactivate(request):
    if request.method == "GET":
        data = {}
        return render(request, 'reactivate.html', context=data)
    elif request.method == "POST":
        tid = request.POST.get('teacherid')
        tpaw = request.POST.get('teacherpaw')
        teachers = ZXYteacher.objects.filter(t_id=tid)
        if teachers.exists():
            teacher = teachers.first()
            if check_password(tpaw, teacher.t_password):
                teachername = teacher.t_name
                teacheremail = teacher.t_email
                u_token = uuid.uuid4().hex
                cache.set(u_token, teacher.t_id, timeout=60 * 60 * 24)
                send_email_activate(teachername, teacheremail, u_token)
                return redirect(reverse("zxy:login_teacher"))
        data = {
            "title": "错误警告",
            "content": "用户名或密码错误，请返回后重新进行激活操作"
        }
        return render(request, 'notice.html', context=data)


# @login_required(login_url="zxy:login_teacher")
def teacher_home(request):
    if request.method == "GET":
        teachername = request.session.get("teachername")
        # print(teachername)
        if teachername:
            data = {
                "teachername": teachername
            }
            return render(request, 'teacher_home.html', context=data)
        else:
            return redirect(reverse("zxy:login_teacher"))


def logout_teacher(request):
    request.session.flush()
    return redirect(reverse("zxy:login_teacher"))


def reset_teacher(request):
    if request.method == "GET":
        data = {}
        return render(request, 'reset_teacher.html', context=data)
    elif request.method == "POST":
        teachername = request.POST.get("teachername")
        teacherid = request.POST.get("teacherid")
        teacheremail = request.POST.get("teacheremail")
        teacherpaw = request.POST.get("teacherpaw")
        # password = make_password(teacherpaw)
        teachers = ZXYteacher.objects.filter(t_id=teacherid)
        if teachers.exists():
            teacher = teachers.first()
            if teacher.t_name == teachername:
                if teacher.t_email == teacheremail:
                    u_token1 = uuid.uuid4().hex
                    u_token2 = uuid.uuid4().hex
                    cache.set(u_token1, teacher.t_id, timeout=60 * 60 * 24)
                    cache.set(u_token2, teacherpaw, timeout=60 * 60 * 24)
                    send_email_reset_t(teachername, teacheremail, u_token1, u_token2)
                    return redirect(reverse("zxy:login_teacher"))
        data = {
            "title": "错误警告",
            "content": "用户名、职工号或邮箱错误，请返回后重新操作"
        }
        return render(request, 'notice.html', context=data)


def resetteacher(request):
    u_token1 = request.GET.get('u_token1')
    u_token2 = request.GET.get('u_token2')
    teacher_id = cache.get(u_token1)
    teacherpaw = cache.get(u_token2)
    if teacher_id and teacherpaw:
        teachers = ZXYteacher.objects.filter(t_id=teacher_id)
        teacher = teachers.first()
        password = make_password(teacherpaw)
        teacher.t_password = password
        teacher.save()
        data = {
            "title": "密码重置成功提示",
            "content": "您的账号密码重置成功，快前往教师登录页面去使用吧"
        }
        return render(request, 'notice.html', context=data)
    data = {
        "title": "密码重置失败提示",
        "content": "密码重置链接已失效，请重新操作"
    }
    return render(request, 'resetteacher_failed.html', context=data)


#用户登录次数限制
@ratelimit(key='post:studentid', rate='10/24h', method=['POST',], block=True)
def login_student(request):
    if request.method == "GET":
        data = {}
        return render(request, 'login_student.html', context=data)
    elif request.method == "POST":
        sid = request.POST.get('studentid')
        spaw = request.POST.get('studentpaw')
        students = ZXYstudent.objects.filter(s_id=sid)
        if students.exists():
            student = students.first()
            if check_password(spaw, student.s_password):
                if student.is_active:
                    studentname = student.s_name
                    request.session['studentname'] = studentname
                    return redirect(reverse("zxy:student_home"))
                else:
                    data = {
                        "title": "账号状态异常提示",
                        "content": "您的账号状态异常，请联系管理员处理后再登录"
                    }
                    return render(request, 'notice.html', context=data)
        return render(request, 'login_error_s.html')


# @login_required(login_url="zxy:login_student")
def student_home(request):
    if request.method == "GET":
        studentname = request.session.get("studentname")
        # print(studentname)
        if studentname:
            data = {
                "studentname": studentname
            }
            return render(request, 'student_home.html', context=data)
        else:
            return redirect(reverse("zxy:login_student"))


def logout_student(request):
    request.session.flush()
    return redirect(reverse("zxy:login_student"))


def reset_student(request):
    if request.method == "GET":
        data = {}
        return render(request, 'reset_student.html', context=data)
    elif request.method == "POST":
        studentname = request.POST.get("studentname")
        studentid = request.POST.get("studentid")
        studentemail = request.POST.get("studentemail")
        studentpaw = request.POST.get("studentpaw")
        # password = make_password(studentpaw)
        students = ZXYstudent.objects.filter(s_id=studentid)
        if students.exists():
            student = students.first()
            if student.s_name == studentname:
                if student.s_email == studentemail:
                    u_token1 = uuid.uuid4().hex
                    u_token2 = uuid.uuid4().hex
                    cache.set(u_token1, student.s_id, timeout=60 * 60 * 24)
                    cache.set(u_token2, studentpaw, timeout=60 * 60 * 24)
                    send_email_reset_s(studentname, studentemail, u_token1, u_token2)
                    return redirect(reverse("zxy:login_student"))
        data = {
            "title": "错误警告",
            "content": "用户名、学号或邮箱错误，请返回后重新操作"
        }
        return render(request, 'notice.html', context=data)


def resetstudent(request):
    u_token1 = request.GET.get('u_token1')
    u_token2 = request.GET.get('u_token2')
    student_id = cache.get(u_token1)
    studentpaw = cache.get(u_token2)
    if student_id and studentpaw:
        students = ZXYstudent.objects.filter(s_id=student_id)
        student = students.first()
        password = make_password(studentpaw)
        student.s_password = password
        student.save()
        data = {
            "title": "密码重置成功提示",
            "content": "您的账号密码重置成功，快前往学生登录页面去使用吧"
        }
        return render(request, 'notice.html', context=data)
    data = {
        "title": "密码重置失败提示",
        "content": "密码重置链接已失效，请重新操作"
    }
    return render(request, 'resetstudent_failed.html', context=data)




def checktid(request):
    tid = request.GET.get('teacherid')
    teachers = ZXYteacher.objects.filter(t_id=tid)
    data = {
        "status": 200,
        "msg": "ok"
    }
    if teachers.exists():
        data['status'] = 901
        data['msg'] = 'teacher already exist'
    else:
        pass
    return JsonResponse(data=data)


def checklogint(request):
    tid = request.GET.get('teacherid')
    tpaw = request.GET.get('teacherpaw')
    teachers = ZXYteacher.objects.filter(t_id=tid)
    data = {
        "status": 902,
        "msg": "user error or password error"
    }
    if teachers.exists():
        teacher = teachers.first()
        if check_password(tpaw, teacher.t_password):
            data["status"] = 200
            data["msg"] = "ok"
    return JsonResponse(data=data)


def send_email(request):
    subject = "ZXY"  # subject, message, from_email 和 recipient_list
    message = ""
    data = {
        'teacher_name': 'Tom',
        'activate_url': 'htt://wwwww'

    }
    html_message = loader.get_template('activate.html').render(data)
    from_email = 'project_user@163.com'
    recipient_list = ['project_user@163.com', ]
    send_mail(subject=subject, message='', html_message=html_message, from_email=from_email, recipient_list=recipient_list)
    return HttpResponse("SUCCESS!")


