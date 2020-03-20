import itertools
import logging
from collections import namedtuple


logger = logging.getLogger('default')


class CourseSelector:

    def _overlap(self, range1, range2):
        pass # TODO

    def _check_validity(self, info_combination, sections):
        """
        :param info_combination:
        A subset of course_info
        :param sections:
        {'CPSC310': '102', 'MATH200': '101', 'CPSC221': '103'} One each
        :return:
        True if no overlap, false otherwise
        """
        date_ranges = []
        sum_avg = 0
        for course, section in sections.items():
            starts = info_combination[course][section]['start']
            duration = info_combination[course][section]['duration']
            sum_avg += info_combination[course][section]['average']
            date_ranges.append((starts, duration))
        avg = 0 if len(sections) == 0 else sum_avg/len(sections)
        # Naive algorithm to see if any two overlap
        i = 0
        n = len(date_ranges)
        valid = True
        while i < n:
            j = i + 1
            while j < n:
                if self._overlap(date_ranges[i], date_ranges[j]):
                    valid = False
                    break
                j += 1
            i += 1
        return valid, avg

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
        for info_combination in combined_list:
            # this is a simple mapping of key to list of sections
            # section_map: {CPSC310: [101, 102], CPSC221:[101,104]}
            section_map = {}
            for course_name in info_combination.keys():
                section_map.update({course_name: list(info_combination[course_name].keys())})
            product = self._product_dict(**section_map)

            max_avg = 0
            # entry: {'CPSC310': '102', 'CPSC221': '103'}
            for entry in product:
                valid, avg = self._check_validity(info_combination, entry)
                if not valid or avg == 0:
                    continue
                if max_avg < avg:
                    max_avg = avg
                    best_entry = entry

        return best_entry

            # TODO left here!
