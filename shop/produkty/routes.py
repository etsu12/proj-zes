from flask import redirect, render_template, url_for, flash, request
from shop import db, app
from .models import Marka, Kategoria

@app.route('/dodajmarke', methods=['GET','POST'])
def dodajmarke():
    if request.method == "POST":
        getmarka = request.form.get('marka')
        marka = Marka(name=getmarka)
        db.session.add(marka)
        flash(f'Marka {getmarka} została dodana do bazy.', 'success')
        db.session.commit()
        return redirect(url_for('dodajmarke'))

    return render_template('produkty/dodajmarke.html',marki='marki')

@app.route('/dodajkategorie', methods=['GET','POST'])
def dodajkategorie():
    if request.method == "POST":
        getkategoria = request.form.get('kategoria')
        kategoria = Kategoria(name=getkategoria)
        db.session.add(kategoria)
        flash(f'Kategoria {getkategoria} została dodana do bazy.', 'success')
        db.session.commit()
        return redirect(url_for('dodajmarke'))

    return render_template('produkty/dodajmarke.html')