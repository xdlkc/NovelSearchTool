import zipfile

from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import os
from novel import Novel
from urllib.request import quote
# from  searchQiDian import *

def zipBook(name):
    dire = r'/home/lkc/code/python/PycharmProjects/flask2/books/{}'.format(name)
    z = zipfile.ZipFile(dire+".zip", 'w')
    if os.path.isdir(dire):
        for d in os.listdir(dire):
            z.write(dire + os.sep + d)
        z.close()
    return dire + ".zip"
# make_targz_one_by_one(dire,dire+r"/")
f = zipBook("大主宰")
print(f)