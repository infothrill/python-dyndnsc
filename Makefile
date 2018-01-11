.PHONY: publish clean

PYTHON=python3

publish:
	@echo "Use 'python setup.py sdist bdist_wheel; twine'"

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
