from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "catzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home_page():
    # render the homepage
    return redirect('/users')

@app.route('/users')
def list_users():
    """Show list of all users in db"""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def new_user():
    """Show a form to add a new user"""
    return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    """post info from new user form to db"""
    first_name = request.form['first_name'] 
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else None
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')    
def edit_user(user_id):
    """Show a form for editing a user"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])    
def submit_edit(user_id):
    "submit changes in form to db"
    edited_user = User.query.get_or_404(user_id)

    edited_user.first_name = request.form['first_name'] 
    edited_user.last_name = request.form['last_name']
    edited_user.image_url = request.form['image_url']

    db.session.add(edited_user)
    db.session.commit()
    return render_template('details.html', user=edited_user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user"""
    deleted_user = User.query.get_or_404(user_id)

    db.session.delete(deleted_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def creat_new_post(user_id):
    """Display a form for a user to create a new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('new_post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def commit_new_post(user_id):
    """Commit post from submitted form"""
    user = User.query.get_or_404(user_id)

    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tagcheckbox')
    new_post = Post(title=title, content=content, user=user)
    for t in tags:
        tag = Tag.query.get_or_404(t)
        new_post.tags.append(tag)
        
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show details about a single post"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit_form(post_id):
    """leads to form to edit post"""
    post = Post.query.get_or_404(post_id)
    post_tags = post.tags
    all_tags = Tag.query.all()
    return render_template('edit_post.html', post=post, post_tags=post_tags, all_tags=all_tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def submit_post_edit(post_id):
    """Submit changes to post from edit form"""
    post = Post.query.get_or_404(post_id)
    new_tags = request.form.getlist('tagcheckbox')
    post.tags = Tag.query.filter(Tag.id.in_(new_tags)).all()

    
    post.title = request.form['title']
    post.content = request.form['content']
    
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete post"""
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')

@app.route('/tags')
def list_tags():
    """show all tags"""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    """Show the details about the tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_details.html', tag=tag)

@app.route('/tags/new')
def tag_add_form():
    """show a form to add a new tag"""
    return render_template('new_tag.html')

@app.route('/tags/new', methods=['POST'])
def commit_new_tag():
    """ Commit tag from form"""

    name = request.form['name']

    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return redirect(f'/tags')

@app.route('/tags/<int:tag_id>/edit')
def tag_edit_form(tag_id):
    """Leads to tag edit form"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def commit_tag_edit(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    tag.name = request.form['name']

    
    db.session.add(tag)
    db.session.commit()

    return redirect(f'/tags/{tag_id}')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Delete the tag"""
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')


