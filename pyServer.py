from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine, desc
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from dbSetup import Base, Company, Product

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
    return render_template("index.html", company=company, product=product)

@app.route("/catalog/addProduct", methods=['GET','POST'])
def addProduct():
    if request.method == 'POST':
        newCompanyName = request.form['CId']
        newProductName = request.form['newPName']
        newProductDescription = request.form['newPDescription']
        Product_0 = Product(pname = newProductName,
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
    return render_template('showCompany.html',company=company, product=product,name=com,count=len(product))

@app.route("/catalog/<cname>/<pname>")
def showProduct(cname,pname):
    product = session.query(Product).filter_by(pname = pname).all()
    del cname, pname
    return render_template('showProduct.html',product=product)

@app.route("/catalog/<pname>_<pid>/Delete")
def deleteProduct(pname,pid):
    del pname
    product = session.query(Product).filter_by(id = pid).one()
    session.delete(product)
    session.commit()
    flash("Deleted Successful!!!")
    return redirect(url_for('index'))

@app.route("/catalog/<pname>_<pid>/Edit", methods=['GET','POST'])
def editProduct(pname,pid):
    if request.method == 'GET':
        product = session.query(Product).filter_by(id = pid).all()
        return render_template('editProduct.html',product=product)
    else:
        product = session.query(Product).filter_by(id = pid).one()
        newProductName = request.form['editedPName']
        newProductDescription = request.form['editedPDescription']
        newProductPC = product.pc
        session.delete(product)
        session.commit()
        product = Product(pname=newProductName,
                          pdescription=newProductDescription,
                          pc=newProductPC)
        session.add(product)
        session.commit()
        flash("Edited Successfully")
        return redirect(url_for('index'))

@app.route("/json")
def showJSON():
    company = session.query(Company).all()
    product = session.query(Product).all()
    return jsonify(Company=[i.serialize for i in company], Product=[i.serialize for i in product])

if __name__ == '__main__':
    print("Running Personalized Server, exclusively for CTRL-CODE")
    # for flashing messages on screen, we are using secret_key
    app.secret_key = "my_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=8001)