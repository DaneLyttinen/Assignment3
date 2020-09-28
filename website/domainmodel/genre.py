class Genre:
    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.genre_name = None
        else:
            self.genre_name = genre_name.strip()

    def __repr__(self):
        return f"<Genre {self.genre_name}>"

    def __eq__(self, other):
        return other.genre_name == self.genre_name

    def __lt__(self, other):
        return self.genre_name[0] < other.genre_name[0]

    def __hash__(self):
        return hash(self.genre_name)