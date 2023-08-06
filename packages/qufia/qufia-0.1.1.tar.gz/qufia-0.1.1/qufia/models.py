
class Tree:

    def __init__(self, fields, data):

        self.fields = [field.lower() for field in fields]

        for i in range(len(fields)):
            self.__dict__[fields[i].lower()] = data[i]


class TreeList:

    def __init__(self, resp=None):

        self.treelist = []

        if resp:
            fields = resp['results']['fields']
            data = resp['results']['data']

            for i in range(len(data)):
                tree = Tree(fields, data[i])
                self.treelist.append(tree)

    def __getitem__(self, idx):

        return self.treelist[idx]

    def __len__(self):

        return len(self.treelist)

    def __iter__(self):

        self.n = 0
        return self

    def __next__(self):

        if self.n < self.__len__():
            result = self.treelist[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration


class Map:

    def __init__(self, plot_grid, meta):

        self.grid = plot_grid

        self.shape = (meta['height'], meta['width'])
        self.location = (meta['longitude'], meta['latitude'])
        self.transform = meta['transform']
    
    def __getitem__(self, tup):

        i, j = tup
        return self.grid[i*self.shape[0] + j]
