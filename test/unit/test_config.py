from coursepicker.utils.config import get_config

import unittest


class CourseParserTest(unittest.TestCase):
    # Returns True or False.
    def test_get_config(self):
        config = get_config('local')
        assert config == {
            'database': {
                'host': 'localhost',
                'db_identifier': 'course-picker',
                'user': 'admin',
                'password': '12345'
            }
        }


if __name__ == '__main__':
    unittest.main()
