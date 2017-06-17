"""
每日推荐爬虫
"""
import os
import re
import sys
from urllib.request import quote
from urllib.request import urlopen
from bs4 import BeautifulSoup
from model.novel_struct import Novel

def recommend_from_qidian():
    url = "http://r.qidian.com/click"
    url = urlopen(url)
    bs = BeautifulSoup(url,'lxml')
    recommend_list = bs.find('div',{"class":"book-img-text"})
    if not recommend_list:
        return "not find recommend!"
    novel_list = []
    for ri in recommend_list.findAll("li"):
        novel = Novel()
        novel.pic = ri.find("div",{"class":"book-img-box"}).find("a").attrs['href']
        novel.link = ri.find("div",{"class":"book-right-info"}).find("p",{"class":"btn"}).find("a").attrs['href']
        novel.name = ri.find("div",{"class":"book-mid-info"}).find("h4").getText("\n")
        novel.author = ri.find("div",{"class":"book-mid-info"}).find("p",{"class":"author"}).find("a").getText("\n")
        novel.author_link =  ri.find("div",{"class":"book-mid-info"}).find("p",{"class":"author"}).find("a").attrs['href']
        novel.kind = ri.find("div",{"class":"book-mid-info"}).find("p",{"class":"author"}).findAll("a")[1].getText("\n")
        novel_list.append(novel)
    return novel_list
