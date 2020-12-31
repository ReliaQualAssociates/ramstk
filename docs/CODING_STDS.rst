The coding standards below are probably out of date so you might review some
of the existing code base to see how badly I haven't followed my own standards.

Naming Conventions for RAMSTK
-----------------------------

1000. Naming conventions shall, generally, follow the guidance provided in PEP8.

1100. *Constants and Variables*
#. All RAMSTK global constants shall be defined in the configuration module.
#. Constants shall be:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | All UPPERCASE with spaces replaced by underscores (\_).                   |
   +---------------------------------------------------------------------------+
   | Prefaced by RAMSTK\_ to identify it as an RAMSTK constant.                |
   +---------------------------------------------------------------------------+
   | A minimum of twelve characters (RAMSTK\_ is 7) and a maximum of 30        |
   | characters.                                                               |
   +---------------------------------------------------------------------------+

#. Variables shall be:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | All lowercase with spaces replaced by underscores (\_).                   |
   +---------------------------------------------------------------------------+
   | A minimum of three characters and a maximum of 30 characters.             |
   +---------------------------------------------------------------------------+
   | A descriptive name when used for program flow control (e.g., for or       |
   | while loops).  For example, _index rather than i or _key rather than k.   |
   +---------------------------------------------------------------------------+
   | Preceded by a single underscore when private in scope.                    |
   +---------------------------------------------------------------------------+

1200. *Classes and Modules*
#. Module names shall be:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | All lowercase with spaces replaced by underscores (\_).                   |
   +---------------------------------------------------------------------------+

#. Class names shall be:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | In the CapWords format.                                                   |
   +---------------------------------------------------------------------------+
   | Alpha characters only.                                                    |
   +---------------------------------------------------------------------------+
   | Prefaced by RAMSTK.                                                       |
   +---------------------------------------------------------------------------+
   | A minimum of 11 characters (RAMSTK is 6) and a maximum of 30 characters.  |
   +---------------------------------------------------------------------------+
   | Suffixed by 'Error' when defining an exception class.                     |
   +---------------------------------------------------------------------------+

1300. *Attributes*
#.  Class attributes shall be:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | All lowercase with spaces replaced by underscores (\_).                   |
   +---------------------------------------------------------------------------+

#. Private instance attribute shall be:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | All lowercase with spaces replaced by underscores (\_).                   |
   +---------------------------------------------------------------------------+
   | Prefaced with _dic to indicate it is a dictionary.                        |
   +---------------------------------------------------------------------------+
   | Prefaced with _lst to indicate it is a a list.                            |
   +---------------------------------------------------------------------------+
   | Prefaced with _tpl to indicate it is a tuple.                             |
   +---------------------------------------------------------------------------+
   | Prefaced with a single underscore (\_) to indicate it is a scalar.        |
   +---------------------------------------------------------------------------+

#. Public instance attributes shall be:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | All lowercase with spaces replaced by underscores (\_).                   |
   +---------------------------------------------------------------------------+
   | Prefaced with dic to indicate it is a dictionary.                         |
   +---------------------------------------------------------------------------+
   | Prefaced with lst to indicate it is a a list.                             |
   +---------------------------------------------------------------------------+
   | Prefaced with tpl to indicate it is a tuple.                              |
   +---------------------------------------------------------------------------+
   | Un-prefaced to indicate it is a scalar.                                   |
   +---------------------------------------------------------------------------+

1400. *Functions and Methods*
#. Functions and methods shall be:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | All lowercase with underscores (\_) replacing spaces.                     |
   +---------------------------------------------------------------------------+
   | A minimum of five characters and a maximum of 50 characters.              |
   +---------------------------------------------------------------------------+
   | Prefaced by a single underscore (\_) if not a public function or method.  |
   +---------------------------------------------------------------------------+

#. Function and method arguments shall be:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | All lowercase with underscores (\_) replacing spaces.                     |
   +---------------------------------------------------------------------------+
   | A minimum of five characters and a maximum of 30 characters.              |
   +---------------------------------------------------------------------------+
   | Prefaced by a double underscore (\_\_) if it is unused in the function    |
   | or methods (e.g., in widget callback methods).                            |
   +---------------------------------------------------------------------------+

1500. *Tags*
#. Tags may be used to assist in place holding during development.

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | FIXME to indicate non-working code that needs to be re-worked before      |
   | check-in.                                                                 |
   +---------------------------------------------------------------------------+
   | TODO to indicate missing code/functionality that needs to be added.       |
   +---------------------------------------------------------------------------+
   | CR to point to the RAMSTK GitHub project issue tracking the condition.    |
   +---------------------------------------------------------------------------+

#. FIXME tags shall:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | **NOT** be included in any code checked in to the RAMSTK git repository.  |
   +---------------------------------------------------------------------------+
   | Be converted to a CR tag when an issue is created to track the condition. |
   +---------------------------------------------------------------------------+

#. TODO tags shall:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | **NOT** be included in any code checked in to the RAMSTK git repository.  |
   +---------------------------------------------------------------------------+
   | Be converted to an ISSUE tag when an issue is created to track the        |
   | condition.                                                                |
   +---------------------------------------------------------------------------+

#. CR tags shall:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | Include the issue number and brief description.  For example:             |
   |                                                                           |
   |    CR 88: Handle Errors in FMEA WorkView _do_load_tree() Method           |
   +---------------------------------------------------------------------------+

