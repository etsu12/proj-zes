from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators
from flask_wtf.file import FileRequired, FileAllowed, FileField

class KlientRejestracjaForm(Form):
    dane = StringField('Imię i nazwisko: ')
    login = StringField('Login: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    haslo = PasswordField('Hasło: ', [validators.DataRequired(), validators.EqualTo('potwierdz', message='Hasła muszą się zgadzać')])
    potwierdz = PasswordField('Potwierdź hasło: ', [validators.DataRequired()])
    kraj = StringField('Kraj: ', [validators.DataRequired()])
    panstwo = StringField('Państwo: ', [validators.DataRequired()])
    miasto = StringField('Miasto: ', [validators.DataRequired()])
    kontakt = StringField('Kontakt: ', [validators.DataRequired()])
    adres = StringField('Adres: ', [validators.DataRequired()])
    kodpocztowy = StringField('Kod pocztowy: ', [validators.DataRequired()])

    profilowe = FileField('Zdjęcie profilowe: ', validators=[FileAllowed(['jpg','png','jpeg','gif'], 'Tylko zdjęcia')])

    zatwierdz = SubmitField('Zarejestruj')
    