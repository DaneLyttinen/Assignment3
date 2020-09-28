import csv
import os
from bisect import bisect_left
from datetime import date, datetime
from typing import List
from werkzeug.security import generate_password_hash

from website.directory.repository import AbstractRepository, RepositoryException
from website.domainmodel import movie, user, review, watchlist, actor, director, genre
from website.domainmodel.user import User


class MemoryRepository(AbstractRepository):
    # Articles ordered by date, not id. id is assumed unique.

    def __init__(self):
        self._movies = list()
        self._movies_index = dict()
        self._genre = list()
        self._users = list()
        self._reviews = list()

    def add_user(self, user: user.User):
        self._users.append(user)

    def get_user(self, username) -> user.User:
        return next((User for User in self._users if user.User.user_name == username), None)

    def get_movie(self, id: int) -> movie:
        article = None

        try:
            article = self._movies_index[id]
        except KeyError:
            pass  # Ignore exception and return None.

        return article

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

    def get_number_of_articles(self):
        return len(self._movies)

    def get_first_article(self):
        article = None

        if len(self._movies) > 0:
            article = self._movies[0]
        return article

    def get_last_article(self):
        article = None

        if len(self._movies) > 0:
            article = self._movies[-1]
        return article

    def get_articles_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent Article ids in the repository.
        existing_ids = [id for id in id_list if id in self._movies_index]

        # Fetch the Articles.
        articles = [self._movies_index[id] for id in existing_ids]
        return articles

    def get_date_of_previous_article(self, article: movie.Movie):
        previous_date = None

        try:
            index = self.movie_index(article)
            for stored_article in reversed(self._movies[0:index]):
                if stored_article.date < article.release:
                    previous_date = stored_article.release
                    break
        except ValueError:
            # No earlier articles, so return None.
            pass

        return previous_date

    def get_date_of_next_article(self, article: movie):
        next_date = None

        try:
            index = self.movie_index(article)
            for stored_article in self._movies[index + 1:len(self._movies)]:
                if stored_article.release > article.release:
                    next_date = stored_article.release
                    break
        except ValueError:
            # No subsequent articles, so return None.
            pass

        return next_date

    def add_comment(self, comment: review.Review):
        super().add_comment(comment)
        self._reviews.append(comment)

    def get_comments(self):
        return self._reviews

    # Helper method to return article index.
    def movie_index(self, article: movie.Movie):
        index = bisect_left(self._movies, article)
        if index != len(self._movies) and self._movies[index].date == article.release:
            return index
        raise ValueError


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_articles_and_tags(data_path: str, repo: MemoryRepository):
    tags = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'news_articles.csv')):

        article_key = int(data_row[0])
        number_of_tags = len(data_row) - 6
        article_tags = data_row[-number_of_tags:]

        # Add any new tags; associate the current article with tags.
        for tag in article_tags:
            if tag not in tags.keys():
                tags[tag] = list()
            tags[tag].append(article_key)
        del data_row[-number_of_tags:]

        # Create Article object.
        article = Article(
            date=date.fromisoformat(data_row[1]),
            title=data_row[2],
            first_para=data_row[3],
            hyperlink=data_row[4],
            image_hyperlink=data_row[5],
            id=article_key
        )

        # Add the Article to the repository.
        repo.add_article(article)

    # Create Tag objects, associate them with Articles and add them to the repository.
    for tag_name in tags.keys():
        tag = Tag(tag_name)
        for article_id in tags[tag_name]:
            article = repo.get_article(article_id)
            make_tag_association(article, tag)
        repo.add_tag(tag)


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
    load_articles_and_tags(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load comments into the repository.
    load_comments(data_path, repo, users)
