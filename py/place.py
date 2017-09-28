class Place:
    def __init__(self, name, position, other_data):
        self.name = name
        self.position = position
        self.other_data = other_data

    def __str__(self):
        return self.name

