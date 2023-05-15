from market import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from market.models import User, Item
from market.forms import RegisterUser, LoginUser, PurchaseItem, SellItem

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/user')
def user_page():
    users = User.query.all()
    return render_template('user.html', users=users)

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItem()
    sell_form = SellItem()
    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        purchased_object = Item.query.filter_by(name=purchased_item).first()
        if purchased_object:
            if current_user.balance >= purchased_object.price:
                purchased_object.owner = current_user.id
                current_user.balance -= purchased_object.price
                db.session.commit()
                flash(f'Congratulations! You just purchased {purchased_object.name} for {purchased_object.price}$.', category='success')
            else:
                flash(f'Your balance is not enough to purchase {purchased_object.name}.', category='danger')
        sold_item = request.form.get('sold_item')
        sold_object = Item.query.filter_by(name=sold_item).first()
        if sold_object:
            sold_object.owner = None
            current_user.balance += sold_object.price
            db.session.commit()
            flash(f'Congratulations! You just sold {sold_object.name} for {sold_object.price}$.', category='success')
        return redirect(url_for('market_page'))
    if request.method == 'GET':
        items = Item.query.filter_by(owner=None).all()
        purchased_items = Item.query.filter_by(owner=current_user.id).all()
        return render_template('market.html', items=items, purchased_items=purchased_items, purchase_form=purchase_form, sell_form=sell_form)

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