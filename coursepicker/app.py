import falcon
import logging
from coursepicker.handlers.v1 import CoursePickerV1Handler
from coursepicker.database.database import DatabaseAccess
from coursepicker.utils.config import get_config
from coursepicker.course_selector import CourseSelector
from wsgiref import simple_server

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('api')
env = 'prod'  # TODO make configurable


class App(falcon.API):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        config = get_config(env)
        db = DatabaseAccess(config)
        db.init_session()
        course_selector = CourseSelector()
        logger.info("API Server is starting")
        self.add_route("/v1", CoursePickerV1Handler(config, db, course_selector))


application = App()


if __name__ == "__main__":
    httpd = simple_server.make_server("127.0.0.1", 5000, application)  # no cover
    httpd.serve_forever()
