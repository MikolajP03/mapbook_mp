


map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=600, corner_radius=4)
map_widget.set_zoom(6)
map_widget.set_position(52.2, 21)
map_widget.grid(row=0, column=0)
users: list = [User("A", "B", "Marywilska 44, 03-042 Warszawa", "C")]