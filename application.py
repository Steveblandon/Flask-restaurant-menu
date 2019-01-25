from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, request, redirect, url_for, render_template, flash, jsonify
import config as cfg


application = Flask(__name__)
engine = create_engine('%s+%s://%s:%s@%s:%s/%s' % (cfg.DB_DIALECT, cfg.DB_DRIVER, 
    cfg.DB_USER, cfg.DB_PASS, cfg.DB_HOST, cfg.DB_PORT, cfg.DB_NAME))
Base.metadata.bind = engine
dbsession = sessionmaker(bind=engine)


@application.route('/')
@application.route('/restaurants/')
def restaurants():
    session_ = dbsession()
    restaurants = session_.query(Restaurant).all()
    session_.close()
    return render_template('restaurants.html', restaurants=restaurants)


@application.route('/restaurants/new/', methods=['POST','GET'])
def new_restaurant():
    session_ = dbsession()
    if request.method == 'POST':
        restaurant = Restaurant(name=request.form['restaurant_name'])
        session_.add(restaurant)
        session_.commit()
        flash('restaurant "%s" has been added!' % restaurant.name)
        session_.close()
        return redirect(url_for('restaurants'))
    else:
        session_.close()
        return render_template('new_restaurant.html')


@application.route('/restaurants/<int:restaurant_id>/edit/', methods=['POST','GET'])
def edit_restaurant(restaurant_id):
    session_ = dbsession()
    restaurant = session_.query(Restaurant).filter_by(id=restaurant_id).first()
    if restaurant != None:
        if request.method == 'POST':
            restaurant.name = request.form['restaurant_name']
            session_.add(restaurant)
            session_.commit()
            flash('restaurant "%s" has been edited!' % restaurant.name)
            session_.close()
            return redirect(url_for('restaurants'))
        else:
            session_.close()
            return render_template('edit_restaurant.html', restaurant=restaurant)
    session_.close()


@application.route('/restaurants/<int:restaurant_id>/delete/', methods=['POST','GET'])
def del_restaurant(restaurant_id):
    session_ = dbsession()
    restaurant = session_.query(Restaurant).filter_by(id=restaurant_id).first()
    if restaurant != None:        
        if request.method == 'POST':
            session_.delete(restaurant)
            session_.commit()
            flash('restaurant "%s" has been deleted!' % restaurant.name)
            session_.close()
            return redirect(url_for('restaurants'))
        else:
            session_.close()
            return render_template('del_restaurant.html', restaurant=restaurant)
    session_.close()


@application.route('/restaurants/<int:restaurant_id>/menu/')
def menu_items(restaurant_id):
    session_ = dbsession()
    restaurant = session_.query(Restaurant).filter_by(id=restaurant_id).first()
    if restaurant != None:
        menu_items = session_.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
        session_.close()
        return render_template('menu_items.html', menu_items=menu_items, restaurant=restaurant)


@application.route('/restaurants/<int:restaurant_id>/new/', methods=['POST','GET'])
def new_menu_item(restaurant_id):
    session_ = dbsession()
    if request.method == 'POST':
        menu_item = MenuItem()
        menu_item.name = request.form['menu_item_name']
        menu_item.price = request.form['menu_item_price']
        menu_item.description = request.form['menu_item_desc']
        menu_item.restaurant_id = restaurant_id
        session_.add(menu_item)
        session_.commit()
        flash('menu item "%s" has been added!' % menu_item.name)
        session_.close()
        return redirect(url_for('menu_items', restaurant_id=restaurant_id))
    else:
        restaurant = session_.query(Restaurant).filter_by(id=restaurant_id).first()
        session_.close()
        if restaurant != None:
            return render_template('new_menu_item.html', restaurant_id=restaurant_id)


@application.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>/edit/', methods=['POST','GET'])
def edit_menu_item(restaurant_id, menu_item_id):
    session_ = dbsession()
    menu_item = session_.query(MenuItem).filter_by(id = menu_item_id).first()
    if menu_item != None:
        if request.method == 'POST':
            menu_item.name = request.form['menu_item_name']
            menu_item.price = request.form['menu_item_price']
            menu_item.description = request.form['menu_item_desc']
            session_.add(menu_item)
            session_.commit()
            flash('menu item "%s" has been edited!' % menu_item.name)
            session_.close()
            return redirect(url_for('menu_items', restaurant_id=restaurant_id))
        else:
            restaurant = session_.query(Restaurant).filter_by(id=restaurant_id).first()
            session_.close()
            if restaurant != None:
                return render_template('edit_menu_item.html', menu_item=menu_item, restaurant=restaurant)
    session_.close()


@application.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>/delete/', methods=['POST','GET'])
def del_menu_item(restaurant_id, menu_item_id):
    session_ = dbsession()
    menu_item = session_.query(MenuItem).filter_by(id = menu_item_id).first()
    if menu_item != None:
        if request.method == 'POST':
            session_.delete(menu_item)
            session_.commit()
            flash('menu item "%s" has been deleted!' % menu_item.name)
            session_.close()
            return redirect(url_for('menu_items', restaurant_id=restaurant_id))
        else:
            restaurant = session_.query(Restaurant).filter_by(id=restaurant_id).first()
            session_.close()
            return render_template('del_menu_item.html', menu_item=menu_item, restaurant=restaurant)
    session_.close()


# @application.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>/JSON/')
# def menu_itemJSON(restaurant_id, menu_item_id):
#     session_ = dbsession()
#     menu_item = session_.query(MenuItem).filter_by(id=menu_item_id).first()
#     if menu_item != None:
#         return jsonify(MenuItem=menu_item.serialize)
#     else:
#         return '{}'


if __name__ == '__main__':
    application.debug = cfg.FLASK_ENABLE_DEBUG
    application.secret_key = cfg.SESSION_SECRET
    # application.run(host=cfg.APP_HOST, port=cfg.APP_PORT)
    application.run()