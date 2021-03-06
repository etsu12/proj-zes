from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos, search
from .models import Marka, Kategoria, dodajProdukt
from .forms import dodajProdukty
import secrets, os

def marki():
    marki = Marka.query.join(dodajProdukt, (Marka.id == dodajProdukt.marka_id)).all()
    return marki

def kategorie():
    kategorie = Kategoria.query.join(dodajProdukt, (Kategoria.id == dodajProdukt.kategoria_id)).all()
    return kategorie

@app.route('/')
def home():
    page = request.args.get('page',1,type=int)
    produkty = dodajProdukt.query.filter(dodajProdukt.ilosc > 0).order_by(dodajProdukt.id.desc()).paginate(page=page, per_page=8)
    return render_template('produkty/index.html', produkty=produkty, marki=marki(), kategorie=kategorie())

@app.route('/wynik')
def wynik():
    searchword = request.args.get('q')
    produkty = dodajProdukt.query.msearch(searchword, fields=['nazwa','opis'] , limit=6)
    return render_template('produkty/wynik.html', produkty=produkty, marki=marki(), kategorie=kategorie())

@app.route('/produkt/<int:id>')
def single_page(id):
    produkt = dodajProdukt.query.get_or_404(id)
    return render_template('produkty/single_page.html', produkt=produkt, marki=marki(), kategorie=kategorie())

@app.route('/marka/<int:id>')
def get_marka(id):
    get_m = Marka.query.filter_by(id=id).first_or_404()
    page = request.args.get('page', 1, type=int)
    marka = dodajProdukt.query.filter_by(marka=get_m).paginate(page=page, per_page=6)
    return render_template('produkty/index.html', marka=marka, marki=marki(), kategorie=kategorie(), get_m=get_m)

@app.route('/kategorie/<int:id>')
def get_kategoria(id):
    page = request.args.get('page',1,type=int)
    get_kat = Kategoria.query.filter_by(id=id).first_or_404()
    getkat_prod = dodajProdukt.query.filter_by(kategoria=get_kat).paginate(page=page, per_page=6)
    return render_template('produkty/index.html', getkat_prod=getkat_prod, kategorie=kategorie(), marki=marki(), get_kat=get_kat)

