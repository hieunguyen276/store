from msilib.schema import AdminUISequence
from flask import jsonify
from email import message
from turtle import title
from flask import render_template, request, flash, redirect, url_for
from scipy.fftpack import idst
from app import app
from sqlalchemy import func
from app.models import *
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
import json

@app.route("/")
def index():
    return render_template ("index.html")


@app.route("/manager")
@login_required    #kiểm tra yêu cầu và chuyển về trang admin
def manager():
    return render_template ("manager.html")


# ---------- sign up using flask form----------------
@app.route("/signUp", methods=["GET", "POST"])
def signUp():
    """show sign up form"""

    form = signUpForm()
    if form.validate_on_submit(): #nếu tất cả dữ liệu đúng thì bằng true cho phép dăng ký người dùng mới
        adminId = form.adminId.data #lấy dữ liệu từ class form
        fullName = form.fullName.data
        password = form.password.data
        phone = form.phone.data
        email = form.email.data
        NewAdmin = Admin(admin_id=adminId, fullname=fullName, password=password, phone=phone, email=email)
        NewAdmin.set_password(form.password.data)
        db.session.add(NewAdmin)
        db.session.commit()
        flash('Congratulations, you have become an admin')
        return redirect(url_for('index'))
    return render_template("signUp.html", form=form)


#------------Login-----------------------
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('manager'))
    form = loginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(admin_id=form.adminId.data).first()
        if admin is None or not admin.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(admin, remember=form.remember_me.data)
        next_page = request.args.get('next') #Tham số next đc gán giá trị của url yêu cầu ban đầu
        if not next_page:                      #từ đó ứng dụng sẽ biết cần phải trở lại trang tr khi admin đăng nhập thành công
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


#-----------------Logout-----------------------------
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


#-------------admin_manager-----------------------------
@app.route('/admin_manager')
def admin_manager():
    admins = Admin.query.all()
    return render_template("admin_manager.html", admin=admins)


#-----------------admin_delete----------------------------

@app.route("/admin_delete", methods=["POST"])
def admin_delete():
    admin_id = int(request.form.get("admin_id"))
    admin = Admin.query.get(admin_id)
    db.session.delete(admin)
    db.session.commit()
    return redirect (url_for('admin_manager'))

#------------------admin_update----------------------------

@app.route('/admin_update_s1')
def admin_update_s1():
    admins = Admin.query.all()
    return render_template("admin_update_s1.html", admin=admins)


@app.route("/admin_update_s2/<int:admin_id>")
def admin_update_s2(admin_id):
    admin = Admin.query.get(admin_id)
    return render_template("admin_update_s2.html", admin=admin)


@app.route("/admin_update_result")
def admin_update_result():
    adminId = request.args.get("adminId")
    admin_id = request.args.get("admin_id")
    fullname = request.args.get("fullname")
    password = request.args.get("password")
    phone = request.args.get("phone")
    email = request.args.get("email")
    
    admin = Admin.query.get(adminId)
    admin.admin_id = admin_id
    admin.fullname = fullname
    admin.password = password
    admin.phone = phone
    admin.email = email
    db.session.commit()
    flash ('Update success')
    return redirect(url_for('admin_update_s1'))
    #return render_template("admin_update_s1.html", message=message)
    

#-------------supplier_manager-----------------------------
@app.route('/supplier_manager')
def supplier_manager():
    suppliers = Supplier.query.all()
    return render_template("supplier_manager.html", supplier=suppliers)


@app.route("/add_supplier")
def add_supplier():
    return render_template("add_supplier.html")


@app.route("/add_supplier_s1", methods=["POST"])
def add_supplier_s1():
    supplier_id = request.form.get("supplier_id")
    supplier_name = request.form.get("supplier_name")
    adress = request.form.get("adress")
    phone = request.form.get("phone")
    fax = request.form.get("fax")
    home_page = request.form.get("home_page")

    supplier = Supplier(supplier_id=supplier_id, supplier_name=supplier_name, adress=adress, phone=phone, fax=fax, home_page=home_page)
    db.session.add(supplier)
    db.session.commit()
    return redirect(url_for('supplier_manager'))


# ---------------------supplier_update----------------------

@app.route("/supplier_update_s1")
def supplier_update_s1():
    supplier = Supplier.query.all()
    return render_template("supplier_update_s1.html", supplier=supplier)


@app.route("/supplier_update_s2/<int:supplier_id>")
def supplier_update_s2(supplier_id):
    supplier = Supplier.query.get(supplier_id)
    return render_template("supplier_update_s2.html", supplier=supplier)


