# zxy_project
智学云-教学办公一体化平台

## 环境配置
* 下载python 3.6/3.7。及以上版本，具体请参考 [python](https://www.python.org/downloads/) 查看安装前的准备及安装过程。
* 在./zxy_project/djangotest目录下，使用pip安装： `pip install -r requirements.txt`下载项目运行依赖包。
* 然后终端下执行:
* ```bash
     python manage.py makemigrations
     python manage.py migrate
  ```
* 创建超级用户，在终端下执行:
* ```bash
    python manage.py createsuperuser
  ```
* 开始运行，在终端下执行:
* ```bash
   python manage.py runserver
  ```
* 至此即可浏览器打开: http://127.0.0.1:8000/zxy/index 运行本项目。
## 使用说明
### 项目文件说明：
这部分将展示zxy_project的文件结构全貌。文件树如下：

 ```
├── djangotest                   # 项目源代码文件
│     ├── App                    # 学生、教师应用文件
│     ├── document_template      # 表格、文档模板文件
│     ├── static                 # 静态资源文件
│     │     ├── css              # 页面样式文件
│     │     ├── images           # 页面图片文件
│     │     └── js               # 页面js文件
│     ├── templates              # 前端html模板文件
│     ├── xadmin                 # xadmin插件自定义修改后的源码
│     ├── ZXY                    # 项目配置文件
│     ├── manage.py              # django启动文件
│     └── requirements.txt       # 项目依赖配置文件
└──README.md
```
#### 6.3.2 路由说明：(默认主机IP:端口号127.0.0.1:8000)
* `主机IP:端口号/zxy/index`智学云Web首页
* `主机IP:端口号/zxy/xadmin`智学云后台管理登陆页面
*  其他页面路径可点击跳转页面后获取
