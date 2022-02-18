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
   | Be converted to an CR tag when an issue is created to track the condition.|
   +---------------------------------------------------------------------------+

#. CR tags shall:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | Include the issue number and brief description.  For example:             |
   |                                                                           |
   |    CR 88: Handle Errors in FMEA WorkView \_do\_load\_tree() Method        |
   +---------------------------------------------------------------------------+
   | Be removed from the code when the code is checked into the pull request   |
   | addressing the issue.                                                     |
   +---------------------------------------------------------------------------+

Design Conventions for RAMSTK
-----------------------------

2000. *General Architecture*
#. Data **shall** be stored in referential databases.
#. RAMSTK **shall** follow a MVC architecture.
#. Controllers are referred to as managers.
#. Data managers are used to control the flow of data between the data base, the views, and the analysis manager.
#. Analysis managers are used to control the flow of analyses.

2100. *Record Model*
#. There **shall** be a record model meta-class.

2200. *Table Model*
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
#. All methods in the data manager meta-class:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | Used by child classes **shall** be public.                                |
   +---------------------------------------------------------------------------+
   | Not used be child classes or called only as a PyPubSub listener **shall** |
   | be private.                                                               |
   +---------------------------------------------------------------------------+

#. All methods in the child classes:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | Called by the meta-class **shall** be public.                             |
   +---------------------------------------------------------------------------+
   | Only called internally or as a PyPubSub listener **shall** be private.    |
   +---------------------------------------------------------------------------+
   | **Shall** conform with all naming conventions.                            |
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
   |    \_set\_assessment\_points(self, \*\*kwargs)                            |
   +---------------------------------------------------------------------------+
   | Conform with all naming conventions.                                      |
   +---------------------------------------------------------------------------+

2400. *GUI Components*
#. If the function or method creates a simple or aggregate widget, it shall begin with make (public) or _make_ (private).

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | _make_assessment_inputs_page(self)                                        |
   +---------------------------------------------------------------------------+
   | make_buttonbox(self)                                                      |
   +---------------------------------------------------------------------------+

#. If the function or method is a callback signal that is not a user request, it should begin with on (public) or _on_ (private).

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | on_focus_out(self, entry, new_text)                                       |
   +---------------------------------------------------------------------------+
   | _on_edit(self, __cell, path, new_text, position)                          |
   +---------------------------------------------------------------------------+

#. If the function or method is a callback signal that is a user request (button press, etc.), it should be begin with do\_request\_ (public) or _do_request_ (private).

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | do_request_calculate(self, __button)                                      |
   +---------------------------------------------------------------------------+
   | _do_request_update(self, __button)                                        |
   +---------------------------------------------------------------------------+

2500. *List Views*
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

2600. *Module Views*
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

2700. *Work Views*
#. All Work Views shall have the following public methods:
#. All Work Views shall have the following private methods:
#. Any or all of the work view methods *should* be abstracted to a meta-class.
#. All methods in the work view meta-class:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | Used by child classes **shall** be public.                                |
   +---------------------------------------------------------------------------+
   | Not used by child classes or called only as a PyPubSub listener **shall** |
   | be private as denoted by a leading underscore '_'.                        |
   +---------------------------------------------------------------------------+
   | Conform with all naming conventions.                                      |
   +---------------------------------------------------------------------------+

#. All methods in the child classes:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | Called by the WorkView meta-class **shall** be public.                    |
   +---------------------------------------------------------------------------+
   | Only called internally or as a PyPubSub listener **shall** be private as  |
   | denoted by a leading underscore '_'.                                      |
   +---------------------------------------------------------------------------+
   | Used solely to create the GUI **shall** be mangled as denoted by two      |
   | leading underscores '__'.                                                 |
   +---------------------------------------------------------------------------+
   | Conform with all naming conventions.                                      |
   +---------------------------------------------------------------------------+

