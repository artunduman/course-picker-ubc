from coursepicker.utils.course_parser import CourseParser

import unittest


class CourseParserTest(unittest.TestCase):

    def setUp(self):
        self.course_parser = CourseParser(['CPSC322', 'MATH200', 'MATH221'])

    # Returns True or False.
    def test_parse_courses(self):
        result = self.course_parser.parse()
        assert result == {
            'CPSC': ['322'],
            'MATH': ['200', '221']
        }


if __name__ == '__main__':
    unittest.main()
