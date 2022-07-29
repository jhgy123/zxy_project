from asyncio.log import logger

from django.apps import apps

import xadmin
from xadmin.plugins.utils import get_context_dict
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader


#excel 导入
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    def block_top_toolbar(self, context, nodes):
        context = get_context_dict(context or {})
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html', context=context))

xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)


# def excel_into_model(appname, model_name, excel_file):
#     import xlrd
#     exec('from %s.models import %s' % (appname, model_name))
#     table1 = excel_file.sheet_by_index(0)
#     objs = []
#     nrows = table1.nrows
#     for index in range(2,nrows):
#         row_values = table1.row_values(index)


def excel_into_model(appname, model_name, excel_file):
    import xlrd
    #tmp[7].verbose_name.__str__()
    try:
        appname_ = apps.get_model(appname, model_name)
        fields = appname_._meta.fields
        #导入model,动态导入
        exec('from %s.models import %s' % (appname, model_name))
    except :
        logger.info('model_name and appname is not exist')
    field_name = []
    #只导入第一个sheet中的数据
    table = excel_file.sheet_by_index(0)
    nrows = table.nrows
    table_header = table.row_values(1)
    for cell in table_header:
        for name in fields:
            if cell in name.verbose_name.__str__():
                field_name.append(name.name)
    # if 'add_time' in field_name:
    #     field_name.remove('add_time')
    for rows in range(2, nrows):
        # 行的数据,创建对象,进行报错数据
        exec('obj' + '=%s()' % model_name)
        columns = len(field_name)
        for column in range(columns):
            exec('obj.%s' % field_name[column] +'="%s"' % (table.cell_value(rows, column)))
        exec('obj.save()')