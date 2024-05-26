import json
import random
import matplotlib.pyplot as plt
import difflib


def read_data():
    """Reads  the movies database"""
    with open("movies_data.json", "r") as fileobj:
        return json.loads(fileobj.read())


MOVIES_DATABASE = read_data()


def sync_database():
    """Synchronizes the movies database"""
    updated_database = json.dumps(MOVIES_DATABASE)
    with open('movies_data.json', 'w') as fileobj:
        fileobj.write(updated_database)


def display_movies():
    """Displays the movies in the database"""
    print()
    print(f"\u001b[37m\u001b[43m{len(MOVIES_DATABASE)} movies in total\u001b[0m")
    for movie in MOVIES_DATABASE:
        print(f"\u001b[36m{movie['title']}: {movie['rating']}, released in {movie['year_of_release']}\u001b[0m")


def add_movie():
    """Adds a movie to the movies' database.
    Loads the information from the JSON file, adds the movie,
    and saves it.
    """
    """Adds new movies to the movies database"""
    add_title = input("\u001b[35mPlease enter a new movie: \u001b[0m")
    movie_exists = False
    while not movie_exists:
        for movie in MOVIES_DATABASE:
            if add_title.lower() == movie['title'].lower():
                movie_exists = True
                print(f"Movie {add_title} already exist!")
                add_title = input("\u001b[35mPlease enter a different movie name: \u001b[0m")
                break
        if not movie_exists:
            break
    while True:
        try:
            add_rating = float(input("\u001b[35mPlease enter a rating: \u001b[0m"))
            break
        except ValueError:
            print("\u001b[31mInvalid input. Please enter a valid float number for the rating.\u001b[0m")

    if 0 > add_rating or add_rating > 10:
        add_rating = float(input("\u001b[31m\u001b[1mPlease provide a number between 0.0 and 10.0: \u001b[0m"))

    while True:
        try:
            add_year = int(input("\u001b[35mPlease enter the year of release: \u001b[0m"))
            break
        except ValueError:
            print("\u001b[31m\u001b[1mInvalid input. Please enter a valid year.\u001b[0m")

    new_movie = {
        "title": add_title,
        "rating": add_rating,
        "year_of_release": add_year
    }
    MOVIES_DATABASE.append(new_movie)
    print(f"\u001b[36mMovie {add_title} successfully added")
    sync_database()
    display_movies()
    return MOVIES_DATABASE


def delete_movie():
    """Updates a movie from the movies' database.
    Loads the information from the JSON file, updates the movie,
    and saves it."""
    movie_to_be_deleted = input("\u001b[35mPlease select a movie to be deleted: \u001b[0m")
    movie_found = False
    for i in range(len(MOVIES_DATABASE)):
        if MOVIES_DATABASE[i]['title'] == movie_to_be_deleted:
            del MOVIES_DATABASE[i]
            print(f"\u001b[36mThe movie {movie_to_be_deleted} successfully deleted.\u001b[0m")
            movie_found = True
            break
    if not movie_found:
        print("\u001b[31m\u001b[1mError! The movie is not part of the database!\u001b[0m")
    sync_database()
    display_movies()


def update_movie():
    """Updates the movies database"""
    movie_to_be_updated= input("\u001b[35mPlease select a movie to be updated: \u001b[0m")
    movie_found = False
    for i in range(len(MOVIES_DATABASE)):
        if MOVIES_DATABASE[i]['title'] == movie_to_be_updated:
            MOVIES_DATABASE[i]['rating'] = float(input("\u001b[35mPlease insert a new rating: "))
            if 0 > MOVIES_DATABASE[i]['rating'] or MOVIES_DATABASE[i]['rating'] > 10:
                MOVIES_DATABASE[i]['rating'] = float(input("\u001b[31m\u001b[1mPlease provide a rating between 0 and 10: \u001b[0m"))
            print(f"\u001b[36mThe movie {movie_to_be_updated} successfully updated.")
            movie_found = True
            break
    if not movie_found:
        print("\u001b[31m\u001b[1mError! The movie you are trying to update is not part of the database!\u001b[0m")
    sync_database()
    display_movies()
    return MOVIES_DATABASE


def stats():
    ratings_sum = 0
    ratings_list = []
    for movie in MOVIES_DATABASE:
        ratings_sum += movie['rating']
        ratings_list.append(movie['rating'])
    average_rating = ratings_sum / len(MOVIES_DATABASE)
    print("\u001b[36mAverage rating: \u001b[0m", round(average_rating,2))

    ratings_list.sort()
    length_of_values_list = len(ratings_list)
    if length_of_values_list % 2 == 0:
        median_rating = (ratings_list[length_of_values_list // 2 - 1] + ratings_list[length_of_values_list // 2]) / 2
    else:
        median_rating = ratings_list[length_of_values_list // 2]
    print("\u001b[36mMedian rating: \u001b[0m", median_rating)

    best_movie = max(MOVIES_DATABASE, key=lambda x:x['rating'])
    print(f"\u001b[36mBest movie: {best_movie['title']}, {best_movie['rating']}, {best_movie['year_of_release']}")

    worst_movie = min(MOVIES_DATABASE, key=lambda x:x['rating'])
    print(f"\u001b[36mWorst movie: {worst_movie['title']}, {worst_movie['rating']}, {worst_movie['year_of_release']}")

    sync_database()

    return average_rating, median_rating, best_movie['title'], worst_movie['title']


def random_movie():
    random_movie = random.choice(MOVIES_DATABASE)
    print(f"\u001b[36mYour movie for tonight: \u001b[1m{random_movie['title']},\u001b[0m \u001b[36mit's rated \u001b[1m{random_movie['rating']}\u001b[0m")
    return random_movie


def search_movie():
    matches = []
    similarity_cutoff = 0.5
    search_key = input("\u001b[35mEnter part of movie name: ")
    for movie in MOVIES_DATABASE:
        ratio = difflib.SequenceMatcher(None, search_key, movie['title']).ratio()
        if ratio >= similarity_cutoff:
            matches.append((movie['title'], movie['rating']))
    if not matches:
        print("\u001b[31m\u001b[1mNo matches found.\u001b[0m")
    # print(matches)
    for movie, rating in matches:
        print(f"\u001b[36m{movie}, {rating}")
    return matches


def sort_by_rating():
    sorted_movies = sorted(MOVIES_DATABASE, key=lambda d: d['rating'], reverse=True)
    # print(sorted_movies)
    for movie in sorted_movies:
        print(f"\u001b[36m{movie['title']}: {movie['rating']}")
    return sorted_movies


def rating_histogram():
    ratings = []
    for movie in MOVIES_DATABASE:
        ratings.append(movie['rating'])
    # print(ratings)
    plt.figure(figsize=(10, 5))
    plt.hist(ratings, color='pink', width=0.4)
    plt.show()
    plt.savefig('Ratings_chart.png')


def movies_database():
    display_movies()
    add_movie()
    delete_movie()
    update_movie()
    stats()
    random_movie()
    search_movie()
    rating_histogram()
    sort_by_rating()


if __name__ == "__main__":
    movies_database()