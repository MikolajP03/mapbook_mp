from tkinter import *
import tkintermapview

root = Tk()
root.title("Catering_MP")
root.geometry("1920x1200")

subframe = Frame(root)
ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(subframe)
ramka_szczegoly_obiektow = Frame(subframe)
ramka_mapa = Frame(root)

ramka_lista_obiektow.grid(row=0, column=0, padx=50)
subframe.grid(row=0, column=1, padx=50)
ramka_formularz.grid(row=0, column=0, sticky=N)
ramka_szczegoly_obiektow.grid(row=1, column=0, sticky=N)
ramka_mapa.grid(row=2, column=0, columnspan=2)

map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=600, corner_radius=4)
map_widget.set_zoom(4)
map_widget.set_position(52.2, 21)
map_widget.grid(row=0, column=0)
