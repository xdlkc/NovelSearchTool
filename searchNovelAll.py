'''
SoDu上搜索小说
'''
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import os
from urllib.request import quote
from novel import Novel
from selenium import webdriver

def search(str):
    novel = []

    url = "http://book.easou.com/w/index.html"
    chrome = webdriver.Chrome()
    chrome.get(url)
    chrome.find_element_by_class_name("q").clear()
    chrome.find_element_by_class_name("q").send_keys(str)
    # chrome.find_element_by_class_name()
    # url = urlopen(url)
    # bs = BeautifulSoup(url,'lxml')
    # # 获得所有小说体的结构
    # print(bs)
    # n = bs.find("ul").findAll("li")
    # for ni in n:
    #     pic = ni.find("img").attrs["src"]
    #     novel_link = "http://book.easou.com/" + ni.find("div",{"class":"name"}).find("a",{"class":"common"}).attrs["href"]
    #     name = ni.find("div",{"class":"name"}).find("a",{"class":"common"}).getText()
    #     author_link ="http://book.easou.com/" +  ni.find("span",{"class":"author"}).find("a",{"class":"common"}).attrs["href"]
    #     author = ni.find("span",{"class":"author"}).find("a",{"class":"common"}).getText()
    #     kind = ni.find("span",{"class":"kind"}).find("a",{"class":"common"}).getText()
    #     novel.append(Novel(name,author,kind,novel_link,pic,author_link))
    # return novel
    #

if __name__ == '__main__':
    search("斗破苍穹")