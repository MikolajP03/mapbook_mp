from tkinter import *
import tkintermapview
from bs4 import BeautifulSoup
import requests
from geopy.geocoders import Nominatim
from catering_lib.model import *
# from mapbook_lib.controller import get_coordinates

users: list = []
companies: list = []


class User:
    def __init__(self, imie: str, nazwisko: str, lokalizacja: str) -> None:
        self.imie = imie
        self.nazwisko = nazwisko
        self.lokalizacja = lokalizacja
        self.coordinates = User.get_coordinates(self)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.imie,
                                            marker_color_circle="blue")

    def get_coordinates(self) -> list:
        geolocator = Nominatim(user_agent="CateringMap")
        location = geolocator.geocode(self.lokalizacja)
        return [location.latitude, location.longitude]


class Company:
    def __init__(self, nazwa_firmy: str, lokalizacja: str) -> None:
        self.nazwa_firmy = nazwa_firmy
        self.lokalizacja = lokalizacja
        self.coordinates = Company.get_coordinates(self)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.nazwa_firmy,
                                            marker_color_circle="green")

    def get_coordinates(self) -> list:
        geolocator = Nominatim(user_agent="CateringMap")
        location = geolocator.geocode(self.lokalizacja)
        return [location.latitude, location.longitude]


def show_users() -> None:
    listbox_lista_obiektow.delete(0, END)
    for idx, user in enumerate(users):
        listbox_lista_obiektow.insert(idx, user.imie)


def show_companies() -> None:
    listbox_lista_firm.delete(0, END)
    for idx, company in enumerate(companies):
        listbox_lista_firm.insert(idx, company.nazwa_firmy)


def add_user():
    name = entry_imie.get()
    surname = entry_nazwisko.get()
    location = entry_location_prac.get()
    new_user = User(imie=name, nazwisko=surname, lokalizacja=location)
    users.append(new_user)

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
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


def show_user_details():
    i = listbox_lista_obiektow.index(ACTIVE)
    imie = users[i].imie
    nazwisko = users[i].nazwisko
    lokalizacja = users[i].lokalizacja
    label_imie_szczegoly_obiektu_wartosc.config(text=imie)
    label_nazwisko_szczegoly_obiektu_wartosc.config(text=nazwisko)
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


def edit_user():
    i = listbox_lista_obiektow.index(ACTIVE)
    imie = users[i].imie
    nazwisko = users[i].nazwisko
    lokalizacja = users[i].lokalizacja

    entry_imie.insert(0, imie)
    entry_nazwisko.insert(0, nazwisko)
    entry_location_prac.insert(0, lokalizacja)
    button_dodaj_uzytkownika.config(text="Zapisz zmiany", command=lambda: update_user(i))


def edit_company():
    i = listbox_lista_firm.index(ACTIVE)
    nazwa_firmy = companies[i].nazwa_firmy
    lokalizacja = companies[i].lokalizacja

    entry_nazwa_firmy.insert(0, nazwa_firmy)
    entry_location_firma.insert(0, lokalizacja)
    button_dodaj_firme.config(text="Zapisz zmiany", command=lambda: update_company(i))


def update_user(i):
    users[i].imie = entry_imie.get()
    users[i].nazwisko = entry_nazwisko.get()
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


root = Tk()
root.title("Catering_MP")
root.geometry("1024x760")


# FRAME
ramka_lista_obiektow = Frame(root)
ramka_formularz_prac = Frame(root)
ramka_formularz_firma = Frame(root)
ramka_szczegoly_obiektow = Frame(root)
ramka_szczegoly_firmy = Frame(root)
ramka_mapa = Frame(root)

ramka_lista_obiektow.grid(row=0, column=0, padx=50)
ramka_formularz_prac.grid(row=0, column=1)
ramka_formularz_firma.grid(row=0, column=2)
ramka_szczegoly_obiektow.grid(row=1, column=0, columnspan=2, padx=50, pady=20)
# ramka_szczegoly_firmy.grid(row=2, column=0, columnspan=2, padx=50, pady=20)

ramka_mapa.grid(row=2, column=0, columnspan=2)

# RAMKA LISTA PRACOWNIKÓW
label_lista_obiektow = Label(ramka_lista_obiektow, text="Lista pracowników: ")
listbox_lista_obiektow = Listbox(ramka_lista_obiektow)
button_szczegoly_obiektu = Button(ramka_lista_obiektow, text="Pokaż szczegóły ", command=show_user_details)
button_usun_obiekt = Button(ramka_lista_obiektow, text="Usuń pracownika", command=remove_user)
button_edytuj_obiekt = Button(ramka_lista_obiektow, text="Edytuj pracownika", command=edit_user)