Design Conventions for RAMSTK
-----------------------------

2000. *General Architecture*
#. Data **shall** be stored in referential databases.
#. RAMSTK **shall** follow a MVC architecture.
#. Controllers are referred to as managers.
#. Data managers are used to control the flow of data between the data base, the views, and the analysis manager.
#. Analysis managers are used to control the flow of analyses.

2100. *Data Managers*
#. There **shall** be a data manager meta-class.
#. All data managers **shall** have the following methods:

    #. _on_select_revision(self, attributes)
    #. do_connect(self, dao)
    #. do_create_all_codes(self, prefix)
    #. do_delete(self, node_id, table)
    #. do_get_attributes(self, node_id, table)
    #. do_select(self, node_id, table)
    #. do_set_attributes(self, node_id, package)
    #. do_set_tree(self, module_tree)
    #. do_update_all(self)
    #. do_get_tree(self)
    #. do_select_all(self, attributes)
    #. do_update(self, node_id)

#. Any or all of the data manager methods *should* be abstracted to the data manager meta-class.
#. For data manager functions or methods unique to a particular RAMSTK work stream module, naming shall adhere to the following conventions:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | All methods should be named the same as the data model method and         |
   | prefaced with request\_.  For example:                                    |
   |                                                                           |
   |    request_do_calculate_rpn(self)                                         |
   |    request_get_planned_burndown(self)                                     |
   +---------------------------------------------------------------------------+
   | Shall be public in scope.                                                 |
   +---------------------------------------------------------------------------+
   | Conform with all naming conventions.                                      |
   +---------------------------------------------------------------------------+

2200. *Analysis Managers*
#. There **shall** be an analysis manager meta-class.
#. All analysis managers **shall** have the following methods:

2300. *Data Models*
#. Models provide abstraction of the data base tables.
#. There **shall** be one model per data base table.
#. Data models may have the following public/private methods/functions:
#. For data model functions or methods unique to a particular RAMSTK module, naming shall adhere to the following conventions:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | If the function or method responds to a user request, it shall begin      |
   | with do\_ (public) or \_do\_ (private).  For example:                     |
   |                                                                           |
   |    _do_add_actions(self, cause_id, parent_id)                             |
   |    _do_calculate_rpn(self)                                                |
   +---------------------------------------------------------------------------+
   | If the function or method retrieves something, it shall begin with get\_  |
   | (public) or \_get\_ (private).  For example:                              |
   |                                                                           |
   |    get_actual_burndown(self)                                              |
   |    get_assessment_points(self)                                            |
   |    get_planned_burndown(self)                                             |
   +---------------------------------------------------------------------------+
   | If the function or method does something, it should begin with set\_      |
   | (public) or \_set\_ (private).  For example:                              |
   |                                                                           |
   |    \_set\_assessment\_points(self, **kwargs)                              |
   +---------------------------------------------------------------------------+
   | Conform with all naming conventions.                                      |
   +---------------------------------------------------------------------------+

2400. GUI Components
#. If the function or method creates a simple or aggregate widget, it shall begin with make (public) or _make_ (private).

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | _make_assessment_inputs_page(self)                                        |
   +---------------------------------------------------------------------------+
   | _make_buttonbox(self)                                                     |
   +---------------------------------------------------------------------------+

#. If the function or method is a callback signal that is not a user request, it should begin with on (public) or _on_ (private).

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | _on_focus_out(self, entry, new_text)                                      |
   +---------------------------------------------------------------------------+
   | _on_edit(self, __cell, path, new_text, position)                          |
   +---------------------------------------------------------------------------+

#. If the function or method is a callback signal that is a user request (button press, etc.), it should be begin with do\_request\_ (public) or _do_request_ (private).

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | _do_request_calculate(self, __button)                                     |
   +---------------------------------------------------------------------------+
   | _do_request_update(self, __button)                                        |
   +---------------------------------------------------------------------------+

#. View functions and methods should, generally, be "private" (prefaced by a single underscore '_') as they would only need to be called by other View functions and methods and would not be part of the public API.

2500. List Views
#. All List Views shall have the following public methods:
#. All List Views shall have the following private methods:
#. For List View functions or methods unique to a particular RAMSTK module, naming shall adhere to the following conventions:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | Be private in scope.                                                      |
   +---------------------------------------------------------------------------+
   | Conform with all naming conventions.                                      |
   +---------------------------------------------------------------------------+

2600. Module Views
#. All Module Views shall have the following public methods:
#. All Module Views shall have the following private methods:
#. Module Views may have the following public/private methods/functions:
#. Module View functions or methods unique to a particular RAMSTK module, naming shall adhere to the following conventions:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | Be private in scope.                                                      |
   +---------------------------------------------------------------------------+
   | Conform with all naming conventions.                                      |
   +---------------------------------------------------------------------------+

2700. Work Views
#. All Work Views shall have the following public methods:
#. All Work Views shall have the following private methods:
#. Work Views may contain one or more of the following private methods as needed:
#. For Work View functions or methods unique to a particular RAMSTK module, naming shall adhere to the following conventions:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | Be private in scope.                                                      |
   +---------------------------------------------------------------------------+
   | Conform with all naming conventions.                                      |
   +---------------------------------------------------------------------------+
