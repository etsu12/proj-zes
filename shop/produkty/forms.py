from wtforms import IntegerField, StringField, BooleanField, TextAreaField, validators, Form
from flask_wtf.file import FileAllowed, FileField, FileRequired

class dodajProdukty(Form):
    nazwa = StringField('Nazwa',[validators.DataRequired()])
    cena = IntegerField('Cena',[validators.DataRequired()])
    znizka = IntegerField('Zniżka', default=0)
    ilosc = IntegerField('Ilość',[validators.DataRequired()])
    opis = TextAreaField('Opis',[validators.DataRequired()])
    kolory = TextAreaField('Kolory',[validators.DataRequired()])

    zdjecie_1 = FileField('Zdjęcie 1', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    zdjecie_2 = FileField('Zdjęcie 1', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    zdjecie_3 = FileField('Zdjęcie 1', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])