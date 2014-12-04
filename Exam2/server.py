#! coding: utf-8
"""
student number:13331235
name: TanXiao
head: Web2.0-Hw4
"""
import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import sys
reload(sys)
sys.setdefaultencoding('GBK')

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

def get_userinfo(path):
    """
    从users.txt中读取数据
    """
    thefile = open(os.path.join(path, 'userData', 'users.txt'), 'r')
    userlist = thefile.read().splitlines()
    for x in range(0, len(userlist)):
        userlist[x] = userlist[x].split(',')
    return userlist

def set_userinfo(path, username, password):
    """
    向users.txt中写入数据
    """
    thefile = open(os.path.join(path, 'userData', 'users.txt'), 'a')
    thefile.write(username+','+password+'\n')
    thefile.close()

def get_questions(path):
    """
    从questions.txt中读取数据
    """
    thefile = open(os.path.join(path, 'questionData', 'questions.txt'), 'r')
    allquestions = thefile.read().splitlines()
    questions = []
    for everyquestion in allquestions:
        everyline = everyquestion.split(';')
        onequestion = question(everyline[0],everyline[1],everyline[2],\
                               everyline[3],everyline[4],everyline[5],\
                               everyline[6],everyline[7].split(','))
        questions.append(onequestion)
    return questions

class question:
    """
    参数顺序：投票数，回答数，回答状态，浏览数，姓名，时间，内容，标签
    """
    def __init__(self, toupiao, huidashu, huida, liulan,\
                 name, time, content, tags):
        self.toupiao = toupiao
        self.huidashu = huidashu
        self.huida = huida
        self.liulan = liulan
        self.name = name
        self.time = time
        self.content = content
        self.tags = tags

    def set_question(self, path):
        """
        向questions.txt中写入数据
        """
        thefile = open(os.path.join(path, 'questionData', 'questions.txt'), 'a')
        alltag = ""
        for x in range(0, len(self.tags)):
            if x != 0:
                alltag = alltag + ','
            alltag = alltag + self.tags[x]
        thefile.write(self.toupiao+';'+self.huidashu+';'\
                      +self.huida+';'+self.liulan+';'\
                      +self.name+';'+self.time+';'\
                      +self.content+';'+alltag+'\n')
        thefile.close()

    def get_answer(self):
        """
        在此处生成问题的回答状态，传入html的class里
        """
        ans = "answers"
        if self.huidashu[0] != '0':
            ans = ans + ' ' + "answered"
        if self.huida == "解决":
            ans = ans + ' ' + "solved"
        return ans

    def get_vote(self):
        """
        在此处生成问题的投票状态，传入html的class里
        """
        vote = "votes hidden-xs"
        if self.toupiao[0] == '-':
            vote = vote + ' ' + "minus"
        elif self.toupiao[0] == '0':
            pass
        else:
            vote = vote + ' ' + "plus"
        return vote

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_cookie("user")

class MainHandler(BaseHandler):
    """
    主页
    """
    def get(self):
        Login = False
        name = None
        if self.current_user:
            Login = True
        if Login is True:
            name = self.get_cookie("user")
        path = os.path.join(os.path.dirname(__file__), "static")
        questions = get_questions(path)
        self.render('index.html', Login=Login, name=name, questions=questions)

class LoginHandler(BaseHandler):
    """
    LoginHandler
    登陆页面，传入signinup的是"login"
    """
    def get(self):
        if self.current_user:
            self.redirect("/")
            return
        self.render('signinup.html', Login="login")

    def post(self):
        name = self.get_argument("name", None)
        password = self.get_argument("password", None)
        path = os.path.join(os.path.dirname(__file__), "static")
        userlist = get_userinfo(path)
        success = False
        # 用户名密码填写不完整，留在原页面
        if name == None or password == None:
            self.render('signinup.html', Login="login")
        for user in userlist:
            if name == user[0] and password == user[1]:
                success = True
        # 用户名密码检验正确后重定向到主页
        if success == True:
            self.set_cookie("user", self.get_argument("name"))
            self.redirect("/")
        # 用户名密码检验不通过留在原页面
        else:
            self.render('signinup.html', Login="login")

class LogoutHandler(BaseHandler):
    """
    LogoutHandler
    """
    def get(self):
        # 登出时清空cookie并返回主页
        self.clear_cookie("user")
        self.redirect("/")

class SignInHandler(BaseHandler):
    """
    SignInHandler
    注册页面，传入signinup的是"signin"
    """
    def get(self):
        if self.current_user:
            self.redirect("/")
            return
        self.render('signinup.html', Login="signin")

    def post(self):
        name = self.get_argument("name", None)
        password = self.get_argument("password", None)
        path = os.path.join(os.path.dirname(__file__), "static")
        userlist = get_userinfo(path)
        success = True
        # 用户名密码填写不完整，留在原页面
        if name == None or password == None:
            self.render('signinup.html', Login="signin")
        print len(password)
        for user in userlist:
            if name == user[0]:
                success = False
        # 用户名密码检验正确后，信息写入文件，重定向到主页
        if success == True:
            # 密码大于等于六位，否则留在原页面
            if len(password) >= 6:
                set_userinfo(path, name, password)
                self.set_cookie("user", self.get_argument("name"))
                self.redirect("/")
            else:
                self.render('signinup.html', Login="signin")
        # 用户名密码检验不通过留在原页面
        else:
            self.render('signinup.html', Login="signin")

class AskHandler(BaseHandler):
    """
    提问页面(时间仓促没有做验证是否逗号隔开的工作)
    """
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        name = self.get_cookie("user")
        self.render('ask.html', name=name)
    def post(self):
        name = self.get_cookie("user")
        title = self.get_argument("title", None)
        tags = self.get_argument("tags", None)
        content = self.get_argument("content", None)
        path = os.path.join(os.path.dirname(__file__), "static")
        if title == None or tags == None or content == None:
            self.render('ask.html', name=name)
            return
        if title == "" or tags == "" or content == "":
            self.render('ask.html', name=name)
            return
        thisquestion = question('0', '0', '回答', '0',\
                                name, '刚刚', title, tags.split(','))
        thisquestion.set_question(path)
        self.redirect("/")

if __name__ == "__main__":
    APP = tornado.web.Application(
        handlers=[(r'/', MainHandler), (r'/login', LoginHandler),\
                  (r'/logout', LogoutHandler), (r'/signup', SignInHandler),\
                  (r'/ask', AskHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        autoescape=None,
        debug=True
    )
    HTTP_SERVER = tornado.httpserver.HTTPServer(APP)
    HTTP_SERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
