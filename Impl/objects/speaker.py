class Speaker:
    def __init__(self, name, id, party):
        self.name = name
        self.id = id
        self.party = party


    # getter
    @property
    def name(self):
        return self._name
        
    @property
    def id(self):
        return self._id
    
    @property
    def party(self):
        return self._party
    

    # setter
    @name.setter
    def name(self, value):
        self._name = value

    @id.setter
    def id(self, value):
        self._id = value

    @party.setter
    def party(self, value):
        self._party = value