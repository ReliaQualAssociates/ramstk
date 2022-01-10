# The RAMS ToolKit (RAMSTK)
> A ToolKit for **R**eliability, **A**vailability, **M**aintainability, and
> **S**afety (RAMS) analyses.

<table>
    <tr>
        <th>Documentation</th>
        <td>
            <a href='https://ramstk.readthedocs.io/en/latest/?badge=latest'><img src='https://readthedocs.org/projects/ramstk/badge/?version=latest' alt='Documentation Status' /></a>
        </td>
    </tr>
    <tr>
        <th>Tests</th>
        <td>
        <img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/ReliaQualAssociates/ramstk/RAMSTK%20Test%20Suite?label=Build%20%26%20Test">
        <a href="https://codecov.io/gh/ReliaQualAssociates/ramstk"><img src="https://codecov.io/gh/ReliaQualAssociates/ramstk/branch/master/graph/badge.svg?token=sFOa7EjZAg"/></a>
        <a href='https://coveralls.io/github/ReliaQualAssociates/ramstk?branch=master'><img src='https://coveralls.io/repos/github/ReliaQualAssociates/ramstk/badge.svg?branch=master' alt='Coverage Status' /></a>
    </td>
    </tr>
    <tr>
        <th>Quality</th>
        <td>
            <a href="https://www.codefactor.io/repository/github/reliaqualassociates/ramstk"><img src="https://www.codefactor.io/repository/github/reliaqualassociates/ramstk/badge" alt="CodeFactor" /></a>
            <img alt="Quality Gate" src="https://sonarcloud.io/api/project_badges/measure?project=ReliaQualAssociates_ramstk&metric=alert_status">
        </td>
    </tr>
    <tr>
        <th>Packages</th>
        <td>
            <img alt="GitHub release (latest SemVer including pre-releases)" src="https://img.shields.io/github/v/release/ReliaQualAssociates/ramstk?include_prereleases&label=GitHub%20Release">
            <img alt="PyPI" src="https://img.shields.io/pypi/v/ramstk?label=PyPi%20Release">
        </td>
    </tr>
</table>

## 🚩 Table of Contents
- [Features](#-features)
- [Installing](#-installing)
    - [Prerequisites](#prerequisites)
    - [Download](#download)
    - [Running the Tests](#running-the-tests)
- [Usage](#-usage)
- [Documentation](#documentation)
- [Contributing](#-contributing)
- [Authors](#-authors)
- [License](#-license)
- [Similar Products](#similar-products)

## Disclaimer

RAMSTK attempts to use [Semantic Versioning](https://semver.org/) 2.0.0.  Per
4, major version 0 is for initial development and anything may change at
any time.  That is certainly the case for RAMSTK!  Because RAMSTK is a one
developer show, there is no active develop branch at the moment.  This may
change after release of 1.0.0.  Until then, tagged releases can be used, but
the `latest` tag may not work and may not be backwards-compatible.  While major
version is at 0, breaking changes will be reflected in bumps to the minor
version number.  That is, version 0.15.0 is not compatible with version 0.14.0.
Also at this time, patch versions will not be released.  This will change after
version 1.0.0 is released.

## 🎨&nbsp; Features

RAMSTK is built on the concept of modules where a module is a collection of
 related information and/or analyses pertinent to system development.  The
  modules currently included in RAMSTK are:

* Function Module
  - Functional decomposition
  - Hazards analysis
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

## 💾&nbsp; Installing

These instructions will hopefully get RAMSTK up and running on your local
machine.  RAMSTK uses a Makefile to install/uninstall itself because there are
various icon, data, and configuration files that also need to be installed
outside site-packages.  Thus, only the actual RAMSTK application is available
at PyPi and the initial installation must be done using the source asset at
GitHub for the release you wish to install or cloning the RAMSTK repository if
you'd like the latest code.

RAMSTK uses [postgresql](https://www.postgresql.org/) for its database
 engine.  You'll need to have a user with read/write access to a postgresql
  server to use RAMSTK.

### Download and Install

Install any missing RAMSTK dependencies using pip, your package manager, and/or
build from source.  Then download the \<version> of RAMSTK source from GitHub
you wish to install.

```shell
$ wget https://github.com/ReliaQualAssociates/ramstk/archive/v<version>.tar.gz
$ tar -xf v<version>.tar.gz
$ cd ramstk-<version>
$ make install
```

The install target recognizes PREFIX=<non-default install path> so you can
 install RAMSTK in your $HOME or a virtual environment.  Since RAMSTK is
  still a version 0 product, it's highly recommended that you install in a
   virtual environment.

```shell
$ wget https://github.com/ReliaQualAssociates/ramstk/archive/v<version>.tar.gz
$ tar -xf v<version>.tar.gz
$ cd ramstk-<version>
$ make PREFIX=$VIRTUAL_ENV install
```

When upgrading RAMSTK, you can simply:

```shell
$ pip install
```

This will only install the latest RAMSTK version from PyPi and will leave
configuration, data, and icon files untouched.  If you are using the latest
code from GitHub, you can also use the Makefile:

```shell
$ make install.dev
```

### Development Dependencies

I use [poetry](https://github.com/python-poetry/poetry) to manage the
dependencies for RAMSTK while I'm developing.  Using the Makefile, install as
follows:

```shell
$ make depends
```

This should get all the needed development and runtime requirements installed
if they're not already.

### Running the Tests

To run the entire test suite for RAMSTK after installing, simply execute:

```shell
$ make test
```

To run the test suite with coverage, execute:

```shell
$ make coverage
```

To run specific tests or groups of tests, use pytest:

```shell
$ pytest -m integration tests/modules/test_allocation.py
$ pytest -m calculation tests/analyses/prediction
```

## 🔨&nbsp; Usage

After installing RAMSTK, it can be launched from a terminal emulator:

```
$ ramstk
```

This is a good option if you need to file an issue as the output should be
 included in your report.

RAMSTK installs a *.desktop file and can be found where ever applications in
 the category Math or Science are listed.

## Documentation

Documentation for RAMSTK can be found at [Read the Docs](https://ramstk.readthedocs.io/en/latest) You should check it out!

## 💬&nbsp; Contributing

Please read [CONTRIBUTING.md](https://github.com/ReliaQualAssociates/ramstk/tree/develop/docs/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

Also read [DEVELOPMENT_ENV.md](https://github.com/ReliaQualAssociates/ramstk/tree/develop/docs/DEVELOPMENT_ENV.md) for instructions on setting up a development environment to work on and test RAMSTK.

## 🍞&nbsp; Authors

* **Doyle 'weibullguy' Rowland** - *Initial work* - [weibullguy](https://github.com/weibullguy)

## 📜&nbsp; License
This project is licensed under the BSD-3-Clause License - see the [LICENSE](https://github.com/ReliaQualAssociates/ramstk/blob/develop/LICENSE) file for details.

RAMSTK is also registered with the United States Copyright Office under
 registration number TXu 1-896-035.

## Similar Products

The following are commercially available products that perform RAMS analyses
.  We are not endorsing any of them; they are all fine products and may be a
 better fit for you or your organization depending on your needs and budget
 .  Obviously, we would prefer you use RAMSTK.

* [PTC Windchill Quality](https://www.ptc.com/en/products/plm/capabilities/quality)
* [ReliaSoft Synthesis](https://www.reliasoft.com/products)
