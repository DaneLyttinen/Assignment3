
class Actor:
    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.actor_full_name = None
        else:
            self.actor_full_name = actor_full_name.strip()
        self.colleague_list = []

    def __repr__(self):
        return f"<Actor {self.actor_full_name}>"

    def __eq__(self, other):
        return other.actor_full_name == self.actor_full_name

    def __lt__(self, other):
        return self.actor_full_name[0] < other.actor_full_name[0]

    def __hash__(self):
        return hash(self.actor_full_name)

    def check_if_this_actor_worked_with(self, colleague):
        if colleague in self.colleague_list or self in colleague.colleague_list:
            return True
        else:
            return False

    def add_actor_colleague(self, colleague):
        self.colleague_list.append(colleague)
        colleague.colleague_list.append(self)

