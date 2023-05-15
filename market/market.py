from market import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from market.models import User, Item
from market.forms import RegisterUser, LoginUser, PurchaseItem, SellItem

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