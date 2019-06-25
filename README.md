# The RAMS ToolKit (RAMSTK)
> A toolkit for **R**eliability, **A**vailability, **M**aintainability, and **S**afety (RAMS) analyses.

[![Github](https://img.shields.io/github/release/ReliaQualAssociates/ramstk/all.svg)](https://github.com/ReliaQualAssociates/ramstk/releases)
[![PyPI](https://img.shields.io/pypi/v/RAMSTK.svg)](https://pypi.python.org/pypi/RAMSTK/)
[![Develop Build Status](https://travis-ci.org/ReliaQualAssociates/ramstk.svg?branch=develop)](https://travis-ci.org/ReliaQualAssociates/ramstk)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/281487d67cff4b7a8fd7bd4ef878a45e)](https://www.codacy.com/app/ReliaQualAssociates/ramstk?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ReliaQualAssociates/ramstk&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/281487d67cff4b7a8fd7bd4ef878a45e)](https://www.codacy.com/app/ReliaQualAssociates/ramstk?utm_source=github.com&utm_medium=referral&utm_content=ReliaQualAssociates/ramstk&utm_campaign=Badge_Coverage)
[![Coverage Status](https://coveralls.io/repos/github/ReliaQualAssociates/ramstk/badge.svg?branch=master)](https://coveralls.io/github/ReliaQualAssociates/ramstk?branch=master)
[![CodeFactor](https://www.codefactor.io/repository/github/reliaqualassociates/ramstk/badge)](https://www.codefactor.io/repository/github/reliaqualassociates/ramstk)
[![BCH Compliance](https://bettercodehub.com/edge/badge/ReliaQualAssociates/ramstk?branch=master)](https://bettercodehub.com/)

## 🚩 Table of Contents
- [Features](#-features)
- [Installing](#-installing)
    - [Prerequisites](#prerequisites)
    - [Using pip](#using-pip)
    - [Download](#download)
    - [Running the Tests](#running-the-tests)
- [Usage](#-usage)
- [Documentation](#-docs)
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

RAMSTK requires PyGTK to be installed.  If you plan to install RAMSTK in a virtual environment (not a terrible idea if you're just giving RAMSTK a spin), please see [DEVELOPMENT_ENV.md](https://github.com/weibullguy/ramstk/tree/develop/docs/DEVELOPMENT_ENV.md) for instructions on installing RAMSTK dependencies.  Otherwise, simply use your package manager to install PyGTK and one of the options below to install the remaining dependencies.

### Using pip

To install from PyPI using pip, simply issue the following command:

```sh
$ pip install ramstk
```

With the exception of PyGTK, pip will install any missing runtime dependencies automatically.

### Download

Install any missing RAMSTK dependencies using pip, your package manager, and/or build from source.  Then download the <version> of RAMSTK source from GitHub Releases you wish to install.

```sh
$ tar -xf ramstk-<version>.tar.gz
$ cd ramstk-<version>
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

## 🔨 Usage

After installing RAMSTK, it can be launched from a terminal emulator:

```
$ ramstk
```

This is a good option if you need to file an issue as the output should be included in your report.

RAMSTK installs a *.desktop file and can be found where ever applications in the category Math or Science are listed.

## Documentation

Documentation for RAMSTK can be found [here](https://reliaqualassociates.github.io/ramstk/).  You should check it out!

## 💬 Contributing

Please read [CONTRIBUTING.md](https://github.com/weibullguy/ramstk/tree/develop/docs/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

Also read [DEVELOPMENT_ENV.md](https://github.com/weibullguy/ramstk/tree/develop/docs/DEVELOPMENT_ENV.md) for instructions on setting up a development environment to work on and test RAMSTK.

## 🍞 Authors

* **Doyle 'weibullguy' Rowland** - *Initial work* - [weibullguy](https://github.com/weibullguy)

## 📜 License

This project is licensed under the BSD-3-Clause License - see the [LICENSE](https://github.com/weibullguy/ramstk/blob/develop/LICENSE) file for details.

RAMSTK is also registered with the United States Copyright Office under registration number TXu 1-896-035.

## Similar Products

The following are commercially available products that perform RAMS analyses.  We are not endorsing any of them; they are all fine products and may be a better fit for you or your organization depending on your needs and budget.  Obviously, we would prefer you use RAMSTK.

* [PTC Windchill Quality](https://www.ptc.com/en/products/plm/capabilities/quality)
* [ReliaSoft Synthesis](https://www.reliasoft.com/products)
