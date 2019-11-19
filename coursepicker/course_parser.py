class CourseParser(object):
    def __init__(self, course_name):
        self.course_name = course_name
        self.course_name_length = 7
        self.course_code_length = 4

    '''
    Returns tuple (Course Code, Course Number)
    '''
    def parse(self):
        if len(self.course_name) is not self.course_name_length:
            raise Exception('Course name should be {} characters'.format(self.course_name_length))
        
        course_code = self.course_name[:self.course_code_length].upper()
        course_number = self.course_name[self.course_code_length:]

        if not course_code.isalpha() or not course_number.isdigit():
            raise Exception('Invalid course code or number: Code: {} Number: {}'.format(course_code, course_number))

        return (course_code, course_number)



