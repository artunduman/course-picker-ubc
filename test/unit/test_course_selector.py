from coursepicker.course_selector import CourseSelector

import unittest


class CourseSelectorTest(unittest.TestCase):

    def setUp(self):
        self.course_selector = CourseSelector()

    def test_dummy(self):
        course_info = {
            'CPSC310': {
                '101': {
                    'start': '12:30',
                    'end': '14:00',
                    'days': 'Tue Thu',
                    'prof': 'john-doe',
                    'average': 88.0,
                },
                '102': {
                    'start': '14:00',
                    'end': '15:30',
                    'days': 'Tue Thu',
                    'prof': 'jane-doe',
                    'average': 89.0,
                }
            },
            'CPSC221': {
                '103': {
                    'start': '14:00',
                    'end': '15:30',
                    'days': 'Tue Thu',
                    'prof': 'jenny-doe',
                    'average': 82.0,
                }
            },
            'MATH200': {
                '101': {
                    'start': '14:00',
                    'end': '15:30',
                    'days': 'Tue Thu',
                    'prof': 'jenny-doe',
                    'average': 81.0,
                }
            }
        }
        import pdb; pdb.set_trace()
        self.course_selector.select_by_average(course_info, 2)
        assert True

    def test_product_dict(self):
        pass # TODO

    # Returns True or False.
    def test_select_courses_simple_overlap(self):
        course_info = {
            'CPSC310': {
                '101': {
                    'start': '12:30',
                    'end': '14:00',
                    'days': 'Tue Thu',
                    'prof': 'john-doe',
                    'average': 88.0,
                },
            },
            'CPSC221': {
                '102': {
                    'start': '12:30',
                    'end': '14:00',
                    'days': 'Tue Thu',
                    'prof': 'john-doe',
                    'average': 89.0,
                }
            }
        }

        result = self.course_selector.select_by_average(course_info, 1)
        assert result == [('CPSC221', '102')]

    def test_select_courses_no_possible_combination(self):
        course_info = {
            'CPSC310': {
                '101': {
                    'start': '12:30',
                    'end': '14:00',
                    'days': 'Tue Thu',
                    'prof': 'john-doe',
                    'average': 88.0,
                },
                '102': {
                    'start': '12:30',
                    'end': '14:00',
                    'days': 'Tue Thu',
                    'prof': 'john-doe',
                    'average': 89.0,
                }
            }
        }
        result = self.course_selector.select_by_average(course_info, 2)
        assert result == []


    def test_select_courses_optimize_average(self):
        course_info = {
            'CPSC310': {
                '101': {
                    'start': '12:30',
                    'end': '14:00',
                    'days': 'Tue Thu',
                    'prof': 'john-doe',
                    'average': 88.0,
                },
                '102': {
                    'start': '14:00',
                    'end': '15:30',
                    'days': 'Tue Thu',
                    'prof': 'jane-doe',
                    'average': 89.0,
                }
            },
            'CPSC221': {
                '103': {
                    'start': '14:00',
                    'end': '15:30',
                    'days': 'Tue Thu',
                    'prof': 'jenny-doe',
                    'average': 82.0,
                }
            }
        }
        result = self.course_selector.select_by_average(course_info, 2)
        # TODO # assert result ==

if __name__ == '__main__':
    unittest.main()
