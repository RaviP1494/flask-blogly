"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User

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
    return render_template('user.html', u = u)

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

