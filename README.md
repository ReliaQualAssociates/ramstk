# The RAMS ToolKit (RAMSTK)
> A ToolKit for **R**eliability, **A**vailability, **M**aintainability, and
> **S**afety (RAMS) analyses.

<table>
    <tr>
        <th>Documentation</th>
        <td>
            <img alt="Read the Docs" src="https://img.shields.io/readthedocs/ramstk?label=RTD">
        </td>
    </tr>
    <tr>
        <th>Tests</th>
        <td>
        <img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/ReliaQualAssociates/ramstk/RAMSTK%20Test%20Suite?label=Build%20%26%20Test">
        <img alt="Codecov" src="https://img.shields.io/codecov/c/github/ReliaQualAssociates/ramstk?label=Codecov">
        <img alt="Coveralls github" src="https://img.shields.io/coveralls/github/ReliaQualAssociates/ramstk?label=Coveralls">
    </td>
    </tr>
    <tr>
        <th>Quality</th>
        <td>
            <img alt="CodeFactor Grade" src="https://img.shields.io/codefactor/grade/github/ReliaQualAssociates/ramstk?label=CodeFactor">
            <a href="https://www.deepcode.ai/app/gh/ReliaQualAssociates/ramstk/_/dashboard?utm_content=gh%2FReliaQualAssociates%2Framstk"><img alt="Deep Code" src="https://www.deepcode.ai/api/gh/badge?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybTEiOiJnaCIsIm93bmVyMSI6IlJlbGlhUXVhbEFzc29jaWF0ZXMiLCJyZXBvMSI6InJhbXN0ayIsImluY2x1ZGVMaW50IjpmYWxzZSwiYXV0aG9ySWQiOjI1MTA4LCJpYXQiOjE2MDkxMzcwNTl9.R5P6VLkyK1LK6Jc5PjJ8QrLRq6zNuVxnzdjZCJbH7_k"></a>
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

## 🎨 Features

RAMSTK is built on the concept of modules where a module is a collection of
 related information and/or analyses pertinent to system development.  The
  modules currently included in RAMSTK are:

* Function Module
  - Functional decomposition
  - Functional FMEA
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

These instructions will get RAMSTK up and running on your local machine
. Note that the Makefile contains all the commands needed to install or work
 with RAMSTK.  You should consult the help output for more information.

GitHub and PyPi releases will be made available once RAMSTK reaches v1.0.0
.  Until then, the only way to install RAMSTK is to clone the repository or
 download the source package and follow the instructions below.

### Prerequisites

I use [pip-tools](https://github.com/jazzband/pip-tools) to manage the
 dependencies for RAMSTK while I'm developing so the requirements.txt file
  is formated for use with the pip-sync command.  However, it will also work
   with pip.

```sh
$ pip install -r requirements.txt
```

should get all the needed runtime requirements installed if they're not
 already.

If you're planning to do some development work on RAMSTK, the following
 would be the better approach:

```sh
$ pip install pyenv
$ make mkvenv
$ make usevenv ramstk-venv
$ pip install pip-tools
$ make depends
```

This will install [pyenv](https://github.com/pyenv/pyenv), create a virtual
 environment with the default name of ramstk-venv, activate that virtual
  environment, install pip-tools, and then install all the RAMSTK
   dependencies needed for testing, development, and runtime.

RAMSTK uses [postgresql](https://www.postgresql.org/) for it's database
 engine.  You'll need to have a user with read/write access to a postgresql
  server to use RAMSTK.

### Download

Install any missing RAMSTK dependencies using pip, your package manager, and
/or build from source.  Then download the <version> of RAMSTK source from
 GitHub Releases you wish to install.

```sh
$ wget https://github.com/ReliaQualAssociates/ramstk/archive/v<tag>.tar.gz
$ tar -xf v<tag>.tar.gz
$ cd ramstk-<tag>
$ make install
```

The install target recognizes PREFIX=<non-default install path> so you can
 install RAMSTK in your $HOME or a virtual environment.  Since RAMSTK is
  still a version 0 product, it's highly recommended that you install in a
   virtual environment.

```sh
$ wget https://github.com/ReliaQualAssociates/ramstk/archive/v<tag>.tar.gz
$ tar -xf v<tag>.tar.gz
$ cd ramstk-<tag>
$ make PREFIX=$VIRTUAL_ENV install
```

### Running the Tests

To run the entire test suite for RAMSTK after installing, simply execute:

```sh
$ make test
```

To run the test suite with coverage, execute:

```sh
$ make coverage
```

To run specific tests or groups of tests, use pytest:

```sh
$ pytest -m integration tests/modules/test_allocation.py
$ pytest -m calculation tests/analyses/prediction
```

## 🔨 Usage

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

## 💬 Contributing

Please read [CONTRIBUTING.md](https://github.com/ReliaQualAssociates/ramstk/tree/develop/docs/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

Also read [DEVELOPMENT_ENV.md](https://github.com/ReliaQualAssociates/ramstk/tree/develop/docs/DEVELOPMENT_ENV.md) for instructions on setting up a development environment to work on and test RAMSTK.

## 🍞 Authors

* **Doyle 'weibullguy' Rowland** - *Initial work* - [weibullguy](https://github.com/weibullguy)

## 📜 License
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
