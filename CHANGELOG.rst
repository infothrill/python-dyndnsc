.. :changelog:

Release history
---------------
0.5.1 (July 7th 2019)
++++++++++++++++++++++
- improved: pin pytest version to `version smaller than 5.0.0 <https://docs.pytest.org/en/latest/py27-py34-deprecation.html>`_

0.5.0 (June 25th 2019)
++++++++++++++++++++++
- improved: simplified notification plugin and externalized them using entry_points
- added: WAN IP detection through DNS (detector 'dnswanip')
- improved: replaced built-in daemon code with `daemonocle <https://pypi.python.org/pypi/daemonocle>`_
- switched to `pytest <https://pytest.org>`_ for running tests
- changed (**INCOMPATIBLE**): dropped support for python 2.6 and python 3.3
- added: new command line option -v to control verbosity
- improved: infinite loop and daemon stability, diagnostics #57
- improved: updated list of external urls for IP discovery
- improved: install documentation updated
- improved: add many missing docstrings and fixed many code smells
- improved: run `flake8 <http://flake8.pycqa.org/>`_ code quality checks in CI
- improved: run `check-manifest <https://pypi.python.org/pypi/check-manifest>`_ in CI
- improved: run `safety <https://pypi.python.org/pypi/safety>`_ in CI

0.4.4 (December 27th 2017)
++++++++++++++++++++++++++
- fixed: fixed wheel dependency on python 2.6 and 3.3
- fixed: pep8 related changes, doc fixes

0.4.3 (June 26th 2017)
++++++++++++++++++++++
- fixed: nsupdate URLs
- fixed: several minor cosmetic issues, mostly testing related

0.4.2 (March 8th 2015)
++++++++++++++++++++++
- added: support for https://www.duckdns.org
- fixed: user configuration keys now override built-in presets

0.4.1 (February 16th 2015)
++++++++++++++++++++++++++
- bugfixes

0.4.0 (February 15th 2015)
++++++++++++++++++++++++++

- changed (**INCOMPATIBLE**): command line arguments have been drastically adapted
  to fit different update protocols and detectors
- added: config file support
- added: running against multiple update services in one go using config file
- improved: for python < 3.2, install more dependencies to get SNI support
- improved: the DNS resolution automatically resolves using the same address
  family (ipv4/A or ipv6/AAAA or any) as the detector configured
- improved: it is now possible to specify arbitrary service URLs for the
  different updater protocols.
- fixed: naming conventions
- fixed: http connection robustness (i.e. catch more errors and handle them as
  being transient)
- changed: dependency on netifaces was removed, but if installed, the
  functionality remains in place
- a bunch of pep8, docstring and documntation updates

0.3.4 (January 3rd 2014)
++++++++++++++++++++++++
- added: initial support for dnsimple.com through
  `dnsimple-dyndns <https://pypi.python.org/pypi/dnsimple-dyndns>`_
- added: plugin based desktop notification (growl and OS X notification center)
- changed: for python3.3+, use stdlib 'ipaddress' instead of 'IPy'
- improved: dyndns2 update is now allowed to timeout
- improved: freedns.afraid.org robustness
- improved: webcheck now has an http timeout
- improved: naming conventions in code
- added: initial documentation using sphinx

0.3.3 (December 2nd 2013)
+++++++++++++++++++++++++
- added: experimental support for http://freedns.afraid.org
- added: detecting ipv6 addresses using 'webcheck6' or 'webcheck46'
- fixed: long outstanding state bugs in detector base class
- improved: input validation in Iface detection
- improved: support pytest conventions

0.3.2 (November 16th 2013)
++++++++++++++++++++++++++
- added: command line option --debug to explicitly increase loglevel
- fixed potential race issues in detector base class
- fixed: several typos, test structure, naming conventions, default loglevel
- changed: dynamic importing of detector code

0.3.1 (November 2013)
+++++++++++++++++++++
- added: support for https://nsupdate.info
- fixed: automatic installation of 'requests' with setuptools dependencies
- added: more URL sources for 'webcheck' IP detection
- improved: switched optparse to argparse for future-proofing
- fixed: logging initialization warnings
- improved: ship tests with source tarball
- improved: use reStructuredText rather than markdown

0.3  (October 2013)
+++++++++++++++++++
- moved project to https://github.com/infothrill/python-dyndnsc
- added continuous integration tests using http://travis-ci.org
- added unittests
- dyndnsc is now a package rather than a single file module
- added more generic observer/subject pattern that can be used for
  desktop notifications
- removed growl notification
- switched all http related code to the "requests" library
- added http://www.noip.com
- removed dyndns.majimoto.net
- dropped support for python <= 2.5 and added support for python 3.2+

0.2.1 (February 2013)
+++++++++++++++++++++
- moved code to git
- minimal PEP8 changes and code restructuring
- provide a makefile to get dependencies using buildout

0.2.0 (February 2010)
+++++++++++++++++++++
- updated IANA reserved IP address space
- Added new IP Detector: running an external command
- Minimal syntax changes based on the 2to3 tool, but remaining compatible
  with python 2.x

0.1.2 (July 2009)
+++++++++++++++++
- Added a couple of documentation files to the source distribution

0.1.1 (September 2008)
++++++++++++++++++++++
- Focus: initial public release
