PY?=python3
WORKDIR?=.
VENVDIR?=$(WORKDIR)/.venv
REQUIREMENTS_TXT?=$(wildcard requirements-dev.txt)  # Multiple paths are supported (space separated)
MARKER=$(VENVDIR)/pyvenv.cfg


VENV=$(VENVDIR)/bin
MANAGEPY=$(VENV)/python manage.py

.PHONY: venv
venv: $(MARKER)

$(VENV):
	$(PY) -m venv $(VENVDIR)
	$(VENV)/python -m pip install --upgrade pip setuptools wheel

$(MARKER): $(REQUIREMENTS_TXT) | $(VENV)
	$(VENV)/python -m pip install -r $(REQUIREMENTS_TXT) --no-warn-script-location
	touch $(MARKER)


.PHONY: check
check: venv
	$(VENV)/python manage.py check

.PHONY: django-shell
django-shell: check
	$(VENV)/python manage.py shell

.PHONY: runserver
runserver: venv
	$(VENV)/python manage.py runserver

.PHONY: makemigrations
makemigrations: check
	$(VENV)/python manage.py makemigrations

.PHONY: test
test: check
	$(VENV)/python manage.py test

.PHONY: migrate
migrate: makemigrations
	$(VENV)/python manage.py migrate