from datetime import date

import pytest

from website.Home.services import NonExistentMovieException
from website.authentication.services import AuthenticationException
from website.Home import services as home_services
from website.authentication import services as auth_services
from website.domainmodel.model import Movie, Review, Genre
from website.movie_genre import services as genre_services
from website.directory.memory_repository import MemoryRepository


def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'thorke'
    password = 'abcd1A23'
    auth_services.add_user(username, password, in_memory_repo)
    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


def test_can_add_review(in_memory_repo):
    movie_title = "Inception"
    movie = in_memory_repo.get_movie_by_title(movie_title)
    review_text = 'Super good movie!'
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    # Call the service layer to add the comment.
    home_services.add_review(movie, review_text, 10, new_username, in_memory_repo)

    # Retrieve the comments for the article from the repository.
    reviews = movie.reviews

    # Check that the comments include a comment with the new comment text.
    assert reviews != []


def test_cannot_add_comment_for_non_existent_movie(in_memory_repo):
    movie = Movie("not real", 2020)
    review_text = 'Super good movie!'
    username = 'fmercury'
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    # Call the service layer to attempt to add the comment.
    with pytest.raises(home_services.NonExistentMovieException):
        home_services.add_review(movie, review_text, 10, new_username, in_memory_repo)


def test_cannot_add_comment_by_unknown_user(in_memory_repo):
    movie = in_memory_repo.get_movie_by_title("Inception")
    review_text = 'Super good movie!'
    username = 'gmichael'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(home_services.UnknownUserException):
        home_services.add_review(movie, review_text, 10, username, in_memory_repo)


def test_get_reviews_for_movie_without_comments(in_memory_repo):
    movie = in_memory_repo.get_movie_by_title("Inception")
    assert len(movie.reviews) == 0


def test_get_10_movies_genre(in_memory_repo):
    genre = Genre("Action")
    action_movies = home_services.get_10_movies_genre(in_memory_repo, genre)
    assert len(action_movies) == 10
    for movie in action_movies:
        assert genre in movie.genres


def test_get_genres(in_memory_repo):
    genres = home_services.get_genres(in_memory_repo)
    assert len(genres) == 20
    for genre in genres:
        assert type(genre) is Genre

def test_get_10_movies(in_memory_repo):
    movies = home_services.get_ten_movies(in_memory_repo)
    assert len(movies) == 10
    for movie in movies:
        assert type(movie) is Movie


def test_get_reviews_for_movie(in_memory_repo):
    movie = home_services.get_movie(in_memory_repo, "Inception")
    reviews = movie.reviews
    review = Review(movie, "Best movie ever", 10)
    movie.add_review(review)
    # Check that 1 comments were returned for movie with title Inception.
    assert len(movie.reviews) == 1

def test_get_movies_actor(in_memory_repo):
    actors = genre_services.get_movies_by_actor(in_memory_repo, "Matt Damon")
    assert len(actors) == 10

def test_get_movies_non_existant_actor(in_memory_repo):
    with pytest.raises(genre_services.NonExistentActorException):
        genre_services.get_movies_by_actor(in_memory_repo, None)

def test_get_movies_director(in_memory_repo):
    movies = genre_services.get_movies_by_director(in_memory_repo, "Christopher Nolan")
    assert len(movies) == 5
    for movie in movies:
        assert movie.director.director_full_name == "Christopher Nolan"

def test_get_movies_non_existant_director(in_memory_repo):
    with pytest.raises(genre_services.NonExistentDirectorException):
        genre_services.get_movies_by_director(in_memory_repo, None)

def test_get_all_movies_genre(in_memory_repo):
    genre = Genre("Western")
    movies = genre_services.get_all_movies_genre(in_memory_repo, genre)
    assert len(movies) == 7
    for movie in movies:
        assert genre in movie.genres

def test_get_all_movies_non_existant_genre(in_memory_repo):
    with pytest.raises(genre_services.NonExistentGenreException):
        genre_services.get_all_movies_genre(in_memory_repo, None)