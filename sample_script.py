import sqlalchemy
from sqlalchemy import create_engine,Column,Integer,String,ForeignKey,Table,Text,inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship

import glob
import json
import pandas as pd

from config import *
from db_config import *

new_customer = Customer(name='Sam',customer_type='individual')
# new_customer.name = 'Conary'
# new_customer.customer_type = 'individual'
session.add(new_customer)
session.commit()

for customer in session.query(Customer):
    print(customer.name,customer.customer_type)


data = pd.read_csv('./orders.csv')
data["Item's Variant"].value_counts()
data.columns
for i,row in data.iterrows():
    new_order = Order(order_number=row['Order #'])
    print(row['Order #'])
    session.add(new_order)
session.commit()


for order in session.query(Order):
    print(order.id,order.order_number)

customers = enumerate(data['Billing Customer'].unique().tolist())
for i,cust in customers:
    print(i,cust)
#     new_cust = Customer(name=cust)
#     session.add(new_cust)
# session.commit()

df = pd.read_sql_query('SELECT * FROM customers',con=engine)
