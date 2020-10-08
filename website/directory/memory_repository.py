import csv
import os
from bisect import bisect_left
from datetime import date, datetime
from typing import List
from werkzeug.security import generate_password_hash

from website.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from website.directory.repository import AbstractRepository, RepositoryException
from website.domainmodel import movie, user, review, watchlist, actor, director, genre
from website.domainmodel.actor import Actor
from website.domainmodel.director import Director
from website.domainmodel.genre import Genre
from website.domainmodel.movie import Movie
from website.domainmodel.review import Review
from website.domainmodel.user import User
from website.datafilereaders import movie_file_csv_reader


class MemoryRepository(AbstractRepository):
    # Articles ordered by date, not id. id is assumed unique.

    def __init__(self):
        self._movies = list()
        self._movies_index = dict()
        self._genre = list()
        self._users = list()
        self._reviews = list()
        self._actors = list()
        self._directors = list()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.user_name == username), None)

    def add_movie(self, movie: Movie):
        if type(movie) is Movie and movie not in self._movies:
            self._movies.append(movie)

    def get_movie(self, id: Movie) -> Movie:
        movie = None

        try:
            for i in self._movies:
                if i == id:
                    movie = i;
        except KeyError:
            pass  # Ignore exception and return None.

        return movie

    def get_movies_by_date(self, target_movie: movie.Movie.title) -> List[movie.Movie]:
        target_article = movie.Movie(
            title=target_movie,
            release=target_movie.release
        )
        matching_articles = list()

        try:
            index = self.movie_index(target_article)
            for article in self._movies[index:None]:
                if article.date == target_movie:
                    matching_articles.append(article)
                else:
                    break
        except ValueError:
            # No articles for specified date. Simply return an empty list.
            pass

        return matching_articles

    def get_number_of_movies(self):
        return len(self._movies)

    def sort_movies_by_date(self):
        self._movies.sort(key=lambda x: x.release, reverse=True)

    def get_first_movie(self):
        movie = None
        if len(self._movies) > 0:
            movie = self._movies[0]
        return movie

    def get_last_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[-1]
        return movie

    def get_movie_by_title(self, title):
        # Strip out any ids in id_list that don't represent Article ids in the repository.

        for movie in self._movies:
            if movie.title == title:
                return movie
        # Fetch the Articles.


    def get_date_of_previous_movie(self, article: movie.Movie):
        previous_date = None

        try:
            index = self.movie_index(article)
            for stored_movie in reversed(self._movies[0:index]):
                if stored_movie.release < article.release:
                    previous_date = stored_movie.release
                    break
        except ValueError:
            # No earlier articles, so return None.
            pass

        return previous_date

    def get_date_of_next_movie(self, movie: Movie):
        next_date = None

        try:
            index = self.movie_index(movie)
            for stored_movie in self._movies[index + 1:len(self._movies)]:
                if stored_movie.release > movie.release:
                    next_date = stored_movie.release
                    break
        except ValueError:
            # No subsequent articles, so return None.
            pass

        return next_date

    def add_comment(self, comment: Review):
        super().add_comment(comment)
        self._reviews.append(comment)

    def get_comments(self):
        return self._reviews

    # Helper method to return article index.
    def movie_index(self, movie: Movie):
        index = bisect_left(self._movies, movie)
        if index != len(self._movies) and self._movies[index].date == movie.release:
            return index
        raise ValueError

    def get_10_top_rated(self):
        a_list = sorted(self._movies, key=lambda x: x.release, reverse=True)

    def get_10_movies(self):
        a_list = []
        count = 0
        a_sort = sorted(self._movies, key=lambda x: x.rating, reverse=True)
        for i in a_sort:
            if count < 10:
                a_list.append(i)
            else:
                break
            count += 1
        return a_list

    def get_genres(self):
        return self._genre

    def add_genre(self, genre):
        if type(genre) is Genre and genre not in self._genre:
            self._genre.append(genre)

    def get_actors(self):
        return self._actors

    def add_actors(self, actor):
        if type(actor) is Actor and actor not in self._actors:
            self._actors.append(actor)

    def get_director(self):
        return self._directors

    def add_director(self, director):
        if type(director) is Director and director not in self._directors:
            self._directors.append(director)

    def get_10_movies_genre(self, genre):
        if type(genre) is not Genre:
            return
        a_list = []
        count = 0
        for movie in self._movies:
            if genre in movie.genres:
                a_list.append(movie)
            if genre == Genre("Western") and len(a_list) == 5:
                break
            if genre == Genre("Musical") and len(a_list) == 5:
                break
            if len(a_list) == 10:
                break
        return a_list

    def get_all_movies_genre(self, genre):
        if type(genre) is not Genre:
            return
        a_list = []
        count = 0
        print(self._movies)
        for movie in self._movies:
            if genre in movie.genres:
                a_list.append(movie)
        return a_list


def load_movies(data_path: str, repo: MemoryRepository):
    tags = dict()
    data_path = "C:\\Users\Dane\\Desktop\\Assignment2\\website\\datafilereaders\\datafiles"
    movie_file_reader = MovieFileCSVReader(data_path)
    movie_file_reader.read_csv_file()
    for data_row in movie_file_reader.dataset_of_movies:
        repo.add_movie(data_row)


def load_genres(data_path: str, repo: MemoryRepository):
    data_path = "C:\\Users\Dane\\Desktop\\Assignment2\\website\\datafilereaders\\datafiles"
    movie_file_reader = MovieFileCSVReader(data_path)
    movie_file_reader.read_csv_file()
    for genre in movie_file_reader.dataset_of_genres:
        repo.add_genre(genre)


def load_actors(data_path: str, repo: MemoryRepository):
    data_path = "C:\\Users\Dane\\Desktop\\Assignment2\\website\\datafilereaders\\datafiles"
    movie_file_reader = MovieFileCSVReader(data_path)
    movie_file_reader.read_csv_file()
    for act in movie_file_reader.dataset_of_actors:
        repo.add_actors(act)


def load_directors(data_path: str, repo: MemoryRepository):
    data_path = "C:\\Users\Dane\\Desktop\\Assignment2\\website\\datafilereaders\\datafiles"
    movie_file_reader = MovieFileCSVReader(data_path)
    movie_file_reader.read_csv_file()
    for dict in movie_file_reader.dataset_of_directors:
        repo.add_director(dict)


def load_users(data_path: str, repo: MemoryRepository):
    users = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(
            username=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_comments(data_path: str, repo: MemoryRepository, users):
    for data_row in read_csv_file(os.path.join(data_path, 'comments.csv')):
        comment = make_comment(
            comment_text=data_row[3],
            user=users[data_row[1]],
            article=repo.get_article(int(data_row[2])),
            timestamp=datetime.fromisoformat(data_row[4])
        )
        repo.add_comment(comment)


def populate(data_path: str, repo: MemoryRepository):
    # Load articles and tags into the repository.
    load_movies(data_path, repo)

    load_genres(data_path, repo)

    load_actors(data_path, repo)

    load_directors(data_path, repo)
