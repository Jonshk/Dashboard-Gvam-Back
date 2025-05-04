# app/models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from database import Base   # <-- aquí importas Base desde database.py



class User(Base):
    __tablename__ = "users"
    id       = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role     = Column(String, nullable=False, default="user")


class Center(Base):
    __tablename__ = "centers"
    id = Column(Integer, primary_key=True, index=True)
    center = Column(String, nullable=False)
    phonenumber = Column(String, nullable=False)

    orders     = relationship("Order",    back_populates="center")
    repairs    = relationship("Repair",   back_populates="center")
    receptions = relationship("Reception",back_populates="center")

class Order(Base):
    __tablename__ = "orders"
    id               = Column(Integer, primary_key=True, index=True)
    center_id        = Column(Integer, ForeignKey("centers.id"), nullable=False)
    shipping_company = Column(String, nullable=False)
    order_date       = Column(Date,   nullable=False)

    center = relationship("Center", back_populates="orders")
    items  = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"
    order_id     = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    product_name = Column(String,  primary_key=True)
    quantity     = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")

class Repair(Base):
    __tablename__ = "repairs"
    id          = Column(Integer, primary_key=True, index=True)
    center_id   = Column(Integer, ForeignKey("centers.id"), nullable=False)
    repair_type = Column(String,  nullable=False)
    repair_date = Column(Date,    nullable=False)

    center = relationship("Center", back_populates="repairs")
    items  = relationship("RepairItem", back_populates="repair", cascade="all, delete-orphan")

class RepairItem(Base):
    __tablename__ = "repair_items"
    repair_id       = Column(Integer, ForeignKey("repairs.id"), primary_key=True)
    product_name    = Column(String,  primary_key=True)
    repair_quantity = Column(Integer, nullable=False)

    repair = relationship("Repair", back_populates="items")

class Reception(Base):
    __tablename__ = "receptions"
    id             = Column(Integer, primary_key=True, index=True)
    center_id      = Column(Integer, ForeignKey("centers.id"), nullable=False)
    reception_date = Column(Date,    nullable=False)

    center = relationship("Center", back_populates="receptions")
    items  = relationship("ReceptionItem", back_populates="reception", cascade="all, delete-orphan")

class ReceptionItem(Base):
    __tablename__ = "reception_items"
    reception_id = Column(Integer, ForeignKey("receptions.id"), primary_key=True)
    product_name = Column(String,  primary_key=True)
    quantity     = Column(Integer, nullable=False)

    reception = relationship("Reception", back_populates="items")

class StockCategory(Base):
    __tablename__ = "stock_categories"
    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String,  unique=True, nullable=False)

    subcategories = relationship("StockSubcategory", back_populates="category", cascade="all, delete-orphan")

class StockSubcategory(Base):
    __tablename__ = "stock_subcategories"
    id          = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("stock_categories.id"), nullable=False)
    name        = Column(String,  nullable=False)

    category = relationship("StockCategory",    back_populates="subcategories")
    items    = relationship("StockItem", back_populates="subcategory", cascade="all, delete-orphan")

class StockItem(Base):
    __tablename__ = "stock_items"
    id             = Column(Integer, primary_key=True, index=True)
    subcategory_id = Column(Integer, ForeignKey("stock_subcategories.id"), nullable=False)
    product_name   = Column(String, nullable=False)
    quantity       = Column(Integer, nullable=False)
    price          = Column(Float,   nullable=False)
    image_path     = Column(Text,    nullable=True)
    estado         = Column(String,  nullable=True)

    subcategory = relationship("StockSubcategory", back_populates="items")
