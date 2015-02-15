Dyndnsc Debian Package
======================

To create a DEB package:

    sudo apt-get install python-setuptools
    sudo apt-get install build-essential devscripts debhelper
    git clone git://github.com/infothrill/python-dyndnsc.git
    cd python-dyndnsc
    # TODO:
    make deb

The debian package file will be placed in the `../` directory. This can then be added to an APT repository or installed with `dpkg -i <package-file>`.

Note that `dpkg -i` does not resolve dependencies.

To install the DEB package and resolve dependencies:

    sudo dpkg -i <package-file>
    sudo apt-get -fy install
