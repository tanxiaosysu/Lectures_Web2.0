"""
student number:13331235
name: TanXiao
head: Web2.0-Lab3
content: exercise1 ~ exercise5
"""
import os.path
import re

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


TOTAL = os.listdir('static/songs')
SONGINFO = []
PLAYLIST = []
for x in range(0, len(TOTAL)):
    patsong = re.compile(r'mp3')
    if patsong.search(TOTAL[x]):
        filesize = os.path.getsize('static/songs/'+TOTAL[x])
        sizelevel = ''
        if filesize >= 1048576:
            filesize = round(filesize / 1048576.0, 2)
            sizelevel = ' mb'
        elif filesize >= 1024:
            filesize = round(filesize / 1024.0, 2)
            sizelevel = ' kb'
        else:
            sizelevel = ' b'
        # temp is a list to store the information of a song
        temp = [TOTAL[x], filesize, sizelevel]
        # SONGINFO is a list to store temp
        SONGINFO.append(temp)
    patplay = re.compile(r'txt')
    if patplay.search(TOTAL[x]):
        # use PLAYLIST to store the information of PLAYLISTs
        PLAYLIST.append(TOTAL[x])

class MainHandler(tornado.web.RequestHandler):
    """
    mainhandler
    """
    def get(self):
        # get listname
        _listname = self.get_argument('listname', 'None')
        if _listname != 'None':
            selectedlist = []
            with open(('static/songs/'+_listname), 'r') as file_load:
                templist = file_load.read().splitlines()
            for x_loop in range(0, len(SONGINFO)):
                for y_loop in range(0, len(templist)):
                    line = templist[y_loop]
                    if SONGINFO[x_loop][0] == line:
                        selectedlist.append(SONGINFO[x_loop])
                        break
            self.render(
                'music.html',
                returnlink=True,
                songslist=selectedlist,
                #if listname is exist, hire the PLAYLIST
                playlistlist=None
            )
        else:
            self.render(
                'music.html',
                returnlink=False,
                songslist=SONGINFO,
                playlistlist=PLAYLIST
            )

if __name__ == "__main__":
    APP = tornado.web.Application(
        handlers=[(r'/', MainHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    HTTP_SERVER = tornado.httpserver.HTTPServer(APP)
    HTTP_SERVER.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
