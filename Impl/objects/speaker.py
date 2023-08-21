class Speaker:
    def __init__(self, id, firstname, lastname, title, bday, religion, jobs, party):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.title = title
        self.bday = bday
        self.religion = religion
        self.jobs = jobs
        self.party = party

    def __init__(self):
        pass


    # getter
    @property
    def id(self):
        return self._id
    
    @property
    def firstname(self):
        return self._firstname
    
    @property
    def lastname(self):
        return self._lastname
    
    @property
    def title(self):
        return self._title
    
    @property
    def bday(self):
        return self._bday
    
    @property
    def religion(self):
        return self._religion
    
    @property
    def jobs(self):
        return self._jobs
    
    @property
    def party(self):
        return self._party
    
    # setter
    @id.setter
    def id(self, value):
        self._id = value

    @firstname.setter
    def firstname(self, value):
        self._firstname = value

    @lastname.setter
    def lastname(self, value):
        self._lastname = value

    @title.setter
    def title(self, value):
        self._title = value

    @bday.setter
    def bday(self, value):
        self._bday = value

    @religion.setter
    def religion(self, value):
        self._religion = value

    @jobs.setter
    def jobs(self, value):
        self._jobs = value

    @party.setter
    def party(self, value):
        self._party = value
