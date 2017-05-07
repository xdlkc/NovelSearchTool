'''
服务器后台
'''
from flask import Flask,render_template,url_for,request,send_file,jsonify,abort
from novel import Novel
from searchQiDian import *
import json

app = Flask(__name__)
pa = 1
n_list = []
# host = " "
port = 5000
host = "127.0.0.1"

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/main.html')
def index1():
    return render_template('main.html')

@app.route('/novel_search',methods=['POST'])
def search_novel():
    form = request.form
    text = form.get('content')
    novel_list = search(text)
    for i in range(len(novel_list[0])):
        n = Novel(novel_list[0][i], novel_list[1][i],novel_list[2][i],novel_list[3][i],novel_list[4][i], novel_list[5][i])
        n_list.append(n)
    # return render_template('search_result.html',text=text, novel=n_list)
    return render_template("search_result.html",novel=json.dumps(n_list,default=convert))

@app.route('/author.html')
def author():
    return render_template("author.html")

@app.route('/xinxi.html')
def xinxi():
    return render_template('xinxi.html')

@app.route('/jianjie.html')
def jianjie():
    return render_template('jianjie.html')

@app.route('/novel_search/download/<name>', methods=['POST'])
def do(name):
    index = 0
    for i in range(len(n_list)):
        if n_list[i].name == name:
            index = i
            break
    name = n_list[index].name
    download(n_list[index])
    dire = zipBook(name)
    dire = "http://{}:{}/static/books/{}.zip".format(host,port,name)
    return render_template("download.html",dire=dire,name=name)

# 转化json对象
def convert(obj):
    d = {}
    d.update(obj.__dict__)
    return d

if __name__ == "__main__":
    app.run(debug=True,port=port,host=host)