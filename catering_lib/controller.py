from tkinter import *
import tkintermapview
from geopy.geocoders import Nominatim, ArcGIS
import time
from catering_lib.model import *
from catering_lib.interface import *

users: list = []
companies: list = []
places: list = []


def show_users() -> None:
    listbox_lista_obiektow.delete(0, END)
    for idx, user in enumerate(users):
        listbox_lista_obiektow.insert(idx, user.imie)
        time.sleep(1)


def show_companies() -> None:
    listbox_lista_firm.delete(0, END)
    for idx, company in enumerate(companies):
        listbox_lista_firm.insert(idx, company.nazwa_firmy)
        time.sleep(1)


def show_places() -> None:
    listbox_lista_lokali.delete(0, END)
    for idx, place in enumerate(places):
        listbox_lista_lokali.insert(idx, place.lokalizacja)
        time.sleep(1)


def add_user():
    name = entry_imie.get()
    surname = entry_nazwisko.get()
    company = entry_firma_prac.get()
    location = entry_location_prac.get()
    new_user = User(imie=name, nazwisko=surname, lokalizacja=location, firma_prac=company)
    users.append(new_user)

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_firma_prac.delete(0, END)
    entry_location_prac.delete(0, END)
    entry_imie.focus()
    show_users()


def add_company():
    name = entry_nazwa_firmy.get()
    location = entry_location_firma.get()
    new_company = Company(nazwa_firmy=name, lokalizacja=location)
    companies.append(new_company)

    entry_nazwa_firmy.delete(0, END)
    entry_location_firma.delete(0, END)
    entry_nazwa_firmy.focus()
    show_companies()


def add_place():
    name = entry_lokal_firma.get()
    location = entry_location_lokal.get()
    new_place = Place(lokal_firma=name, lokalizacja=location)
    places.append(new_place)

    entry_lokal_firma.delete(0, END)
    entry_location_lokal.delete(0, END)
    entry_lokal_firma.focus()
    show_places()


def remove_user():
    i = listbox_lista_obiektow.index(ACTIVE)
    users[i].marker.delete()
    users.pop(i)
    show_users()


def remove_company():
    i = listbox_lista_firm.index(ACTIVE)
    companies[i].marker.delete()
    companies.pop(i)
    show_companies()


def remove_place():
    i = listbox_lista_lokali.index(ACTIVE)
    places[i].marker.delete()
    places.pop(i)
    show_places()


def show_user_details():
    i = listbox_lista_obiektow.index(ACTIVE)
    imie = users[i].imie
    nazwisko = users[i].nazwisko
    lokalizacja = users[i].lokalizacja
    firma = users[i].firma_prac
    label_imie_szczegoly_obiektu_wartosc.config(text=imie)
    label_nazwisko_szczegoly_obiektu_wartosc.config(text=nazwisko)
    label_firma_prac_szczegoly_obiektu_wartosc.config(text=firma)
    label_lokalizacja_szczegoly_obiektu_wartosc.config(text=lokalizacja)
    map_widget.set_position(users[i].coordinates[0], users[i].coordinates[1])
    map_widget.set_zoom(12)


def show_company_details():
    i = listbox_lista_firm.index(ACTIVE)
    nazwa = companies[i].nazwa_firmy
    lokalizacja = companies[i].lokalizacja
    label_nazwa_firmy_szczegoly_wartosc.config(text=nazwa)
    label_lokalizacja_firmy_szczegoly_wartosc.config(text=lokalizacja)
    map_widget.set_position(companies[i].coordinates[0], companies[i].coordinates[1])
    map_widget.set_zoom(12)


def show_place_details():
    i = listbox_lista_lokali.index(ACTIVE)
    nazwa = places[i].lokal_firma
    lokalizacja = places[i].lokalizacja
    label_lokal_firma_szczegoly_wartosc.config(text=nazwa)
    label_lokalizacja_lokalu_szczegoly_wartosc.config(text=lokalizacja)
    map_widget.set_position(places[i].coordinates[0], places[i].coordinates[1])
    map_widget.set_zoom(12)


