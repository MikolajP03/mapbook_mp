import time
from geopy.geocoders import Nominatim
from catering_lib.interface import map_widget


class User:
    def __init__(self, imie: str, nazwisko: str, lokalizacja: str, firma_prac: str) -> None:
        self.imie = imie
        self.nazwisko = nazwisko
        self.lokalizacja = lokalizacja
        self.firma_prac = firma_prac
        self.coordinates = User.get_coordinates(self)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.imie,
                                            marker_color_circle="blue")

    def get_coordinates(self) -> list:
        geolocator = Nominatim(user_agent="CateringMap")
        location = geolocator.geocode(self.lokalizacja)
        time.sleep(1)
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
        time.sleep(1)
        return [location.latitude, location.longitude]


class Place:
    def __init__(self, lokal_firma: str, lokalizacja: str) -> None:
        self.lokal_firma = lokal_firma
        self.lokalizacja = lokalizacja
        self.coordinates = Place.get_coordinates(self)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.lokalizacja,
                                            marker_color_circle="yellow")

    def get_coordinates(self) -> list:
        geolocator = Nominatim(user_agent="CateringMap")
        location = geolocator.geocode(self.lokalizacja)
        time.sleep(1)
        return [location.latitude, location.longitude]


users_dataset: list = [User("A", "B", "Marywilska 44, 03-042 Warszawa", "C"),
                       User("Mikołaj", "Pochopień", "Krzyżówki 36, 03-193 Warszawa", "Masters Catering", )]
companies_dataset: list = [Company("Catering 66", "Sokołowska 22, 01-142 Warszawa"),
                           Company("Masters Catering", "Marszałkowska 82, 00-517 Warszawa"),
                           Company("Royal Catering", "Korkowa 47, 04-502 Warszawa")]
places_dataset: list = [Place("Catering 66", "Łazienkowska 3, 00-449 Warszawa"),
                        Place("Catering 66", "Światowida 17, 03-144 Warszawa"),
                        Place("Masters Catering", "Głębocka 15, 03-287 Warszawa")]
