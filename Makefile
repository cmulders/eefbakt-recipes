.PHONY: check runserver makemigrations migrate

check:
	.venv/bin/python manage.py check

runserver: check
	.venv/bin/python manage.py runserver

makemigrations: check
	.venv/bin/python manage.py makemigrations

migrate: makemigrations
	.venv/bin/python manage.py migrate