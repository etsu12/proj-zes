from flask import render_template, session, request, redirect, url_for, flash

from shop import app, db, bcrypt
from .forms import RegistrationForm
from .models import User
import os

@app.route('/')
def home():
    return "Home page of the shop"

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data,
                     password=hash_password)
        db.session.add(user)
        flash('Dziękujemy za rejestrację')
        return redirect(url_for('home'))
    return render_template('admin/rejestracja.html', form=form, title="Rejestracja")