FROM python:3
ADD . /
WORKDIR /
ADD requirements.txt /
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "chateval.wsgi"]