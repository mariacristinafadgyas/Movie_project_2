import random
import matplotlib.pyplot as plt
import difflib
import os
from dotenv import load_dotenv
import movie_storage
import requests
import country_converter as coco

load_dotenv()
API_KEY = os.getenv('API_KEY')
PARTIAL_URL = os.getenv('PARTIAL_URL')

REQUEST_URL = PARTIAL_URL + API_KEY + "&t="


def display_movies():
    """Displays the movies in the database"""
    movies_database = movie_storage.read_data()
    print()
    print(f"\u001b[38;5;208;1m{len(movies_database)} movies in total\u001b[0m")
    for movie in movies_database:
        print(f"\u001b[38;5;38;1m{movie['title']}: \u001b[38;5;160;1m{movie['rating']}\u001b[0m, released in \u001b["
              f"38;5;28;1m{movie['year_of_release']}\u001b[0m")


def add_movie():
    """Adds a movie to the movies structure"""
    movies_database = movie_storage.read_data()
    while True:
        try:
            title = input("\u001b[35mPlease enter a new movie: \u001b[0m")
            search_rq_url = REQUEST_URL + title
            movie_info = requests.get(search_rq_url)
            res_movie_info = movie_info.json()
            add_title = res_movie_info["Title"]

            movie_exists = False
            for movie in movies_database:
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
    add_movie_imdb_id = res_movie_info["imdbID"]
    add_country = res_movie_info["Country"]

    new_movie = {
        "title": add_title,
        "rating": add_rating,
        "year_of_release": add_year,
        "poster": add_poster,
        "note": "",
        "imdbID": add_movie_imdb_id,
        "country": add_country
    }
    movie_storage.add_movie(new_movie)
    print(f"\u001b[36mMovie {add_title} successfully added")
    print()
    display_movies()


def delete_movie():
    """Deletes a movie from the movies structure"""
    movie_to_be_deleted = input("\u001b[35mPlease select a movie to be deleted: \u001b[0m")

    movie_storage.delete_movie(movie_to_be_deleted)
    display_movies()


def update_movie():
    """Updates the movies structure"""
    movie_to_be_updated = input("\u001b[35mPlease select a movie to be updated: \u001b[0m")

    movie_storage.update_movie(movie_to_be_updated)
    display_movies()


def stats():
    """Displays the movies statistics"""
    movies_database = movie_storage.read_data()
    ratings_sum = 0
    ratings_list = []
    for movie in movies_database:
        ratings_sum += movie['rating']
        ratings_list.append(movie['rating'])
    average_rating = ratings_sum / len(movies_database)
    print("\u001b[38;5;129;1mAverage rating: \u001b[0m", round(average_rating, 2))

    ratings_list.sort()
    length_of_values_list = len(ratings_list)
    if length_of_values_list % 2 == 0:
        median_rating = (ratings_list[length_of_values_list // 2 - 1] + ratings_list[length_of_values_list // 2]) / 2
    else:
        median_rating = ratings_list[length_of_values_list // 2]
    print("\u001b[38;5;129;1mMedian rating: \u001b[0m", median_rating)

    best_movie = max(movies_database, key=lambda x: x['rating'])
    print(f"\u001b[38;5;220;1mBest movie: \u001b[36m{best_movie['title']}, {best_movie['rating']}, "
          f"{best_movie['year_of_release']}\u001b[0m")

    worst_movie = min(movies_database, key=lambda x: x['rating'])
    print(f"\u001b[38;5;220;1mWorst movie: \u001b[36m{worst_movie['title']}, {worst_movie['rating']}, "
          f"{worst_movie['year_of_release']}\u001b[0m")

    return average_rating, median_rating, best_movie['title'], worst_movie['title']


def random_movie():
    """Displays a random movie to the screen"""
    movies_database = movie_storage.read_data()
    sel_random_movie = random.choice(movies_database)
    print(f"\u001b[36mYour movie for tonight: \u001b[38;5;202;1m{sel_random_movie['title']},"
          f"\u001b[0m \u001b[36mit's rated \u001b[38;5;220;1m{sel_random_movie['rating']}\u001b[0m")
    return random_movie


def search_movie():
    """Searches a movie using fuzzy search"""
    movies_database = movie_storage.read_data()
    matches = []
    similarity_cutoff = 0.5
    search_key = input("\u001b[35mEnter part of movie name: ")
    for movie in movies_database:
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
    """Sorts the movies by rating"""
    movies_database = movie_storage.read_data()
    sorted_movies = sorted(movies_database, key=lambda d: d['rating'], reverse=True)
    for movie in sorted_movies:
        print(f"\u001b[36m{movie['title']}: \u001b[38;5;220;1m{movie['rating']}\u001b[0m")
    return sorted_movies


def rating_histogram():
    """Saves to file the movies histogram"""
    movies_database = movie_storage.read_data()
    ratings = []
    for movie in movies_database:
        ratings.append(movie['rating'])
    plt.figure(figsize=(10, 5))
    plt.hist(ratings, color='pink', width=0.4)
    plt.show()
    plt.savefig('Ratings_chart.png')


def get_country_flag(movie_country):
    """Retrieves country codes"""
    if "," in movie_country:
        first_country = movie_country.split(',')[0].strip()
    else:
        first_country = movie_country.strip()

    iso2_country_code = coco.convert(names=first_country, to='ISO2')  # Conversion to ISO2 code

    return iso2_country_code


def serialize_movie(movie_obj):
    """Receives a movie object as parameter and returns a string containing
    the desired data for a single movie"""
    output = ''
    output += '<li>'
    output += '<div class="movie">'
    output += (f'<a href="https://www.imdb.com/title/{movie_obj["imdbID"]}/">'
               f'<img class="movie-poster" src={movie_obj["poster"]}/></a>')
    output += f'<div class="movie-title">{movie_obj["title"]}</div>'
    output += f'<div class="movie-year">{movie_obj["year_of_release"]}</div>'
    output += f'<div class="movie-rating">Rating: {movie_obj["rating"]}</div>'
    # output += f'<img  class="movie-country" src="https://flagsapi.com/DE/shiny/32.png" >'
    output += (f'<img class="movie-country" src="https://flagsapi.com/'
               f'{get_country_flag(movie_obj["country"])}/shiny/32.png" >')
    output += f'<div class="movie-note">{movie_obj["note"]}</div>'
    output += '</div>'
    output += '</li>'
    return output


def serialize_movies():
    """Receives a list of dictionaries containing movies data as parameter and returns
    a string containing the desired data for the whole list of movies"""
    movies_database = movie_storage.read_data()
    output = ''
    for movie in movies_database:
        output += serialize_movie(movie)
    return output


def generate_html_file(output):
    """Receives the output string of the previous function and the path of the HTML
    template as parameters and generates the HTML file"""
    replaced_output = ""
    with open("index_template.html", "r") as fileobj:
        template = fileobj.read()

    if "__TEMPLATE_TITLE__" in template:
        replaced_output = template.replace("__TEMPLATE_TITLE__", "My Favorite Movie App")

    if "__TEMPLATE_MOVIE_GRID__" in template:
        replaced_output = replaced_output.replace("__TEMPLATE_MOVIE_GRID__", output)

    with open("index.html", "w") as file_output:
        file_output.write(replaced_output)

    print("\u001b[36mWebsite was generated successfully.\u001b[0m")
