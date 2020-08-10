from django.http.request import QueryDict
from django.db.models import Q

__author__ = 'Teeh Amaral'


class FilterGET(object):
    search_fields = None
    request = None

    def __init__(self, request, search_fields=[]):
        self.search_fields = search_fields
        self.request = request

    def search(self, query):
        entry_query = self.get_query(query, self.search_fields)
        return entry_query

    def get_query(self, query_string, search_fields):
        query = None
        terms = query_string[0].split('+')
        for term in terms:
            or_query = None
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query

        return query

    def getQuerySet(self):
        q = QueryDict(self.request.META["QUERY_STRING"], mutable=True)
        search_list = Q()
        if q.__contains__('q'):
            search_list = self.search(q.pop('q'))

        return search_list


def getDestinationLatLong(lat, lng, distance):
    from math import cos, sin, atan2, radians, degrees, asin

    '''returns the lat an long of destination point
    given the start lat, long, aziuth, and distance'''
    R = 6378.1  # Radius of the Earth in km
    brng = radians(360)  # Bearing is degrees converted to radians.
    d = distance / 1000  # Distance m converted to km

    lat1 = radians(lat)  # Current dd lat point converted to radians
    lon1 = radians(lng)  # Current dd long point converted to radians

    lat2 = asin(sin(lat1) * cos(d / R) + cos(lat1) * sin(d / R) * cos(brng))

    lon2 = lon1 + atan2(sin(brng) * sin(d / R) * cos(lat1),
                        cos(d / R) - sin(lat1) * sin(lat2))

    # convert back to degrees
    lat2 = degrees(lat2)
    lon2 = degrees(lon2)

    round_number = 1

    return [round(lat2, round_number), round(lon2, round_number)]


def getPathLength(lat1, lng1, lat2, lng2):
    from math import cos, sin, atan2, sqrt, radians

    '''calculates the distance between two lat, long coordinate pairs'''
    R = 6371000  # radius of earth in m
    lat1rads = radians(lat1)
    lat2rads = radians(lat2)
    deltaLat = radians((lat2 - lat1))
    deltaLng = radians((lng2 - lng1))
    a = sin(deltaLat / 2) * sin(deltaLat / 2) + cos(lat1rads) * cos(lat2rads) * sin(deltaLng / 2) * sin(deltaLng / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = R * c

    return d
