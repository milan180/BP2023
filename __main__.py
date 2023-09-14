from model import *
from model.relacije import *
from model.cache import region, api

#novi_gosti = Gosti(ime="Ivan", prezime="Ivic", broj_stola=5, status_narudzbe=True)
#novi_stolovi = Stolovi(broj_stola = 5, broj_sjedala = 9, lokacija = "dolje", status = True)
#nova_pica = Pica(naziv = "ness", Opis = "jako dobro pice", cijena = 5, kategorija ="bezalkoholno")
#nove_narudzbe = Narudzbe(ID_gosta = 5, vrijeme_narudzbe = "2023-05-06 12:00:00", status = "dostavljeno", ukupna_cijena = 2) 
#nove_stavke_narudzbe = Stavke_narudzbe(ID_narudzba = 5, ID_pica = 5, kolicina = 1)
#novi_konobari = Konobari(ime = "Mario", prezime = "Maric", broj_stola = 5)

#session.add(novi_gosti)
#session.add(novi_stolovi)
#session.add(nova_pica)
#session.add(nove_narudzbe)
#session.add(nove_stavke_narudzbe)
#session.add(novi_konobari)
#session.commit()

print("Podaci su uspješno dodani u bazu podataka.")


k = Konobari(first_name="Ante", last_name="Anic", broj_stola="12")
session.add(k)
session.commit()


ID = 5
KEY = f'konobari_{ID}'
k = region.get(KEY)
print(k)
if k is api.NO_VALUE:
    k = session.query(Konobari).filter(Konobari.id==ID).one()
    region.set(KEY, k)
print(k.ime + " " + k.prezime)