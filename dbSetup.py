from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        return {
            'Id': self.id,
            'Name': self.name,
            'Email': self.email,
            'Picture': self.picture
        }


class Company(Base):
    __tablename__ = 'comp'

    id = Column(Integer, primary_key=True)
    cname = Column(String(50), nullable=False,)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'Id': self.id,
            'Company': self.cname,
        }


class Product(Base):
    __tablename__ = 'prod'

    id = Column(Integer, primary_key=True)
    pname = Column(String(50), nullable=False)
    pdescription = Column(String(150))
    comp = relationship(Company)
    pc = Column(Integer, ForeignKey('comp.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'Id': self.id,
            'Product': self.pname,
            'Product Description': self.pdescription,
            'Product Company': self.pc
        }


engine = create_engine('postgresql+psycopg2://abc:cba@localhost/mazak')
Base.metadata.create_all(engine)
