import datetime

import pytest

from sqlalchemy.exc import IntegrityError

from website.domainmodel.model import User, Movie, Review, Genre, Actor, Director, make_review


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:username, :password)',
                          {'username': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :username',
                                {'username': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_movie(empty_session):
    empty_session.execute(
        'INSERT INTO movies (title,release,description,director,runtime,rating,metascore,num_of_ratings,image_hyperlink) VALUES'
        '("Fake_movie", 2020, "terrible fake movie","Director Ben", 155,7.6,88,145.5,"fake-link")'
    )
    row = empty_session.execute("SELECT id from movies").fetchone()
    return row[0]


def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genres (name) VALUES ("Western"), ("Action")'
    )
    rows = list(empty_session.execute('SELECT id from genres'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_genre_association(empty_session, genres_key, movie_key):
    stmt = 'INSERT INTO movie_genres (movie_id,genre_id) VALUES (:movie_id, :genre_id)'
    for genre_key in genres_key:
        empty_session.execute(stmt, {'movie_id': movie_key, "genre_id": genre_key})


def insert_actors(empty_session):
    empty_session.execute(
        'INSERT INTO actors (full_name) VALUES ("Brad Pitt"), ("Matt Damon")'
    )
    rows = list(empty_session.execute('SELECT id from actors'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_actor_association(empty_session, actors_key, movie_key):
    stmt = 'INSERT INTO movie_actors (movie_id,actor_id) VALUES (:movie_id, :actor_id)'
    for actor_key in actors_key:
        empty_session.execute(stmt, {'movie_id': movie_key, "actor_id": actor_key})


def insert_review_movie(empty_session):
    movie_key = insert_movie(empty_session)
    user_key = insert_user(empty_session)

    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        'INSERT INTO reviews (user_id, movie_id, rating, comment, timestamp) VALUES'
        '(:user_id, :movie_id, 5, "Comment 1", :timestamp_1),'
        '(:user_id, :movie_id, 10, "Comment 2", :timestamp_2)',
        {'user_id': user_key, 'movie_id': movie_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT id from movies').fetchone()
    return row[0]


def make_movie():
    movie = Movie(
        "Fake_movie", 2020
    )
    movie.runtime_minutes = 155
    movie.rating = 7.6
    movie.metascore = "88"
    movie.num_of_ratings = 145.5
    movie.description = "terrible fake movie"
    movie.image = "fake-link"
    return movie


def make_user():
    user = User("Andrew", "111")
    return user


def make_genre():
    genre = Genre("Action")
    return genre


def make_actor():
    actor = Actor("Johnny depp")
    return actor


def make_director():
    director = Director("Director Ben")
    return director


def test_loading_of_users(empty_session):
    users = list()
    users.append(("andrew", "1234"))
    users.append(("cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("andrew", "1234"),
        User("cindy", "1111")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("andrew", "111")]


def test_saving_of_users_with_common_username(empty_session):
    insert_user(empty_session, ("andrew", "1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("andrew", "111")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_movie(empty_session):
    movie_key = insert_movie(empty_session)
    expected_movie = make_movie()
    fetched_movie = empty_session.query(Movie).one()

    assert expected_movie == fetched_movie



def test_loading_of_genre_movie(empty_session):
    movie_key = insert_movie(empty_session)
    genre_keys = insert_genres(empty_session)
    insert_genre_association(empty_session, genre_keys, movie_key)

    movie = empty_session.query(Movie).get(movie_key)
    genres = [empty_session.query(Genre).get(key) for key in genre_keys]

    for genre in genres:
        assert genre in movie.genres


def test_loading_of_actor_movie(empty_session):
    movie_key = insert_movie(empty_session)
    actor_keys = insert_actors(empty_session)
    insert_actor_association(empty_session, actor_keys, movie_key)

    movie = empty_session.query(Movie).get(movie_key)
    actors = [empty_session.query(Actor).get(key) for key in actor_keys]

    for actor in actors:
        assert actor in movie.actors


def test_loading_of_commented_movie(empty_session):
    insert_review_movie(empty_session)

    rows = empty_session.query(Movie).all()
    movie = rows[0]

    assert len(movie._reviews) == 2

    for review in movie._reviews:
        assert review._movie is movie


def test_saving_of_comment(empty_session):
    movie_key = insert_movie(empty_session)
    user_key = insert_user(empty_session, ("andrew", "1234"))

    rows = empty_session.query(Movie).all()
    movie = rows[0]
    user = empty_session.query(User).filter(User._user_name == "andrew").one()

    # Create a new Comment that is bidirectionally linked with the User and Article.
    comment_text = "Some comment text."
    comment = make_review(comment_text, user, movie, 10, datetime.datetime.now())

    # Note: if the bidirectional links between the new Comment and the User and
    # Article objects hadn't been established in memory, they would exist following
    # committing the addition of the Comment to the database.
    empty_session.add(comment)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, movie_id, comment FROM reviews'))

    assert rows == [(user_key, movie_key, comment_text)]


def test_saving_of_movie(empty_session):
    movie = make_movie()
    director = make_director()
    empty_session.add(director)
    movie.director = director
    empty_session.add(movie)
    empty_session.commit()
    directors = list(empty_session.execute(
        'SELECT * FROM directors'
    ))
    print(movie.director)
    test = list(empty_session.execute(
        'SELECT * FROM movies'
    ))
    print(test)
    rows = list(empty_session.execute(
            'SELECT title,release,description, runtime,rating,metascore,num_of_ratings,image_hyperlink FROM movies'))

    assert rows == [("Fake_movie", 2020, "terrible fake movie", 155, 7.6, "88", 145.5, "fake-link")]


def test_saving_movie_with_actors_genres(empty_session):
    movie = make_movie()
    genre = make_genre()
    actor = make_actor()
    empty_session.add(genre)
    empty_session.add(actor)
    empty_session.commit()

    movie.genres.append(genre)
    movie.actors.append(actor)

    empty_session.add(movie)
    empty_session.commit()

    # Test test_saving_of_article() checks for insertion into the articles table.
    rows = list(empty_session.execute('SELECT id FROM movies'))
    movie_key = rows[0][0]

    # Check that the tags table has a new record.
    rows = list(empty_session.execute('SELECT id, name FROM genres'))
    genre_key = rows[0][0]
    assert rows[0][1] == "Action"

    # Check that the article_tags table has a new record.
    rows = list(empty_session.execute('SELECT movie_id, genre_id from movie_genres'))
    movie_foreign_key = rows[0][0]
    genre_foreign_key = rows[0][1]

    assert movie_key == movie_foreign_key
    assert genre_key == genre_foreign_key


def test_save_commented_movie(empty_session):
    # Create Article User objects.
    movie = make_movie()
    user = make_user()

    # Create a new Comment that is bidirectionally linked with the User and Article.
    comment_text = "Some comment text."
    comment = make_review(comment_text, user, movie,10)


    empty_session.add(movie)
    empty_session.commit()

    # Test test_saving_of_article() checks for insertion into the articles table.
    rows = list(empty_session.execute('SELECT id FROM movies'))
    movie_key = rows[0][0]

    # Test test_saving_of_users() checks for insertion into the users table.
    rows = list(empty_session.execute('SELECT id FROM users'))
    user_key = rows[0][0]

    # Check that the comments table has a new record that links to the articles and users
    # tables.
    rows = list(empty_session.execute('SELECT user_id, movie_id, comment FROM reviews'))
    assert rows == [(user_key, movie_key, comment_text)]