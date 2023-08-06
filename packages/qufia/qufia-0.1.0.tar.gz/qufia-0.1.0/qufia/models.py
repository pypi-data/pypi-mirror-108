
class Tree:
    
    def __init__(self, fields, data):

        self.fields = [field.lower() for field in fields]

        for i in range(len(fields)):
            self.__dict__[fields[i].lower()] = data[i]
    
class TreeList:
    
    def __init__(self, resp):

        self.treelist = []

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
            

class Plot:
    pass

class Map:
    
    def __init__(self, resp):

        self.width = resp['meta']['width']
        self.height = resp['meta']['height']

        self.lut = resp['cnLookUp']
        self.idx_array = resp['idxArray']
    