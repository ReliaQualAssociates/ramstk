# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.requirement.workview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Requirement Work View."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.utilities import boolean_to_integer
from ramstk.views.gtk3 import Gdk, GObject, Gtk, Pango, _
from ramstk.views.gtk3.widgets import (
    RAMSTKButton, RAMSTKCheckButton, RAMSTKComboBox, RAMSTKDateSelect,
    RAMSTKEntry, RAMSTKFrame, RAMSTKTextView, RAMSTKWorkView)


class GeneralData(RAMSTKWorkView):
    """
    Display general Requirement attribute data in the RAMSTK Work Book.

    The Requirement Work View displays all the general data attributes for the
    selected Requirement.  The attributes of a requirement Work View are:

    :cvar str _module: the name of the module.

    :ivar list _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar list _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar list _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar list _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """
    # Define private dict class attributes.
    _dic_keys = {
        0: ['requirement_code', 'string'],
        1: ['description', 'string'],
        2: 'requirement_type',
        4: ['specification', 'string'],
        5: ['page_number', 'string'],
        6: ['figure_number', 'string'],
        7: 'priority',
        8: 'owner',
        9: ['requirement_code', 'string'],
        10: ['validated_date', 'date']
    }

    # Define private list class attributes.
    _lst_labels: List[str] = [
        _("Requirement Code:"),
        _("Requirement Description:"),
        _("Requirement Type:"), "",
        _("Specification:"),
        _("Page Number:"),
        _("Figure Number:"),
        _("Priority:"),
        _("Owner:"), "",
        _("Validated Date:")
    ]
    _lst_title: List[str] = [_("General Information"), ""]

    # Define private scalar class attributes.
    _module: str = 'requirement'
    _tablabel: str = _("General\nData")
    _tabtooltip: str = _(
        "Displays general information for the selected Requirement.")

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize the Requirement Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=True)

        # Initialize private dictionary attributes.
        self._dic_icons['create_code'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/create_code.png')

        # Initialize private list attributes.
        self._lst_icons = ['create_code']
        self._lst_tooltips = [
            _("Automatically create code for the selected requirement.")
        ]
        self._lst_callbacks = [self._do_request_create_code]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.btnValidateDate: RAMSTKButton = RAMSTKButton()

        self.chkDerived: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Requirement is derived."))
        self.chkValidated: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Requirement is validated."))

        self.cmbOwner: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbRequirementType: RAMSTKComboBox = RAMSTKComboBox(index=1,
                                                                 simple=False)
        self.cmbPriority: RAMSTKComboBox = RAMSTKComboBox()

        self.txtCode: RAMSTKEntry = RAMSTKEntry()
        self.txtFigNum: RAMSTKEntry = RAMSTKEntry()
        self.txtName: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())
        self.txtPageNum: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecification: RAMSTKEntry = RAMSTKEntry()
        self.txtValidatedDate: RAMSTKEntry = RAMSTKEntry()

        self._dic_switch: Dict[str, Union[object, str]] = {
            'derived': [self.chkDerived.do_update, 'toggled'],
            'description': [self.txtName.do_update, 'changed'],
            'figure_number': [self.txtFigNum.do_update, 'changed'],
            'page_number': [self.txtPageNum.do_update, 'changed'],
            'specification': [self.txtSpecification.do_update, 'changed'],
            'validated': [self.chkValidated.do_update, 'toggled'],
            'validated_date': [self.txtValidatedDate.do_update, 'changed']
        }

        self._lst_widgets = [
            self.txtCode, self.txtName, self.cmbRequirementType,
            self.chkDerived, self.txtSpecification, self.txtPageNum,
            self.txtFigNum, self.cmbPriority, self.cmbOwner, self.chkValidated,
            self.txtValidatedDate
        ]

        self.__set_properties()
        self.__load_combobox()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'request_clear_workviews')
        pub.subscribe(self._do_load_page, 'selected_requirement')
        pub.subscribe(self._do_load_code, 'succeed_create_requirement_code')

        pub.subscribe(self.on_edit, 'mvw_editing_requirement')
        pub.subscribe(self.do_set_cursor_active, 'succeed_create_code')
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_requirement')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_create_requirement_code')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_update_requirement')

    def __load_combobox(self):
        """
        Load the RAMSTK ComboBox widgets with lists of information.

        :return: None
        :rtype: None
        """
        # Load the requirement type Gtk.ComboBox(); each _type is
        # (Code, Description, Type).
        _types = []
        # pylint: disable=unused-variable
        for __, _key in enumerate(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_REQUIREMENT_TYPE):
            _types.append(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_REQUIREMENT_TYPE[_key])
        self.cmbRequirementType.do_load_combo(entries=list(_types),
                                              simple=False)

        # Load the owner Gtk.ComboBox(); each _owner is
        # (Description, Group Type).
        _owners = []
        for _index, _key in enumerate(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_WORKGROUPS):
            _owners.append(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_WORKGROUPS[_key])
        self.cmbOwner.do_load_combo(list(_owners))

        # Load the priority Gtk.Combo().
        _priorities = [["1"], ["2"], ["3"], ["4"], ["5"]]
        self.cmbPriority.do_load_combo(_priorities)

    def __make_ui(self) -> None:
        """
        Build the user interface for the Requirement General Data tab.

        :return: None
        :rtype: None
        """
        super().make_tab_label(
            tablabel=self._tablabel,
            tooltip=self._tabtooltip,
        )
        super().make_toolbuttons(
            icons=self._lst_icons,
            tooltips=self._lst_tooltips,
            callbacks=self._lst_callbacks,
        )

        _frame: RAMSTKFrame = super().do_make_panel_fixed(
            start=0,
            end=len(self._lst_labels),
        )
        _frame.do_set_properties(
            bold=True,
            title=self._lst_title[0],
        )

        # Add the validation date dialog launcher button to the right of the
        # validated date RAMSTKEntry.
        _fixed: Gtk.Fixed = _frame.get_children()[0].get_children(
        )[0].get_children()[0]
        _entry: RAMSTKEntry = _fixed.get_children()[-1]
        _x_pos: int = _fixed.child_get_property(_entry, 'x') + 205
        _y_pos: int = _fixed.child_get_property(_entry, 'y')
        _fixed.put(self.btnValidateDate, _x_pos, _y_pos)

        self.pack_end(_frame, True, True, 0)

        self.show_all()

    def __set_callbacks(self) -> None:
        """
        Set the callback methods and requirements.

        :return: None
        :rtype: None
        """
        self.btnValidateDate.dic_handler_id[
            'released'] = self.btnValidateDate.connect('button-release-event',
                                                       self._do_select_date,
                                                       self.txtValidatedDate)

        self.chkDerived.dic_handler_id['toggled'] = self.chkDerived.connect(
            'toggled', self._on_toggled, 3)
        self.chkValidated.dic_handler_id[
            'toggled'] = self.chkValidated.connect('toggled', self._on_toggled,
                                                   9)

        self.cmbRequirementType.dic_handler_id[
            'changed'] = self.cmbRequirementType.connect(
                'changed', self._on_combo_changed, 2)
        self.cmbPriority.dic_handler_id['changed'] = self.cmbPriority.connect(
            'changed', self._on_combo_changed, 7)
        self.cmbOwner.dic_handler_id['changed'] = self.cmbOwner.connect(
            'changed', self._on_combo_changed, 8)

        self.txtCode.dic_handler_id['changed'] = self.txtCode.connect(
            'focus-out-event', self._on_focus_out, 0)
        self.txtName.dic_handler_id['changed'] = self.txtName.do_get_buffer(
        ).connect('changed', self._on_focus_out, None, 1)
        self.txtSpecification.dic_handler_id[
            'changed'] = self.txtSpecification.connect('focus-out-event',
                                                       self._on_focus_out, 4)
        self.txtPageNum.dic_handler_id['changed'] = self.txtPageNum.connect(
            'focus-out-event', self._on_focus_out, 5)
        self.txtFigNum.dic_handler_id['changed'] = self.txtFigNum.connect(
            'focus-out-event', self._on_focus_out, 6)
        self.txtValidatedDate.dic_handler_id[
            'changed'] = self.txtValidatedDate.connect('focus-out-event',
                                                       self._on_focus_out, 10)

    def __set_properties(self) -> None:
        """
        Set the properties of the General Data Work View and widgets.

        :return: None
        :rtype: None
        """
        # ----- BUTTONS
        self.btnValidateDate.do_set_properties(height=25, width=25)

        self.chkDerived.do_set_properties(tooltip=_(
            "Indicates whether or not the selected requirement is "
            "derived."),
                                          width=400)
        self.chkValidated.do_set_properties(tooltip=_(
            "Indicates whether or not the selected requirement is "
            "validated."),
                                            width=400)

        # ----- COMBOBOXES
        self.cmbPriority.do_set_properties(width=50)

        # ----- ENTRIES
        self.txtCode.do_set_properties(
            width=125,
            tooltip=_("A unique code for the selected requirement."))
        self.txtName.do_set_properties(
            height=100,
            width=800,
            tooltip=_("The description of the selected requirement."))
        self.txtValidatedDate.do_set_properties(
            tooltip=_("The date the selected requirement was validated."))

    def _do_clear_page(self) -> None:
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        self.txtCode.do_update('', signal='changed')
        self.txtName.do_update('', signal='changed')

        self.cmbRequirementType.do_update(0, signal='changed')

        self.chkDerived.do_update(False, signal='toggled')
        self.txtSpecification.do_update('', signal='changed')
        self.txtPageNum.do_update('', signal='changed')
        self.txtFigNum.do_update('', signal='changed')

        self.cmbPriority.do_update(0, signal='changed')
        self.cmbOwner.do_update(0, signal='changed')

        self.chkValidated.do_update(False, signal='toggled')
        self.txtValidatedDate.do_update('', signal='changed')

    def _do_load_code(self, requirement_code: int) -> None:
        """
        Load the Requirement code RAMSTKEntry().

        :param str requirement_code: the Requirement code to load.
        :return: None
        :rtype: None
        """
        self.txtCode.do_update(str(requirement_code), signal='changed')

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Requirement General Data page.

        :param dict attributes: the Requirement attributes to load into the
            Work View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['requirement_id']

        self.txtCode.do_update(str(attributes['requirement_code']),
                               signal='changed')
        self.txtName.do_update(str(attributes['description']),
                               signal='changed')
        self.chkDerived.do_update(int(attributes['derived']), signal='toggled')
        self.cmbRequirementType.do_update(int(attributes['requirement_type']),
                                          signal='changed')
        self.txtSpecification.do_update(str(attributes['specification']),
                                        signal='changed')
        self.txtPageNum.do_update(str(attributes['page_number']),
                                  signal='changed')
        self.txtFigNum.do_update(str(attributes['figure_number']),
                                 signal='changed')
        self.cmbPriority.do_update(int(attributes['priority']),
                                   signal='changed')
        self.cmbOwner.do_update(int(attributes['owner']), signal='changed')
        self.chkValidated.do_update(int(attributes['validated']),
                                    signal='toggled')
        if attributes['validated']:
            self.txtValidatedDate.do_update(str(attributes['validated_date']),
                                            signal='changed')
        else:
            self.txtValidatedDate.do_update("", signal='changed')

    def _do_request_create_code(self, __button: Gtk.ToolButton) -> None:
        """
        Request that requirement codes be built.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _prefix = self.cmbRequirementType.get_value()

        super().do_set_cursor_busy()
        pub.sendMessage('request_create_requirement_code',
                        node_id=self._record_id,
                        prefix=_prefix)

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save the currently selected Requirement.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_requirement', node_id=self._record_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save all the Requirements.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_all_requirements')

    @staticmethod
    def _do_select_date(__button: RAMSTKButton, __event: Gdk.Event,
                        entry: RAMSTKEntry) -> str:
        """
        Request to launch a date selection dialog.

        This method is used to select the validation date for the Requirement.

        :param __button: the ramstk.RAMSTKButton() that called this method.
        :type __button: :class:`ramstk.gui.gtk.ramstk.RAMSTKButton`
        :param __event: the Gdk.Event() that called this method.
        :type __event: :class:`Gdk.Event`
        :param entry: the Gtk.Entry() that the new date should be displayed in.
        :type entry: :class:`Gtk.Entry`
        :return: _date; the date in ISO-8601 (YYYY-mm-dd) format.
        :rtype: str
        """
        _dialog = RAMSTKDateSelect()

        _date = _dialog.do_run()
        _dialog.do_destroy()

        entry.set_text(str(_date))

        return _date

    def _on_combo_changed(self, combo: Gtk.CellRendererCombo,
                          index: int) -> None:
        """
        Retrieve Gtk.ComboBox() changes and assign to Requirement attribute.

        :param Gtk.CellRendererCombo combo: the Gtk.CellRendererCombo() that
            called this method.
        :param int index: the position in the Requirement class Gtk.TreeModel()
            associated with the data from the calling Gtk.CellRendererCombo().
        :return: None
        :rtype: None
        """
        super().on_combo_changed(combo, index, 'wvw_editing_requirement')

    # pylint: disable=unused-argument
    def _on_focus_out(self, entry: Gtk.Entry, __event: Gdk.EventFocus,
                      index: int) -> None:
        """
        Handle changes made in RAMSTKEntry() and RAMSTKTextView() widgets.

        This method is called by:

            * RAMSTKEntry() 'focus-out-event' signal
            * RAMSTKTextView() 'changed' signal

        This method sends the 'wvw_editing_requirement' message.

        :param entry: the Gtk.Entry() that called the method.
        :type entry: :class:`Gtk.Entry`
        :param __event: the Gdk.EventFocus that triggered the signal.
        :type __event: :class:`Gdk.EventFocus`
        :param int index: the position in the Requirement class Gtk.TreeModel()
            associated with the data from the calling Gtk.Entry().
        :return: None
        :rtype: None
        """
        super().on_focus_out(entry, index, 'wvw_editing_requirement')

    def _on_toggled(self, checkbutton: RAMSTKCheckButton, index: int) -> None:
        """
        Handle RAMSTKCheckButton() 'toggle' signals.

        :param checkbutton: the RAMSTKCheckButton() that called this method.
        :type: :class:`ramstk.gui.gtk.ramstk.Button.RAMSTKCheckButton`
        :param int index: the index in the signal handler ID list.
        :return: None
        :rtype: None
        """
        super().on_toggled(checkbutton,
                           index,
                           message='wvw_editing_requirement')


class RequirementAnalysis(RAMSTKWorkView):
    """
    Display Requirement attribute data in the RAMSTK Work Book.

    The Requirement Analysis Work View displays all the analysis questions and
    answers for the selected Requirement. The attributes of a Requirement
    Analysis Work View are:

    :cvar str _module: the name of the module.

    :ivar list _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar list _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar list _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar list _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    :ivar list _lst_clear_a: the list of integers [0, 1] corresponding to the
        answers to the Clarity questions.
    :ivar list _lst_complete_a: the list of integers [0, 1] corresponding to
        the answers to the Completeness questions.
    :ivar list _lst_consistent_a: the list of integers [0, 1] corresponding to
        the answers to the Consistency questions.
    :ivar list _lst_verifiable_a: the list of integers [0, 1] corresponding to
        the answers to the Verifiability questions.
    :ivar int _requirement_id: the ID of the Requirement Data Model currently
        being controlled.
    :ivar tvwClear: the :class:`Gtk.RAMSTKTreeView` listing all the Clarity
        questions and answers.
    :ivar tvwComplete: the :class:`Gtk.RAMSTKTreeView` listing all the
        Completeness questions and answers.
    :ivar tvwConsistent: the :class:`Gtk.RAMSTKTreeView` listing all the
        Consistency questions and answers.
    :ivar tvwVerifiable: the :class:`Gtk.RAMSTKTreeView` listing all the
        Verifiability questions and answers.
    """
    _lst_clear = [
        _("1. The requirement clearly states what is needed or "
          "desired."),
        _("2. The requirement is unambiguous and not open to "
          "interpretation."),
        _("3. All terms that can have more than one meaning are "
          "qualified so that the desired meaning is readily "
          "apparent."),
        _("4. Diagrams, drawings, etc. are used to increase "
          "understanding of the requirement."),
        _("5. The requirement is free from spelling and "
          "grammatical errors."),
        _("6. The requirement is written in non-technical "
          "language using the vocabulary of the stakeholder."),
        _("7. Stakeholders understand the requirement as written."),
        _("8. The requirement is clear enough to be turned over "
          "to an independent group and still be understood."),
        _("9. The requirement avoids stating how the problem is "
          "to be solved or what techniques are to be used.")
    ]
    _lst_complete = [
        _("1. Performance objectives are properly documented "
          "from the user's point of view."),
        _("2. No necessary information is missing from the "
          "requirement."),
        _("3. The requirement has been assigned a priority."),
        _("4. The requirement is realistic given the technology "
          "that will used to implement the system."),
        _("5. The requirement is feasible to implement given the "
          "defined project time frame, scope, structure and "
          "budget."),
        _("6. If the requirement describes something as a "
          "'standard' the specific source is cited."),
        _("7. The requirement is relevant to the problem and its "
          "solution."),
        _("8. The requirement contains no implied design details."),
        _("9. The requirement contains no implied implementation "
          "constraints."),
        _("10. The requirement contains no implied project "
          "management constraints.")
    ]
    _lst_consistent = [
        _("1. The requirement describes a single need or want; "
          "it could not be broken into several different "
          "requirements."),
        _("2. The requirement requires non-standard hardware or "
          "must use software to implement."),
        _("3. The requirement can be implemented within known "
          "constraints."),
        _("4. The requirement provides an adequate basis for "
          "design and testing."),
        _("5. The requirement adequately supports the business "
          "goal of the project."),
        _("6. The requirement does not conflict with some "
          "constraint, policy or regulation."),
        _("7. The requirement does not conflict with another "
          "requirement."),
        _("8. The requirement is not a duplicate of another "
          "requirement."),
        _("9. The requirement is in scope for the project.")
    ]
    _lst_verifiable = [
        _("1. The requirement is verifiable by testing, "
          "demonstration, review, or analysis."),
        _("2. The requirement lacks 'weasel words' (e.g. "
          "various, mostly, suitable, integrate, maybe, "
          "consistent, robust, modular, user-friendly, "
          "superb, good)."),
        _("3. Any performance criteria are quantified such that "
          "they are testable."),
        _("4. Independent testing would be able to determine "
          "whether the requirement has been satisfied."),
        _("5. The task(s) that will validate and verify the "
          "final design satisfies the requirement have been "
          "identified."),
        _("6. The identified V&amp;V task(s) have been added to "
          "the validation plan (e.g., DVP)")
    ]

    # Define private scalar class attributes.
    _module: str = 'requirement'
    _tablabel: str = "<span weight='bold'>" + _("Analysis") + "</span>"
    _tabtooltip: str = _("Analyzes the selected requirement.")

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize the Requirements analysis work view.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=True)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks: List[object] = []
        self._lst_icons: List[str] = []
        self._lst_tooltips: List[str] = []

        self._lst_clear_a: List = []
        self._lst_complete_a: List = []
        self._lst_consistent_a: List = []
        self._lst_verifiable_a: List = []

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.tvwClear: Gtk.TreeView = Gtk.TreeView()
        self.tvwComplete: Gtk.TreeView = Gtk.TreeView()
        self.tvwConsistent: Gtk.TreeView = Gtk.TreeView()
        self.tvwVerifiable: Gtk.TreeView = Gtk.TreeView()

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._do_load_page, 'selected_requirement')

        pub.subscribe(self.do_set_cursor_active, 'succeed_update_requirement')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_update_requirement')

    def __make_treeview(self, index: int
                        ) -> Tuple[Gtk.ListStore, Gtk.TreeViewColumn]:
        """
        Build the Gtk.TreeView() for the Requirements Analyses.

        :param int index: the index of the Gtk.TreeView() being built.  Used in
                          callback methods.
        :return: (_model, _column); the Gtk.ListStore() and
                                    Gtk.TreeViewColumn() to apply to the RAMSTK
                                    TreeView().
        :rtype: tuple
        """
        _model = Gtk.ListStore()
        _model.set_column_types(
            [GObject.TYPE_INT, GObject.TYPE_STRING, GObject.TYPE_INT])

        _column = Gtk.TreeViewColumn()

        _cell = Gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('visible', 0)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=0)

        _cell = Gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('wrap-width', 650)
        _cell.set_property('wrap-mode', Pango.WrapMode.WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, markup=1)

        _cell = Gtk.CellRendererToggle()
        _cell.set_property('activatable', 1)
        _cell.connect('toggled', self._on_cell_edit, _model, index)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, active=2)

        _column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)

        return (_model, _column)

    def __make_ui(self) -> None:
        """
        Build the user interface for the Requirement Analysis tab.

        :return: None
        :rtype: None
        """
        _vpaned_left, _vpaned_right = super().do_make_layout_llrr()

        _vpaned_left.pack1(self.__make_ui_clear(), False)
        _vpaned_left.pack2(self.__make_ui_complete(), False)
        _vpaned_right.pack1(self.__make_ui_consistent(), False)
        _vpaned_right.pack2(self.__make_ui_verifiable(), False)

        self.show_all()

    def __make_ui_clear(self) -> Gtk.Frame:
        """
        Build the Gtk.TreeView() to display the questions about clarity.

        :return: _frame; the RAMSTK Frame() containing the clarity questions.
        :rtype: :class:`ramstk.gui.gtk.ramstk.RAMSTKFrame`
        """
        _frame: RAMSTKFrame = super().do_make_panel_treeview(self.tvwClear, )
        _frame.do_set_properties(
            bold=True,
            title=_("Clarity of Requirement"),
        )

        (_model, _column) = self.__make_treeview(0)
        self.tvwClear.set_model(_model)
        self.tvwClear.set_headers_visible(False)
        self.tvwClear.append_column(_column)

        _model.clear()
        for _index, _answer in enumerate(self._lst_clear):
            _model.append([_index, _answer, 0])

        return _frame

    def __make_ui_complete(self) -> Gtk.Frame:
        """
        Build the Gtk.TreeView() to display questions about completeness.

        :return: _frame; the RAMSTK Frame() containing the completeness
                         questions.
        :rtype: :class:`ramstk.gui.gtk.ramstk.RAMSTKFrame`
        """
        _frame: RAMSTKFrame = super().do_make_panel_treeview(
            self.tvwComplete, )
        _frame.do_set_properties(
            bold=True,
            title=_("Completeness of Requirement"),
        )

        (_model, _column) = self.__make_treeview(1)
        self.tvwComplete.set_model(_model)
        self.tvwComplete.set_headers_visible(False)
        self.tvwComplete.append_column(_column)

        _model.clear()
        for _index, _answer in enumerate(self._lst_complete):
            _model.append([_index, _answer, 0])

        return _frame

    def __make_ui_consistent(self) -> Gtk.Frame:
        """
        Build the Gtk.TreeView() to display the questions about consistency.

        :return: _frame; the RAMSTK Frame() containing the consistency
                         questions.
        :rtype: :class:`ramstk.gui.gtk.ramstk.RAMSTKFrame`
        """
        _frame: RAMSTKFrame = super().do_make_panel_treeview(
            self.tvwConsistent, )
        _frame.do_set_properties(
            bold=True,
            title=_("Consistency of Requirement"),
        )

        (_model, _column) = self.__make_treeview(2)
        self.tvwConsistent.set_model(_model)
        self.tvwConsistent.set_headers_visible(False)
        self.tvwConsistent.append_column(_column)

        _model.clear()
        for _index, _answer in enumerate(self._lst_consistent):
            _model.append([_index, _answer, 0])

        return _frame

    def __make_ui_verifiable(self) -> Gtk.Frame:
        """
        Build the Gtk.TreeView() to display questions about verifiability.

        :return: _frame; the RAMSTK Frame() containing the verifiability
                         questions.
        :rtype: :class:`ramstk.gui.gtk.ramstk.RAMSTKFrame`
        """
        _frame: RAMSTKFrame = super().do_make_panel_treeview(
            self.tvwVerifiable, )
        _frame.do_set_properties(
            bold=True,
            title=_("Verifiability of Requirement"),
        )

        (_model, _column) = self.__make_treeview(3)
        self.tvwVerifiable.set_model(_model)
        self.tvwVerifiable.set_headers_visible(False)
        self.tvwVerifiable.append_column(_column)

        _model.clear()
        for _index, _answer in enumerate(self._lst_verifiable):
            _model.append([_index, _answer, 0])

        return _frame

    def _do_clear_page(self) -> None:
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        for _treeview in [
                self.tvwClear, self.tvwComplete, self.tvwConsistent,
                self.tvwVerifiable
        ]:
            _model = _treeview.get_model()
            _columns = _treeview.get_columns()
            for _column in _columns:
                _treeview.remove_column(_column)

            _model.clear()

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Requirements analysis page.

        :return: None
        :rtype: None
        """
        self._record_id = attributes['requirement_id']

        # Load the Requirement analyses answers.  It's easiest to pack the
        # answers into a list and iterate for each tree.
        self._lst_clear_a = [
            attributes['q_clarity_0'], attributes['q_clarity_1'],
            attributes['q_clarity_2'], attributes['q_clarity_3'],
            attributes['q_clarity_4'], attributes['q_clarity_5'],
            attributes['q_clarity_6'], attributes['q_clarity_7'],
            attributes['q_clarity_8']
        ]
        _model = self.tvwClear.get_model()
        _row = _model.get_iter_first()
        for _answer in self._lst_clear_a:
            _model.set_value(_row, 2, _answer)
            _row = _model.iter_next(_row)

        self._lst_complete_a = [
            attributes['q_complete_0'], attributes['q_complete_1'],
            attributes['q_complete_2'], attributes['q_complete_3'],
            attributes['q_complete_4'], attributes['q_complete_5'],
            attributes['q_complete_6'], attributes['q_complete_7'],
            attributes['q_complete_8'], attributes['q_complete_9']
        ]
        _model = self.tvwComplete.get_model()
        _row = _model.get_iter_first()
        for _answer in self._lst_complete_a:
            _model.set_value(_row, 2, _answer)
            _row = _model.iter_next(_row)

        self._lst_consistent_a = [
            attributes['q_consistent_0'], attributes['q_consistent_1'],
            attributes['q_consistent_2'], attributes['q_consistent_3'],
            attributes['q_consistent_4'], attributes['q_consistent_5'],
            attributes['q_consistent_6'], attributes['q_consistent_7'],
            attributes['q_consistent_8']
        ]
        _model = self.tvwConsistent.get_model()
        _row = _model.get_iter_first()
        for _answer in self._lst_consistent_a:
            _model.set_value(_row, 2, _answer)
            _row = _model.iter_next(_row)

        self._lst_verifiable_a = [
            attributes['q_verifiable_0'], attributes['q_verifiable_1'],
            attributes['q_verifiable_2'], attributes['q_verifiable_3'],
            attributes['q_verifiable_4'], attributes['q_verifiable_5']
        ]
        _model = self.tvwVerifiable.get_model()
        _row = _model.get_iter_first()
        for _answer in self._lst_verifiable_a:
            _model.set_value(_row, 2, _answer)
            _row = _model.iter_next(_row)

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to save the currently selected Requirement.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_requirement', node_id=self._record_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save all the Requirements.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_all_requirements')

    def _on_cell_edit(self, cell: Gtk.CellRendererToggle, path: str,
                      model: Gtk.TreeModel, position: int) -> None:
        """
        Handle edits of the Requirement Analysis RAMSTKTreeview().

        :param cell: the Gtk.CellRendererToggle() that was toggled.
        :type cell: :class:`Gtk.CellRendererToggle`
        :param str path: the Gtk.TreeView() path of the Gtk.CellRenderer()
                         that was edited.
        :param model: the Gtk.TreeModel() for the Gtk.Treeview() that is being
                      edited.
        :type model: :class:`Gtk.TreeModel`
        :param int position: the position of the Requirement analysis
            Gtk.Treeview() questions being answered.  Indices are:

                             * 0 = clarity
                             * 1 = completeness
                             * 2 = consistency
                             * 3 = verifiability

        :return: None
        :rtype: None
        """
        _key = ''
        _position = model[path][0]

        _new_text: int = boolean_to_integer(not cell.get_active())
        model[path][2] = _new_text

        try:
            if position == 0:
                self._lst_clear_a[_position] = _new_text
                _key = 'q_clarity_{0:d}'.format(_position)
            elif position == 1:
                self._lst_complete_a[_position] = _new_text
                _key = 'q_complete_{0:d}'.format(_position)
            elif position == 2:
                self._lst_consistent_a[_position] = _new_text
                _key = 'q_consistent_{0:d}'.format(_position)
            elif position == 3:
                self._lst_verifiable_a[_position] = _new_text
                _key = 'q_verifiable_{0:d}'.format(_position)
        except IndexError as _error:
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        pub.sendMessage('wvw_editing_requirement',
                        node_id=[self._record_id, -1],
                        package={_key: _new_text})
