from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos
from shop.produkty.models import dodajProdukt
from shop.produkty.routes import marki, kategorie


def MergeSlowniki(slownik1, slownik2):
    if isinstance(slownik1, list) and isinstance(slownik2, list):
        return slownik1 + slownik2
    elif isinstance(slownik1, dict) and isinstance(slownik2, dict):
        return dict(list(slownik1.items()) + list(slownik2.items()))
    return False

@app.route('/dodajkoszyk', methods=['POST'])
def DodajKoszyk():
    try:
        produkt_id = request.form.get('produkt_id')
        ilosc = int(request.form.get('ilosc'))
        kolory = request.form.get('kolory')
        produkt = dodajProdukt.query.filter_by(id=produkt_id).first()
        if produkt_id and ilosc and kolory and request.method == "POST":
            SlownikPrzedmioty = {produkt_id:{'nazwa': produkt.nazwa, 'cena':produkt.cena, 'znizka':produkt.znizka, 'kolor':kolory, 'ilosc':ilosc, 'zdjecie':produkt.zdjecie_1, 'kolory': produkt.kolory}}

            if 'Koszyk' in session:
                print(session['Koszyk'])
                if produkt_id in session['Koszyk']:
                    for key, item in session['Koszyk'].items():
                        if int(key) == int(produkt_id):
                            session.modified = True
                            item['ilosc'] += 1
                else:
                     session['Koszyk'] = MergeSlowniki( session['Koszyk'], SlownikPrzedmioty)
                     return redirect(request.referrer)
            else:
                session['Koszyk'] = SlownikPrzedmioty
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/koszyk')
def getKoszyk():
    if 'Koszyk' not in session or len(session['Koszyk']) <= 0:
        return redirect(url_for('home'))
    suma = 0
    lacznasuma = 0
    for key, produkt in session['Koszyk'].items():
        znizka = (produkt['znizka']/100) * float(produkt['cena']) * float(produkt['ilosc'])
        suma += float(produkt['cena']) * int(produkt['ilosc'])
        suma -= znizka
        podatek = ("%.2f" % (.06 * float(suma)))
        lacznasuma = float("%.2f" % (1.06 * suma))
    return render_template('produkty/koszyk.html', podatek = podatek, lacznasuma = lacznasuma, marki=marki(), kategorie=kategorie())

@app.route('/wyczysc')
def pusty_koszyk():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)

@app.route('/edytujkoszyk/<int:code>', methods=['POST'])
def edytujkoszyk(code):
    if 'Koszyk' not in session or len(session['Koszyk']) <= 0:
       return redirect(url_for('home'))
    if request.method == "POST":
        ilosc = request.form.get('ilosc')
        kolor = request.form.get('kolor')
        try:
            session.modified = True
            for key, item in session['Koszyk'].items():
                if int(key) == code:
                    item['ilosc'] = ilosc
                    item['kolor'] = kolor
                    flash('Przedmiot został zaktualizowany!')
                    return redirect(url_for('getKoszyk'))
        except Exception as e:
            print(e)
            return redirect(url_for('getKoszyk'))

@app.route('/usunprzedmiot/<int:id>')
def usunprzedmiot(id):
    if 'Koszyk' not in session or len(session['Koszyk']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Koszyk'].items():
            if int(key) == id:
                session['Koszyk'].pop(key, None)
                return redirect(url_for('getKoszyk'))
    except Exception as e:
        print(e)
        return redirect(url_for('getKoszyk'))

@app.route('/wyczysckoszyk')
def wyczysckoszyk():
    try:
        session.pop('Koszyk', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)