class Party:
    def __init__(self, name):
        self.name = name 

    def __init__(self):
        pass


    # getter
    @property
    def name(self):
        return self._name	
    
    # setter
    @name.setter
    def name(self, value):
        self._name = value

    # to doc

    def to_document(self):
        doc = {"name": self._name}
        return doc

        