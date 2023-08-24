class Comment:
    def __init__(self, content):
        self.content = content

    def __init__(self):
        pass


    # getter

    @property
    def content(self):
        return self._content

    # setter

    @content.setter
    def content(self, value):
        self._content = value

    # to doc
    
    def to_document(self):
        doc = {"content": self._content}
        return doc
