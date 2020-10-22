from datetime import date, datetime

from website.domainmodel.model import User, Movie, Actor, Director, Review, Genre, make_review

import pytest


@pytest.fixture()
def movie():
    return Movie("Guardians of the Galaxy", 2014
    )


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


@pytest.fixture()
def review():
    movie = Movie("Guardians of the Galaxy", 2014
    )
    return Review(movie, "Terrible movie", 1)


def test_user_construction(user):
    assert user.user_name == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie 1234567890>'

    for comment in user.reviews:
        # User should have an empty list of Comments after construction.
        assert False


def test_movie_construction(movie):
    assert movie.title == "Guardians of the Galaxy"
    assert movie.release == 2014

    assert movie.reviews == []
    assert movie.actors == []
    assert movie.director == None
    assert movie.reviews == []
    assert movie.genres == []



    assert repr(
        movie) == '<Movie Guardians of the Galaxy, 2014>'


def test_movie_less_than_operator():
    movie_1 = Movie(
        "Guardians of the Galaxy", 2014
    )

    movie_2 = Movie(
        "Prometheus", 2012
    )

    assert movie_1 < movie_2


def test_review_construction(review):

    assert review.movie.__str__() == '<Movie Guardians of the Galaxy, 2014>'
    assert review.review_text == "Terrible movie"
    assert review.rating == 1


def test_make_review_establishes_relationships(movie, user):
    review_text = 'Best movie ever!'
    review = make_review(review_text, user, movie,10,datetime.today())

    # Check that the User object knows about the review.
    assert review in user.reviews

    # Check that the review knows about the User.
    assert review.user is user

    # Check that movie knows about the review.
    assert review in movie.reviews

    # Check that the review knows about the movie.
    assert review.movie is movie

    assert review in user.reviews


def test_make_review_multiple(movie, user):
    review_text = 'Best movie ever!'
    review = make_review(review_text, user, movie, 10)

    review_text = 'Actually nevermind!!'
    review = make_review(review_text, user, movie,0)
    assert len(movie.reviews) == 2