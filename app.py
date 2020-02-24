import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'sqlite.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控


db = SQLAlchemy(app)


@app.route('/')
def index():
    name = "Long"
    movies = [
        {'title': '杀破狼', 'year': '2003'},
        {'title': '扫毒', 'year': '2018'},
        {'title': '捉妖记', 'year': '2016'},
        {'title': '囧妈', 'year': '2020'},
        {'title': '葫芦娃', 'year': '1989'},
        {'title': '玻璃盒子', 'year': '2020'},
        {'title': '调酒师', 'year': '2020'},
        {'title': '釜山行', 'year': '2017'},
        {'title': '导火索', 'year': '2005'},
        {'title': '叶问', 'year': '2015'},
    ]
    return render_template('index.html', name=name, movies=movies)
