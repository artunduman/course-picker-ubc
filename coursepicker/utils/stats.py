from coursepicker.database.database import Grade
from functools import lru_cache


def get_profs(courses):
    """
    :param courses: course names to query profs of
    :return: returns dict of {profname: {course: CPSC310, section:101}}
    """
    raise NotImplementedError()  # TODO


@lru_cache(1024)
def _get_prof(course, session):
    raise NotImplementedError()  # TODO


def enrich_averages(info, db_access):
    """
    Will enrich all the fields in main info dictionary
    with prof averages.
    """
    for course, sections in info.items():
        for section_number, meta in sections.items():
            prof = meta['prof']
            if not prof:
                continue
            grade_entries = db_access.get_grades_by_prof(prof)
            sm = 0
            total_students = 0
            for grade_entry in grade_entries:
                average, students = grade_entry.avg, grade_entry.enrolled
                sm += average * students
                total_students += students
            if total_students > 0:
                overall_avg = sm / total_students
            else:
                overall_avg = None
            meta.update({'average': overall_avg})
    return info
