from typing import Iterable
import random

from website.directory.repository import AbstractRepository
from website.domainmodel.movie import Movie


def get_ten_movies(repo: AbstractRepository):
    movies = repo.get_10_movies()
    return movies


def get_genres(repo: AbstractRepository):
    genres = repo.get_genres()
    return genres


def get_10_movies_genre(repo: AbstractRepository, genre):
    movies = repo.get_10_movies_genre(genre)
    return movies

def get_all_movies_genre(repo: AbstractRepository, genre):
    movies = repo.get_all_movies_genre(genre)
    return movies