# ChatEval
A scientific framework for evaluating neural open domain chatbots.

## Dependencies
- Django (web framework)
- Bulma (CSS framework)
- MySQL (database)
- Amazon S3 (Dataset storage)
- Magnitude (word embedding format)

## Usage
### (Optional) Docker Installation
ChatEval supports the use of Docker as both a development and deployment tool.

0. Install [Docker](https://docker.com/).
1. Configure environment variables in `Dockerfile` by adding `ENV variable value` for each environment variable.
2. Build Docker image by using `docker build -t chateval .` (this may take some time).
3. Run ChatEval on port 8000 by using `docker run chateval`
4. Access app at [localhost:8000](localhost:8000) and admin SQL page at [localhost:8000/admin](localhost:8000/admin).
5. Run the [evaluation microservice](https://github.com/chateval/evaluation) at localhost:8001.

### Running `application`
ChatEval's primary microservice is `application`, which handles our Django back-end and SQL database. To run this:

0. Install dependencies using `pip install -r requirements.txt`.
2. Edit database information in `/chateval/settings.py`.
3. Run server migrations using `python manage.py makemigrations && python manage.py migrate`.
4. Create an `env.sh` (and source using `source env.sh`) containing:
```
export DB_NAME=
export DB_USER=
export DB_PASSWORD=
export DB_HOST=
export DB_PORT=
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_STORAGE_BUCKET_NAME=
export EMAIL_PASSWORD=
export EVAL_LOCATION=
```
5. Run server using `python manage.py runserver`
6. Download `.magnitude` word embeddings from [here](http://magnitude.plasticity.ai/word2vec/GoogleNews-vectors-negative300.magnitude) and place the vectors in `/eval/scripts/files/google_news.magnitude`.
7. Populate database using `python manage.py loaddata init.json`.
8. Access app at [localhost:8000](localhost:8000) and admin SQL page at [localhost:8000/admin](localhost:8000/admin).

### Running `evaluation`
ChatEval's evaluation microservice is available [here](https://github.com/chateval/evaluation) and handles the evaluation of  models to abstract Mechanical Turk interactions and to offload computation for loading/querying word embeddings. The location for this API is configurable as an environment variable named `EVAL_LOCATION` and is defaulted to [localhost:8001](localhost:8001). Note the location must be configured for both `application` and `evaluation`.
