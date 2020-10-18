PY?=python3
WORKDIR?=.
VENVDIR?=$(WORKDIR)/.venv
REQUIREMENTS_TXT?=$(wildcard requirements*.txt)  # Multiple paths are supported (space separated)
MARKER=$(VENVDIR)/pyvenv.cfg


VENV=$(VENVDIR)/bin
MANAGEPY=$(VENV)/python manage.py

.PHONY: venv
venv: $(MARKER)

$(VENV):
	$(PY) -m venv $(VENVDIR)
	$(VENV)/python -m pip install --upgrade pip setuptools wheel

$(MARKER): $(REQUIREMENTS_TXT) | $(VENV)
	$(VENV)/python -m pip install $(foreach path,$(REQUIREMENTS_TXT),-r $(path)) --no-warn-script-location
	touch $(MARKER)


.PHONY: check
check: venv
	$(VENV)/python manage.py check

.PHONY: shell
shell: check
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

.PHONY: backup
backup:
	-rm -r remote
	scp -r cesar.local:/var/opt/recipes/ remote