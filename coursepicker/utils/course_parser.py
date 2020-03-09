# USEFUL
import logging

logger = logging.getLogger('course-parser')


class CourseParser(object):
    def __init__(self, course_names):
        self.course_names = course_names
        self.course_name_length = 7
        self.course_code_length = 4

    def _parse_course(self, course_name):
        logger.info('Parsing course: {}'.format(course_name))
        if len(course_name) is not self.course_name_length:
            raise Exception('Course name should be {} characters, found {}'.format(
                self.course_name_length,
                course_name
            ))
        
        course_code = course_name[:self.course_code_length].upper()
        course_number = course_name[self.course_code_length:]

        if not course_code.isalpha() or not course_number.isdigit():
            raise Exception('Invalid course code or number: Code: {} Number: {}'.format(course_code, course_number))

        return course_code, course_number

    def parse(self):
        """
        Parser that returns a dictionary of course code lists per course subject
        example:
        {
            'CPSC': ['310', '213'],
            'MATH': ['221']
        }
        :return:
        """
        courses = dict()
        for course_name in self.course_names:
            course_name, course_code = self._parse_course(course_name)
            courses.setdefault(course_name, []).append(course_code)

        return courses
