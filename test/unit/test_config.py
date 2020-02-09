from coursepicker.config import get_config

import unittest


class CourseParserTest(unittest.TestCase):
    # Returns True or False.
    def test_get_config(self):
        config = get_config('/opt/coursepicker/test/unit/utils/test_config.ini')
        assert config._sections == {
            'database': {
                'host': 'localhost',
                'db_identifier': 'course-picker',
                'user': 'admin',
                'password': '12345'
            },
            'auth': {
                'client': 'ubc-course-picker'
            }
        }


if __name__ == '__main__':
    unittest.main()
