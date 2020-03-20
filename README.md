# Course Picker UBC

A dockerized web API to optimize 

## Getting Started

To start the server locally, build and run the docker image
```
docker-compose run --rm coursepicker
```
### Prerequisites

You need docker installed on your machine

http://docs.docker.com/install/

### Installing

After running the service, you can try the endpoint (It will work once the big PR is merged)
```
curl -XGET hostname/v1?course=cpsc310&course=econ345
```

## Running the tests

```
docker-compose run --rm test
```

## Progress
Some more time and testing needed before the big PR is merged
and the functionality start working