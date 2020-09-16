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
            "watchlists": list(map(lambda x: x.serialize(), self.watchlists)),
            "admin":self.admin
            # do not serialize the password, its a security breach
        }

watchelements = db.Table('watchelements',
        db.Column('watchlist_id', db.Integer, db.ForeignKey('watch_list.id'), primary_key=True),
        db.Column('stock_id', db.Integer, db.ForeignKey('stock.id'), primary_key=True)
    )

class WatchList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False )
    name = db.Column(db.String(120), unique=False, nullable=False)

    stocks= db.relationship('Stock',secondary="watchelements", back_populates="watchlists")


    def __repr__(self):
        return '<WatchList %r>' % self.name

    def watch_list_serialize(self):
        return {
            "id": self.id, 
            "name": self.name
        }

    def serialize(self):
        return {
            "stocks" : list(map(lambda x: x.serialize(), self.stocks))
        }   
 

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    symbol = db.Column(db.String(12))

    watchlists= db.relationship('WatchList', secondary="watchelements", back_populates="stocks")

    def __repr__(self):
        return '<Stock %r>' % self.symbol

    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "symbol": self.symbol,
        }
