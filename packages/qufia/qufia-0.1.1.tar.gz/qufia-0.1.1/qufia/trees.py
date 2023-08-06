
from .models import TreeList

def search_trees(client, fields=None, where=None, limit=None, offset=None):

    path = '/trees'

    params = {
        'fields': fields,
        'where': where,
        'limit': limit,
        'offset': offset
    }

    resp = client.request(path, params)

    treelist = TreeList(resp)

    return treelist

def get_tree_by_cn(client, tree_cn):

    return search_trees(client, where=f'cn="{tree_cn}"') 

def get_trees_by_plt_cn(client, plt_cn):

    return search_trees(client, where=f'plt_cn="{plt_cn}"')