def edit_user():
    i = listbox_lista_obiektow.index(ACTIVE)
    imie = users[i].imie
    nazwisko = users[i].nazwisko
    firma_prac = users[i].firma_prac
    lokalizacja = users[i].lokalizacja

    entry_imie.insert(0, imie)
    entry_nazwisko.insert(0, nazwisko)
    entry_firma_prac.insert(0, firma_prac)
    entry_location_prac.insert(0, lokalizacja)
    button_dodaj_uzytkownika.config(text="Zapisz zmiany", command=lambda: update_user(i))


def edit_company():
    i = listbox_lista_firm.index(ACTIVE)
    nazwa_firmy = companies[i].nazwa_firmy
    lokalizacja = companies[i].lokalizacja

    entry_nazwa_firmy.insert(0, nazwa_firmy)
    entry_location_firma.insert(0, lokalizacja)
    button_dodaj_firme.config(text="Zapisz zmiany", command=lambda: update_company(i))


def edit_place():
    i = listbox_lista_lokali.index(ACTIVE)
    lokal_firma = places[i].lokal_firma
    lokalizacja = places[i].lokalizacja

    entry_lokal_firma.insert(0, lokal_firma)
    entry_location_lokal.insert(0, lokalizacja)
    button_dodaj_lokal.config(text="Zapisz zmiany", command=lambda: update_place(i))


def update_user(i):
    users[i].imie = entry_imie.get()
    users[i].nazwisko = entry_nazwisko.get()
    users[i].firma_prac = entry_firma_prac.get()
    users[i].lokalizacja = entry_location_prac.get()
    users[i].coordinates = User.get_coordinates(users[i])
    users[i].marker.delete()
    users[i].marker = map_widget.set_marker(users[i].coordinates[0], users[i].coordinates[1], text=users[i].imie,
                                            marker_color_circle="blue")

    button_dodaj_uzytkownika.config(text="Zapisz zmiany", command=add_user)
    show_users()
    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_location_prac.delete(0, END)
    entry_imie.focus()
    show_users()


def update_company(i):
    companies[i].nazwa_firmy = entry_nazwa_firmy.get()
    companies[i].lokalizacja = entry_location_firma.get()
    companies[i].coordinates = Company.get_coordinates(companies[i])
    companies[i].marker.delete()
    companies[i].marker = map_widget.set_marker(companies[i].coordinates[0], companies[i].coordinates[1],
                                                text=companies[i].nazwa_firmy,
                                                marker_color_circle="green")

    button_dodaj_firme.config(text="Zapisz zmiany", command=add_company)
    show_companies()
    entry_nazwa_firmy.delete(0, END)
    entry_location_firma.delete(0, END)
    entry_nazwa_firmy.focus()
    show_companies()


def update_place(i):
    places[i].lokal_firma = entry_lokal_firma.get()
    places[i].lokalizacja = entry_location_lokal.get()
    places[i].coordinates = Place.get_coordinates(places[i])
    places[i].marker.delete()
    places[i].marker = map_widget.set_marker(places[i].coordinates[0], places[i].coordinates[1],
                                             text=places[i].lokalizacja,
                                             marker_color_circle="yellow")

    button_dodaj_lokal.config(text="Zapisz zmiany", command=add_place)
    show_places()
    entry_lokal_firma.delete(0, END)
    entry_location_lokal.delete(0, END)
    entry_lokal_firma.focus()
    show_places()


def filter_users():
    listbox_lista_obiektow.delete(0, END)
    for idx, user in enumerate(users):
        user.marker.delete()
        if user.firma_prac == entry_filter_users.get():
            listbox_lista_obiektow.insert(idx, user.imie)
            user.marker = map_widget.set_marker(user.coordinates[0], user.coordinates[1],
                                                text=user.imie, marker_color_circle="blue")


