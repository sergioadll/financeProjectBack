from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()
#class UserType(enum.Enum):
#    admin = 1
#    trader = 0

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    admin = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    watchlists =  db.relationship('WatchList', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "last_name": self.last_name,
            "watchlists": self.watchlists,
            "admin":self.admin
            # do not serialize the password, its a security breach
        }
class WatchList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False )
    name = db.Column(db.String(120), unique=False, nullable=False)

    watchelements= db.relationship('WatchElement',backref='watch_list', lazy=True)


    def __repr__(self):
        return '<WatchList %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "user_id":self.user_id,
            "name": self.name,
        }    

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    symbol = db.Column(db.String(12))

    watchelements= db.relationship('WatchElement', backref='stock', lazy=True)

    def __repr__(self):
        return '<Stock %r>' % self.symbol

    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "symbol": self.symbol,
        }

class WatchElement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    watchlist_id = db.Column(db.Integer, db.ForeignKey("watch_list.id"))
    stock_id = db.Column(db.Integer, db.ForeignKey("stock.id"))




    def __repr__(self):
        return '<WatchElement %r>' % self.stock_id

    def serialize(self):
        return {
            "id": self.id,
            "watchlist_id":self.watchlist_id,
            "stock_symbol": self.stock_id,
        }

