# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.Requirement.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Requirement Work View."""

# Import third party modules.
from pubsub import pub

# Import other RAMSTK modules.
from ramstk.Utilities import boolean_to_integer
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _, Gdk, GObject, Gtk, Pango
from .WorkView import RAMSTKWorkView


class GeneralData(RAMSTKWorkView):
    """
    Display Requirement attribute data in the RAMSTK Work Book.

    The Work View displays all the attributes for the selected Requirement. The
    attributes of a Work View are:

    :ivar int _requirement_id: the ID of the Requirement Data Model currently
                               being displayed.
    :ivar chkDerived: the :class:`Gtk.CheckButton` used to indicate the
                      selected Requirement is derived.
    :ivar chkValidated: the :class:`Gtk.CheckButton` used to indicates the
                        selected Requirement has been validated.
    :ivar cmbOwner: the :class:`Gtk.ComboBox` used to display/select the
                    owning organization for the Requirement.
    :ivar cmbRequirementType: the :class:`Gtk.ComboBox` used to
                              display/select the type of Requirement.
    :ivar cmbPriority: the :class:`Gtk.ComboBox` used to display/select the
                       priority of the Requirement.
    :ivar txtFigNum: the :class:`Gtk.Entry` used to display/enter the
                     spcification figure number associated with the
                     Requirement.
    :ivar txtPageNum: the :class:`Gtk.Entry` used to display/enter the
                      specification page number associated with the
                      Requirement.
    :ivar txtSpecification: the :class:`Gtk.Entry` used to display/enter the
                            governing specification.
    :ivar txtValidatedDate: the :class:`Gtk.Entry` used to display/enter the
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

        # Connect to callback requirements for editable Gtk.Widgets().
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

        self.pack_start(self.__make_buttonbox(), expand=False, fill=False)
        self.pack_start(self.__make_page(), expand=True, fill=True)
        self.show_all()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._do_load_page, 'selected_requirement')
        pub.subscribe(self._do_load_code, 'created_requirement_code')
        pub.subscribe(self._on_edit, 'mvw_editing_requirement')

    def __make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the Gtk.ButtonBox() for the Requirement Work View.

        :return: _buttonbox; the Gtk.ButtonBox() for the Requirement Work View.
        :rtype: :class:`Gtk.ButtonBox`
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

    def __make_page(self):
        """
        Make the Requirement Work View General Data Gtk.Notebook() page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Load the requirement type Gtk.ComboBox(); each _type is
        # (Code, Description, Type).
        _types = []
        for _index, _key in enumerate(
                self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_REQUIREMENT_TYPE):
            _types.append(self._mdcRAMSTK.RAMSTK_CONFIGURATION.
                          RAMSTK_REQUIREMENT_TYPE[_key])
        self.cmbRequirementType.do_load_combo(
            list(_types), index=1, simple=False)

        # Load the owner Gtk.ComboBox(); each _owner is
        # (Description, Group Type).
        _owners = []
        for _index, _key in enumerate(
                self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_WORKGROUPS):
            _owners.append(
                self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_WORKGROUPS[_key])
        self.cmbOwner.do_load_combo(list(_owners))

        # Load the priority Gtk.Combo().
        _priorities = [["1"], ["2"], ["3"], ["4"], ["5"]]
        self.cmbPriority.do_load_combo(_priorities)

        # Build the General Data page.
        _fixed = Gtk.Fixed()

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

        # Create the label for the Gtk.Notebook() tab.
        _label = ramstk.RAMSTKLabel(
            _(u"General\nData"),
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_(u"Displays general information for the selected "
                      u"requirement."))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        return _frame

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

    def _do_load_code(self, code):
        """
        Load the Requirement code RAMSTKEntry().

        :param str code: the Requirement code to load.
        :return: None
        :rtype: None
        """
        self.txtCode.handler_block(self._lst_handler_id[0])
        self.txtCode.set_text(str(code))
        self.txtCode.handler_unblock(self._lst_handler_id[0])

        return None

    def _do_load_page(self, attributes):
        """
        Load the Requirements general data page.

        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']
        self._requirement_id = attributes['requirement_id']
        RAMSTKWorkView.on_select(
            self,
            title=_(u"Analyzing Requirement {0:s} - {1:s}").format(
                str(attributes['requirement_code']),
                str(attributes['description'])))

        self.txtCode.handler_block(self._lst_handler_id[0])
        self.txtCode.set_text(str(attributes['requirement_code']))
        self.txtCode.handler_unblock(self._lst_handler_id[0])

        self.txtName.handler_block(self._lst_handler_id[1])
        self.txtName.set_text(str(attributes['description']))
        self.txtName.handler_unblock(self._lst_handler_id[1])

        self.chkDerived.handler_block(self._lst_handler_id[3])
        self.chkDerived.set_active(attributes['derived'])
        self.chkDerived.handler_unblock(self._lst_handler_id[3])

        self.cmbRequirementType.handler_block(self._lst_handler_id[2])
        _types = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_REQUIREMENT_TYPE
        self.cmbRequirementType.set_active(0)
        _idx = 1
        for _key, _type in _types.iteritems():
            if _type[1] == attributes['requirement_type']:
                self.cmbRequirementType.set_active(_idx)
            else:
                _idx += 1
        self.cmbRequirementType.handler_unblock(self._lst_handler_id[2])

        self.txtSpecification.handler_block(self._lst_handler_id[4])
        self.txtSpecification.set_text(str(attributes['specification']))
        self.txtSpecification.handler_unblock(self._lst_handler_id[4])

        self.txtPageNum.handler_block(self._lst_handler_id[5])
        self.txtPageNum.set_text(str(attributes['page_number']))
        self.txtPageNum.handler_unblock(self._lst_handler_id[5])

        self.txtFigNum.handler_block(self._lst_handler_id[6])
        self.txtFigNum.set_text(str(attributes['figure_number']))
        self.txtFigNum.handler_unblock(self._lst_handler_id[6])

        self.cmbPriority.handler_block(self._lst_handler_id[7])
        self.cmbPriority.set_active(int(attributes['priority']))
        self.cmbPriority.handler_unblock(self._lst_handler_id[7])

        self.cmbOwner.handler_block(self._lst_handler_id[8])
        _groups = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_WORKGROUPS
        self.cmbOwner.set_active(0)
        for _key, _group in _groups.iteritems():
            if _group[0] == attributes['owner']:
                self.cmbOwner.set_property('active', int(_key))
        self.cmbOwner.handler_unblock(self._lst_handler_id[8])

        self.chkValidated.handler_block(self._lst_handler_id[9])
        self.chkValidated.set_active(int(attributes['validated']))
        self.chkValidated.handler_unblock(self._lst_handler_id[9])

        self.txtValidatedDate.handler_block(self._lst_handler_id[10])
        if attributes['validated']:
            self.txtValidatedDate.set_text(str(attributes['validated_date']))
        else:
            self.txtValidatedDate.set_text("")
        self.txtValidatedDate.handler_unblock(self._lst_handler_id[10])

        return None

    def _do_request_update(self, __button):
        """
        Send request to save the currently selected Requirement.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage(
            'request_update_requirement', node_id=self._requirement_id)
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

        return None

    def _do_request_update_all(self, __button):
        """
        Request to save all the Requirements.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_requirements')
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

        return None

    @staticmethod
    def _do_select_date(__button, __event, entry):
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
        _dialog = ramstk.RAMSTKDateSelect()

        _date = _dialog.do_run()
        _dialog.do_destroy()

        entry.set_text(str(_date))

        return _date

    def _on_combo_changed(self, combo, index):
        """
        Retrieve Gtk.ComboBox() changes and assign to Requirement attribute.

        :param Gtk.CellRendererCombo combo: the Gtk.CellRendererCombo() that
                                            called this method.
        :param int index: the position in the Requirement class Gtk.TreeModel()
                          associated with the data from the calling
                          Gtk.Entry().
        :return: None
        :rtype: None
        """
        _dic_keys = {
            2: 'requirement_type',
            7: 'priority',
            8: 'owner',
        }
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

        pub.sendMessage(
            'wvw_editing_requirement',
            module_id=self._requirement_id,
            key=_key,
            value=_new_text)

        combo.handler_unblock(self._lst_handler_id[index])

        return None

    def _on_edit(self, module_id, key, value):  # pylint: disable=unused-argument
        """
        Update the Requirement Work View Gtk.Widgets().

        This method updates the Requirement Work View Gtk.Widgets() with
        changes to the Requirement data model attributes.  This method is
        called whenever an attribute is edited in a different RAMSTK View.

        :param int module_id: the ID of the Requirement being edited.  This
                              parameter is required to allow the PyPubSub
                              signals to call this method and the
                              request_set_attributes() method in the
                              RAMSTKDataController.
        :param str key: the key in the Requirement attributes list of the
                        attribute that was edited.
        :param str value: the new text to update the Gtk.Widget() with.
        :return: None
        :rtype: None
        """
        if key == 'derived':
            self.chkDerived.handler_block(self._lst_handler_id[2])
            self.chkDerived.set_active(int(value))
            self.chkDerived.handler_unblock(self._lst_handler_id[2])
        elif key == 'description':
            self.txtName.handler_block(self._lst_handler_id[3])
            self.txtName.set_text(str(value))
            self.txtName.handler_unblock(self._lst_handler_id[3])
        elif key == 'figure_number':
            self.txtFigNum.handler_block(self._lst_handler_id[4])
            self.txtFigNum.set_text(str(value))
            self.txtFigNum.handler_unblock(self._lst_handler_id[4])
        elif key == 'page_number':
            self.txtPageNum.handler_block(self._lst_handler_id[6])
            self.txtPageNum.set_text(str(value))
            self.txtPageNum.handler_unblock(self._lst_handler_id[6])
        elif key == 'specification':
            self.txtSpecification.handler_block(self._lst_handler_id[10])
            self.txtSpecification.set_text(str(value))
            self.txtSpecification.handler_unblock(self._lst_handler_id[10])
        elif key == 'validated':
            self.chkValidated.handler_block(self._lst_handler_id[12])
            self.chkValidated.set_active(int(value))
            self.chkValidated.handler_unblock(self._lst_handler_id[12])
        elif key == 'validated_date':
            self.txtValidatedDate.handler_block(self._lst_handler_id[13])
            self.txtValidatedDate.set_text(str(value))
            self.txtValidatedDate.handler_unblock(self._lst_handler_id[13])

        return None

    def _on_focus_out(self, entry, index):
        """
        Retrieve RAMSTKEntry() changes and assign to Requirement attributes.

        This method retrieves changes to Requirement attributes through the
        various Gtk.Widgets() and assign the new data to the appropriate
        Requirement data model attribute.  This method is called by:

            * Gtk.Entry() 'changed' signal
            * Gtk.TextView() 'changed' signal

        This method sends the 'wvwEditedRequirement' message.

        :param Gtk.Entry entry: the Gtk.Entry() that called the method.
        :param int index: the position in the Requirement class Gtk.TreeModel()
                          associated with the data from the calling
                          Gtk.Widget().
        :return: None
        :rtype: None
        """
        _key = ''
        _text = ''

        entry.handler_block(self._lst_handler_id[index])

        if index == 0:
            _key = 'requirement_code'
            _new_text = str(entry.get_text())
        elif index == 1:
            _key = 'description'
            _new_text = str(entry.get_text())
        elif index == 4:
            _key = 'specification'
            _new_text = str(entry.get_text())
        elif index == 5:
            _key = 'page_number'
            _new_text = str(entry.get_text())
        elif index == 6:
            _key = 'figure_number'
            _new_text = str(entry.get_text())
        elif index == 10:
            _key = 'validate_date'
            _new_text = str(entry.get_text())

        pub.sendMessage(
            'editing_requirement',
            module_id=self._requirement_id,
            key=_key,
            value=_new_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return None

    def _on_toggled(self, togglebutton, index):
        """
        Retrieve Gtk.CheckButton() changes and assign to Requirement attribute.

        :param togglebutton: the Gtk.CheckButton() that called this method.
        :type togglebutton: :class:`Gtk.CheckButton`
        :param int index: the position in the Requirement class Gtk.TreeModel()
                          associated with the data from the calling
                          Gtk.Entry().
        :return: None
        :rtype: None
        """
        _key = ''
        _text = ''

        togglebutton.handler_block(self._lst_handler_id[index])

        if index == 3:
            _key = 'derived'
            _new_text = int(togglebutton.get_active())
        elif index == 9:
            _key = 'validate'
            _new_text = int(togglebutton.get_active())

        pub.sendMessage(
            'wvw_editing_requirement',
            module_id=self._requirement_id,
            key=_key,
            value=_new_text)

        togglebutton.handler_unblock(self._lst_handler_id[index])

        return None


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
    :ivar tvwClear: the :class:`Gtk.RAMSTKTreeView` listing all the Clarity
                    questions and answers.
    :ivar tvwComplete: the :class:`Gtk.RAMSTKTreeView` listing all the
                       Completeness questions and answers.
    :ivar tvwConsistent: the :class:`Gtk.RAMSTKTreeView` listing all the
                         Consistency questions and answers.
    :ivar tvwVerifiable: the :class:`Gtk.RAMSTKTreeView` listing all the
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
        self.tvwClear = Gtk.TreeView()
        self.tvwComplete = Gtk.TreeView()
        self.tvwConsistent = Gtk.TreeView()
        self.tvwVerifiable = Gtk.TreeView()

        self.pack_start(self.__make_buttonbox(), expand=False, fill=False)
        self.pack_start(self.__make_page(), expand=True, fill=True)
        self.show_all()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._do_load_page, 'selected_requirement')

    def __make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the Gtk.ButtonBox() for the Requirement Work View.

        :return: _buttonbox; the Gtk.ButtonBox() for the Requirement Work View.
        :rtype: :class:`Gtk.ButtonBox`
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

    def __make_page(self):
        """
        Make the Requirement Analysis Work View page.

        :return: _hpaned
        :rtype: :class:`Gtk.HPaned`
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
        _hpaned = Gtk.HPaned()

        # Create quadrant #1 (upper left) for determining if the
        # requirement is clear.
        _vpaned = Gtk.VPaned()
        _hpaned.pack1(_vpaned, resize=False)

        _scrollwindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                 Gtk.PolicyType.AUTOMATIC)
        _scrollwindow.add(self.tvwClear)

        _frame = ramstk.RAMSTKFrame(label=_(u"Clarity of Requirement"))
        _frame.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack1(_frame, resize=False)

        # Create quadrant #3 (lower left) for determining if the
        # requirement is complete.
        _scrollwindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                 Gtk.PolicyType.AUTOMATIC)
        _scrollwindow.add(self.tvwComplete)

        _frame = ramstk.RAMSTKFrame(label=_(u"Completeness of Requirement"))
        _frame.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack2(_frame, resize=False)

        # Create quadrant #2 (upper right) for determining if the
        # requirement is consistent.
        _vpaned = Gtk.VPaned()
        _hpaned.pack2(_vpaned, resize=False)

        _scrollwindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                 Gtk.PolicyType.AUTOMATIC)
        _scrollwindow.add(self.tvwConsistent)

        _frame = ramstk.RAMSTKFrame(label=_(u"Consistency of Requirement"))
        _frame.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack1(_frame, resize=False)

        # Create quadrant #4 (lower right) for determining if the
        # requirement is verifiable.
        _scrollwindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                 Gtk.PolicyType.AUTOMATIC)
        _scrollwindow.add(self.tvwVerifiable)

        _frame = ramstk.RAMSTKFrame(label=_(u"Verifiability of Requirement"))
        _frame.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
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
            _model = Gtk.ListStore(GObject.TYPE_INT, GObject.TYPE_STRING,
                                   GObject.TYPE_INT)
            _treeview.set_model(_model)
            _treeview.set_headers_visible(False)

            _column = Gtk.TreeViewColumn()

            _cell = Gtk.CellRendererText()
            _cell.set_property('editable', 0)
            _cell.set_property('visible', 0)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=0)

            _cell = Gtk.CellRendererText()
            _cell.set_property('cell-background', '#E5E5E5')
            _cell.set_property('editable', 0)
            _cell.set_property('wrap-width', 650)
            _cell.set_property('wrap-mode', Pango.WrapMode.WORD_CHAR)
            _cell.set_property('yalign', 0.1)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, markup=1)

            _cell = Gtk.CellRendererToggle()
            _cell.set_property('activatable', 1)
            _cell.set_property('cell-background', '#E5E5E5')
            _cell.connect('toggled', self._on_cell_edit, None, 2, _model,
                          _index)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, active=2)

            _column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)

            _treeview.append_column(_column)

        _model = self.tvwClear.get_model()
        _model.clear()
        for _index, _answer in enumerate(_lst_clear):
            _model.append(
                [_index, "<span weight='bold'>" + _answer + "</span>", 0])

        _model = self.tvwComplete.get_model()
        _model.clear()
        for _index, _answer in enumerate(_lst_complete):
            _model.append(
                [_index, "<span weight='bold'>" + _answer + "</span>", 0])

        _model = self.tvwConsistent.get_model()
        _model.clear()
        for _index, _answer in enumerate(_lst_consistent):
            _model.append(
                [_index, "<span weight='bold'>" + _answer + "</span>", 0])

        _model = self.tvwVerifiable.get_model()
        _model.clear()
        for _index, _answer in enumerate(_lst_verifiable):
            _model.append(
                [_index, "<span weight='bold'>" + _answer + "</span>", 0])

        # Insert the tab.
        _label = Gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Analysis") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(Gtk.Justification.CENTER)
        _label.set_tooltip_text(_(u"Analyzes the selected requirement."))
        _label.show_all()
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        return _hpaned

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

    def _do_load_page(self, attributes):
        """
        Load the Requirements analysis page.

        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']
        self._requirement_id = attributes['requirement_id']
        RAMSTKWorkView.on_select(
            self,
            title=_(u"Analyzing Requirement {0:s} - {1:s}").format(
                str(attributes['requirement_code']),
                str(attributes['description'])))

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

        return None

    def _do_request_update(self, __button):
        """
        Send request to save the currently selected Requirement.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage(
            'request_update_requirement', node_id=self._requirement_id)
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

        return None

    def _do_request_update_all(self, __button):
        """
        Request to save all the Requirements.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_requirements')
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

        return None

    def _on_cell_edit(self, cell, path, new_text, position, model, index):
        """
        Handle edits of the Requirement Analysis RAMSTKTreeview().

        :param cell: the Gtk.CellRendererToggle() that was toggled.
        :type cell: :class:`Gtk.CellRendererToggle`
        :param str path: the Gtk.TreeView() path of the Gtk.CellRenderer()
                         that was edited.
        :param model: the Gtk.TreeModel() for the Gtk.Treeview() that is being
                      edited.
        :type model: :class:`Gtk.TreeModel`
        :param int index: the index of the Requirement analysis Gtk.Treeview()
                          questions being answered.  Indices are:

                             * 0 = clarity
                             * 1 = completeness
                             * 2 = consistency
                             * 3 = verifiability

        :return: None
        :rtype: None
        """
        position = model[path][0]

        new_text = boolean_to_integer(not cell.get_active())
        model[path][2] = new_text

        try:
            if index == 0:
                self._lst_clear_a[position] = new_text
                _key = 'q_clarity_{0:d}'.format(position)
            elif index == 1:
                self._lst_complete_a[position] = new_text
                _key = 'q_complete_{0:d}'.format(position)
            elif index == 2:
                self._lst_consistent_a[position] = new_text
                _key = 'q_consistent_{0:d}'.format(position)
            elif index == 3:
                self._lst_verifiable_a[position] = new_text
                _key = 'q_verifiable_{0:d}'.format(position)
        except IndexError:
            _debug_msg = ("RAMSTK ERROR: No position {0:d} in Requirements "
                          "Analysis question list for index {1:d}.").format(
                              position, index)
            self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_DEBUG_LOG.error(
                _debug_msg)

        pub.sendMessage(
            'wvw_editing_requirement',
            module_id=self._requirement_id,
            key=_key,
            value=new_text)

        return None
