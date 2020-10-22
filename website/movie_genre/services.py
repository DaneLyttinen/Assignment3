from website.directory.repository import AbstractRepository
from website.domainmodel.model import Movie, Review, User


def get_movies_by_title(repo: AbstractRepository, title):
    movies = repo.get_movies_by_title(title)
    return movies


def get_movies_by_director(repo: AbstractRepository, title):
    movies = repo.get_movies_by_director(title)
    return movies


def get_movies_by_actor(repo: AbstractRepository, title):
    movies = repo.get_movies_by_actor(title)
    return movies

def get_all_movies_genre(repo: AbstractRepository, genre):
    movies = repo.get_all_movies_genre(genre)
    return movies