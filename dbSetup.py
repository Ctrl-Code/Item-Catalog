from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class Company(Base):
    __tablename__ = 'comp'
    id = Column(Integer, primary_key=True)
    cname = Column(String(50), nullable=False,)


class Product(Base):
    __tablename__ = 'prod'
    id = Column(Integer, primary_key=True)
    pname = Column(String(50), nullable=False)
    pdescription = Column(String(150))
    comp = relationship(Company)
    pc = Column(Integer, ForeignKey('comp.id'))


engine = create_engine('postgresql+psycopg2://abc:cba@localhost/mazak')
Base.metadata.create_all(engine)
