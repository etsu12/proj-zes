from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos, search, bcrypt
from .forms import KlientRejestracjaForm
from .model import Rejestracja
import secrets, os

@app.route('/klient/rejestracja', methods=['GET','POST'])
def klient_rejestracja():
    form = KlientRejestracjaForm(request.form)
    if request.method == 'POST':
        hash_haslo = bcrypt.generate_password_hash(form.haslo.data)
        rejestracja = Rejestracja(dane=form.dane.data, login=form.login.data, email=form.email.data, haslo=hash_haslo, kraj=form.kraj.data,
        panstwo=form.panstwo.data, miasto=form.miasto.data, kontakt=form.kontakt.data, adres=form.adres.data, kodpocztowy=form.kodpocztowy.data)
        db.session.add(rejestracja)
        flash(f'Witaj  {form.dane.data}! Dziękujemy za rejestrację.', 'success')
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('klient/rejestracja.html', form=form)