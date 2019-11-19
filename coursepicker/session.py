sessions = {
    'WINTER': 'W',
    'SUMMER': 'S'
}


class Session(object):
    def __init__(self, full_session):
        self._year = full_session[:4]
        self._term = full_session[4]

    '''
    eg: 2018W
    '''
    def get_full_session(self):
        return '{}{}'.format(self._year, self._term)

    def get_session_year(self):
        return self._year

    '''
    One of ['W', 'S']
    '''
    def get_session_term(self):
        return self._term

    def __add__(self, r):
        years = int(r/2)
        session_switch = abs(r)%2
        if session_switch is 1:
            term = sessions['WINTER'] if self.session == sessions['SUMMER'] else sessions['WINTER']
        self.current_year += years
        return self.get_year()

    def __sub__(self, r):
        return self.__add__(-r)
