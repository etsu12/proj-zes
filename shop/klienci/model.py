from shop import db
from datetime import datetime

class Rejestracja(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    dane = db.Column(db.String(50), unique = False)
    login = db.Column(db.String(50), unique = True)
    email = db.Column(db.String(50), unique = True)
    haslo = db.Column(db.String(200), unique = False)
    kraj = db.Column(db.String(50), unique = False)
    panstwo = db.Column(db.String(50), unique = False)
    miasto = db.Column(db.String(50), unique = False)
    kontakt = db.Column(db.String(50), unique = False)
    adres = db.Column(db.String(50), unique = False)
    kodpocztowy = db.Column(db.String(50), unique = False)
    profilowe = db.Column(db.String(200), unique = False, default='profilowe.jpg')
    data_stworzenia = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Rejestracja %r>' % self.name

db.create_all()