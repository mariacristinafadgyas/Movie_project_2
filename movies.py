import sys
from movie_storage import *


def display_welcome_message():
    print('''\u001b[32m ********** My Movies Database **********

    Menu:
    0. Exit
    1. List movies
    2. Add movie
    3. Delete movie
    4. Update movie
    5. Stats
    6. Random movie
    7. Search movie
    8. Movies sorted by rating
    9. Create Rating Histogram
    \u001b[0m''')


def show_options():
    user_choice = int(input("\u001b[35mEnter choice (0-9): \u001b[0m"))
    if user_choice == 0:
        print("Bye!")
        sys.exit()
    elif user_choice == 1:
        display_movies()
    elif user_choice == 2:
        add_movie()
    elif user_choice == 3:
        delete_movie()
    elif user_choice == 4:
        update_movie()
    elif user_choice == 5:
        stats()
    elif user_choice == 6:
        random_movie()
    elif user_choice == 7:
        search_movie()
    elif user_choice == 8:
        sort_by_rating()
    elif user_choice == 9:
        rating_histogram()
    else:
        print("\u001b[31m\u001b[1mPlease select a number between 1 and 9.\u001b[0m")

    print()
    input("\u001b[33mPress Enter to continue...")

    while True:
        print()
        search_again = input('\u001b[35mDo you want to select another option (Y/N)?\u001b[0m')
        if search_again == 'Y' or search_again == 'y':
            display_welcome_message()
            show_options()
        elif search_again == 'N' or search_again == 'n':
            sys.exit()
        else:
            print('\u001b[31m\u001b[1mSelect Y for Yes or, N for No\u001b[0m')


def main():
    display_welcome_message()
    show_options()


if __name__ == "__main__":
    main()