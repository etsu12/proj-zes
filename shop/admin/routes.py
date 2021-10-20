from flask import render_template, session, request, redirect, url_for, flash

from shop import app, db, bcrypt
from .forms import RegistrationForm
from .models import User
import os

@app.route('/')
def home():
    return render_template('admin/index.html', title="Strona administracyjna")

@app.route('/rejestracja', methods=['GET', 'POST'])
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