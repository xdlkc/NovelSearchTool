'''
服务器后台
'''
from flask import Flask,render_template,url_for,request,send_file,jsonify,abort,redirect
from novel import Novel
from searchQiDian import *
import json

app = Flask(__name__)
port = 80
host = "10.177.68.13"

def downloads(dire,name):
    return render_template("download.html",dire=dire,name=name)

@app.route('/')
@app.route('/main.html')
def index():
    return render_template('main.html')


@app.route('/novel_search/<key>',methods=['POST'])
def search_novel(key):
    text = request.form.get('content')
    text = r"{}".format(text)
    novel = search(text)
    if not novel:
        return render_template("NoResult.html")
    return render_template("search_result.html",novel=json.dumps(novel,default=convert))

@app.route('/novel_search/<key>/download/<author>/<name>', methods=['POST'])
def do(key,author, name):
    fp = open("{}/key/{}.txt".format(sys.path[0],key),'r')
    for f in fp.readlines():
        l = f.split(" ")
        if l[0] == name and l[1] == author:
            novel = Novel(l[0],l[1],l[2],l[4],l[3],l[5])
            download(novel)
    fp.close()
    zipBook(name)
    dire = "http://{}:{}/static/books/{}.zip".format(host,port,name)
    return render_template("download.html",dire=dire,name=name)

@app.route('/author.html')
def author():
    return render_template("author.html")

@app.route('/xinxi.html')
def xinxi():
    return render_template('xinxi.html')

@app.route('/jianjie.html')
def jianjie():
    return render_template('jianjie.html')

# 转化json对象
def convert(obj):
    d = {}
    d.update(obj.__dict__)
    return d

if __name__ == "__main__":
    app.run(port=port,host=host)