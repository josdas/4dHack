import googlemaps
from googlemaps.distance_matrix import distance_matrix
from googlemaps.places import places as GooglePlace
from googlemaps.places import places_photo as GooglePlacePhoto
from googlemaps.directions import directions as GoogleDirections
import place
from functools import lru_cache

GOOGLE_API_KEY_PLACES = 'AIzaSyB9M7xrpriW3xLs7Ml9lVmWpVctXQJJ50I'  # 'AIzaSyDKGWd0jRVivr0pE3qDbB2byuqUslp5O_k'
GOOGLE_API_KEY_DISTANCE = 'AIzaSyAPj-Ve1KeGZJLDxOfDXhsS9dzpYECWCU4' #'AIzaSyAkThybQY1wmBGHSKH96nrUkaBKQcMyrxc'# 'AIzaSyC4jSZqis47UqaA4Uahfxh8QwnKSJi0vhc' #'AIzaSyAYIsrbLSd5vLMuOqJpelFgi6N04qk9hEo' #   #   #
GOOGLE_API_KEY_DIRECTIONS = 'AIzaSyDHsLvj8Oyo0pElWFEfq7XLlmu1JS-O4Rg'


class GMap:
    """Map is a cover on goolge maps"""

    def __init__(self):
        if not hasattr(GMap, 'instance'):
            GMap.instance = True
            GMap.gmaps_places = googlemaps.Client(key=GOOGLE_API_KEY_PLACES)
            GMap.gmaps_distance = googlemaps.Client(key=GOOGLE_API_KEY_DISTANCE)
            GMap.gmaps_directions = googlemaps.Client(key=GOOGLE_API_KEY_DIRECTIONS)
        else:
            self.gmaps_places = GMap.gmaps_places
            self.gmaps_distance = GMap.gmaps_distance
            self.gmaps_directions = GMap.gmaps_directions

    @lru_cache(maxsize=None)
    def get_duration(self, first_point, second_point, transit_mode='transit'):
        """
        Result is a distance between two points with selected transit_mode
        transit_mode in {transit, walking}
        """
        request = distance_matrix(self.gmaps_distance, first_point, second_point,
                                  mode=transit_mode,
                                  language='ru')
        elements = request['rows'][0]['elements'][0]
        if elements['status'] != 'OK':
            return None
        duration = elements['duration']['value']
        return duration // 60

    @lru_cache(maxsize=128)
    def get_places(self, place_name, location, radius=2000, min_price=None, max_price=None):
        def get_price_level(money):
            if money > 1500:
                return 3
            elif money > 600:
                return 2
            elif money > 200:
                return 1
            return 0

        if max_price is not None:
            max_price = get_price_level(max_price)
        if min_price is not None:
            min_price = get_price_level(min_price)

        request = GooglePlace(self.gmaps_places, place_name,
                              radius=radius,
                              # min_price=min_price,  # it is bug
                              # max_price=max_price,
                              # open_now=True,
                              location=location,
                              language='ru')
        if request['status'] != 'OK':
            return []
        elements = request['results']
        places = []
        for element in elements:
            name = element['name']
            position_lat_lng = element['geometry']['location']
            position = position_lat_lng['lat'], position_lat_lng['lng']
            info = {}
            for label in ['types', 'rating', 'address']:
                if label in element:
                    info[label] = element[label]
            info['type'] = place_name
            """if element.get('photos', []):
               reference = element['photos'][0]['photo_reference']
               photo = GooglePlacePhoto(self.gmaps_places, reference, max_height=200, max_width=200)
               print(photo)
               pass"""
            places.append(place.Place(name, position, info))
        return places

    @lru_cache(maxsize=128)
    def get_position_from_name(self, place_name, location):
        places = self.get_places(place_name=place_name + ", Санкт-Петербург",
                                 location=location,
                                 radius=10000)
        return places[0].position


if __name__ == '__main__':
    gmap = GMap()
    print(gmap.get_directions((59.974597, 30.336504), (59.964200, 30.357014)))
    print(gmap.get_places('restaurant'))
    assert gmap.get_duration('new york', 'chicago') == 44268
    gmap.get_duration((59.974597, 30.336504), (59.964200, 30.357014))
