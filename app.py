"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:drowssap@localhost:5432/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def user_list():
    ulist = User.query.all()
    return render_template('userlist.html', ulist = ulist)

@app.route('/users/new')
def new_user():
    return render_template('newuser.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    img_url = request.form.get('img_url')
    u = User(first_name = fname, last_name = lname, img_url = img_url)
    db.session.add(u)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:uid>')
def user_view(uid):
    u = User.query.get(uid)
    posts = u.posts
    return render_template('user.html', u = u, posts = posts)

@app.route('/users/<int:uid>/edit')
def user_edit(uid):
    return render_template('edituser.html')
    
@app.route('/users/<int:uid>/edit', methods=["POST"])
def user_update(uid):
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    img_url = request.form.get('img_url')

    u = User.query.get(uid)
    
    u.first_name = fname
    u.last_name = lname
    u.img_url = img_url

    db.session.add(u)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:uid>/delete', methods=["POST"])
def user_delete(uid):
    u = User.query.get(uid)
    db.session.delete(u)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:uid>/posts/new')
def new_post(uid):
    tags = Tag.query.all()
    return render_template('newpost.html', uid=uid, tags = tags)


@app.route('/users/<int:uid>/posts/new', methods=["POST"])
def make_post(uid):
    title = request.form.get('title')
    content = request.form.get('content')
    print(request.form.getlist("tags"))
    tids = [tid for tid in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tids)).all()
    p = Post(title = title, content = content, uid = uid, tags = tags)
    db.session.add(p)
    db.session.commit()
    return redirect(f'/users/{uid}')

@app.route('/posts/<int:pid>')
def post_view(pid):
    p = Post.query.get(pid)
    tags = p.tags
    return render_template('post.html', post = p, tags = tags)

@app.route('/posts/<int:pid>/edit')
def post_edit(pid):
    p = Post.query.get(pid)
    tags = Tag.query.all()
    return render_template('editpost.html', tags = tags)

@app.route('/posts/<int:pid>/edit', methods=["POST"])
def post_update(pid):
    title = request.form.get('title')
    content = request.form.get('content')
    tids = [tid for tid in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tids)).all()
    p = Post.query.get(pid)
    p.title = title
    p.content = content
    p.tags = tags
    db.session.add(p)
    db.session.commit()
    return redirect(f'/users/{p.user.id}')

@app.route('/posts/<int:pid>/delete', methods=["POST"])
def post_delete(pid):
    p = Post.query.get(pid)
    print(p.user.id)
    db.session.delete(p)
    db.session.commit()
    return redirect (f'/users/{p.user.id}')

@app.route('/tags/new')
def new_tag():
    return render_template('/newtag.html')

@app.route('/tags/new', methods=["POST"])
def add_tag():
    tag = request.form.get('tag')
    t = Tag(name=tag)
    db.session.add(t)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags')
def tag_list():
    tags = Tag.query.all()
    return render_template('/taglist.html', tags = tags)

@app.route('/tags/<int:tid>')
def tag_view(tid):
    t = Tag.query.get(tid)
    posts = t.posts
    return render_template('/tag.html', tag = t, posts = posts)

@app.route('/tags/<int:tid>/edit')
def tag_edit(tid):
    t = Tag.query.get(tid)
    return render_template('/edittag.html', tag = t)

@app.route('/tags/<int:tid>/edit', methods=["POST"])
def tag_update(tid):
    name = request.form.get(tag)
    t = Tag.query.get(tid)
    t.name = name
    db.session.add(t)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tid>/delete', methods=["POST"])
def tag_delete(tid):
    t = Tag.query.get(tid)
    db.session.delete(t)
    db.session.commit()
    return redirect('/tags')