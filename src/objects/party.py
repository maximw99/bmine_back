class Party:

    def __init__(self, name, vibe, speeches):
        self.name = name 
        self.vibe = vibe
        self.speeches = speeches


    # getter
    @property
    def name(self):
        return self._name	
    
    @property
    def vibe(self):
        return self._vibe	
    
    @property
    def speeches(self):
        return self._speeches	
    
    
    # setter
    @name.setter
    def name(self, value):
        self._name = value

    @vibe.setter
    def vibe(self, value):
        self._vibe = value

    @speeches.setter
    def speeches(self, value):
        self._speeches = value


    # to doc

    def to_document(self):
        doc = {"name": self._name, "vibe": self._vibe, "speeches": self._speeches}
        return doc

        