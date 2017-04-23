'''
小说信息结构体
'''
class Novel(object):
    def __init__(self, name, writer, type, link, pic, writer_link):
        self.name = name
        self.writter = writer
        self.type = type
        self.link = "http:"+link
        self.pic = "http:" + pic
        self.writer_link = writer_link
        self.intro = ''
    def get_intro(self, intro):
        self.intro += intro