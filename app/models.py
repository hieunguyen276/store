from email.policy import default

from numpy import product
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from geoalchemy2 import Geometry


class Supplier(db.Model):
    __tablename__ = "Suppliers"
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.String, nullable=False)
    supplier_name = db.Column(db.String, nullable=False)
    adress = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    fax = db.Column(db.String, nullable=False)
    home_page = db.Column(db.String, nullable=False)
    product =db.relationship("Product", backref="product", lazy=True)
    
    # def add_product(self, product_id, product_name, product_type, unit_price, amount, id_supplier):
    #     p = Product(product_id=product_id, product_name=product_name,product_type=product_type, unit_price=unit_price, amount=amount, id_supplier=id_supplier, supplier_id=self.id)
    #     db.session.add(p)
    #     db.session.commit()
        
        
class Product(db.Model):
    __tablename__ = "Products"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String, nullable=False)
    product_name = db.Column(db.String, nullable=False)
    product_type = db.Column(db.String, nullable=False)
    unit_price = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    id_supplier = db.Column(db.String, db.ForeignKey("Suppliers.id"), nullable=False)
    

class Customer(db.Model):
    __tablename__ = "Customers"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String, nullable=False)
    customer_name = db.Column(db.String, nullable=False)
    adress = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

#lớp usermixin triển khai các mặc định cho thuộc tính 
class Admin(UserMixin, db.Model):
    __tablename__ = "Admins"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.String, nullable=False)
    fullname = db.Column(db.String)
    password = db.Column(db.String)
    phone = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    
    #decorator
    @login.user_loader  #tải thông tin người dùng từ csdl dựa trên id
    def load_user(id):
        return Admin.query.get(int(id))
    
    def set_password(self, password_input):
        self.password = generate_password_hash(password_input)


    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)
    

class Storepoint(db.Model):
    __tablename__ = "Storepoint"
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    geom = db.Column(Geometry('POINT'))
    