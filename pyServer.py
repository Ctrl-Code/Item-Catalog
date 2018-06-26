from flask import Flask, render_template, request, redirect, url_for, jsonify, flash

# for creating anti-forgery state tokens
from flask import session as login_session
import random, string

from sqlalchemy import create_engine, desc
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from dbSetup import Base, Company, Product, User

# for creating oauth2 login
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json','r').read())['web']['client_id']

engine = create_engine('postgresql+psycopg2://abc:cba@localhost/mazak')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    company = session.query(Company).all()
    product = session.query(Product).order_by(desc(Product.id)).limit(7)
    if 'username' not in login_session:
        return render_template("publicIndex.html", company=company, product=product)
    else:
        return render_template("index.html", company=company, product=product)

# Creating anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    # login_session below is a dictionary
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
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
    result = json.loads(h.request(url, 'GET')[1])
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
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

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

    user_id = getUserID(login_session['email'])
    if user_id == None:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("Welcome %s!!!" % login_session['username'])
    print ("done!")
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print ('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print ('result is ')
    print (result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Logged Out!!!")
        return redirect(url_for('index'))
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route("/catalog/addProduct", methods=['GET','POST'])
def addProduct():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCompanyName = request.form['CId']
        newProductName = request.form['newPName']
        newProductDescription = request.form['newPDescription']
        user_id = login_session['user_id']
        print(user_id)
        Product_0 = Product(user_id = user_id,
                            pname = newProductName,
                            pdescription = newProductDescription,
                            pc = newCompanyName)
        session.add(Product_0)
        session.commit()
        return redirect(url_for('index'))
    else:
        company = session.query(Company).all()
        return render_template("addProduct.html", company=company)

@app.route("/catalog/<com>/items")
def showCompany(com):
    company = session.query(Company).all()
    var = session.query(Company).filter_by(cname=com).first()
    product = session.query(Product).filter_by(pc=var.id).all()
    if 'username' not in login_session:
        return render_template('publicShowCompany.html',company=company, product=product,name=com,count=len(product))
    else:
        return render_template('showCompany.html',company=company, product=product,name=com,count=len(product))

@app.route("/catalog/<cname>/<pname>")
def showProduct(cname,pname):
    product = session.query(Product).filter_by(pname = pname).all()
    del cname, pname
    if 'username' not in login_session:
        return render_template('publicShowProduct.html',product=product)
    else:
        return render_template('showProduct.html',product=product)

@app.route("/catalog/<pname>_<pid>/Delete")
def deleteProduct(pname,pid):
    if 'username' not in login_session:
        return redirect('/login')
    else:
        del pname
        product = session.query(Product).filter_by(id = pid).one()
        user = session.query(User).filter_by(email=login_session['email']).one()
        if product.user_id == user.id:
            session.delete(product)
            session.commit()
            flash("Item Deleted!!!")
            return redirect(url_for('index'))
        else:
            return '''<h1>Sorry %s you are not authorised to delete this Product.
            </h1><h2>Note: You can only perform this action on the Products you have
            added.</h2>''' % login_session['username']

@app.route("/catalog/<pname>_<pid>/Edit", methods=['GET','POST'])
def editProduct(pname,pid):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'GET':
        product = session.query(Product).filter_by(id = pid).all()
        user = session.query(User).filter_by(email=login_session['email']).one()
        for i in product:
            if i.user_id == user.id:
                return render_template('editProduct.html',product=product)
            else:
                return '''<h1>Sorry %s you are not authorised to edit the details of this Product.
                </h1><h2>Note: You can only perform this action only on the Products you have
                added.</h2>''' % login_session['username']
    else:
        product = session.query(Product).filter_by(id = pid).one()
        ProductName = request.form['editedPName']
        ProductDescription = request.form['editedPDescription']
        ProductPC = product.pc
        ProductUserId = product.user_id
        session.delete(product)
        session.commit()
        product = Product(pname=ProductName,
                          pdescription=ProductDescription,
                          pc=ProductPC,
                          user_id=ProductUserId)
        session.add(product)
        session.commit()
        flash("Item Edited!!!")
        return redirect(url_for('index'))

@app.route("/json")
def showJSON():
    company = session.query(Company).all()
    product = session.query(Product).all()
    return jsonify(Company=[i.serialize for i in company], Product=[i.serialize for i in product])

# User Helper Functions ie createUser, getUserInfo, getUserID

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

if __name__ == '__main__':
    print("Running Personalized Server, exclusively for CTRL-CODE")
    # for flashing messages on screen, we are using secret_key
    app.secret_key = "my_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=8001)