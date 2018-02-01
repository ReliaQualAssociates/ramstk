# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.Hardware.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Hardware Work View."""

import locale  # pragma: no cover

from datetime import date  # pragma: no cover

from pubsub import pub  # pylint: disable=E0401

# Import other RTK modules.
from Utilities import boolean_to_integer  # pylint: disable=E0401
from gui.gtk import rtk  # pylint: disable=E0401
from gui.gtk.rtk.Widget import _, gtk  # pylint: disable=E0401,W0611
from .WorkView import RTKWorkView
from .components import wvwCapacitorAI, wvwCapacitorSI, wvwCapacitorAR, \
    wvwCapacitorSR, wvwConnectionAI, wvwConnectionSI, wvwConnectionAR, \
    wvwConnectionSR, wvwMiscellaneousAI, wvwMiscellaneousSI, \
    wvwMiscellaneousAR, wvwMiscellaneousSR, wvwInductorAI, wvwInductorSI, \
    wvwInductorAR, wvwInductorSR, wvwIntegratedCircuitAI, \
    wvwIntegratedCircuitSI, wvwIntegratedCircuitAR, wvwIntegratedCircuitSR, \
    wvwMeterAI, wvwMeterSI, wvwMeterAR, wvwMeterSR


class GeneralData(RTKWorkView):
    """
    Display Hardware attribute data in the RTK Work Book.

    The Work View displays all the general data attributes for the selected
    Hardware. The attributes of a Hardware General Data Work View are:

    :cvar list _lst_labels:

    :ivar int _hardware_id: the ID of the Hardware currently being displayed.

    :ivar chkRepairable: indicates whether or not the selected hardware item
                         is repairable.
    :ivar chkTagged: indicates whether or not the part is 'tagged'.  The tag
                     can indicate whatever the user chooses.
    :ivar cmbCategory: the component category of the hardware item.
    :ivar cmbCostType: the type cost estimate.
    :ivar cmbManufacturer: the manufacturer of the hardware item.
    :ivar cmbSubcategory: the component subcategory of the hardware item.

    :ivar txtAltPartNum: the alternate part number (if any) of the selected
                         hardware item.
    :ivar txtAttachments: hyperlinks to any documents associated with the
                          selected hardware item.
    :ivar txtCAGECode: the Commerical and Government Entity (CAGE) Code of the
                       selected hardware item.
    :ivar txtCompRefDes: the composite reference designator of the selected
                         hardware item.
    :ivar txtCost: the unit cost of the selected hardware item.
    :ivar txtDescription: the description of the selected hardware item.
    :ivar txtFigureNumber: the figure number in the governing specification for
                           the selected hardware item.
    :ivar txtLCN: the Logistics Control Number (LCN) of the selected hardware
                  item.
    :ivar txtName: the name of the selected hardware item.
    :ivar txtNSN: the National Stock Number (NSN) of the selected hardware
                  item.
    :ivar txtPageNumber: the page number in the governing specification for the
                         selected hardware item.
    :ivar txtPartNumber: the part number of the selected hardware item.
    :ivar txtQuantity: the number of the selected hardware items in the
                       design.
    :ivar txtRefDes: the reference designator of the selected hardware item.
    :ivar txtRemarks: any remarks associated with the selected hardware item.
    :ivar txtSpecification: the specification (if any) governing the selected
                            hardware item.
    :ivar txtYearMade: the year the the selected hardware item was
                       manufactured.

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

    # Define private list attributes.
    # We add an empty string in the positions where a gtk.CheckButton() will be
    # placed.
    _lst_labels = [[
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

    def __init__(self, controller):
        """
        Initialize the Work View for the Hardware package.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKWorkView.__init__(self, controller, module='Hardware')

        # Initialize private dictionary attributes.
        self._dic_icons[
            'comp_ref_des'] = controller.RTK_CONFIGURATION.RTK_ICON_DIR + \
            '/32x32/rollup.png'

        # Initialize private list attributes.

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

        self.txtAltPartNum = rtk.RTKEntry(
            tooltip=_(u"The alternate part "
                      u"number (if any) of the "
                      u"selected hardware item."))
        self.txtAttachments = rtk.RTKTextView(
            gtk.TextBuffer(),
            width=600,
            tooltip=_(u"Hyperlinks to any documents associated with the "
                      u"selected hardware item."))
        self.txtCAGECode = rtk.RTKEntry(
            tooltip=_(u"The Commerical and "
                      u"Government Entity (CAGE) "
                      u"Code of the selected "
                      u"hardware item."))
        self.txtCompRefDes = rtk.RTKEntry(
            tooltip=_(u"The composite reference "
                      u"designator of the "
                      u"selected hardware item."))
        self.txtCost = rtk.RTKEntry(
            width=100,
            tooltip=_(u"The unit cost of the selected hardware item."))
        self.txtDescription = rtk.RTKTextView(
            gtk.TextBuffer(),
            width=600,
            tooltip=_(u"The description of the selected hardware item."))
        self.txtFigureNumber = rtk.RTKEntry(
            tooltip=_(u"The figure number in "
                      u"the governing "
                      u"specification for the "
                      u"selected hardware "
                      u"item."))
        self.txtLCN = rtk.RTKEntry(
            tooltip=_(u"The Logistics Control Number "
                      u"(LCN) of the selected hardware "
                      u"item."))
        self.txtName = rtk.RTKEntry(
            width=600, tooltip=_(u"The name of the selected hardware item."))
        self.txtNSN = rtk.RTKEntry(
            tooltip=_(u"The National Stock Number (NSN) of the selected "
                      u"hardware item."))
        self.txtPageNumber = rtk.RTKEntry(
            tooltip=_(u"The page number in the "
                      u"governing specification "
                      u"for the selected "
                      u"hardware item."))
        self.txtPartNumber = rtk.RTKEntry(
            tooltip=_(u"The part number of the selected hardware item."))
        self.txtQuantity = rtk.RTKEntry(
            width=50,
            tooltip=_(
                u"The number of the selected hardware items in the design."))
        self.txtRefDes = rtk.RTKEntry(
            tooltip=_(
                u"The reference designator of the selected hardware item."))
        self.txtRemarks = rtk.RTKTextView(
            gtk.TextBuffer(),
            width=600,
            tooltip=_(u"Enter any remarks associated with the selected "
                      u"hardware item."))
        self.txtSpecification = rtk.RTKEntry(
            tooltip=_(u"The specification (if any) governing the selected "
                      u"hardware item."))
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
        self._lst_handler_id.append(
            self.txtDescription.do_get_buffer().connect(
                'changed', self._on_focus_out, 11))
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

        pub.subscribe(self._do_load_subcategory, 'changedCategory')
        pub.subscribe(self._on_select, 'selectedHardware')
        pub.subscribe(self._on_edit, 'mvwEditedHardware')

    def _do_load_subcategory(self, category_id):
        """
        Load the component subcategory RTKCombo().

        This method loads the component subcategory RTKCombo() when the
        component category RTKCombo() is changed.

        :param int category_id: the component category ID to load the
                                subcategory RTKCombo() for.
        :return: False if successful or True if an error is encountered
        :rtype: bool
        """
        _return = False

        _model = self.cmbSubcategory.get_model()
        _model.clear()

        if category_id > 0:
            _subcategory = self._mdcRTK.RTK_CONFIGURATION.RTK_SUBCATEGORIES[
                category_id]

            _data = []
            for _key in _subcategory:
                _data.append([_subcategory[_key]])

            self.cmbSubcategory.do_load_combo(_data)

        return _return

    def _do_request_make_comp_ref_des(self, __button):
        """
        Send request to create the composite reference designator.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        (
            _error_code, _msg
        ) = self._dtc_data_controller.request_make_composite_reference_designator(
            node_id=self._hardware_id)
        if _error_code == 0:
            _attributes = self._dtc_data_controller.request_get_attributes(
                self._hardware_id)

            self.txtCompRefDes.handler_block(self._lst_handler_id[9])
            self.txtCompRefDes.set_text(str(_attributes['comp_ref_des']))
            self.txtCompRefDes.handler_unblock(self._lst_handler_id[9])

        else:
            _return = True

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
            _(u"Creates the composite reference designator for the selected "
              u"hardware item."),
            _(u"Saves the currently selected Hardware to the open "
              u"RTK Project database."),
        ]
        _callbacks = [
            self._do_request_make_comp_ref_des, self._do_request_update
        ]
        _icons = ['comp_ref_des', 'save']

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

        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels[0], _fixed, 5,
                                              5)
        _x_pos += 50

        _hbox.pack_start(_frame, expand=True, fill=True)

        # Move the labels after the description to account for the extra
        # vertical space needed by the description RTKTextView().
        for _index in xrange(4, 13):  # pylint: disable=undefined-variable
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

        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels[1], _fixed, 5,
                                              5)
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

        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels[2], _fixed, 5,
                                              5)
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
        Retrieve RTKCombo() changes and assign to Hardware attribute.

        This method is called by:

            * gtk.Combo() 'changed' signal

        This method emits the 'changedSubcategory' message.

        :param combo: the RTKCombo() that called this method.
        :type combo: :class:`rtk.gui.gtk.rtk.RTKCombo`
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
            _attributes = self._dtc_data_controller.request_get_attributes(
                self._hardware_id)

            if index == 2:
                _attributes['category_id'] = int(combo.get_active())
                pub.sendMessage(
                    'changedCategory', category_id=_attributes['category_id'])
            elif index == 3:
                _attributes['cost_type_id'] = int(combo.get_active())
            elif index == 4:
                _attributes['manufacturer_id'] = int(combo.get_active())
                self.txtCAGECode.set_text(_model.get(_row, 2)[0])
            elif index == 5:
                _attributes['subcategory_id'] = int(combo.get_active())
                pub.sendMessage(
                    'changedSubcategory',
                    subcategory_id=_attributes['subcategory_id'])

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

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

            * RTKEntry() 'changed' signal
            * RTKTextView() 'changed' signal

        This method sends the 'wvwEditedHardware' message.

        :param entry: the RTKEntry() or RTKTextView() that called the method.
        :type entry: :class:`rtk.gui.gtk.rtk.RTKEntry` or
                     :class:`rtk.gui.gtk.rtk.RTKTextView`
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
            _attributes = self._dtc_data_controller.request_get_attributes(
                self._hardware_id)

            if index == 6:
                _position = 2
                _text = str(entry.get_text())
                _attributes['alt_part_num'] = _text
            elif index == 7:
                _position = None
                _text = self.txtAttachments.do_get_text()
                _attributes['attachments'] = _text
            elif index == 8:
                _position = 3
                _text = str(entry.get_text())
                _attributes['cage_code'] = _text
            elif index == 9:
                _position = 4
                _text = str(entry.get_text())
                _attributes['comp_ref_des'] = _text
            elif index == 10:
                _position = 5
                try:
                    _text = float(entry.get_text())
                except ValueError:
                    _text = 0.0
                _attributes['cost'] = _text
            elif index == 11:
                _position = 8
                _text = self.txtDescription.do_get_text()
                _attributes['description'] = _text
            elif index == 12:
                _position = 10
                _text = str(entry.get_text())
                _attributes['figure_number'] = _text
            elif index == 13:
                _position = 11
                _text = str(entry.get_text())
                _attributes['lcn'] = _text
            elif index == 14:
                _position = 15
                _text = str(entry.get_text())
                _attributes['name'] = _text
            elif index == 15:
                _position = 16
                _text = str(entry.get_text())
                _attributes['nsn'] = _text
            elif index == 16:
                _position = 17
                _text = str(entry.get_text())
                _attributes['page_number'] = _text
            elif index == 17:
                _position = 20
                _text = str(entry.get_text())
                _attributes['part_number'] = _text
            elif index == 18:
                _position = 21
                try:
                    _text = int(entry.get_text())
                except ValueError:
                    _text = 1
                _attributes['quantity'] = _text
            elif index == 19:
                _position = 22
                _text = str(entry.get_text())
                _attributes['ref_des'] = _text
            elif index == 20:
                _position = 23
                _text = self.txtRemarks.do_get_text()
                _attributes['remarks'] = _text
            elif index == 21:
                _position = 25
                _text = str(entry.get_text())
                _attributes['specification_number'] = _text
            elif index == 22:
                _position = 29
                try:
                    _text = int(entry.get_text())
                except ValueError:
                    _text = date.today()
                _attributes['year_of_manufacture'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

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

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        # Disable the category RTKCombo() if the hardware item is not a part.
        if _attributes['part'] == 1:
            self.cmbCategory.set_button_sensitivity(gtk.SENSITIVITY_ON)

            self.cmbCategory.set_active(_attributes['category_id'])

            self.cmbSubcategory.handler_block(self._lst_handler_id[5])
            self.cmbSubcategory.set_active(_attributes['subcategory_id'])
            self.cmbSubcategory.handler_unblock(self._lst_handler_id[5])

        else:
            self.cmbCategory.set_button_sensitivity(gtk.SENSITIVITY_OFF)

        self.chkRepairable.handler_block(self._lst_handler_id[0])
        self.chkRepairable.set_active(_attributes['repairable'])
        self.chkRepairable.handler_unblock(self._lst_handler_id[0])

        self.chkTagged.handler_block(self._lst_handler_id[1])
        self.chkTagged.set_active(_attributes['tagged_part'])
        self.chkTagged.handler_unblock(self._lst_handler_id[1])

        self.cmbCostType.handler_block(self._lst_handler_id[3])
        self.cmbCostType.set_active(_attributes['cost_type_id'])
        self.cmbCostType.handler_unblock(self._lst_handler_id[3])

        self.cmbManufacturer.handler_block(self._lst_handler_id[4])
        self.cmbManufacturer.set_active(_attributes['manufacturer_id'])
        self.cmbManufacturer.handler_unblock(self._lst_handler_id[4])

        self.txtAltPartNum.handler_block(self._lst_handler_id[6])
        self.txtAltPartNum.set_text(str(_attributes['alt_part_num']))
        self.txtAltPartNum.handler_unblock(self._lst_handler_id[6])

        _textbuffer = self.txtAttachments.do_get_buffer()
        _textbuffer.handler_block(self._lst_handler_id[7])
        _textbuffer.set_text(_attributes['attachments'])
        _textbuffer.handler_unblock(self._lst_handler_id[7])

        self.txtCAGECode.handler_block(self._lst_handler_id[8])
        self.txtCAGECode.set_text(str(_attributes['cage_code']))
        self.txtCAGECode.handler_unblock(self._lst_handler_id[8])

        self.txtCompRefDes.handler_block(self._lst_handler_id[9])
        self.txtCompRefDes.set_text(str(_attributes['comp_ref_des']))
        self.txtCompRefDes.handler_unblock(self._lst_handler_id[9])

        self.txtCost.handler_block(self._lst_handler_id[10])
        self.txtCost.set_text(str(locale.currency(_attributes['cost'])))
        self.txtCost.handler_unblock(self._lst_handler_id[10])

        _textbuffer = self.txtDescription.do_get_buffer()
        _textbuffer.handler_block(self._lst_handler_id[11])
        _textbuffer.set_text(str(_attributes['description']))
        _textbuffer.handler_unblock(self._lst_handler_id[11])

        self.txtFigureNumber.handler_block(self._lst_handler_id[12])
        self.txtFigureNumber.set_text(str(_attributes['figure_number']))
        self.txtFigureNumber.handler_unblock(self._lst_handler_id[12])

        self.txtLCN.handler_block(self._lst_handler_id[13])
        self.txtLCN.set_text(str(_attributes['lcn']))
        self.txtLCN.handler_unblock(self._lst_handler_id[13])

        self.txtName.handler_block(self._lst_handler_id[14])
        self.txtName.set_text(str(_attributes['name']))
        self.txtName.handler_unblock(self._lst_handler_id[14])

        self.txtNSN.handler_block(self._lst_handler_id[15])
        self.txtNSN.set_text(str(_attributes['nsn']))
        self.txtNSN.handler_unblock(self._lst_handler_id[15])

        self.txtPageNumber.handler_block(self._lst_handler_id[16])
        self.txtPageNumber.set_text(str(_attributes['page_number']))
        self.txtPageNumber.handler_unblock(self._lst_handler_id[16])

        self.txtPartNumber.handler_block(self._lst_handler_id[17])
        self.txtPartNumber.set_text(str(_attributes['part_number']))
        self.txtPartNumber.handler_unblock(self._lst_handler_id[17])

        self.txtQuantity.handler_block(self._lst_handler_id[18])
        self.txtQuantity.set_text(str(_attributes['quantity']))
        self.txtQuantity.handler_unblock(self._lst_handler_id[18])

        self.txtRefDes.handler_block(self._lst_handler_id[19])
        self.txtRefDes.set_text(str(_attributes['ref_des']))
        self.txtRefDes.handler_unblock(self._lst_handler_id[19])

        _textbuffer = self.txtRemarks.do_get_buffer()
        _textbuffer.handler_block(self._lst_handler_id[20])
        _textbuffer.set_text(_attributes['remarks'])
        _textbuffer.handler_unblock(self._lst_handler_id[20])

        self.txtSpecification.handler_block(self._lst_handler_id[21])
        self.txtSpecification.set_text(
            str(_attributes['specification_number']))
        self.txtSpecification.handler_unblock(self._lst_handler_id[21])

        self.txtYearMade.handler_block(self._lst_handler_id[22])
        self.txtYearMade.set_text(str(_attributes['year_of_manufacture']))
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
            _attributes = self._dtc_data_controller.request_get_attributes(
                self._hardware_id)

            if index == 0:
                _position = 24
                _text = boolean_to_integer(self.chkRepairable.get_active())
                _attributes['repairable'] = _text
            elif index == 1:
                _position = 26
                _text = boolean_to_integer(self.chkTagged.get_active())
                _attributes['tagged_part'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

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

    :cvar list _lst_assess_labels: the text to use for the assessment input
                                   widget labels.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.

    :ivar cmbActiveEnviron: the operating environment for the hardware item.
    :ivar cmbDormantEnviron: the storage environment for the hardware item.
    :ivar cmbFailureDist: the statistical failure distribution of the hardware
                          item.
    :ivar cmbHRType: the type of reliability assessment for the selected
                     hardware item.
    :ivar cmbHRMethod: the assessment method to use for the selected hardware
                       item.
    :ivar fraDesignRatings: the container to embed the piece part design
                            attributes gtk.Fised().
    :ivar fraOperatingStress: the container to embed the piece part operating
                              stresses gtk.Fixed().
    :ivar txtActiveTemp: the ambient temperature in the operating environment.
    :ivar txtAddAdjFactor: an adjustment factor to add to the assessed hazard
                           rate or MTBF.
    :ivar txtDormantTemp: the ambient temperature in the storage environment.
    :ivar txtFailScale: the scale parameter of the statistical failure
                        distribution.
    :ivar txtFailShape: the shape parameter of the statistical failure
                        distribution.
    :ivar txtFailLocation: the location parameter of the statistical failure
                           distribution.
    :ivar txtMultAdjFactor: an adjustment factor to multiply the assessed
                            hazard rate or MTBF by.
    :ivar txtSpecifiedHt: the stated hazard rate.
    :ivar txtSpecifiedHtVar: the variance of the stated hazard rate.
    :ivar txtSpecifiedMTBF: the stated mean time between failure (MTBF).
    :ivar txtSpecifiedMTBFVar: the variance of the stated mean time between
                               failure (MTBF).

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | cmbActiveEnviron - `changed`              |
    +----------+-------------------------------------------+
    |     1    | cmbDormantEnviron - `changed`             |
    +----------+-------------------------------------------+
    |     2    | cmbFailureDist - `changed`                |
    +----------+-------------------------------------------+
    |     3    | cmbHRType - `changed`                     |
    +----------+-------------------------------------------+
    |     4    | cmbHRMethod - `changed`                   |
    +----------+-------------------------------------------+
    |     5    | txtActiveTemp - `changed`                 |
    +----------+-------------------------------------------+
    |     6    | txtAddAdjFactor - `changed`               |
    +----------+-------------------------------------------+
    |     7    | txtDormantTemp - `changed`                |
    +----------+-------------------------------------------+
    |     8    | txtFailScale - `changed`                  |
    +----------+-------------------------------------------+
    |     9    | txtFailShape - `changed`                  |
    +----------+-------------------------------------------+
    |    10    | txtFailLocation - `changed`               |
    +----------+-------------------------------------------+
    |    11    | txtMultAdjFactor - `changed`              |
    +----------+-------------------------------------------+
    |    12    | txtSpecifiedHt - `changed`                |
    +----------+-------------------------------------------+
    |    13    | txtSpecifiedHtVar - `changed`             |
    +----------+-------------------------------------------+
    |    14    | txtSpecifiedMTBF - `changed`              |
    +----------+-------------------------------------------+
    |    15    | txtSpecifiedMTBFVar - `changed`           |
    +----------+-------------------------------------------+
    """

    # Define private list attributes.
    _lst_labels = [[
        _(u"Assessment Type:"),
        _(u"Assessment Method:"),
        _(u"Failure Distribution:"),
        _(u"Scale Parameter:"),
        _(u"Shape Parameter:"),
        _(u"Location Parameter:"),
        _(u"Stated Hazard Rate [h(t)]:"),
        _(u"Stated h(t) Variance:"),
        _(u"Stated MTBF:"),
        _(u"Stated MTBF Variance:"),
        _(u"Additive Adjustment Factor:"),
        _(u"Multiplicative Adjustment Factor:")
    ], [
        _(u"Active Environment:"),
        _(u"Dormant Environment:"),
        _(u"Active Temperature (\u00B0C):"),
        _(u"Dormant Temperature (\u00B0C):"),
        _(u"Mission Time:"),
        _(u"Duty Cycle:")
    ]]

    def __init__(self, controller):
        """
        Initialize an instance of the Hardware assessment input view.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKWorkView.__init__(self, controller, module='Hardware')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hardware_id = None
        self._wvwCapacitorAI = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbActiveEnviron = rtk.RTKComboBox(
            index=1,
            simple=False,
            tooltip=_(u"The operating environment for the hardware item."))
        self.cmbDormantEnviron = rtk.RTKComboBox(
            tooltip=_(u"The storage environment for the hardware item."))
        self.cmbFailureDist = rtk.RTKComboBox(
            tooltip=_(
                u"The statistical failure distribution of the hardware item."))
        self.cmbHRType = rtk.RTKComboBox(
            tooltip=_(
                u"The type of reliability assessment for the selected hardware "
                u"item."))
        self.cmbHRMethod = rtk.RTKComboBox(
            tooltip=_(
                u"The assessment method to use for the selected hardware item."
            ))

        self.scwDesignRatings = rtk.RTKScrolledWindow(None)
        self.scwOperatingStress = rtk.RTKScrolledWindow(None)

        self.txtActiveTemp = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The ambient temperature in the operating environment."))
        self.txtAddAdjFactor = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"An adjustment factor to add to the assessed hazard rate or "
                u"MTBF."))
        self.txtDormantTemp = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The ambient temperature in the storage environment."))
        self.txtDutyCycle = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The duty cycle of the selected hardware item."))
        self.txtFailScale = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The scale parameter of the statistical failure distribution."
            ))
        self.txtFailShape = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The shape parameter of the statistical failure distribution."
            ))
        self.txtFailLocation = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The location parameter of the statistical failure "
                      u"distribution."))
        self.txtMissionTime = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The mission time of the selected hardware item."))
        self.txtMultAdjFactor = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"An adjustment factor to multiply the assessed hazard rate "
                u"or MTBF by."))
        self.txtSpecifiedHt = rtk.RTKEntry(
            width=125, tooltip=_(u"The stated hazard rate."))
        self.txtSpecifiedHtVar = rtk.RTKEntry(
            width=125, tooltip=_(u"The variance of the stated hazard rate."))
        self.txtSpecifiedMTBF = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The stated mean time between failure (MTBF)."))
        self.txtSpecifiedMTBFVar = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The variance of the stated mean time between failure "
                      u"(MTBF)."))

        self._lst_handler_id.append(
            self.cmbActiveEnviron.connect('changed', self._on_combo_changed,
                                          0))
        self._lst_handler_id.append(
            self.cmbDormantEnviron.connect('changed', self._on_combo_changed,
                                           1))
        self._lst_handler_id.append(
            self.cmbFailureDist.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbHRType.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbHRMethod.connect('changed', self._on_combo_changed, 4))

        self._lst_handler_id.append(
            self.txtActiveTemp.connect('changed', self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtAddAdjFactor.connect('changed', self._on_focus_out, 6))
        self._lst_handler_id.append(
            self.txtDormantTemp.connect('changed', self._on_focus_out, 7))
        self._lst_handler_id.append(
            self.txtFailScale.connect('changed', self._on_focus_out, 8))
        self._lst_handler_id.append(
            self.txtFailShape.connect('changed', self._on_focus_out, 9))
        self._lst_handler_id.append(
            self.txtFailLocation.connect('changed', self._on_focus_out, 10))
        self._lst_handler_id.append(
            self.txtMultAdjFactor.connect('changed', self._on_focus_out, 11))
        self._lst_handler_id.append(
            self.txtSpecifiedHt.connect('changed', self._on_focus_out, 12))
        self._lst_handler_id.append(
            self.txtSpecifiedHtVar.connect('changed', self._on_focus_out, 13))
        self._lst_handler_id.append(
            self.txtSpecifiedMTBF.connect('changed', self._on_focus_out, 14))
        self._lst_handler_id.append(
            self.txtSpecifiedMTBFVar.connect('changed', self._on_focus_out,
                                             15))
        self._lst_handler_id.append(
            self.txtDutyCycle.connect('changed', self._on_focus_out, 16))
        self._lst_handler_id.append(
            self.txtMissionTime.connect('changed', self._on_focus_out, 17))

        self.pack_start(self._make_buttonbox(), expand=False, fill=False)
        self.pack_start(
            self._make_assessment_input_page(), expand=True, fill=True)
        self.show_all()

        pub.subscribe(self._on_select, 'selectedHardware')
        # pub.subscribe(self._on_edit, 'mvwEditedHardware')

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

        if self._dtc_data_controller.request_calculate(self._hardware_id):
            _error_code = 1
            _msg[0] = 'RTK ERROR: Calculating reliability attributes.'

        if _error_code != 0:
            _prompt = _(u"An error occurred when attempting to calculate "
                        u"Hardware {0:d}. \n\n\t" + _msg[0] + "\n\t" +
                        _msg[1] + "\n\n").format(self._hardware_id)
            _error_dialog = rtk.RTKMessageDialog(
                _prompt, self._dic_icons['error'], 'error')
            if _error_dialog.do_run() == gtk.RESPONSE_OK:
                _error_dialog.do_destroy()

            _return = True

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

    def _do_set_sensitive(self, type_id):
        """
        Set certain widgets sensitive or insensitive.

        This method will set the sensitivity of various widgets depending on
        the reliability assessment type selected.

        :param int type_id: the ID of the reliability assessment type selected.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        if type_id == 1:
            self.cmbFailureDist.set_sensitive(False)
            self.cmbHRMethod.set_sensitive(True)
            self.txtFailLocation.set_sensitive(False)
            self.txtFailScale.set_sensitive(False)
            self.txtFailShape.set_sensitive(False)
            self.txtSpecifiedHt.set_sensitive(False)
            self.txtSpecifiedHtVar.set_sensitive(False)
            self.txtSpecifiedMTBF.set_sensitive(False)
            self.txtSpecifiedMTBFVar.set_sensitive(False)
        elif type_id == 2:
            self.cmbFailureDist.set_sensitive(True)
            self.cmbHRMethod.set_sensitive(False)
            self.txtFailLocation.set_sensitive(True)
            self.txtFailScale.set_sensitive(True)
            self.txtFailShape.set_sensitive(True)
            self.txtSpecifiedHt.set_sensitive(False)
            self.txtSpecifiedHtVar.set_sensitive(False)
            self.txtSpecifiedMTBF.set_sensitive(False)
            self.txtSpecifiedMTBFVar.set_sensitive(False)
        elif type_id == 3:
            self.cmbFailureDist.set_sensitive(False)
            self.cmbHRMethod.set_sensitive(False)
            self.txtFailLocation.set_sensitive(False)
            self.txtFailScale.set_sensitive(False)
            self.txtFailShape.set_sensitive(False)
            self.txtSpecifiedHt.set_sensitive(True)
            self.txtSpecifiedHtVar.set_sensitive(True)
            self.txtSpecifiedMTBF.set_sensitive(False)
            self.txtSpecifiedMTBFVar.set_sensitive(False)
        elif type_id == 4:
            self.cmbFailureDist.set_sensitive(False)
            self.cmbHRMethod.set_sensitive(False)
            self.txtFailLocation.set_sensitive(False)
            self.txtFailScale.set_sensitive(False)
            self.txtFailShape.set_sensitive(False)
            self.txtSpecifiedHt.set_sensitive(False)
            self.txtSpecifiedHtVar.set_sensitive(False)
            self.txtSpecifiedMTBF.set_sensitive(True)
            self.txtSpecifiedMTBFVar.set_sensitive(True)

        return _return

    def _make_assessment_input_page(self):
        """
        Make the Hardware class gtk.Notebook() assessment input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Load the gtk.ComboBox() widgets.
        _model = self.cmbActiveEnviron.get_model()
        _model.clear()

        _data = []
        for _key in self._mdcRTK.RTK_CONFIGURATION.RTK_ACTIVE_ENVIRONMENTS:
            _data.append([
                self._mdcRTK.RTK_CONFIGURATION.RTK_ACTIVE_ENVIRONMENTS[_key][
                    0], self._mdcRTK.RTK_CONFIGURATION.RTK_ACTIVE_ENVIRONMENTS[
                        _key][1],
                self._mdcRTK.RTK_CONFIGURATION.RTK_ACTIVE_ENVIRONMENTS[_key][3]
            ])
        self.cmbActiveEnviron.do_load_combo(_data, index=1, simple=False)

        _model = self.cmbDormantEnviron.get_model()
        _model.clear()

        _data = []
        for _key in self._mdcRTK.RTK_CONFIGURATION.RTK_DORMANT_ENVIRONMENTS:
            _data.append([
                self._mdcRTK.RTK_CONFIGURATION.RTK_DORMANT_ENVIRONMENTS[_key][
                    1]
            ])
        self.cmbDormantEnviron.do_load_combo(_data)

        _model = self.cmbFailureDist.get_model()
        _model.clear()

        _data = [[_(u"1P Exponential")], [_(u"2P Exponential")],
                 [_(u"Gaussian")], [_(u"Lognormal")], [_(u"2P Weibull")],
                 [_(u"3P Weibull")]]
        self.cmbFailureDist.do_load_combo(_data)

        _model = self.cmbHRType.get_model()
        _model.clear()

        _data = []
        for _key in self._mdcRTK.RTK_CONFIGURATION.RTK_HR_TYPE:
            _data.append([self._mdcRTK.RTK_CONFIGURATION.RTK_HR_TYPE[_key][1]])
        self.cmbHRType.do_load_combo(_data)

        _model = self.cmbHRMethod.get_model()
        _model.clear()

        _data = []
        for _key in self._mdcRTK.RTK_CONFIGURATION.RTK_HR_MODEL:
            _data.append(
                [self._mdcRTK.RTK_CONFIGURATION.RTK_HR_MODEL[_key][0]])
        self.cmbHRMethod.do_load_combo(_data)

        # Build the assessment input page starting with the top left half.
        _hbox = gtk.HBox()
        _vpaned = gtk.VPaned()
        _fixed = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fixed)
        _frame = rtk.RTKFrame(label=_(u"Assessment Inputs"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels[0], _fixed, 5,
                                              5)
        _x_pos += 50

        _vpaned.pack1(_frame, True, True)
        _hbox.pack_start(_vpaned, expand=True, fill=True)

        _fixed.put(self.cmbHRType, _x_pos, _y_pos[0])
        _fixed.put(self.cmbHRMethod, _x_pos, _y_pos[1])
        _fixed.put(self.cmbFailureDist, _x_pos, _y_pos[2])
        _fixed.put(self.txtFailScale, _x_pos, _y_pos[3])
        _fixed.put(self.txtFailShape, _x_pos, _y_pos[4])
        _fixed.put(self.txtFailLocation, _x_pos, _y_pos[5])
        _fixed.put(self.txtSpecifiedHt, _x_pos, _y_pos[6])
        _fixed.put(self.txtSpecifiedHtVar, _x_pos, _y_pos[7])
        _fixed.put(self.txtSpecifiedMTBF, _x_pos, _y_pos[8])
        _fixed.put(self.txtSpecifiedMTBFVar, _x_pos, _y_pos[9])
        _fixed.put(self.txtAddAdjFactor, _x_pos, _y_pos[10])
        _fixed.put(self.txtMultAdjFactor, _x_pos, _y_pos[11])

        _fixed.show_all()

        # Now add the bottom left pane.  This is just an RTKFrame() and will be
        # the container for component-specific design attributes.
        _frame = rtk.RTKFrame(label=_(u"Design Ratings"))
        _frame.add(self.scwDesignRatings)
        _vpaned.pack2(_frame, True, True)

        # Now add the top right pane.
        _vpaned = gtk.VPaned()
        _fixed = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fixed)
        _frame = rtk.RTKFrame(label=_(u"Environmental Inputs"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels[1], _fixed, 5,
                                              5)
        _x_pos += 50

        _fixed.put(self.cmbActiveEnviron, _x_pos, _y_pos[0])
        _fixed.put(self.cmbDormantEnviron, _x_pos, _y_pos[1])
        _fixed.put(self.txtActiveTemp, _x_pos, _y_pos[2])
        _fixed.put(self.txtDormantTemp, _x_pos, _y_pos[3])
        _fixed.put(self.txtDutyCycle, _x_pos, _y_pos[4])
        _fixed.put(self.txtMissionTime, _x_pos, _y_pos[5])

        _fixed.show_all()

        _vpaned.pack1(_frame, True, True)

        # Finally, add the bottom right pane.  This is just an RTKFrame() and
        # will be the container for component-specific design attributes.
        _frame = rtk.RTKFrame(label=_(u"Operating Stresses"))
        _frame.add(self.scwOperatingStress)
        _vpaned.pack2(_frame, True, True)

        _hbox.pack_end(_vpaned, expand=True, fill=True)

        # Create the label for the gtk.Notebook() tab.
        _label = rtk.RTKLabel(
            _(u"Assessment\nInputs"),
            height=30,
            width=-1,
            justify=gtk.JUSTIFY_CENTER,
            tooltip=_(u"Displays reliability assessment inputs for the "
                      u"selected hardware item."))
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

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RTKCombo() changes and assign to Hardware attribute.

        This method is called by:

            * gtk.Combo() 'changed' signal

        :param combo: the RTKCombo() that called this method.
        :type combo: :class:`rtk.gui.gtk.rtk.RTKCombo`
        :param int index: the position in the Hardware class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Entry().  Indices are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    0    | cmbActiveEnviron |    3    | cmbHRType        |
            +---------+------------------+---------+------------------+
            |    1    | cmbDormantEnviron|    4    | cmbHRMethod      |
            +---------+------------------+---------+------------------+
            |    2    | cmbFailureDist   |         |                  |
            +---------+------------------+---------+------------------+

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        combo.handler_block(self._lst_handler_id[index])

        _model = combo.get_model()
        _row = combo.get_active_iter()

        if self._dtc_data_controller is not None:
            _attributes = self._dtc_data_controller.request_get_attributes(
                self._hardware_id)

            if index == 0:
                _attributes['environment_active_id'] = int(combo.get_active())
            elif index == 1:
                _attributes['environment_dormant_id'] = int(combo.get_active())
            elif index == 2:
                _attributes['failure_distribution_id'] = int(
                    combo.get_active())
            elif index == 3:
                _attributes['hazard_rate_type_id'] = int(combo.get_active())
                # Set certain widgets as sensitive and insensitive depending on
                # the type of assessment selected.
                self._do_set_sensitive(_attributes['hazard_rate_type_id'])
            elif index == 4:
                _attributes['hazard_rate_method_id'] = int(combo.get_active())

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        combo.handler_unblock(self._lst_handler_id[index])

        return _return

    def _on_focus_out(self, entry, index):
        """
        Retrieve changes made in RTKEntry() widgets..

        This method is called by:

            * RTKEntry() 'changed' signal
            * RTKTextView() 'changed' signal

        This method sends the 'wvwEditedHardware' message.

        :param entry: the RTKEntry() or RTKTextView() that called the method.
        :type entry: :class:`rtk.gui.gtk.rtk.RTKEntry` or
                     :class:`rtk.gui.gtk.rtk.RTKTextView`
        :param int index: the position in the Hardware class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Widget().  Indices are:

            +---------+---------------------+---------+---------------------+
            |  Index  | Widget              |  Index  | Widget              |
            +=========+=====================+=========+=====================+
            |    5    | txtActiveTemp       |   12    | txtSpecifiedHt      |
            +---------+---------------------+---------+---------------------+
            |    6    | txtAddAdjFactor     |   13    | txtSpecifiedHtVar   |
            +---------+---------------------+---------+---------------------+
            |    7    | txtDormantTemp      |   14    | txtSpecifiedMTBF    |
            +---------+---------------------+---------+---------------------+
            |    8    | txtFailScale        |   15    | txtSpecifiedMTBFVar |
            +---------+---------------------+---------+---------------------+
            |    9    | txtFailShape        |   16    | txtDutyCycle        |
            +---------+---------------------+---------+---------------------+
            |   10    | txtFailLocation     |   17    | txtMissionTime      |
            +---------+---------------------+---------+---------------------+
            |   11    | txtMultAdjFactor    |         |                     |
            +---------+---------------------+---------+---------------------+

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _index = -1
        _return = False
        _text = ''

        entry.handler_block(self._lst_handler_id[index])

        if self._dtc_data_controller is not None:
            _attributes = self._dtc_data_controller.request_get_attributes(
                self._hardware_id)

            try:
                _text = float(entry.get_text())
            except ValueError:
                _text = 0.0

            if index == 5:
                _attributes['temperature_active'] = _text
            elif index == 6:
                _position = 30
                _attributes['add_adj_factor'] = _text
            elif index == 7:
                _attributes['temperature_dormant'] = _text
            elif index == 8:
                _position = 60
                _attributes['scale_parameter'] = _text
            elif index == 9:
                _position = 61
                _attributes['shape_parameter'] = _text
            elif index == 10:
                _position = 47
                _attributes['location_parameter'] = _text
            elif index == 11:
                _position = 54
                _attributes['mult_adj_factor'] = _text
            elif index == 12:
                _position = 41
                _attributes['hazard_rate_specified'] = _text
            elif index == 13:
                _position = 46
                _attributes['hr_specified_variance'] = _text
            elif index == 14:
                _position = 50
                _attributes['mtbf_specified'] = _text
            elif index == 15:
                _position = 53
                _attributes['mtbf_spec_variance'] = _text
            elif index == 16:
                _position = 9
                _attributes['duty_cycle'] = _text
            elif index == 17:
                _position = 14
                _attributes['mission_time'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

            pub.sendMessage(
                'wvwEditedHardware', position=_position, new_text=_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def _on_select(self, module_id, **kwargs):
        """
        Load the hardware assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited Hardware
                              item.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False
        _component_ai = None
        _component_si = None

        self._hardware_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        self._dtc_data_controller = self._mdcRTK.dic_controllers['hardware']
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtDutyCycle.handler_block(self._lst_handler_id[16])
        self.txtDutyCycle.set_text(self.fmt.format(_attributes['duty_cycle']))
        self.txtDutyCycle.handler_unblock(self._lst_handler_id[16])

        self.txtMissionTime.handler_block(self._lst_handler_id[17])
        self.txtMissionTime.set_text(
            self.fmt.format(_attributes['mission_time']))
        self.txtMissionTime.handler_unblock(self._lst_handler_id[17])

        # Clear the component-specific gtk.ScrolledWindow()s.
        for _child in self.scwDesignRatings.get_children():
            self.scwDesignRatings.remove(_child)

        for _child in self.scwOperatingStress.get_children():
            self.scwOperatingStress.remove(_child)

        # Add the appropriate component-specific work view to the
        # gtk.ScrolledWindow()s.
        if _attributes['category_id'] == 1:
            _component_ai = wvwIntegratedCircuitAI(
                self._dtc_data_controller, self._hardware_id,
                _attributes['subcategory_id'])
            _component_si = wvwIntegratedCircuitSI(
                self._dtc_data_controller, self._hardware_id,
                _attributes['subcategory_id'])
        elif _attributes['category_id'] == 4:
            _component_ai = wvwCapacitorAI(self._dtc_data_controller,
                                           self._hardware_id,
                                           _attributes['subcategory_id'])
            _component_si = wvwCapacitorSI(self._dtc_data_controller,
                                           self._hardware_id,
                                           _attributes['subcategory_id'])
        elif _attributes['category_id'] == 5:
            _component_ai = wvwInductorAI(self._dtc_data_controller,
                                          self._hardware_id,
                                          _attributes['subcategory_id'])
            _component_si = wvwInductorSI(self._dtc_data_controller,
                                          self._hardware_id,
                                          _attributes['subcategory_id'])

        elif _attributes['category_id'] == 8:
            _component_ai = wvwConnectionAI(self._dtc_data_controller,
                                            self._hardware_id,
                                            _attributes['subcategory_id'])
            _component_si = wvwConnectionSI(self._dtc_data_controller,
                                            self._hardware_id,
                                            _attributes['subcategory_id'])
        elif _attributes['category_id'] == 9:
            _component_ai = wvwMeterAI(self._dtc_data_controller,
                                               self._hardware_id,
                                               _attributes['subcategory_id'])
            _component_si = wvwMeterSI(self._dtc_data_controller,
                                               self._hardware_id,
                                               _attributes['subcategory_id'])
        elif _attributes['category_id'] == 10:
            _component_ai = wvwMiscellaneousAI(self._dtc_data_controller,
                                               self._hardware_id,
                                               _attributes['subcategory_id'])
            _component_si = wvwMiscellaneousSI(self._dtc_data_controller,
                                               self._hardware_id,
                                               _attributes['subcategory_id'])

        # Load the component-specific widgets.
        if _component_ai is not None:
            _component_ai.fmt = self.fmt
            self.scwDesignRatings.add_with_viewport(_component_ai)
            _component_ai.on_select(module_id)

        if _component_si is not None:
            _component_si.fmt = self.fmt
            self.scwOperatingStress.add_with_viewport(_component_si)
            _component_si.on_select(module_id)

        self.scwDesignRatings.show_all()
        self.scwOperatingStress.show_all()

        self.cmbActiveEnviron.handler_block(self._lst_handler_id[0])
        self.cmbActiveEnviron.set_active(_attributes['environment_active_id'])
        self.cmbActiveEnviron.handler_unblock(self._lst_handler_id[0])

        self.cmbDormantEnviron.handler_block(self._lst_handler_id[1])
        self.cmbDormantEnviron.set_active(
            _attributes['environment_dormant_id'])
        self.cmbDormantEnviron.handler_unblock(self._lst_handler_id[1])

        self.txtActiveTemp.handler_block(self._lst_handler_id[5])
        self.txtActiveTemp.set_text(
            self.fmt.format(_attributes['temperature_active']))
        self.txtActiveTemp.handler_unblock(self._lst_handler_id[5])

        self.txtDormantTemp.handler_block(self._lst_handler_id[7])
        self.txtDormantTemp.set_text(
            self.fmt.format(_attributes['temperature_dormant']))
        self.txtDormantTemp.handler_unblock(self._lst_handler_id[7])

        self.cmbFailureDist.handler_block(self._lst_handler_id[2])
        self.cmbFailureDist.set_active(_attributes['failure_distribution_id'])
        self.cmbFailureDist.handler_unblock(self._lst_handler_id[2])

        self.cmbHRType.handler_block(self._lst_handler_id[3])
        self.cmbHRType.set_active(_attributes['hazard_rate_type_id'])
        self.cmbHRType.handler_unblock(self._lst_handler_id[3])

        self.cmbHRMethod.handler_block(self._lst_handler_id[4])
        self.cmbHRMethod.set_active(_attributes['hazard_rate_method_id'])
        self.cmbHRMethod.handler_unblock(self._lst_handler_id[4])

        self.txtAddAdjFactor.handler_block(self._lst_handler_id[6])
        self.txtAddAdjFactor.set_text(
            self.fmt.format(_attributes['add_adj_factor']))
        self.txtAddAdjFactor.handler_unblock(self._lst_handler_id[6])

        self.txtFailScale.handler_block(self._lst_handler_id[8])
        self.txtFailScale.set_text(
            self.fmt.format(_attributes['scale_parameter']))
        self.txtFailScale.handler_unblock(self._lst_handler_id[8])

        self.txtFailShape.handler_block(self._lst_handler_id[9])
        self.txtFailShape.set_text(
            self.fmt.format(_attributes['shape_parameter']))
        self.txtFailShape.handler_unblock(self._lst_handler_id[9])

        self.txtFailLocation.handler_block(self._lst_handler_id[10])
        self.txtFailLocation.set_text(
            self.fmt.format(_attributes['location_parameter']))
        self.txtFailLocation.handler_unblock(self._lst_handler_id[10])

        self.txtMultAdjFactor.handler_block(self._lst_handler_id[11])
        self.txtMultAdjFactor.set_text(
            self.fmt.format(_attributes['mult_adj_factor']))
        self.txtMultAdjFactor.handler_unblock(self._lst_handler_id[11])

        self.txtSpecifiedHt.handler_block(self._lst_handler_id[12])
        self.txtSpecifiedHt.set_text(
            self.fmt.format(_attributes['hazard_rate_specified']))
        self.txtSpecifiedHt.handler_unblock(self._lst_handler_id[12])

        self.txtSpecifiedHtVar.handler_block(self._lst_handler_id[13])
        self.txtSpecifiedHtVar.set_text(
            self.fmt.format(_attributes['hr_specified_variance']))
        self.txtSpecifiedHtVar.handler_unblock(self._lst_handler_id[13])

        self.txtSpecifiedMTBF.handler_block(self._lst_handler_id[14])
        self.txtSpecifiedMTBF.set_text(
            self.fmt.format(_attributes['mtbf_specified']))
        self.txtSpecifiedMTBF.handler_unblock(self._lst_handler_id[14])

        self.txtSpecifiedMTBFVar.handler_block(self._lst_handler_id[15])
        self.txtSpecifiedMTBFVar.set_text(
            self.fmt.format(_attributes['mtbf_spec_variance']))
        self.txtSpecifiedMTBFVar.handler_unblock(self._lst_handler_id[15])

        self._do_set_sensitive(_attributes['hazard_rate_type_id'])

        # Set the calculate button sensitive only if the selected hardware
        # item is a part.
        if _attributes['part'] == 1:
            self.get_children()[0].get_children()[0].set_sensitive(True)
        else:
            self.get_children()[0].get_children()[0].set_sensitive(False)

        return _return


class AssessmentResults(RTKWorkView):
    """
    Display Hardware assessment results attribute data in the RTK Work Book.

    The Hardware Assessment Results view displays all the assessment results
    for the selected Hardware.  The attributes of a Hardware Assessment Results
    View are:

    :cvar list _lst_labels: the text to use for the reliability assessment
                            results widget labels.

    :ivar int _hardware_id: the ID of the Hardware currently being displayed.

    :ivar txtActiveHt: displays the active failure intensity for the selected
                       hardware item.
    :ivar txtActiveHtVar: displays the active failure intensity variance.
    :ivar txtDormantHt: displays the dormant failure intensity for the selected
                        hardware item.
    :ivar txtDormantHtVar: displays the dormant failure intensity variance.
    :ivar txtSoftwareHt: displays the software failure intensity for the
                         selected hardware item."))
    :ivar txtLogisticsHt: displays the logistics failure intensity for the
                          selected hardware item.  This is the sum of the
                          active, dormant, and software hazard rates.
    :ivar txtLogisticsHtVar: displays the logistics failure intensity variance.
    :ivar txtMissionHt: displays the mission failure intensity for the selected
                        hardware item.
    :ivar txtMissionHtVar: displays the mission failure intensity variance.
    :ivar txtLogisticsMTBF: displays the logistics mean time between failure
                            (MTBF) for the selected hardware item.
    :ivar txtLogisticsMTBFVar: displays the logistics MTBF variance.
    :ivar txtMissionMTBF: displays the mission mean time between failure (MTBF)
                          for the selected hardware item.
    :ivar txtMissionMTBFVar: displays the mission MTBF variance.
    :ivar txtLogisticsRt: displays the logistics reliability for the selected
                          hardware item.
    :ivar txtLogisticsRtVar: displays the logistics reliability variance.
    :ivar txtMissionRt: displays the mission reliability for the selected
                        hardware item.
    :ivar txtMissionRtVar: displays the mission reliability variance.
    :ivar txtMPMT: displays the mean preventive maintenance time (MPMT) for the
                   selected hardware item.
    :ivar txtMCMT: displays the mean corrective maintenance time (MCMT) for the
                   selected hardware item.
    :ivar txtMTTR: displays the mean time to repair (MTTR) for the selected
                   hardware item.
    :ivar txtMMT: displays the mean maintenance time (MMT) for the selected
                  hardware item.  This includes preventive and corrective
                  maintenance.
    :ivar txtLogisticsAt: displays the logistics availability for the selected
                          hardware item.
    :ivar txtLogisticsAtVar: displays the logistics availability variance.
    :ivar txtMissionAt: displays the mission availability for the selected
                        hardware item.
    :ivar txtMissionAtVar: displays the mission availability variance.
    :ivar txtPartCount: displays the total part count for the selected hardware
                        item.
    :ivar txtPercentHt: the percentage of the system failure intensity the
                        selected hardware item represents.
    :ivar txtTotalCost: displays the total cost of the selected hardware item.
    :ivar txtCostFailure: displays the cost per failure of the selected
                          hardware item.
    :ivar txtCostHour: displays the failure cost per mission hour for the
                       selected hardware item.
    """

    # Define private list attributes.
    _lst_labels = [[
        _(u"Active Failure Intensity [\u03BB(t)]:"),
        _(u"Dormant \u03BB(t):"),
        _(u"Software \u03BB(t):"),
        _(u"Logistics \u03BB(t):"),
        _(u"Mission \u03BB(t):"),
        _(u"Percent \u03BB(t):"),
        _(u"Logistics MTBF:"),
        _(u"Mission MTBF:"),
        _(u"Logistics Reliability [R(t)]:"),
        _(u"Mission R(t):")
    ], [
        _(u"Logistics Availability [A(t)]:"),
        _(u"Mission A(t):"),
        _(u"Total Cost:"),
        _(u"Cost/Failure:"),
        _(u"Cost/Hour:"),
        _(u"Total # of Parts:")
    ]]

    def __init__(self, controller):
        """
        Initialize the Work View for the Hardware package.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKWorkView.__init__(self, controller, module='Hardware')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hardware_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.scwReliability = rtk.RTKScrolledWindow(None)
        self.scwStress = rtk.RTKScrolledWindow(None)

        self.txtActiveHt = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the active failure intensity for the "
                      u"selected hardware item."))
        self.txtActiveHtVar = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the variance on the active failure intensity "
                      u"for the selected hardware item."))
        self.txtCostFailure = rtk.RTKEntry(
            width=125,
            editable=False,
            tooltip=_(u"Displays the cost per failure of the selected "
                      u"hardware item."))
        self.txtCostHour = rtk.RTKEntry(
            width=125,
            editable=False,
            tooltip=_(u"Displays the failure cost per operating hour for the "
                      u"selected hardware item."))
        self.txtDormantHt = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the dormant failure intensity for the "
                      u"selected hardware item."))
        self.txtDormantHtVar = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(
                u"Displays the variance on the dormant failure intensity "
                u"for the selected hardware item."))
        self.txtLogisticsAt = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the logistics availability for the selected "
                      u"hardware item."))
        self.txtLogisticsAtVar = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the variance on the logistics availability "
                      u"for the selected hardware item."))
        self.txtLogisticsHt = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the logistics failure intensity for the "
                      u"selected hardware item.  This is the sum of the "
                      u"active, dormant, and software hazard rates."))
        self.txtLogisticsHtVar = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the variance on the logistics failure "
                      u"intensity for the selected hardware item."))
        self.txtLogisticsMTBF = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the logistics mean time between failure "
                      u"(MTBF) for the selected hardware item."))
        self.txtLogisticsMTBFVar = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the variance on the logistics MTBF for the "
                      u"selected hardware item."))
        self.txtLogisticsRt = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the logistics reliability for the selected "
                      u"hardware item."))
        self.txtLogisticsRtVar = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the variance on the logistics reliability "
                      u"for the selected hardware item."))
        self.txtMCMT = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mean corrective maintenance time (MCMT) "
                      u"for the selected hardware item."))
        self.txtMissionAt = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mission availability for the selected "
                      u"hardware item."))
        self.txtMissionAtVar = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the variance on the mission availability for "
                      u"the selected hardware item."))
        self.txtMissionHt = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mission failure intensity for the "
                      u"selected hardware item."))
        self.txtMissionHtVar = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the variance on the mission failure "
                      u"intensity for the selected hardware item."))
        self.txtMissionMTBF = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mission mean time between failure (MTBF) "
                      u"for the selected hardware item."))
        self.txtMissionMTBFVar = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the variance on the mission MTBF for the "
                      u"selected hardware item."))
        self.txtMissionRt = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mission reliability for the selected "
                      u"hardware item."))
        self.txtMissionRtVar = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the variance on the mission reliability for "
                      u"the selected hardware item."))
        self.txtMMT = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mean maintenance time (MMT) for the "
                      u"selected hardware item.  This includes preventive and "
                      u"corrective maintenance."))
        self.txtMPMT = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mean preventive maintenance time (MPMT) "
                      u"for the selected hardware item."))
        self.txtMTTR = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mean time to repair (MTTR) for the "
                      u"selected hardware item."))
        self.txtPartCount = rtk.RTKEntry(
            width=125,
            editable=False,
            tooltip=_(u"Displays the total part count for the selected "
                      u"hardware item."))
        self.txtPercentHt = rtk.RTKEntry(
            width=125,
            editable=False,
            tooltip=_(u"Displays the percentage of the system failure "
                      u"intensity the selected hardware item represents."))
        self.txtSoftwareHt = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the software failure intensity for the "
                      u"selected hardware item."))
        self.txtTotalCost = rtk.RTKEntry(
            width=125,
            editable=False,
            tooltip=_(u"Displays the total cost of the selected hardware "
                      u"item."))

        self.pack_start(self._make_buttonbox(), expand=False, fill=False)
        self.pack_start(
            self._make_assessment_results_page(), expand=True, fill=True)
        self.show_all()

        pub.subscribe(self._on_select, 'selectedHardware')
        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_page(self, module_id=None):
        """
        Load the assessment result page widgets with attribute values.

        :param int module_id: the ID of the hardware item to load.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtTotalCost.set_text(
            str(locale.currency(_attributes['total_cost'])))
        self.txtCostFailure.set_text(
            str(locale.currency(_attributes['cost_failure'])))
        self.txtCostHour.set_text(
            str(locale.currency(_attributes['cost_hour'])))
        self.txtPartCount.set_text(
            str('{0:d}'.format(_attributes['total_part_count'])))

        self.txtActiveHt.set_text(
            str(self.fmt.format(_attributes['hazard_rate_active'])))
        self.txtActiveHtVar.set_text(
            str(self.fmt.format(_attributes['hr_active_variance'])))

        self.txtDormantHt.set_text(
            str(self.fmt.format(_attributes['hazard_rate_dormant'])))
        self.txtDormantHtVar.set_text(
            str(self.fmt.format(_attributes['hr_dormant_variance'])))

        self.txtSoftwareHt.set_text(
            str(self.fmt.format(_attributes['hazard_rate_software'])))

        self.txtPercentHt.set_text(
            str(self.fmt.format(_attributes['hazard_rate_percent'])))

        self.txtLogisticsAt.set_text(
            str(self.fmt.format(_attributes['availability_logistics'])))
        self.txtLogisticsAtVar.set_text(
            str(self.fmt.format(_attributes['avail_log_variance'])))
        self.txtLogisticsHt.set_text(
            str(self.fmt.format(_attributes['hazard_rate_logistics'])))
        self.txtLogisticsHtVar.set_text(
            str(self.fmt.format(_attributes['hr_logistics_variance'])))
        self.txtLogisticsMTBF.set_text(
            str(self.fmt.format(_attributes['mtbf_logistics'])))
        self.txtLogisticsMTBFVar.set_text(
            str(self.fmt.format(_attributes['mtbf_log_variance'])))
        self.txtLogisticsRt.set_text(
            str(self.fmt.format(_attributes['reliability_logistics'])))
        self.txtLogisticsRtVar.set_text(
            str(self.fmt.format(_attributes['reliability_log_variance'])))

        self.txtMissionAt.set_text(
            str(self.fmt.format(_attributes['availability_mission'])))
        self.txtMissionAtVar.set_text(
            str(self.fmt.format(_attributes['avail_mis_variance'])))
        self.txtMissionHt.set_text(
            str(self.fmt.format(_attributes['hazard_rate_mission'])))
        self.txtMissionHtVar.set_text(
            str(self.fmt.format(_attributes['hr_mission_variance'])))
        self.txtMissionMTBF.set_text(
            str(self.fmt.format(_attributes['mtbf_mission'])))
        self.txtMissionMTBFVar.set_text(
            str(self.fmt.format(_attributes['mtbf_miss_variance'])))
        self.txtMissionRt.set_text(
            str(self.fmt.format(_attributes['reliability_mission'])))
        self.txtMissionRtVar.set_text(
            str(self.fmt.format(_attributes['reliability_miss_variance'])))

        return _return

    def _do_request_calculate(self, __button):
        """
        Send request to calculate the selected Hardware item.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _error_code = 0
        _msg = ['', '']

        if self._dtc_data_controller.request_calculate(self._hardware_id):
            _error_code = 1
            _msg[0] = 'RTK ERROR: Calculating reliability attributes.'

        if _error_code != 0:
            _prompt = _(u"An error occurred when attempting to calculate "
                        u"Hardware {0:d}. \n\n\t" + _msg[0] + "\n\t" +
                        _msg[1] + "\n\n").format(self._hardware_id)
            _error_dialog = rtk.RTKMessageDialog(
                _prompt, self._dic_icons['error'], 'error')
            if _error_dialog.do_run() == gtk.RESPONSE_OK:
                _error_dialog.do_destroy()

            _return = True

        return _return

    def _do_request_update(self, __button):
        """
        Send request to save the currently selected Hardware item.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_update(self._hardware_id)

    def _make_assessment_results_page(self):
        """
        Make the Hardware class gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _hbox = gtk.HBox()

        # Build the assessment results page starting with the top left half.
        _vpaned = gtk.VPaned()

        _frame = rtk.RTKFrame(label=_(u"Reliability Results"))
        _vpaned.pack1(_frame, True, True)

        _fixed = gtk.Fixed()
        _scrollwindow = rtk.RTKScrolledWindow(_fixed)
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels[0], _fixed, 5,
                                              5)
        _x_pos += 50

        _fixed.put(self.txtActiveHt, _x_pos, _y_pos[0])
        _fixed.put(self.txtActiveHtVar, _x_pos + 135, _y_pos[0])
        _fixed.put(self.txtDormantHt, _x_pos, _y_pos[1])
        _fixed.put(self.txtDormantHtVar, _x_pos + 135, _y_pos[1])
        _fixed.put(self.txtSoftwareHt, _x_pos, _y_pos[2])
        _fixed.put(self.txtLogisticsHt, _x_pos, _y_pos[3])
        _fixed.put(self.txtLogisticsHtVar, _x_pos + 135, _y_pos[3])
        _fixed.put(self.txtMissionHt, _x_pos, _y_pos[4])
        _fixed.put(self.txtMissionHtVar, _x_pos + 135, _y_pos[4])
        _fixed.put(self.txtPercentHt, _x_pos, _y_pos[5])
        _fixed.put(self.txtLogisticsMTBF, _x_pos, _y_pos[6])
        _fixed.put(self.txtLogisticsMTBFVar, _x_pos + 135, _y_pos[6])
        _fixed.put(self.txtMissionMTBF, _x_pos, _y_pos[7])
        _fixed.put(self.txtMissionMTBFVar, _x_pos + 135, _y_pos[7])
        _fixed.put(self.txtLogisticsRt, _x_pos, _y_pos[8])
        _fixed.put(self.txtLogisticsRtVar, _x_pos + 135, _y_pos[8])
        _fixed.put(self.txtMissionRt, _x_pos, _y_pos[9])
        _fixed.put(self.txtMissionRtVar, _x_pos + 135, _y_pos[9])

        _fixed.show_all()

        # Now add the bottom left pane.  This is just an RTKScrolledwindow()
        # and will be the container for component-specific reliability results.
        _frame = rtk.RTKFrame(label=_(u"Assessment Model Results"))
        _frame.add(self.scwReliability)

        _vpaned.pack2(_frame, True, True)

        _hbox.pack_start(_vpaned, expand=True, fill=True)

        # Now add the top right pane.
        _vpaned = gtk.VPaned()
        _fixed = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fixed)
        _frame = rtk.RTKFrame(label=_(u"Availability Results"))
        _frame.add(_scrollwindow)

        _vpaned.pack1(_frame, True, True)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels[1], _fixed, 5,
                                              5)
        _x_pos += 50

        _fixed.put(self.txtLogisticsAt, _x_pos, _y_pos[0])
        _fixed.put(self.txtLogisticsAtVar, _x_pos + 135, _y_pos[0])
        _fixed.put(self.txtMissionAt, _x_pos, _y_pos[1])
        _fixed.put(self.txtMissionAtVar, _x_pos + 135, _y_pos[1])
        _fixed.put(self.txtTotalCost, _x_pos, _y_pos[2])
        _fixed.put(self.txtCostFailure, _x_pos, _y_pos[3])
        _fixed.put(self.txtCostHour, _x_pos, _y_pos[4])
        _fixed.put(self.txtPartCount, _x_pos, _y_pos[5])

        # Finally, add the bottom right pane.  This is just an RTKFrame() and
        # will be the container for component-specific design attributes.
        _frame = rtk.RTKFrame(label=_(u"Stress Results"))
        _frame.add(self.scwStress)
        _vpaned.pack2(_frame, True, True)

        _hbox.pack_end(_vpaned, expand=True, fill=True)

        _label = rtk.RTKLabel(
            _(u"Assessment\nResults"),
            height=30,
            width=-1,
            justify=gtk.JUSTIFY_CENTER,
            tooltip=_(u"Displays reliability, "
                      u"maintainability, and availability "
                      u"assessment results for the selected "
                      u"{0:s}.").format(self._module))
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

    def _on_select(self, module_id, **kwargs):
        """
        Load the Hardware Work View class gtk.Notebook() widgets.

        :param int hardware_id: the Hardware ID of the selected/edited
                                Hardware.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False
        _component_ar = None
        _component_sr = None

        self._hardware_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        self._dtc_data_controller = self._mdcRTK.dic_controllers['hardware']
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self._do_load_page()

        # Clear the component-specific gtk.ScrolledWindow()s.
        for _child in self.scwReliability.get_children():
            self.scwReliability.remove(_child)

        for _child in self.scwStress.get_children():
            self.scwStress.remove(_child)

        # Add the appropriate component-specific work view to the
        # gtk.ScrolledWindow()s.
        if _attributes['category_id'] == 1:
            _component_ar = wvwIntegratedCircuitAR(
                self._dtc_data_controller, self._hardware_id,
                _attributes['subcategory_id'])
            _component_sr = wvwIntegratedCircuitSR(
                self._dtc_data_controller, self._hardware_id,
                _attributes['subcategory_id'])
        elif _attributes['category_id'] == 4:
            _component_ar = wvwCapacitorAR(self._dtc_data_controller,
                                           self._hardware_id,
                                           _attributes['subcategory_id'])
            _component_sr = wvwCapacitorSR(self._dtc_data_controller,
                                           self._hardware_id,
                                           _attributes['subcategory_id'])
        elif _attributes['category_id'] == 5:
            _component_ar = wvwInductorAR(self._dtc_data_controller,
                                          self._hardware_id,
                                          _attributes['subcategory_id'])
            _component_sr = wvwInductorSR(self._dtc_data_controller,
                                          self._hardware_id,
                                          _attributes['subcategory_id'])
        elif _attributes['category_id'] == 8:
            _component_ar = wvwConnectionAR(self._dtc_data_controller,
                                            self._hardware_id,
                                            _attributes['subcategory_id'])
            _component_sr = wvwConnectionSR(self._dtc_data_controller,
                                            self._hardware_id,
                                            _attributes['subcategory_id'])
        elif _attributes['category_id'] == 9:
            _component_ar = wvwMeterAR(self._dtc_data_controller,
                                       self._hardware_id,
                                       _attributes['subcategory_id'])
            _component_sr = wvwMeterSR(self._dtc_data_controller,
                                       self._hardware_id,
                                       _attributes['subcategory_id'])
        elif _attributes['category_id'] == 10:
            _component_ar = wvwMiscellaneousAR(self._dtc_data_controller,
                                               self._hardware_id,
                                               _attributes['subcategory_id'])
            _component_sr = wvwMiscellaneousSR(self._dtc_data_controller,
                                               self._hardware_id,
                                               _attributes['subcategory_id'])

        # Load the component-specific widgets.
        if _component_ar is not None:
            _component_ar.fmt = self.fmt
            self.scwReliability.add_with_viewport(_component_ar)
            _component_ar.on_select(module_id)

        if _component_sr is not None:
            _component_sr.fmt = self.fmt
            self.scwStress.add_with_viewport(_component_sr)
            _component_sr.on_select(module_id)

        # Set the calculate button sensitive only if the selected hardware
        # item is a part.
        if _attributes['part'] == 1:
            self.get_children()[0].get_children()[0].set_sensitive(True)
        else:
            self.get_children()[0].get_children()[0].set_sensitive(False)

        return _return
