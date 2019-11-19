import requests
import logging

from course_parser import CourseParser

logger = logging.getLogger('CoursePicker')

ENDPOINT = 'ubc-courses-api.herokuapp.com'

class CoursesManager(object):

    def __init__(self, courses, session, term):
        self.course_list = self.parse_courses(courses)
        self.session = session
        self.term = term
        self.requests_session = requests.Session()
    
    '''
    Returns list of (code, number) tuples
    '''
    def parse_courses(self, courses):
        course_list = []
        for course in courses:
            course_parser = CourseParser(course)
            try:
                course_list.append(course_parser.parse())
            except Exception as e:
                logger.error('Exception caught: {}'.format(e))
        return course_list


    def _get_sections(self, course_code, course_number):
        url = "https://{}/{}/{}/{}".format(
            ENDPOINT,
            self.session.get_full_session(),
            course_code,
            course_number
        )
        logger.info('Querying with url: {}'.format(url))
        resp = self.requests_session.get(url)
        if resp.status_code is not requests.codes.ok:
            msg = 'No course {}{} found in session {}'.format(course_code, course_number, self.session.get_full_session())
            raise Exception(msg)
            logger.error('In get_sections resp.status_code: {}'.format(resp.status_code))

        return resp.json()['sections']


    '''
    Filters out labs
    '''
    def _get_filtered_sections(self, course_code, course_number):
        sections = self._get_sections(course_code, course_number)
        filtered = [k for k in sections if k[0] != 'L']
        return filtered

    '''
    @param sections: list of section numbers to query
    '''
    def _get_section_info(self, course_code, course_number, section):
        url = "https://{}/{}/{}/{}/{}".format(
            ENDPOINT,
            self.session.get_full_session(),
            course_code,
            course_number,
            section
        )

        logger.info('Querying with URL: {}'.format(url))
        resp = self.requests_session.get(url)

        assert resp.status_code is requests.codes.ok
        if resp.status_code is not requests.codes.ok:
            logger.error('In get_section_prof, resp.status_code: {}'.format(resp.status_code))
        resp = resp.json()
        return (resp['instructors'][0], resp['start'], resp['end'], resp['days'], resp['activity'], resp['term'])

    '''
    Example response:
    <course_name>.<section>
    {
        'CPSC310': {
            '101': {
                'start': '12:30',
                'end': '14:00',
                'days': 'Tue Thu',
                'instructor': 'DOE, JOHN',
            }
        }
    }
    '''
    def get_sections_info_json(self):
        return_val = {}
        for code, number in self.course_list:
            course = '{}{}'.format(code, number)
            current_dict = {}
            sections = self._get_filtered_sections(code, number)
            for section in sections:
                prof_name, start, end, days, activity, term = self._get_section_info(code, number, section)
                section_info = {
                    'start': start,
                    'end': end,
                    'days': days,
                    'instructor': prof_name
                }
                if activity == 'Lecture' and int(term) == self.term:
                    current_dict[section] = section_info
            return_val[course] = current_dict
        return return_val

