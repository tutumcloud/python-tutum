clean:
	rm -rf venv venv3 build dist *.egg-info
	find . -name '*.pyc' -delete

prepare:clean
	set -ex
	virtualenv venv
	venv/bin/pip install mock
	venv/bin/pip install -r requirements.txt
	venv/bin/python setup.py install

test:prepare
	venv/bin/python setup.py test

