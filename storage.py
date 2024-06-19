class Objetos():
    def __init__(self, id, nome, img, inventory_id):
        self._id = id
        self._nome = nome
        self._img = img
        self._inventory_id = inventory_id

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id    

    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, nome):
        self.nome = nome

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

    
class Inventario():
    def __init__(self, id, lista, status):
        self._id = id
        self._lista = lista
        self._status = status
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id

    @property
    def lista(self):
        return self._lista
    
    @lista.setter
    def lista(self, lista):
        self._lista = lista

    @property
    def status(self):
        return self._status
    
    @status.setter
    def lista(self, status):
        self._status = status

    def change_status(self):
        if self._status == 0:
            self._status = 1
        else:
            self._status = 0

    def add_obj(self, objeto: Objetos):
        if objeto._id in self._lista:
            return
        else:
            self._lista.append(objeto)

    def rem_obj(self, obj):
        if obj not in self._lista:
            return
        else:
            for i in self._lista:
                if obj.id == i.id:
                    self._lista.remove(i)
    