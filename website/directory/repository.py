import abc
from typing import List
from datetime import date, datetime

from website.domainmodel.model import User, Review, Movie, Genre

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_10_movies(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_title(self, title) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_director(self, title: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_actor(self, title: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_10_movies_genre(self, genre) -> Genre:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_movies_genre(self, genre) -> Genre:
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_title(self, title) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_review_for_movie(self, movie) -> Movie:
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds an Article to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, id: Movie) -> Movie:
        """ Returns Article with id from the repository.

        If there is no Article with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Comment to the repository.

        If the Comment doesn't have bidirectional links with an Article and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Comment not correctly attached to a User')
        if review.movie is None or review not in review.movie.reviews:
            raise RepositoryException('Comment not correctly attached to an Article')

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Comments stored in the repository. """
        raise NotImplementedError
