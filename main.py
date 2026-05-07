from mapbook_lib.model import users
from mapbook_lib.controller import read_users, add_user, remove_user, update_user, update_user_post, get_user_map


def main():
    while True:
        print("=====MENU=====")
        print("0 - zakończ program")
        print("1 - wyswietl listę znajomych")
        print("2 - dodaj znajomego")
        print("3 - usuń znajomego")
        print("4 - edytuj znajomego")
        print("5 - edytuj post")
        print("6 - wyświetl mapę")
        choice = input("Wybierz opcję menu")
        print(f"Wybrano opcję {choice}")
        if choice == "0":
            break
        if choice == "1":
            read_users(users)
        if choice == "2":
            add_user(users)
        if choice == "3":
            remove_user(users)
        if choice == "4":
            update_user(users)
        if choice == "5":
            update_user_post(users)
        if choice == "6":
            get_user_map(users)


if __name__ == "__main__":
    main()
