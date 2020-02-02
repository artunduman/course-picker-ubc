FROM python:3.7

RUN mkdir /opt/coursepicker/
WORKDIR /opt/coursepicker/

COPY requirements.txt requirements.txt
RUN pip3.7 install -r requirements.txt

COPY ./coursepicker /opt/coursepicker/coursepicker

CMD ['gunicorn', '-b', '127.0.0.1:5000', 'coursepicker.app:application']
