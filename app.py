from typing import List, Optional
from sqlalchemy import create_engine, text, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email_address: Mapped[str]
    address: Mapped[str]
    country_code: Mapped[str] = mapped_column(String(2))
    # add a 1-to-1 relationship to CreditCard
    credit_card: Mapped["CreditCard"] = relationship("CreditCard", back_populates="customer")
    # add a 1-to-1 relationship to Order
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="customer")

    def __repr__(self) -> str:
        return f"<Customer(name={self.name!r})>"

class CreditCard(Base):
    __tablename__ = "credit_card"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer: Mapped[Customer] = relationship("Customer", back_populates="credit_card")
    number: Mapped[str] = mapped_column(String(19))

    def __repr__(self) -> str:
        return f"<CreditCard(number={self.number!r})>"

# add a Product with name, price, description, and category
class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float]
    description: Mapped[str]
    category: Mapped[str] = mapped_column(String(100))
    # add a 1-to-1 relationship to Order
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="product")

    def __repr__(self) -> str:
        return f"<Product(name={self.name!r})>"

# add an Order with customer_id, product_id, and quantity
class Order(Base):
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer: Mapped[Customer] = relationship("Customer", back_populates="orders")
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    product: Mapped[Product] = relationship("Product", back_populates="orders")
    quantity: Mapped[int]

    def __repr__(self) -> str:
        return f"<Order(quantity={self.quantity!r})>"


from sqlalchemy import create_engine
engine = create_engine("sqlite:///my_database.db", echo=True)
Base.metadata.create_all(engine)

# TOOL TO CREATE FAKE DATA 
from faker import Faker
fake = Faker(["en_US", "en_GB", "en_CA", "es_MX", "de_DE", "fr_FR", "ja_JP"])

with Session(engine) as session:

    # for i in range(3):
    #     product = Product(name=f"Product {i}", price=9.99, description="ABC", category="XYZ")
    #     session.add(product)

    # for i in range(3):
    #     customer = Customer(name=fake.name(), email_address=fake.email(), address=fake.address(), country_code=fake.country_code())
    #     session.add(customer)
    
    #     credit_card = CreditCard(number=fake.credit_card_number(), customer=customer)
    #     session.add(credit_card)

    #     order = Order(customer=customer, product_id=fake.random_int(min=1, max=10), quantity=fake.random_int(min=1, max=5))
    #     session.add(order)    


    session.commit()


    from sqlalchemy import select
    from sqlalchemy import func

    query = select(Customer)
    results = session.execute(query).scalars().all()
    print(f" ***************** View all customers:  {results} *********************")

    query2 = select(Customer).where(Customer.country_code == "LU")
    results = session.execute(query2).scalars().all()
    print (f" ***************** These are the customers who country code is LU: {results}")

    query3 = select(Customer.country_code, func.count(Customer.country_code)).group_by(Customer.country_code)
    results = session.execute(query3).all()
    print (f" ********* Count by Country Code: {results} ************")

    query4 = select(Customer.name, CreditCard.number).join(CreditCard)
    results = session.execute(query4).all()
    print(f"********** This displays each customer name with their corresponsing credit card # {results}***********")

#  ** one to many relationship **
    query5 = select(Customer.id, func.count(Order.id)).join(Order).group_by(Customer.id)
    results = session.execute(query5).all()
    print(f" *****  Results of one-to-many. This shows customer id's with their number of orders: {results}")












