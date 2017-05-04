.PHONY: all run

all: run

run: venv
	cd mysite; python manage.py runserver 0.0.0.0:8000

venv: requirements.txt
	virtualenv $@
	. $@/bin/activate ; pip install -r $^

clean:
	-rm -rf venv
