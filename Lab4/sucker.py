#coding:utf-8
"""
student number:13331235
name: TanXiao
head: Web2.0-Lab4
"""
import os.path
import re

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

def validate_card(cardnumber, cardtype):
    """
    判断卡号是否有效
    """
    validate = re.compile(r'\d{4}\D*\s*\d{4}\D*\s*\d{4}\D*\s*\d{4}\D*\s*')
    if validate.search(cardnumber):
        if cardnumber[0] == '4' and cardtype == 'visa':
            return True
        elif cardnumber[0] == '5' and cardtype == 'mastercard':
            return True
    return False

def get_userprofile(path):
    """
    从suckers.txt中读取表单数据
    """
    thefile = open(os.path.join(path, 'suckers.txt'), 'r')
    userprofile = thefile.read().splitlines()
    users = []
    for everyuser in userprofile:
        temp = everyuser.split(';')
        oneuser = Userinfo((temp[0]), (temp[1]), (temp[2]), (temp[3]))
        users.append(oneuser)
    return users

class Userinfo:
    """
    存储信息
    """
    def __init__(self, name, section, cardnumber, cardtype):
        self.name = name
        self.section = section
        self.cardnumber = cardnumber
        self.cardtype = cardtype

    def set_userprofile(self, path):
        """
        将表单数据写入suckers.txt中
        """
        thefile = open(os.path.join(path, 'suckers.txt'), 'a')
        thefile.write(self.name+';'+self.section+';'\
                     +self.cardnumber+';'+self.cardtype\
                     +'\n')
        thefile.close()

class MainHandler(tornado.web.RequestHandler):
    """
    MainHandler
    """
    def get(self):
        self.render('buyagrade.html')

class SuckerHandler(tornado.web.RequestHandler):
    """
    SuckerHandler
    """
    def get(self):
        back = self.get_argument("back", None)
        if back != None:
            return self.redirect("/")

        username = self.get_argument('name', None)
        section = self.get_argument('section', None)
        cardnumber = self.get_argument('cardnumber', None)
        cardtype = self.get_argument('cardtype', None)
        completed = False
        rightcard = False
        user = None
        userlist = None

        if username != "" and cardnumber != "":
            completed = True
            rightcard = validate_card(cardnumber, cardtype)
            if rightcard == True:
                # 将卡号中的字符去掉
                tempnum = ''
                for x_loop in range(0, len(cardnumber)):
                    if cardnumber[x_loop] >= '0' and cardnumber[x_loop] <= '9':
                        tempnum += cardnumber[x_loop]
                cardnumber = tempnum
                user = Userinfo(username, section, cardnumber, cardtype)
                path = os.path.join(os.path.dirname(__file__), "static")
                user.set_userprofile(path)
                userlist = get_userprofile(path)
        self.render(
            'sucker.html',
            back=back,
            completed=completed,
            rightcard=rightcard,
            user=user,
            userlist=userlist
        )

if __name__ == "__main__":
    APP = tornado.web.Application(
        handlers=[(r'/', MainHandler), (r'/sucker', SuckerHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        autoescape=None,
        debug=True
    )
    HTTP_SERVER = tornado.httpserver.HTTPServer(APP)
    HTTP_SERVER.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
