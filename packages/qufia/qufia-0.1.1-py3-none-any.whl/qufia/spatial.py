
from .models import Map, TreeList
from .trees import get_trees_by_plt_cn
import copy

def get_plot_grid(client, lng, lat, radius):

    path = '/spatial/center'

    params = {
        'lng': lng,
        'lat': lat,
        'radius': radius
    }

    resp = client.request(path, params)

    lut = resp['cnLookUp']
    idx_array = resp['idxArray']
    for i in lut.keys():
        cn = lut[i]
        lut[i] = get_trees_by_plt_cn(client, cn)

    plot_grid = []
    for i in idx_array:
        if i:
            plot_grid.append(copy.deepcopy(lut[str(i)]))
        else:
            plot_grid.append(TreeList())
    
    return Map(plot_grid, resp['meta'])