#. All WorkView classes shall have the following attributes:

   +-----------------+----------------+----------------------------------------+
   | Attribute       | Type           | Description                            |                                                                 |
   +=================+================+========================================+
   | _dic_icons      | Dict[str, str] | dict of icons to use with the key being|
   |                 |                | a human readable name and the value    |
   |                 |                | being the absolute path to the icon    |
   |                 |                | file.                                  |
   +-----------------+----------------+----------------------------------------+
   | _lst_label_text | List[str]      | list of text for each label that will  |
   |                 |                | be displayed on the WorkView.          |
   +-----------------+----------------+----------------------------------------+
   | _lst_widgets    | List[object]   | list of widgets to place on the        |
   |                 |                | WorkView.                              |
   +-----------------+----------------+----------------------------------------+
   | _module         | str            | name of the RAMSTK workflow module     |
   |                 |                | (e.g., 'revision', 'hardware', etc.)   |
   +-----------------+----------------+----------------------------------------+
   | _notebook       | RASMTKNotebook | Gtk.Notebook that contains each of the |
   |                 |                | 'pages' for the module's WorkView.     |
   +-----------------+----------------+----------------------------------------+
   | _revision_id    | int            | currently selected Revision ID.        |
   +-----------------+----------------+----------------------------------------+
   | _parent_id      | int            | parent ID of the currently selected    |
   |                 |                | workflow item.                         |
   +-----------------+----------------+----------------------------------------+
   | _record_id      | int            | ID (e.g., function ID, hardware ID,    |
   |                 |                | etc.) of the currently selected        |
   |                 |                | workflow item.                         |
   +-----------------+----------------+----------------------------------------+
   | _fmt            | str            | format string for displaying numerical |
   |                 |                | information.                           |
   +-----------------+----------------+----------------------------------------+
   | _hbx_tab_label  | Gtk.HBox       | Gtk.HBox containing the label for the  |
   |                 |                | Gtk.Notebook tab.                      |
   +-----------------+----------------+----------------------------------------+

#. _lst_label_text and _lst_widgets **shall**:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | Contain the label text and widgets in the same order (i.e., the label text|
   | at position 0 corresponds to the information displayed in the widget at   |
   | position 0).                                                              |
   +---------------------------------------------------------------------------+
   | Be listed in the order (top to bottom) they will be displayed on the      |
   | WorkView.                                                                 |
   +---------------------------------------------------------------------------+

#. _lst_label_text and _lst_widget may:

   +---------------------------------------------------------------------------+
   |                                                                           |
   +===========================================================================+
   | Be sliced for display in different sections in the WorkView (e.g., a      |
   | WorkView page is split up by Gtk.Box or Gtk.Paned and the list of         |
   | labels/widgets are divided into the different sections).                  |
   +---------------------------------------------------------------------------+

2800. *RAMSTK Widgets*
#. GUI toolkit widget classes *should* be super-classed to create RAMSTK widget classes.
#. RAMSTK widget classes **shall** be named RAMSTK<widget> where <widget> is the name of the underlying toolkit widget class.  For example, the RAMSTK widget implementing the pygobject GtkEntry() would be named RAMSTKEntry().
#. RAMSTK widget classes **shall** inherit from the parent widget(s).
#. RAMSTK widget classes **shall** contain helper or wrapper methods to handle the detailed implementation of the action; these methods shall be public.
#. All RAMSTK widgets shall have the following public methods:

    1. do_set_properties(): used to set all visual properties of the widget with sensible defaults; this provides for a consistent look and feel.
    #. do_update(), if an updatable widget: used to update the displayed information in the widget; this simply reduces code duplication and eases the development/maintenance of the views using the widgets.

#. All RAMSTK widget classes should have a type definition (*.pyi) file associated with them.
#. Default property values for RAMSTK widget classes may be user-configurable.

Exception and Error Handling
----------------------------

3000. Exceptions caught by GUI components that are or may be the result of user error (e.g., missing data, incorrect data type, etc.) shall raise a warning dialog to inform the user of the potential problem.
#. The warning dialog in 1, above, should provide a "hint" to help the user fix the problem; for example, what data is required for a calculation.
#. Exception caught by GUI components that are the result of other than user error (e.g., missing data from the database) shall raise an error dialog to inform the user of the problem.
#. The error dialog in 3, above, should provide the user a concise statement regarding the cause of the error; for example, data X from the common database is missing.
#. The error dialog in 3, above, may provide the user a hyperlink to the RAMSTK issue system to simplify the process for the user to submit an issue ticket if desired.
#. All exceptions caught by GUI components shall be logged at the debug level.Exception caught by GUI components that are the result of other than user error (e.g., missing data from the database) shall raise an error dialog to inform the user of the problem.

Test Conventions
----------------

10000. Each function or method **shall** have at least one test; this test may be either a unit test or an integration test.

10100. *Unit Tests*
#. **Shall not** use pypubsub to call the function/method being tested; call the method being tested directly, even private ones.
#. **Shall** use mocks for database tables.
#. **Shall** use a mock for the DAO.
#. **Shall** use fixtures to create test objects (e.g., data manager, analysis manager).

10200. *Integration Tests*
#. **Shall** use pypubsub to call the function/method being tested.
#. **Shall** use actual data models.
#. **Shall** use actual DAO.
#. **Shall** use fixtures to create test objects (e.g., data manager, analysis manager).
