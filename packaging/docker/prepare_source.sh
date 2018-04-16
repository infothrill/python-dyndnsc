#!/bin/bash -xe
# this allows us to copy the source into the docker image without
# bothering to install git or other more complicated logic inside it. Also,
# this script outputs the current version so we can tag the create image with it.
if ! test -d src;
then
	hash tox 2>&- || pip install tox 1>&2
	tox -e build > /dev/null
	mkdir src
	ls ../../dist/*.tar.gz | grep dyndnsc | xargs -n1 tar -C src --strip-components 1 -xzf
	python -c "import re, os; print(re.compile(r'.*__version__ = \"(.*?)\"', re.S).match(open(os.path.join('src/dyndnsc', '__init__.py'), 'r').read()).group(1))" > src/version
fi
cat src/version
