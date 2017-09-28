import googlemaps
from googlemaps.distance_matrix import distance_matrix
from googlemaps.places import places as GooglePlace
from googlemaps.directions import directions as GoogleDirections
import place
from functools import lru_cache

GOOGLE_API_KEY_PLACES = 'AIzaSyDKGWd0jRVivr0pE3qDbB2byuqUslp5O_k'
GOOGLE_API_KEY_DISTANCE = 'AIzaSyC4jSZqis47UqaA4Uahfxh8QwnKSJi0vhc'
GOOGLE_API_KEY_DIRECTIONS = 'AIzaSyDHsLvj8Oyo0pElWFEfq7XLlmu1JS-O4Rg'


class GMap:
    """Map is a cover on goolge maps"""

    def __init__(self):
        self.gmaps_places = googlemaps.Client(key=GOOGLE_API_KEY_PLACES)
        self.gmaps_distance = googlemaps.Client(key=GOOGLE_API_KEY_DISTANCE)
        self.gmaps_directions = googlemaps.Client(key=GOOGLE_API_KEY_DIRECTIONS)

    @lru_cache(maxsize=128)
    def get_duration(self, first_point, second_point, transit_mode='transit'):
        """
        Result is a distance between two points with selected transit_mode
        transit_mode in {transit, walking}
        """
        request = distance_matrix(self.gmaps_distance, first_point, second_point,
                                  transit_mode=transit_mode,
                                  language='ru')
        elements = request['rows'][0]['elements'][0]
        if elements['status'] != 'OK':
            return None
        duration = elements['duration']['value']
        return duration // 60

    @lru_cache(maxsize=128)
    def get_places(self, place_name, location=None, radius=None, min_price=None, max_price=None):
        request = GooglePlace(self.gmaps_places, place_name,
                              radius=radius,
                              min_price=min_price,
                              max_price=max_price,
                              open_now=True,
                              location=location,
                              language='ru')
        print(request)
        if request['status'] != 'OK':
            return None
        elements = request['results']
        places = []
        for element in elements:
            name = element['name']
            position_lat_lng = element['geometry']['location']
            position = position_lat_lng['lat'], position_lat_lng['lng']
            info = {
                'types': element['types'],
                'rating': element['rating'],
                'address': element['formatted_address']
                'type': place_name
            }
            places.append(place.Place(name, position, info))
        return places

    @lru_cache(maxsize=128)
    def get_duration_way(self, start, finish, positions):
        duration = self.get_duration(start.position, positions[0].position) \
                   + self.get_duration(positions[-1].position, finish.position)
        for i in range(len(positions) - 1):
            duration += self.get_duration(positions[i].position, positions[i + 1].position, transit_mode='walking')
        return duration

    @lru_cache(maxsize=128)  # IT IS NOT WORKING
    def get_directions(self, start, finish):  # todo
        request = GoogleDirections(self.gmaps_directions, start, finish,
                                   mode='transit',
                                   region='ru',
                                   language='ru')
        elements = request[0]['legs'][0]['steps']
        distription = []
        points = []
        for element in elements:
            points.append()
            distription.append(element['html_instructions'])
        return (points, distription)


if __name__ == '__main__':
    gmap = GMap()
    print(gmap.get_directions((59.974597, 30.336504), (59.964200, 30.357014)))
    print(gmap.get_places('restaurant'))
    assert gmap.get_duration('new york', 'chicago') == 44268
    gmap.get_duration((59.974597, 30.336504), (59.964200, 30.357014))
