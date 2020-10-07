from website.datafilereaders.movie_file_csv_reader import MovieFileCSVReader

from flask import Flask

app = Flask(__name__)


def main():
    filename = 'datafilereaders/datafiles/Data1000Movies.csv'
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()


if __name__ == "__main__":
    app.run(host='localhost', port=5000, threaded=False)
