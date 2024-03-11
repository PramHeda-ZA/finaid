from Funding import app, mail
from flask import render_template, redirect, request, url_for,flash
from Funding.models import Item, User, ApplicationForm as ApplicationFormModel
from Funding.forms import RegisterForm,LoginForm,ApplicationF,ProfileForm,ContactForm 
from Funding import db
from flask_login import login_user,logout_user,current_user, login_required
from flask_mail import Message

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

@app.route('/Bursaries')
def bursary_page():
    items = ApplicationFormModel.query.all()
    return render_template('bursarylist.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data,
                              role = form.role.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged in as {user_to_create.username}', category='success')
        return redirect(url_for('home_page'))
    
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('profile'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('home_page'))

@app.route('/ApplicationForm', methods=['GET', 'POST'])
def application_form_page():
    form = ApplicationF()
    
    if form.validate_on_submit():
        application_data = ApplicationFormModel(
            name=form.name.data,
            company=form.company.data,
            description=form.description.data,
            enddate=form.enddate.data,
            link=form.link.data
        )
        
        db.session.add(application_data)
        db.session.commit()

        flash('Application submitted successfully!', category='success')
        return redirect(url_for('home_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error occurred in Application Form: {err_msg}', category='danger')

    return render_template('applicationform.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email_address = form.email_address.data
        current_user.role = form.role.data

        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email_address.data = current_user.email_address
        form.role.data = current_user.role

    return render_template('profile.html', form=form)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        subject = 'Contact Form Submission'
        body = f"Name: {form.name.data}\nEmail: {form.email.data}\n\n{form.message.data}"
        recipient = 'your_outlook_email@example.com'  # Replace with your email

        message = Message(subject=subject, body=body, recipients=[recipient])

        try:
            mail.send(message)
            flash('Your message has been sent!', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'danger')

    return render_template('contact.html', form=form)