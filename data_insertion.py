import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from dotenv import load_dotenv
import os

# Read the Excel file
df = pd.read_excel(r"C:\Users\venki\Work\Data_Engineering\Data_cleaning\processed_data_updated_3.xlsx")

# Load environment variables from .env file
load_dotenv()

# Define the SQLAlchemy models
Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    CustomerID = Column(String(50), primary_key=True)
    CountryID = Column(Integer, ForeignKey('countries.CountryID'))

class Country(Base):
    __tablename__ = 'countries'
    CountryID = Column(Integer, primary_key=True, autoincrement=True)
    CountryName = Column(String(255), unique=True, nullable=False)  # Specifying length

class Invoice(Base):
    __tablename__ = 'invoices'
    InvoiceNo = Column(String(50), primary_key=True)
    hour = Column(Integer)
    minute = Column(Integer)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    CustomerID = Column(String(50), ForeignKey('customers.CustomerID'))
    CountryID = Column(Integer, ForeignKey('countries.CountryID'))


class InvoiceItem(Base):
    __tablename__ = 'invoice_items'
    InvoiceItemID = Column(Integer, primary_key=True, autoincrement=True)
    InvoiceNo = Column(String(50), ForeignKey('invoices.InvoiceNo'))
    ProductID = Column(String(50))
    Quantity = Column(Integer)
    UnitPrice = Column(Float(50))
    TotalPrice = Column(Float(50))

# Get database connection credentials from environment variables
DATABASE_TYPE = os.getenv("DATABASE_TYPE")
DBAPI = os.getenv("DBAPI")
ENDPOINT = os.getenv("ENDPOINT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")

engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}/{DATABASE}")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Function to get or create a CountryID
def get_or_create_country_id(session, country_name):
    country = session.query(Country).filter_by(CountryName=country_name).first()
    if not country:
        country = Country(CountryName=country_name)
        session.add(country)
        session.commit()
    return country.CountryID

# Populate the tables
for index, row in df.iterrows():
    country_id = get_or_create_country_id(session, row['Country'])
    customer = Customer(CustomerID=row['CustomerID'], CountryID=country_id)
    invoice = Invoice(
        InvoiceNo=row['InvoiceNo'],
        hour=row['hour'],
        minute=row['minute'],
        year=row['year'],
        month=row['month'],
        day=row['day'],
        CustomerID=row['CustomerID'],
        CountryID=country_id
    )
    invoice_item = InvoiceItem(
        InvoiceNo=row['InvoiceNo'],
        ProductID=row['StockCode'],
        Quantity=row['Quantity'],
        UnitPrice=row['UnitPrice'],
        TotalPrice=row['Quantity'] * row['UnitPrice']
    )
    session.merge(customer)
    session.merge(invoice)
    session.add(invoice_item)

session.commit()
