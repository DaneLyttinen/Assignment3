from domainmodel.genre import Genre
from domainmodel.actor import Actor
from domainmodel.director import Director

class Movie:
    def __init__(self, title: str, release: int):
        if title == "" or type(title) is not str:
            self._title = None
        else:
            self._title = title.strip()
        if release == "" or type(release) is not int or release < 1900:
            self.release = None
        else:
            self.release = release

        self._description: str
        self._director: Director = None
        self._actors = []
        self._genres = []
        self._runtime_minutes: int

    def __repr__(self):
        return f"<Movie {self._title}, {self.release}>"

    def __eq__(self, other):
        return other.title == self.title and other.release == self.release

    def __lt__(self, other):
        return self.__repr__() < other.__repr__()

    def __hash__(self):
        return hash((self.title, self.release))

    @property
    def actors(self):
        return self._actors

    @property
    def genres(self):
        return self._genres

    def add_actor(self, actor):
        if type(actor) is Actor and actor not in self._actors:
            self._actors.append(actor)

    def remove_actor(self, actor):
        if actor in self._actors:
            self._actors.remove(actor)
        else:
            pass

    def add_genre(self, genre):
        if type(genre) is Genre and genre not in self._genres:
            self._genres.append(genre)

    def remove_genre(self, genre):
        if genre in self._genres:
            self._genres.remove(genre)
        else:
            pass

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if type(value) is str:
            self._title = value.strip()

    @property
    def description(self):
        return self._description.strip()

    @description.setter
    def description(self, desc):
        if type(desc) is str:
            self._description = desc.strip()

    @actors.setter
    def actors(self, ac):
        if ac not in self._actors and type(ac) is Actor:
            self._actors.append(ac)
        else:
            pass

    @genres.setter
    def genres(self, value):
        if value not in self._genres and type(value) is Genre:
            self._genres.append(value)
        else:
            pass

    @property
    def runtime_minutes(self):
        return self._runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, value):
        if value > 0 and type(value) is int:
            self._runtime_minutes = value
        else:
            raise ValueError

    @property
    def director(self) -> Director:
        return self._director

    @director.setter
    def director(self, value):
        if type(value) is Director:
            self._director = value
