.PHONY: init test coverage install publish docs-init docs clean

init:
	pip install -r requirements.txt

test:
	python setup.py test

coverage:
	coverage run --source=dyndnsc setup.py test

coveralls:
	pip install coveralls
	coveralls

install:
	python setup.py install

publish:
	python setup.py register
	python setup.py sdist upload
	python setup.py bdist_wheel upload


docs-init:
	pip install -r docs/requirements.txt

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

clean:
	@echo "Cleaning up distutils stuff"
	rm -rf build
	rm -rf dist
	rm -rf *.egg
	rm -rf *.egg-info
	@echo "Cleaning up byte compiled python stuff"
	find . -type f -regex ".*\.py[co]$$" -delete
