from website.directory.repository import AbstractRepository
from website.domainmodel.model import Movie, Review, User

class NonExistentActorException(Exception):
    pass

class NonExistentDirectorException(Exception):
    pass

class NonExistentGenreException(Exception):
    pass

class NonExistentMovieException(Exception):
    pass

def get_movies_by_title(repo: AbstractRepository, title):
    if title is None:
        raise NonExistentMovieException
    movies = repo.get_movies_by_title(title)
    return movies


def get_movies_by_director(repo: AbstractRepository, title):
    if title is None:
        raise NonExistentDirectorException
    movies = repo.get_movies_by_director(title)

    return movies


def get_movies_by_actor(repo: AbstractRepository, title):
    if title is None:
        raise NonExistentActorException
    movies = repo.get_movies_by_actor(title)
    return movies

def get_all_movies_genre(repo: AbstractRepository, genre):
    if genre is None:
        raise NonExistentGenreException
    movies = repo.get_all_movies_genre(genre)
    return movies
