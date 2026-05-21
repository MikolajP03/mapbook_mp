from tkinter import *
import tkintermapview
from bs4 import BeautifulSoup
import requests
from mapbook_lib.controller import get_coordinates

users: list = []


class User:
    def __init__(self, imie: str, nazwisko: str, posty: int, lokalizacja: str) -> None:
        self.imie = imie
        self.nazwisko = nazwisko
        self.posty = posty
        self.lokalizacja = lokalizacja
        self.coordinates = User.get_coordinates(self)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.imie)

    def get_coordinates(self) -> list:
        url = f"https://pl.wikipedia.org/wiki/{self.lokalizacja}"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response_html = BeautifulSoup(response.text, "html.parser")
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        return [latitude, longitude]


def show_users() -> None:
    listbox_lista_obiektow.delete(0, END)
    for idx, user in enumerate(users):
        listbox_lista_obiektow.insert(idx, user.imie)


def add_user():
    name = entry_imie.get()
    surname = entry_nazwisko.get()
    posts = entry_liczba_postow.get()
    location = entry_location.get()
    # print(name, surname, posts, location)
    new_user = User(imie=name, nazwisko=surname, posty=int(posts), lokalizacja=location)
    users.append(new_user)
    # print(users)
    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_liczba_postow.delete(0, END)
    entry_location.delete(0, END)
    entry_imie.focus()
    show_users()


def remove_user():
    i = listbox_lista_obiektow.index(ACTIVE)
    users[i].marker.delete()
    users.pop(i)
    show_users()


def show_user_details():
    i = listbox_lista_obiektow.index(ACTIVE)
    imie = users[i].imie
    nazwisko = users[i].nazwisko
    posty = users[i].posty
    lokalizacja = users[i].lokalizacja
    label_imie_szczegoly_obiektu_wartosc.config(text=imie)
    label_nazwisko_szczegoly_obiektu_wartosc.config(text=nazwisko)
    label_liczba_postow_szczegoly_obiektu_wartosc.config(text=posty)
    label_lokalizacja_szczegoly_obiektu_wartosc.config(text=lokalizacja)
    map_widget.set_position(users[i].coordinates[0], users[i].coordinates[1])
    map_widget.set_zoom(12)


def edit_user():
    i = listbox_lista_obiektow.index(ACTIVE)
    imie = users[i].imie
    nazwisko = users[i].nazwisko
    posty = users[i].posty
    lokalizacja = users[i].lokalizacja

    entry_imie.insert(0, imie)
    entry_nazwisko.insert(0, nazwisko)
    entry_liczba_postow.insert(0, posty)
    entry_location.insert(0, lokalizacja)
    button_dodaj_uzytkownika.config(text="Zapisz zmiany", command=lambda: update_user(i))


def update_user(i):
    users[i].imie = entry_imie.get()
    users[i].nazwisko = entry_nazwisko.get()
    users[i].posty = entry_liczba_postow.get()
    users[i].lokalizacja = entry_location.get()
    users[i].coordinates = get_coordinates(users[i])
    users[i].marker.delete()
    users[i].marker = map_widget.set_marker(users[i].coordinates[0], users[i].coordinates[1], text=users[i].imie)

    button_dodaj_uzytkownika.config(text="Zapisz zmiany", command=add_user)
    show_users()
    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_liczba_postow.delete(0, END)
    entry_location.delete(0, END)
    entry_imie.focus()
    show_users()


root = Tk()
root.title("Mapbook_MP")
root.geometry("1024x760")

# FRAME
ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektow = Frame(root)
ramka_mapa = Frame(root)

ramka_lista_obiektow.grid(row=0, column=0, padx=50)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_obiektow.grid(row=1, column=0, columnspan=2, padx=50, pady=20)
ramka_mapa.grid(row=2, column=0, columnspan=2)

# RAMKA LISTA OBIEKTOW
label_lista_obiektow = Label(ramka_lista_obiektow, text="Lista znajomych: ")
listbox_lista_obiektow = Listbox(ramka_lista_obiektow)
button_szczegoly_obiektu = Button(ramka_lista_obiektow, text="Pokaż szczegóły ", command=show_user_details)
button_usun_obiekt = Button(ramka_lista_obiektow, text="Usuń obiekt", command=remove_user)
button_edytuj_obiekt = Button(ramka_lista_obiektow, text="Edytuj obiekt", command=edit_user)

label_lista_obiektow.grid(row=0, column=0)
listbox_lista_obiektow.grid(row=1, column=0)
button_szczegoly_obiektu.grid(row=2, column=0)
button_usun_obiekt.grid(row=2, column=1)
button_edytuj_obiekt.grid(row=2, column=2)

# RAMKA FORMULARZ
label_formularz = Label(ramka_formularz, text="Formularz:")
label_imie = Label(ramka_formularz, text="Imię:")
label_nazwisko = Label(ramka_formularz, text="Nazwisko:")
label_liczba_postow = Label(ramka_formularz, text="Liczba Postów:")
label_location = Label(ramka_formularz, text="Lokalizacja:")
entry_imie = Entry(ramka_formularz)
entry_nazwisko = Entry(ramka_formularz)
entry_liczba_postow = Entry(ramka_formularz)
entry_location = Entry(ramka_formularz)
button_dodaj_uzytkownika = Button(ramka_formularz, text="Dodaj użytkownika", command=add_user)

label_formularz.grid(row=0, column=0, columnspan=2)
label_imie.grid(row=1, column=0, sticky=W)
label_nazwisko.grid(row=2, column=0, sticky=W)
label_liczba_postow.grid(row=3, column=0, sticky=W)
label_location.grid(row=4, column=0, sticky=W)
entry_imie.grid(row=1, column=1)
entry_nazwisko.grid(row=2, column=1)
entry_liczba_postow.grid(row=3, column=1)
entry_location.grid(row=4, column=1)
button_dodaj_uzytkownika.grid(row=5, column=0, columnspan=2)

# RAMKA SZCZEGOLY OBIEKTU
label_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text="Szczegóły użytkownika:")
label_imie_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text="Imię:")
label_nazwisko_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text="Nazwisko:")
label_liczba_postow_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text="Liczba Postów:")
label_lokalizacja_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text="Lokalizacja:")

label_imie_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_nazwisko_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_liczba_postow_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_lokalizacja_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektow, text="...")

label_szczegoly_obiektu.grid(row=0, column=0, sticky=W, columnspan=2)
label_imie_szczegoly_obiektu.grid(row=1, column=0, sticky=W)
label_imie_szczegoly_obiektu_wartosc.grid(row=1, column=1, sticky=W)
label_nazwisko_szczegoly_obiektu.grid(row=1, column=2, sticky=W)
label_nazwisko_szczegoly_obiektu_wartosc.grid(row=1, column=3, sticky=W)
label_liczba_postow_szczegoly_obiektu.grid(row=1, column=4, sticky=W)
label_liczba_postow_szczegoly_obiektu_wartosc.grid(row=1, column=5, sticky=W)
label_lokalizacja_szczegoly_obiektu.grid(row=1, column=6, sticky=W)
label_lokalizacja_szczegoly_obiektu_wartosc.grid(row=1, column=7, sticky=W)

# RAMKA MAPA
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1024, height=600, corner_radius=4, )
map_widget.set_zoom(6)
map_widget.set_position(52.2, 21)
map_widget.grid(row=0, column=0)

root.mainloop()
