class Daytopic:
    def __init__(self, nr ,speeches):
        self.nr = nr
        self.speeches = speeches

    def __init__(self):
        pass

    # getter

    @property
    def nr(self):
        return self._nr
    
    @property
    def speeches(self):
        return self._speeches

    # setter

    @nr.setter
    def nr(self, value):
        self._nr = value

    @speeches.setter
    def speeches(self, value):
        self._speeches = value
