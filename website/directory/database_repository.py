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
from website.domainmodel.model import User,Movie,Genre,Review,Actor,Director
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
            user = self._session_cm.session.query(User).filter_by(_username=username).one()
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

    def add_director(self, director: Director):
        with self._session_cm as scm:
            scm.session.add(director)
            scm.commit()

    def get_10_movies_genre(self, genre) -> Genre:
        a_list = []
        try:
            if genre == Genre("Western") or genre == Genre("Musical"):
                a_list = self._session_cm.session.query(Movie).filter(Movie.genres.like(genre)).limit(5)
            else:
                a_list = self._session_cm.session.query(Movie).filter(Movie.genres.like(genre)).limit(10)
        except NoResultFound:
            pass
        return a_list

    def get_all_movies_genre(self, genre):
        a_list = []
        try:
            a_list = self._session_cm.session.query(Movie).filter(Movie.genres.like(genre)).all()
        except NoResultFound:
            pass
        return a_list

    def get_10_movies(self):
        a_List = []


    def get_genres(self):
        genres = []
        try:
            genres = self._session_cm.session.query(Genre).all()
        except NoResultFound:
            pass
        return genres

    def get_movie_by_title(self, id: str) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter(Movie.title == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return movie

    def get_number_of_movies(self):
        number_of_movies = self._session_cm.session.query(Movie).count()
        return number_of_movies

    def get_movies_by_director(self, director: str):
        movie_list =[]
        try:
            movie_list = self._session_cm.session.query(Movie).filter(Movie.director == director).all()
        except NoResultFound:
            pass
        return movie_list

    def get_movies_by_actor(self, actor: str):
        movie_list =[]
        try:
            movie_list = self._session_cm.session.query(Movie).filter(Movie.actors == actor).all()
        except NoResultFound:
            pass
        return movie_list

    def get_all_movies_genre(self, genre) -> Genre:
        movie_list = []
        try:
            movie_list = self._session_cm.session.query(Movie).filter(Movie.genres == genre.genre_name).all()
        except NoResultFound:
            pass
        return movie_list





def populate(session_factory, data_path, data_filename):

    filename = os.path.join(data_path, data_filename)
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()

    session = session_factory()

    for movie in movie_file_reader.dataset_of_movies:
        session.add(movie)
    for actor in movie_file_reader.dataset_of_actors:
        session.add(actor)
    for director in movie_file_reader.dataset_of_directors:
        session.add(director)
    for genre in movie_file_reader.dataset_of_genres:
        session.add(genre)

    session.commit()

