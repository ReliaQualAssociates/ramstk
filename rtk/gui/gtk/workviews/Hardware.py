# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.Hardware.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Hardware Work View."""

from datetime import date  # pragma: no cover

from pubsub import pub  # pylint: disable=E0401

# Import other RTK modules.
from Utilities import boolean_to_integer  # pylint: disable=E0401
from gui.gtk import rtk  # pylint: disable=E0401
from gui.gtk.rtk.Widget import _, gtk  # pylint: disable=E0401,W0611
from .WorkView import RTKWorkView


class GeneralData(RTKWorkView):
    """
    Display Hardware attribute data in the RTK Work Book.

    The Work View displays all the general data attributes for the selected
    Hardware. The attributes of a Hardware General Data Work View are:

    :ivar int _hardware_id: the ID of the Hardware currently being displayed.
    :ivar chkSafetyCritical: the :class:`rtk.gui.gtk.rtk.RTKCheckButton` to
                             display/edit the Hardware's safety criticality.
    :ivar txtTotalCost: the :class:`rtk.gui.gtk.rtk.RTKEntry` to display the
                        Hardware cost.
    :ivar txtModeCount: the :class:`rtk.gui.gtk.rtk.RTKEntry` to display the
                        number of failure modes the hardware is susceptible to.

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | chkRepairable - `toggled`                 |
    +----------+-------------------------------------------+
    |     1    | chkTagged - `toggled`                     |
    +----------+-------------------------------------------+
    |     2    | cmbCategory - `changed`                   |
    +----------+-------------------------------------------+
    |     3    | cmbCostType - `changed`                   |
    +----------+-------------------------------------------+
    |     4    | cmbManufacturer - `changed`               |
    +----------+-------------------------------------------+
    |     5    | cmbSubcategory - `changed`                |
    +----------+-------------------------------------------+
    |     6    | txtAltPartNum - `changed`                 |
    +----------+-------------------------------------------+
    |     7    | txtAttachments - `changed`                |
    +----------+-------------------------------------------+
    |     8    | txtCAGECode - `changed`                   |
    +----------+-------------------------------------------+
    |     9    | txtCompRefDes - `changed`                 |
    +----------+-------------------------------------------+
    |    10    | txtCost - `changed`                       |
    +----------+-------------------------------------------+
    |    11    | txtDescription - `changed`                |
    +----------+-------------------------------------------+
    |    12    | txtFigureNumber - `changed`               |
    +----------+-------------------------------------------+
    |    13    | txtLCN - `changed`                        |
    +----------+-------------------------------------------+
    |    14    | txtName - `changed`                       |
    +----------+-------------------------------------------+
    |    15    | txtNSN - `changed`                        |
    +----------+-------------------------------------------+
    |    16    | txtPageNumber - `changed`                 |
    +----------+-------------------------------------------+
    |    17    | txtPartNumber - `changed`                 |
    +----------+-------------------------------------------+
    |    18    | txtQuantity - `changed`                   |
    +----------+-------------------------------------------+
    |    19    | txtRefDes - `changed`                     |
    +----------+-------------------------------------------+
    |    20    | txtRemarks - `changed`                    |
    +----------+-------------------------------------------+
    |    21    | txtSpecification - `changed`              |
    +----------+-------------------------------------------+
    |    22    | txtYearMade - `changed`                   |
    +----------+-------------------------------------------+
    """

    def __init__(self, controller):
        """
        Initialize the Work View for the Hardware package.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKWorkView.__init__(self, controller, module='Hardware')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        # We add an empty string in the positions where a gtk.CheckButton()
        # will be placed.
        self._lst_gendata_labels = [[
            _(u"Part Number:"),
            _(u"Alternate Part Number:"),
            _(u"Name:"),
            _(u"Description:"),
            _(u"Reference Designator:"),
            _(u"Composite Ref. Des."),
            _(u"Category:"),
            _(u"Subcategory:"),
            _(u"Specification:"),
            _(u"Page Number:"),
            _(u"Figure Number:"), "",
            _(u"LCN:")
        ], [
            _(u"Manufacturer:"),
            _(u"CAGE Code:"),
            _(u"NSN:"),
            _(u"Year Made:"),
            _(u"Quantity:"),
            _(u"Unit Cost:"),
            _(u"Cost Calculation Method:")
        ], ["", _(u"Attachments:"), _(u"Remarks:")]]

        # Initialize private scalar attributes.
        self._hardware_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # General data page widgets.

        # General Data page widgets.
        self.chkRepairable = rtk.RTKCheckButton(
            label=_(u"Repairable"),
            tooltip=_(u"Indicates whether or not the selected hardware item "
                      u"is repairable."))
        self.chkTagged = rtk.RTKCheckButton(label=_(u"Tagged Part"))

        self.cmbCategory = rtk.RTKComboBox()
        self.cmbCostType = rtk.RTKComboBox()
        self.cmbManufacturer = rtk.RTKComboBox(simple=False)
        self.cmbSubcategory = rtk.RTKComboBox()

        self.txtAltPartNum = rtk.RTKEntry(tooltip=_(
            u"The alternate part "
            u"number (if any) of the "
            u"selected hardware item."))
        self.txtAttachments = rtk.RTKTextView(
            gtk.TextBuffer(),
            width=600,
            tooltip=_(u"Hyperlinks to any documents associated with the "
                      u"selected hardware item."))
        self.txtCAGECode = rtk.RTKEntry(tooltip=_(u"The Commerical and "
                                                  u"Government Entity (CAGE) "
                                                  u"Code of the selected "
                                                  u"hardware item."))
        self.txtCompRefDes = rtk.RTKEntry(tooltip=_(
            u"The composite reference "
            u"designator of the "
            u"selected hardware item."))
        self.txtCost = rtk.RTKEntry(
            width=100,
            tooltip=_(u"The unit cost of the selected hardware item."))
        self.txtDescription = rtk.RTKTextView(
            gtk.TextBuffer(),
            width=600,
            tooltip=_(u"The description of the selected hardware item."))
        self.txtFigureNumber = rtk.RTKEntry(tooltip=_(u"The figure number in "
                                                      u"the governing "
                                                      u"specification for the "
                                                      u"selected hardware "
                                                      u"item."))
        self.txtLCN = rtk.RTKEntry(tooltip=_(u"The Logistics Control Number "
                                             u"(LCN) of the selected hardware "
                                             u"item."))
        self.txtName = rtk.RTKEntry(
            width=600, tooltip=_(u"The name of the selected hardware item."))
        self.txtNSN = rtk.RTKEntry(tooltip=_(
            u"The National Stock Number (NSN) of the selected hardware item."))
        self.txtPageNumber = rtk.RTKEntry(tooltip=_(u"The page number in the "
                                                    u"governing specification "
                                                    u"for the selected "
                                                    u"hardware item."))
        self.txtPartNumber = rtk.RTKEntry(
            tooltip=_(u"The part number of the selected hardware item."))
        self.txtQuantity = rtk.RTKEntry(
            width=50,
            tooltip=_(
                u"The number of the selected hardware items in the design."))
        self.txtRefDes = rtk.RTKEntry(tooltip=_(
            u"The reference designator of the selected hardware item."))
        self.txtRemarks = rtk.RTKTextView(
            gtk.TextBuffer(),
            width=600,
            tooltip=_(u"Enter any remarks associated with the selected "
                      u"hardware item."))
        self.txtSpecification = rtk.RTKEntry(tooltip=_(
            u"The specification (if any) governing the selected hardware item."
        ))
        self.txtYearMade = rtk.RTKEntry(
            width=100,
            tooltip=_(
                u"The year the the selected hardware item was manufactured."))

        # Connect to callback hardwares for editable gtk.Widgets().
        self._lst_handler_id.append(
            self.chkRepairable.connect('toggled', self._on_toggled, 0))
        self._lst_handler_id.append(
            self.chkTagged.connect('toggled', self._on_toggled, 1))

        self._lst_handler_id.append(
            self.cmbCategory.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbCostType.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbManufacturer.connect('changed', self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.cmbSubcategory.connect('changed', self._on_combo_changed, 5))

        self._lst_handler_id.append(
            self.txtAltPartNum.connect('changed', self._on_focus_out, 6))
        self._lst_handler_id.append(self.txtAttachments.do_get_buffer()
                                    .connect('changed', self._on_focus_out, 7))
        self._lst_handler_id.append(
            self.txtCAGECode.connect('changed', self._on_focus_out, 8))
        self._lst_handler_id.append(
            self.txtCompRefDes.connect('changed', self._on_focus_out, 9))
        self._lst_handler_id.append(
            self.txtCost.connect('changed', self._on_focus_out, 10))
        self._lst_handler_id.append(self.txtDescription.do_get_buffer(
        ).connect('changed', self._on_focus_out, 11))
        self._lst_handler_id.append(
            self.txtFigureNumber.connect('changed', self._on_focus_out, 12))
        self._lst_handler_id.append(
            self.txtLCN.connect('changed', self._on_focus_out, 13))
        self._lst_handler_id.append(
            self.txtName.connect('changed', self._on_focus_out, 14))
        self._lst_handler_id.append(
            self.txtNSN.connect('changed', self._on_focus_out, 15))
        self._lst_handler_id.append(
            self.txtPageNumber.connect('changed', self._on_focus_out, 16))
        self._lst_handler_id.append(
            self.txtPartNumber.connect('changed', self._on_focus_out, 17))
        self._lst_handler_id.append(
            self.txtQuantity.connect('changed', self._on_focus_out, 18))
        self._lst_handler_id.append(
            self.txtRefDes.connect('changed', self._on_focus_out, 19))
        self._lst_handler_id.append(self.txtRemarks.do_get_buffer().connect(
            'changed', self._on_focus_out, 20))
        self._lst_handler_id.append(
            self.txtSpecification.connect('changed', self._on_focus_out, 21))
        self._lst_handler_id.append(
            self.txtYearMade.connect('changed', self._on_focus_out, 22))

        self.pack_start(self._make_buttonbox(), expand=False, fill=False)
        self.pack_start(self._make_general_data_page(), expand=True, fill=True)
        self.show_all()

        pub.subscribe(self._on_select, 'selectedHardware')
        pub.subscribe(self._on_edit, 'mvwEditedHardware')

    def _do_load_subcategory(self, category):
        """
        Load the component subcategory RTKCombo().

        This method loads the component subcategory RTKCombo() when the
        component category RTKCombo() is changed.

        :param int category: the component category ID to load the subcategory
                             RTKCombo() for.
        :return: False if successful or True if an error is encountered
        :rtype: bool
        """
        _return = False

        _model = self.cmbSubcategory.get_model()
        _model.clear()

        _subcategory = self._mdcRTK.RTK_CONFIGURATION.RTK_SUBCATEGORIES[
            category]
        _data = []
        for _key in _subcategory:
            _data.append([_subcategory[_key]])

        self.cmbSubcategory.do_load_combo(_data)

        return _return

    def _do_request_update(self, __button):
        """
        Send request to save the currently selected Hardware.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_update(self._hardware_id)

    def _make_buttonbox(self):
        """
        Make the gtk.ButtonBox() for the Hardware class Work View.

        :return: _buttonbox; the gtk.ButtonBox() for the Hardware class Work
                 View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Saves the currently selected Hardware to the open "
              u"RTK Project database."),
        ]
        _callbacks = [
            self._do_request_update,
        ]
        _icons = [
            'save',
        ]

        _buttonbox = RTKWorkView._make_buttonbox(self, _icons, _tooltips,
                                                 _callbacks, 'vertical')

        return _buttonbox

    def _make_general_data_page(self):
        """
        Make the Hardware class gtk.Notebook() general data page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Load the gtk.ComboBox() widgets.
        _model = self.cmbCategory.get_model()
        _model.clear()

        _data = []
        for _key in self._mdcRTK.RTK_CONFIGURATION.RTK_CATEGORIES:
            _data.append([self._mdcRTK.RTK_CONFIGURATION.RTK_CATEGORIES[_key]])
        self.cmbCategory.do_load_combo(_data)

        _model = self.cmbCostType.get_model()
        _model.clear()

        _data = []
        for _key in self._mdcRTK.RTK_CONFIGURATION.RTK_COST_TYPE:
            _data.append(
                [self._mdcRTK.RTK_CONFIGURATION.RTK_COST_TYPE[_key][1]])
        self.cmbCostType.do_load_combo(_data)

        _model = self.cmbManufacturer.get_model()
        _model.clear()

        _data = []
        for _key in self._mdcRTK.RTK_CONFIGURATION.RTK_MANUFACTURERS:
            _data.append(
                self._mdcRTK.RTK_CONFIGURATION.RTK_MANUFACTURERS[_key])
        self.cmbManufacturer.do_load_combo(_data, simple=False)

        # Build the General Data page starting with the left half.
        _hbox = gtk.HBox()
        _fixed = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fixed)
        _frame = rtk.RTKFrame(label=_(u"Hardware Description"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_gendata_labels[0],
                                              _fixed, 5, 5)
        _x_pos += 50

        _hbox.pack_start(_frame, expand=True, fill=True)

        # Move the labels after the description to account for the extra
        # vertical space needed by the description RTKTextView().
        for _index in xrange(4, 13):
            _fixed.move(_fixed.get_children()[_index], 5,
                        _y_pos[_index - 1] + 100)

        _fixed.put(self.txtPartNumber, _x_pos, _y_pos[0])
        _fixed.put(self.txtAltPartNum, _x_pos, _y_pos[1])
        _fixed.put(self.txtName, _x_pos, _y_pos[2])
        _fixed.put(self.txtDescription.scrollwindow, _x_pos, _y_pos[3])
        _fixed.put(self.txtRefDes, _x_pos, _y_pos[3] + 100)
        _fixed.put(self.txtCompRefDes, _x_pos, _y_pos[4] + 100)
        _fixed.put(self.cmbCategory, _x_pos, _y_pos[5] + 100)
        _fixed.put(self.cmbSubcategory, _x_pos, _y_pos[6] + 100)
        _fixed.put(self.txtSpecification, _x_pos, _y_pos[7] + 100)
        _fixed.put(self.txtPageNumber, _x_pos, _y_pos[8] + 100)
        _fixed.put(self.txtFigureNumber, _x_pos, _y_pos[9] + 100)
        _fixed.put(self.chkRepairable, _x_pos, _y_pos[10] + 100)
        _fixed.put(self.txtLCN, _x_pos, _y_pos[11] + 100)

        _fixed.show_all()

        # Now add the right hand side starting with the top pane.
        _vpaned = gtk.VPaned()
        _fixed = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fixed)
        _frame = rtk.RTKFrame(label=_(u"Purchasing Information"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_gendata_labels[1],
                                              _fixed, 5, 5)
        _x_pos += 50

        _fixed.put(self.cmbManufacturer, _x_pos, _y_pos[0])
        _fixed.put(self.txtCAGECode, _x_pos, _y_pos[1])
        _fixed.put(self.txtNSN, _x_pos, _y_pos[2])
        _fixed.put(self.txtYearMade, _x_pos, _y_pos[3])
        _fixed.put(self.txtQuantity, _x_pos, _y_pos[4])
        _fixed.put(self.txtCost, _x_pos, _y_pos[5])
        _fixed.put(self.cmbCostType, _x_pos, _y_pos[6])

        _fixed.show_all()

        _vpaned.pack1(_frame, True, True)
        _fixed = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fixed)
        _frame = rtk.RTKFrame(label=_(u"Miscellaneous Information"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_gendata_labels[2],
                                              _fixed, 5, 5)
        _x_pos += 50

        # Move the Remarks label down to accomodate for the Attachments entry.
        _fixed.move(_fixed.get_children()[2], 5, _y_pos[1] + 100)

        _fixed.put(self.chkTagged, _x_pos, _y_pos[0])
        _fixed.put(self.txtAttachments.scrollwindow, _x_pos, _y_pos[1])
        _fixed.put(self.txtRemarks.scrollwindow, _x_pos, _y_pos[1] + 100)

        _fixed.show_all()

        _vpaned.pack2(_frame, True, True)

        _hbox.pack_end(_vpaned, expand=True, fill=True)

        # Create the label for the gtk.Notebook() tab.
        _label = rtk.RTKLabel(
            _(u"General\nData"),
            height=30,
            width=-1,
            justify=gtk.JUSTIFY_CENTER,
            tooltip=_(u"Displays general information for the selected "
                      u"hardware item."))
        self.hbx_tab_label.pack_start(_label)

        return _hbox

    def _on_combo_changed(self, combo, index):
        """
        Retrieve gtk.ComboBox() changes and assign to Hardware attribute.

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
            _hardware = self._dtc_data_controller.request_select(
                self._hardware_id)

            if index == 2:
                _hardware['category_id'] = combo.get_active() - 1
                self._do_load_subcategory(_hardware['category_id'])
            elif index == 3:
                _hardware['cost_type_id'] = combo.get_active() - 1
            elif index == 4:
                _hardware['manufacturer_id'] = combo.get_active() - 1
                self.txtCAGECode.set_text(_model.get(_row, 2)[0])
            elif index == 5:
                _hardware['subcategory_id'] = combo.get_active() - 1

        combo.handler_unblock(self._lst_handler_id[index])

        return _return

    def _on_edit(self, index, new_text):
        """
        Update the Work View gtk.Widgets() when Hardware attributes change.

        This method is called whenever an attribute is edited in a different
        view.

        :param int index: the index in the Hardware attributes list of the
                          attribute that was edited.
        :param str new_text: the new text to update the gtk.Widget() with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        if index == 5:
            self.txtCode.handler_block(self._lst_handler_id[0])
            self.txtCode.set_text(str(new_text))
            self.txtCode.handler_unblock(self._lst_handler_id[0])
        elif index == 15:
            self.txtName.handler_block(self._lst_handler_id[1])
            self.txtName.set_text(new_text)
            self.txtName.handler_unblock(self._lst_handler_id[1])
        elif index == 17:
            _textbuffer = self.txtRemarks.do_get_buffer()
            _textbuffer.handler_block(self._lst_handler_id[2])
            _textbuffer.set_text(new_text)
            _textbuffer.handler_unblock(self._lst_handler_id[2])

        return _return

    def _on_focus_out(self, entry, index):
        """
        Retrieve changes made in RTKEntry() widgets..

        This method is called by:

            * gtk.Entry() 'changed' signal
            * gtk.TextView() 'changed' signal

        This method sends the 'wvwEditedHardware' message.

        :param gtk.Entry entry: the gtk.Entry() that called the method.
        :param int index: the position in the Hardware class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Widget().  Indices are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    6    | txtAltPartNum    |   15    | txtNSN           |
            +---------+------------------+---------+------------------+
            |    7    | txtAttachments   |   16    | txtPageNumber    |
            +---------+------------------+---------+------------------+
            |    8    | txtCAGECode      |   17    | txtPartNumber    |
            +---------+------------------+---------+------------------+
            |    9    | txtCompRefDes    |   18    | txtQuantity      |
            +---------+------------------+---------+------------------+
            |   10    | txtCost          |   19    | txtRefDes        |
            +---------+------------------+---------+------------------+
            |   11    | txtDescription   |   20    | txtRemarks       |
            +---------+------------------+---------+------------------+
            |   12    | txtFigureNumber  |   21    | txtSpecification |
            +---------+------------------+---------+------------------+
            |   13    | txtLCN           |   22    | txtYearMade      |
            +---------+------------------+---------+------------------+
            |   14    | txtName          |         |                  |
            +---------+------------------+---------+------------------+

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _index = -1
        _return = False
        _text = ''

        entry.handler_block(self._lst_handler_id[index])

        if self._dtc_data_controller is not None:
            _hardware = self._dtc_data_controller.request_select(
                self._hardware_id)

            if index == 6:
                _position = 2
                _text = str(entry.get_text())
                _hardware['alt_part_num'] = _text
            elif index == 7:
                _position = None
                _text = self.txtAttachments.do_get_text()
                _hardware['attachments'] = _text
            elif index == 8:
                _position = 3
                _text = str(entry.get_text())
                _hardware['cage_code'] = _text
            elif index == 9:
                _position = 4
                _text = str(entry.get_text())
                _hardware['comp_ref_des'] = _text
            elif index == 10:
                _position = 5
                try:
                    _text = float(entry.get_text())
                except ValueError:
                    _text = 0.0
                _hardware['cost'] = _text
            elif index == 11:
                _position = 8
                _text = self.txtDescription.do_get_text()
                _hardware['description'] = _text
            elif index == 12:
                _position = 10
                _text = str(entry.get_text())
                _hardware['figure_number'] = _text
            elif index == 13:
                _position = 11
                _text = str(entry.get_text())
                _hardware['lcn'] = _text
            elif index == 14:
                _position = 15
                _text = str(entry.get_text())
                _hardware['name'] = _text
            elif index == 15:
                _position = 16
                _text = str(entry.get_text())
                _hardware['nsn'] = _text
            elif index == 16:
                _position = 17
                _text = str(entry.get_text())
                _hardware['page_number'] = _text
            elif index == 17:
                _position = 20
                _text = str(entry.get_text())
                _hardware['part_number'] = _text
            elif index == 18:
                _position = 21
                try:
                    _text = int(entry.get_text())
                except ValueError:
                    _text = 1
                _hardware['quantity'] = _text
            elif index == 19:
                _position = 22
                _text = str(entry.get_text())
                _hardware['ref_des'] = _text
            elif index == 20:
                _position = 23
                _text = self.txtRemarks.do_get_text()
                _hardware['remarks'] = _text
            elif index == 21:
                _position = 25
                _text = str(entry.get_text())
                _hardware['specification_number'] = _text
            elif index == 22:
                _position = 29
                try:
                    _text = int(entry.get_text())
                except ValueError:
                    _text = date.today()
                _hardware['year_of_manufacture'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _hardware, 'general')

            pub.sendMessage(
                'wvwEditedHardware', position=_position, new_text=_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def _on_select(self, module_id, **kwargs):
        """
        Load the Hardware Work View class gtk.Notebook() widgets.

        :param int hardware_id: the Hardware ID of the selected/edited
                                Hardware.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        self._dtc_data_controller = self._mdcRTK.dic_controllers['hardware']
        _hardware = self._dtc_data_controller.request_select(self._hardware_id)

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id, 'general')

        # Disable the category RTKCombo() if the hardware item is not a part.
        if _attributes['part'] == 1:
            self.cmbCategory.set_button_sensitivity(gtk.SENSITIVITY_ON)

            self.cmbCategory.handler_block(self._lst_handler_id[2])
            self.cmbCategory.set_active(_hardware['category_id'] + 1)
            self.cmbCategory.handler_unblock(self._lst_handler_id[2])

            self.cmbSubcategory.handler_block(self._lst_handler_id[5])
            self.cmbSubcategory.set_active(_hardware['subcategory_id'] + 1)
            self.cmbSubcategory.handler_unblock(self._lst_handler_id[5])

        else:
            self.cmbCategory.set_button_sensitivity(gtk.SENSITIVITY_OFF)

        self.chkRepairable.handler_block(self._lst_handler_id[0])
        self.chkRepairable.set_active(_hardware['repairable'])
        self.chkRepairable.handler_unblock(self._lst_handler_id[0])

        self.chkTagged.handler_block(self._lst_handler_id[1])
        self.chkTagged.set_active(_hardware['tagged_part'])
        self.chkTagged.handler_unblock(self._lst_handler_id[1])

        self.cmbCostType.handler_block(self._lst_handler_id[3])
        self.cmbCostType.set_active(_hardware['cost_type_id'] + 1)
        self.cmbCostType.handler_unblock(self._lst_handler_id[3])

        self.cmbManufacturer.handler_block(self._lst_handler_id[4])
        self.cmbManufacturer.set_active(_hardware['manufacturer_id'] + 1)
        self.cmbManufacturer.handler_unblock(self._lst_handler_id[4])

        self.txtAltPartNum.handler_block(self._lst_handler_id[6])
        self.txtAltPartNum.set_text(str(_hardware['alt_part_num']))
        self.txtAltPartNum.handler_unblock(self._lst_handler_id[6])

        _textbuffer = self.txtAttachments.do_get_buffer()
        _textbuffer.handler_block(self._lst_handler_id[7])
        _textbuffer.set_text(_hardware['attachments'])
        _textbuffer.handler_unblock(self._lst_handler_id[7])

        self.txtCAGECode.handler_block(self._lst_handler_id[8])
        self.txtCAGECode.set_text(str(_hardware['cage_code']))
        self.txtCAGECode.handler_unblock(self._lst_handler_id[8])

        self.txtCompRefDes.handler_block(self._lst_handler_id[9])
        self.txtCompRefDes.set_text(str(_hardware['comp_ref_des']))
        self.txtCompRefDes.handler_unblock(self._lst_handler_id[9])

        self.txtCost.handler_block(self._lst_handler_id[10])
        self.txtCost.set_text(str(_hardware['cost']))
        self.txtCost.handler_unblock(self._lst_handler_id[10])

        _textbuffer = self.txtDescription.do_get_buffer()
        _textbuffer.handler_block(self._lst_handler_id[11])
        _textbuffer.set_text(str(_hardware['description']))
        _textbuffer.handler_unblock(self._lst_handler_id[11])

        self.txtFigureNumber.handler_block(self._lst_handler_id[12])
        self.txtFigureNumber.set_text(str(_hardware['figure_number']))
        self.txtFigureNumber.handler_unblock(self._lst_handler_id[12])

        self.txtLCN.handler_block(self._lst_handler_id[13])
        self.txtLCN.set_text(str(_hardware['lcn']))
        self.txtLCN.handler_unblock(self._lst_handler_id[13])

        self.txtName.handler_block(self._lst_handler_id[14])
        self.txtName.set_text(str(_hardware['name']))
        self.txtName.handler_unblock(self._lst_handler_id[14])

        self.txtNSN.handler_block(self._lst_handler_id[15])
        self.txtNSN.set_text(str(_hardware['nsn']))
        self.txtNSN.handler_unblock(self._lst_handler_id[15])

        self.txtPageNumber.handler_block(self._lst_handler_id[16])
        self.txtPageNumber.set_text(str(_hardware['page_number']))
        self.txtPageNumber.handler_unblock(self._lst_handler_id[16])

        self.txtPartNumber.handler_block(self._lst_handler_id[17])
        self.txtPartNumber.set_text(str(_hardware['part_number']))
        self.txtPartNumber.handler_unblock(self._lst_handler_id[17])

        self.txtQuantity.handler_block(self._lst_handler_id[18])
        self.txtQuantity.set_text(str(_hardware['quantity']))
        self.txtQuantity.handler_unblock(self._lst_handler_id[18])

        self.txtRefDes.handler_block(self._lst_handler_id[19])
        self.txtRefDes.set_text(str(_hardware['ref_des']))
        self.txtRefDes.handler_unblock(self._lst_handler_id[19])

        _textbuffer = self.txtRemarks.do_get_buffer()
        _textbuffer.handler_block(self._lst_handler_id[20])
        _textbuffer.set_text(_hardware['remarks'])
        _textbuffer.handler_unblock(self._lst_handler_id[20])

        self.txtSpecification.handler_block(self._lst_handler_id[21])
        self.txtSpecification.set_text(str(_hardware['specification_number']))
        self.txtSpecification.handler_unblock(self._lst_handler_id[21])

        self.txtYearMade.handler_block(self._lst_handler_id[22])
        self.txtYearMade.set_text(str(_hardware['year_of_manufacture']))
        self.txtYearMade.handler_unblock(self._lst_handler_id[22])

        return _return

    def _on_toggled(self, togglebutton, index):
        """
        Handle RTKCheckButton() 'toggle' signals.

        :param togglebutton: the RTKToggleButton() that called this method.
        :type: :class:`rtk.gui.gtk.rtk.Button.RTKToggleButton`
        :param int index: the index in the signal handler ID list.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        togglebutton.handler_block(self._lst_handler_id[index])

        if self._dtc_data_controller is not None:
            _hardware = self._dtc_data_controller.request_select(
                self._hardware_id)

            if index == 0:
                _position = 24
                _text = boolean_to_integer(self.chkRepairable.get_active())
                _hardware['repairable'] = _text
            elif index == 1:
                _position = 26
                _text = boolean_to_integer(self.chkTagged.get_active())
                _hardware['tagged_part'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _hardware, 'general')

            pub.sendMessage(
                'wvwEditedHardware', position=_position, new_text=_text)

        togglebutton.handler_unblock(self._lst_handler_id[index])

        return _return


class AssessmentInputs(RTKWorkView):
    """
    Display Hardware assessment input attribute data in the RTK Work Book.

    The Hardware assessment input view displays all the assessment inputs for
    the selected Hardware item.  This includes, currently, inputs for
    MIL-HDBK-217FN2 and NSWC-11.  The attributes of a Hardware assessment
    input view are:

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    """

    def __init__(self, controller):
        """
        Initialize an instance of the Hardware assessment input view.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKWorkView.__init__(self, controller, module='Hardware')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_assess_labels = [[
            _(u"Assessment Method:"),
            _(u"Assessment Model:"),
            _(u"Failure Distribution:"),
            _(u"Scale Parameter:"),
            _(u"Shape Parameter:"),
            _(u"Location Parameter:"),
            _(u"Specified Hazard Rate [h(t)]:"),
            _(u"Variance h(t):"),
            _(u"Specified MTBF:"),
            _(u"MTBF Variance:"),
            _(u"Additive Adjustment Factor:"),
            _(u"Multiplicative Adjustment Factor:")
        ], [
            _(u"Active Environment:"),
            _(u"Dormant Environment:"),
            _(u"Active Temperature (\u00B0C):"),
            _(u"Dormant Temperature (\u00B0C):")
        ]]

        # Initialize private scalar attributes.
        self._hardware_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbActiveEnviron = rtk.RTKComboBox(
            tooltip=_(u"The operating environment for the hardware item."))
        self.cmbDormantEnviron = rtk.RTKComboBox(
            tooltip=_(u"The storage environment for the hardware item."))
        self.cmbFailureDist = rtk.RTKComboBox(tooltip=_(
            u"The statistical failure distribution of the hardware item."))
        self.cmbHRMethod = rtk.RTKComboBox(tooltip=_(
            u"The method for assessing the reliability attributes of the "
            u"hardware item."))
        self.cmbHRModel = rtk.RTKComboBox(tooltip=_(
            u"The model to use for assessing the relibility attributes of "
            u"the hardware item."))

        self.fraDesignRatings = rtk.RTKFrame(label=_(u"Design Ratings"))
        self.fraOperatingStress = rtk.RTKFrame(label=_(u"Operating Stresses"))

        self.txtActiveTemp = rtk.RTKEntry(tooltip=_(
            u"The ambient temperature in the operating environment."))
        self.txtAddAdj = rtk.RTKEntry(tooltip=_(
            u"An adjustment factor to add to the assessed hazard rate or "
            u"MTBF."))
        self.txtDormantTemp = rtk.RTKEntry(
            tooltip=_(u"The ambient temperature in the storage environment."))
        self.txtFailScale = rtk.RTKEntry(tooltip=_(
            u"The scale parameter of the statistical failure distribution."))
        self.txtFailShape = rtk.RTKEntry(tooltip=_(
            u"The shape parameter of the statistical failure distribution."))
        self.txtFailLocation = rtk.RTKEntry(tooltip=_(
            u"The location parameter of the statistical failure "
            u"distribution."))
        self.txtMultAdj = rtk.RTKEntry(tooltip=_(
            u"An adjustment factor to multiply the assessed hazard rate or "
            u"MTBF by."))
        self.txtSpecifiedHt = rtk.RTKEntry(
            tooltip=_(u"The stated hazard rate."))
        self.txtSpecifiedHtVar = rtk.RTKEntry(
            tooltip=_(u"The variance of the stated hazard rate."))
        self.txtSpecifiedMTBF = rtk.RTKEntry(
            tooltip=_(u"The stated mean time between failure (MTBF)."))
        self.txtSpecifiedMTBFVar = rtk.RTKEntry(tooltip=_(
            u"The variance of the stated mean time between failure "
            u"(MTBF)."))

    def _do_request_calculate(self, __button):
        """
        Send request to calculate the selected hardware.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _error_code = 0
        _msg = ['', '']

        if self._dtc_data_controller.request_calculate_mtbf(self._hardware_id):
            _error_code = 1
            _msg[0] = 'Error calculating reliability attributes.'

        if self._dtc_data_controller.request_calculate_availability(
                self._hardware_id):
            _error_code = 1
            _msg[1] = 'Error calculating availability attributes.'

        if _error_code != 0:
            _prompt = _(u"An error occurred when attempting to calculate "
                        u"Hardware {0:d}. \n\n\t" + _msg[0] + "\n\t" + _msg[1]
                        + "\n\n").format(self._hardware_id)
            _error_dialog = rtk.RTKMessageDialog(
                _prompt, self._dic_icons['error'], 'error')
            if _error_dialog.do_run() == gtk.RESPONSE_OK:
                _error_dialog.do_destroy()

            _return = True
        else:
            pub.sendMessage('calculatedHardware', module_id=self._hardware_id)

        return _return

    def _make_assessment_input_page(self):
        """
        Make the Hardware class gtk.Notebook() assessment input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Load the gtk.ComboBox() widgets.
        _model = self.cmbCategory.get_model()
        _model.clear()

        _data = []
        for _key in self._mdcRTK.RTK_CONFIGURATION.RTK_CATEGORIES:
            _data.append([self._mdcRTK.RTK_CONFIGURATION.RTK_CATEGORIES[_key]])
        self.cmbCategory.do_load_combo(_data)

        _model = self.cmbCostType.get_model()
        _model.clear()

        _data = []
        for _key in self._mdcRTK.RTK_CONFIGURATION.RTK_COST_TYPE:
            _data.append(
                [self._mdcRTK.RTK_CONFIGURATION.RTK_COST_TYPE[_key][1]])
        self.cmbCostType.do_load_combo(_data)

        _model = self.cmbManufacturer.get_model()
        _model.clear()

        _data = []
        for _key in self._mdcRTK.RTK_CONFIGURATION.RTK_MANUFACTURERS:
            _data.append(
                self._mdcRTK.RTK_CONFIGURATION.RTK_MANUFACTURERS[_key])
        self.cmbManufacturer.do_load_combo(_data, simple=False)

        # Build the General Data page starting with the left half.
        _hbox = gtk.HBox()
        _fixed = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fixed)
        _frame = rtk.RTKFrame(label=_(u"Hardware Description"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_gendata_labels[0],
                                              _fixed, 5, 5)
        _x_pos += 50

        _hbox.pack_start(_frame, expand=True, fill=True)

        # Move the labels after the description to account for the extra
        # vertical space needed by the description RTKTextView().
        for _index in xrange(4, 13):
            _fixed.move(_fixed.get_children()[_index], 5,
                        _y_pos[_index - 1] + 100)

        _fixed.put(self.txtPartNumber, _x_pos, _y_pos[0])
        _fixed.put(self.txtAltPartNum, _x_pos, _y_pos[1])
        _fixed.put(self.txtName, _x_pos, _y_pos[2])
        _fixed.put(self.txtDescription.scrollwindow, _x_pos, _y_pos[3])
        _fixed.put(self.txtRefDes, _x_pos, _y_pos[3] + 100)
        _fixed.put(self.txtCompRefDes, _x_pos, _y_pos[4] + 100)
        _fixed.put(self.cmbCategory, _x_pos, _y_pos[5] + 100)
        _fixed.put(self.cmbSubcategory, _x_pos, _y_pos[6] + 100)
        _fixed.put(self.txtSpecification, _x_pos, _y_pos[7] + 100)
        _fixed.put(self.txtPageNumber, _x_pos, _y_pos[8] + 100)
        _fixed.put(self.txtFigureNumber, _x_pos, _y_pos[9] + 100)
        _fixed.put(self.chkRepairable, _x_pos, _y_pos[10] + 100)
        _fixed.put(self.txtLCN, _x_pos, _y_pos[11] + 100)

        _fixed.show_all()

        # Now add the right hand side starting with the top pane.
        _vpaned = gtk.VPaned()
        _fixed = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fixed)
        _frame = rtk.RTKFrame(label=_(u"Purchasing Information"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_gendata_labels[1],
                                              _fixed, 5, 5)
        _x_pos += 50

        _fixed.put(self.cmbManufacturer, _x_pos, _y_pos[0])
        _fixed.put(self.txtCAGECode, _x_pos, _y_pos[1])
        _fixed.put(self.txtNSN, _x_pos, _y_pos[2])
        _fixed.put(self.txtYearMade, _x_pos, _y_pos[3])
        _fixed.put(self.txtQuantity, _x_pos, _y_pos[4])
        _fixed.put(self.txtCost, _x_pos, _y_pos[5])
        _fixed.put(self.cmbCostType, _x_pos, _y_pos[6])

        _fixed.show_all()

        _vpaned.pack1(_frame, True, True)
        _fixed = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fixed)
        _frame = rtk.RTKFrame(label=_(u"Miscellaneous Information"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_gendata_labels[2],
                                              _fixed, 5, 5)
        _x_pos += 50

        # Move the Remarks label down to accomodate for the Attachments entry.
        _fixed.move(_fixed.get_children()[2], 5, _y_pos[1] + 100)

        _fixed.put(self.chkTagged, _x_pos, _y_pos[0])
        _fixed.put(self.txtAttachments.scrollwindow, _x_pos, _y_pos[1])
        _fixed.put(self.txtRemarks.scrollwindow, _x_pos, _y_pos[1] + 100)

        _fixed.show_all()

        _vpaned.pack2(_frame, True, True)

        _hbox.pack_end(_vpaned, expand=True, fill=True)

        # Create the label for the gtk.Notebook() tab.
        _label = rtk.RTKLabel(
            _(u"General\nData"),
            height=30,
            width=-1,
            justify=gtk.JUSTIFY_CENTER,
            tooltip=_(u"Displays general information for the selected "
                      u"hardware item."))
        self.hbx_tab_label.pack_start(_label)

        return _hbox

    def _make_buttonbox(self):
        """
        Make the gtk.ButtonBox() for the Hardware class Work View.

        :return: _buttonbox; the gtk.ButtonBox() for the Hardware class Work
                 View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Calculate the currently selected Hardware item."),
            _(u"Saves the currently selected Hardware item to the open "
              u"RTK Project database.")
        ]
        _callbacks = [self._do_request_calculate, self._do_request_update]

        _icons = ['calculate', 'save']
        _buttonbox = RTKWorkView._make_buttonbox(self, _icons, _tooltips,
                                                 _callbacks, 'vertical')

        return _buttonbox


class AssessmentResults(RTKWorkView):
    """
    Display Hardware attribute data in the RTK Work Book.

    The Hardware Assessment Results view displays all the assessment results
    for the selected Hardware.  The attributes of a Hardware Assessment Results
    View are:

    :ivar int _hardware_id: the ID of the Hardware currently being displayed.
    """

    def __init__(self, controller):
        """
        Initialize the Work View for the Hardware package.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKWorkView.__init__(self, controller, module='Hardware')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_assess_labels[1].append(_(u"Total Mode Count:"))

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self._hardware_id = None

        self.txtModeCount = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the total "
                      u"number of failure modes "
                      u"associated with the "
                      u"selected Hardware."))

        self.pack_start(
            self._make_assessment_results_page(), expand=True, fill=True)
        self.show_all()

        pub.subscribe(self._on_select, 'selectedHardware')
        pub.subscribe(self._on_select, 'calculatedHardware')

    def _make_assessment_results_page(self):
        """
        Make the Hardware class gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        (_hbx_page, __, _fxd_right, ___, _x_pos_r, __,
         _y_pos_r) = RTKWorkView._make_assessment_results_page(self)

        _fxd_right.put(self.txtModeCount, _x_pos_r, _y_pos_r[8] + 30)
        _fxd_right.show_all()

        self.txtActiveHt.set_sensitive(False)
        self.txtDormantHt.set_sensitive(False)
        self.txtSoftwareHt.set_sensitive(False)
        self.txtReliability.set_sensitive(False)
        self.txtMissionRt.set_sensitive(False)

        return _hbx_page

    def _on_select(self, module_id, **kwargs):
        """
        Load the Hardware Work View class gtk.Notebook() widgets.

        :param int hardware_id: the Hardware ID of the selected/edited
                                Hardware.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        self._dtc_data_controller = self._mdcRTK.dic_controllers['hardware']
        _hardware = self._dtc_data_controller.request_select(self._hardware_id)

        #self.txtAvailability.set_text(
        #    str(self.fmt.format(_hardware.availability_logistics)))
        #self.txtMissionAt.set_text(
        #    str(self.fmt.format(_hardware.availability_mission)))
        #self.txtMissionHt.set_text(
        #    str(self.fmt.format(_hardware.hazard_rate_mission)))
        #self.txtPredictedHt.set_text(
        #    str(self.fmt.format(_hardware.hazard_rate_logistics)))

        #self.txtMMT.set_text(str(self.fmt.format(_hardware.mmt)))
        #self.txtMCMT.set_text(str(self.fmt.format(_hardware.mcmt)))
        #self.txtMPMT.set_text(str(self.fmt.format(_hardware.mpmt)))

        #self.txtMissionMTBF.set_text(
        #    str(self.fmt.format(_hardware.mtbf_mission)))
        #self.txtMTBF.set_text(str(self.fmt.format(_hardware.mtbf_logistics)))
        #self.txtMTTR.set_text(str(self.fmt.format(_hardware.mttr)))

        #self.txtTotalCost.set_text(str(locale.currency(_hardware.cost)))
        #self.txtModeCount.set_text(
        #    str('{0:d}'.format(_hardware.total_mode_count)))
        #self.txtPartCount.set_text(
        #    str('{0:d}'.format(_hardware.total_part_count)))

        return _return
