import random
import matplotlib.pyplot as plt
import difflib
import sys


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


def movies_library():
    movies = [{
        "title": "The Shawshank Redemption",
        "rating": 9.5,
        "year_of_release": 2000},
        {"title": "Pulp Fiction",
         "rating": 8.8,
         "year_of_release": 1990}
    ]
    return movies


def display_movies(movies):
    print()
    print(f"\u001b[37m\u001b[43m{len(movies)} movies in total\u001b[0m")
    for movie in movies:
        print(f"\u001b[36m{movie['title']}: {movie['rating']}, released in {movie['year_of_release']}\u001b[0m")


def add_movie(movies):
    add_title = input("\u001b[35mPlease enter a name: \u001b[0m")
    add_rating = float(input("\u001b[35mPlease enter a rating: \u001b[0m"))
    if 0 > add_rating or add_rating > 10:
        add_rating = float(input("\u001b[31m\u001b[1mPlease provide a number between 0.0 and 10.0: \u001b[0m"))
    add_year = int(input("\u001b[35mPlease enter the year of release: \u001b[0m"))
    new_movie = {
        "title": add_title,
        "rating": add_rating,
        "year_of_release": add_year
    }
    movies.append(new_movie)
    print(f"\u001b[36mMovie {add_title} successfully added")
    display_movies(movies)
    return movies


def delete_movie(movies):
    movie_to_be_deleted = input("\u001b[35mPlease select a movie to be deleted: \u001b[0m")
    movie_found = False
    for i in range(len(movies)):
        if movies[i]['title'] == movie_to_be_deleted:
            del movies[i]
            print(f"\u001b[36mThe movie {movie_to_be_deleted} successfully deleted.\u001b[0m")
            movie_found = True
            break
    if not movie_found:
        print("\u001b[31m\u001b[1mError! The movie is not part of the database!\u001b[0m")


def update_movie(movies):
    movie_to_be_updated= input("\u001b[35mPlease select a movie to be updated: \u001b[0m")
    movie_found = False
    for i in range(len(movies)):
        if movies[i]['title'] == movie_to_be_updated:
            movies[i]['rating'] = float(input("\u001b[35mPlease insert a new rating: "))
            if 0 > movies[i]['rating'] or movies[i]['rating'] > 10:
                movies[i]['rating'] = float(input("\u001b[31m\u001b[1mPlease provide a rating between 0 and 10: \u001b[0m"))
            print(f"\u001b[36mThe movie {movie_to_be_updated} successfully updated.")
            movie_found = True
            break
    if not movie_found:
        print("\u001b[31m\u001b[1mError! The movie you are trying to update is not part of the database!\u001b[0m")
    return movies


def stats(movies):
    ratings_sum = 0
    ratings_list = []
    for movie in movies:
        ratings_sum += movie['rating']
        ratings_list.append(movie['rating'])
    average_rating = ratings_sum / len(movies)
    print("\u001b[36mAverage rating: \u001b[0m", round(average_rating,2))

    ratings_list.sort()
    length_of_values_list = len(ratings_list)
    if length_of_values_list % 2 == 0:
        median_rating = (ratings_list[length_of_values_list // 2 - 1] + ratings_list[length_of_values_list // 2]) / 2
    else:
        median_rating = ratings_list[length_of_values_list // 2]
    print("\u001b[36mMedian rating: \u001b[0m", median_rating)


    best_movie = max(movies, key=lambda x:x['rating'])
    print(f"\u001b[36mBest movie: {best_movie['title']}, {best_movie['rating']}, {best_movie['year_of_release']}")

    worst_movie = min(movies, key=lambda x:x['rating'])
    print(f"\u001b[36mWorst movie: {worst_movie['title']}, {worst_movie['rating']}, {worst_movie['year_of_release']}")

    return average_rating, median_rating, best_movie['title'], worst_movie['title']


def random_movie(movies):
    random_movie = random.choice(movies)
    print(f"\u001b[36mYour movie for tonight: \u001b[1m{random_movie['title']},\u001b[0m \u001b[36mit's rated \u001b[1m{random_movie['rating']}\u001b[0m")
    return random_movie


def search_movie(movies):
    matches = []
    similarity_cutoff = 0.5
    search_key = input("\u001b[35mEnter part of movie name: ")
    for movie in movies:
        ratio = difflib.SequenceMatcher(None, search_key, movie['title']).ratio()
        if ratio >= similarity_cutoff:
            matches.append((movie['title'], movie['rating']))
    if not matches:
        print("\u001b[31m\u001b[1mNo matches found.\u001b[0m")
    # print(matches)
    for movie, rating in matches:
        print(f"\u001b[36m{movie}, {rating}")
    return matches


def sort_by_rating(movies):
    sorted_movies = sorted(movies, key=lambda d: d['rating'], reverse=True)
    # print(sorted_movies)
    for movie in sorted_movies:
        print(f"\u001b[36m{movie['title']}: {movie['rating']}")
    return sorted_movies


def rating_histogram(movies):
    ratings = []
    for movie in movies:
        ratings.append(movie['rating'])
    # print(ratings)
    plt.figure(figsize=(10, 5))
    plt.hist(ratings, color='pink', width=0.4)
    plt.show()
    plt.savefig('Ratings_chart.png')


def show_options(movies):
    user_choice = int(input("\u001b[35mEnter choice (0-9): \u001b[0m"))
    if user_choice == 0:
        print("Bye!")
        sys.exit()
    elif user_choice == 1:
        display_movies(movies)
    elif user_choice == 2:
        add_movie(movies)
    elif user_choice == 3:
        delete_movie(movies)
    elif user_choice == 4:
        update_movie(movies)
    elif user_choice == 5:
        stats(movies)
    elif user_choice == 6:
        random_movie(movies)
    elif user_choice == 7:
        search_movie(movies)
    elif user_choice == 8:
        sort_by_rating(movies)
    elif user_choice == 9:
        rating_histogram(movies)
    else:
        print("\u001b[31m\u001b[1mPlease select a number between 1 and 9.\u001b[0m")

    print()
    input("\u001b[33mPress Enter to continue...")

    while True:
        print()
        search_again = input('\u001b[35mDo you want to select another option (Y/N)?\u001b[0m')
        if search_again == 'Y' or search_again == 'y':
            display_welcome_message()
            show_options(movies)
        elif search_again == 'N' or search_again == 'n':
            exit()
        else:
            print('\u001b[31m\u001b[1mSelect Y for Yes or, N for No\u001b[0m')


def main():
    display_welcome_message()
    movies = movies_library()
    show_options(movies)


if __name__ == "__main__":
    main()