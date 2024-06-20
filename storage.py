class Object():
    def __init__(self, id, name, img, inventory_id):
        self._id = id
        self._name = name
        self._img = img
        self._inventory_id = inventory_id
   
    def __repr__(self) -> str:
        return f'{self._name}'

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
        self.name = name

    @property
    def img(self):
        return self._img
    
    @img.setter
    def img(self, img):
        self._img = img

    @property
    def inventory_id(self):
        return self._inventory_id
    
    @inventory_id.setter
    def inventory_id(self, id):
        self._inventory_id = id

    
class Inventory():
    def __init__(self, id: int, objects: list, status: int):
        self._id = id
        self._objects = objects
        self._status = status
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id

    @property
    def objects(self):
        return self._objects
    
    @objects.setter
    def objects(self, objects):
        self._objects = objects

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, status):
        self._status = status
            
    def is_open(self):
        return self._status == 1
    
    def open(self):
        self.status = 1
        
    def close(self):
        self.status = 0

    def add_obj(self, object: Object):
        if object._id in self._objects:
            print('Object already in inventory')
        else:
            self._objects.append(object)

    def rem_obj(self, obj):
        if obj not in self._objects:
            return
        else:
            for i in self._objects:
                if obj.id == i.id:
                    self._objects.remove(i)
    