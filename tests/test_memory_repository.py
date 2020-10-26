import os
from datetime import date, datetime
from typing import List

import pytest

from website.directory import memory_repository
from website.directory.repository import AbstractRepository, RepositoryException
from website.domainmodel.model import Movie, User, Review, Actor, Director, Genre, make_review, ReviewException

from website.datafilereaders import movie_file_csv_reader
from website.directory import memory_repository

x = memory_repository.MemoryRepository()
data_path = os.path.join('website', 'datafilereaders', 'datafiles')
memory_repository.load_movies(data_path, x)


def test_repository_can_load_movies():
    data_path = os.path.join('website', 'datafilereaders', 'datafiles')
    x = memory_repository.MemoryRepository()
    memory_repository.load_movies(data_path, x)


def test_repository_can_add_a_user():
    x = memory_repository.MemoryRepository()
    user = User('dave', '123456789')
    x.add_user(user)

    assert x.get_user('dave') is user


def test_repository_can_get_review_of_movie():
    a_movie = Movie("Guardians of the Galaxy", 2014)
    movie = x.get_movie(a_movie)
    review_text = "not good"
    rating = 2
    user = User("daneln", "Dane1337")
    review = Review(movie, "not good", 2)
    a_review = make_review(review_text, user, movie, rating)
    x.add_review(a_review)
    a_reviewer = x.get_review_for_movie(movie)
    assert a_reviewer[0] == review


def test_repository_movies_have_rating():
    a_movie = Movie("Guardians of the Galaxy", 2014)
    movie = x.get_movie(a_movie)

    assert movie.rating == 8.1


def test_repository_get_10_movies_with_genre():
    a_genre = Genre("Action")
    genre_list = x.get_10_movies_genre(a_genre)
    assert len(genre_list) == 10


def test_repository_can_retrieve_a_user():
    x = memory_repository.MemoryRepository()
    user = User('dave', '123456789')
    x.add_user(user)
    user = x.get_user('dave')
    assert user == User('dave', '123456789')


def test_repository_does_not_retrieve_a_non_existent_user():
    x = memory_repository.MemoryRepository()
    user = x.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count():
    x = memory_repository.MemoryRepository()
    data_path = os.path.join('website', 'datafilereaders', 'datafiles')
    memory_repository.load_movies(data_path, x)
    number_of_movies = x.get_number_of_movies()

    # Check that the query returned 1000 movies..
    assert number_of_movies == 1000


def test_repository_can_add_movie():
    x = memory_repository.MemoryRepository()
    movie = Movie(
        "Prometheus",
        2010,
    )
    x.add_movie(movie)

    assert x.get_movie(movie) is movie


def test_repository_can_retrieve_movie():
    x = memory_repository.MemoryRepository()
    data_path = os.path.join('website', 'datafilereaders', 'datafiles')
    memory_repository.load_movies(data_path, x)
    a_movie = Movie("Guardians of the Galaxy", 2014)
    a_genre = Genre("Action,Adventure,Sci-Fi")

    movie = x.get_movie(a_movie)

    # Check that the Movie has the expected title.
    assert movie.title == "Guardians of the Galaxy"
    assert movie.release == 2014

    assert str(movie.genres) == '[<Genre Action>, <Genre Adventure>, <Genre Sci-Fi>]'


def test_repository_does_not_retrieve_a_non_existent_movie():
    a_movie = Movie("fake movie", 2014)
    movie = x.get_movie(a_movie)
    assert movie is None


def test_repository_movies_have_genres():
    newlist = x.get_10_movies()

    # Check that the query returned 10 Articles.
    assert len(newlist) == 10
    assert newlist[0].genres is not None


def test_repository_can_retrieve_top_rated_movies():
    movies = x.get_10_movies()
    # Check that the query returned 10 Movies.
    assert len(movies) == 10
    assert movies[0].rating == 9.0


def test_repository_can_retrieve_movies_by_title():
    movies = x.get_movies_by_title("da")
    print(movies)


def test_repository_can_retrieve_movies_by_actor():
    actor = Actor("Maika Monroe")
    movies = x.get_movies_by_actor("Maika")
    for movie in movies:
        assert actor in movie.actors

def test_repository_can_retrieve_movie_url():
    url = memory_repository.imdb_from_title("The Dark Knight", 2008)
    assert url == "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg"


def test_repository_can_retrieve_movies_by_director():
    movies = x.get_movies_by_director("ron howard")
    assert len(movies) == 5


def test_repository_can_get_latest_movies():
    x.sort_movies_by_release()
    latest_movie = x.get_first_movie()
    oldest_movie = x.get_last_movie()
    assert oldest_movie.release == 2006
    assert latest_movie.release == 2016

def test_repository_can_add_a_review():
    x = memory_repository.MemoryRepository()
    user = User('dave', '123456789')
    x.add_user(user)
    movie = Movie(
        "Prometheus",
        2010,
    )
    review = make_review("Not good", user, movie, 4, datetime.today())
    x.add_review(review)

    assert review in x.get_reviews()


def test_repository_does_not_add_a_review_without_a_user():
    movie = Movie(
        "Prometheus",
        2010,
    )
    with pytest.raises(ReviewException):
        review = make_review("Not good", None, movie, 4, datetime.today())


def test_repository_does_not_add_a_review_without_an_movie_properly_attached(in_memory_repo):
    user = User('dave', '123456789')
    in_memory_repo.add_user(user)

    movie = Movie(
        "Prometheus",
        2010,
    )
    review = Review(None,"yeah good", 10)

    with pytest.raises(RepositoryException):
        # Exception expected because the Article doesn't refer to the Comment.
        in_memory_repo.add_review(review)

def test_get_director(in_memory_repo):
    directors = in_memory_repo.get_director()
    assert len(directors) == 644

def test_add_director_duplicate(in_memory_repo):
    director = Director("Taika Waititi")
    in_memory_repo.add_director(director)
    assert in_memory_repo.get_director().count(director) == 1

def test_repository_can_retrieve_reviews(in_memory_repo):
    x = memory_repository.MemoryRepository()
    user = User('dave', '123456789')
    x.add_user(user)
    movie = Movie(
        "Prometheus",
        2010,
    )
    another_movie = Movie("It Follows",2014)
    review = make_review("Not good", user, movie, 4, datetime.today())
    in_memory_repo.add_review(review)
    another_review = make_review("awesome", user, another_movie, 10, datetime.today())
    in_memory_repo.add_review(another_review)

    assert len(in_memory_repo.get_reviews()) == 2
