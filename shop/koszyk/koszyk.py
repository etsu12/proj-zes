from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos
from shop.produkty.models import dodajProdukt


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
        ilosc = request.form.get('ilosc')
        kolory = request.form.get('kolory')
        produkt = dodajProdukt.query.filter_by(id=produkt_id).first()
        if produkt_id and ilosc and kolory and request.method == "POST":
            SlownikPrzedmioty = {produkt_id:{'nazwa': produkt.nazwa, 'cena':produkt.cena, 'znizka':produkt.znizka, 'kolory':kolory, 'ilosc':ilosc, 'zdjecie':produkt.zdjecie_1}}

            if 'Koszyk' in session:
                print(session['Koszyk'])
                if produkt_id in session['Koszyk']:
                    print("Ten produkt już jest w twoim koszyku")
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