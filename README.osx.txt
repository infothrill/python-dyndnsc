On OS X, python comes with some "Extras" built into the /System/ Python, so these
extras are not detected as "site-packages".

One of these is used by the testrunner in buildout (zope.interfaces).
To circumvent the default Apple shipped python stuff, just upgrade:

 $ sudo pip install zope.interfaces --upgrade 