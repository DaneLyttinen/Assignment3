from sqlalchemy import select, inspect
from website.directory.orm import metadata


def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['actors','director_movies', 'directors','genres','movie_actors','movie_genres','movies','reviews','users']

def test_database_populate_select_all_genres(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genre_names = []
        for row in result:
            all_genre_names.append(row['name'])
        print(all_genre_names)
        all_genre_names.sort()
        assert all_genre_names == ['Action',
 'Adventure',
 'Animation',
 'Biography',
 'Comedy',
 'Crime',
 'Drama',
 'Family',
 'Fantasy',
 'History',
 'Horror',
 'Music',
 'Musical',
 'Mystery',
 'Romance',
 'Sci-Fi',
 'Sport',
 'Thriller',
 'War',
 'Western']


def test_database_populate_select_all_directors(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_directors_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_directors_table]])
        result = connection.execute(select_statement)

        all_directors = []
        for row in result:
            all_directors.append(row['name'])
        all_directors.sort()
        assert len(all_directors) == 644


def test_database_populate_select_all_actors(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_actors_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_actors_table]])
        result = connection.execute(select_statement)

        all_directors = []
        for row in result:
            all_directors.append(row['full_name'])
        all_directors.sort()
        assert "50 Cent" in all_directors[0]
        assert "Óscar Jaenada" in all_directors[1984]
        assert len(all_directors) == 1985

def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[7]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])
        all_users.sort()
        assert all_users == ['fmercury', 'mjackson', 'thorke']

def test_database_populate_select_all_movies(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_movies_table = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_movies_table]])
        result = connection.execute(select_statement)

        all_movies = []
        for row in result:
            all_movies.append((row['id'], row['title']))
        a_list = []
        counter = 0
        for row in result:
            a_list.append((row['id'], row['title'], row['release'],row['description'],row['director'],row['runtime'],row['rating'],row['metascore'],row['num_of_ratings'], row['image_hyperlink']))
            counter += 1
            if counter == 10:
                break
        print(a_list)
        nr_movies = len(all_movies)
        assert nr_movies == 1000
        a = [item for item in all_movies if "Nine Lives" in item]
        a1 = [item for item in all_movies if "Up" in item]
        a2 = [item for item in all_movies if "Guardians Of The Galaxy" in item]
        assert a != None
        assert a1 != None
        assert a2 != None

