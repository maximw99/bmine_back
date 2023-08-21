class Party:
    def __init__(self, name, id):
        self.name = name 
        self.id = id

    def __init__(self):
        pass


    # getter
    @property
    def name(self):
        return self._name	
    
    @property
    def id(self):
        return self._id	
    

    # setter
    @name.setter
    def name(self, value):
        self._name = value

    @id.setter
    def id(self, value):
        self._id = value
        