***************
RAMSTK Overview
***************

`RAMSTK` provides several analytical tools for estimating the RAMS metrics for
electromechanical systems.

Requirements
============

RAMSTK requires access to at least one postgresql database server.  Installing
and configuring a postgresql server is outside the scope of RAMSTK
documentation.  Your first resource should be the official postgresql
documents. Internet searches should provide you more assistance if needed.

The project `wiki <https://github.com/ReliaQualAssociates/ramstk/wiki/PostgreSQL-Server-Setup>`_
contains instructions and hints for setting up a postgresql server and
database users for RAMSTK.  They may be helpful, but expect your mileage to
vary.

Installation
============

Since RAMSTK is still a version 0 product, it's highly recommended that you
install in a virtual environment.  The instructions below presume you will
be installing in a virtual environment and system-wide Python packages that
RAMSTK depends on will be unavailable.  That being the case, you will need
various system development packages available via your operating system's
package manager to install RAMSTK.

Once you have installed any missing development file packages using your
operating system's package manager, download the \<version> of RAMSTK
source from GitHub you wish to install.

.. code-block:: bash

    $ wget https://github.com/ReliaQualAssociates/ramstk/archive/v0.15.14.tar.gz
    $ tar -xf v0.15.14.tar.gz
    $ cd ramstk-0.15.14

The other option for obtaining the RAMSTK source code is to clone the
repository.

.. code-block:: bash

    $ git clone https://github.com/ReliaQualAssociates/ramstk.git ramstk.git
    $ cd ramstk.git

Create and activate a virtual environment however you are acustomed to.
One approach is to use pyenv and poetry.  Using pyenv isn't necessary
unless you want to install and use a Python version other than that
provided by your operating system.

.. code-block:: bash

    $ pyenv install 3.8.7
    $ poetry env use ~/.pyenv/shims/python3.8
    $ poetry shell

This will install Python-3.8.7 and tell poetry to use the Python interpreter
you just installed.  Finally, poetry will create, if needed, and activate
the virtual environment using Python-3.8.7 as the interpreter.

Now that the virtual environment is activated, you can install the
necessary RAMSTK dependencies and RAMSTK itself.  Omitting the PREFIX
variable will cause RAMSTK to install to /usr/local by default.

.. code-block:: bash

    $ make depends
    $ make PREFIX=$VIRTUAL_ENV install

When upgrading RAMSTK, you can simply:

.. code-block:: bash

    $ pip install -U ramstk


This will only install the latest RAMSTK version from PyPi and will leave
configuration, data, and icon files untouched.  If you cloned the RAMSTK
repository, you can also use the Makefile:

.. code-block:: bash

    $ git switch master
    $ git pull
    $ make install.dev

License
=======

`RAMSTK` is provided to you under the BSD, 3-clause license, reproduced below.

.. literalinclude:: ../LICENSE
