# Changelog

## [Unreleased](https://github.com/ReliaQualAssociates/ramstk/tree/HEAD)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v1.1.0...HEAD)

**Implemented enhancements:**

-  Move the code for adding Hardware:X matrix records to a seperate method that responds to the 'inserted\_hardware' signal. [\#249](https://github.com/ReliaQualAssociates/ramstk/issues/249)
-  Create and log a useful user and/or debug message in src/ramstk/dao/DAO.py. [\#239](https://github.com/ReliaQualAssociates/ramstk/issues/239)

**Closed issues:**

- PoF Setter Tests Seem to Try and Use Old Test Database [\#273](https://github.com/ReliaQualAssociates/ramstk/issues/273)

**Merged pull requests:**

- \[ImgBot\] Optimize images [\#219](https://github.com/ReliaQualAssociates/ramstk/pull/219) ([imgbot[bot]](https://github.com/apps/imgbot))

## [v1.1.0](https://github.com/ReliaQualAssociates/ramstk/tree/v1.1.0) (2020-04-25)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v1.0.5...v1.1.0)

**Implemented enhancements:**

- Provide Multiple Windows in GUI [\#286](https://github.com/ReliaQualAssociates/ramstk/issues/286)
-  Implement a DAO.db\_last\_id\(\) method to retrieve the value of the last ID from the database. [\#246](https://github.com/ReliaQualAssociates/ramstk/issues/246)
-  Remove the call to do\_set\_properties\(\) in the RAMSTKTextView.\_\_init\_\_\(\) method when all instances of RAMSTKTextView\(\) have been refactored. [\#237](https://github.com/ReliaQualAssociates/ramstk/issues/237)
-  Remove the call to do\_set\_properties\(\) in the RAMSTKEntry.\_\_init\_\_\(\) method when all instances of RAMSTKEntry\(\) have been refactored. [\#236](https://github.com/ReliaQualAssociates/ramstk/issues/236)
-  Remove the call to do\_set\_properties\(\) in the RAMSTKButton.\_\_init\_\_\(\) method when all instances of RAMSTKButton\(\) have been refactored. [\#235](https://github.com/ReliaQualAssociates/ramstk/issues/235)
-  Remove index in calls to the RAMSTKComboBox.do\_load\_combo\(\) method and then remove index from the argument list. [\#234](https://github.com/ReliaQualAssociates/ramstk/issues/234)
-  Remove the call to do\_set\_properties\(\) in the RAMSTKComboBox.\_\_init\_\_\(\) method when all instances of RAMSTKComboBox\(\) have been refactored. [\#233](https://github.com/ReliaQualAssociates/ramstk/issues/233)
- GTK3 Widgets Need Consistent Look and Feel [\#232](https://github.com/ReliaQualAssociates/ramstk/issues/232)
-  Move the status icon code out of the RAMSTK controller and into a GUI module. [\#228](https://github.com/ReliaQualAssociates/ramstk/issues/228)
- Tests/add coverage [\#298](https://github.com/ReliaQualAssociates/ramstk/pull/298) ([weibullguy](https://github.com/weibullguy))
- Feature/update validation gui [\#297](https://github.com/ReliaQualAssociates/ramstk/pull/297) ([weibullguy](https://github.com/weibullguy))
- Refactor/update requirements gui [\#296](https://github.com/ReliaQualAssociates/ramstk/pull/296) ([weibullguy](https://github.com/weibullguy))
- Enhancement - Add postgresql support. [\#294](https://github.com/ReliaQualAssociates/ramstk/pull/294) ([weibullguy](https://github.com/weibullguy))
- Refactor - Function gui update [\#293](https://github.com/ReliaQualAssociates/ramstk/pull/293) ([weibullguy](https://github.com/weibullguy))
- Update Revision views. [\#290](https://github.com/ReliaQualAssociates/ramstk/pull/290) ([weibullguy](https://github.com/weibullguy))
- Update RAMSTK Books [\#288](https://github.com/ReliaQualAssociates/ramstk/pull/288) ([weibullguy](https://github.com/weibullguy))
- Update RAMSTK Books [\#287](https://github.com/ReliaQualAssociates/ramstk/pull/287) ([weibullguy](https://github.com/weibullguy))
- Add boilerplates for GTK3 widgets; issue \#232. [\#284](https://github.com/ReliaQualAssociates/ramstk/pull/284) ([weibullguy](https://github.com/weibullguy))
- Add configurations to Options data manager [\#283](https://github.com/ReliaQualAssociates/ramstk/pull/283) ([weibullguy](https://github.com/weibullguy))
- Add RAMSTKLogManager [\#282](https://github.com/ReliaQualAssociates/ramstk/pull/282) ([weibullguy](https://github.com/weibullguy))
- Move import module to Exim package [\#281](https://github.com/ReliaQualAssociates/ramstk/pull/281) ([weibullguy](https://github.com/weibullguy))
- Move export and import classes to exim package [\#280](https://github.com/ReliaQualAssociates/ramstk/pull/280) ([weibullguy](https://github.com/weibullguy))

## [v1.0.5](https://github.com/ReliaQualAssociates/ramstk/tree/v1.0.5) (2019-08-18)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v1.0.4...v1.0.5)

**Implemented enhancements:**

-  Handle ValueError with an error code and error message in RAMSTKSimilarItem.set\_attributes\(\). [\#252](https://github.com/ReliaQualAssociates/ramstk/issues/252)
-  Log the returned messages. [\#248](https://github.com/ReliaQualAssociates/ramstk/issues/248)
-  Add range check on input factors \(1 - 10\) in RAMSTKAllocation.foo\_apportionment\(\). [\#247](https://github.com/ReliaQualAssociates/ramstk/issues/247)
-  Create and log a useful user and/or debug message in src/ramstk/dao/DAO.py. [\#245](https://github.com/ReliaQualAssociates/ramstk/issues/245)
-  Create and log a useful user and/or debug message in src/ramstk/dao/DAO.py. [\#244](https://github.com/ReliaQualAssociates/ramstk/issues/244)
-  Create and log a useful user and/or debug message in src/ramstk/dao/DAO.py. [\#243](https://github.com/ReliaQualAssociates/ramstk/issues/243)
-  Create and log a useful user and/or debug message in src/ramstk/dao/DAO.py. [\#242](https://github.com/ReliaQualAssociates/ramstk/issues/242)
-  Create and log a useful user and/or debug message in src/ramstk/dao/DAO.py. [\#240](https://github.com/ReliaQualAssociates/ramstk/issues/240)
-  Create and log a useful user and/or debug message in src/ramstk/dao/DAO.py. [\#238](https://github.com/ReliaQualAssociates/ramstk/issues/238)
- Handle ValueError with an error code and error message in RAMSTKSimilarItem.set\_attributes\(\). [\#226](https://github.com/ReliaQualAssociates/ramstk/issues/226)
- Move Similar Item Work View \_do\_request\_edit\_function\(\) method to a stand-alone assistant [\#212](https://github.com/ReliaQualAssociates/ramstk/issues/212)
- Refactor \_on\_combo\_changed\(\) and \_on\_focus\_out\(\) methods in component workviews to eliminate duplicate code. [\#208](https://github.com/ReliaQualAssociates/ramstk/issues/208)
- Refactor workviews to have \_\_make\_ui\(\), \_\_set\_properties\(\), \_\_set\_callbacks\(\) methods [\#207](https://github.com/ReliaQualAssociates/ramstk/issues/207)
- Refactor matrix views to move common code to meta-class [\#206](https://github.com/ReliaQualAssociates/ramstk/issues/206)
- Refactor \_on\_combo\_changed\(\) and \_on\_focus\_out\(\) methods in component workviews to eliminate duplicate code. [\#205](https://github.com/ReliaQualAssociates/ramstk/issues/205)
- Refactor matrix views to move common code to meta-class [\#203](https://github.com/ReliaQualAssociates/ramstk/issues/203)
- Refactor matrix views to move common code to meta-class [\#202](https://github.com/ReliaQualAssociates/ramstk/issues/202)
- Refactor matrix views to move common code to meta-class [\#201](https://github.com/ReliaQualAssociates/ramstk/issues/201)
- Refactor \_on\_combo\_changed\(\) and \_on\_focus\_out\(\) methods to eliminate duplicate code [\#200](https://github.com/ReliaQualAssociates/ramstk/issues/200)
- Offload to \_\_main\_\_.py [\#279](https://github.com/ReliaQualAssociates/ramstk/pull/279) ([weibullguy](https://github.com/weibullguy))
- Add log file config variables [\#278](https://github.com/ReliaQualAssociates/ramstk/pull/278) ([weibullguy](https://github.com/weibullguy))
- Add utilities tests [\#277](https://github.com/ReliaQualAssociates/ramstk/pull/277) ([weibullguy](https://github.com/weibullguy))
- Move site config to toml [\#276](https://github.com/ReliaQualAssociates/ramstk/pull/276) ([weibullguy](https://github.com/weibullguy))
- Rewrite database drivers [\#275](https://github.com/ReliaQualAssociates/ramstk/pull/275) ([weibullguy](https://github.com/weibullguy))
- Update Makefile and other tools [\#274](https://github.com/ReliaQualAssociates/ramstk/pull/274) ([weibullguy](https://github.com/weibullguy))
- Group program db tests into classes [\#271](https://github.com/ReliaQualAssociates/ramstk/pull/271) ([weibullguy](https://github.com/weibullguy))
- Update preferences to new API [\#270](https://github.com/ReliaQualAssociates/ramstk/pull/270) ([weibullguy](https://github.com/weibullguy))
- update options to new API [\#269](https://github.com/ReliaQualAssociates/ramstk/pull/269) ([weibullguy](https://github.com/weibullguy))
- update physics of failure to new API [\#268](https://github.com/ReliaQualAssociates/ramstk/pull/268) ([weibullguy](https://github.com/weibullguy))
- refactor: update FMEA to new API [\#267](https://github.com/ReliaQualAssociates/ramstk/pull/267) ([weibullguy](https://github.com/weibullguy))
- chore: add makefile [\#266](https://github.com/ReliaQualAssociates/ramstk/pull/266) ([weibullguy](https://github.com/weibullguy))
- refactor\(Val\): add matrix manager [\#265](https://github.com/ReliaQualAssociates/ramstk/pull/265) ([weibullguy](https://github.com/weibullguy))
- refactor: add status to validation [\#264](https://github.com/ReliaQualAssociates/ramstk/pull/264) ([weibullguy](https://github.com/weibullguy))
- chore: The Great Renaming [\#263](https://github.com/ReliaQualAssociates/ramstk/pull/263) ([weibullguy](https://github.com/weibullguy))
- update validation to new API [\#262](https://github.com/ReliaQualAssociates/ramstk/pull/262) ([weibullguy](https://github.com/weibullguy))
- update stakeholder model/controller [\#261](https://github.com/ReliaQualAssociates/ramstk/pull/261) ([weibullguy](https://github.com/weibullguy))
- update requirement module to new API [\#260](https://github.com/ReliaQualAssociates/ramstk/pull/260) ([weibullguy](https://github.com/weibullguy))
- Feature/update programdb models [\#259](https://github.com/ReliaQualAssociates/ramstk/pull/259) ([weibullguy](https://github.com/weibullguy))
- feature/refactor function [\#256](https://github.com/ReliaQualAssociates/ramstk/pull/256) ([weibullguy](https://github.com/weibullguy))
- update documentation [\#255](https://github.com/ReliaQualAssociates/ramstk/pull/255) ([weibullguy](https://github.com/weibullguy))
- feature/revision refactor [\#254](https://github.com/ReliaQualAssociates/ramstk/pull/254) ([weibullguy](https://github.com/weibullguy))
- Feature/make analyses mvc [\#253](https://github.com/ReliaQualAssociates/ramstk/pull/253) ([weibullguy](https://github.com/weibullguy))
- Add target to docs/Makefile to auto publish gh-pages [\#223](https://github.com/ReliaQualAssociates/ramstk/pull/223) ([weibullguy](https://github.com/weibullguy))
- Refactor MIL-HDBK-217F part stress methods [\#220](https://github.com/ReliaQualAssociates/ramstk/pull/220) ([weibullguy](https://github.com/weibullguy))
- Move docs to GitHub Pages [\#217](https://github.com/ReliaQualAssociates/ramstk/pull/217) ([weibullguy](https://github.com/weibullguy))
- Refactor piQ assignment for parts count analyses [\#216](https://github.com/ReliaQualAssociates/ramstk/pull/216) ([weibullguy](https://github.com/weibullguy))
- Issue \#204: Remove duplicate code in overstressed methods [\#214](https://github.com/ReliaQualAssociates/ramstk/pull/214) ([weibullguy](https://github.com/weibullguy))
- Feature/similar item undup code [\#213](https://github.com/ReliaQualAssociates/ramstk/pull/213) ([weibullguy](https://github.com/weibullguy))

**Fixed bugs:**

- add method to delete usage profile elements [\#258](https://github.com/ReliaQualAssociates/ramstk/pull/258) ([weibullguy](https://github.com/weibullguy))
- add method to delete failure definition [\#257](https://github.com/ReliaQualAssociates/ramstk/pull/257) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- Add devtools dir and a few helper scripts [\#224](https://github.com/ReliaQualAssociates/ramstk/pull/224) ([weibullguy](https://github.com/weibullguy))

## [v1.0.4](https://github.com/ReliaQualAssociates/ramstk/tree/v1.0.4) (2019-05-21)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v1.0.2...v1.0.4)

**Implemented enhancements:**

- PyGTK deprecation [\#58](https://github.com/ReliaQualAssociates/ramstk/issues/58)
- Support Python 3 [\#57](https://github.com/ReliaQualAssociates/ramstk/issues/57)

## [v1.0.2](https://github.com/ReliaQualAssociates/ramstk/tree/v1.0.2) (2019-05-10)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v1.0.3...v1.0.2)

**Implemented enhancements:**

- Update to Python 3 and pygobject. [\#198](https://github.com/ReliaQualAssociates/ramstk/pull/198) ([weibullguy](https://github.com/weibullguy))

## [v1.0.3](https://github.com/ReliaQualAssociates/ramstk/tree/v1.0.3) (2019-04-20)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v1.0.1...v1.0.3)

## [v1.0.1](https://github.com/ReliaQualAssociates/ramstk/tree/v1.0.1) (2018-10-09)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v1.0.0...v1.0.1)

## [v1.0.0](https://github.com/ReliaQualAssociates/ramstk/tree/v1.0.0) (2018-09-30)

[Full Changelog](https://github.com/ReliaQualAssociates/ramstk/compare/v1.0.0.rc1...v1.0.0)

**Fixed bugs:**

- Import Hardware Does Not Create Similar Item Table Records [\#140](https://github.com/ReliaQualAssociates/ramstk/issues/140)
- New RAMSTK Program Database Not Opening; Must Restart RAMSTK [\#139](https://github.com/ReliaQualAssociates/ramstk/issues/139)



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