label_lista_obiektow.grid(row=0, column=0)
listbox_lista_obiektow.grid(row=1, column=0)
button_szczegoly_obiektu.grid(row=2, column=0)
button_usun_obiekt.grid(row=3, column=0)
button_edytuj_obiekt.grid(row=4, column=0)

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

# RAMKA FORMULARZ PRACOWNIKA
label_formularz_prac = Label(ramka_formularz_prac, text="Dodaj pracownika:")
label_imie = Label(ramka_formularz_prac, text="Imię:")
label_nazwisko = Label(ramka_formularz_prac, text="Nazwisko:")
label_location_prac = Label(ramka_formularz_prac, text="Lokalizacja:")
entry_imie = Entry(ramka_formularz_prac)
entry_nazwisko = Entry(ramka_formularz_prac)
entry_location_prac = Entry(ramka_formularz_prac)
button_dodaj_uzytkownika = Button(ramka_formularz_prac, text="Dodaj pracownika", command=add_user)

label_formularz_prac.grid(row=0, column=0, columnspan=2)
label_imie.grid(row=1, column=0, sticky=W)
label_nazwisko.grid(row=2, column=0, sticky=W)
label_location_prac.grid(row=3, column=0, sticky=W)
entry_imie.grid(row=1, column=1)
entry_nazwisko.grid(row=2, column=1)
entry_location_prac.grid(row=3, column=1)
button_dodaj_uzytkownika.grid(row=4, column=0, columnspan=2)

# RAMKA FORMULARZ FIRMY
label_formularz_firma = Label(ramka_formularz_prac, text="Dodaj firmę:")
label_nazwa_firmy = Label(ramka_formularz_prac, text="Nazwa firmy:")
label_location_firma = Label(ramka_formularz_prac, text="Lokalizacja:")
entry_nazwa_firmy = Entry(ramka_formularz_prac)
entry_location_firma = Entry(ramka_formularz_prac)
button_dodaj_firme = Button(ramka_formularz_prac, text="Dodaj firmę", command=add_company)

label_formularz_firma.grid(row=0, column=2, columnspan=2)
label_nazwa_firmy.grid(row=1, column=2, sticky=W)
label_location_firma.grid(row=2, column=2, sticky=W)
entry_nazwa_firmy.grid(row=1, column=3)
entry_location_firma.grid(row=2, column=3)
button_dodaj_firme.grid(row=4, column=3, columnspan=2)

# RAMKA SZCZEGOLY PRACOWNIKA
label_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text="Szczegóły pracownika:")
label_imie_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text="Imię:")
label_nazwisko_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text="Nazwisko:")
label_lokalizacja_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text="Lokalizacja:")

label_imie_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_nazwisko_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_lokalizacja_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektow, text="...")

label_szczegoly_obiektu.grid(row=0, column=0, sticky=W, columnspan=2)
label_imie_szczegoly_obiektu.grid(row=1, column=0, sticky=W)
label_imie_szczegoly_obiektu_wartosc.grid(row=1, column=1, sticky=W)
label_nazwisko_szczegoly_obiektu.grid(row=1, column=2, sticky=W)
label_nazwisko_szczegoly_obiektu_wartosc.grid(row=1, column=3, sticky=W)
label_lokalizacja_szczegoly_obiektu.grid(row=1, column=4, sticky=W)
label_lokalizacja_szczegoly_obiektu_wartosc.grid(row=1, column=5, sticky=W)

# RAMKA SZCZEGOLY FIRMY
label_szczegoly_firmy = Label(ramka_szczegoly_obiektow, text="Szczegóły firmy:")
label_nazwa_szczegoly_firmy = Label(ramka_szczegoly_obiektow, text="Nazwa:")
label_lokalizacja_firmy_szczegoly = Label(ramka_szczegoly_obiektow, text="Lokalizacja:")

label_nazwa_firmy_szczegoly_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_lokalizacja_firmy_szczegoly_wartosc = Label(ramka_szczegoly_obiektow, text="...")

label_szczegoly_firmy.grid(row=2, column=0, sticky=W, columnspan=2)
label_nazwa_szczegoly_firmy.grid(row=3, column=1, sticky=W)
label_nazwa_firmy_szczegoly_wartosc.grid(row=3, column=2, sticky=W)
label_lokalizacja_firmy_szczegoly.grid(row=3, column=3, sticky=W)
label_lokalizacja_firmy_szczegoly_wartosc.grid(row=3, column=4, sticky=W)

# RAMKA MAPA
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1024, height=600, corner_radius=4, )
map_widget.set_zoom(6)
map_widget.set_position(52.2, 21)
map_widget.grid(row=0, column=0)

root.mainloop()
