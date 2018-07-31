# The RAMS ToolKit (RAMSTK)
> A toolkit for **R**eliability, **A**vailability, **M**aintainability, and **S**afety (RAMS) analyses.

[![Github](https://img.shields.io/github/release/weibullguy/rtk/all.svg)](https://github.com/weibullguy/rtk/releases)
[![PyPI](https://img.shields.io/pypi/v/RAMSTK.svg)](https://pypi.python.org/pypi/RAMSTK/)

***Please note the development branch is currently the default branch until version 1.0.0 is released.***

[![Build Status](https://travis-ci.org/weibullguy/rtk.svg?branch=develop)](https://travis-ci.org/weibullguy/rtk)
[![Build status](https://ci.appveyor.com/api/projects/status/eh0md738pyoiick0/branch/develop?svg=true)](https://ci.appveyor.com/project/weibullguy/rtk/branch/develop)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f668feeaec0f46d5990a3c45aefc3923)](https://www.codacy.com/app/weibullguy/rtk?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=weibullguy/rtk&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/f668feeaec0f46d5990a3c45aefc3923)](https://www.codacy.com/app/weibullguy/rtk?utm_source=github.com&utm_medium=referral&utm_content=weibullguy/rtk&utm_campaign=Badge_Coverage)
[![Coverage Status](https://coveralls.io/repos/github/weibullguy/rtk/badge.svg?branch=develop)](https://coveralls.io/github/weibullguy/rtk?branch=develop)
[![Documentation Status](https://readthedocs.org/projects/rtk/badge/?version=develop)](http://rtk.readthedocs.io/en/develop/?badge=develop)

## 🚩 Table of Contents
- [Features](#-features)
- [Installing](#-installing)
    - [Prerequisites](#prerequisites)
    - [Using pip](#using-pip)
    - [Download](#download)
    - [Running the Tests](#running-the-tests)
- [Usage](#-usage)
- [Docs](#-docs)
- [Examples](#-examples)
- [Contributing](#-contributing)
- [Authors](#-authors)
- [License](#-license)
- [Similar Products](#-similar-products)

## 🎨 Features

RAMSTK is built on the concept of modules where a module is a collection of related information and/or analyses pertinent to system development.  The modules currently included in RAMSTK are:

* Function Module
  - Functional decomposition
  - Functional FMEA
  - Hardware/Function matrix
* Requirements Module
  - Stakeholder input prioritization
  - Requirement development
  - Analysis of requirement for clarity, completeness, consistency, and verifiability
* Hardware Module
  - Reliability allocation
      - Equal apportionment
      - AGREE apportionment
      - ARINC apportionment
      - Feasibility of Objectives
  - Hazards analysis
  - Hardware reliability predictions using various methods
      - Similar items analysis
      - MIL-HDBK-217F parts count
      - MIL-HDBK-217F parts stress
  - FMEA/FMECA
      - RPN
      - MIL-STD-1629A, Task 102 Criticality Analysis
  - Physics of failure analysis
* Validation Module
      - Task description
      - Task acceptance value(s)
      - Task time
      - Task cost
      - Overall validation plan time/cost estimates

## 💾 Installing

These instructions will get RAMSTK up and running on your local machine.

### Prerequisites

RAMSTK requires PyGTK to be installed.  If you plan to install RAMSTK in a virtual environment (not a terrible idea if you're just giving RAMSTK a spin), please see [DEVELOPMENT_ENV.md](https://github.com/weibullguy/rtk/tree/develop/docs/DEVELOPMENT_ENV.md) for instructions on installing RAMSTK dependencies.  Otherwise, simply use your package manager to install PyGTK and one of the options below to install the remaining dependencies.

### Using pip

To install from PyPI using pip, simply issue the following command:

```sh
$ pip install RAMSTK
```

With the exception of PyGTK, pip will install any missing runtime dependencies automatically.

### Download

Install any missing RAMSTK dependencies using pip, your package manager, and/or build from source.  Then download the <version> of RAMSTK source from GitHub Releases you wish to install.

```sh
$ tar -xf RAMSTK-<version>.tar.gz
$ cd RAMSTK-<version>
$ python setup.py install
```

### Running the Tests

To run the entire test suite for RAMSTK after installing, simply execute:

```
$ python setup.py test
```

To run specific tests or groups of tests, use pytest:

```
$ pytest -m integration tests/modules/test_allocation.py
$ pytest -m calculation tests/analyses/prediction
```

#### Coding Style Tests

The test directory contains a script named RunTests.py.  This is for executing static checkers such as pylint and is intended for developers.  It makes it easier to integrate into an IDE.  You can execute the following to see what RunTests.py wraps:

```
$ tests/RunTests.py --help
```

## 🔨 Usage

After installing RAMSTK, it can be launched from a terminal emulator:

```
$ ramstk
```

This is a good option if you need to file an issue as the output should be included in your report.

RAMSTK installs a *.desktop file and can be found where ever applications in the category Math or Science are listed.

## 💬 Contributing

Please read [CONTRIBUTING.md](https://github.com/weibullguy/rtk/tree/develop/docs/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

Also read [DEVELOPMENT_ENV.md](https://github.com/weibullguy/rtk/tree/develop/docs/DEVELOPMENT_ENV.md) for instructions on setting up a development environment to work on and test RAMSTK.

## 🍞 Authors

* **Doyle 'weibullguy' Rowland** - *Initial work* - [weibullguy](https://github.com/weibullguy)

## 📜 License

This project is licensed under the BSD-3-Clause License - see the [LICENSE](https://github.com/weibullguy/rtk/blob/develop/LICENSE) file for details.

RAMSTK is also registered with the United States Copyright Office under registration number TXu 1-896-035.

## Similar Products

The following are commercially available products that perform RAMS analyses.  We are not endorsing any of them; they are all fine products and may be a better fit for you or your organization depending on your needs and budget.  Obviously, we would prefer you use RAMSTK.

* [PTC Windchill Quality](https://www.ptc.com/en/products/plm/capabilities/quality)
* [ReliaSoft Synthesis](https://www.reliasoft.com/products)
