# ChatEval
A scientific framework for evaluating chatbots.

## Dependencies
- Django
- Bulma (CSS framework)
- MySQL

## Usage
0. Install django using `pip install django` or `conda install django`.
2. Edit database information in `/chateval/settings.py`.
3. Run server migrations using `python manage.py makemigrations && python manage.py migrate`. (Note: `python3` might be required depending on your python installation)
4. Run server using `python manage.py runserver`
5. Access app at [localhost:8000](localhost:8000) and admin SQL page at [localhost:8000/admin](localhost:8000/admin).

## Code Documentation
Documentation for the codebase is available in `DOCUMENTATION.md`.
