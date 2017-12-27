.PHONY: init test coverage install publish docs-init docs clean

PYTHON=python

init:
	pip install -r requirements.txt

test:
	$(PYTHON) setup.py test

coverage:
	coverage run --source=dyndnsc setup.py test

coveralls:
	pip install coveralls
	coveralls

install:
	$(PYTHON) setup.py install

publish:
	$(PYTHON) setup.py register
	$(PYTHON) setup.py sdist upload
	$(PYTHON) setup.py bdist_wheel upload


docs-init:
	pip install -r docs/requirements.txt

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

deb:
	# this requires `apt-get install debhelper python3-all`
	# Please note that this is not the way "official" debian packages are built
	# Please also note that dyndnsc is best supported in python3, so debs for python2 are
	# simply left out.
	pip install stdeb
	$(PYTHON) setup.py --command-packages=stdeb.command bdist_deb


clean:
	@echo "Cleaning up distutils and tox stuff"
	rm -rf build dist deb_dist
	rm -rf *.egg .eggs *.egg-info
	rm -rf .tox
	@echo "Cleaning up byte compiled python stuff"
	find . -regex "\(.*__pycache__.*\|*.py[co]\)" -delete

