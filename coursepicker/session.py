sessions = {
    'WINTER': 'W',
    'SUMMER': 'S'
}


class Session(object):
    def __init__(self, full_session):
        assert len(full_session) == 5
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
        term = self._term
        if session_switch is 1:
            if self._term == sessions['SUMMER']:
                term = sessions['WINTER']
            else:
                term = sessions['SUMMER']
                years += 1
        new_year = int(self._year) + years
        return '{}{}'.format(new_year, term)

    def __sub__(self, r):
        return self.__add__(-r)
