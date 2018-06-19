from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy import join, select
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

@app.route("/catalog/addProduct", methods=['POST','GET'])
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

# @app.route("/index/createCompany/data", methods=['POST'])
# def createEntry():
#     if request.method == 'POST':
#         company = session.query(Company).all()
#         # status = 1 indicates that a new entry is added
#         status = 1
#         var = request.form['cname']
#         for i in company:
#             if var == i.cname:
#                 status = 0
#                 break
#             else:
#                 continue
#         if status == 1:
#             Company_x = Company(cname = request.form['cname'])
#             session.add(Company_x)
#             session.commit()
#             Product_x = Product(pname = request.form['pname'],
#                 pdescription = request.form['pdescription'],
#                 pc = Company_x.id)
#             session.add(Product_x)
#             session.commit()
#             company = session.query(Company).all()
#             product = session.query(Product).all()
#             return render_template("index.html", company=company, product=product)
#         else:
#             return "Sorry but this Company already exists.\nChoose a new name."

@app.route("/catalog/<com>/items")
def showCompany(com):
    company = session.query(Company).all()
    var = session.query(Company).filter_by(cname=com).first()
    product = session.query(Product).filter_by(pc=var.id).all()
    return render_template('showCompany.html',company=company, product=product,name=com,count=len(product))

@app.route("/catalog/<cname>/<pname>")
def showProduct(cname,pname):
    del cname
    product = session.query(Product).filter_by(pname = pname).all()
    return render_template('showProduct.html',product=product)

@app.route("/json")
def showJSON():
    product = session.query(Product).all()
    return jsonify(Product=[i.serialize for i in product])

if __name__ == '__main__':
    print("Running Personalized Server, exclusively for Cheetah")
    app.debug = True
    app.run(host='0.0.0.0', port=8001)