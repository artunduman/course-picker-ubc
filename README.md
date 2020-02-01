# CoursePickerUBC

This is a Dockerized web API to make course selection easier for UBC students. 

# API
GET hostname/v1?course=cpsc310&course=econ345

# Progress
MVP: API takes in a list of courses with an HTTP GET and returns a JSON of sections with highest historically average profs

# Next steps: 
- Non-overlapping courses
- Selection among many courses (3 out of 5 given etc.)