# Changelog

## [v0.19.0](https://github.com/ReliaQualAssociates/ramstk/tree/v0.19.0) (2022-06-12)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.18.1...v0.19.0)

New Features

- feat: add ability to export RAMSTK program data [\#1088](https://github.com/ReliaQualAssociates/ramstk/pull/1088) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- ci: add msys2 test suite to GH action workflow [\#1073](https://github.com/ReliaQualAssociates/ramstk/pull/1073) ([weibullguy](https://github.com/weibullguy))
- test: move tests into meta-class [\#1066](https://github.com/ReliaQualAssociates/ramstk/pull/1066) ([weibullguy](https://github.com/weibullguy))

## [v0.18.1](https://github.com/ReliaQualAssociates/ramstk/tree/v0.18.1) (2022-05-13)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.18.0...v0.18.1)

Bug Fixes

- feat: add methods to remove existing failure modes [\#1068](https://github.com/ReliaQualAssociates/ramstk/pull/1068) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- test: move tests into meta-class [\#1066](https://github.com/ReliaQualAssociates/ramstk/pull/1066) ([weibullguy](https://github.com/weibullguy))
- refactor: remove record\_id attribute from table models [\#1058](https://github.com/ReliaQualAssociates/ramstk/pull/1058) ([weibullguy](https://github.com/weibullguy))

## [v0.18.0](https://github.com/ReliaQualAssociates/ramstk/tree/v0.18.0) (2022-04-14)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.17.1...v0.18.0)

New Features

- feat: add derating criteria for fuse, relay, resistor, and switch [\#1051](https://github.com/ReliaQualAssociates/ramstk/pull/1051) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- build: add support for Python 3.9 and 3.10 [\#1043](https://github.com/ReliaQualAssociates/ramstk/pull/1043) ([weibullguy](https://github.com/weibullguy))
- build: drop support for Python 3.6 [\#1041](https://github.com/ReliaQualAssociates/ramstk/pull/1041) ([weibullguy](https://github.com/weibullguy))
- refactor: refactor the plot widget class [\#1040](https://github.com/ReliaQualAssociates/ramstk/pull/1040) ([weibullguy](https://github.com/weibullguy))

## [v0.17.1](https://github.com/ReliaQualAssociates/ramstk/tree/v0.17.1) (2022-03-30)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.17.0...v0.17.1)

Bug Fixes

- feat: add functions to set default MIL-HDBK-217F values [\#1038](https://github.com/ReliaQualAssociates/ramstk/pull/1038) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- test: move ATTRIBUTES from test files to conftest as a fixture [\#1031](https://github.com/ReliaQualAssociates/ramstk/pull/1031) ([weibullguy](https://github.com/weibullguy))

## [v0.17.0](https://github.com/ReliaQualAssociates/ramstk/tree/v0.17.0) (2022-03-11)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.16.3...v0.17.0)

New Features

- feat: rename fld\_action\_recommended to fld\_description [\#1028](https://github.com/ReliaQualAssociates/ramstk/pull/1028) ([weibullguy](https://github.com/weibullguy))

## [v0.16.3](https://github.com/ReliaQualAssociates/ramstk/tree/v0.16.3) (2022-03-10)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.16.2...v0.16.3)

Bug Fixes

- feature: use database triggers to add records on Hardware insert [\#1026](https://github.com/ReliaQualAssociates/ramstk/pull/1026) ([weibullguy](https://github.com/weibullguy))

## [v0.16.2](https://github.com/ReliaQualAssociates/ramstk/tree/v0.16.2) (2022-03-05)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.16.1...v0.16.2)

Bug Fixes

- fix: raise dialog to inform user of issues encountered while running application [\#1023](https://github.com/ReliaQualAssociates/ramstk/pull/1023) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- refactor: use keys instead of numbers for loading Hazard Analysis CellRendererCombos [\#1022](https://github.com/ReliaQualAssociates/ramstk/pull/1022) ([weibullguy](https://github.com/weibullguy))

## [v0.16.1](https://github.com/ReliaQualAssociates/ramstk/tree/v0.16.1) (2022-03-04)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.16.0...v0.16.1)

Bug Fixes

- fix: widget sensitivity not changing on subcategory change [\#1020](https://github.com/ReliaQualAssociates/ramstk/pull/1020) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- refactor: remove if-else control block in do\_select\_all\(\) method [\#1019](https://github.com/ReliaQualAssociates/ramstk/pull/1019) ([weibullguy](https://github.com/weibullguy))
- refactor: organize models by type [\#1016](https://github.com/ReliaQualAssociates/ramstk/pull/1016) ([weibullguy](https://github.com/weibullguy))
- chore\(deps\): bump xlsxwriter from 3.0.2 to 3.0.3 [\#1014](https://github.com/ReliaQualAssociates/ramstk/pull/1014) ([dependabot[bot]](https://github.com/apps/dependabot))
- refactor: remove pubsub "fail\_XX\_YY" messages [\#1013](https://github.com/ReliaQualAssociates/ramstk/pull/1013) ([weibullguy](https://github.com/weibullguy))

## [v0.16.0](https://github.com/ReliaQualAssociates/ramstk/tree/v0.16.0) (2022-02-25)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.22...v0.16.0)

New Features

- feat: add assistant to edit hazard analysis user defined functions [\#1011](https://github.com/ReliaQualAssociates/ramstk/pull/1011) ([weibullguy](https://github.com/weibullguy))

## [v0.15.22](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.22) (2022-02-24)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.21...v0.15.22)

Bug Fixes

- fix: validation tasks now load on insert [\#1009](https://github.com/ReliaQualAssociates/ramstk/pull/1009) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- refactor: move ramstk\_user to sub-package [\#1008](https://github.com/ReliaQualAssociates/ramstk/pull/1008) ([weibullguy](https://github.com/weibullguy))
- refactor: move ramstk\_type to sub-package [\#1007](https://github.com/ReliaQualAssociates/ramstk/pull/1007) ([weibullguy](https://github.com/weibullguy))
- refactor: move ramstk\_status to sub-package [\#1004](https://github.com/ReliaQualAssociates/ramstk/pull/1004) ([weibullguy](https://github.com/weibullguy))
- refactor: move ramstk\_stakeholders to sub-package [\#1003](https://github.com/ReliaQualAssociates/ramstk/pull/1003) ([weibullguy](https://github.com/weibullguy))
- refactor: move ramstk\_rpn to sub-package [\#1002](https://github.com/ReliaQualAssociates/ramstk/pull/1002) ([weibullguy](https://github.com/weibullguy))
- refactor: move ramstk\_model to sub package [\#1001](https://github.com/ReliaQualAssociates/ramstk/pull/1001) ([weibullguy](https://github.com/weibullguy))
- refactor: move ramstk\_method to sub-package [\#999](https://github.com/ReliaQualAssociates/ramstk/pull/999) ([weibullguy](https://github.com/weibullguy))
- refactor: move ramstk\_measurement to sub-package [\#997](https://github.com/ReliaQualAssociates/ramstk/pull/997) ([weibullguy](https://github.com/weibullguy))
- refactor: move ramstk\_manufacturer to sub-package [\#996](https://github.com/ReliaQualAssociates/ramstk/pull/996) ([weibullguy](https://github.com/weibullguy))
- refactor: move ramstk\_load\_history to sub-package [\#993](https://github.com/ReliaQualAssociates/ramstk/pull/993) ([weibullguy](https://github.com/weibullguy))
- refactor: move ramstk\_hazards to subpackage [\#992](https://github.com/ReliaQualAssociates/ramstk/pull/992) ([weibullguy](https://github.com/weibullguy))
- refactor: move ramstk\_group to a package [\#991](https://github.com/ReliaQualAssociates/ramstk/pull/991) ([weibullguy](https://github.com/weibullguy))
- refactor: make ramstk\_condition sub-package [\#990](https://github.com/ReliaQualAssociates/ramstk/pull/990) ([weibullguy](https://github.com/weibullguy))
- ci: fix typo in workflow file [\#989](https://github.com/ReliaQualAssociates/ramstk/pull/989) ([weibullguy](https://github.com/weibullguy))

## [v0.15.21](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.21) (2022-02-20)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.20...v0.15.21)

Bug Fixes

- fix: prevent adding sibling to top level hardware item [\#986](https://github.com/ReliaQualAssociates/ramstk/pull/986) ([weibullguy](https://github.com/weibullguy))

## [v0.15.20](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.20) (2022-02-20)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.19...v0.15.20)

Bug Fixes

- fix: hazard rate calculations not recursively calculated [\#982](https://github.com/ReliaQualAssociates/ramstk/pull/982) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- ci: add commit key so action can trigger new workflow [\#981](https://github.com/ReliaQualAssociates/ramstk/pull/981) ([weibullguy](https://github.com/weibullguy))

## [v0.15.19](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.19) (2022-02-19)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.18...v0.15.19)

Bug Fixes

- fix: component widgets not loading saved values [\#979](https://github.com/ReliaQualAssociates/ramstk/pull/979) ([weibullguy](https://github.com/weibullguy))

## [v0.15.18](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.18) (2022-02-18)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.17...v0.15.18)

## [v0.15.17](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.17) (2022-02-18)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.16...v0.15.17)

## [v0.15.16](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.16) (2022-02-17)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.15...v0.15.16)

## [v0.15.15](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.15) (2022-02-17)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.14...v0.15.15)

## [v0.15.14](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.14) (2022-02-12)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.13...v0.15.14)

## [v0.15.13](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.13) (2022-02-03)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.12...v0.15.13)

## [v0.15.12](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.12) (2022-01-28)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.11...v0.15.12)

## [v0.15.11](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.11) (2022-01-28)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.10...v0.15.11)

## [v0.15.10](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.10) (2022-01-27)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.9...v0.15.10)

## [v0.15.9](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.9) (2022-01-26)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.8...v0.15.9)

## [v0.15.8](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.8) (2022-01-25)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.7...v0.15.8)

## [v0.15.7](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.7) (2022-01-23)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.6...v0.15.7)

## [v0.15.6](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.6) (2022-01-23)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.5...v0.15.6)

## [v0.15.5](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.5) (2022-01-22)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.4...v0.15.5)

## [v0.15.4](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.4) (2022-01-20)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.3...v0.15.4)

## [v0.15.3](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.3) (2022-01-19)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.2...v0.15.3)

## [v0.15.2](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.2) (2022-01-10)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.1...v0.15.2)

## [v0.15.1](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.1) (2022-01-09)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.15.0...v0.15.1)

## [v0.15.0](https://github.com/ReliaQualAssociates/ramstk/tree/v0.15.0) (2022-01-07)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.14.2...v0.15.0)

## [v0.14.2](https://github.com/ReliaQualAssociates/ramstk/tree/v0.14.2) (2021-07-19)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.14.1...v0.14.2)

## [v0.14.1](https://github.com/ReliaQualAssociates/ramstk/tree/v0.14.1) (2021-02-05)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.14.0...v0.14.1)

## [v0.14.0](https://github.com/ReliaQualAssociates/ramstk/tree/v0.14.0) (2021-02-04)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.13.0...v0.14.0)

## [v0.13.0](https://github.com/ReliaQualAssociates/ramstk/tree/v0.13.0) (2021-01-26)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.12.3...v0.13.0)

## [v0.12.3](https://github.com/ReliaQualAssociates/ramstk/tree/v0.12.3) (2021-01-23)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.12.2...v0.12.3)

## [v0.12.2](https://github.com/ReliaQualAssociates/ramstk/tree/v0.12.2) (2021-01-23)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.12.1...v0.12.2)

## [v0.12.1](https://github.com/ReliaQualAssociates/ramstk/tree/v0.12.1) (2021-01-22)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.12.0...v0.12.1)

## [v0.12.0](https://github.com/ReliaQualAssociates/ramstk/tree/v0.12.0) (2021-01-19)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.11.0...v0.12.0)

## [v0.11.0](https://github.com/ReliaQualAssociates/ramstk/tree/v0.11.0) (2021-01-16)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v0.10.0...v0.11.0)



