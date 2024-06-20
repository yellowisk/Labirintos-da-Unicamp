class Maze():
    def __init__(self, id: int, name: str, background: str, path: list[list[int]]):
        self.id = id
        self.name = name
        self.background = background
        self.path = path
        
    def __repr__(self):
        return f'{self.name}'
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
        
    @property
    def background(self):
        return self._background
    
    @background.setter
    def background(self, background):
        self._background = background
        
    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, path):
        self._path = path