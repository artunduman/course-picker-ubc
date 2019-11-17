#!/usr/bin/env python
import argparse

from courses_manager import CoursesManager

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--courses',
                        dest='courses',
                        required=True,
                        help='Space separated course names')
    
    return parser.parse_args()

def run_server(args):
    courses_manager = CoursesManager()
    courses = args.courses
    for course in courses:
        resp = courses_manager.get_course()



if __name__ == "__main__":
    args = get_args()
    run_server(args)
    