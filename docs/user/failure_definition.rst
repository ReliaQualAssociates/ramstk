
.. _sec-failure-definitions:

Failure Definitions
===================

Failure definitions should be developed and agreed upon early in the
development program.  These failure definitions should be used throughout the
entire life-cycle of the product.  It is best to define failures as the
functions are being defined.  Functional failure definitions will fall into
one of the following categories:

#. Too much function.
#. Too little function.
#. Intermittent functionality.
#. Function not there when required.
#. Function present when not required.

As requirements/specifications are identified these functional failure
definitions can be amended with performance values or new, performance-based
failure definitions can be added.

Module Book
-----------
Failure Definitions are unable to be displayed in the Module Book.

Work Book
---------

.. figure:: ./figures/failure_definitions.png

Failure Definitions are displayed in the List Book when the Revision work
stream is selected in the Module Book.  The following attributes are
displayed for each Failure Definition.

.. tabularcolumns:: |r|l|l|
.. table:: **Failure Definition Attributes**

   +---------------+----------+------------------------------------+
   | Attribute     | Editable | Source of Data                     |
   +===============+==========+====================================+
   | Revision ID   | No       | Assigned by database.              |
   +---------------+----------+------------------------------------+
   | Function ID   | No       | Assigned by database.              |
   +---------------+----------+------------------------------------+
   | Definition ID | No       | Assigned by database.              |
   +---------------+----------+------------------------------------+
   | Definition    | Yes      | Free form entry.                   |
   +---------------+----------+------------------------------------+
   | End Effect?   | Yes      | Check button. (future)             |
   +---------------+----------+------------------------------------+

Adding and Removing Failure Definitions from the List Book
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When adding a new function, no failure definitions will exist.  To add a new
Failure Definition to the open `RAMSTK` Program database, select the function
in the module book you'd like to add a failure definition and then:

* Press the 'Add' button to the left of the definition list.
* Right click on the definition list and select 'Add' from the pop-up menu.

This will add a new Failure Definition that is associated with the selected
function.

To remove the currently selected Failure Definition from the open `RAMSTK`
Program database:

* Press the 'Remove' button to the left of the definition list.
* Right click on the definition list and select 'Remove' from the pop-up menu.

You will be presented with a dialog confirming you want to delete the selected
Failure Definition and all associated data.  Confirm your intentions to complete
the removal.

Saving Failure Definitions from the List Book
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To save changes to the currently selected Failure Definition

* Press the 'Save' button to the left of the definition list.
* Right click on the definition list and select 'Save' from the pop-up menu.

All pending changes to the currently selected Failure Definition are committed
to the open `RAMSTK` Program database.

To save changes to all Failure Definitions:

* Press the 'Save All' button to the left of the definition list.
* Right click on the definition list and select 'Save All' from the pop-up menu.

All pending changes to all Failure Definitions associated with the selected
Revision are committed to the open `RAMSTK` Program database.

Analyzing Failure Definitions
-----------------------------
There are no analyses associated with Failure Definitions.
