class Place:
    def __init__(self, name, position, other_data):
        self.name = name
        self.position = position
        self.info = other_data

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return 1