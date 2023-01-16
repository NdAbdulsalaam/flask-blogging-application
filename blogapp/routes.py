from flask import render_template, url_for, flash, redirect
from blogapp import app, db, bcrypt
from blogapp.forms import RegistrationForm, LoginForm
from blogapp.models import User, Post

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

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts= posts)

@app.route("/about")
def about():
    return render_template('about.html', title = "About")

@app.route("/register", methods=['GEt', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)

@app.route("/login", methods=['GEt', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "olaitansalaam2012@gmail.com" and form.password.data =="123456":
            flash(f'Welcome!', 'success')
            return redirect(url_for('home'))
        else:
            flash("Confirm email and password", "danger")
    return render_template('login.html', title="Login", form=form)