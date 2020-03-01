import os
import datetime
import random

from flask_login import current_user, login_required, login_user, logout_user

from watchlist import app, db
from flask import request, redirect, url_for, flash, render_template, make_response, session

from watchlist.models import Articles, User


# 首页
@app.route('/')
def index():
    articles = Articles.query.all()
    return render_template('index.html', articles=articles)


# 查看博客
@app.route('/blog/lblog/<int:blog_id>')
def look_blog(blog_id):
    blog = Articles.query.get_or_404(blog_id)
    return render_template('look_blog.html', articles=blog)


# 我的博客页面
@app.route('/blog/myblog')
@login_required
def my_blog():
    articles = Articles.query.filter_by(user_id=current_user.id)
    return render_template('my_blog.html', articles=articles)


# 发布博客页面
@app.route('/blog/cblog', methods=['GET', 'POST'])
@login_required
def create_blog():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        # print(title, '\n', content)
        if not title or not content:
            flash('标题或内容未填写')
            return redirect(url_for('create_blog', title=title, content=content))

        elif len(title) > 20:
            flash('标题长度不符--[len<20]')
            return redirect(url_for('create_blog', title=title, content=content))

        elif len(content) > 50000:
            flash('内容过长~~~~[len<50000]')
            return redirect(url_for('create_blog', title=title, content=content))
        article = Articles(title=title, content=content, author=current_user.name, user_id=current_user.id)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('my_blog'))
    return render_template('create_blog.html')


# 编辑博客信息页面
@app.route('/blog/edit/<int:blog_id>', methods=["GET", "POST"])
@login_required
def edit(blog_id):
    articles = Articles.query.get_or_404(blog_id)

    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash('标题或内容未填写')
            return redirect(url_for('create_blog', title=title, content=content))

        elif len(title) > 20:
            flash('标题长度不符--[len<20]')
            return redirect(url_for('create_blog', title=title, content=content))

        elif len(content) > 50000:
            flash('内容过长~~~~[len<50000]')
        articles.title = title
        articles.content = content
        db.session.commit()
        flash('博客信息已经更新')
        return redirect(url_for('index'))
    return render_template('edit.html', articles=articles)


# 修改用户昵称
@app.route('/user/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('输入错误')
            return redirect(url_for('settings'))
        current_user.name = name
        db.session.commit()
        flash('设置name成功')
        return redirect(url_for('index'))

    return render_template('settings.html')


# 删除博客
@app.route('/blog/delete/<int:blog_id>', methods=["POST"])
@login_required
def delete(blog_id):
    article = Articles.query.get_or_404(blog_id)
    db.session.delete(article)
    db.session.commit()
    flash('删除成功')
    return redirect(url_for('index'))


# 用户登录 flask提供的login_user()函数
@app.route('/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('输入错误')
            return redirect(url_for('login'))
        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登录成功
            flash('登陆成功')
            return redirect(url_for('index'))  # 登陆成功返回首页
        flash('用户名或密码输入错误')
        return redirect(url_for('login'))
    return render_template('login.html')


# 用户登出
@app.route('/user/logout')
def logout():
    logout_user()
    flash('退出登录')
    return redirect(url_for('index'))


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


@app.route('/upload/', methods=['POST', 'OPTIONS'])
def upload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        filepath = os.path.join(app.static_folder, 'upload', rnd_name)
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
    else:
        error = 'post error'
    res = """<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


@app.route('/test/')
def test():
    return render_template('test.html')
