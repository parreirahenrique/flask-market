from market import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from market.models import User, Item
from market.forms import RegisterUser, LoginUser, PurchaseItem, SellItem, AddItem

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItem()
    sell_form = SellItem()
    add_form = AddItem()
    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        purchased_object = Item.query.filter_by(name=purchased_item).first()
        if purchased_object:
            old_owner = User.query.filter_by(id=purchased_object.owner).first()
            print(purchased_item)
            print(current_user.balance)
            print(purchased_object.__dict__)
            if current_user.balance >= purchased_object.price:
                purchased_object.owner = current_user.id
                current_user.balance -= purchased_object.price
                old_owner.balance += purchased_object.price
                purchased_object.for_sale = False
                db.session.commit()
                flash(f'Congratulations! You just purchased {purchased_object.name} for {purchased_object.price}$.', category='success')
            else:
                flash(f'Your balance is not enough to purchase {purchased_object.name}.', category='danger')
        sold_item = request.form.get('sold_item')
        sold_object = Item.query.filter_by(name=sold_item).first()
        if sold_object:
            sold_object.for_sale = True
            db.session.commit()
            flash(f'Your Product {sold_object.name} is now for sale for {sold_object.price}$.', category='success')
        print(request.form.getlist('flexCheckDefault'))
        add_object = Item(
            name=add_form.name.data,
            price=add_form.price.data,
            barcode=add_form.barcode.data,
            description=add_form.description.data,
            owner=current_user.id
        )
        if add_form.validate_on_submit():
            db.session.add(add_object)
            db.session.commit()
        return redirect(url_for('market_page'))
    if request.method == 'GET':
        items = Item.query.filter_by(for_sale=True).all()
        purchased_items = Item.query.filter_by(owner=current_user.id).filter_by(for_sale=False).all()
        return render_template('market.html', items=items, purchased_items=purchased_items, purchase_form=purchase_form, sell_form=sell_form, add_form=add_form)