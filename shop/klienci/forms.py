from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from .model import Rejestracja

class KlientRejestracjaForm(FlaskForm):
    dane = StringField('Imię i nazwisko: ')
    login = StringField('Login: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    haslo = PasswordField('Hasło: ', [validators.DataRequired(), validators.EqualTo('potwierdz', message='Hasła muszą się zgadzać')])
    potwierdz = PasswordField('Potwierdź hasło: ', [validators.DataRequired()])
    kraj = StringField('Kraj: ', [validators.DataRequired()])
    miasto = StringField('Miasto: ', [validators.DataRequired()])
    kontakt = StringField('Kontakt: ', [validators.DataRequired()])
    adres = StringField('Adres: ', [validators.DataRequired()])
    kodpocztowy = StringField('Kod pocztowy: ', [validators.DataRequired()])

    profilowe = FileField('Zdjęcie profilowe: ', validators=[FileAllowed(['jpg','png','jpeg','gif'], 'Tylko zdjęcia')])

    zatwierdz = SubmitField('Zarejestruj')

    def validate_login(self, login):
        if Rejestracja.query.filter_by(login=login.data).first():
            raise ValidationError("Ten login jest już zajęty.")

    def validate_email(self, email):
        if Rejestracja.query.filter_by(email=email.data).first():
            raise ValidationError("Ten adres email jest już zajęty.")
    
class KlientLoginForm(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    haslo = PasswordField('Hasło: ', [validators.DataRequired()])
