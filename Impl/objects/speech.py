class Speech:
    def __init__(self, id, speaker, content):
        self.id = id
        self.speaker = speaker
        self.content = content


    # getter
    @property
    def id(self):
        return self._id

    @property
    def speaker(self):
        return self._id

    @property
    def content(self):
        return self._id

    # setter
    @id.setter
    def id(self, value):
        self._id = value

    @speaker.setter
    def speaker(self, value):
        self._speaker = value

    @content.setter
    def content(self, value):
        self._content = value

