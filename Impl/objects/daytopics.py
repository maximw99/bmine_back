class Daytopic:
    def __init__(self, nr ,speeches, topic):
        self.nr = nr
        self.speeches = speeches
        self.topic = topic

    def __init__(self):
        pass

    # getter

    @property
    def nr(self):
        return self._nr
    
    @property
    def speeches(self):
        return self._speeches
    
    @property
    def topic(self):
        return self._topic

    # setter

    @nr.setter
    def nr(self, value):
        self._nr = value

    @speeches.setter
    def speeches(self, value):
        self._speeches = value

    @speeches.setter
    def topic(self, value):
        self._topic = value

    # to doc

    def to_document(self):
        doc = {"_id": self._nr, "speeches": None, "topic": self._topic}
        return doc
