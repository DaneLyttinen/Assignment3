import csv
import os
import urllib.parse
from bisect import bisect_left
from datetime import date, datetime
from typing import List

import requests
from flask import request
from werkzeug.security import generate_password_hash

from website.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from website.directory.repository import AbstractRepository, RepositoryException
from website.domainmodel.model import Movie, User, Review, Actor, Director, Genre, make_review
from website.datafilereaders import movie_file_csv_reader


class MemoryRepository(AbstractRepository):
    # Articles ordered by date, not id. id is assumed unique.

    def __init__(self):
        self._movies = list()
        self._movies_index = dict()
        self._genre = list()
        self._users = list()
        self._reviews = list()
        self._actors = list()
        self._directors = list()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> str:
        return next((user for user in self._users if user.user_name == username), None)

    def add_movie(self, movie: Movie):
        if type(movie) is Movie and movie not in self._movies:
            self._movies.append(movie)

    def get_movies_by_director(self, director: str):
        movie_list = []
        director = director.lower()
        for movie in self._movies:
            if movie.director is not None:
                if director in movie.director.director_full_name.lower():
                    movie_list.append(movie)
        return movie_list

    def get_movies_by_actor(self, actor: str):
        movie_list = []
        actor = actor.lower()
        for movie in self._movies:
            for actors in movie.actors:
                if actor in actors.actor_full_name.lower():
                    movie_list.append(movie)
        return movie_list

    def get_movies_by_title(self, title: str):
        movie_list = []
        title = title.lower()
        for movie in self._movies:
            movie_title = str(movie.title)
            movie_titles = movie_title.lower()
            if title in movie_titles:
                movie_list.append(movie)
        return movie_list

    def get_movie(self, id: Movie) -> Movie:
        movie = None

        try:
            for i in self._movies:
                if i == id:
                    movie = i;
        except KeyError:
            pass  # Ignore exception and return None.

        return movie

    def get_number_of_movies(self):
        return len(self._movies)

    def sort_movies_by_release(self):
        self._movies.sort(key=lambda x: x.release, reverse=True)

    def get_first_movie(self):
        movie = None
        if len(self._movies) > 0:
            movie = self._movies[0]
        return movie

    def get_last_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[len(self._movies) - 1]
        return movie

    def get_movie_by_title(self, title):
        for movie in self._movies:
            if movie.title == title:
                return movie

    def get_review_for_movie(self, movie: Movie):
        list_of_reviews = []
        for review in self._reviews:
            if movie == review.movie:
                list_of_reviews.append(review)
        return list_of_reviews

    def add_review(self, comment: Review):
        super().add_review(comment)
        self._reviews.append(comment)

    def get_reviews(self):
        return self._reviews

    def get_10_movies(self):
        a_list = []
        count = 0
        a_sort = sorted(self._movies, key=lambda x: x.rating, reverse=True)
        for i in a_sort:
            if count < 10:
                a_list.append(i)
            else:
                break
            count += 1
        return a_list

    def get_genres(self):
        return self._genre

    def add_genre(self, genre):
        if type(genre) is Genre and genre not in self._genre:
            self._genre.append(genre)

    def get_actors(self):
        return self._actors

    def add_actors(self, actor):
        if type(actor) is Actor and actor not in self._actors:
            self._actors.append(actor)

    def get_director(self):
        return self._directors

    def add_director(self, director):
        if type(director) is Director and director not in self._directors:
            self._directors.append(director)
        else:
            pass

    def get_10_movies_genre(self, genre):
        if type(genre) is not Genre:
            return
        a_list = []
        count = 0
        for movie in self._movies:
            if genre in movie.genres:
                a_list.append(movie)
            if genre == Genre("Western") and len(a_list) == 5:
                break
            if genre == Genre("Musical") and len(a_list) == 5:
                break
            if len(a_list) == 10:
                break
        return a_list

    def get_all_movies_genre(self, genre):
        if type(genre) is not Genre:
            return
        a_list = []
        count = 0
        for movie in self._movies:
            if genre in movie.genres:
                a_list.append(movie)
        return a_list


def load_movies(data_path: str, repo: MemoryRepository):
    tags = dict()
    movie_file_reader = MovieFileCSVReader(data_path)
    movie_file_reader.read_csv_file()
    for data_row in movie_file_reader.dataset_of_movies:
        repo.add_movie(data_row)


def load_genres(data_path: str, repo: MemoryRepository):
    movie_file_reader = MovieFileCSVReader(data_path)
    movie_file_reader.read_csv_file()
    for genre in movie_file_reader.dataset_of_genres:
        repo.add_genre(genre)


def load_actors(data_path: str, repo: MemoryRepository):
    movie_file_reader = MovieFileCSVReader(data_path)
    movie_file_reader.read_csv_file()
    for act in movie_file_reader.dataset_of_actors:
        repo.add_actors(act)


def load_directors(data_path: str, repo: MemoryRepository):
    movie_file_reader = MovieFileCSVReader(data_path)
    movie_file_reader.read_csv_file()
    for dict in movie_file_reader.dataset_of_directors:
        repo.add_director(dict)


def populate(data_path: str, repo: MemoryRepository):
    # Load articles and tags into the repository.
    load_movies(data_path, repo)

    load_genres(data_path, repo)

    load_actors(data_path, repo)

    load_directors(data_path, repo)


def imdb_from_title(title, year):
    pattern = 'https://api.themoviedb.org/3/search/movie?api_key=67cfd6550d69776df1bbefcd79c38b6e&language=en-US&'
    encoded_title = urllib.parse.quote(title)

    url = pattern.format(query=encoded_title, year=year)
    url = pattern + "query=" + encoded_title + "&year=" + str(year)
    r = requests.get(url)
    res = r.json()
    movie_id = res['results'][0]['poster_path']
    print(movie_id)
    image_url = 'https://image.tmdb.org/t/p/w500'+str(movie_id)
    return image_url