@app.route("/supplier_update_result")
def supplier_update_result():
    supplierId = request.args.get("supplierId")
    supplier_id = request.args.get("supplier_id")
    supplier_name = request.args.get("supplier_name")
    adress = request.args.get("adress")
    phone = request.args.get("phone")
    fax = request.args.get("fax")
    home_page = request.args.get("home_page")
    
    supplier = Supplier.query.get(supplierId)
    supplier.supplier_id = supplier_id
    supplier.supplier_name = supplier_name
    supplier.adress = adress
    supplier.phone = phone
    supplier.fax = fax
    supplier.home_page = home_page
    db.session.commit()
    #message ="Successfully updated admin information"
    return redirect(url_for('supplier_manager'))


# ---------------------supplier_delete----------------------

@app.route("/supplier_delete")
def supplier_delete():
    suppliers = Supplier.query.all()
    return render_template("supplier_delete.html",supplier=suppliers)


@app.route("/supplier_delete_s1", methods=["POST"])
def supplier_delete_s1():
    supplierId = int(request.form.get("supplierId"))
    supplier = Supplier.query.get(supplierId)
    db.session.delete(supplier)
    db.session.commit()
    return redirect (url_for('supplier_manager'))

#----------------Search for supplier--------------

@app.route("/search_supplier")
def search_supplier():
    return render_template("search_supplier.html")

@app.route("/search_supplierv2", methods=["GET", "POST"])
def search_supplierv2():
    supplier_name = request.args.get("supplier_name")
    supplier = Supplier.query.filter_by(supplier_name=supplier_name).all()
    message = "Dưới đây là nhà cung cấp bạn tìm:   "
    return render_template("search_supplierv2.html" ,supplier=supplier, supplier_name=supplier_name, message=message)


#-------------customer_manager-----------------------------
@app.route('/customer_manager')
def customer_manager():
    customers = Customer.query.all()
    return render_template("customer_manager.html", customer=customers)


@app.route("/add_customer")
def add_customer():
    return render_template("add_customer.html")


@app.route("/add_customer_s1", methods=["POST"])
def add_customer_s1():
    customer_id = request.form.get("customer_id")
    customer_name = request.form.get("customer_name")
    adress = request.form.get("adress")
    phone = request.form.get("phone")
    email = request.form.get("email")

    customer = Customer(customer_id=customer_id, customer_name=customer_name, adress=adress, phone=phone, email=email)
    db.session.add(customer)
    db.session.commit()
    return redirect(url_for('customer_manager'))



# ---------------------customer_upgrade----------------------

@app.route("/customer_update_s1")
def customer_update_s1():
    customer =Customer.query.all()
    return render_template("customer_update_s1.html", customer=customer)


@app.route("/customer_update_s2/<int:customer_id>")
def customer_update_s2(customer_id):
    customer = Customer.query.get(customer_id)
    return render_template("customer_update_s2.html", customer=customer)


@app.route("/customer_update_result")
def customer_update_result():
    customerId = request.args.get("customerId")
    customer_id = request.args.get("customer_id")
    customer_name = request.args.get("customer_name")
    adress = request.args.get("adress")
    phone = request.args.get("phone")
    email = request.args.get("email")
    
    supplier = Customer.query.get(customerId)
    supplier.customer_id = customer_id
    supplier.customer_name = customer_name
    supplier.adress = adress
    supplier.phone = phone
    supplier.email = email
    db.session.commit()
    #message ="Successfully updated customer information"
    return redirect(url_for('customer_manager'))


# ---------------------customer_delete----------------------

@app.route("/customer_delete")
def customer_delete():
    customers = Customer.query.all()
    return render_template("customer_delete.html",customer=customers)


@app.route("/customer_delete_s1", methods=["POST"])
def customer_delete_s1():
    customerId1 = int(request.form.get("customerId1"))
    customer = Customer.query.get(customerId1)
    db.session.delete(customer)
    db.session.commit()
    return redirect (url_for('customer_manager'))



#-------------product_manager-----------------------------
@app.route('/product_manager')
def product_manager():
    products = Product.query.all()
    return render_template("product_manager.html", product=products)


@app.route("/add_product")
def add_product():
    return render_template("add_product.html")


@app.route("/add_product_s1", methods=["POST"])
def add_product_s1():
    product_id = request.form.get("product_id")
    product_name = request.form.get("product_name")
    product_type = request.form.get("product_type")
    unit_price = request.form.get("unit_price")
    amount = request.form.get("amount")
    id_supplier = request.form.get("id_supplier")

    product = Product(product_id=product_id, product_name=product_name, product_type=product_type, unit_price=unit_price, amount=amount, id_supplier=id_supplier)
    # supplierID = request.form.get("supplierID")
    # supplier = Supplier.query.get(supplierID)
    # supplier.add_product(product_id, product_name, product_type, unit_price, amount, id_supplier)
    db.session.add(product)
    db.session.commit()
    return redirect(url_for('product_manager'))

# ---------------------product_update----------------------

@app.route("/product_update_s1")
def product_update_s1():
    product = Product.query.all()
    return render_template("product_update_s1.html", product=product)


