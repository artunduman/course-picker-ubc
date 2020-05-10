from coursepicker.utils.config import get_config

import unittest


class CourseParserTest(unittest.TestCase):
    # Returns True or False.
    def test_get_config(self):
        config = get_config('local')
        assert config == {
            'database': {
                'host': 'coursepickerubc_db_1:5432',
                'db_identifier': 'postgres',
                'user': 'postgres',
                'password': 'example'
            },
            'courses-api': {
                'endpoint': 'ubc-courses-api.herokuapp.com'
            }
        }


if __name__ == '__main__':
    unittest.main()
