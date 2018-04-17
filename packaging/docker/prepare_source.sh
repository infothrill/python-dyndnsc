#!/bin/bash -xe
# this allows us to copy the source into the docker image without
# bothering to install git or other more complicated logic inside it. Also,
# this script outputs the current version so we can tag the created image
# with it.
if ! test -d src;
then
    cat /etc/*release 1>&2 || true  # display distribution name
    env 1>&2 # display env vars
    id 1>&2 # display current user
    if ! hash tox 2>&-;
    then
        if ! hash virtualenv 2>&-;
        then
            if [ "$(id -u)" = 0 ]; then
                apt-get update 1>&2 && apt-get install -y python-virtualenv 1>&2
            fi
            # else: no idea
        fi
        virtualenv .venv 1>&2
        source .venv/bin/activate
        pip install tox 1>&2
    fi
    tox -e build 1>&2
    mkdir src
    ls ../../dist/dyndnsc-*.tar.gz | xargs -n1 tar -C src --strip-components 1 -xzf
    python -c "import re, os; print(re.compile(r'.*__version__ = \"(.*?)\"', re.S).match(open(os.path.join('src/dyndnsc', '__init__.py'), 'r').read()).group(1))" > src/version
fi
cat src/version