@app.route("/product_update_s2/<int:product_id>")
def product_update_s2(product_id):
    product = Product.query.get(product_id)
    return render_template("product_update_s2.html", product=product)


@app.route("/product_update_result")
def product_update_result():
    productId = request.args.get("productId")
    product_id = request.args.get("product_id")
    product_name = request.args.get("product_name")
    product_type = request.args.get("product_type")
    unit_price = request.args.get("unit_price")
    amount = request.args.get("amount")
    id_supplier = request.args.get("id_supplier")
    
    product = Product.query.get(productId)
    product.product_id = product_id
    product.product_name = product_name
    product.product_type = product_type
    product.unit_price = unit_price
    product.amount = amount
    product.id_supplier = id_supplier
    db.session.commit()
    #message ="Successfully updated admin information"
    return redirect(url_for('product_manager'))


# ---------------------product_delete----------------------

@app.route("/product_delete")
def product_delete():
    products = Product.query.all()
    return render_template("product_delete.html",product=products)


@app.route("/product_delete_s1", methods=["POST"])
def product_delete_s1():
    productId1 = int(request.form.get("productId1"))
    product = Product.query.get(productId1)
    db.session.delete(product)
    db.session.commit()
    return redirect (url_for('product_manager'))

#----------------Search for product--------------

@app.route("/search_product")
def search_product():
    return render_template("search_product.html")

@app.route("/search_productv2", methods=["GET", "POST"])
def search_productv2():
    product_name = request.args.get("product_name")
    product = Product.query.filter_by(product_name=product_name).all()
    message = "Dưới đây là sản phẩm bạn tìm:   "
    return render_template("search_productv2.html" ,product=product, product_name=product_name, message=message)


#--------------------GIS---------------

@app.route("/map_store")
def map_store():
    return render_template("map_store.html")

@app.route("/add_store", methods=["GET"])
def add_store():
    form = addstore()
    return render_template("add_store.html", form=form)


@app.route("/add_storev1", methods=["POST"])
def add_storev1():
    """add new ATM"""
    # Get form information.
    id = request.form.get("id")
    store_name = request.form.get("store_name")
    address = request.form.get("address")
    image = request.form.get("image")
    geomInput = 'Point(' + request.form.get("lng") + " " + request.form.get("lat") + ")"
    newStore = Storepoint(id=id, store_name=store_name, address=address, image=image, geom=func.ST_GeomFromText(geomInput, 4326))
    db.session.add(newStore)
    db.session.commit()
    message = "Thêm thành công chi nhánh mới"
    return render_template("map_store.html", message=message)


# Api
@app.route("/data/stores")
def store_get_API():
    """Return feature in point table"""
    store = db.session.query(Storepoint.id, Storepoint.store_name, Storepoint.address, Storepoint.image, \
    func.ST_AsGeoJSON(Storepoint.geom).label('geometry')).all()
    # Nhận tất cả
    storeFeatures = []  # lưu trữ tất cả các cửa hàng
    for store in store:  # tạo geojson cho mỗi cửa hàng
        store_temp = {}
        store_temp["type"] = "Feature"
        store_temp["properties"] = {
            "id": store.id,
            "name": store.store_name,
            "address": store.address,
            "image": store.image,
        }
        store_temp["geometry"] = json.loads(store.geometry)
        #json.loads loại bỏ các ký tự / khi sử dụng hàm ST_AsGeoJSON
        storeFeatures.append(store_temp)  # thêm cửa hàng geojson vào danh sách

    return jsonify({  # chuyển đổi sang định dạng geojson
            "features": storeFeatures
        })

#----------------update_store------------------------------


@app.route("/update_store")
def update_store():
    store = Storepoint.query.all()
    return render_template("update_store.html", store=store)
    


@app.route("/update_storev1", methods=["POST"])
def update_storev1():
    form = addstore()
    id = request.form.get("id")
    store = Storepoint.query.filter_by(id=id).first()
    return render_template("update_storev1.html", store=store, form=form)


@app.route("/update_storev2", methods=["POST"])
def update_storev2():
    id = request.form.get("id")
    store_name = request.form.get("store_name")
    address = request.form.get("address")
    image = request.form.get("image")
    geom = 'Point(' + request.form.get("lng") + " " + request.form.get("lat") + ")"

    store = Storepoint.query.get(id)

    store.store_name = store_name
    store.address = address
    store.image = image
    store.geom = func.ST_GeomFromText(geom, 4326)
    db.session.commit()
    message = "Update success"
    return render_template("map_store.html", message=message)


#-------------------------delete_store------------------------------------


@app.route("/delete_store")
def delete_store():
    store = Storepoint.query.all()
    return render_template("delete_store.html", store=store)


@app.route("/delete_storev1", methods=["POST"])
def delete_storev1():
    id = request.form.get("id")
    store = Storepoint.query.get(id)
    db.session.delete(store)
    db.session.commit()
    message = "Delete success"
    return render_template("map_store.html", message=message)