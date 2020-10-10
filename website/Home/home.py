from flask import Blueprint, render_template, url_for, request
from better_profanity import profanity
from flask_wtf import FlaskForm, Form
from werkzeug.utils import redirect
from wtforms import TextAreaField, HiddenField, SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, Length, ValidationError
import website.directory.repository as repo
import website.directory.memory_repository as mem
import website.Home.services as services
from website.domainmodel.model import Genre
import website.movie_genre.movie_genre

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    ten_movies = services.get_ten_movies(repo.repo_instance)
    genres = services.get_genres(repo.repo_instance)
    movies_genres = {}
    search = MovieSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    genre_url = []
    for genre in genres:
        try:
            movies_genres[genre] = services.get_10_movies_genre(repo.repo_instance, genre)
            genre_url.append(url_for('all_movies_bp.movies_by_genre', genre=genre))
        except:
            pass

    return render_template(
        'home/home.html',
        ten_movies=ten_movies,
        genres=genres,
        movies_genres=movies_genres,
        genre_url=genre_url,
        form=search
    )

@home_blueprint.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']


@home_blueprint.route('/genres', methods=['GET'])
def movies_by_genre():
    genre = request.args.get('genre')

    return redirect(url_for('all_movies_bp.movies_by_genre'))


class MovieSearchForm(Form):
    choices = [('Title'), ('Title'),
               ('Actor'), ('Actor'),
               ('Director'), ('Director')]
    select = SelectField('Search movies:', choices=choices)
    search = StringField('')
