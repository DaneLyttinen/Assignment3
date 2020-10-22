import os
from datetime import date, datetime
from typing import List

import pytest

from website.directory import memory_repository
from website.directory.repository import AbstractRepository, RepositoryException
from website.domainmodel.model import Movie, User, Review, Actor, Director, Genre, make_review

from website.datafilereaders import movie_file_csv_reader
from website.directory import memory_repository

x = memory_repository.MemoryRepository()
data_path = os.path.join('../website', 'datafilereaders', 'datafiles')
memory_repository.load_movies(data_path, x)


def test_repository_can_load_movies():
    data_path = os.path.join('../website', 'datafilereaders', 'datafiles')
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
    print(genre_list)
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
    data_path = os.path.join('../website', 'datafilereaders', 'datafiles')
    memory_repository.load_movies(data_path, x)
    number_of_movies = x.get_number_of_movies()

    # Check that the query returned 6 Articles.
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
    data_path = os.path.join('../website', 'datafilereaders', 'datafiles')
    memory_repository.load_movies(data_path, x)
    a_movie = Movie("Guardians of the Galaxy", 2014)
    a_genre = Genre("Action,Adventure,Sci-Fi")

    movie = x.get_movie(a_movie)

    # Check that the Movie has the expected title.
    assert movie.title == "Guardians of the Galaxy"
    assert movie.release == 2014

    assert movie.genres == '[<Genre Action>, <Genre Adventure>, <Genre Sci-Fi>]'


def test_repository_does_not_retrieve_a_non_existent_movie():
    a_movie = Movie("fake movie", 2014)
    movie = x.get_movie(a_movie)
    assert movie is None


def test_repository_movies_have_genres():
    newlist = x.get_10_movies()

    # Check that the query returned 10 Articles.
    assert len(newlist) == 10
    print(newlist[0].genres)
    assert newlist[0].genres is not None


def test_repository_can_retrieve_top_rated_movies():
    movies = x.get_10_movies()
    print(movies[0])
    # Check that the query returned 10 Movies.
    assert len(movies) == 10
    assert movies[0].rating == 9.0


def test_repository_can_retrieve_movies_by_title():
    movies = x.get_movies_by_title("da")
    print(movies)


def test_repository_can_retrieve_movies_by_actor():
    movies = x.get_movies_by_actor("Maika")
    for movie in movies:
        print(movie.actors)
    print(movies)

def test_repository_can_retrieve_movie_url():
    memory_repository.imdb_from_title("The Dark Knight", 2008)



def test_repository_can_retrieve_movies_by_director():
    movies = x.get_movies_by_director("ron howard")
    print(movies)
    assert len(movies) == 5

def test_repository_can_retrieve_tags(in_memory_repo):
    tags: List[Tag] = in_memory_repo.get_tags()

    assert len(tags) == 4

    tag_one = [tag for tag in tags if tag.tag_name == 'New Zealand'][0]
    tag_two = [tag for tag in tags if tag.tag_name == 'Health'][0]
    tag_three = [tag for tag in tags if tag.tag_name == 'World'][0]
    tag_four = [tag for tag in tags if tag.tag_name == 'Politics'][0]

    assert tag_one.number_of_tagged_articles == 3
    assert tag_two.number_of_tagged_articles == 2
    assert tag_three.number_of_tagged_articles == 3
    assert tag_four.number_of_tagged_articles == 1


def test_repository_can_get_first_movie():
    x.sort_movies_by_release()
    latest_movie = x.get_first_movie()
    print(latest_movie.release)
    oldest_movie = x.get_last_movie()
    assert oldest_movie.release == 2006
    assert latest_movie.release == 2016


def test_repository_can_get_last_article(in_memory_repo):
    article = in_memory_repo.get_last_article()
    assert article.title == 'Coronavirus: Death confirmed as six more test positive in NSW'


def test_repository_can_get_articles_by_ids(in_memory_repo):
    articles = in_memory_repo.get_articles_by_id([2, 5, 6])

    assert len(articles) == 3
    assert articles[
               0].title == 'Covid 19 coronavirus: US deaths double in two days, Trump says quarantine not necessary'
    assert articles[1].title == "Australia's first coronavirus fatality as man dies in Perth"
    assert articles[2].title == 'Coronavirus: Death confirmed as six more test positive in NSW'


def test_repository_does_not_retrieve_article_for_non_existent_id(in_memory_repo):
    articles = in_memory_repo.get_articles_by_id([2, 9])

    assert len(articles) == 1
    assert articles[
               0].title == 'Covid 19 coronavirus: US deaths double in two days, Trump says quarantine not necessary'


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    articles = in_memory_repo.get_articles_by_id([0, 9])

    assert len(articles) == 0


def test_repository_returns_article_ids_for_existing_tag(in_memory_repo):
    article_ids = in_memory_repo.get_article_ids_for_tag('New Zealand')

    assert article_ids == [1, 3, 4]


def test_repository_returns_an_empty_list_for_non_existent_tag(in_memory_repo):
    article_ids = in_memory_repo.get_article_ids_for_tag('United States')

    assert len(article_ids) == 0


def test_repository_returns_date_of_previous_article(in_memory_repo):
    article = in_memory_repo.get_article(6)
    previous_date = in_memory_repo.get_date_of_previous_article(article)

    assert previous_date.isoformat() == '2020-03-01'


def test_repository_returns_none_when_there_are_no_previous_articles(in_memory_repo):
    article = in_memory_repo.get_article(1)
    previous_date = in_memory_repo.get_date_of_previous_article(article)

    assert previous_date is None


def test_repository_returns_date_of_next_article(in_memory_repo):
    article = in_memory_repo.get_article(3)
    next_date = in_memory_repo.get_date_of_next_article(article)

    assert next_date.isoformat() == '2020-03-05'


def test_repository_returns_none_when_there_are_no_subsequent_articles(in_memory_repo):
    article = in_memory_repo.get_article(6)
    next_date = in_memory_repo.get_date_of_next_article(article)

    assert next_date is None


def test_repository_can_add_a_tag(in_memory_repo):
    tag = Tag('Motoring')
    in_memory_repo.add_tag(tag)

    assert tag in in_memory_repo.get_tags()


def test_repository_can_add_a_comment():
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


def test_repository_does_not_add_a_comment_without_a_user():
    movie = Movie(
        "Prometheus",
        2010,
    )
    review = make_review("Not good", None, movie, 4, datetime.today())

    with pytest.raises(RepositoryException):
        x.add_review(review)


def test_repository_does_not_add_a_review_without_an_movie_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')

    movie = Movie(
        "Prometheus",
        2010,
    )
    comment = add(None, "Trump's onto it!", datetime.today())

    user.add_comment(comment)

    with pytest.raises(RepositoryException):
        # Exception expected because the Article doesn't refer to the Comment.
        in_memory_repo.add_comment(comment)


def test_repository_can_retrieve_comments(in_memory_repo):
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
    print(in_memory_repo.get_reviews())
    assert len(in_memory_repo.get_reviews()) == 2
