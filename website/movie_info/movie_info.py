from flask import Blueprint, render_template, request, session, url_for
from better_profanity import profanity
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
import website.directory.repository as repo
import website.directory.memory_repository as mem
import website.Home.services as services
from flask_wtf import FlaskForm

from website.authentication.authentication import login_required

movie_info_blueprint = Blueprint(
    'movie_info_bp', __name__)


@movie_info_blueprint.route('/info', methods=['GET'])
def movie_info():
    movie = request.args.get('movie')
    movie_to_show_comments = request.args.get('view_reviews_for')
    print(movie)
    if movie_to_show_comments is None:
        # No view-comments query parameter, so set to a non-existent article id.
        movie_to_show_comments = -1
    else:
        # Convert article_to_show_comments from string to int.
        movie_to_show_comments = str(movie_to_show_comments)

    a_movie = services.get_movie(repo.repo_instance, movie)
    if a_movie is None:
        movie = movie[0:len(movie) - 1]
        a_movie = services.get_movie(repo.repo_instance, movie)
    return render_template(
        'movies/movie_info.html',
        movie=a_movie,
        show_comments_for_movie=movie_to_show_comments
    )


@movie_info_blueprint.route('/comment', methods=['GET', 'POST'])
@login_required
def comment_on_movie():
    username = session['username']
    form = CommentForm()


    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the article id, representing the commented article, from the form.
        movie = form.movie_id.data
        a_movie = services.get_movie(repo.repo_instance, movie)
        if a_movie is None:
            movie = movie[0:len(movie) - 1]
            a_movie = services.get_movie(repo.repo_instance, movie)

        print(username)
        # Use the service layer to store the new comment.
        services.add_review(a_movie, form.comment.data, form.review.data, username, repo.repo_instance)

        # Retrieve the article in dict form.

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('movie_info_bp.movie_info', movie=a_movie.title, view_comments_for=a_movie))
    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        a_movie = request.args.get('movie')

        # Store the article id in the form.
        form.movie_id.data = a_movie
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        a_movie = str(form.movie_id.data)
    movie = services.get_movie(repo.repo_instance, a_movie)
    return render_template(
        "movies/comment_on_movie.html",
        title='Edit article',
        movie=movie,
        form=form,
        handler_url=url_for("movie_info_bp.comment_on_movie"),

    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    review = IntegerField('Review', [
        DataRequired(),
        NumberRange(min=0, max=10, message='Your input was not a number or out of the range')

    ])
    movie_id = HiddenField("Movie id")
    submit = SubmitField('Submit')
