class Speech:
    def __init__(self, id, speaker, content, comments):
        self.id = id
        self.speaker = speaker
        self.content = content
        self.comments = comments

    def __init__(self):
        pass


    # getter

    @property
    def id(self):
        return self._id

    @property
    def speaker(self):
        return self._speaker

    @property
    def content(self):
        return self._content
    
    @property
    def comments(self):
        return self._comments

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

    @comments.setter
    def comments(self, value):
        self._comments = value

    # to doc

    def to_document(self):
        doc = {"_id": self._id, "speaker": None, "content": self._content, "comments": None}
        return doc

