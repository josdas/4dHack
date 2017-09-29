class Place:
    def __init__(self, name, position, info):
        self.name = name
        self.position = tuple(position)
        self.info = info

    def to_dick(self):
        return {
            'name': self.name,
            'position': list(self.position),
            'info': self.info
        }

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return self.position.__hash__()
