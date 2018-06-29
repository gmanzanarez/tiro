import sqlalchemy
from sqlalchemy import create_engine,Column,Integer,String,ForeignKey,Table,Text,inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship

import glob
import json
import pandas as pd

from config import *


Base = declarative_base()

## Builds a many to many relationship between parts and fragments
order_product = Table('order_product', Base.metadata,
    Column('order_id', ForeignKey('orders.id'), primary_key=True),
    Column('product_id', ForeignKey('products.id'), primary_key=True)
)

class Customer(Base):
    '''Describes a well within a plate'''
    __tablename__ = 'customers'

    id = Column(Integer,primary_key=True)
    name = Column(String)
    customer_type = Column(String)

    orders = relationship("Order",back_populates='customers')


class Order(Base):
    '''Describes a well within a plate'''
    __tablename__ = 'orders'

    id = Column(Integer,primary_key=True)
    order_number = Column(String)
    invoice = Column(String)
    date = Column(String)

    # A part can have many fragments and one fragment can have many parts
    products = relationship('Product',
                            secondary=order_product,
                            back_populates='orders')

    # One well can only have a single part inside of it if assembly/seq_plate
    customer_id = Column(Integer,ForeignKey('customers.id'))
    customers = relationship("Customer",back_populates='orders')



class Product(Base):
    '''Describes a well within a plate'''
    __tablename__ = 'products'

    id = Column(Integer,primary_key=True)
    product_name = Column(String)
    variant = Column(String)
    price = Column(String)

    # A part can have many fragments and one fragment can have many parts
    orders = relationship('Order',
                            secondary=order_product,
                            back_populates='products')


## Connect to the database specified in the config file
engine = sqlalchemy.create_engine(CONNECTION_STRING, echo=False)

## Create and commit all of the tables
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


#
