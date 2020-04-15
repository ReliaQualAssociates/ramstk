# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.requirement.workview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Requirement Work View."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKButton, RAMSTKCheckButton, RAMSTKComboBox, RAMSTKDateSelect,
    RAMSTKEntry, RAMSTKFrame, RAMSTKLabel, RAMSTKTextView,
    RAMSTKTreeView, RAMSTKWorkView, do_make_buttonbox
)


class GeneralData(RAMSTKWorkView):
    """
    Display general Requirement attribute data in the RAMSTK Work Book.

    The Requirement Work View displays all the general data attributes for the
    selected Requirement. The attributes of a Requirement General Data Work
    View are:

    Callbacks signals in _lst_handler_id:
    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | txtCode `focus_out_event`                 |
    +----------+-------------------------------------------+
    |     1    | txtName `focus_out_event`                 |
    +----------+-------------------------------------------+
    |     2    | txtRemarks `changed`                      |
    +----------+-------------------------------------------+
    """

    # Define private list attributes.
    _lst_labels = [
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

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'requirement') -> None:
        """
        Initialize the Requirement Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger, module)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=True)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._requirement_id: int = -1

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.btnValidateDate = RAMSTKButton()

        self.chkDerived = RAMSTKCheckButton(label=_("Requirement is derived."))
        self.chkValidated = RAMSTKCheckButton(
            label=_("Requirement is validated."))

        self.cmbOwner = RAMSTKComboBox()
        self.cmbRequirementType = RAMSTKComboBox(index=1, simple=False)
        self.cmbPriority = RAMSTKComboBox()

        self.txtCode = RAMSTKEntry()
        self.txtFigNum = RAMSTKEntry()
        self.txtName = RAMSTKTextView(Gtk.TextBuffer())
        self.txtPageNum = RAMSTKEntry()
        self.txtSpecification = RAMSTKEntry()
        self.txtValidatedDate = RAMSTKEntry()

        self.__set_properties()
        #self.__load_combobox()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'request_clear_workviews')
        pub.subscribe(self._do_load_page, 'selected_requirement')
        pub.subscribe(self._on_edit, 'mvw_editing_requirement')

        pub.subscribe(self.do_set_cursor_active, 'succeed_update_requirement')
        pub.subscribe(self._do_set_cursor_active, 'fail_update_requirement')

    def __load_combobox(self):
        """
        Load the RAMSTK ComboBox widgets with lists of information.

        :return: None
        :rtype: None
        """
        # Load the requirement type Gtk.ComboBox(); each _type is
        # (Code, Description, Type).
        _types = []
        for _index, _key in enumerate(
                self.RAMSTK_CONFIGURATION.RAMSTK_REQUIREMENT_TYPE):
            _types.append(
                self.RAMSTK_CONFIGURATION.RAMSTK_REQUIREMENT_TYPE[_key])
        self.cmbRequirementType.do_load_combo(entries=list(_types),
                                              simple=False)

        # Load the owner Gtk.ComboBox(); each _owner is
        # (Description, Group Type).
        _owners = []
        for _index, _key in enumerate(
                self.RAMSTK_CONFIGURATION.RAMSTK_WORKGROUPS):
            _owners.append(self.RAMSTK_CONFIGURATION.RAMSTK_WORKGROUPS[_key])
        self.cmbOwner.do_load_combo(list(_owners))

        # Load the priority Gtk.Combo().
        _priorities = [["1"], ["2"], ["3"], ["4"], ["5"]]
        self.cmbPriority.do_load_combo(_priorities)

    def __make_ui(self) -> None:
        """
        Create the Requirement Work View general data page.

        :return: None
        :rtype: None
        """
        _lst_tweak = [75, 75, 85, 85, 85, 95, 95, 95, 105, 105]
        (_x_pos, _y_pos, _fixed) = super().make_ui(icons=[],
                                                   tooltips=[],
                                                   callbacks=[])

        # self.txtName has a height of 100 so the labels need adjusted.
        # The first two labels will be properly placed and the last two
        # widgets are the common RAMSTKEntry() widgets that we don't want to
        # move.
        for _idx, _label in enumerate(_fixed.get_children()[2:-1]):
            _fixed.move(_label, 5, _y_pos[_idx + 2] + _lst_tweak[_idx])

        _fixed.put(self.txtName.scrollwindow, _x_pos, _y_pos[1])
        _fixed.put(self.cmbRequirementType, _x_pos, _y_pos[2] + _lst_tweak[0])
        _fixed.put(self.chkDerived, _x_pos, _y_pos[3] + _lst_tweak[1])
        _fixed.put(self.txtSpecification, _x_pos, _y_pos[4] + _lst_tweak[2])
        _fixed.put(self.txtPageNum, _x_pos, _y_pos[5] + _lst_tweak[3])
        _fixed.put(self.txtFigNum, _x_pos, _y_pos[6] + _lst_tweak[4])
        _fixed.put(self.cmbPriority, _x_pos, _y_pos[7] + _lst_tweak[5])
        _fixed.put(self.cmbOwner, _x_pos, _y_pos[8] + _lst_tweak[6])
        _fixed.put(self.chkValidated, _x_pos, _y_pos[9] + _lst_tweak[7])
        _fixed.put(self.txtValidatedDate, _x_pos, _y_pos[10] + _lst_tweak[8])
        _fixed.put(self.btnValidateDate, _x_pos + 205,
                   _y_pos[10] + _lst_tweak[9])

        _label = RAMSTKLabel(_("General\nData"))
        _label.do_set_properties(
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_(
                "Displays general information for the selected Requirement"))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def __set_callbacks(self) -> None:
        """
        Set the callback methods and requirements.

        :return: None
        :rtype: None
        """
        self._lst_handler_id.append(
            self.txtCode.connect('focus-out-event', self._on_focus_out, 0))
        self._lst_handler_id.append(self.txtName.do_get_buffer().connect(
            'changed', self._on_focus_out, None, 1))
        self._lst_handler_id.append(
            self.cmbRequirementType.connect('changed', self._on_combo_changed,
                                            2))
        self._lst_handler_id.append(
            self.chkDerived.connect('toggled', self._on_toggled, 3))
        self._lst_handler_id.append(
            self.txtSpecification.connect('focus-out-event',
                                          self._on_focus_out, 4))
        self._lst_handler_id.append(
            self.txtPageNum.connect('focus-out-event', self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtFigNum.connect('focus-out-event', self._on_focus_out, 6))
        self._lst_handler_id.append(
            self.cmbPriority.connect('changed', self._on_combo_changed, 7))
        self._lst_handler_id.append(
            self.cmbOwner.connect('changed', self._on_combo_changed, 8))
        self._lst_handler_id.append(
            self.chkValidated.connect('toggled', self._on_toggled, 9))
        self._lst_handler_id.append(
            self.txtValidatedDate.connect('focus-out-event',
                                          self._on_focus_out, 10))
        self._lst_handler_id.append(
            self.btnValidateDate.connect('button-release-event',
                                         self._do_select_date,
                                         self.txtValidatedDate))

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
        self.txtCode.do_update('', self._lst_handler_id[0])
        self.txtName.do_update('', self._lst_handler_id[1])

        self.cmbRequirementType.handler_block(self._lst_handler_id[2])
        self.cmbRequirementType.set_active(0)
        self.cmbRequirementType.handler_unblock(self._lst_handler_id[2])

        self.chkDerived.do_update(False, self._lst_handler_id[3])
        self.txtSpecification.do_update('', self._lst_handler_id[4])
        self.txtPageNum.do_update('', self._lst_handler_id[5])
        self.txtFigNum.do_update('', self._lst_handler_id[6])

        self.cmbPriority.handler_block(self._lst_handler_id[7])
        self.cmbPriority.set_active(0)
        self.cmbPriority.handler_unblock(self._lst_handler_id[7])

        self.cmbOwner.handler_block(self._lst_handler_id[8])
        self.cmbOwner.set_active(0)
        self.cmbOwner.handler_unblock(self._lst_handler_id[8])

        self.chkValidated.do_update(False, self._lst_handler_id[9])
        self.txtValidatedDate.do_update('', self._lst_handler_id[10])

    def _do_load_code(self, code):
        """
        Load the Requirement code RAMSTKEntry().

        :param str code: the Requirement code to load.
        :return: None
        :rtype: None
        """
        self.txtCode.do_update(str(code), self._lst_handler_id[0])

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Requirement General Data page.

        :param dict attributes: the Requirement attributes to load into the
            Work View widgets.
        :return: None
        :rtype: None
        """
        self._requirement_id = attributes['requirement_id']

        self.txtCode.do_update(str(attributes['requirement_code']),
                               self._lst_handler_id[0])
        self.txtName.do_update(str(attributes['description']),
                               self._lst_handler_id[1])
        self.chkDerived.do_update(int(attributes['derived']),
                                  self._lst_handler_id[3])
        self.cmbRequirementType.do_update(attributes['requirement_type'],
                                          self._lst_handler_id[2])
        self.txtSpecification.do_update(str(attributes['specification']),
                                        self._lst_handler_id[4])
        self.txtPageNum.do_update(str(attributes['page_number']),
                                  self._lst_handler_id[5])
        self.txtFigNum.do_update(str(attributes['figure_number']),
                                 self._lst_handler_id[6])
        self.cmbPriority.do_update(str(attributes['priority']),
                                   self._lst_handler_id[7])
        self.cmbOwner.do_update(str(attributes['owner']),
                                self._lst_handler_id[8])
        self.chkValidated.do_update(int(attributes['validated']),
                                    self._lst_handler_id[9])
        if attributes['validated']:
            self.txtValidatedDate.do_update(str(attributes['validated_date']),
                                            self._lst_handler_id[10])
        else:
            self.txtValidatedDate.do_update("", self._lst_handler_id[10])

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save the currently selected Requirement.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_requirement',
                        node_id=self._requirement_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save all the Requirements.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_requirements')
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

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

    # pylint: disable=unused-argument
    def _do_set_cursor_active(self, error_message: str) -> None:
        """
        Returns the cursor to the active cursor on a fail message.

        The meta-class do_set_active() method expects node_id as the data
        package, but the fail messages carry an error message as the package.
        This method simply calls the meta-class method in response to fail
        messages.

        :param str error_message: the error message associated with the fail
            message.
        :return: None
        :rtype: None
        """
        self.do_set_cursor_active(node_id=self._requirement_id)

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
        _dic_keys = {2: 'requirement_type', 7: 'priority', 8: 'owner'}
        try:
            _key = _dic_keys[index]
        except KeyError:
            _key = ''

        combo.handler_block(self._lst_handler_id[index])

        _model = combo.get_model()
        _row = combo.get_active_iter()

        if _key == 'requirement_type':
            _new_text = [_model.get_value(_row, 0), _model.get_value(_row, 1)]
        elif _key == 'priority':
            _new_text = int(_model.get_value(_row, 0))
        elif _key == 'owner':
            _new_text = _model.get_value(_row, 0)
        else:
            _new_text = ''

        pub.sendMessage('wvw_editing_requirement',
                        node_id=[self._requirement_id, -1],
                        package={_key: _new_text})

        combo.handler_unblock(self._lst_handler_id[index])

    def _on_edit(self, node_id: List[int], package: Dict[str, Any]) -> None:
        """
        Update the Requirement Work View Gtk.Widgets().

        This method updates the Requirement Work View Gtk.Widgets() with
        changes to the Requirement data model attributes.  The moduleview sends
        a dict that relates the database field and the new data for that field.

            `package` key: `package` value

        corresponds to:

            database field name: new value

        This method uses the key to determine which widget needs to be
        updated with the new data.

        :param list node_id: a list of the ID's of the record in the RAMSTK
            Program database table whose attributes are to be set.  The list
            is:

                0 - Requirement ID

        :param dict package: the key:value for the attribute being updated.
        :return: None
        :rtype: None
        """
        _module_id = node_id[0]
        [[_key, _value]] = package.items()
        _dic_switch = {
            'derived': [self.chkDerived.do_update, 2],
            'description': [self.txtName.do_update, 3],
            'figure_number': [self.txtFigNum.do_update, 4],
            'page_number': [self.txtPageNum.do_update, 6],
            'specification': [self.txtSpecification.do_update, 10],
            'validated': [self.chkValidated.do_update, 12],
            'validated_date': [self.txtValidatedDate.do_update, 13],
        }

        (_function, _id) = _dic_switch.get(_key)
        _function(_value, self._lst_handler_id[_id])

    def _on_focus_out(
            self,
            entry: Gtk.Entry,
            __event: Gdk.EventFocus,  # pylint: disable=unused-argument
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
        _dic_keys = {
            0: 'requirement_code',
            1: 'description',
            4: 'specification',
            5: 'page_number',
            6: 'figure_number',
            9: 'requirement_code',
            10: 'validated_date'
        }
        try:
            _key = _dic_keys[index]
        except KeyError as _error:
            _key = ''
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        entry.handler_block(self._lst_handler_id[index])

        if index == 1:
            _new_text: str = self.txtName.do_get_text()
        else:
            _new_text = str(entry.get_text())

        pub.sendMessage('wvw_editing_requirement',
                        node_id=[self._requirement_id, -1],
                        package={_key: _new_text})

        entry.handler_unblock(self._lst_handler_id[index])

    def _on_toggled(self, checkbutton: RAMSTKCheckButton, index: int) -> None:
        """
        Handle RAMSTKCheckButton() 'toggle' signals.

        :param checkbutton: the RAMSTKCheckButton() that called this method.
        :type: :class:`ramstk.gui.gtk.ramstk.Button.RAMSTKCheckButton`
        :param int index: the index in the signal handler ID list.
        :return: None
        :rtype: None
        """
        _dic_keys = {3: 'derived', 9: 'validated'}
        try:
            _key = _dic_keys[index]
        except KeyError as _error:
            _key = ''
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        checkbutton.handler_block(self._lst_handler_id[index])

        _new_text = int(checkbutton.get_active())

        pub.sendMessage('wvw_editing_requirement',
                        node_id=[self._requirement_id, -1, ''],
                        package={_key: _new_text})

        checkbutton.handler_unblock(self._lst_handler_id[index])
