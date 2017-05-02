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
    return render_template("search_result.html",novel=n_list[0:10])
n = []
@app.route('/novel_search/page=<int:page>')
def part_page(page=1):
    if page*10 > len(n_list):
        abort(404)
    else:
        pa = page
        return render_template('search_result.html', novel=n_list[(page-1)*10 : page*10])

@app.route('/novel_search/page_next')
def next():
    if pa > 5:
        abort(404)
    else:
        return render_template('search_result.html',novel=n_list[pa*10 : (pa+1)*10])
n = 87
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
    dire = zipBook(name)
    return render_template("download.html")

def convert(obj):
    d = {}
    d.update(obj.__dict__)
    return d

if __name__ == "__main__":
    app.run(debug=True,port=5000)