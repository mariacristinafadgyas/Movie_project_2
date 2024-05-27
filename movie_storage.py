import json
import random
import matplotlib.pyplot as plt
import difflib
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

REQUEST_URL = "http://www.omdbapi.com/?apikey=" + API_KEY + "&t="


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
    while True:
        try:
            title = input("\u001b[35mPlease enter a new movie: \u001b[0m")
            search_rq_url = REQUEST_URL + title
            movie_info = requests.get(search_rq_url)
            res_movie_info = movie_info.json()
            add_title = res_movie_info["Title"]

            movie_exists = False
            for movie in MOVIES_DATABASE:
                if add_title.lower() == movie['title'].lower():
                    movie_exists = True
                    print(f"Movie {add_title} already exist!")
                    break
            if not movie_exists:
                break
        except ConnectionError:
            print("\u001b[31m\u001b[1mPlease check your internet connection!\u001b[0m")
        except KeyError:
            print("\u001b[31m\u001b[1mPlease provide an actual film name!\u001b[0m")

    rating_str = res_movie_info["Ratings"][0]["Value"]
    add_rating = float(rating_str.split('/')[0])
    add_year = res_movie_info["Year"]
    add_poster = res_movie_info["Poster"]

    new_movie = {
        "title": add_title,
        "rating": add_rating,
        "year_of_release": add_year,
        "poster": add_poster
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


def serialize_movie(movie_obj):
    """Receives a movie object as parameter and returns a string containing
    the desired data for a single movie"""
    output = ''
    output += '<li>'
    output += '<div class="movie">'
    output += f'<img class="movie-poster" src={movie_obj["poster"]}/>'
    output += f'<div class="movie-title">{movie_obj["title"]}</div>'
    output += f'<div class="movie-year">{movie_obj["year_of_release"]}</div>'
    output += '</div>'
    output += '</li>'
    return output


def serialize_movies():
    """Receives a list of dictionaries containing movies data as parameter and returns
    a string containing the desired data for the whole list of movies"""
    output = ''
    for movie in MOVIES_DATABASE:
        output += serialize_movie(movie)
    return output


def generate_html_file(output):
    """Receives the output string of the previous function and the path of the HTML
    template as parameters and generates the HTML file"""
    with open("index_template.html", "r") as fileobj:
        template = fileobj.read()

    if "__TEMPLATE_TITLE__" in template:
        replaced_output = template.replace("__TEMPLATE_TITLE__", "My Favorite Movie App")

    if "__TEMPLATE_MOVIE_GRID__" in template:
        replaced_output = replaced_output.replace("__TEMPLATE_MOVIE_GRID__", output)

    with open("index.html", "w") as file_output:
        file_output.write(replaced_output)

    print("\u001b[36mWebsite was generated successfully.\u001b[0m")


def movies_database():
    display_movies()
    # add_movie()
    # delete_movie()
    # update_movie()
    # stats()
    # random_movie()
    # search_movie()
    # rating_histogram()
    # sort_by_rating()
    # serialize_movie()
    # output = serialize_movies()
    # generate_html_file(output)


if __name__ == "__main__":
    movies_database()


