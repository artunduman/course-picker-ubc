# USEFUL

import requests
import logging
import datetime

from coursepicker.utils.course_parser import CourseParser
from functools import lru_cache
from enum import Enum


class Weekdays(Enum):
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5


logger = logging.getLogger('CoursePicker')


class CoursesManager(object):
    def __init__(self, courses, config):
        self.config = config['courses-api']
        self.course_dict = self.parse_courses(courses)
        self.session = self.config['current_session']
        self.term = self.config['current_term']
        self.requests_session = requests.Session()

    def _parse_to_datetime(self, days, start, end):
        """
        :param days: string representing weekdays
        :param start: string of start hour
        :return: list of start datetime objects and timedelta of length (for the first week of 2001)
        """
        ret = []
        try:
            # These are just for delta
            start_time = datetime.datetime.strptime(start, '%H:%M')
            end_time = datetime.datetime.strptime(end, '%H:%M')
        except ValueError:
            logger.error("The dates start: {} end: {} don't match HH:MM")
            return
        delta = end_time - start_time
        for day in days:
            starts = start.strip().split(':')
            start_datetime = datetime.datetime(
                2001,
                1,
                getattr(Weekdays, day),
                int(starts[0]),
                int(starts[1])
            )
            ret.append(start_datetime)
        return ret, delta

    '''
    Returns list of (code, number) tuples
    '''
    def parse_courses(self, courses):
        course_dict = {}
        course_parser = CourseParser(courses)
        try:
            course_dict = course_parser.parse()
        except Exception as e:
            logger.error('Exception caught: {}'.format(e))
        return course_dict

    @lru_cache(1024)
    def _get_sections(self, course_code, course_number):
        url = "https://{}/{}/{}/{}".format(
            self.config['endpoint'],
            self.session,
            course_code,
            course_number
        )
        logger.info('Querying with url: {}'.format(url))
        resp = self.requests_session.get(url)
        if resp.status_code is not requests.codes.ok:
            msg = 'No course {}{} found in session {}'.format(course_code, course_number, self.session)
            logger.error('In get_sections resp.status_code: {}'.format(resp.status_code))
            raise Exception(msg)

        sections = {}
        if not resp:
            logger.debug('No response for querying sections')
        else:
            sections = resp.json()['sections']  # Buggy
        return sections

    def _normalize(self, prof_name):
        logger.debug('Normalizing name: {}'.format(prof_name))
        if ',' in prof_name:
            last, first = prof_name.split(',')
            last = last.strip().replace(' ', '-')
            first = first.strip().replace(' ', '-')
            return '{}-{}'.format(first, last).lower()
        else:
            return ''

    def _get_filtered_sections(self, course_code, course_number):
        """
        Filters out labs
        """
        sections = self._get_sections(course_code, course_number)
        filtered = [k for k in sections if k[0] != 'L']
        return filtered

    '''
    @param sections: list of section numbers to query
    '''
    @lru_cache(2048)
    def _get_section_info(self, course_code, course_number, section):
        url = "https://{}/{}/{}/{}/{}".format(
            self.config['endpoint'],
            self.session,
            course_code,
            course_number,
            section
        )

        logger.debug('Querying with URL: {}'.format(url))
        resp = self.requests_session.get(url)

        assert resp.status_code is requests.codes.ok
        if resp.status_code is not requests.codes.ok:
            logger.error('In get_section_prof, resp.status_code: {}'.format(resp.status_code))
        resp = resp.json()
        return (resp['instructors'][0], resp['start'], resp['end'], resp['days'], resp['activity'], resp['term'])

    '''
    Example return:
    <course_name>.<section>
    {
        'CPSC310': {
            '101': {
                'start': ,
                'end': '14:00',
                'prof': 'john-doe',
            }
        }
    }
    '''
    def get_sections_info_json(self):
        return_val = {}
        for code, numbers in self.course_dict.items():
            for number in numbers:
                course = '{}{}'.format(code, number)
                current_dict = {}
                sections = self._get_filtered_sections(code, number)
                for section in sections:
                    prof_name, start, end, days, activity, term = self._get_section_info(code, number, section)
                    prof_name = self._normalize(prof_name)
                    start_times, duration = self._parse_to_datetime(days, start, end)
                    section_info = {
                        'start': start_times,
                        'duration': duration,
                        'prof': prof_name
                    }
                    logger.debug('info: {} activity: {} term: {} will_add? {}'.format(
                        section_info,
                        activity,
                        term,
                        (activity == 'Lecture') and (term == self.term)
                    ))
                    if (activity == 'Lecture') and (term == self.term):
                        current_dict[section] = section_info
                return_val[course] = current_dict
        return return_val
