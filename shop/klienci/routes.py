from flask import redirect, render_template, url_for, flash, request, session, current_app
from flask_login import login_required, current_user, logout_user, login_user
from shop import db, app, photos, search, bcrypt, login_manager
from .forms import KlientRejestracjaForm, KlientLoginForm
from .model import KlientZamowienie, Rejestracja
import secrets, os
import json

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

@app.route('/getzamowienie')
@login_required
def get_zamowienie():
    if current_user.is_authenticated:
        klient_id = current_user.id
        faktura = secrets.token_hex(5)
        try:
            zamowienie = KlientZamowienie(faktura=faktura, klient_id=klient_id, zamowienia=session['Koszyk'])
            db.session.add(zamowienie)
            db.session.commit()
            session.pop('Koszyk')
            flash('Twoje zamówienie zostało wysłane pomyślnie','success')
            return redirect(url_for('zamowienia', faktura=faktura))
        except Exception as e:
            print(e)
            flash('Coś poszło nie tak podczas wysyłania zamówienia', 'danger')
            return redirect(url_for('getKoszyk'))

@app.route('/zamowienia/<faktura>')
@login_required
def zamowienia(faktura):
    if current_user.is_authenticated:
        sumaCalosc = 0
        sumaCzesc = 0
        klient_id = current_user.id
        klient = Rejestracja.query.filter_by(id=klient_id).first()
        zamowienia = KlientZamowienie.query.filter_by(klient_id=klient_id).order_by(KlientZamowienie.id.desc()).first() # tylko jeden rekord
        for _key, produkt in zamowienia.zamowienia.items():
            znizka = (produkt['znizka']/100) * float(produkt['cena']) * float(produkt['ilosc'])
            sumaCzesc += float(produkt['cena']) * int(produkt['ilosc'])
            sumaCzesc -= znizka
            podatek = ("%.2f" % (.06 * float(sumaCzesc)))
            sumaCalosc = float("%.2f" % (1.06 * sumaCzesc))

    else:
        return redirect(url_for('klientLogin'))
    return render_template('klient/zamowienie.html', faktura=faktura, podatek=podatek, sumaCzesc=sumaCzesc, sumaCalosc=sumaCalosc, klient=klient, zamowienia=zamowienia)