def filter_places():
    listbox_lista_lokali.delete(0, END)
    for idx, place in enumerate(places):
        place.marker.delete()
        if place.lokal_firma == entry_filter_places.get():
            listbox_lista_lokali.insert(idx, place.lokalizacja)
            place.marker = map_widget.set_marker(place.coordinates[0], place.coordinates[1],
                                                 text=place.lokalizacja, marker_color_circle="yellow")


def unfilter_users():
    listbox_lista_obiektow.delete(0, END)
    for idx, user in enumerate(users):
        listbox_lista_obiektow.insert(idx, user.imie)
        user.marker = map_widget.set_marker(user.coordinates[0], user.coordinates[1],
                                            text=user.imie, marker_color_circle="blue")
        time.sleep(1)


def unfilter_places():
    listbox_lista_lokali.delete(0, END)
    for idx, place in enumerate(places):
        listbox_lista_lokali.insert(idx, place.lokalizacja)
        place.marker = map_widget.set_marker(place.coordinates[0], place.coordinates[1],
                                             text=place.lokalizacja, marker_color_circle="yellow")
        time.sleep(1)


def unfilter_companies():
    listbox_lista_firm.delete(0, END)
    for idx, company in enumerate(companies):
        listbox_lista_firm.insert(idx, company.nazwa_firmy)
        company.marker = map_widget.set_marker(company.coordinates[0], company.coordinates[1],
                                               text=company.nazwa_firmy, marker_color_circle="green")
        time.sleep(1)


# RAMKA LISTA PRACOWNIKÓW
label_lista_obiektow = Label(ramka_lista_obiektow, text="Lista pracowników: ")
listbox_lista_obiektow = Listbox(ramka_lista_obiektow)
button_szczegoly_obiektu = Button(ramka_lista_obiektow, text="Pokaż szczegóły ", command=show_user_details)
button_usun_obiekt = Button(ramka_lista_obiektow, text="Usuń pracownika", command=remove_user)
button_edytuj_obiekt = Button(ramka_lista_obiektow, text="Edytuj pracownika", command=edit_user)
entry_filter_users = Entry(ramka_lista_obiektow)
button_filter_users = Button(ramka_lista_obiektow, text="Filtruj pracowników", command=filter_users)
button_unfilter_users = Button(ramka_lista_obiektow, text="Usuń filtr", command=unfilter_users)

label_lista_obiektow.grid(row=0, column=0)
listbox_lista_obiektow.grid(row=1, column=0)
button_szczegoly_obiektu.grid(row=2, column=0)
button_usun_obiekt.grid(row=3, column=0)
button_edytuj_obiekt.grid(row=4, column=0)
entry_filter_users.grid(row=5, column=0)
button_filter_users.grid(row=6, column=0)
button_unfilter_users.grid(row=7, column=0)

# RAMKA LISTA FIRM
label_lista_firm = Label(ramka_lista_obiektow, text="Lista firm: ")
listbox_lista_firm = Listbox(ramka_lista_obiektow)
button_szczegoly_firmy = Button(ramka_lista_obiektow, text="Pokaż szczegóły ", command=show_company_details)
button_usun_firme = Button(ramka_lista_obiektow, text="Usuń firmę", command=remove_company)
button_edytuj_firme = Button(ramka_lista_obiektow, text="Edytuj firmę", command=edit_company)

label_lista_firm.grid(row=0, column=3)
listbox_lista_firm.grid(row=1, column=3)
button_szczegoly_firmy.grid(row=2, column=3)
button_usun_firme.grid(row=3, column=3)
button_edytuj_firme.grid(row=4, column=3)

