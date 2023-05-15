from market import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from market.models import User, Item
from market.forms import LoginUser

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginUser()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'You are succesfuly logged in as {attempted_user.username}.', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not matching, please try again.', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
    logout_user()
    flash('You have been successfully logged out.', category='info')
    return redirect(url_for('home_page'))