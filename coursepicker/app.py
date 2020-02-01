import falcon
import logging
from coursepicker.handlers.v1 import CoursePickerV1Handler

from wsgiref import simple_server

logger = logging.getLogger('api')


class App(falcon.API):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        logger.info("API Server is starting")

        self.add_route("/v1", CoursePickerV1Handler())


application = App()

if __name__ == "__main__":
    httpd = simple_server.make_server("127.0.0.1", 5000, application)
    httpd.serve_forever()
