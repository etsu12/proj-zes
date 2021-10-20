from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    username = StringField('Nazwa użytkownika', [validators.Length(min=4, max=25, message="Pole musi zawierać minimalnie 4 znaki, a maksymalnie 25.")])
    email = StringField('Adres e-mail', [validators.Length(min=6, max=35, message="Pole musi zawierać minimalnie 6 znaków, a maksymalnie 35."), validators.Email("Niepoprawny adres email")])
    password = PasswordField('Hasło', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Hasła muszą się zgadzać')
    ])
    confirm = PasswordField('Powtórz hasło')