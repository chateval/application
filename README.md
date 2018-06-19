# ChatEval
A scientific framework for evaluating chatbots. Scientific
paper available [here](https://github.com/chateval/ChatEval/blob/master/paper/Chatbot_Evaluation_Demo_2018_EMNLP.pdf).

## Dependencies
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
