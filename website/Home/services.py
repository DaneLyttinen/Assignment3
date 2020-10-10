from typing import Iterable
import random

from website.directory.repository import AbstractRepository
from website.domainmodel.model import Movie, Review, User


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


def add_review(movie: Movie, comment_text: str, rating: int, username: str, repo: AbstractRepository):
    # Check that the article exists.
    movie = repo.get_movie(movie)
    if movie is None:
        raise NonExistentArticleException

    user = repo.get_user(username)
    print("current user",user)
    if user is None:
        raise UnknownUserException

    # Create comment.
    comment = Review(movie, comment_text, rating)
    comment.user = user
    user.add_review(comment)
    movie.add_review(comment)
    print("all reviews", user.reviews)

    # Update the repository.
    repo.add_review(comment)
