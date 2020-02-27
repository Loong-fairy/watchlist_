import click
from watchlist import app, db

# 自定义initdb
from watchlist.models import Movie, User


@app.cli.command()
@click.option('--drop', is_flag=True, help='删除之后在创建')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('初始化数据库')


# 自定义命令forge, 把数据写入数据库
@app.cli.command()
def forge():
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
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('数据导入完成')


# 生成管理员账号的函数
@app.cli.command()
@click.option('--username', prompt=True, help='用来登录的用户名')
@click.option('--password', prompt=True, hide_input=True, help='用来登录的密码', confirmation_prompt=True)
def admin(username, password):
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('更新用户')
        user.username = username
        user.set_password(password)
    else:
        click.echo('创建用户')
        user = User(username=username, name="Admin")
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('创建管理员账号完成')