# RAMKA LISTA LOKALI
label_lista_lokali = Label(ramka_lista_obiektow, text="Lista lokali: ")
listbox_lista_lokali = Listbox(ramka_lista_obiektow)
button_szczegoly_lokalu = Button(ramka_lista_obiektow, text="Pokaż szczegóły ", command=show_place_details)
button_usun_lokal = Button(ramka_lista_obiektow, text="Usuń lokal", command=remove_place)
button_edytuj_lokal = Button(ramka_lista_obiektow, text="Edytuj lokal", command=edit_place)
entry_filter_places = Entry(ramka_lista_obiektow)
button_filter_places = Button(ramka_lista_obiektow, text="Filtruj lokale", command=filter_places)
button_unfilter_places = Button(ramka_lista_obiektow, text="Usuń filtr", command=unfilter_places)

label_lista_lokali.grid(row=0, column=6)
listbox_lista_lokali.grid(row=1, column=6)
button_szczegoly_lokalu.grid(row=2, column=6)
button_usun_lokal.grid(row=3, column=6)
button_edytuj_lokal.grid(row=4, column=6)
entry_filter_places.grid(row=5, column=6)
button_filter_places.grid(row=6, column=6)
button_unfilter_places.grid(row=7, column=6)

# RAMKA FORMULARZ PRACOWNIKA
label_formularz_prac = Label(ramka_formularz, text="Dodaj pracownika:")
label_imie = Label(ramka_formularz, text="Imię:")
label_nazwisko = Label(ramka_formularz, text="Nazwisko:")
label_firma_prac = Label(ramka_formularz, text="Firma: ")
label_location_prac = Label(ramka_formularz, text="Lokalizacja:")
entry_imie = Entry(ramka_formularz)
entry_nazwisko = Entry(ramka_formularz)
entry_firma_prac = Entry(ramka_formularz)
entry_location_prac = Entry(ramka_formularz)
button_dodaj_uzytkownika = Button(ramka_formularz, text="Dodaj pracownika", command=add_user)

label_formularz_prac.grid(row=0, column=0, columnspan=2)
label_imie.grid(row=1, column=0, sticky=W)
label_nazwisko.grid(row=2, column=0, sticky=W)
label_firma_prac.grid(row=3, column=0, sticky=W)
label_location_prac.grid(row=4, column=0, sticky=W)
entry_imie.grid(row=1, column=1)
entry_nazwisko.grid(row=2, column=1)
entry_firma_prac.grid(row=3, column=1)
entry_location_prac.grid(row=4, column=1)
button_dodaj_uzytkownika.grid(row=5, column=0, columnspan=2)

# RAMKA FORMULARZ FIRMY
label_formularz_firma = Label(ramka_formularz, text="Dodaj firmę:")
label_nazwa_firmy = Label(ramka_formularz, text="Nazwa firmy:")
label_location_firma = Label(ramka_formularz, text="Lokalizacja:")
entry_nazwa_firmy = Entry(ramka_formularz)
entry_location_firma = Entry(ramka_formularz)
button_dodaj_firme = Button(ramka_formularz, text="Dodaj firmę", command=add_company)

label_formularz_firma.grid(row=0, column=2, columnspan=2)
label_nazwa_firmy.grid(row=1, column=2, sticky=W)
label_location_firma.grid(row=2, column=2, sticky=W)
entry_nazwa_firmy.grid(row=1, column=3)
entry_location_firma.grid(row=2, column=3)
button_dodaj_firme.grid(row=4, column=3, columnspan=2)

# RAMKA FORMULARZ LOKALU
label_formularz_lokal = Label(ramka_formularz, text="Dodaj lokal:")
label_lokal_firma = Label(ramka_formularz, text="Nazwa lokalu:")
label_location_lokal = Label(ramka_formularz, text="Lokalizacja:")
entry_lokal_firma = Entry(ramka_formularz)
entry_location_lokal = Entry(ramka_formularz)
button_dodaj_lokal = Button(ramka_formularz, text="Dodaj lokal", command=add_place)

