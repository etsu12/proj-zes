from flask import redirect, render_template, url_for, flash, request, session, current_app
from flask_login import login_required, current_user, logout_user, login_user
from shop import db, app, photos, search, bcrypt, login_manager
from .forms import KlientRejestracjaForm, KlientLoginForm
from .model import Rejestracja
import secrets, os

@app.route('/klient/rejestracja', methods=['GET','POST'])
def klient_rejestracja():
    form = KlientRejestracjaForm()
    if form.validate_on_submit():
        print(form.errors)
        hash_haslo = bcrypt.generate_password_hash(form.haslo.data)
        rejestracja = Rejestracja(dane=form.dane.data, login=form.login.data, email=form.email.data, haslo=hash_haslo, kraj=form.kraj.data, 
        miasto=form.miasto.data, kontakt=form.kontakt.data, adres=form.adres.data, kodpocztowy=form.kodpocztowy.data)
        db.session.add(rejestracja)
        flash(f'Witaj  {form.dane.data}! Dziękujemy za rejestrację.', 'success')
        db.session.commit()
        return redirect(url_for('klientLogin'))

    return render_template('klient/rejestracja.html', form=form)

@app.route('/klient/login', methods=['GET', 'POST'])
def klientLogin():
    form = KlientLoginForm()
    if form.validate_on_submit():
        user = Rejestracja.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.haslo, form.haslo.data):
            login_user(user)
            flash('Pomyślnie zalogowano', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Wprowadzono nieprawidłowe dane', 'danger')
        return redirect(url_for('klientLogin'))

    return render_template('klient/login.html', form=form)

@app.route('/klient/wyloguj')
def klient_wyloguj():
    logout_user()
    return redirect(url_for('home'))