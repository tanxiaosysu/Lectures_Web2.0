#coding:utf-8
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

def get_userprofile(path):
    """
    从singles.txt中读取表单数据
    """
    thefile = open(os.path.join(path, 'singles.txt'), 'r')
    userprofile = thefile.read().splitlines()
    users = []
    for everyuser in userprofile:
        temp = everyuser.split(',')
        oneuser = Userinfo(temp[0], temp[1], temp[2], temp[3],\
                           temp[4], temp[5], temp[6], temp[7])
        users.append(oneuser)
    return users

class Userinfo(object):
    """
    存储信息
    """
    def __init__(self, name, gender, age, persontype,\
                 section, seeking, lowage, highage):
        self.name = name
        self.gender = gender
        self.age = age
        self.persontype = persontype
        self.section = section
        self.seeking = seeking
        self.lowage = lowage
        self.highage = highage

    def match(self, otheruser):
        """
        判断是否匹配
        """
        for x_loop in otheruser.seeking:
            if self.gender == x_loop:
                return True
        return False

    def dimension(self, otheruser):
        """
        计算匹配度
        """
        output = 0
        if int(self.age) >= int(otheruser.lowage)\
            and int(self.age) <= int(otheruser.highage):
            output += 1
        if self.section == otheruser.section:
            output += 2
        for x_loop in range(0, 4):
            if self.persontype[x_loop] == otheruser.persontype[x_loop]:
                output += 1
        return output

    def validate(self):
        """
        检查信息正确性
        """
        if self.completed() == False:
            return False
        # 输入年龄为非数字
        for x_loop in self.age:
            if x_loop < '0' or x_loop > '9':
                return False
        for x_loop in self.lowage:
            if x_loop < '0' or x_loop > '9':
                return False
        for x_loop in self.highage:
            if x_loop < '0' or x_loop > '9':
                return False
        # 输入最小年龄和最大年龄范围错误(HTML已经保证输入年龄最大为两位数)
        if int(self.highage) < int(self.lowage):
            return False
        # 输入个性错误
        if len(self.persontype) != 4:
            return False
        if self.persontype[0] != 'I' and self.persontype[0] != 'E':
            return False
        if self.persontype[1] != 'N' and self.persontype[1] != 'S':
            return False
        if self.persontype[2] != 'F' and self.persontype[2] != 'T':
            return False
        if self.persontype[3] != 'J' and self.persontype[3] != 'P':
            return False
        return True

    def completed(self):
        """
        检查信息是否完整
        """
        if self.name == "" or self.age == "" or self.persontype == ""\
            or self.lowage == "" or self.highage == "" or self.seeking == "":
            return False
        return True

    def imagefilename(self):
        """
        返回图片文件名
        """
        name = ""
        for x_loop in range(0, len(self.name)):
            if self.name[x_loop] == ' ':
                name += '_'
            else:
                name += self.name[x_loop]
        return name

    def set_userprofile(self, path):
        """
        将表单数据写入singles.txt中
        """
        thefile = open(os.path.join(path, 'singles.txt'), 'a')
        thefile.write(self.name+','+self.gender+','\
                     +self.age+','+self.persontype+','\
                     +self.section+','+self.seeking+','\
                     +self.lowage+','+self.highage+'\n')
        thefile.close()

class MainHandler(tornado.web.RequestHandler):
    """
    MainHandler
    """
    def get(self):
        self.render('index.html')

class ResultsPageHandler(tornado.web.RequestHandler):
    """
    ResultsPageHandler
    """
    def get(self):
        back = self.get_argument("back", None)
        if back != None:
            return self.redirect("/")

        name = self.get_argument('name', None)
        gender = self.get_argument('gender', None)
        age = self.get_argument('age', None)
        persontype = self.get_argument('persontype', None)
        section = self.get_argument('section', None)
        lowage = self.get_argument('lowage', None)
        highage = self.get_argument('highage', None)

        seeking = ""
        if self.get_argument('seekingm', None) != None:
            seeking += self.get_argument('seekingm', None)
        if self.get_argument('seekingf', None) != None:
            seeking += self.get_argument('seekingf', None)
        login_user = Userinfo(name, gender, age, persontype,\
                             section, seeking, lowage, highage)
        completed = login_user.completed()
        validateinfo = login_user.validate()
        userlist = None

        if completed == True and validateinfo == True:
            path = os.path.join(os.path.dirname(__file__), "static")
            userlist = get_userprofile(path)
            userlist = filter(lambda x: login_user.match(x)\
                              and login_user.dimension(x) >= 3, userlist)
            login_user.set_userprofile(path)

        self.render(
            'results.html',
            back=back,
            completed=completed,
            validateinfo=validateinfo,
            user=login_user,
            userlist=userlist
        )

if __name__ == "__main__":
    APP = tornado.web.Application(
        handlers=[(r'/', MainHandler), (r'/results', ResultsPageHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        autoescape=None,
        debug=True
    )
    HTTP_SERVER = tornado.httpserver.HTTPServer(APP)
    HTTP_SERVER.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
