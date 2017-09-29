class Path:
    def __init__(self, places, tags):
        self.places = places
        self.tags = tags

    def __str__(self):
        return 'From {} to {} with tags {}'.format(self.places[0].position, self.places[-1].position, self.tags)
