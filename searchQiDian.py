'''
起点小说网指定搜索内容搜索
'''
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import os
from urllib.request import quote
import os,zipfile,tarfile
import sys
from novel import Novel


# 查找小说
def search(str):
    novel = []
    page_count = 1
    str_dir = r"{}/key/{}.txt".format(sys.path[0],str)
    if not os.path.exists(str_dir):
        fp = open(str_dir,'w')
        flag = True
    else:
        fp = open(str_dir, 'r')
        flag = False
        #     for f in fp.readlines():
        #         l = f.split(" ")
        #         novel.append(Novel(l[0],l[1],l[2],l[4],l[3],l[5]))
        #         # print(l)
    str = str.replace("\n", "").replace(" ", "")
    base_url = "http://se.qidian.com/?kw=" + quote(str) + "&page="
    url = base_url + "{}".format(page_count)
    while True:
        url = urlopen(url)
        bs = BeautifulSoup(url, "lxml")
        if bs.find('span', {"class": "no-data-img"}):
            break
        result = bs.find("div", {"class": "book-img-text"}).findAll("li")
        for i in result:
            temp = i.find("h4").getText()
            name = temp

            temp = i.find("a", {"class": "name"}).getText("\n")
            author = temp

            temp = i.find("p", {"class": "author"}).findAll("a")[1].getText()
            kind = temp

            temp = i.find("img").attrs["src"]
            pic = temp

            temp = i.find("a").attrs["href"]
            link = temp

            temp = i.find("p", {"class": "author"}).findAll("a")[0].attrs["href"]
            author_link = temp
            if flag:
                fp.write("{} {} {} {} {} {}\n".format(name,author,kind,link,pic,author_link))
            novel.append(Novel(name, author, kind, link, pic, author_link))
        if page_count == 10:
            break
        page_count += 1
        url = base_url + "{}".format(page_count)
    fp.close()
    return novel

# 查找某个小说的链接
def find(key, name, author):

    fp = open(r"{}.txt".format(key), 'r')
    for f in fp.readlines():
        l = f.split(" ",7)
        if l[0] == name and l[1] == author:
            return Novel(l[0],l[1],l[2],l[4],l[3],l[5])
    fp.close()
    return

# 下载
def download(novel):
    str_dire = r"{}/static/books/{}".format(sys.path[0],novel.name)
    link = novel.link
    name = novel.name
    if not os.path.exists(str_dire):
        os.mkdir(str_dire)
    else:
        return r'{}/static/books/{}'.format(sys.path[0],name)
    if "http" in link:
        url = link + "#Catalog"
    else:
        url = "http:" + link + "#Catalog"
    directory = str_dire
    url = urlopen(url)

    bs = BeautifulSoup(url, "html5lib")
    try:
        f = bs.findAll("div", {"class": "volume-wrap"})
    except AttributeError as e:
        # print(e)
        return
    for fi in f:
        if "免费" not in fi.find("h3").find("span").getText():
            continue
        for fii in fi.findAll("li", {"data-rid": re.compile(r'\d*')}):
            chapter_name = fii.getText("\n").replace("\n", "")
            chapter_dire = r"{}/{}.txt".format(directory, chapter_name)
            chapter_file = open(chapter_dire, 'wb+')
            try:
                chapter_url = "http:" + fii.find("a").attrs["href"]
                # print(chapter_url)
                chapter_url = urlopen(chapter_url)
                chapter_bs = BeautifulSoup(chapter_url, "lxml")
                chapter_book = chapter_bs.find("div", {"class": "read-content j_readContent"})
                chapter_file.write(chapter_book.getText("\n").encode("gbk", "ignore"))
            except AttributeError as e:
                continue
            finally:
                chapter_file.close()
    return r'{}/static/books/{}'.format(sys.path[0],name)

# 压缩小说
def zipBook(name):
    dire = r'{}/static/books/{}'.format(sys.path[0],name)
    z = zipfile.ZipFile(dire+".zip", 'w')
    if os.path.isdir(dire):
        for d in os.listdir(dire):
            z.write(dire + os.sep + d, name+os.sep+d)
        z.close()
    return dire + ".zip"
