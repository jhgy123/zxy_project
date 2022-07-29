from django.db import models

# Create your models here.


class ZXYteacher(models.Model):
    t_id = models.CharField('职工号', max_length=11, primary_key=True, unique=True)
    t_name = models.CharField('姓名', max_length=32)
    t_email = models.CharField('邮箱', max_length=64)
    t_password = models.CharField('密码', max_length=256)
    is_active = models.BooleanField('账号是否已激活', default=False)
    is_delete = models.BooleanField('账号是否已删除', default=False)

    class Meta:
        db_table = 'zxy_teacher'
        verbose_name = u'教师账号管理'
        verbose_name_plural = verbose_name


class ZXYstudent(models.Model):
    s_id = models.CharField('学号', max_length=11, primary_key=True, unique=True)
    s_name = models.CharField('姓名', max_length=32)
    s_email = models.CharField('邮箱', max_length=64)
    s_password = models.CharField('密码', max_length=256)
    is_active = models.BooleanField('账号是否已激活', default=False)
    is_delete = models.BooleanField('账号是否已删除', default=False)

    class Meta:
        db_table = 'zxy_student'
        verbose_name = u'学生账号管理'
        verbose_name_plural = verbose_name