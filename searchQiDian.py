'''
起点小说网指定搜索内容搜索
'''
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import os
from urllib.request import quote
def search(str):
    str = str.replace("\n","").replace(" ","")
    url = "http://se.qidian.com/?kw="+quote(str)
    url = urlopen(url)
    bs = BeautifulSoup(url,"lxml")

    result = bs.find("div",{"class":"book-img-text"}).findAll("li")
    link = []
    name = []
    writer = []
    pic = []
    type = []
    writer_link = []
    for i in result:
        temp = i.find("a").attrs["href"]
        link.append(temp)
        temp = i.find("h4").getText()
        name.append(temp)
        temp = i.find("a",{"class":"name"}).getText("\n")
        writer.append(temp)
        temp = i.find("p",{"class":"author"}).findAll("a")[1].getText()
        type.append(temp)
        temp = i.find("img").attrs["src"]
        pic.append(temp)
        temp = i.find("p",{"class":"author"}).findAll("a")[0].attrs["href"]
        writer_link.append(temp)
    return [name, writer, type, link, pic, writer_link]
    # str_dire = r"f:\novel\{}".format(str)
    # if not os.path.exists(str_dire):
    #     os.mkdir(str_dire)
    # for i in range(len(link)):
    #     if "http" in link[i]:
    #         continue
    #     url = "http:"+link[i]+"#Catalog"
    #     directory = r"f:\novel\{}\{}".format(str, name[i])
    #     print("{}开始下载".format(name[i]))
    #     if not os.path.exists(directory):
    #         os.mkdir(directory)
    #     url = urlopen(url)
    #
    #     bs = BeautifulSoup(url,"lxml")
    #     try:
    #         f = bs.findAll("div",{"class":"volume-wrap"})
    #     except AttributeError as e:
    #         # print(e)
    #         continue
    #     for fi in f:
    #         if  "免费" not in fi.find("h3").find("span").getText() :
    #             continue
    #         for fii in fi.findAll("li",{"data-rid":re.compile(r'\d*')}):
    #             chapter_name = fii.getText("\n").replace("\n","")
    #             chapter_dire = r"{}\{}.txt".format(directory,chapter_name)
    #             chapter_file = open(chapter_dire, 'wb+')
    #             try:
    #                 chapter_url = "http:" + fii.find("a").attrs["href"]
    #                 # print(chapter_url)
    #                 chapter_url = urlopen(chapter_url)
    #                 chapter_bs = BeautifulSoup(chapter_url, "lxml")
    #                 chapter_book = chapter_bs.find("div", {"class": "read-content j_readContent"})
    #                 chapter_file.write(chapter_book.getText("\n").encode("gbk","ignore"))
    #                 print(chapter_url)
    #             except AttributeError as e:
    #                 continue
    #             finally:
    #                 chapter_file.close()
    #     print("{}下载成功,保存在{}目录下".format(name[i], directory))
    #
