import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

REQUEST_URL = "http://www.omdbapi.com/?apikey=" + API_KEY + "&t="


def read_data():
    """Reads  the movies database"""
    with open("movies_data.json", "r") as fileobj:
        movies_database = json.loads(fileobj.read())
    return movies_database


def sync_database(movies_database):
    """Synchronizes the movies database"""
    updated_database = json.dumps(movies_database)
    with open('movies_data.json', 'w') as fileobj:
        fileobj.write(updated_database)


def add_movie(new_movie):
    """Adds a new movie to the movies' database.
    Loads the information from the JSON file, adds the movie,
    and synchronizes the database.
    """
    movies_database = read_data()
    movies_database.append(new_movie)

    sync_database(movies_database)
    return movies_database


def delete_movie(movie_to_be_deleted):
    """Deletes a movie from the movies' database.
    Loads the information from the JSON file, deletes the movie,
    and synchronizes the database."""
    movies_database = read_data()
    movie_found = False
    for i in range(len(movies_database)):
        if movies_database[i]['title'].lower() == movie_to_be_deleted.lower():
            del movies_database[i]
            print(
                f"\u001b[36mThe movie \u001b[38;5;160m{movie_to_be_deleted.capitalize()}\u001b[0m \u001b[36m "
                f"successfully deleted.\u001b[0m")
            movie_found = True
            break
    if not movie_found:
        print("\u001b[31m\u001b[1mError! The movie is not part of the database!\u001b[0m")
    sync_database(movies_database)
    return movies_database


def update_movie(movie_to_be_updated):
    """Updates the movies database"""
    movies_database = read_data()

    movie_found = False
    for i in range(len(movies_database)):
        if movies_database[i]['title'].lower() == movie_to_be_updated.lower():
            movies_database[i]['note'] = input("\u001b[38;5;49;1mPlease enter movie note 🙄: \u001b[0m")
            print(f"\u001b[38;5;181;1mThe movie \u001b[38;5;213;1m"
                  f"{movie_to_be_updated}\u001b[38;5;181;1m was successfully updated.\u001b[0m")
            movie_found = True
            break
    if not movie_found:
        print("\u001b[38;5;197;1mError! The movie you are trying to update is not part of the database!\u001b[0m")
    sync_database(movies_database)
    return movies_database
