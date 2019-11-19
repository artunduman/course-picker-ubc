#!/usr/bin/env python
import argparse
import logging
import json

from courses_manager import CoursesManager
from courses_manager import CoursesManager
from course_parser import CourseParser
from session import Session

# logger = logging.get_logger('CoursePicker')

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--courses',
                        dest='courses',
                        required=True,
                        nargs='+',
                        help='Space separated course names, eg: CPSC310')

    parser.add_argument('--previous-terms',
                        dest='prev_terms',
                        type=int,
                        default=3,
                        help='Number of previous terms to check')

    parser.add_argument('--session',
                        dest='session',
                        default='2019W',
                        help='Current year session, default: 2019W')

    parser.add_argument('--term',
                        dest='term',
                        required=True,
                        type=int,
                        help='The term that you are willing to take the course')
    
    return parser.parse_args()


def run(args):
    current_session = Session(args.session)
    courses_manager = CoursesManager(args.courses, current_session, args.term)
    info = courses_manager.get_sections_info_json()
    # print(json.dumps(info, indent=4))
    


        

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    args = get_args()
    run(args)
    