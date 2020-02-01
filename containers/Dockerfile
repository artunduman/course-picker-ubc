FROM python:3.7

RUN mkdir /opt/coursepicker/
WORKDIR /opt/coursepicker/

COPY requirements.txt requirements.txt
RUN pip3.7 install -r requirements.txt

COPY ./coursepicker /opt/coursepicker/coursepicker

