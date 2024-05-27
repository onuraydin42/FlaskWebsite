from dataclasses import dataclass
from restaurantres import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash


#------------------------------------------------------------------------------------------------
@dataclass
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    activated = db.Column(db.Boolean, default=True)

    def __init__(self, username, email, password, activated):
        self.username = username
        self.email = email
        self.password = password
        self.activated = activated

    @classmethod
    def get_all_users(cls):
        return cls.query.all()
    
    @classmethod
    def get_user_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def add_user(cls, username, email, password):
        
        user = cls(username, email, password, True)
    
        db.session.add(user)
        db.session.commit()

    @classmethod
    def update_user(cls, id, username, email, password):
        user = cls.query.filter_by(id=id).first()
        user.username = username
        user.email = email
        user.password = password
        db.session.commit()
    
    @classmethod
    def delete_user(cls, id):
        user = cls.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()

    @classmethod
    def activate_user(cls, id):
        user = cls.query.filter_by(id=id).first()
        user.activated = True
        db.session.commit()
    
    @classmethod
    def deactivate_user(cls, id):
        user = cls.query.filter_by(id=id).first()
        user.activated = False
        db.session.commit()

    @classmethod
    def get_deactive_users(cls):
        return cls.query.filter_by(activated=False).all()
    
    @property
    def is_active(self):
        return self.activated
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

#------------------------------------------------------------------------------------------------
@dataclass
class Admin(db.Model):
        __tablename__ = "admin"

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(120), nullable=False, unique=True)
        email = db.Column(db.String(120), nullable=False, unique=True)
        password = db.Column(db.String(500))
        mod = db.Column(db.Integer, default=0)

        def __init__(self, id, name, email, password, mod):
            self.id = id
            self.name = name
            self.email = email
            self.password = password
            self.mod = mod

        @classmethod
        def get_all_admins(cls):
            return cls.query.all()

        @classmethod
        def get_admin_by_id(cls, id):
            return cls.query.filter_by(id=id).first()

        @classmethod
        def add_admin(cls, name, email, password):
            admin = cls(None, name, email, password, 0)
            db.session.add(admin)
            db.session.commit()

        @classmethod
        def update_admin(cls, id, name, email, password):
            admin = cls.query.filter_by(id=id).first()
            admin.name = name
            admin.email = email
            admin.password = password
            db.session.commit()

        @classmethod
        def delete_admin(cls, id):
            admin = cls.query.filter_by(id=id).first()
            db.session.delete(admin)
            db.session.commit()
#------------------------------------------------------------------------------------------------
@dataclass
class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def __init__(self, name, id):
        self.id = id
        self.name = name

    @classmethod
    def get_all_categories(cls):
        return cls.query.all()
    
    @classmethod
    def get_category_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def add_category(cls, name):
        category = cls(name, None)
        db.session.add(category)
        db.session.commit()
    
    @classmethod
    def update_category(cls, id, name):
        category = cls.query.filter_by(id=id).first()
        category.name = name
        db.session.commit()
    
    @classmethod
    def delete_category(cls, id):
        category = cls.query.filter_by(id=id).first()
        db.session.delete(category)
        db.session.commit()
        return category
#------------------------------------------------------------------------------------------------
@dataclass
class Product(db.Model):
    table_name = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.Float)
    oldPrice = db.Column(db.Float)
    description = db.Column(db.String(120))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __init__(self, id, name, price, oldPrice, description, category_id):
        self.id = id
        self.name = name
        self.price = price
        self.oldPrice = oldPrice
        self.description = description
        self.category_id = category_id

    @classmethod
    def get_all_products(cls):
        return cls.query.all()
    
    @classmethod
    def get_product_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def add_product(cls, name, price, oldPrice, description, category_id):
        product = cls(None, name, price, oldPrice, description, category_id)
        db.session.add(product)
        db.session.commit()
    
    @classmethod
    def update_product(cls, id, name, price, old_price, description, category_id):
        product = cls.query.filter_by(id=id).first()
        product.name = name
        product.price = price
        product.oldPrice = old_price
        product.description = description
        product.category_id = category_id
        db.session.commit()
    
    @classmethod
    def delete_product(cls, id):
        product = cls.query.filter_by(id=id).first()
        db.session.delete(product)
        db.session.commit()
        return product
    
@dataclass
class Reservation(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    phonenumber = db.Column(db.String(120))
    date = db.Column(db.String(120))
    time = db.Column(db.String(120))
    guests = db.Column(db.Integer)
    tablenum= db.Column(db.Integer)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String(500))


    def __init__(self, id, user_id, phonenumber, date, time, guests, tablenum, rating, comment):
        self.id = id
        self.user_id = user_id
        self.phonenumber = phonenumber
        self.date = date
        self.time = time
        self.guests = guests
        self.tablenum = tablenum
        self.rating = rating
        self.comment = comment

    @classmethod
    def get_all_reservations(cls):
        return cls.query.all()
    
    @classmethod
    def get_reservation_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def add_reservation(cls, user_id, phonenumber, date, time, guests, tablenum, rating=None, comment=None):
        reservation = cls(None, user_id, phonenumber, date, time, guests, tablenum, rating, comment)
        db.session.add(reservation)
        db.session.commit()
    
    @classmethod
    def update_reservation_rating_comment(cls, id, rating, comment):
        reservation = cls.query.filter_by(id=id).first()
        reservation.rating = rating
        reservation.comment = comment
        db.session.commit()

    @classmethod
    def delete_reservation(cls, id):
        reservation = cls.query.filter_by(id=id).first()
        db.session.delete(reservation)
        db.session.commit()
        return reservation
    
    @classmethod
    def get_reservations_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def is_table_reserved(cls, date, time, tablenum):
        reservation = cls.query.filter_by(date=date, time=time, tablenum=tablenum).first()
        return reservation is not None
    
    

    @classmethod
    def determine_price_level(cls):
        density = cls.query.count()
        if density < 10:
            return "low"
        elif density < 20:
            return "medium"
        else:
            return "high"
    
    @classmethod
    def calculate_price(cls,price_level):
        if price_level == "low":
            return 100
        elif price_level == "medium":
            return 200
        else:
            return 300

