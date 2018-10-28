# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.Requirement.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Requirement Work View."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.Utilities import boolean_to_integer
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _, gobject, gtk, pango
from .WorkView import RAMSTKWorkView


class GeneralData(RAMSTKWorkView):
    """
    Display Requirement attribute data in the RAMSTK Work Book.

    The Work View displays all the attributes for the selected Requirement. The
    attributes of a Work View are:

    :ivar int _requirement_id: the ID of the Requirement Data Model currently
                               being displayed.
    :ivar chkDerived: the :class:`gtk.CheckButton` used to indicate the
                      selected Requirement is derived.
    :ivar chkValidated: the :class:`gtk.CheckButton` used to indicates the
                        selected Requirement has been validated.
    :ivar cmbOwner: the :class:`gtk.ComboBox` used to display/select the
                    owning organization for the Requirement.
    :ivar cmbRequirementType: the :class:`gtk.ComboBox` used to
                              display/select the type of Requirement.
    :ivar cmbPriority: the :class:`gtk.ComboBox` used to display/select the
                       priority of the Requirement.
    :ivar txtFigNum: the :class:`gtk.Entry` used to display/enter the
                     spcification figure number associated with the
                     Requirement.
    :ivar txtPageNum: the :class:`gtk.Entry` used to display/enter the
                      specification page number associated with the
                      Requirement.
    :ivar txtSpecification: the :class:`gtk.Entry` used to display/enter the
                            governing specification.
    :ivar txtValidatedDate: the :class:`gtk.Entry` used to display/enter the
                            Requirement was validated.

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | txtCode `changed`                         |
    +----------+-------------------------------------------+
    |     1    | txtName `changed`                         |
    +----------+-------------------------------------------+
    |     2    | cmbRequirementType `changed`              |
    +----------+-------------------------------------------+
    |     3    | chkDerived `toggled`                      |
    +----------+-------------------------------------------+
    |     4    | txtSpcification `changed`                 |
    +----------+-------------------------------------------+
    |     5    | txtPageNum `changed`                      |
    +----------+-------------------------------------------+
    |     6    | txtFigNum `changed`                       |
    +----------+-------------------------------------------+
    |     7    | cmbPriority `changed`                     |
    +----------+-------------------------------------------+
    |     8    | cmbOwner `changed`                        |
    +----------+-------------------------------------------+
    |     9    | chKValidated `toggled`                    |
    +----------+-------------------------------------------+
    |    10    | txtValidateDate `changed`                 |
    +----------+-------------------------------------------+
    """

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Requirement Work View.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKWorkView.__init__(self, controller, module='Requirement')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_gendata_labels = [
            _(u"Requirement Code:"),
            _(u"Requirement Description:"),
            _(u"Requirement Type:"), "",
            _(u"Specification:"),
            _(u"Page Number:"),
            _(u"Figure Number:"),
            _(u"Priority:"),
            _(u"Owner:"), "",
            _(u"Validated Date:")
        ]

        # Initialize private scalar attributes.
        self._requirement_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.btnValidateDate = ramstk.RAMSTKButton(
            height=25, width=25, label="...")

        self.chkDerived = ramstk.RAMSTKCheckButton(
            label=_(u"Requirement is derived."),
            tooltip=_(u"Indicates whether or not the selected requirement is "
                      u"derived."))
        self.chkValidated = ramstk.RAMSTKCheckButton(
            label=_(u"Requirement is validated."),
            tooltip=_(u"Indicates whether or not the selected requirement is "
                      u"validated."))

        self.cmbOwner = ramstk.RAMSTKComboBox()
        self.cmbRequirementType = ramstk.RAMSTKComboBox(index=1, simple=False)
        self.cmbPriority = ramstk.RAMSTKComboBox(width=50)

        self.txtCode = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(u"A unique code for the selected requirement."))
        self.txtFigNum = ramstk.RAMSTKEntry()
        self.txtName = ramstk.RAMSTKEntry(
            width=800,
            tooltip=_(u"The description of the selected requirement."))
        self.txtPageNum = ramstk.RAMSTKEntry()
        self.txtSpecification = ramstk.RAMSTKEntry()
        self.txtValidatedDate = ramstk.RAMSTKEntry()

        # Connect to callback requirements for editable gtk.Widgets().
        self._lst_handler_id.append(
            self.txtCode.connect('changed', self._on_focus_out, 0))
        self._lst_handler_id.append(
            self.txtName.connect('changed', self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.cmbRequirementType.connect('changed', self._on_combo_changed,
                                            2))
        self._lst_handler_id.append(
            self.chkDerived.connect('toggled', self._on_toggled, 3))
        self._lst_handler_id.append(
            self.txtSpecification.connect('changed', self._on_focus_out, 4))
        self._lst_handler_id.append(
            self.txtPageNum.connect('changed', self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtFigNum.connect('changed', self._on_focus_out, 6))
        self._lst_handler_id.append(
            self.cmbPriority.connect('changed', self._on_combo_changed, 7))
        self._lst_handler_id.append(
            self.cmbOwner.connect('changed', self._on_combo_changed, 8))
        self._lst_handler_id.append(
            self.chkValidated.connect('toggled', self._on_toggled, 9))
        self._lst_handler_id.append(
            self.txtValidatedDate.connect('changed', self._on_focus_out, 10))
        self._lst_handler_id.append(
            self.btnValidateDate.connect('button-release-event',
                                         self._do_select_date,
                                         self.txtValidatedDate))

        self.pack_start(self._make_buttonbox(), expand=False, fill=False)
        self.pack_start(self._make_page(), expand=True, fill=True)
        self.show_all()

        pub.subscribe(self._on_select, 'selectedRequirement')
        pub.subscribe(self._on_edit, 'mvwEditedRequirement')
        pub.subscribe(self._on_edit, 'calculatedRequirement')
        pub.subscribe(self._do_clear_page, 'closedProgram')

    def _do_clear_page(self):
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        self.txtCode.handler_block(self._lst_handler_id[0])
        self.txtCode.set_text('')
        self.txtCode.handler_unblock(self._lst_handler_id[0])

        self.txtName.handler_block(self._lst_handler_id[1])
        self.txtName.set_text('')
        self.txtName.handler_unblock(self._lst_handler_id[1])

        self.chkDerived.handler_block(self._lst_handler_id[3])
        self.chkDerived.set_active(False)
        self.chkDerived.handler_unblock(self._lst_handler_id[3])

        self.cmbRequirementType.handler_block(self._lst_handler_id[2])
        self.cmbRequirementType.set_active(0)
        self.cmbRequirementType.handler_unblock(self._lst_handler_id[2])

        self.txtSpecification.handler_block(self._lst_handler_id[4])
        self.txtSpecification.set_text('')
        self.txtSpecification.handler_unblock(self._lst_handler_id[4])

        self.txtPageNum.handler_block(self._lst_handler_id[5])
        self.txtPageNum.set_text('')
        self.txtPageNum.handler_unblock(self._lst_handler_id[5])

        self.txtFigNum.handler_block(self._lst_handler_id[6])
        self.txtFigNum.set_text('')
        self.txtFigNum.handler_unblock(self._lst_handler_id[6])

        self.cmbPriority.handler_block(self._lst_handler_id[7])
        self.cmbPriority.set_active(0)
        self.cmbPriority.handler_unblock(self._lst_handler_id[7])

        self.cmbOwner.handler_block(self._lst_handler_id[8])
        self.cmbOwner.set_active(0)
        self.cmbOwner.handler_unblock(self._lst_handler_id[8])

        self.chkValidated.handler_block(self._lst_handler_id[9])
        self.chkValidated.set_active(False)
        self.chkValidated.handler_unblock(self._lst_handler_id[9])

        self.txtValidatedDate.handler_block(self._lst_handler_id[10])
        self.txtValidatedDate.set_text('')
        self.txtValidatedDate.handler_unblock(self._lst_handler_id[10])

        return None

    def _do_load_page(self, **kwargs):  # pylint: disable=unused-argument
        """
        Load the Requirements general data page.

        :return: False if successful and True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _requirement = self._dtc_data_controller.request_do_select(
            self._requirement_id)

        self.txtCode.handler_block(self._lst_handler_id[0])
        self.txtCode.set_text(str(_requirement.requirement_code))
        self.txtCode.handler_unblock(self._lst_handler_id[0])

        self.txtName.handler_block(self._lst_handler_id[1])
        self.txtName.set_text(_requirement.description)
        self.txtName.handler_unblock(self._lst_handler_id[1])

        self.chkDerived.handler_block(self._lst_handler_id[3])
        self.chkDerived.set_active(_requirement.derived)
        self.chkDerived.handler_unblock(self._lst_handler_id[3])

        self.cmbRequirementType.handler_block(self._lst_handler_id[2])
        _types = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_REQUIREMENT_TYPE
        self.cmbRequirementType.set_active(0)
        _idx = 1
        for _key, _type in _types.iteritems():
            if _type[1] == _requirement.requirement_type:
                self.cmbRequirementType.set_active(_idx)
            else:
                _idx += 1
        self.cmbRequirementType.handler_unblock(self._lst_handler_id[2])

        self.txtSpecification.handler_block(self._lst_handler_id[4])
        self.txtSpecification.set_text(str(_requirement.specification))
        self.txtSpecification.handler_unblock(self._lst_handler_id[4])

        self.txtPageNum.handler_block(self._lst_handler_id[5])
        self.txtPageNum.set_text(str(_requirement.page_number))
        self.txtPageNum.handler_unblock(self._lst_handler_id[5])

        self.txtFigNum.handler_block(self._lst_handler_id[6])
        self.txtFigNum.set_text(str(_requirement.figure_number))
        self.txtFigNum.handler_unblock(self._lst_handler_id[6])

        self.cmbPriority.handler_block(self._lst_handler_id[7])
        self.cmbPriority.set_active(int(_requirement.priority))
        self.cmbPriority.handler_unblock(self._lst_handler_id[7])

        self.cmbOwner.handler_block(self._lst_handler_id[8])
        _groups = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_WORKGROUPS
        self.cmbOwner.set_active(0)
        for _key, _group in _groups.iteritems():
            if _group[0] == _requirement.owner:
                self.cmbOwner.set_property('active', int(_key))
        self.cmbOwner.handler_unblock(self._lst_handler_id[8])

        self.chkValidated.handler_block(self._lst_handler_id[9])
        self.chkValidated.set_active(_requirement.validated)
        self.chkValidated.handler_unblock(self._lst_handler_id[9])

        self.txtValidatedDate.handler_block(self._lst_handler_id[10])
        if _requirement.validated:
            self.txtValidatedDate.set_text(str(_requirement.validated_date))
        else:
            self.txtValidatedDate.set_text("")
        self.txtValidatedDate.handler_unblock(self._lst_handler_id[10])

        return _return

    def _do_request_update(self, __button):
        """
        Request to save the currently selected Requirement.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(gtk.gdk.WATCH)
        _return = self._dtc_data_controller.request_do_update(
            self._requirement_id)
        self.set_cursor(gtk.gdk.LEFT_PTR)

        return _return

    def _do_request_update_all(self, __button):
        """
        Request to save all the Requirements.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(gtk.gdk.WATCH)
        _return = self._dtc_data_controller.request_do_update_all()
        self.set_cursor(gtk.gdk.LEFT_PTR)

        return _return

    @staticmethod
    def _do_select_date(__button, __event, entry):
        """
        Request to launch a date selection dialog.

        This method is used to select the validation date for the Requirement.

        :param __button: the ramstk.RAMSTKButton() that called this method.
        :type __button: :class:`ramstk.gui.gtk.ramstk.RAMSTKButton`
        :param __event: the gtk.gdk.Event() that called this method.
        :type __event: :class:`gtk.gdk.Event`
        :param entry: the gtk.Entry() that the new date should be displayed in.
        :type entry: :class:`gtk.Entry`
        :return: _date; the date in ISO-8601 (YYYY-mm-dd) format.
        :rtype: str
        """
        _dialog = ramstk.RAMSTKDateSelect()

        _date = _dialog.do_run()
        _dialog.do_destroy()

        entry.set_text(str(_date))

        return _date

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the gtk.ButtonBox() for the Requirement Work View.

        :return: _buttonbox; the gtk.ButtonBox() for the Requirement Work View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = []
        _callbacks = []
        _icons = []

        _buttonbox = ramstk.do_make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1)

        return _buttonbox

    def _make_page(self):
        """
        Make the Requirement Work View General Data gtk.Notebook() page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Load the requirement type gtk.ComboBox(); each _type is
        # (Code, Description, Type).
        _types = []
        for _index, _key in enumerate(
                self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_REQUIREMENT_TYPE):
            _types.append(self._mdcRAMSTK.RAMSTK_CONFIGURATION.
                          RAMSTK_REQUIREMENT_TYPE[_key])
        self.cmbRequirementType.do_load_combo(
            list(_types), index=1, simple=False)

        # Load the owner gtk.ComboBox(); each _owner is
        # (Description, Group Type).
        _owners = []
        for _index, _key in enumerate(
                self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_WORKGROUPS):
            _owners.append(
                self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_WORKGROUPS[_key])
        self.cmbOwner.do_load_combo(list(_owners))

        # Load the priority gtk.Combo().
        _priorities = [["1"], ["2"], ["3"], ["4"], ["5"]]
        self.cmbPriority.do_load_combo(_priorities)

        # Build the General Data page.
        _fixed = gtk.Fixed()

        _scrollwindow = ramstk.RAMSTKScrolledWindow(_fixed)
        _frame = ramstk.RAMSTKFrame(label=_(u"General Information"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = ramstk.make_label_group(self._lst_gendata_labels,
                                                 _fixed, 5, 5)
        _x_pos += 50

        _fixed.put(self.txtCode, _x_pos, _y_pos[0])
        _fixed.put(self.txtName, _x_pos, _y_pos[1])
        _fixed.put(self.cmbRequirementType, _x_pos, _y_pos[2])
        _fixed.put(self.chkDerived, _x_pos, _y_pos[3] + 5)
        _fixed.put(self.txtSpecification, _x_pos, _y_pos[4])
        _fixed.put(self.txtPageNum, _x_pos, _y_pos[5])
        _fixed.put(self.txtFigNum, _x_pos, _y_pos[6])
        _fixed.put(self.cmbPriority, _x_pos, _y_pos[7])
        _fixed.put(self.cmbOwner, _x_pos, _y_pos[8])
        _fixed.put(self.chkValidated, _x_pos, _y_pos[9] + 5)
        _fixed.put(self.txtValidatedDate, _x_pos, _y_pos[10])
        _fixed.put(self.btnValidateDate, _x_pos + 205, _y_pos[10])

        _fixed.show_all()

        # Create the label for the gtk.Notebook() tab.
        _label = ramstk.RAMSTKLabel(
            _(u"General\nData"),
            height=30,
            width=-1,
            justify=gtk.JUSTIFY_CENTER,
            tooltip=_(u"Displays general information for the selected "
                      u"requirement."))
        self.hbx_tab_label.pack_start(_label)

        return _frame

    def _on_combo_changed(self, combo, index):
        """
        Retrieve gtk.ComboBox() changes and assign to Requirement attribute.

        :param gtk.CellRendererCombo combo: the gtk.CellRendererCombo() that
                                            called this method.
        :param int index: the position in the Requirement class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Entry().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        combo.handler_block(self._lst_handler_id[index])

        _model = combo.get_model()
        _row = combo.get_active_iter()

        if self._dtc_data_controller is not None:
            _requirement = self._dtc_data_controller.request_do_select(
                self._requirement_id)

            if index == 2:
                _index = 11
                _prefix = _model.get_value(_row, 0)
                _text = _model.get_value(_row, 1)
                _requirement.requirement_type = str(_text)
                _requirement.requirement_code = \
                    _requirement.create_code(_prefix)
                self.txtCode.set_text(str(_requirement.requirement_code))
            elif index == 7:
                _index = 8
                _text = int(_model.get_value(_row, 0))
                _requirement.priority = _text
            elif index == 8:
                _index = 5
                _text = _model.get_value(_row, 0)
                _requirement.owner = _text

            pub.sendMessage(
                'wvwEditedRequirement', position=_index, new_text=_text)

        combo.handler_unblock(self._lst_handler_id[index])

        return _return

    def _on_edit(self, index, new_text):
        """
        Update the Requirement Work View gtk.Widgets().

        This method updates Work View gtk.Widgets() with changes to the
        Requirement data model attributes.  This method is called whenever an
        attribute is edited in a different view.

        :param int index: the index in the Requirement attributes list of the
                          attribute that was edited.
        :param str new_text: the new text to update the gtk.Widget() with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        if index == 3:
            self.txtName.handler_block(self._lst_handler_id[1])
            self.txtName.set_text(str(new_text))
            self.txtName.handler_unblock(self._lst_handler_id[1])
        elif index == 4:
            self.txtFigNum.handler_block(self._lst_handler_id[6])
            self.txtFigNum.set_text(str(new_text))
            self.txtFigNum.handler_unblock(self._lst_handler_id[6])
        elif index == 5:
            self.cmbOwner.handler_block(self._lst_handler_id[8])
            _groups = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_WORKGROUPS
            for _key, _group in _groups.iteritems():
                if _group[0] == new_text:
                    self.cmbOwner.set_property('active', int(_key))
            self.cmbOwner.handler_unblock(self._lst_handler_id[8])
        elif index == 6:
            self.txtPageNum.handler_block(self._lst_handler_id[5])
            self.txtPageNum.set_text(str(new_text))
            self.txtPageNum.handler_unblock(self._lst_handler_id[5])
        elif index == 8:
            self.cmbPriority.handler_block(self._lst_handler_id[7])
            self.cmbPriority.set_property('active', int(new_text))
            self.cmbPriority.handler_unblock(self._lst_handler_id[7])
        elif index == 9:
            self.txtCode.handler_block(self._lst_handler_id[0])
            self.txtCode.set_text(str(new_text))
            self.txtCode.handler_unblock(self._lst_handler_id[0])
        elif index == 10:
            self.txtSpecification.handler_block(self._lst_handler_id[4])
            self.txtSpecification.set_text(str(new_text))
            self.txtSpecification.handler_unblock(self._lst_handler_id[4])
        elif index == 11:
            self.cmbRequirementType.handler_block(self._lst_handler_id[2])
            _types = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_REQUIREMENT_TYPE
            for _key, _type in _types.iteritems():
                if _type[1] == new_text:
                    self.cmbRequirementType.set_property('active', int(_key))
            self.cmbRequirementType.handler_unblock(self._lst_handler_id[2])
        elif index == 13:
            self.txtValidatedDate.handler_block(self._lst_handler_id[10])
            self.txtValidatedDate.set_text(str(new_text))
            self.txtValidatedDate.handler_unblock(self._lst_handler_id[10])

        return _return

    def _on_focus_out(self, entry, index):
        """
        Retrieve RAMSTKEntry() changes and assign to Requirement attributes.

        This method retrieves changes to Requirement attributes through the
        various gtk.Widgets() and assign the new data to the appropriate
        Requirement data model attribute.  This method is called by:

            * gtk.Entry() 'changed' signal
            * gtk.TextView() 'changed' signal

        This method sends the 'wvwEditedRequirement' message.

        :param gtk.Entry entry: the gtk.Entry() that called the method.
        :param int index: the position in the Requirement class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Widget().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _index = -1
        _return = False
        _text = ''

        entry.handler_block(self._lst_handler_id[index])

        if self._dtc_data_controller is not None:
            _requirement = self._dtc_data_controller.request_do_select(
                self._requirement_id)

            if index == 0:
                _index = 9
                _text = str(entry.get_text())
                _requirement.requirement_code = _text
            elif index == 1:
                _index = 3
                _text = str(entry.get_text())
                _requirement.description = _text
            elif index == 4:
                _index = 10
                _text = str(entry.get_text())
                _requirement.specification = _text
            elif index == 5:
                _index = 6
                _text = str(entry.get_text())
                _requirement.page_number = _text
            elif index == 6:
                _index = 4
                _text = str(entry.get_text())
                _requirement.figure_number = _text
            elif index == 10:
                _index = 13
                _text = str(entry.get_text())
                _requirement.validated_date = _text

            pub.sendMessage(
                'wvwEditedRequirement', position=_index, new_text=_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def _on_select(self, module_id, **kwargs):  # pylint: disable=unused-argument
        """
        Load the Requirement Work View gtk.Notebook() widgets.

        :param int module_id: the Requirement ID of the selected/edited
                              Requirement.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._requirement_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKBaseView.__init__
        self._dtc_data_controller = self._mdcRAMSTK.dic_controllers[
            'requirement']
        self._do_load_page()

        return _return

    def _on_toggled(self, togglebutton, index):
        """
        Retrieve gtk.CheckButton() changes and assign to Requirement attribute.

        :param togglebutton: the gtk.CheckButton() that called this method.
        :type togglebutton: :class:`gtk.CheckButton`
        :param int index: the position in the Requirement class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Entry().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        togglebutton.handler_block(self._lst_handler_id[index])

        if self._dtc_data_controller is not None:
            _requirement = self._dtc_data_controller.request_do_select(
                self._requirement_id)

            if index == 3:
                _index = 2
                _requirement.derived = int(togglebutton.get_active())
            elif index == 9:
                _index = 12
                _requirement.validated = int(togglebutton.get_active())

            pub.sendMessage(
                'wvwEditedRequirement',
                position=_index,
                new_text=int(togglebutton.get_active()))

        togglebutton.handler_unblock(self._lst_handler_id[index])

        return _return


class RequirementAnalysis(RAMSTKWorkView):
    """
    Display Requirement attribute data in the RAMSTK Work Book.

    The Requirement Analysis Work View displays all the analysis questions and
    answers for the selected Requirement. The attributes of a Requirement
    Analysis Work View are:

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
    :ivar tvwClear: the :class:`gtk.RAMSTKTreeView` listing all the Clarity
                    questions and answers.
    :ivar tvwComplete: the :class:`gtk.RAMSTKTreeView` listing all the
                       Completeness questions and answers.
    :ivar tvwConsistent: the :class:`gtk.RAMSTKTreeView` listing all the
                         Consistency questions and answers.
    :ivar tvwVerifiable: the :class:`gtk.RAMSTKTreeView` listing all the
                         Verifiability questions and answers.
    """

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the Requirement package.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKWorkView.__init__(self, controller, module='Requirement')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_clear_a = []
        self._lst_complete_a = []
        self._lst_consistent_a = []
        self._lst_verifiable_a = []

        # Initialize private scalar attributes.
        self._requirement_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.tvwClear = gtk.TreeView()
        self.tvwComplete = gtk.TreeView()
        self.tvwConsistent = gtk.TreeView()
        self.tvwVerifiable = gtk.TreeView()

        self.pack_start(self._make_buttonbox(), expand=False, fill=False)
        self.pack_start(self._make_page(), expand=True, fill=True)
        self.show_all()

        pub.subscribe(self._on_select, 'selectedRequirement')
        pub.subscribe(self._do_clear_page, 'closedProgram')

    def _do_clear_page(self):
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

        return None

    def _do_request_update(self, __button):
        """
        Save the currently selected Requirement.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(gtk.gdk.WATCH)
        _return = self._dtc_data_controller.request_do_update(
            self._requirement_id)
        self.set_cursor(gtk.gdk.LEFT_PTR)

        return _return

    def _do_request_update_all(self, __button):
        """
        Request to save all the Requirements.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(gtk.gdk.WATCH)
        _return = self._dtc_data_controller.request_do_update_all()
        self.set_cursor(gtk.gdk.LEFT_PTR)

        return _return

    def _do_edit_cell(self, cell, path, new_text, position, model, index):  # pylint: disable=unused-argument
        """
        Handle edits of the Requirement Analysis RAMSTKTreeview().

        :param cell: the gtk.CellRendererToggle() that was toggled.
        :type cell: :class:`gtk.CellRendererToggle`
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer()
                         that was edited.
        :param model: the gtk.TreeModel() for the gtk.Treeview() that is being
                      edited.
        :type model: :class:`gtk.TreeModel`
        :param int index: the index of the Requirement analysis gtk.Treeview()
                          questions being answered.  Indices are:

                             * 0 = clarity
                             * 1 = completeness
                             * 2 = consistency
                             * 3 = verifiability

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _requirement = self._dtc_data_controller.request_do_select(
            self._requirement_id)

        _answer = boolean_to_integer(not cell.get_active())
        model[path][2] = _answer

        _position = model[path][0]

        try:
            if index == 0:
                self._lst_clear_a[_position] = _answer
                _requirement.q_clarity_0 = self._lst_clear_a[0]
                _requirement.q_clarity_1 = self._lst_clear_a[1]
                _requirement.q_clarity_2 = self._lst_clear_a[2]
                _requirement.q_clarity_3 = self._lst_clear_a[3]
                _requirement.q_clarity_4 = self._lst_clear_a[4]
                _requirement.q_clarity_5 = self._lst_clear_a[5]
                _requirement.q_clarity_6 = self._lst_clear_a[6]
                _requirement.q_clarity_7 = self._lst_clear_a[7]
                _requirement.q_clarity_8 = self._lst_clear_a[8]
            elif index == 1:
                self._lst_complete_a[_position] = _answer
                _requirement.q_complete_0 = self._lst_complete_a[0]
                _requirement.q_complete_1 = self._lst_complete_a[1]
                _requirement.q_complete_2 = self._lst_complete_a[2]
                _requirement.q_complete_3 = self._lst_complete_a[3]
                _requirement.q_complete_4 = self._lst_complete_a[4]
                _requirement.q_complete_5 = self._lst_complete_a[5]
                _requirement.q_complete_6 = self._lst_complete_a[6]
                _requirement.q_complete_7 = self._lst_complete_a[7]
                _requirement.q_complete_8 = self._lst_complete_a[8]
                _requirement.q_complete_9 = self._lst_complete_a[9]
            elif index == 2:
                self._lst_consistent_a[_position] = _answer
                _requirement.q_consistent_0 = self._lst_consistent_a[0]
                _requirement.q_consistent_1 = self._lst_consistent_a[1]
                _requirement.q_consistent_2 = self._lst_consistent_a[2]
                _requirement.q_consistent_3 = self._lst_consistent_a[3]
                _requirement.q_consistent_4 = self._lst_consistent_a[4]
                _requirement.q_consistent_5 = self._lst_consistent_a[5]
                _requirement.q_consistent_6 = self._lst_consistent_a[6]
                _requirement.q_consistent_7 = self._lst_consistent_a[7]
                _requirement.q_consistent_8 = self._lst_consistent_a[8]
            elif index == 3:
                self._lst_verifiable_a[_position] = _answer
                _requirement.q_verifiable_0 = self._lst_verifiable_a[0]
                _requirement.q_verifiable_1 = self._lst_verifiable_a[1]
                _requirement.q_verifiable_2 = self._lst_verifiable_a[2]
                _requirement.q_verifiable_3 = self._lst_verifiable_a[3]
                _requirement.q_verifiable_4 = self._lst_verifiable_a[4]
                _requirement.q_verifiable_5 = self._lst_verifiable_a[5]
        except IndexError:
            _debug_msg = ("RAMSTK ERROR: No position {0:d} in Requirements "
                          "Analysis question list for index {1:d}.").format(
                              _position, index)
            self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_DEBUG_LOG.error(
                _debug_msg)

        return _return

    def _do_load_page(self, **kwargs):  # pylint: disable=unused-argument
        """
        Load the Requirements analysis page.

        :return: False if successful and True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _requirement = self._dtc_data_controller.request_do_select(
            self._requirement_id)

        # Load the Requirement analyses answers.  It's easiest to pack the
        # answers into a list and iterate for each tree.
        self._lst_clear_a = [
            _requirement.q_clarity_0, _requirement.q_clarity_1,
            _requirement.q_clarity_2, _requirement.q_clarity_3,
            _requirement.q_clarity_4, _requirement.q_clarity_5,
            _requirement.q_clarity_6, _requirement.q_clarity_7,
            _requirement.q_clarity_8
        ]
        _model = self.tvwClear.get_model()
        _row = _model.get_iter_first()
        for _answer in self._lst_clear_a:
            _model.set_value(_row, 2, _answer)
            _row = _model.iter_next(_row)

        self._lst_complete_a = [
            _requirement.q_complete_0, _requirement.q_complete_1,
            _requirement.q_complete_2, _requirement.q_complete_3,
            _requirement.q_complete_4, _requirement.q_complete_5,
            _requirement.q_complete_6, _requirement.q_complete_7,
            _requirement.q_complete_8, _requirement.q_complete_9
        ]
        _model = self.tvwComplete.get_model()
        _row = _model.get_iter_first()
        for _answer in self._lst_complete_a:
            _model.set_value(_row, 2, _answer)
            _row = _model.iter_next(_row)

        self._lst_consistent_a = [
            _requirement.q_consistent_0, _requirement.q_consistent_1,
            _requirement.q_consistent_2, _requirement.q_consistent_3,
            _requirement.q_consistent_4, _requirement.q_consistent_5,
            _requirement.q_consistent_6, _requirement.q_consistent_7,
            _requirement.q_consistent_8
        ]
        _model = self.tvwConsistent.get_model()
        _row = _model.get_iter_first()
        for _answer in self._lst_consistent_a:
            _model.set_value(_row, 2, _answer)
            _row = _model.iter_next(_row)

        self._lst_verifiable_a = [
            _requirement.q_verifiable_0, _requirement.q_verifiable_1,
            _requirement.q_verifiable_2, _requirement.q_verifiable_3,
            _requirement.q_verifiable_4, _requirement.q_verifiable_5
        ]
        _model = self.tvwVerifiable.get_model()
        _row = _model.get_iter_first()
        for _answer in self._lst_verifiable_a:
            _model.set_value(_row, 2, _answer)
            _row = _model.iter_next(_row)

        return _return

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the gtk.ButtonBox() for the Requirement Work View.

        :return: _buttonbox; the gtk.ButtonBox() for the Requirement Work View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = []
        _callbacks = []
        _icons = []

        _buttonbox = ramstk.do_make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1)

        return _buttonbox

    def _make_page(self):
        """
        Make the Requirement Analysis Work View page.

        :return: _hpaned
        :rtype: :class:`gtk.HPaned`
        """
        _lst_clear = [
            _(u"1. The requirement clearly states what is needed or "
              u"desired."),
            _(u"2. The requirement is unambiguous and not open to "
              u"interpretation."),
            _(u"3. All terms that can have more than one meaning are "
              u"qualified so that the desired meaning is readily "
              u"apparent."),
            _(u"4. Diagrams, drawings, etc. are used to increase "
              u"understanding of the requirement."),
            _(u"5. The requirement is free from spelling and "
              u"grammatical errors."),
            _(u"6. The requirement is written in non-technical "
              u"language using the vocabulary of the stakeholder."),
            _(u"7. Stakeholders understand the requirement as written."),
            _(u"8. The requirement is clear enough to be turned over "
              u"to an independent group and still be understood."),
            _(u"9. The requirement avoids stating how the problem is "
              u"to be solved or what techniques are to be used.")
        ]
        _lst_complete = [
            _(u"1. Performance objectives are properly documented "
              u"from the user's point of view."),
            _(u"2. No necessary information is missing from the "
              u"requirement."),
            _(u"3. The requirement has been assigned a priority."),
            _(u"4. The requirement is realistic given the technology "
              u"that will used to implement the system."),
            _(u"5. The requirement is feasible to implement given the "
              u"defined project time frame, scope, structure and "
              u"budget."),
            _(u"6. If the requirement describes something as a "
              u"'standard' the specific source is cited."),
            _(u"7. The requirement is relevant to the problem and its "
              u"solution."),
            _(u"8. The requirement contains no implied design details."),
            _(u"9. The requirement contains no implied implementation "
              u"constraints."),
            _(u"10. The requirement contains no implied project "
              u"management constraints.")
        ]
        _lst_consistent = [
            _(u"1. The requirement describes a single need or want; "
              u"it could not be broken into several different "
              u"requirements."),
            _(u"2. The requirement requires non-standard hardware or "
              u"must use software to implement."),
            _(u"3. The requirement can be implemented within known "
              u"constraints."),
            _(u"4. The requirement provides an adequate basis for "
              u"design and testing."),
            _(u"5. The requirement adequately supports the business "
              u"goal of the project."),
            _(u"6. The requirement does not conflict with some "
              u"constraint, policy or regulation."),
            _(u"7. The requirement does not conflict with another "
              u"requirement."),
            _(u"8. The requirement is not a duplicate of another "
              u"requirement."),
            _(u"9. The requirement is in scope for the project.")
        ]
        _lst_verifiable = [
            _(u"1. The requirement is verifiable by testing, "
              u"demonstration, review, or analysis."),
            _(u"2. The requirement lacks 'weasel words' (e.g. "
              u"various, mostly, suitable, integrate, maybe, "
              u"consistent, robust, modular, user-friendly, "
              u"superb, good)."),
            _(u"3. Any performance criteria are quantified such that "
              u"they are testable."),
            _(u"4. Independent testing would be able to determine "
              u"whether the requirement has been satisfied."),
            _(u"5. The task(s) that will validate and verify the "
              u"final design satisfies the requirement have been "
              u"identified."),
            _(u"6. The identified V&amp;V task(s) have been added to "
              u"the validation plan (e.g., DVP)")
        ]

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hpaned = gtk.HPaned()

        # Create quadrant #1 (upper left) for determining if the
        # requirement is clear.
        _vpaned = gtk.VPaned()
        _hpaned.pack1(_vpaned, resize=False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwClear)

        _frame = ramstk.RAMSTKFrame(label=_(u"Clarity of Requirement"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack1(_frame, resize=False)

        # Create quadrant #3 (lower left) for determining if the
        # requirement is complete.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwComplete)

        _frame = ramstk.RAMSTKFrame(label=_(u"Completeness of Requirement"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack2(_frame, resize=False)

        # Create quadrant #2 (upper right) for determining if the
        # requirement is consistent.
        _vpaned = gtk.VPaned()
        _hpaned.pack2(_vpaned, resize=False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwConsistent)

        _frame = ramstk.RAMSTKFrame(label=_(u"Consistency of Requirement"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack1(_frame, resize=False)

        # Create quadrant #4 (lower right) for determining if the
        # requirement is verifiable.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwVerifiable)

        _frame = ramstk.RAMSTKFrame(label=_(u"Verifiability of Requirement"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack2(_frame, resize=False)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display requirements analysis       #
        # information.                                                  #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        for _index, _treeview in enumerate([
                self.tvwClear, self.tvwComplete, self.tvwConsistent,
                self.tvwVerifiable
        ]):
            _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                                   gobject.TYPE_INT)
            _treeview.set_model(_model)
            _treeview.set_headers_visible(False)

            _column = gtk.TreeViewColumn()

            _cell = gtk.CellRendererText()
            _cell.set_property('editable', 0)
            _cell.set_property('visible', 0)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=0)

            _cell = gtk.CellRendererText()
            _cell.set_property('cell-background', '#E5E5E5')
            _cell.set_property('editable', 0)
            _cell.set_property('wrap-width', 650)
            _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
            _cell.set_property('yalign', 0.1)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, markup=1)

            _cell = gtk.CellRendererToggle()
            _cell.set_property('activatable', 1)
            _cell.set_property('cell-background', '#E5E5E5')
            _cell.connect('toggled', self._do_edit_cell, None, None, _model,
                          _index)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, active=2)

            _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

            _treeview.append_column(_column)

        _model = self.tvwClear.get_model()
        _model.clear()
        for _index, _clear in enumerate(_lst_clear):
            _model.append(
                [_index, "<span weight='bold'>" + _clear + "</span>", 0])

        _model = self.tvwComplete.get_model()
        _model.clear()
        for _index, _complete in enumerate(_lst_complete):
            _model.append(
                [_index, "<span weight='bold'>" + _complete + "</span>", 0])

        _model = self.tvwConsistent.get_model()
        _model.clear()
        for _index, _consistent in enumerate(_lst_consistent):
            _model.append(
                [_index, "<span weight='bold'>" + _consistent + "</span>", 0])

        _model = self.tvwVerifiable.get_model()
        _model.clear()
        for _index, _verifiable in enumerate(_lst_verifiable):
            _model.append(
                [_index, "<span weight='bold'>" + _verifiable + "</span>", 0])

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Analysis") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_tooltip_text(_(u"Analyzes the selected requirement."))
        _label.show_all()
        self.hbx_tab_label.pack_start(_label)

        return _hpaned

    def _on_select(self, module_id, **kwargs):
        """
        Load the Requirement Analysis Work View gtk.Notebook() widgets.

        :param int module_id: the Requirement ID of the selected Requirement.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._requirement_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKBaseView.__init__
        self._dtc_data_controller = self._mdcRAMSTK.dic_controllers[
            'requirement']

        return self._do_load_page(**kwargs)
