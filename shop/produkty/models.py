from shop import db

from datetime import datetime


class dodajProdukt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(80), nullable=False)
    cena = db.Column(db.Numeric(10,2), nullable=False)
    znizka = db.Column(db.Integer, default=0)
    ilosc = db.Column(db.Integer, nullable=False)
    kolory = db.Column(db.Text, nullable=False)
    opis = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    marka_id = db.Column(db.Integer, db.ForeignKey('marka.id'),nullable=False)
    marka = db.relationship('Marka',backref=db.backref('marki', lazy=True))

    kategoria_id = db.Column(db.Integer, db.ForeignKey('kategoria.id'),nullable=False)
    kategoria = db.relationship('Kategoria',backref=db.backref('posts', lazy=True))

    zdjecie_1 = db.Column(db.String(150), nullable=False, default='image.jpg')
    zdjecie_2 = db.Column(db.String(150), nullable=False, default='image.jpg')
    zdjecie_3 = db.Column(db.String(150), nullable=False, default='image.jpg')

    def __repr__(self):
        return '<dodajProdukt %r>' % self.name

class Marka(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

class Kategoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

db.create_all()