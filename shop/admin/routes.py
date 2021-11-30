from flask import render_template, session, request, redirect, url_for, flash

from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from shop.produkty.models import dodajProdukt
import os

@app.route('/')
def admin():
    if 'email' not in session:
        flash(f'Proszę się zalogować.','danger')
        return redirect(url_for('login'))
    produkty = dodajProdukt.query.all()
    return render_template('admin/index.html', title="Strona administracyjna", produkty=produkty)

@app.route('/rejestracja', methods=['GET','POST'])
def rejestruj():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data,
                     password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Dziękujemy za rejestrację, {form.username.data}','success')
        return redirect(url_for('home'))
    return render_template('admin/rejestracja.html', form=form, title="Rejestracja")

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Witaj, {form.email.data}. Zostałeś zalogowany.','success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wprowadzono błędne hasło.', 'danger')

    return render_template('admin/login.html', form=form, title="Logowanie")