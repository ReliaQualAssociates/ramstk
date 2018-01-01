## (unreleased)

### Other

* Adding .gitchangelog.rc so CHANGELOGS can start being generated. [Doyle Rowland]

* Merge branch 'feature/connections' into develop. [Doyle Rowland]

* Add additional connection type. [Doyle Rowland]

  - Add PCB edge connectors.
  - Add IC socket connectors.
  - Update requirements.txt with proper capatalization for package names.
  - Add commands to ISSUE_TEMPLATE.md to get the package versions needed.

* Add Connection component class. [Doyle Rowland]

  - Update setup.py to include only the packages that have been updated.
  - New file analyses/prediction/Connection.py.
  - New file tests/_analyses/prediction/TestConnection.py.
  - Add Connection to API documentation.
  - Add TestConnection to TestPackage.py.
  - New file RTKCommonDB.sql added to tools/ for rapid re-creation as common DB is populated.

* Remove more dead files. [Doyle Rowland]

* Remove old capacitor files. [Doyle Rowland]

* Merge branch 'feature/calculate_all' into develop. [Doyle Rowland]

* Fix items not saving after calculations. [Doyle Rowland]

  - Set work view calculate button insensitive when an assembly is selected.
  - Add code to iteratively set the attributes after calulating the entire system.
  - Add voltage stress calculation to overstress method too (allows it calculate even when using parts count method).

* Update hardware module view with calculation results. [Doyle Rowland]

  - Fix cost calculations so parent items are sums of child items.
  - Remove code to update module view from work view.
  - Add _on_calculate method to hardware module view.
  - Subscribe _on_calculate to 'calculatedHardware' pubsub message.

* Add method to iteratively calculate the entire hardware system. [Doyle Rowland]

  - Add total_cost field to RTKHardware.
  - Update TestRTKHardware to account for total_cost field.
  - Add temperature_knee field to RTKDesignElectric (for derate curves).
  - Update TestRTKDesignElectric to account for temperature_knee field.
  - Add calculate_all method to HardwareBoM data model.
  - Moved adjustment calculations into separate staticmethods (allows them to be called for assemblies).
  - Add request_calculate_all method to HardwareBoM data controller.
  - Add _do_request_calculate_all method and button to buttonbox for Hardware module view.
  - Moved code that loads Hardware assessment results widgets into new _do_load_page() method.
  - Set new _do_load_page() method to be called in response to 'calculatedHardware' message.

* Fix hardware insert method. [Doyle Rowland]

  - Handle DuplicatedNodeIdError in data models.
  - Return focus to previously selected row after update.

* Merge branch 'hotfix/insert_hardware' into develop. [Doyle Rowland]

* Create ISSUE_TEMPLATE.md. [Doyle Rowland]

* Merge branch 'feature/capacitors' into develop. [Doyle Rowland]

* Add derate plot with operating point to capacitor. [Doyle Rowland]

* Add capacitor result views. [Doyle Rowland]

  - Add quality RTKComboBox() to assessment intput view.
  - Convert assessment input to use only request_get_attributes().
  - Add AssessmentResults class.
  - Add StressResults class.
  - Update format from 'g' to 'G' so numbers can be displayed in scientific notation.

* Update methods to calculate parameters. [Doyle Rowland]

  - Add logistics failure rate.
  - Add MTBF calculations.
  - Add reliability calculations.
  - Add variance calculations for above parameters.
  - Add cost calculations.

* Update methods in Hardware package. [Doyle Rowland]

  Changes simply access to and saving of attributes accross tables and in BoM.

  - Return BoM attribute dict from get_attributes().
  - Set BoM data to attribute dict and then set each table's attributes in set_attributes().
  - Update every table in update() and create aggregate error code and error message.

* Clean up pylint and PEP8 errors/warnings. [Doyle Rowland]

  - Remove rtk/hardware/ModuleBook.py as it is no longer needed.

* Add Capacitor assessment and stress inputs Work View. [Doyle Rowland]

  - Add containers for Capacitor assessment inputs.
  - Add containers for Capacitor stress inputs.
  - Add code to Hardware Work View to embed component containers.
  - Update TestCapacitor.py to account for ac and DC operating voltage.

* Renamed kwargs to attributes for ease of understanding. [Doyle Rowland]

* Add capacitor calculation module. [Doyle Rowland]

  - Add functions for calculating capacitor attributes (analyses.prediction.Capacitor).
  - Update TestCapacitor.py to account for new functions.
  - Add TestCapacitor.py to tests/_hardware.TestPackage.py.
  - Add Capacitor functions to API documentation.

* Update hardware model and controller. [Doyle Rowland]

  These changes make the aggregate data model/controller API compatible with the simple data model/controller API for a consistent RTK API.

  - Select method changed to return RTK Program database table record.
  - Update method changed to update each table using table-specific data model methods.
  - Add calculate method to Hardware BoM data model.
  - Add request_select method to Hardware BoM data controller.
  - Add request_calculate method to Hardware BoM data controller.
  - Update Hardware BoM test suite to account for above changes.
  - Update Hardware Work View methods to use new data controller methods.

* Removed unneeded hardware module files. [Doyle Rowland]

