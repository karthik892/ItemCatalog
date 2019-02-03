from flask import Flask, render_template, url_for
from flask import request, redirect, flash, jsonify
from flask import session as login_session
import random
import string

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from Database import Category, Item, User

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import datetime

app = Flask(__name__)
Base = declarative_base()

engine = create_engine('sqlite:///ItemCatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


@app.route("/")
def mainPage():
    """
    Returns the Home Page.
    Contains a category list and a list of recently created items
    """
    session = DBSession()
    categories = session.query(Category).all()
    top_items = session.query(Item).order_by(desc(Item.creation_date)).limit(5)
    return render_template(
        'home.html',
        categories=categories,
        top_items=top_items
    )


@app.route("/<string:category_name>")
def itemListPage(category_name):
    """Returns the item list page for a specific category"""
    session = DBSession()
    categories = session.query(Category).all()
    items = session.query(Item)\
        .filter(Item.category_name == category_name).all()
    return render_template(
        'view_category.html',
        categories=categories,
        items=items,
        cat_name=category_name
    )


@app.route("/<string:category_name>/<string:item_name>")
def ItemDetailPage(category_name, item_name):
    """Returns the Item Details page for a specific item"""
    session = DBSession()
    item = session.query(Item).filter(Item.name == item_name).first()
    return render_template('view_item.html', item=item)


@app.route("/<string:category_name>/add", methods=['GET', 'POST'])
def ItemAddPage(category_name):
    """
    The GET returns a page to allow a user to add a new item
    to the specified category,
    the POST processes data from the add item form
    """
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        frmName = request.form['itemname']
        frmDescription = request.form['itemdesc']
        if frmName == '':
            flash('Item name is a compulsory field and must have a value')
            return render_template(
                'add_item.html',
                category_name=category_name
            )
        session = DBSession()
        newItem = Item(
            name=frmName,
            description=frmDescription,
            category_name=category_name,
            creation_date=datetime.datetime.now(),
            creator_email=login_session['email']
        )
        session.add(newItem)
        session.commit()
        flash("Added " + request.form['itemname'] + " to " + category_name)
        return redirect(url_for('mainPage'))
    else:
        return render_template('add_item.html', category_name=category_name)


@app.route(
    "/<string:category_name>/<string:item_name>/edit",
    methods=['GET', 'POST']
)
def ItemEditPage(category_name, item_name):
    """
    The GET returns a page to allow a user to edit a existing item,
    the POST processes data from the modify item form
    """
    if 'username' not in login_session:
        return redirect('/login')
    session = DBSession()
    item = session.query(Item).filter(Item.name == item_name).first()
    if request.method == 'POST':
        frmName = request.form['itemname']
        frmDescription = request.form['itemdesc']
        if login_session['email'] != item.creator_email:
            flash('Invalid user, cannot complete request')
            return redirect(url_for('mainPage'))
        newItem = Item(
            name=frmName,
            description=frmDescription,
            category_name=category_name
        )
        session.merge(newItem)
        session.commit()
        flash("Updated " + item_name + " in " + category_name)
        return redirect(url_for('mainPage'))
    else:
        return render_template('modify_item.html', item=item)


@app.route(
    "/<string:category_name>/<string:item_name>/delete",
    methods=['GET', 'POST']
)
def ItemDeletePage(category_name, item_name):
    """
    The GET prompts the user to confirm that they
    would like to delete the specified item,
    the POST deletes the specified item
    """
    if 'username' not in login_session:
        return redirect('/login')
    session = DBSession()
    if request.method == 'POST':
        item = session.query(Item)\
            .filter(Item.name == request.form['itemname']).first()
        if login_session["email"] != item.creator_email:
            flash('Invalid user, cannot complete request')
            return redirect(url_for('mainPage'))
        session.delete(item)
        session.commit()
        flash("Deleted " + item_name + " from " + category_name)
        return redirect(url_for('mainPage'))
    else:
        item = session.query(Item).filter(Item.name == item_name).first()
        return render_template('delete_item.html', item=item)


@app.route("/login")
def login():
    """Displays the login page"""
    state = ''.join(
        random.choice(
            string.ascii_uppercase + string.digits
        ) for x in range(32)
    )
    login_session['state'] = state
    return render_template("login.html", STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Processes a login via Google"""
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()

    result = json.loads((h.request(url, 'GET')[1]).decode())

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    # if stored_access_token is not None and gplus_id == stored_gplus_id:
    #    response = make_response(json.dumps(
    #    'Current user is already connected.'), 200)
    #    response.headers['Content-Type'] = 'application/json'
    #    return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    session = DBSession()
    session.merge(User(
        name=login_session['username'],
        email=login_session['email']
    ))
    session.commit()
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 30px; height: 30px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """Processes a logout via Google"""
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected.'),
            401
        )
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'\
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Logout Successful")
        return redirect(url_for("mainPage"))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400)
        )
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route("/api/item/list")
def getJSON():
    """Returns a JSON representation of the data stored in the database"""
    session = DBSession()
    categories = session.query(Item).all()
    return jsonify(Category=[i.serialize for i in categories])


@app.route('/api/item/<string:item_name>')
def getItemJSON(item_name):
    """Returns a JSON representation of a specific item"""
    session = DBSession()
    item = session.query(Item).filter(Item.name == item_name).first()
    print(item)
    return jsonify(Item=item.serialize)


def wsgi_startup():
    app.secret_key = 'fdhjsdbhjfhdkcxxd'
    app.run(host="0.0.0.0", debug=True)


if __name__ == '__main__':
    app.secret_key = 'fdhjsdbhjfhdkcxxd'
    app.run(host="0.0.0.0", debug=True)
#    app.run()
