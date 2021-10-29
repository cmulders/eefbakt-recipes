PY?=python3
WORKDIR?=.
VENVDIR?=$(WORKDIR)/.venv
REQUIREMENTS_TXT?=$(wildcard requirements*.txt)  # Multiple paths are supported (space separated)
MARKER=$(VENVDIR)/pyvenv.cfg

ICLOUD_DIR = $(HOME)/Library/Mobile\ Documents/com\~apple\~CloudDocs/Recepten-site
VENV=$(VENVDIR)/bin
MANAGEPY=$(VENV)/python manage.py

.PHONY: venv
venv: $(MARKER)

$(VENV):
	$(PY) -m venv $(VENVDIR)
	$(VENV)/python -m pip install --upgrade pip setuptools wheel

$(MARKER): $(REQUIREMENTS_TXT) | $(VENV)
	$(VENV)/python -m pip install $(foreach path,$(REQUIREMENTS_TXT),-r $(path)) --no-warn-script-location --upgrade
	touch $(MARKER)

.PHONY: upgrade
upgrade: $(REQUIREMENTS_TXT) | $(VENV)
	touch $(REQUIREMENTS_TXT)
	$(MAKE) venv

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
	rsync -rt -h --delete --progress 192.168.178.17:/var/opt/recipes/ remote

.PHONY: restore
restore:
	rsync remote/db.sqlite3 db.sqlite3
	rsync -rt -h --delete remote/media/ media

.PHONY: gen-pdf
gen-pdf: backup restore
	$(VENV)/python manage.py generate_pdf export-pdf/
	
.PHONY: sync-icloud
sync-icloud: #gen-pdf | backup
	rsync -av export-pdf/ $(ICLOUD_DIR)