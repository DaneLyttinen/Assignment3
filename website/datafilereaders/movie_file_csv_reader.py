import csv
import os
import urllib.parse

import requests

from website.domainmodel.model import Movie, Actor, Genre, Director


class MovieFileCSVReader:
    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__dataset_of_movies = set()
        self.__dataset_of_actors = set()
        self.__dataset_of_directors = set()
        self.__dataset_of_genres = set()

    def read_csv_file(self):
        with open(os.path.join(self.__file_name, 'Data1000Movies.csv'), mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)

            index = 0
            for row in movie_file_reader:
                title = row['Title']
                release_year = int(row['Year'])
                movie = Movie(title, release_year)
                url = imdb_from_title(title, release_year)
                movie.image = str(url)
                if movie not in self.__dataset_of_movies:
                    self.__dataset_of_movies.add(movie)
                actors = row['Actors'].split(",")
                for actor in actors:
                    a_actor = Actor(actor)
                    movie.add_actor(a_actor)
                    if a_actor not in self.__dataset_of_actors:
                        self.__dataset_of_actors.add(a_actor)
                metascore = row['Metascore']
                movie.metascore = str(metascore)
                num_of_ratings = row['Votes']
                movie.num_of_ratings = float(num_of_ratings)
                director = row["Director"]
                director1 = Director(director)
                movie.director = director1
                description = row["Description"]
                movie.description = description
                rating = row["Rating"]

                runtime = row["Runtime (Minutes)"]

                movie.runtime_minutes = int(runtime)
                movie.rating = float(rating)
                if director1 not in self.__dataset_of_directors:
                    self.__dataset_of_directors.add(director1)
                genres = row["Genre"].split(",")
                for genre in genres:
                    a_genre = Genre(genre)
                    movie.add_genre(a_genre)
                    if a_genre not in self.__dataset_of_genres:
                        self.__dataset_of_genres.add(a_genre)
                index += 1

    @property
    def dataset_of_movies(self):
        return self.__dataset_of_movies

    @property
    def dataset_of_actors(self):
        return self.__dataset_of_actors

    @property
    def dataset_of_directors(self):
        return self.__dataset_of_directors

    @property
    def dataset_of_genres(self):
        return self.__dataset_of_genres


def imdb_from_title(title, year):
    pattern = 'https://api.themoviedb.org/3/search/movie?api_key=67cfd6550d69776df1bbefcd79c38b6e&language=en-US&'
    encoded_title = urllib.parse.quote(title)

    url = pattern.format(query=encoded_title, year=year)
    url = pattern + "query=" + encoded_title + "&year=" + str(year)
    r = requests.get(url)
    res = r.json()
    try:
        movie_id = res['results'][0]['poster_path']
        image_url = 'https://image.tmdb.org/t/p/w500' + str(movie_id)
        return image_url
    except:
        return "No image"


