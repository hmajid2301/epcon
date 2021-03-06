
import urllib.request, urllib.parse, urllib.error
import http.client
import json

G = 'maps.google.com'

# FIXME: use this function or this one, but the code is in double assopy.utils.geocode
def geocode(address, key, country):  # pragma: no cover
    """
    Get the coordinates from Google Maps for a specified address
    """
    # see http://code.google.com/intl/it/apis/maps/documentation/geocoding/#GeocodingRequests
    params = {
        'q': address.encode('utf-8') if isinstance(address, str) else address,
        'key': key,
        'sensor': 'false',
        'output': 'json',
        'oe': 'utf8',
    }
    if country:
        params['gl'] = country

    url = '/maps/geo?' + urllib.parse.urlencode(list(params.items()))
    conn = http.client.HTTPConnection(G)
    try:
        conn.request('GET', url)
        r = conn.getresponse()
        if r.status == 200:
            return json.loads(r.read())
        else:
            return {'Status': {'code': r.status }}
    finally:
        conn.close()
