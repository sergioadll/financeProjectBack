from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer primary_key=True, db.relationship('WatchList', lazy=True))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    admin = db.Column(db.Boolean() unique=False, nullable=False, default=False)


    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password":self.password,
            "name":self.name,
            "last_name": self.last_name,
            "admin":self.Admin,
            "id_lazy": list(map(lambda x: x.serialize(), self.children))
            # do not serialize the password, its a security breach
        }

class WatchList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    name = db.Column(db.String(120), unique=False, nullable=False)


    def __repr__(self):
        return '<WatchList %r>' % self.user_id

    def serialize(self):
        return {
            "id": self.id,
            "user_id":self.user_id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    symbol = db.Column(db.String(12),  db.relationship('ElementList', lazy=True))


    def __repr__(self):
        return '<Stock %r>' % self.watchlist_id   //que nos lo expliquen 

    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "symbol": self.symbol,
            # do not serialize the password, its a security breach
        }

class ElementList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    watchlist_id = db.Column(db.Integer, db.ForeignKey("WatchList.id"))
    stock_symbol = db.Column(db.String(12), db.ForeignKey("Stock.symbol"))


    def __repr__(self):
        return '<ElementList %r>' % self.watchlist_id   //que nos lo expliquen 

    def serialize(self):
        return {
            "id": self.id,
            "watchlist_id":self.watchlist_id,
            "stock_symbol": self.stock_symbol,
            # do not serialize the password, its a security breach
        }
