from coursepicker.utils.stats import enrich_averages, get_profs
from coursepicker.courses_manager import CoursesManager
import falcon
import json


class CoursePickerV1Handler:
    def __init__(self, config, database, course_selector):
        self.config = config
        self.db = database
        self.course_selector = course_selector

    def on_get(self, req, res):
        params = req.params
        courses = params.get('course', list())
        number_of_courses = params.get('howMany', 0)
        courses_manager = CoursesManager(courses, self.config)
        info = courses_manager.get_sections_info_json()
        info = enrich_averages(info, self.db)

        res.body = json.dumps(info)
        res.status = falcon.HTTP_200