@app.route('/dodajmarke', methods=['GET','POST'])
def dodajmarke():
    if 'email' not in session:
        flash(f'Prosz?? si?? zalogowa??.','danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getmarka = request.form.get('marka')
        marka = Marka(name=getmarka)
        db.session.add(marka)
        flash(f'Marka {getmarka} zosta??a dodana do bazy.', 'success')
        db.session.commit()
        return redirect(url_for('dodajmarke'))
    return render_template('produkty/dodajmarke.html',marki='marki')

@app.route('/aktualizujmarke/<int:id>', methods=['GET','POST'])
def aktualizujmarke(id):
    if 'email' not in session:
        flash(f'Prosz?? si?? zalogowa??.','danger')
        return redirect(url_for('login'))

    aktualizujmarke = Marka.query.get_or_404(id)
    marka = request.form.get('marka')
    if request.method=="POST":
        aktualizujmarke.name = marka
        flash(f'Marka zosta??a zaktualizowana', 'success')
        db.session.commit()
        return redirect(url_for('marki'))

    return render_template('produkty/aktualizujmarke.html', title='Aktualizacja marki', aktualizujmarke = aktualizujmarke)

@app.route('/usunmarke/<int:id>', methods=['POST'])
def usunmarke(id):
    marka = Marka.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(marka)
        db.session.commit()
        flash(f'Marka {marka.name} zosta??a usuni??ta z bazy', 'success')
        return redirect(url_for('admin'))
    flash(f'Marka {marka.name} nie mo??e zosta?? usuni??ta', 'warning')
    return redirect(url_for('admin'))

@app.route('/dodajkategorie', methods=['GET','POST'])
def dodajkategorie():
    if 'email' not in session:
        flash(f'Prosz?? si?? zalogowa??.','danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getkategoria = request.form.get('kategoria')
        kategoria = Kategoria(name=getkategoria)
        db.session.add(kategoria)
        flash(f'Kategoria {getkategoria} zosta??a dodana do bazy.', 'success')
        db.session.commit()
        return redirect(url_for('dodajmarke'))
    return render_template('produkty/dodajmarke.html')

@app.route('/aktualizujkategorie/<int:id>', methods=['GET','POST'])
def aktualizujkategorie(id):
    if 'email' not in session:
        flash(f'Prosz?? si?? zalogowa??.','danger')
        return redirect(url_for('login'))

    aktualizujkategorie = Kategoria.query.get_or_404(id)
    kategoria = request.form.get('kategoria')
    if request.method=="POST":
        aktualizujkategorie.name = kategoria
        flash(f'Kategoria zosta??a zaktualizowana', 'success')
        db.session.commit()
        return redirect(url_for('kategorie'))

    return render_template('produkty/aktualizujmarke.html', title='Aktualizacja kategorii', aktualizujkategorie = aktualizujkategorie)

@app.route('/usunkategorie/<int:id>', methods=['POST'])
def usunkategorie(id):
    kategoria = Kategoria.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(kategoria)
        db.session.commit()
        flash(f'Kategoria {kategoria.name} zosta??a usuni??ta z bazy', 'success')
        return redirect(url_for('admin'))
    flash(f'Kategoria {kategoria.name} nie mo??e zosta?? usuni??ta', 'warning')
    return redirect(url_for('admin'))

@app.route('/dodajprodukt', methods=['GET','POST'])
def dodajprodukt():
    if 'email' not in session:
        flash(f'Prosz?? si?? zalogowa??.','danger')
        return redirect(url_for('login'))
    marki = Marka.query.all()
    kategorie = Kategoria.query.all()
    form = dodajProdukty(request.form)
    if request.method == "POST":
        nazwa = form.nazwa.data
        cena = form.cena.data
        znizka = form.znizka.data
        ilosc = form.ilosc.data
        kolory = form.kolory.data
        opis = form.opis.data
        marka = request.form.get('marka')
        kategoria = request.form.get('kategoria')
        zdjecie_1 = photos.save(request.files.get('zdjecie_1'), name=secrets.token_hex(10) + ".")
        zdjecie_2 = photos.save(request.files.get('zdjecie_2'), name=secrets.token_hex(10) + ".")
        zdjecie_3 = photos.save(request.files.get('zdjecie_3'), name=secrets.token_hex(10) + ".")

        dodajpro = dodajProdukt(nazwa=nazwa, cena=cena, znizka=znizka, ilosc=ilosc, kolory=kolory, opis=opis, marka_id=marka, kategoria_id=kategoria, zdjecie_1=zdjecie_1, 
        zdjecie_2=zdjecie_2, zdjecie_3=zdjecie_3)
        db.session.add(dodajpro)
        flash(f'Produkt {nazwa} zosta?? dodany do bazy.', 'success')
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('produkty/dodajprodukt.html', title="Dodawanie produktu", form=form, marki=marki, kategorie=kategorie)

@app.route('/aktualizujprodukt/<int:id>', methods=['GET','POST'])
def aktualizujprodukt(id):
    marki = Marka.query.all()
    kategorie = Kategoria.query.all()
    produkt = dodajProdukt.query.get_or_404(id)
    marka = request.form.get('marka')
    kategoria = request.form.get('kategoria')
    form = dodajProdukty(request.form)
    if request.method == "POST":
        produkt.nazwa = form.nazwa.data
        produkt.cena = form.cena.data
        produkt.znizka = form.znizka.data
        produkt.marka_id = marka
        produkt.kategoria_id = kategoria
        produkt.kolory = form.kolory.data
        produkt.opis = form.opis.data
        if request.files.get('zdjecie_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produkt.zdjecie_1))
                produkt.zdjecie_1 = photos.save(request.files.get('zdjecie_1'), name=secrets.token_hex(10) + ".")
            except:
                produkt.zdjecie_1 = photos.save(request.files.get('zdjecie_1'), name=secrets.token_hex(10) + ".")

        if request.files.get('zdjecie_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produkt.zdjecie_2))
                produkt.zdjecie_2 = photos.save(request.files.get('zdjecie_2'), name=secrets.token_hex(10) + ".")
            except:
                produkt.zdjecie_2 = photos.save(request.files.get('zdjecie_2'), name=secrets.token_hex(10) + ".")

        if request.files.get('zdjecie_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produkt.zdjecie_3))
                produkt.zdjecie_3 = photos.save(request.files.get('zdjecie_3'), name=secrets.token_hex(10) + ".")
            except:
                produkt.zdjecie_3 = photos.save(request.files.get('zdjecie_3'), name=secrets.token_hex(10) + ".")

        db.session.commit()
        flash(f'Produkt zosta?? zaktualizowany','success')
        return redirect('/admin')

    form.nazwa.data = produkt.nazwa
    form.cena.data = produkt.cena
    form.znizka.data = produkt.znizka
    form.ilosc.data = produkt.ilosc
    form.kolory.data = produkt.kolory
    form.opis.data = produkt.opis

    return render_template('produkty/aktualizujprodukt.html', form=form, marki=marki, kategorie=kategorie, produkt=produkt)

@app.route('/usunprodukt/<int:id>', methods=['POST'])
def usunprodukt(id):
    produkt = dodajProdukt.query.get_or_404(id)
    if request.method == "POST":
        try:
             os.unlink(os.path.join(current_app.root_path, "static/images/" + produkt.zdjecie_1))
             os.unlink(os.path.join(current_app.root_path, "static/images/" + produkt.zdjecie_2))
             os.unlink(os.path.join(current_app.root_path, "static/images/" + produkt.zdjecie_3))
        except Exception as e:
              print(e)

        db.session.delete(produkt)
        db.session.commit()
        flash(f'Produkt ({produkt.nazwa}) zosta?? usuni??ty', 'success')
        return redirect(url_for('admin'))
    flash(f'Produkt ({produkt.nazwa}) nie mo??e zosta?? usuni??ty')

    return redirect(url_for('admin'))