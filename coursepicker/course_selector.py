import itertools
import logging
from collections import namedtuple


logger = logging.getLogger('default')


class CourseSelector:

    def _overlap(self, range_tuple_1, range_tuple_2):
        """
        Each of ranges is a tuple of (start_times, duration)
        :return: True if they overlap
        """
        start_1_list, duration_1 = range_tuple_1
        start_2_list, duration_2 = range_tuple_2
        if not isinstance(start_1_list, list) or not isinstance(start_2_list, list):
            raise TypeError('The given tuples should have a alist as first argument')

        for start_1 in start_1_list:
            for start_2 in start_2_list:
                end_1 = start_1 + duration_1
                end_2 = start_2 + duration_2
                if start_1 <= end_2 and start_2 <= end_1:
                    return True
        return False

    def _check_validity(self, info_combination, section_map):
        """
        :param info_combination:
        A subset of course_info
        :param section_map:
        {'CPSC310': '102', 'MATH200': '101', 'CPSC221': '103'} One each
        :return:
        True if no overlap, false otherwise
        """
        date_ranges = []
        sum_avg = 0
        for course, section in section_map.items():
            starts = info_combination[course][section]['start']
            duration = info_combination[course][section]['duration']
            sum_avg += info_combination[course][section]['average']
            date_ranges.append((starts, duration))
        avg = 0 if len(section_map) == 0 else sum_avg / len(section_map)
        # Naive algorithm to see if any two overlap
        i = 0
        n = len(date_ranges)
        while i < n:
            j = i + 1
            while j < n:
                if self._overlap(date_ranges[i], date_ranges[j]):
                    return False, avg
                j += 1
            i += 1
        return True, avg

    @staticmethod
    def _product_dict(**kwargs):
        keys = kwargs.keys()
        vals = list(kwargs.values())
        for instance in itertools.product(*vals):
            yield dict(zip(keys, instance))

    def select_by_average(self, course_info, number_of_sections_to_select):
        """
        At beta, brute forces all non-overlapping combinations and
        returns the best selection of courses in terms of averages of profs
        :param course_info:
        Can be generated by courses_manager
        {
            'CPSC310': {
                '101': {
                    'start': '12:30',
                    'end': '14:00',
                    'days': 'Tue Thu',
                    'prof': 'john-doe',
                    'section': '101'
                }
            }
        }
        :param number_of_sections_to_select:
        How many of these sections/courses I want to pick
        :return:
        List of tuples for selected courses and sections
        """
        combined_list = list(map(dict, itertools.combinations(course_info.items(), number_of_sections_to_select)))
        # This combination doesn't determine the sections, just the courses
        # info_combination = [{CPSC221: {stuff}, CPSC213: {stuff}}, ...]
        best_entry = None
        max_avg = 0
        for info_combination in combined_list:
            # this is a simple mapping of key to list of sections
            # section_map: {CPSC310: [101, 102], CPSC221:[101,104]}
            section_map = {}
            for course_name in info_combination.keys():
                section_map.update({course_name: list(info_combination[course_name].keys())})
            product = self._product_dict(**section_map)

            # entry: {'CPSC310': '102', 'CPSC221': '103'}
            for entry in product:
                valid, avg = self._check_validity(info_combination, entry)
                if not valid or avg == 0:
                    continue
                if max_avg < avg:
                    max_avg = avg
                    best_entry = entry

        return best_entry