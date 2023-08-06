
import requests

class Client:

    def __init__(self, key=''):

        self.key = key
        self._base_url = 'https://api.qufia.com'

        resp = requests.get(self._base_url + '/keys/' + key)
        if not resp.json():
            print('Not authorized/invalid API key')
            exit()

    def request(self, path, params):

        params['key'] = self.key
        resp = requests.get(self._base_url + path, params=params)

        if resp.status_code == requests.codes.ok:
            return resp.json()
        else:
            resp.raise_for_status()

from qufia.trees import get_tree_by_cn
from qufia.trees import get_trees_by_plt_cn
from qufia.spatial import get_plot_grid

Client.get_tree_by_cn = get_tree_by_cn
Client.get_trees_by_plt_cn = get_trees_by_plt_cn
Client.get_plot_grid = get_plot_grid

