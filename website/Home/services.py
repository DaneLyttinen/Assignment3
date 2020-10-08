from typing import Iterable
import random

from website.directory.repository import AbstractRepository
from website.domainmodel.movie import Movie
from website.domainmodel.review import Review


class NonExistentArticleException(Exception):
    pass


class UnknownUserException(Exception):
    pass


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


def get_movie(repo: AbstractRepository, movie):
    movie = repo.get_movie_by_title(movie)
    return movie


def add_comment(movie: Movie, comment_text: str, username: str, repo: AbstractRepository):
    # Check that the article exists.
    movie = repo.get_movie(movie)
    if movie is None:
        raise NonExistentArticleException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create comment.
    comment = Review(movie, comment_text, 10)

    # Update the repository.
    repo.add_comment(comment)
