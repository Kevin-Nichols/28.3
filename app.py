"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag
from sqlalchemy.sql import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'hushhush'

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

########################################################### USERS ROUTES
@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def all_users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('index.html', users=users)

@app.route('/users/new', methods=['GET'])
def new_user_form():
    return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def new_users():
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None
    )
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def display_user(user_id):
    id = User.query.get(user_id)
    return render_template('users.html', user=id)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    id = User.query.get(user_id)
    return render_template('edit_user.html', user=id)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def submit_user_edit(user_id):
    id = User.query.get(user_id)
    id.first_name = request.form['first_name']
    id.last_name = request.form['last_name']
    id.image_url = request.form['image_url']
    db.session.add(id)
    db.session.commit()
    
    flash(f'{id.full_name} details were saved.')
    
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    id = User.query.get(user_id)
    db.session.delete(id)
    db.session.commit()
    
    flash(f'{id.full_name} has been deleted.')
    
    return redirect ('/users')

########################################################### POSTS ROUTES
@app.route('/users/<int:user_id>/posts/new')
def new_posts_form(user_id):
    id = User.query.get(user_id)
    tags = Tag.query.all()
    
    return render_template('new_post.html', user=id, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def new_posts(user_id):
    id = User.query.get(user_id)
    tag_id = [int(tag) for tag in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_id)).all()
    new_post = Post(title=request.form['title'], content=request.form['content'], user=id, tags=tags)
    db.session.add(new_post)
    db.session.commit()
    
    flash('New post added!')
    
    return redirect(f'/users/{user_id}')
    
@app.route('/posts/<int:post_id>')
def display_posts(post_id):
    id = Post.query.get(post_id)
    
    return render_template('posts.html', post=id)

@app.route('/posts/<int:post_id>/edit')
def edit_posts(post_id):
    id = Post.query.get(post_id)
    tags = Tag.query.all()
    
    return render_template('edit_post.html', post=id, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def submit_post_edit(post_id):
    id = Post.query.get(post_id)
    id.title = request.form['title']
    id.content = request.form['content']
    tag_id = [int(tag) for tag in request.form.getlist("tags")]
    id.tags = Tag.query.filter(Tag.id.in_(tag_id)).all()
    db.session.add(id)
    db.session.commit()
    
    flash(f'{id.title} details were saved.')
    
    return redirect(f"/users/{id.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    id = Post.query.get(post_id)
    db.session.delete(id)
    db.session.commit()
    
    flash(f'{id.title} has been deleted.')
    return redirect(f'/users/{id.user_id}')

########################################################### TAGS ROUTES
@app.route('/tags')
def tags_index():
    tags = Tag.query.all()
    
    return render_template('tags_index.html', tags=tags)

@app.route('/tags/new')
def new_tags_form():
    posts = Post.query.all()
    
    return render_template('new_tags.html', posts=posts)

@app.route("/tags/new", methods=["POST"])
def new_tags():
    post_ids = [int(tag) for tag in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    tag_name = Tag(name=request.form['name'], posts=posts)
    db.session.add(tag_name)
    db.session.commit()
    
    flash(f"'{tag_name.name}' has been added as a new tag.")
    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def display_tags(tag_id):
    id = Tag.query.get(tag_id)
    
    return render_template('display_tags.html', tag=id)

@app.route('/tags/<int:tag_id>/edit')
def edit_tags(tag_id):
    id = Tag.query.get(tag_id)
    posts = Post.query.all()
    
    return render_template('edit_tags.html', tag=id, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def submit_tag_edit(tag_id):
    id = Tag.query.get(tag_id)
    id.name = request.form['name']
    post_ids = [int(tag) for tag in request.form.getlist("posts")]
    id.posts = Post.query.filter(Post.id.in_(post_ids)).all()
    db.session.add(id)
    db.session.commit()
    
    flash(f"'{id.name}' details were saved.")
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    id = Tag.query.get(tag_id)
    db.session.delete(id)
    db.session.commit()
    
    flash(f"'{id.name}' has been deleted.")
    return redirect("/tags")