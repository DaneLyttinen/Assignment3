from datetime import date, datetime

import pytest

from website.directory.database_repository import SqlAlchemyRepository
from website.domainmodel.model import User, Genre, Movie, Director, Actor, Review, make_review
from website.directory.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_movies = repo.get_number_of_movies()

    # Check that the query returned 177 Articles.
    assert number_of_movies == 1000


def test_repository_can_add_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_movies = repo.get_number_of_movies()

    new_movies_id = number_of_movies + 1

    movie = Movie(
        "Best Movie Ever",
        2020,
    )
    movie.description = "amazing"
    movie.director = Director("wallah")
    movie.actors.append(Actor("fake"))
    movie.genres.append(Genre("Action"))
    movie.metascore = 80
    movie.runtime_minutes = 155
    movie.num_of_ratings = 550.5
    movie.rating = 9.4
    repo.add_movie(movie)

    assert repo.get_movie(movie) == movie


def test_repository_can_retrieve_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie_by_title("Interstellar")

    # Check that the Article has the expected title.
    assert movie.title == 'Interstellar'

    # Check that the Article is commented as expected.
    comment_one = [comment for comment in article.comments if comment.comment == 'Oh no, COVID-19 has hit New Zealand'][
        0]
    comment_two = [comment for comment in article.comments if comment.comment == 'Yeah Freddie, bad news'][0]

    assert comment_one.user.username == 'fmercury'
    assert comment_two.user.username == "thorke"

    # Check that the Article is tagged as expected.
    assert article.is_tagged_by(Tag('Health'))
    assert article.is_tagged_by(Tag('New Zealand'))


def test_repository_does_not_retrieve_a_non_existent_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie_by_title("Fake Movie")
    assert movie is None


def test_repository_can_retrieve_movies_by_actor(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_actor("Matt Damon")

    # Check that the query returned 3 Articles.
    assert len(movies) == 10

    movies = repo.get_movies_by_actor("Brad Pitt")

    # Check that the query returned 5 Articles.
    assert len(movies) == 13


def test_repository_can_retrieve_movies_by_director(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_director("Michael Bay")

    # Check that the query returned 3 Articles.
    assert len(movies) == 6

    movies = repo.get_movies_by_actor("Brad Pitt")

    # Check that the query returned 5 Articles.
    assert len(movies) == 13


def test_repository_can_retrieve_movies_by_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_all_movies_genre(Genre("Western"))

    # Check that the query returned 3 Articles.
    assert len(movies) == 7

    movies = repo.get_all_movies_genre(Genre("Action"))

    # Check that the query returned 5 Articles.
    assert len(movies) == 303
