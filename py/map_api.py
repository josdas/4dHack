import googlemaps
from googlemaps.distance_matrix import distance_matrix
from googlemaps.places import places as GooglePlace
import place

GOOGLE_API_KEY = 'AIzaSyDKGWd0jRVivr0pE3qDbB2byuqUslp5O_k'


class GMap:
    """Map is a cover on goolge maps"""

    def __init__(self, api_key):
        self.api_key = api_key
        self.gmaps = googlemaps.Client(key=api_key)

    def get_duration(self, first_point, second_point, transit_mode='transit'):
        """
        Result is a distance between two points with selected transit_mode
        transit_mode in {transit, walking}
        """
        request = distance_matrix(self.gmaps, first_point, second_point,
                                  transit_mode=transit_mode,
                                  language='english')
        elements = request['rows'][0]['elements'][0]
        if elements['status'] != 'OK':
            return None
        duration = elements['duration']['value']
        return duration

    def get_places(self, place_name, location=None, radius=None, min_price=None, max_price=None):
        request = GooglePlace(self.gmaps, place_name,
                              radius=radius,
                              min_price=min_price,
                              max_price=max_price,
                              open_now=True,
                              location=location,
                              language='english')
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
            }
            places.append(place.Place(name, position, info))
        return places


if __name__ == '__main__':
    gmap = GMap(GOOGLE_API_KEY)
    temp = gmap.get_places('restaurant')

    assert gmap.get_duration('new york', 'chicago') == 44268
    gmap.get_duration((59.974597, 30.336504), (59.964200, 30.357014))
