from catering_lib.controller import *

users.extend(users_dataset)
companies.extend(companies_dataset)
places.extend(places_dataset)

show_users()
show_companies()
show_places()

root.mainloop()
