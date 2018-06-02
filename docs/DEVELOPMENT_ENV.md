# Establishing a Development Environment

This document describes how to setup a development environment for RTK.  These
instructions ensure every developer is using, ideally, the same environment
regardless of platform.

## Required Tools

The following applications will be required to setup the development
environment.  These may be installed system-wide using your package manager or
installed in a local directory and only available for single user.  Either way,
these tools are only required to setup the RTK development environment, they
are not used **in** the environment:

  - virtualenv
  - virtualenvwrapper

## Create the Virtual Environment

Once the tools in the previous section are installed and available for your
use, the next step is to create a virtual environment to develop RTK in.
Execute the following to setup the virtual environment:
```
~/projects/RTK $ export WORKON_HOME="$HOME/.virtualenvs"
~/projects/RTK $ export PROJECT_HOME-"$HOME/projects"
~/projects/RTK $ source $(which virtualenvwrapper.sh)
~/projects/RTK $ mkvirtualenv rtk-python2.7-pygtk
```

You should now find yourself in a virtual environment named rtk-development.
The paths and virtual environment name above can be changed to whatever you
would like, those are just the names I use.  Whenever you need to work in the
RTK environment, just execute `workon rtk-python2.7-pygtk` to re-enter the
virtual environment.

## Install Python Packages

After you are in the virtual environment, you will need to install the Python
packages needed by RTK to run and some recommended packages for development and
testing.
```
(rtk-python2.7-pygtk) ~/projects/RTK $ pip install -U pip
(rtk-python2.7-pygtk) ~/projects/RTK $ pip install -U setuptools>12.0
(rtk-python2.7-pygtk) ~/projects/RTK $ pip install --only-binary=numpy numpy==1.14.3
(rtk-python2.7-pygtk) ~/projects/RTK $ pip install --only-binary=scipy scipy==1.0.0
(rtk-python2.7-pygtk) ~/projects/RTK $ pip install coverage==4.0.3
(rtk-python2.7-pygtk) ~/projects/RTK $ pip install -r requirements_run.txt
(rtk-python2.7-pygtk) ~/projects/RTK $ pip install -r requirements_dev.txt
(rtk-python2.7-pygtk) ~/projects/RTK $ pip install -r requirements_doc.txt
```

Now that most everything needed in the development environment that can be
installed via PyPi is installed, it is necessary to manually install PyGTK in
the new virtual environment.  It is important to install numpy before PyGTK so
PyGTK will build with numpy support.

First create a build directory and download the PyGTK source tarballs into
that directory:
```
(rtk-python2.7-pygtk) ~/projects/RTK $ cd $PROJECT_HOME
(rtk-python2.7-pygtk) ~/projects/RTK $ mkdir pygtk_build
(rtk-python2.7-pygtk) ~/projects/RTK $ cd pygtk_build
(rtk-python2.7-pygtk) ~/projects/RTK $ wget http://www.cairographics.org/releases/py2cairo-1.10.0.tar.bz2
(rtk-python2.7-pygtk) ~/projects/RTK $ wget http://ftp.gnome.org/pub/GNOME/sources/pygobject/2.28/pygobject-2.28.6.tar.bz2
(rtk-python2.7-pygtk) ~/projects/RTK $ wget http://ftp.gnome.org/pub/GNOME/sources/pygtk/2.24/pygtk-2.24.0.tar.bz2
```

Now build py2cairo and install into the virtual environment:
```
(rtk-python2.7-pygtk) ~/projects/RTK $ tar -xf py2cairo-1.10.0.tar.bz2
(rtk-python2.7-pygtk) ~/projects/RTK $ cd py2cairo-1.10.0
(rtk-python2.7-pygtk) ~/projects/RTK $ ./waf configure --prefix=$VIRTUAL_ENV
(rtk-python2.7-pygtk) ~/projects/RTK $ ./waf build
(rtk-python2.7-pygtk) ~/projects/RTK $ ./waf install
(rtk-python2.7-pygtk) ~/projects/RTK $ cd ..
```

Now build pygobject and install into the virtual environment:
```
(rtk-python2.7-pygtk) ~/projects/RTK $ tar -xf pygobject-2.28.6.tar.bz2
(rtk-python2.7-pygtk) ~/projects/RTK $ cd pygobject-2.28.6
(rtk-python2.7-pygtk) ~/projects/RTK $ ./configure --prefix=$VIRTUAL_ENV --disable-introspection
(rtk-python2.7-pygtk) ~/projects/RTK $ make
(rtk-python2.7-pygtk) ~/projects/RTK $ make install
(rtk-python2.7-pygtk) ~/projects/RTK $ cd ..
```

Now build pygtk and install into the virtual environment:
```
(rtk-python2.7-pygtk) ~/projects/RTK $ tar -xf pygtk-2.24.0.tar.bz2
(rtk-python2.7-pygtk) ~/projects/RTK $ cd pygtk-2.24.0
(rtk-python2.7-pygtk) ~/projects/RTK $ ./configure --prefix=$VIRTUAL_ENV
(rtk-python2.7-pygtk) ~/projects/RTK $ make
(rtk-python2.7-pygtk) ~/projects/RTK $ make install
(rtk-python2.7-pygtk) ~/projects/RTK $ cd $PROJECT_HOME/RTK
```

Optionally, verify PyGTK installed and is importable.
```
(rtk-python2.7-pygtk) ~/projects/RTK $ python

>>> import gtk
>>> quit()
```

Finally, after PyGTK is successfully installed in the virtual environment, it
is time to install matplotlib.  Install matplotlib after PyGTK is necessary so
matplotlib builds the GDK backend.
```
(rtk-python2.7-pygtk) ~/projects/RTK $ pip install matplotlib==1.4.3
```

Optionally, verify the GDK backend shared library (**__backend_gdk.so**) is
installed:
```
(rtk-python2.7-pygtk) ~/projects/RTK $ ls $VIRTUAL_ENV/lib/python2.7/site-packages/matplotlib/backends
```

## Install and Test RTK

Now that all the required runtime, development, and documentation packages are
installed, RTK itself should be installed and tested:
```
(rtk-python2.7-pygtk) ~/projects/RTK $ python setup.py develop
(rtk-python2.7-pygtk) ~/projects/RTK $ which rtk
/home/arowland/.virtualenvs/rtk-python2.7-pygtk/bin/rtk
(rtk-python2.7-pygtk) ~/projects/RTK $ python setup.py test
```

If all goes well, all the tests will pass and you will be ready to develop and
use RTK.  Good luck and thanks for your help!!

Doyle 'weibullguy' Rowland
May 20, 2018
