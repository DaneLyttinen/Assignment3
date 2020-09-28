from datetime import datetime

from website.domainmodel.movie import Movie

class Review:
    def __init__(self, movie: Movie, review_text: str, rating: int):
        if type(movie) is Movie:
            self._movie = movie
        else:
            self._movie = None
        if type(review_text) is str:
            self._review_text = review_text
        else:
            self._review_text = None
        if type(rating) is int and 1 <= rating <= 10:
            self._rating = rating
        else:
            self._rating = None
        self._date = datetime

    def __repr__(self):
        return f"{self._movie}/n" \
               f"Review: {self._review_text}>/n" \
               f"Rating: {self._rating}"

    def __eq__(self, other):
        return self._movie == other._movie and self._rating == other._rating and self._review_text == other._review_text and self._date == other._date

    @property
    def movie(self):
        return self._movie

    @movie.setter
    def movie(self, movies):
        if type(movies) is Movie:
            self._movie = movies
        else:
            self._movie = None

    @property
    def review_text(self):
        return self._review_text

    @review_text.setter
    def review_text(self, reviews):
        if type(reviews) is str:
            self._review_text = reviews
        else:
            self._review_text = None

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, ratings):
        if type(ratings) is int and 1 <= ratings <= 10:
            self._rating = ratings
        else:
            self._rating = None

    @property
    def timestamp(self):
        return self._date

    @timestamp.setter
    def timestamp(self, value):
        self._date = value