* Merge branch 'develop' of https://github.com/weibullguy/rtk into develop. [Doyle Rowland]

  - Fix conflicts:
  	rtk/Configuration.py
  	rtk/dao/RTKDesignElectric.py
  	rtk/dao/RTKDesignMechanic.py
  	rtk/dao/RTKMilHdbkF.py
  	rtk/dao/RTKNSWC.py
  	rtk/dao/RTKReliability.py
  	rtk/validation/Validation.py
  	rtk/validation/WorkBook.py
  	tests/_dao/TestRTKDesignElectric.py
  	tests/_dao/TestRTKDesignMechanic.py
  	tests/_dao/TestRTKHardware.py
  	tests/_dao/TestRTKMilHdbkF.py
  	tests/_dao/TestRTKNSWC.py
  	tests/_dao/TestRTKReliability.py
  	tests/unit/TestHardware.py
  	tests/unit/TestHardwareBoM.py

* Merge pull request #67 from rakhimov/yapf. [Doyle Rowland]

  Apply yapf formatting

* Apply yapf formatting. [rakhimov]

  Fix all the formatting issues in one go with yapf.

* Merge branch 'feature/hardware_update' into develop. [Doyle Rowland]

* Add do_request for composite reference designator. [Doyle Rowland]

* Create hardware assessment results Work View. [Doyle Rowland]

  - Add duty cycle and mission time to assessment input work view.
  - Change default tooltip for RTKLabel to blank string.
  - Allow RTKScrolledWindow child widget to be None.

* Rearrange docs directory. [Doyle Rowland]

  - Move API documentation to api sub-directory.
  - Create user sub-directory for eventual user documentation.

* Create hardware assessment inputs Work View. [Doyle Rowland]

  - Add active and dormant temperature fields to RTKDesignElectric.
  - Add active and dormant temperature to test suites.
  - Change list of label text to class attribute.
  - Rename list of label text to simply _lst_label for all work views.
  - Add reliability attributes to hardware_format.xml.
  - Add coveralls badge to README.md (only 12% atm, need to improve).
  - Remove documentation section from README.md (just click on the badge).

* Add hardware work view general data page. [Doyle Rowland]

  - Create hardware work view.
  - Create hardware general data page.
  - Change RTK global attributes from Treelib tree()s to dicts.

* Add option to insert assembly or piece part; create composite ref des. [Doyle Rowland]

  - Update hardware data model to insert either an assembly or a piece part.
  - Update hardware data controller to pass appropriate parameters to insert assembly or piece part.
  - Update hardware module view to pass appropriate parameters to insert assembly or piece part.
  - Moved method to create the composite reference designators to the hardware module.
  - Update test suites to include inserting piece parts and creating composite ref des.

* Add CONTRIBUTING.md. [Doyle Rowland]

* Unabstracted _make_general_data_page() methods. [Doyle Rowland]

  The amount of duplicate code it eliminated ended up being very little.

* Added tools/StaticChecks.sh to repo. [Doyle Rowland]

* Added coveralls to Travis builds. [Doyle Rowland]

* Removed three widgets from base Work View. [Doyle Rowland]

  Moved the three widgets to each of the individual Work Views.  This may result in some duplication of code, but it makes it easier to deal with the fact that not all modules used each of the three.  The savings wasn't justified.

* Added Hardware Module View. [Doyle Rowland]

* Changed Hardware model to concatenate attributes. [Doyle Rowland]

  This results in one large dictionary of attributes, but using a list of table objects can't work when trying to load into the Module View.

* Added HardwareBoM controller to satisfy new API. [Doyle Rowland]

  - Create HardwareBoM data controller.
  - Updated HardwareBoM model to remove nodes from respective sub-model trees when deleting a Hardware item.
  - Created HardwareBoM controller test package.
  - Added HardwareBoM controller tests to package test suite.
  - Updated test packages to look for hardware ID 1 rather than 3.
  - Updated Hardware package API documentation.
  - Updated RTK database table CASCADEs.

* Merge branch 'feature/hardware_update' of https://github.com/weibullguy/rtk into feature/hardware_update. [Doyle Rowland]

  Conflicts:
  	tests/_hardware/TestHardware.py
  	tests/_hardware/TestPackage.py

* Updated RTK Program database tables for Hardware package. [Doyle Rowland]

  - Removed pragma statements from class and def lines.
  - Added pragma statements to specific lines to skip.
  - Updated Function data model to use revision_id in select_all().
  - Removed validation/Validation.py and validation/WorkBook.py.

* Moved data models from Hardware.py to Model.py. [Doyle Rowland]

  - Created data model for each RTK Program database table.
  - Created aggregate data model for Hardware BoM.
  - Created test file for each data model.
  - Created Hardware package test file including database tables and data models.
  - Updated test_setup.py to create known database condition for tests.
  - pydocstyle clean ups.

* Updated RTK Program database tables for Hardware package. [Doyle Rowland]

  - Removed pragma statements from class and def lines.
  - Added pragma statements to specific lines to skip.
  - Updated Function data model to use revision_id in select_all().
  - Removed validation/Validation.py and validation/WorkBook.py.

* Updated RTK Program database tables to return/use dict for attributes. [Doyle Rowland]

  - Updated RTKDesignElectric, RTKDesignMechanic, RTKHardware, RTKMilHdbkF, RTKNSWC, and RTKReliability.
  - Updated all test files.
  - Moved hardware test files into tests/_hardware directory.
  - Added tests/_hardware/TestPackage.py


## 0.0.0 (2017-07-29)

### Other

* Merge pull request #2 from weibullguy/add-code-of-conduct-1. [Andrew Rowland]

  Create CODE_OF_CONDUCT.md

* Create CODE_OF_CONDUCT.md. [Andrew Rowland]


