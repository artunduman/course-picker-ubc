from coursepicker.utils.stats import get_averages
import falcon
import json


class CoursePickerV1Handler:
    def __init__(self, database):
        self.db = database

    def on_get(self, req, res):
        averages = get_averages(['katie-marshall'], self.db)  # TODO fix hardcode
        res.body = json.dumps(averages)
        res.status = falcon.HTTP_200
