# DEPRECATE

import requests

ENDPOINT = 'ubcgrades.com/api/grades'


class GradesManager(object):
    def __init__(self, info, terms_to_check, current_session):
        self.info_dict = info
        self.terms_to_check = terms_to_check
        self.current_session = current_session
        self.requests_session = requests.Session()

    def get_course_dist(self, session, course_code, course_number):
        url = 'https://{}/{}/{}/{}'.format(
            ENDPOINT,
            session,
            course_code,
            course_number
        )
        
        resp = self.requests_session.get(url)
        assert resp.status_code == requests.codes.ok

        return resp.json()

