from Funding import app
from flask import render_template, redirect, url_for,flash
from Funding.models import Item, User
from Funding.forms import RegisterForm,LoginForm
from Funding import db
from flask_login import login_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home_page.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/funding')
def funding_page():
    items = Item.query.all()
    return render_template('funding.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('funding_page'))
    
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user= User.query.get(form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash('Successful login {attempted_user.username}', category='success')
            return redirect(url_for('funding_page'))
        else:
            flash('username and password are not a match! please try again', category='danger')
    return render_template('login.html', form=form)