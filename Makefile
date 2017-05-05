.PHONY: all run metadata

all: run

run: venv
	. $^/bin/activate ; cd mysite; python manage.py runserver 0.0.0.0:8000

venv: requirements.txt
	virtualenv $@
	. $@/bin/activate ; pip install -r $^

metadata:
	curl -o metadata -s https://drone.sandbox.aws.illinois.edu/metadata/
	curl -F "userfile=@metadata;filename=drone.sandbox.aws.illinois.edu" \
		https://www.testshib.org/procupload.php

clean:
	-rm -rf venv
