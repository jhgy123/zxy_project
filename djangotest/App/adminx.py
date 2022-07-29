from asyncio.log import logger
from hashlib import md5

import xlrd as xlrd
from django.apps import apps
from django.contrib.auth.hashers import make_password
import xadmin
from App.models import ZXYteacher, ZXYstudent
from xadmin.plugins.excel import excel_into_model


class ZXYteacherAdmin(object):
    list_display = ['t_id', 't_name', 't_email', 'is_active', 'is_delete', 't_password']
    search_fields = ['t_id', 't_name']
    list_filter = ['t_id', 't_name', 't_email', 'is_active', 'is_delete']
    list_per_page = 20
    # readonly_fields = ['t_id', 't_name']
    refresh_times = [10, 20, 30, 60]
    list_export = ('xls', 'xml', 'json')
    list_export_fields = ('t_id', 't_name', 't_email')
    model_icon = 'fa fa-user'

    def save_models(self):
        obj = self.new_obj
        teachers = ZXYteacher.objects.filter(t_id=self.new_obj.t_id)
        # print(self.new_obj.t_password)
        if teachers.exists():
            teacher = teachers.first()
            if obj.t_password != teacher.t_password:
                password = obj.t_password
                password = md5(password.encode(encoding='UTF-8')).hexdigest()
                password = make_password(password)
                obj.t_password = password
        else:
            password = obj.t_password
            password = md5(password.encode(encoding='UTF-8')).hexdigest()
            password = make_password(password)
            obj.t_password = password
        # print(self.new_obj.t_password)
        # print(self.new_obj.t_id)
        super().save_models()
        # obj.save()
        # flag = self.org_obj is None and 'create' or 'change'
        # self.log(flag, self.change_message(), self.new_obj)
        #



xadmin.site.register(ZXYteacher, ZXYteacherAdmin)


class ZXYstudentAdmin(object):
    import_excel = True  # 控制开关
    list_display = ['s_id', 's_name', 's_email', 'is_active', 'is_delete', 's_password']
    search_fields = ['s_id', 's_name']
    list_filter = ['s_id', 's_name', 's_email']
    list_per_page = 20
    # readonly_fields = ['s_id', 's_name']
    refresh_times = [10, 20, 30, 60]
    list_export = ('xls', 'xml', 'json')
    list_export_fields = ('s_id', 's_name', 's_email')
    model_icon = 'fa fa-user'

    def save_models(self):
        obj = self.new_obj
        students = ZXYstudent.objects.filter(s_id=self.new_obj.s_id)
        # print(self.new_obj.s_password)
        if students.exists():
            student = students.first()
            if obj.s_password != student.s_password:
                password = obj.s_password
                password = md5(password.encode(encoding='UTF-8')).hexdigest()
                password = make_password(password)
                obj.s_password = password
        else:
            password = obj.s_password
            password = md5(password.encode(encoding='UTF-8')).hexdigest()
            password = make_password(password)
            obj.s_password = password
        # print(self.new_obj.s_password)
        # print(self.new_obj.s_id)
        super().save_models()
        # obj.save()
        # flag = self.org_obj is None and 'create' or 'change'
        # self.log(flag, self.change_message(), self.new_obj)
        #

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            execl_file = request.FILES.get('excel')
            data = xlrd.open_workbook(filename=None, file_contents=request.FILES['excel'].read())
            try:
                appname_ = apps.get_model('App', 'ZXYstudent')
                fields = appname_._meta.fields
                # 导入model,动态导入
                # exec('from %s.models import %s' % (appname, model_name))
            except:
                logger.info('model_name and appname is not exist')
            field_name = []
            # 只导入第一个sheet中的数据
            table = data.sheet_by_index(0)
            rows = table.nrows
            table_header = table.row_values(2)
            for cell in table_header:
                for name in fields:
                    if cell == name.verbose_name.__str__():
                        field_name.append(name.name)
            # if 'add_time' in field_name:
            #     field_name.remove('add_time')
            for row in range(4, rows):
                # 行的数据,创建对象,进行报错数据
                # exec('obj' + '=%s()' % model_name)
                student = ZXYstudent()
                columns = len(field_name)
                for column in range(columns):
                    if 's_id' == field_name[column]:
                        id = int(table.cell_value(row, column+1))
                        s_id = str(id)
                        student.s_id = s_id
                    else:
                        exec('student.%s' % field_name[column] + '="%s"' % (table.cell_value(row, column+1)))
                password = 'zxy@' + student.s_id
                password = md5(password.encode(encoding='UTF-8')).hexdigest()
                password = make_password(password)
                student.s_password = password
                student.is_active = True
                student.save()

        return super(ZXYstudentAdmin, self).post(request, *args, **kwargs)

xadmin.site.register(ZXYstudent, ZXYstudentAdmin)


