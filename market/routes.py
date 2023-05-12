from market import app, db
from flask import render_template, redirect, url_for
from market.models import User, Item
from market.forms import RegisterUser

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/user')
def user_page():
    users = User.query.all()
    return render_template('user.html', users=users)

@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterUser()
    if form.validate_on_submit():
        submited_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
            )
        db.session.add(submited_user)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for error in form.errors.values():
            print(f'There was an error while creating a new user: {error}')
    return render_template('register.html', form=form)