label_formularz_lokal.grid(row=0, column=4, columnspan=2)
label_lokal_firma.grid(row=1, column=4, sticky=W)
label_location_lokal.grid(row=2, column=4, sticky=W)
entry_lokal_firma.grid(row=1, column=5)
entry_location_lokal.grid(row=2, column=5)
button_dodaj_lokal.grid(row=4, column=5, columnspan=2)

# RAMKA SZCZEGOLY PRACOWNIKA
label_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text="Szczegóły pracownika:")
label_imie_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text="Imię:")
label_nazwisko_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text="Nazwisko:")
label_firma_prac_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text="Firma:")
label_lokalizacja_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text="Lokalizacja:")

label_imie_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_nazwisko_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_firma_prac_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_lokalizacja_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektow, text="...")

label_szczegoly_obiektu.grid(row=0, column=0, sticky=W, columnspan=2)
label_imie_szczegoly_obiektu.grid(row=1, column=0, sticky=W)
label_imie_szczegoly_obiektu_wartosc.grid(row=1, column=1, sticky=W)
label_nazwisko_szczegoly_obiektu.grid(row=1, column=2, sticky=W)
label_nazwisko_szczegoly_obiektu_wartosc.grid(row=1, column=3, sticky=W)
label_firma_prac_szczegoly_obiektu.grid(row=1, column=4, sticky=W)
label_firma_prac_szczegoly_obiektu_wartosc.grid(row=1, column=5, sticky=W)
label_lokalizacja_szczegoly_obiektu.grid(row=1, column=6, sticky=W)
label_lokalizacja_szczegoly_obiektu_wartosc.grid(row=1, column=7, sticky=W)

# RAMKA SZCZEGOLY FIRMY
label_szczegoly_firmy = Label(ramka_szczegoly_obiektow, text="Szczegóły firmy:")
label_nazwa_szczegoly_firmy = Label(ramka_szczegoly_obiektow, text="Nazwa firmy:")
label_lokalizacja_firmy_szczegoly = Label(ramka_szczegoly_obiektow, text="Lokalizacja:")

label_nazwa_firmy_szczegoly_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_lokalizacja_firmy_szczegoly_wartosc = Label(ramka_szczegoly_obiektow, text="...")

label_szczegoly_firmy.grid(row=2, column=0, sticky=W, columnspan=2)
label_nazwa_szczegoly_firmy.grid(row=3, column=0, sticky=W)
label_nazwa_firmy_szczegoly_wartosc.grid(row=3, column=1, sticky=W)
label_lokalizacja_firmy_szczegoly.grid(row=3, column=2, sticky=W)
label_lokalizacja_firmy_szczegoly_wartosc.grid(row=3, column=3, sticky=W)

# RAMKA SZCZEGOLY LOKALU
label_szczegoly_lokalu = Label(ramka_szczegoly_obiektow, text="Szczegóły lokalu:")
label_lokal_firma_szczegoly = Label(ramka_szczegoly_obiektow, text="Nazwa firmy:")
label_lokalizacja_lokalu_szczegoly = Label(ramka_szczegoly_obiektow, text="Lokalizacja:")

label_lokal_firma_szczegoly_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_lokalizacja_lokalu_szczegoly_wartosc = Label(ramka_szczegoly_obiektow, text="...")

label_szczegoly_lokalu.grid(row=4, column=0, sticky=W, columnspan=2)
label_lokal_firma_szczegoly.grid(row=5, column=0, sticky=W)
label_lokal_firma_szczegoly_wartosc.grid(row=5, column=1, sticky=W)
label_lokalizacja_lokalu_szczegoly.grid(row=5, column=2, sticky=W)
label_lokalizacja_lokalu_szczegoly_wartosc.grid(row=5, column=3, sticky=W)

# RAMKA MAPA
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=600, corner_radius=4)
map_widget.set_zoom(6)
map_widget.set_position(52.2, 21)
map_widget.grid(row=0, column=0)

users.extend(users_dataset)
companies.extend(companies_dataset)
places.extend(places_dataset)

show_users()
show_companies()
show_places()
