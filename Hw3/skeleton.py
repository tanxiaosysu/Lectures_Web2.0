#coding:utf-8
"""
student number:13331235
name: TanXiao
head: Web2.0-Hw3
"""
import os.path
import re

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

def get_comments(path):
    """
    返回一个装有所有评论的表
    """
    filelist = os.listdir(path)
    comments = []

    for onefile in filelist:
        selectcomment = re.compile(r'review')
        if selectcomment.search(onefile):
            reviewtxt = open(os.path.join(path, onefile))
            review = reviewtxt.read().splitlines()
            review[1] = review[1].lower()
            comments.append(review)
    return comments

def getmovielist(path):
    filelist = os.listdir(path)
    movielist = []

    for onefile in filelist:
        select1 = re.compile(r'images')
        select2 = re.compile(r'stylesheets')
        if select1.search(onefile):
            pass
        elif select2.search(onefile):
            pass
        else:
            movielist.append(onefile)
    return movielist

class movie:
    """
    info: [0]:片名, [1]:年代, [2]:百分比, [3]:总评论数
    dt:右边栏小标题
    dd:右边栏内容
    comments:对于其中的每个comment,
             [0]:评论内容
             [1]:图标
             [2]:名字
             [3]:名字
    """
    def __init__(self, info, dt, dd, comments):
        self.info = info
        self.dt = dt
        self.dd = dd
        self.comments = comments

class MainHandler(tornado.web.RequestHandler):
    """
    mainhandler
    """
    def get(self):
        back = self.get_argument("back", None)
        moviename = self.get_argument('moviename', None)

        if back is not None:
            return self.redirect("/")
        if moviename is not None:
            path = os.path.join(os.path.dirname(__file__), "static/", moviename)
            # 读取info文件
            info_txt = open(os.path.join(path, 'info.txt'))
            Info = info_txt.read().splitlines()
            # 读取generaloverview文件
            dt_dd_txt = open(os.path.join(path, 'generaloverview.txt'))
            dt_dd = dt_dd_txt.read().splitlines()
            Dt = []
            Dd = []
            for everylist in dt_dd:
                Dt.append(everylist.split(':')[0])
                Dd.append(everylist.split(':')[1])
            # 读取review文件
            Review = get_comments(path)
            movieitem = movie(Info, Dt, Dd, Review)
            self.render(
                'skeleton.html',
                movielist=None,
                movieitem=movieitem,
                main=False
            )
        else:
            path = os.path.join(os.path.dirname(__file__), "static")
            movielist = getmovielist(path)
            self.render(
                'skeleton.html',
                movielist=movielist,
                movieitem=None,
                main=True
            )

if __name__ == "__main__":
    APP = tornado.web.Application(
        handlers=[(r'/', MainHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        autoescape=None,
        debug=True
    )
    HTTP_SERVER = tornado.httpserver.HTTPServer(APP)
    HTTP_SERVER.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
