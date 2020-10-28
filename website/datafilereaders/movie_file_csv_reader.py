import csv
import os
import urllib.parse

import requests

from website.domainmodel.model import Movie, Actor, Genre, Director, User


class MovieFileCSVReader:
    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__dataset_of_movies = set()
        self.__dataset_of_actors = set()
        self.__dataset_of_directors = set()
        self.__dataset_of_genres = set()
        self.__dataset_of_users = set()

    def movie_read_csv_file(self):
        with open(os.path.join(self.__file_name), mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)
            index = 0
            for row in movie_file_reader:
                title = row['Title']
                release_year = int(row['Year'])
                movie = Movie(title, release_year)
                # url = imdb_from_title(title, release_year)
                # movie.image = str(url)
                if movie not in self.__dataset_of_movies:
                    self.__dataset_of_movies.add(movie)
                actors = row['Actors'].split(",")
                for actor in actors:
                    a_actor = Actor(actor)
                    for s_actor in self.__dataset_of_actors:
                        if a_actor == s_actor:
                            movie.add_actor(s_actor)
                metascore = row['Metascore']
                movie.metascore = str(metascore)
                num_of_ratings = row['Votes']
                movie.num_of_ratings = float(num_of_ratings)
                director = row["Director"]
                director1 = Director(director)
                for directors in self.__dataset_of_directors:
                    if director1 == directors:
                        movie.director = directors
                description = row["Description"]
                movie.description = description
                rating = row["Rating"]

                runtime = row["Runtime (Minutes)"]

                movie.runtime_minutes = int(runtime)
                movie.rating = float(rating)
                genres = row["Genre"].split(",")
                for genre in genres:
                    a_genre = Genre(genre)
                    for sgenre in self.__dataset_of_genres:
                        if sgenre == a_genre:
                            movie.add_genre(sgenre)
                index += 1
    def read_csv_file(self):
        with open(os.path.join(self.__file_name), mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)
            index = 0
            for row in movie_file_reader:
                actors = row['Actors'].split(",")
                for actor in actors:
                    a_actor = Actor(actor)
                    if a_actor not in self.__dataset_of_actors:
                        self.__dataset_of_actors.add(a_actor)
                director = row["Director"]
                director1 = Director(director)
                if director1 not in self.__dataset_of_directors:
                    self.__dataset_of_directors.add(director1)
                genres = row["Genre"].split(",")
                for genre in genres:
                    a_genre = Genre(genre)
                    if a_genre not in self.__dataset_of_genres:
                        self.__dataset_of_genres.add(a_genre)
                index += 1
        self.movie_read_csv_file()

    def read_csv_file_users(self):
        with open(os.path.join(self.__file_name), mode='r', encoding='utf-8-sig') as csvfile:
            users_file_reader = csv.DictReader(csvfile)
            index = 0
            for row in users_file_reader:
                username = row['username']
                password = row['password']
                user = User(str(username),password)
                self.__dataset_of_users.add(user)
                index += 1

    def read_csv_file_reviews(self):
        with open(os.path.join(self.__file_name), mode='r', encoding='utf-8-sig') as csvfile:
            reviews_file_reader = csv.DictReader(csvfile)
            index = 0
            for row in reviews_file_reader:
                movie = str(row['movie'])
                review_text = str(row['review-text'])
                rating = int(row['rating'])
                user = int(row['author-id'])
                index += 1


    @property
    def dataset_of_movies(self):
        return self.__dataset_of_movies

    @property
    def dataset_of_users(self):
        return self.__dataset_of_users

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


