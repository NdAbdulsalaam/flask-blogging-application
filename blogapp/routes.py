import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from blogapp import app, db, bcrypt
from blogapp.forms import RegistrationForm, LoginForm, UpdateAccountForm
from blogapp.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required

posts = [
    {
        "author": "Nurudeen",
        "title": "Blog post 1",
        "content": "First post content",
        "date": "Jan 14, 2023"
    },
    {
        "author": "Olaitan",
        "title": "Blog post 2",
        "content": "Second post content",
        "date": "Jan 13, 2023"
    },
    {
        "author": "Abdulsalaam",
        "title": "Blog post 3",
        "content": "Third post content",
        "date": "Jan 15, 2023"
    }
]

def save_picture(pics):
    random_name = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(pics.filename)
    pics_fname = random_name + f_ext
    pics_path = os.path.join(app.root_path, 'static/profile_pics', pics_fname)
    
    output_size = (125, 125)
    i = Image.open(pics)
    i.thumbnail(output_size)
    i.save(pics_path)
    
    return pics_fname

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts= posts)

@app.route("/about")
def about():
    return render_template('about.html', title = "About")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data) 
            flash(f'Welcome!', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash("Confirm email and password", "danger")
    return render_template('login.html', title="Login", form=form)

@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_pics.data:
            profile_pics_name = save_picture(form.profile_pics.data)
            current_user.image_file = profile_pics_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account updated successfully", 'success')
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename="profile_pics/" + current_user.image_file)
    return render_template('account.html', title="Acount", image_file=image_file, form=form)