"""
小说信息结构体
小说名     作者      种类      链接      封面      作者链接
"""


class Novel(object):
    def __init__(
            self,
            name='',
            author='',
            kind='',
            link='',
            pic='',
            author_link=''):
        self.name = name
        self.author = author
        self.kind = kind
        self.link = link
        self.pic = pic
        self.author_link = author_link
