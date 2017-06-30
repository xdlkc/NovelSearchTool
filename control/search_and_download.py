"""
小说搜索模块
"""
import os
import re
import sys
from urllib.request import quote
from urllib.request import urlopen
from bs4 import BeautifulSoup
from model.novel_struct import Novel


def search_from_qidian(name):
    """
    起点中文网查找小说 http://www.qidian.com/
    :param name:
    :return:
    """
    novel = []
    page_count = 1
    str_dir = r"{}/key/{}.txt".format(sys.path[0], name)
    if not os.path.exists(str_dir):
        fp = open(str_dir, 'w')
        flag = True
    else:
        fp = open(str_dir, 'r')
        flag = False
    name = name.replace("\n", "").replace(" ", "")
    base_url = "http://se.qidian.com/?kw=" + quote(name) + "&page="
    url = base_url + "{}".format(page_count)
    while True:
        url = urlopen(url)
        bs = BeautifulSoup(url, "lxml")
        if bs.find('span', {"class": "no-data-img"}):
            break
        result = bs.find("div", {"class": "book-img-text"}).findAll("li")
        for i in result:
            novel_name = i.find("h4").getText()
            author = i.find("a", {"class": "name"}).getText("\n")
            kind = i.find("p", {"class": "author"}).findAll("a")[1].getText()
            pic = i.find("img").attrs["src"]
            link = i.find("a").attrs["href"]
            author_link = i.find("p", {"class": "author"}).findAll(
                "a")[0].attrs["href"]
            if flag:
                fp.write(
                    "{} {} {} {} {} {}\n".format(
                        novel_name,
                        author,
                        kind,
                        link,
                        pic,
                        author_link))
            novel.append(
                Novel(
                    novel_name,
                    author,
                    kind,
                    link,
                    pic,
                    author_link))
        if page_count == 10:
            break
        page_count += 1
        url = base_url + "{}".format(page_count)
    fp.close()
    return novel


def search_from_other(name):
    """
    从其他小说资源网站上搜索小说 http://www.zhaoxiaoshuo.com/
    :param name:
    :return:
    """
    novel = []
    page_count = 1
    str_dir = r"{}/key/{}.txt".format(sys.path[0], name)
    if not os.path.exists(str_dir):
        fp = open(str_dir, 'w')
        flag = True
    else:
        fp = open(str_dir, 'r')
        flag = False
    name = name.replace("\n", "").replace(" ", "")
    main_url = "http://www.zhaoxiaoshuo.com"
    base_url = "http://www.zhaoxiaoshuo.com/search?bookname=" + \
        quote(name) + "&author=&page="
    url = base_url + "{}".format(page_count)
    while True:
        url = urlopen(url)
        bs = BeautifulSoup(url, "lxml")
        if not bs.find("ul", {"class": "search_ul"}):
            break
        for fi in bs.find(
            "ul", {
                "class": "search_ul"}).findAll(
            "li", {
                "class": "padd"}):
            link = main_url + fi.find("a").attrs['href']
            novel_bs = BeautifulSoup(urlopen(url), "lxml")
            novel_name = novel_bs.find("div", {"class": "r420"})
            pic = main_url + novel_bs.find("div",
                                           {"class": "con_lwrap"}).find("div",
                                                                        {"class": "con_limg"}).find("img").attrs['src']
            author = novel_bs.find("p", {"class": "author"}).find(
                "span").getText("\n")
            kind = " "
            author_link = " "
            if flag:
                fp.write(
                    "{} {} {} {} {} {}\n".format(
                        novel_name,
                        author,
                        kind,
                        link,
                        pic,
                        author_link))
            novel.append(
                Novel(
                    novel_name,
                    author,
                    kind,
                    link,
                    pic,
                    author_link))
        if page_count == 10:
            break
        page_count += 1
        url = base_url + "{}".format(page_count)
    return novel


def find_from_disk(key, name, author):
    """
    查找某个小说的链接
    :param key:
    :param name:
    :param author:
    :return:
    """
    fp = open(r"{}.txt".format(key), 'r')
    for f in fp.readlines():
        l = f.split(" ", 7)
        if l[0] == name and l[1] == author:
            return Novel(l[0], l[1], l[2], l[4], l[3], l[5])
    fp.close()
    return


# 下载
def download(novel):
    str_dire = r"{}/static/books/{}".format(sys.path[0], novel.name)
    link = novel.link
    name = novel.name
    if not os.path.exists(str_dire):
        os.mkdir(str_dire)
    else:
        return r'{}/static/books/{}'.format(sys.path[0], name)
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
                chapter_url = urlopen(chapter_url)
                chapter_bs = BeautifulSoup(chapter_url, "lxml")
                chapter_book = chapter_bs.find(
                    "div", {"class": "read-content j_readContent"})
                chapter_file.write(
                    chapter_book.getText("\n").encode(
                        "gbk", "ignore"))
            except AttributeError as e:
                continue
            finally:
                chapter_file.close()
    return r'{}/static/books/{}'.format(sys.path[0], name)
