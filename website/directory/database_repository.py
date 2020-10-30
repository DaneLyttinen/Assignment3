import csv
import os

from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from website.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from website.domainmodel.model import User, Movie, Genre, Review, Actor, Director
from website.directory.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(_user_name=username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_movie(self, movie: Movie):
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def add_actors(self, actor: Actor):
        with self._session_cm as scm:
            scm.session.add(actor)
            scm.commit()

    def get_movie(self, id: Movie) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter(Movie._title == id.title).one()
        except NoResultFound:
            pass
        return movie

    def get_movie_by_title(self, title) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter(Movie._title.ilike(title)).one()
        except NoResultFound:
            pass
        return movie

    def add_review(self, review:Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_director(self, director: str):
        director_id = None
        try:
            director_id = self._session_cm.session.query(Director).filter(Director.director_full_name == director).one()
        except NoResultFound:
            pass
        return director_id

    def add_director(self, director: Director):
        with self._session_cm as scm:
            scm.session.add(director)
            scm.commit()

    def get_10_movies_genre(self, genre) -> list:
        movie_list = []
        a_list = []
        row = self._session_cm.session.execute('SELECT id FROM genres WHERE name = :genre_name',{'genre_name':genre.genre_name}).fetchone()
        if row is None:
            movie_list = list()
        else:
            genre_id = row[0]
            if genre.genre_name == "Western" or genre.genre_name == "Musical":
                movie_list = self._session_cm.session.execute(
                    'SELECT movie_id FROM movie_genres WHERE genre_id = :genre_id ORDER BY genre_id ASC LIMIT 5',
                    {'genre_id': genre_id}
                ).fetchall()
            else:
                movie_list = self._session_cm.session.execute(
                    'SELECT movie_id FROM movie_genres WHERE genre_id = :genre_id ORDER BY genre_id ASC LIMIT 10',
                    {'genre_id':genre_id}
                ).fetchall()
        yet_another_list = self.movie_getter_helper(movie_list)
        return yet_another_list

    def get_10_movies(self):
        a_list = []
        movie_list = self._session_cm.session.execute(
            'SELECT title FROM movies ORDER BY rating DESC LIMIT 10'
        ).fetchall()
        for movie in movie_list:
            a_list.extend(self._session_cm.session.query(Movie).filter(Movie._title == movie[0] ))
        return a_list

    def get_genres(self):
        genres = []
        try:
            genres = self._session_cm.session.query(Genre).all()
        except NoResultFound:
            pass
        return genres

    def get_movies_by_title(self, title: str) -> List[Movie]:
        movies = []
        title = "%" + title + "%"
        try:
            movies.extend(self._session_cm.session.query(Movie).filter(Movie._title.ilike(title)).all())
        except NoResultFound:
            pass
        return movies

    def get_number_of_movies(self):
        number_of_movies = self._session_cm.session.query(Movie).count()
        return number_of_movies

    def get_movies_by_director(self, director: str):
        movie_list = []
        row = self._session_cm.session.execute('SELECT name FROM directors WHERE name LIKE :director_name',{'director_name':"%"+director+"%"}).fetchone()
        if row is None:
            movie_list = list()
        else:
            director_id = row[0]
            a_list = self._session_cm.session.execute(
                'SELECT director FROM movies'
            ).fetchall()
            movie_list = self._session_cm.session.execute(
                'SELECT id FROM movies WHERE director = :director_id ORDER BY id ASC',
                {'director_id':director_id}
            ).fetchall()
        yet_another_list = self.movie_getter_helper(movie_list)
        return yet_another_list

    def get_movies_by_actor(self, actor: str):
        movie_list = []
        a_list = []
        print(actor)
        row = self._session_cm.session.execute('SELECT id FROM actors WHERE full_name LIKE :actor_name',{"actor_name":"%"+actor+"%"}).fetchone()
        if row is None:
            movie_list = list()
        else:
            actor_id = row[0]
            print("here",actor_id)
            movie_list = self._session_cm.session.execute(
                'SELECT movie_id FROM movie_actors WHERE actor_id = :actor_id ORDER BY movie_id ASC',
                {'actor_id':actor_id}
            ).fetchall()
        yet_another_list = self.movie_getter_helper(movie_list)
        return yet_another_list

    def get_all_movies_genre(self, genre) -> List[Movie]:
        movie_list = []
        a_list = []
        row = self._session_cm.session.execute('SELECT id FROM genres WHERE name = :genre_name',{'genre_name':genre.genre_name}).fetchone()
        if row is None:
            movie_list = list()
        else:
            genre_id = row[0]
            movie_list = self._session_cm.session.execute(
                'SELECT movie_id FROM movie_genres WHERE genre_id = :genre_id ORDER BY genre_id ASC',
                {'genre_id':genre_id}
            ).fetchall()
        yet_another_list = self.movie_getter_helper(movie_list)
        return yet_another_list

    def get_reviews(self):
        reviews_list = []
        try:
            reviews_list = self._session_cm.session.query(Review).all()
        except NoResultFound:
            pass
        return reviews_list

    def get_review_for_movie(self, movie) -> List[Review]:
        reviews_list = []
        try:
            reviews_list = self._session_cm.session.query(Review).filter(Review._movie == movie).all()
        except NoResultFound:
            pass
        return reviews_list

    def movie_getter_helper(self, movie_list):
        a_list = []
        for movie in movie_list:
            a_list.extend(self._session_cm.session.execute(
                        'SELECT title FROM movies WHERE id = :movie_id',
                        {'movie_id':movie[0]}
                    ).fetchall())
        yet_another_list = []
        for title in a_list:
            movies = self._session_cm.session.query(Movie).filter(Movie._title == title[0]).all()
            yet_another_list.append(movies[0])
        return yet_another_list

def generic_generator(filename, post_process=None):
    with open(filename) as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]

            if post_process is not None:
                row = post_process(row)
            yield row


def populate(session_factory, data_path, data_filename):
    filename = os.path.join(data_path, data_filename)
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()

    session = session_factory()
    for director in movie_file_reader.dataset_of_directors:
        session.add(director)
    for movie in movie_file_reader.dataset_of_movies:
        session.add(movie)
    filename = os.path.join(data_path, "users.csv")
    users_file_reader = MovieFileCSVReader(filename)
    users_file_reader.read_csv_file_users()

    for user in users_file_reader.dataset_of_users:
        session.add(user)

    session.commit()
