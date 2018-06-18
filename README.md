# ChatEval
A scientific framework for evaluating chatbots. Scientific
paper available [here](https://github.com/chateval/ChatEval/blob/master/paper/Chatbot_Evaluation_Demo_2018_EMNLP.pdf).

## Dependencies
<<<<<<< HEAD
- [Django](https://www.djangoproject.com/)
- [Handlebars](https://handlebarsjs.com/) (Templating engine)
- [Bulma](https://bulma.io) (CSS framework) Database)

## Usage
0. Install [Django](https://www.djangoproject.com/)
1. Install Mysql using `pip install mysqlclient`.
2. Make migrations using `python manage.py createmigrations`. (Shows what the database models are)
3. Migrate using `python manage.py migrate`. (Adds the models to the database)
4. Run server using `python manage.py runserver`.
5. Access app at [localhost:8080](localhost:8080).

## Code Documentation
Documentation for the codebase is available in `/docs`.
=======
- Django
- Bulma (CSS framework)
- MySQL

## Usage
0. Install django using `pip install django` or `conda install django`.
2. Edit database information in `/chateval/settings.py`.
3. Run server migrations using `python manage.py makemigrations && python manage.py migrate`. (Note: `python3` might be required depending on your python installation)
4. Create `env.sh` containing
```
export DB_NAME=
export DB_USER=
export DB_PASSWORD=
export DB_HOST=
export DB_PORT=
```
and source using `source env.sh`.

5. Run server using `python manage.py runserver`
6. Access app at [localhost:8000](localhost:8000) and admin SQL page at [localhost:8000/admin](localhost:8000/admin).

## Code Documentation
Documentation for the codebase is available in `DOCUMENTATION.md`.
>>>>>>> 60469281e19c3bb3b3128f38b4b28419ed764137
