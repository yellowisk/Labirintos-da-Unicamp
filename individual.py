from storage import Inventory

class Individual():
    def __init__(self, id: int, name: str, position: tuple, imgs: list[str], maze_id: int):
        self.id = id
        self.name = name
        self.position = position
        self.imgs = imgs
        self.maze_id = maze_id

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
    def position(self):
        return self._position
    
    @position.setter
    def position(self, position):
        self._position = position
        
    @property
    def imgs(self):
        return self._imgs
    
    @imgs.setter
    def imgs(self, imgs):
        self._imgs = imgs
        
    @property
    def maze_id(self):
        return self._maze_id
    
    @maze_id.setter
    def maze_id(self, maze_id):
        self._maze_id = maze_id
        
    def move(self, x, y):
        self.position = (self.position[0] + x, self.position[1] + y)
        
    def is_near(self, someone_else):
        return abs(self.position[0] - someone_else.position[0]) <= 1 and abs(self.position[1] - someone_else.position[1]) <= 1
    
class Player(Individual):
    def __init__(self, id: int, name: str, position: tuple, imgs: list[str], maze_id: int,
                 ind_id: int):
        super().__init__(ind_id, name, position, imgs, maze_id)
        self.id = id
        self.lives = 3
        self.time = 0
        self.points = 0
        
    def __repr__(self):
        return f'{self.name}'
        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id
        
    @property
    def time(self):
        return self._time
    
    @time.setter
    def time(self, time):
        self._time = time
        
    @property
    def lives(self):
        return self._lives
    
    @lives.setter
    def lives(self, lives):
        self._lives = lives
        
    @property
    def points(self):
        return self._points
    
    @points.setter
    def points(self, points):
        self._points = points
        
    def is_alive(self):
        return self.lives > 0
    
class Colleague(Individual):
    def __init__(self, id: int, name: str, position: tuple, imgs: list[str], maze_id: int, ind_id: int):
        super().__init__(ind_id, name, position, imgs, maze_id)
        self.id = id
        self.is_statue = 0
        
    def __repr__(self):
        return f'{self.name}'
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id
    
    @property
    def is_statue(self):
        return self._is_statue
    
    @is_statue.setter
    def is_statue(self, is_statue):
        self._is_statue = is_statue
        
    def to_statue(self):
        self.is_statue = 1
    
class Enemy(Individual):
    def __init__(self, id: int, speed: int, name: str, position: tuple, imgs: list[str], maze_id: int, ind_id: int):
        super().__init__(ind_id, name, position, imgs, maze_id)
        self.id = id
        self.speed = speed
        
    def __repr__(self):
        return f'{self.name}'
        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id
    
    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, speed):
        self._speed = speed