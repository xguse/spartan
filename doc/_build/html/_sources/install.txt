Installation
============

Requirements
------------

The following python modules must be installed for spartan to function properly: ::

	todo: are there any?

The following modules will provide useful but optional functionality: ::

	gffutils
	pybedtools



Installing the latest version from the git repository
-----------------------------------------------------
.. Note:: Git is a **very** useful tool to have installed and to know how to use.  `Learn more here <http://git-scm.com/>`_ and `try it out here <http://try.github.com/>`_.

Clone the repo::

	$ git clone git://github.com/xguse/spartan.git

Install with any unmet requirements using ``pip``: ::

	$ [sudo] pip install -r spartan/requirements.txt spartan

Install using standard ``setup.py`` script: ::

	$ cd spartan
	$ [sudo] python setup.py install

Use ``pip`` to obtain the package from `PyPI <https://pypi.python.org/pypi>`_
------------------------------------------------------------------------------
::

	$ [sudo] pip install spartan Mako PyYAML pprocess



Installing without using ``git`` or ``pip`` for the download
------------------------------------------------------------
After installing the requirements: ::

	$ wget https://github.com/xguse/spartan/archive/master.zip
	$ unzip master.zip
	$ cd spartan-master
	$ [sudo] python setup.py install

Test to see whether the install worked
--------------------------------------
To test whether your installation was successful, open a new terminal session and type the following command. ::

	$ spartan

