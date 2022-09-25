"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post

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
    return render_template('newpost.html', uid=uid)


@app.route('/users/<int:uid>/posts/new', methods=["POST"])
def make_post(uid):
    title = request.form.get('title')
    content = request.form.get('content')
    p = Post(title = title, content = content, uid = uid)
    db.session.add(p)
    db.session.commit()
    return redirect(f'/users/{uid}')

@app.route('/posts/<int:pid>')
def post_view(pid):
    p = Post.query.get(pid)
    return render_template('post.html', post = p)

@app.route('/posts/<int:pid>/edit')
def post_edit(pid):
    p = Post.query.get(pid)
    return render_template('editpost.html')

@app.route('/posts/<int:pid>/edit', methods=["POST"])
def post_update(pid):
    title = request.form.get('title')
    content = request.form.get('content')
    p = Post.query.get(pid)
    p.title = title
    p.content = content
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



