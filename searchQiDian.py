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

link = []
name = []
writer = []
pic = []
type = []
writer_link = []

def search(str):
    page_count = 1
    str = str.replace("\n","").replace(" ","")
    base_url = "http://se.qidian.com/?kw="+quote(str) + "&page="
    url =base_url + "{}".format(page_count)
    while True:
        url = urlopen(url)
        bs = BeautifulSoup(url, "lxml")
        if bs.find('span',{"class":"no-data-img"}):
            break
        result = bs.find("div", {"class": "book-img-text"}).findAll("li")
        for i in result:
            temp = i.find("a").attrs["href"]
            link.append(temp)
            a = temp
            temp = i.find("h4").getText()
            name.append(temp)
            b = temp
            temp = i.find("a", {"class": "name"}).getText("\n")
            writer.append(temp)
            temp = i.find("p", {"class": "author"}).findAll("a")[1].getText()
            type.append(temp)
            temp = i.find("img").attrs["src"]
            pic.append(temp)
            temp = i.find("p", {"class": "author"}).findAll("a")[0].attrs["href"]
            writer_link.append(temp)
        if page_count == 10:
            break
        page_count += 1
        url = base_url + "{}".format(page_count)
    return [name, writer, type, link, pic, writer_link]

def download(novel):
    str_dire = r"/home/lkc/code/python/PycharmProjects/flask2/static/books/{}".format(novel.name)
    link = novel.link
    name = novel.name
    if not os.path.exists(str_dire):
        os.mkdir(str_dire)
    else:
        return r'/home/lkc/code/python/PycharmProjects/flask2/static/books/{}'.format(name)
    if "http" in link:
        url = link + "#Catalog"
    else:
        url = "http:" + link + "#Catalog"
    directory = str_dire
    url = urlopen(url)

    bs = BeautifulSoup(url, "lxml")
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
    return r'/home/lkc/code/python/PycharmProjects/flask2/static/books/{}'.format(name)

# 压缩小说
def zipBook(name):
    dire = r'/home/lkc/code/python/PycharmProjects/flask2/static/books/{}'.format(name)
    z = zipfile.ZipFile(dire+".zip", 'w')
    if os.path.isdir(dire):
        for d in os.listdir(dire):
            z.write(dire + os.sep + d, name+os.sep+d)
        z.close()
    return dire + ".zip"
if __name__ == '__main__':
    search("天残土豆")
    print(link[0])
    print(name[0])