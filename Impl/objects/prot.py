class Prot:
    def __init__(self, date, begin, end, nr, period, daytopics):
        self.date = date
        self.begin = begin
        self.end = end
        self.nr = nr
        self.period = period
        self.daytopics = daytopics

    def __init__(self):
        pass

    # getter

    @property
    def date(self):
        return self._date

    @property
    def begin(self):
        return self._begin

    @property
    def end(self):
        return self._end
    
    @property
    def nr(self):
        return self._nr

    @property
    def period(self):
        return self._period
    
    @property
    def daytopics(self):
        return self._daytopics

    # setter

    @date.setter
    def date(self, value):
        self._date = value

    @begin.setter
    def begin(self, value):
        self._begin = value

    @end.setter
    def end(self, value):
        self._end = value

    @nr.setter
    def nr(self, value):
        self._nr = value

    @period.setter
    def period(self, value):
        self._period = value

    @daytopics.setter
    def daytopics(self, value):
        self._daytopics = value
