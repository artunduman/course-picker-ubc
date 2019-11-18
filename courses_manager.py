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
            self.session,
            course_code,
            course_number
        )
        resp = requests.get(url)
        if resp.status_code is not requests.codes.ok:
            raise Exception('No course {}{} found in session {}'.format(course_code, course_number, session))
            logger.error('In get_sections resp.status_code: {}'.format(resp.status_code))

        return resp.json()['sections']


    '''
    @param sections: list of section numbers to query
    '''
    def _get_section_prof(self, course_code, course_number, section):
        url = "https://{}/{}/{}/{}/{}".format(
            ENDPOINT,
            self.session,
            course_code,
            course_number
        )

        resp = requests.get(url)

        assert resp.status_code is requests.codes.ok
        if resp.status_code is not requests.codes.ok:
            logger.error('In get_section_prof, resp.status_code: {}'.format(resp.status_code))
        
        return resp.json()['instructors'][0]

    '''
    example response:
    [
        'CPSC310': {
            '101': 'DOE, JOHN'
            '102': 'DOE, JANE'
        }
    ]
    '''
    def get_sections_profs_json(self):
        return_val = []
        for code, number in self.course_list:
            course = '{}{}'.format(code, number)
            current_dict = {course: {}}
            sections = self._get_sections(code, number)
            for section in sections:
                prof_name = self._get_section_prof(code, number, sections)
                current_dict.append()

