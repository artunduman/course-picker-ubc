from coursepicker.database.database import Grade


def get_averages(profs, db_access):
    """
    Returns a dict of {profname: avg}
    """
    averages = {}
    for prof in profs:
        query = db_access.session.query(Grade).filter(Grade.professor == prof)  # TODO regex for multiple profs
        sm = 0
        total_students = 0
        for grade_entry in query.all():
            average, students = grade_entry.avg, grade_entry.enrolled
            sm += average * students
            total_students += students
        overall_avg = sm / total_students
        averages.update({prof: overall_avg})
    return averages
