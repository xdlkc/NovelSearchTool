import zipfile

from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import os
from novel import Novel
from urllib.request import quote
from searchNovelAll import search
novel = search("斗破苍穹")
for i in novel:
    print("{}   {}  {}".format(i.name,i.link,i.kind))
    print("{}   {}  {}".format(i.pic, i.author_link, i.author))