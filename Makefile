clean:
	rm -rf venv venv3 build dist *.egg-info
	find . -name '*.pyc' -delete

prepare:clean
	set -ex
	pip install mock
	pip install -r requirements.txt
	python setup.py install
	python3 setup.py install

test:prepare
	python setup.py test
	python3 setup.py test
