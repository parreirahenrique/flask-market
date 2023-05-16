from market import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from market.models import User, Item
from market.forms import RegisterUser, LoginUser, PurchaseItem, SellItem, UserPassword, DepositForm, DeleteUser

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/user', methods=['GET', 'POST'])
@login_required
def user_page():
    user = User.query.filter_by(id=current_user.id).first()
    password_form = UserPassword()
    deposit_form =  DepositForm()
    delete_form = DeleteUser()
    if request.method == 'GET':
        return render_template('user.html', user=user, password_form=password_form, deposit_form=deposit_form, delete_form=delete_form)
    elif request.method == 'POST':
        if password_form.validate_on_submit():
            user.password = password_form.password.data
            db.session.commit()
            flash(f'Password changed succesfuly!', category='success')
        elif password_form.errors == {'password_validation': ['Field must be equal to password.']}:
            flash(f'Your passwords must match. Please, try again.', category='danger')
        if deposit_form.validate_on_submit():
            user.balance += deposit_form.balance.data
            db.session.commit()
            flash(f'{deposit_form.balance.data}$ was successfully deposited into your account!', category='success')
        if delete_form.validate_on_submit():
            username = user.username
            logout_user()
            db.session.delete(user)
            db.session.commit()
            flash(f'The user {username} was succesfully deleted.', category='info')
        return redirect(url_for('user_page'))
    

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
        login_user(submited_user)
        flash(f'Account created succesfuly! You are now logged in as {submited_user.username}.', category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for error in form.errors.values():
            flash(f'There was an error while creating a new user: {error}', category='danger')
    return render_template('register.html', form=form)