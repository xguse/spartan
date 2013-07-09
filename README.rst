=========
spartan
=========

-----------------------------------------------------------------------------------------------------------------------------------------------------
A spartan bioinformatics package, providing only the essentials and nothing fancy or luxurious. Enough to get the job done quickly without flourish.
-----------------------------------------------------------------------------------------------------------------------------------------------------


README
=======

This is ``spartan``. 

``spartan`` is a central place that I have decided to store/develop
many of the bioinformatics classes/functions/scripts that I have written and find I use a lot.

As the name implies, this is pretty functional code, but I have only done MINIMAL user-proofing.
For the most part if a function/method expects a gff file you should do your due diligence that that
file is indeed formatted correctly.  If someone wants to add more, I welcome it.  However if I am going
to add code it will be to add functionality.

After all, this is ``spartan``.


INSTALL
==========

By cloning the repo: ::

	git clone https://github.com/xguse/spartan.git 
	[sudo] pip install spartan/

If you don't use ``pip`` (but you **should** be using ``pip``): ::

	git clone https://github.com/xguse/spartan.git 
	cd spartan/
	[sudo] python setup.py install

With ``pip`` without cloning the repo: ::
	
	pip install https://github.com/xguse/spartan.git
	
	
	

Credits
-------

- `Distribute`_
- `Buildout`_
- `modern-package-template`_

.. _Buildout: http://www.buildout.org/
.. _Distribute: http://pypi.python.org/pypi/distribute
.. _`modern-package-template`: http://pypi.python.org/pypi/modern-package-template
