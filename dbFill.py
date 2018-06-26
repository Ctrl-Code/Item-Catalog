from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbSetup import Base, Company, Product, User

engine = create_engine('postgresql+psycopg2://abc:cba@localhost/mazak')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Feeding the data to the database

User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

Company_1 = Company(user_id=1, cname="Samsung")
session.add(Company_1)
session.commit()

Company_2 = Company(user_id=1, cname="OnePlus")
session.add(Company_2)
session.commit()

Company_3 = Company(user_id=1, cname="Motorola")
session.add(Company_3)
session.commit()

Product_11 = Product(user_id=1, pname="Galaxy S9+",
            pdescription = "",
            pc = Company_1.id)
session.add(Product_11)
session.commit()

Product_12 = Product(user_id=1, pname = "Galaxy S9",
            pdescription = "",
            pc = Company_1.id)
session.add(Product_12)
session.commit()

Product_13 = Product(user_id=1, pname = "Galaxy S8+",
            pdescription = "",
            pc = Company_1.id)
session.add(Product_13)
session.commit()

Product_14 = Product(user_id=1, pname = "Galaxy Note8",
            pdescription = "",
            pc = Company_1.id)
session.add(Product_14)
session.commit()

Product_15 = Product(user_id=1, pname = "Galaxy Note5",
            pdescription = "",
            pc = Company_1.id)
session.add(Product_15)
session.commit()

Product_21 = Product(user_id=1, pname="OnePlus One",
            pdescription = "",
            pc = Company_2.id)
session.add(Product_21)
session.commit()

Product_22 = Product(user_id=1, pname="OnePlus Two",
            pdescription = "",
            pc = Company_2.id)
session.add(Product_22)
session.commit()

Product_23 = Product(user_id=1, pname="OnePlus X",
            pdescription = "",
            pc = Company_2.id)
session.add(Product_23)
session.commit()

Product_24 = Product(user_id=1, pname="OnePlus 3",
            pdescription = "",
            pc = Company_2.id)
session.add(Product_24)
session.commit()

Product_25 = Product(user_id=1, pname="OnePlus 3T",
            pdescription = "",
            pc = Company_2.id)
session.add(Product_25)
session.commit()

Product_26 = Product(user_id=1, pname="OnePlus 5",
            pdescription = "",
            pc = Company_2.id)
session.add(Product_26)
session.commit()

Product_27 = Product(user_id=1, pname="OnePlus 5T",
            pdescription = "",
            pc = Company_2.id)
session.add(Product_27)
session.commit()

Product_28 = Product(user_id=1, pname="OnePlus 6",
            pdescription = "",
            pc = Company_2.id)
session.add(Product_28)
session.commit()

Product_29 = Product(user_id=1, pname="OnePlus 6T",
            pdescription = "",
            pc = Company_2.id)
session.add(Product_29)
session.commit()

Product_31 = Product(user_id=1, pname="Moto z2 force",
            pdescription = "",
            pc = Company_3.id)
session.add(Product_31)
session.commit()

Product_32 = Product(user_id=1, pname="Moto z2 play",
            pdescription = "",
            pc = Company_3.id)
session.add(Product_32)
session.commit()

Product_33 = Product(user_id=1, pname="Moto z",
            pdescription = "",
            pc = Company_3.id)
session.add(Product_33)
session.commit()

Product_34 = Product(user_id=1, pname="Moto x4",
            pdescription = "",
            pc = Company_3.id)
session.add(Product_34)
session.commit()

Product_35 = Product(user_id=1, pname="Moto x force",
            pdescription = "",
            pc = Company_3.id)
session.add(Product_35)
session.commit()

Product_36 = Product(user_id=1, pname="Moto x play",
            pdescription = "",
            pc = Company_3.id)
session.add(Product_36)
session.commit()