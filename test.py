from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver

pphjs_path = r"F:\phantomjs-2.1.1-windows\bin\phantomjs.exe"
driver = webdriver.PhantomJS(executable_path=pphjs_path)
url = "http://book.qidian.com/info/1209977#Catalog"
driver.get(url)

url = urlopen(url)
bs = BeautifulSoup(url, 'html.parser')
print(bs.find("div", {"class": "volume"}))
#
# i = driver.find_element_by_class_name("volume").text
# print(i)
