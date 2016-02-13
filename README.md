# WebsiteForCouples
##开放源代码许可
部分CSS和JS文件来自于muicss项目:[muicss](https://github.com/muicss/mui)  
服务器程序使用了Flask项目的库:[Flask](https://github.com/mitsuhiko/flask)
##简介
一个小型网站，情侣【亦可是基友 可以在上面发表一些文字或是分享图片、音乐，设计为只有两个账户，账户没有存在数据库中，所以可以避免在登陆界面进行SQL注入攻击，但是表单没有进行输入验证，所以不能避免在登陆后的界面中进行的XSS攻击
##已知bug：  
在Windows和Linux系统上的路径有异，Linux上的数据库路径、文件存储路径需要用绝对路径，但是在HTML文档中却需要使用相对路径，例如：  
>\#runserver.py:  
>file = request.file['file']  
>file.save('/srv/http/static/upload' + file.filename)  

>&lt;!--index.html--&gt;  
>&lt;img src="../static/upload/filename.png"&gt;

发布得匆忙，在代码中并没有对路径这个问题进行仔细研究，所以在使用中还请多加修改

##How to start: 
0.系统要求：  
* OS:Windows/Linux  
* Python 3.4或以上
* Python-flask 库
* Sqlite3 
  
1.打开server.ini，修改数据库路径、上传文件存储路径、是否调试以及端口号  
2.打开runserver.py，修改你需要显示的纪念日的日期，以及两位用户的用户名和密码，密码使用了明文，考虑到安全性可以再用md5加密一次  
3.创建数据库： 
>$ sqlite3 data.db3  
>  \>.read init_database.sql  
>  \>.exit  

4.启动服务：  
Windows:双击runserver.py运行  
Linux:  
> python ./runserver.py &  
  
  
欢迎提交Pull Request
