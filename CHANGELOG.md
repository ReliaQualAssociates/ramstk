## 1.0.0 (Three Nines)

### Bug Fixes
* Can now close RAMSTK Program database without closing RAMSTK [Close #21]
* Add error handlers [Close #78][Close #83][Close #94]

### New and Improved
* RAMSTK
  - Module View is now read only [Close #3]
  - Add busy cursor [Close #37]
  - Add pop-up menus on right-click. [Close #91]
* Hardware module
  - Program database tables updated to new API. 
  - Data model and data controller updated to new API. 
  - Module View updated to new API. 
  - Work Views updated to new API.
  - Component calculations moved to modules under analyses/prediction directory.
* Assistants
  - Set Options assistant [Close #60]
  - Set Preferences assistant [Close #60]
  - Import project assistant [Close #13]
  - Export/Report assistant [Close #4][Close #9][Close #19][Close #41]

### Out with the Old
* Remove Delete Project assistant - use the rm command.

### Quality Assurance
* Apply RAMSTK coding conventions throughout the codebase.
  - [Close #98]
  - [Close #101]
  - [Close #106]
  - [Close #114]
  - [Close #110]
  - [Close #113]
  - [Close #111]
  - [Close #108]
  - [Close #112]
  - [Close #102]
  - [Close #109]
* Refactor codebase to use consistent method/function calls.
  - [Close #95]
  - [Close #97]
  - [Close #105]
* Merge pull request #67 from rakhimov/yapf (thank you for your input).

### Other
* Open "staging" branch to hold modules still requiring update to new API.
* Update to use pytest instead of nose.
* Cleanup and reorganize package directory/file structure.
* Rename files and update references from rtk to ramstk.

## v0.4.0 (2017-12-11)
### Other
* First RTK release with the following modules updated to the new API:
  - Revision Module 
  - Function Module 
  - Requirement/Specification Module 
  - Validation Module
