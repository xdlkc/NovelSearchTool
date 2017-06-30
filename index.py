"""
服务器后台
"""
import json

from flask import Flask, render_template, request
from biz.json_tool import convert_to_json
from biz.zip import zip_book
from control.search_and_download import *

app = Flask(__name__)
port = 12138
host = "127.0.0.1"


@app.route('/')
@app.route('/main.html')
def index():
    return render_template('main.html')

@app.route("/recommend.html")
def recommend():
    return render_template("")

@app.route('/novel_search/<key>', methods=['POST'])
def search_novel(key):
    text = request.form.get('content')
    text = r"{}".format(text)
    novel = search_from_qidian(text)
    if not novel:
        return render_template("page_not_found.html")
    return render_template(
        "search_result_all.html",
        novel=json.dumps(
            novel,
            default=convert_to_json))


@app.route('/novel_search/<key>/download/<author>/<name>', methods=['POST'])
def do(key, author, name):
    fp = open("{}/key/{}.txt".format(sys.path[0], key), 'r')
    for f in fp.readlines():
        l = f.split(" ")
        if l[0] == name and l[1] == author:
            novel = Novel(l[0], l[1], l[2], l[4], l[3], l[5])
            download(novel)
    fp.close()
    zip_book(name)
    dire = "http://{}:{}/static/books/{}.zip".format(host, port, name)
    return render_template("download.html", dire=dire, name=name)


@app.route('/author.html')
def author():
    return render_template("author.html")


@app.route('/team_introduce.html')
def team_introduce():
    return render_template('team_introduce.html')


@app.route('/introduce.html')
def introduce():
    return render_template('introduce.html')


if __name__ == "__main__":
    app.run(port=port, host=host)
