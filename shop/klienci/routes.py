from flask import redirect, render_template, url_for, flash, request, session, current_app, make_response
from flask_login import login_required, current_user, logout_user, login_user
from shop import db, app, photos, search, bcrypt, login_manager
from .forms import KlientRejestracjaForm, KlientLoginForm
from .model import KlientZamowienie, Rejestracja
import secrets, os
import json
import pdfkit
import stripe

publishable_key = 'pk_test_51KEzQQJbsOPtazjmDvqi5okBwviAIFg6TSg8FMyPnbnPKqqXcxLS0C6L7OOFAzGFIaNM98osOMqhSwsFlJG9eV9l00Fg3IM3lr'

stripe.api_key = 'sk_test_51KEzQQJbsOPtazjmZY7On3s9L4x2tnnvQH7ABqUh3ObLllLGQRRmT3LVAIMXPq4vsEO6WJBlEJr8QEZ7cuH01EGB00I3uSXrJL'

@app.route('/platnosc', methods=['POST'])
@login_required
def platnosc():
    faktura = request.form.get('faktura')
    ilosc = request.form.get('ilosc')
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        description='Płatność kartą',
        amount=ilosc,
        currency='pln',
    )
    zamowienia = KlientZamowienie.query.filter_by(klient_id=current_user.id, faktura=faktura).order_by(KlientZamowienie.id.desc()).first()
    zamowienia.status = 'Zapłacone'
    db.session.commit()
    return redirect(url_for('dziekujemy'))

@app.route('/dziekujemy')
def dziekujemy():
    return render_template('klient/dziekujemy.html')

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

#usuniecie niepotrzebnych rzeczy z koszyka
def aktualizujkoszyk():
    for _key, product in session['Koszyk'].items():
        session.modified = True
        del product['zdjecie']
        del product['kolory']
    return aktualizujkoszyk


@app.route('/getzamowienie')
@login_required
def get_zamowienie():
    if current_user.is_authenticated:
        klient_id = current_user.id
        faktura = secrets.token_hex(5)
        aktualizujkoszyk()
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
            sumaCalosc = ("%.2f" % (1.06 * float(sumaCzesc)))

    else:
        return redirect(url_for('klientLogin'))
    return render_template('klient/zamowienie.html', faktura=faktura, podatek=podatek, sumaCzesc=sumaCzesc, sumaCalosc=sumaCalosc, klient=klient, zamowienia=zamowienia)

@app.route('/get_pdf/<faktura>', methods=['POST'])
@login_required
def get_pdf(faktura):
    if current_user.is_authenticated:
        sumaCalosc = 0
        sumaCzesc = 0
        klient_id = current_user.id
        config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
        if request.method == "POST":
            klient = Rejestracja.query.filter_by(id=klient_id).first()
            zamowienia = KlientZamowienie.query.filter_by(klient_id=klient_id, faktura=faktura).order_by(KlientZamowienie.id.desc()).first() # tylko jeden rekord
            for _key, produkt in zamowienia.zamowienia.items():
                znizka = (produkt['znizka']/100) * float(produkt['cena']) * float(produkt['ilosc'])
                sumaCzesc += float(produkt['cena']) * int(produkt['ilosc'])
                sumaCzesc -= znizka
                podatek = ("%.2f" % (.06 * float(sumaCzesc)))
                sumaCalosc = ("%.2f" % (1.06 * float(sumaCzesc)))

            rendered = render_template('klient/pdf.html', faktura=faktura, podatek=podatek, sumaCalosc=sumaCalosc, klient=klient, zamowienia=zamowienia)
            pdf = pdfkit.from_string(rendered, False, configuration=config)
            response = make_response(pdf)
            response.headers['content-Type']='application/pdf'
            response.headers['content-Disposition']='inline: filename='+faktura+'.pdf'
            return response
    return request(url_for('zamowienia'))
