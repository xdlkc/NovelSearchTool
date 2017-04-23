'''
服务器后台
'''
from flask import Flask,render_template,url_for,request,send_file
from novel import Novel
from searchQiDian import search
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/novel_search',methods=['POST'])
def search_novel():
    form = request.form
    text = form.get('content')
    novel_list = search(text)
    n_list = []
    for i in range(len(novel_list[0])):
        n = Novel(novel_list[0][i], novel_list[1][i],novel_list[2][i],novel_list[3][i],novel_list[4][i], novel_list[5][i])
        n_list.append(n)
    return render_template('search_result.html',text=text, novel=n_list)

@app.route('/author.html')
def author():
    return render_template("author.html")
if __name__ == "__main__":
    app.run(debug=True,port=5000)