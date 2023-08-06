
from .models import Map

def get_plot_map(client, lng, lat, radius):

    path = '/map/pntrad'

    params = {
        'lng': lng,
        'lat': lat,
        'radius': radius
    }

    resp = client.request(path, params)

    return Map(resp)