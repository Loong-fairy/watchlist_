import click
from watchlist import app, db

# 自定义initdb
from watchlist.models import Articles, User


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
    articles = [
        {'title': '1', 'content': '1', 'author': '1', 'user_id': 1},
        {'title': '2', 'content': '2', 'author': '2', 'user_id': 1},
        {'title': '3', 'content': '3', 'author': '3', 'user_id': 1},
        {'title': '4', 'content': '4', 'author': '4', 'user_id': 1},
        {'title': '5', 'content': '5', 'author': '5', 'user_id': 1},
        {'title': '6', 'content': '6', 'author': '6', 'user_id': 1},
        {'title': '7', 'content': '7', 'author': '7', 'user_id': 1},
        {'title': '8', 'content': '8', 'author': '8', 'user_id': 1},
        {'title': '9', 'content': '9', 'author': '9', 'user_id': 1},
        {'title': '10', 'content': '10', 'author': '10', 'user_id': 1}
    ]
    user = User(name=name)
    db.session.add(user)
    for a in articles:
        blog = Articles(title=a['title'], content=a['content'], author=a['author'], user_id=a['user_id'])
        db.session.add(blog)

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
        user = User(username=username, name="Long")
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('创建管理员账号完成')
