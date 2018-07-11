FROM python:3
ADD . /
ENV DB_NAME new
ENV DB_USER developers
ENV DB_PASSWORD JqrQV0S9dZusXQ
ENV DB_HOST 35.237.91.101
ENV DB_PORT 3306
ENV AWS_ACCESS_KEY_ID AKIAIHKL4NTJYOJ2RXSA
ENV AWS_SECRET_ACCESS_KEY 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
ENV AWS_STORAGE_BUCKET_NAME chateval-models
RUN pip install -r requirements.txt
WORKDIR /eval/scripts/file
RUN wget http://magnitude.plasticity.ai/glove/glove.6B.50d.magnitude && mv glove.6B.50d.magnitude vectors.magnitude
WORKDIR /
CMD [ 'python', 'manage.py', 'runserver', '0.0.0.0:8000' ]