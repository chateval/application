FROM python:3
ADD . /
WORKDIR /
ADD requirements.txt /
RUN pip install -r requirements.txt