# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.workview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Hardware Work View."""

# Standard Library Imports
import locale
from typing import Any, Callable, Dict, List

# Third Party Imports
from pubsub import pub
from sortedcontainers import SortedDict

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton, RAMSTKComboBox, RAMSTKEntry, RAMSTKFrame,
    RAMSTKLabel, RAMSTKScrolledWindow, RAMSTKTextView, RAMSTKWorkView
)


class GeneralData(RAMSTKWorkView):
    """
    Display general Hardware attribute data in the RAMSTK Work Book.

    The Hardware Work View displays all the general data attributes for the
    selected Hardware.

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
    # Define private dict attributes.
    _dic_keys = {
        0: 'repairable',
        1: 'tagged_part',
        2: 'category_id',
        3: 'cost_type_id',
        4: 'manufacturer_id',
        5: 'subcategory_id',
        6: 'alt_part_number',
        7: 'attachments',
        8: 'cage_code',
        9: 'comp_ref_des',
        10: 'cost',
        11: 'description',
        12: 'figure_number',
        13: 'lcn',
        14: 'name',
        15: 'nsn',
        16: 'page_number',
        17: 'part_number',
        18: 'quantity',
        19: 'ref_des',
        20: 'remarks',
        21: 'specification_number',
        22: 'year_of_manufacture'
    }

    # Define private list attributes.
    _lst_labels = [
        _("Reference Designator:"),
        _("Composite Ref. Des."),
        _("Name:"),
        _("Description:"),
        _("Part Number:"),
        _("Alternate Part Number:"),
        _("Category:"),
        _("Subcategory:"),
        _("Specification:"),
        _("Page Number:"),
        _("Figure Number:"),
        _("LCN:"), "",
        _("Manufacturer:"),
        _("CAGE Code:"),
        _("NSN:"),
        _("Year Made:"),
        _("Quantity:"),
        _("Unit Cost:"),
        _("Cost Method:"),
        _("Attachments:"),
        _("Remarks:"), ""
    ]

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'hardware') -> None:
        """
        Initialize the Hardware Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger, module)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.
        self._dic_icons['comp_ref_des'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/rollup.png')

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.chkRepairable: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Repairable"))
        self.chkTagged: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Tagged Part"))

        self.cmbCategory: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbCostType: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbManufacturer: RAMSTKComboBox = RAMSTKComboBox(simple=False)
        self.cmbSubcategory: RAMSTKComboBox = RAMSTKComboBox()

        self.txtAltPartNum: RAMSTKEntry = RAMSTKEntry()
        self.txtAttachments: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())
        self.txtCAGECode: RAMSTKEntry = RAMSTKEntry()
        self.txtCompRefDes: RAMSTKEntry = RAMSTKEntry()
        self.txtCost: RAMSTKEntry = RAMSTKEntry()
        self.txtDescription: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())
        self.txtFigureNumber: RAMSTKEntry = RAMSTKEntry()
        self.txtLCN: RAMSTKEntry = RAMSTKEntry()
        self.txtName: RAMSTKEntry = RAMSTKEntry()
        self.txtNSN: RAMSTKEntry = RAMSTKEntry()
        self.txtPageNumber: RAMSTKEntry = RAMSTKEntry()
        self.txtPartNumber: RAMSTKEntry = RAMSTKEntry()
        self.txtQuantity: RAMSTKEntry = RAMSTKEntry()
        self.txtRefDes: RAMSTKEntry = RAMSTKEntry()
        self.txtRemarks: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())
        self.txtSpecification: RAMSTKEntry = RAMSTKEntry()
        self.txtYearMade: RAMSTKEntry = RAMSTKEntry()

        self._dic_switch: Dict[str, List[Callable, int]] = {
            'description': [self.txtDescription.do_update, 5],
            'name': [self.txtName.do_update, 15],
            'remarks': [self.txtRemarks.do_update, 17]
        }
        self._lst_widgets = [
            self.txtRefDes, self.txtCompRefDes, self.txtName,
            self.txtDescription, self.txtPartNumber, self.txtAltPartNum,
            self.cmbCategory, self.cmbSubcategory, self.txtSpecification,
            self.txtPageNumber, self.txtFigureNumber, self.txtLCN,
            self.chkRepairable, self.cmbManufacturer, self.txtCAGECode,
            self.txtNSN, self.txtYearMade, self.txtQuantity, self.txtCost,
            self.cmbCostType, self.txtAttachments, self.txtRemarks,
            self.chkTagged
        ]

        self.__set_properties()
        self.__load_combobox()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'request_clear_workviews')
        pub.subscribe(self._do_load_page, 'selected_hardware')
        pub.subscribe(self._on_edit, 'mvw_editing_hardware')
        pub.subscribe(self._do_load_subcategory, 'changed_category')

    def __load_combobox(self) -> None:
        """
        Load the RAMSTK ComboBox widgets with lists of information.

        :return: None
        :rtype: None
        """
        self.cmbCostType.do_load_combo([['Assessed'], ['Specified']])

        _data = []
        for _key in self.RAMSTK_USER_CONFIGURATION.RAMSTK_CATEGORIES:
            _data.append(
                [self.RAMSTK_USER_CONFIGURATION.RAMSTK_CATEGORIES[_key]])
        self.cmbCategory.do_load_combo(_data)

        _data = []
        for _key in self.RAMSTK_USER_CONFIGURATION.RAMSTK_MANUFACTURERS:
            _data.append(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_MANUFACTURERS[_key])
        self.cmbManufacturer.do_load_combo(_data, simple=False)

    def __make_ui(self) -> None:
        """
        Create the Hardware WorkView general data page.

        :return: None
        :rtype: None
        """
        # This page has the following layout:
        # +-----+-------------------+-------------------+
        # |  B  |      L. SIDE      |      R. TOP       |
        # |  U  |                   |                   |
        # |  T  |                   |                   |
        # |  T  |                   +-------------------+
        # |  O  |                   |     R. BOTTOM     |
        # |  N  |                   |                   |
        # |  S  |                   |                   |
        # +-----+-------------------+-------------------+
        super().make_toolbuttons(
            icons=['comp_ref_des'],
            tooltips=[
                _("Creates the composite reference designator for the "
                  "selected hardware item.")
            ],
            callbacks=[self._do_request_make_comp_ref_des])
        (__, __, _fixed) = super().make_ui(start=0, end=13)

        _hpaned = Gtk.HPaned()
        self.pack_start(_hpaned, True, True, 0)

        _scrollwindow = RAMSTKScrolledWindow(_fixed)
        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("General Information"))
        _frame.add(_scrollwindow)

        _hpaned.pack1(_frame, True, True)

        _vpaned = Gtk.VPaned()
        _hpaned.pack2(_vpaned, True, True)
        (__, __, _fixed) = super().make_ui(start=13, end=20)

        _scrollwindow = RAMSTKScrolledWindow(_fixed)
        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("Purchasing Information"))
        _frame.add(_scrollwindow)
        _vpaned.pack1(_frame, True)

        (__, __, _fixed) = super().make_ui(start=20)
        _scrollwindow = RAMSTKScrolledWindow(_fixed)
        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("Miscellaneous Information"))
        _frame.add(_scrollwindow)
        _vpaned.pack2(_frame, True, True)

        _label = RAMSTKLabel(_("General\nData"))
        _label.do_set_properties(
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_(
                "Displays general information for the selected Hardware"))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def __set_callbacks(self) -> None:
        """
        Set the callback methods and functions.

        :return: None
        :rtype: None
        """
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
            self.txtAltPartNum.connect('focus-out-event', self._on_focus_out,
                                       6))
        self._lst_handler_id.append(
            self.txtAttachments.do_get_buffer().connect(
                'changed', self._on_focus_out, None, 7))
        self._lst_handler_id.append(
            self.txtCAGECode.connect('focus-out-event', self._on_focus_out, 8))
        self._lst_handler_id.append(
            self.txtCompRefDes.connect('focus-out-event', self._on_focus_out,
                                       9))
        self._lst_handler_id.append(
            self.txtCost.connect('focus-out-event', self._on_focus_out, 10))
        self._lst_handler_id.append(
            self.txtDescription.do_get_buffer().connect(
                'changed', self._on_focus_out, None, 11))
        self._lst_handler_id.append(
            self.txtFigureNumber.connect('focus-out-event', self._on_focus_out,
                                         12))
        self._lst_handler_id.append(
            self.txtLCN.connect('focus-out-event', self._on_focus_out, 13))
        self._lst_handler_id.append(
            self.txtName.connect('focus-out-event', self._on_focus_out, 14))
        self._lst_handler_id.append(
            self.txtNSN.connect('focus-out-event', self._on_focus_out, 15))
        self._lst_handler_id.append(
            self.txtPageNumber.connect('focus-out-event', self._on_focus_out,
                                       16))
        self._lst_handler_id.append(
            self.txtPartNumber.connect('focus-out-event', self._on_focus_out,
                                       17))
        self._lst_handler_id.append(
            self.txtQuantity.connect('focus-out-event', self._on_focus_out,
                                     18))
        self._lst_handler_id.append(
            self.txtRefDes.connect('focus-out-event', self._on_focus_out, 19))
        self._lst_handler_id.append(self.txtRemarks.do_get_buffer().connect(
            'changed', self._on_focus_out, None, 20))
        self._lst_handler_id.append(
            self.txtSpecification.connect('focus-out-event',
                                          self._on_focus_out, 21))
        self._lst_handler_id.append(
            self.txtYearMade.connect('focus-out-event', self._on_focus_out,
                                     22))

    def __set_properties(self) -> None:
        """
        Set the properties of the General Data Work View and widgets.

        :return: None
        :rtype: None
        """
        # ----- BUTTONS
        self.chkRepairable.do_set_properties(
            tooltip=_("Indicates whether or not the selected hardware item is "
                      "repairable."))
        self.chkTagged.do_set_properties()

        # ----- ENTRIES
        self.txtAltPartNum.do_set_properties(
            tooltip=_("The alternate part number (if any) of the selected "
                      "hardware item."))
        self.txtAttachments.do_set_properties(
            width=600,
            tooltip=_("Hyperlinks to any documents associated with the "
                      "selected hardware item."))
        self.txtCAGECode.do_set_properties(
            tooltip=_("The Commerical and Government Entity (CAGE) Code of "
                      "the selected hardware item."))
        self.txtCompRefDes.do_set_properties(
            tooltip=_("The composite reference designator of the selected "
                      "hardware item."))
        self.txtCost.do_set_properties(
            width=100,
            tooltip=_("The unit cost of the selected hardware item."))
        self.txtDescription.do_set_properties(
            width=600,
            tooltip=_("The description of the selected hardware item."))
        self.txtFigureNumber.do_set_properties(
            tooltip=_("The figure number in the governing specification for "
                      "the selected hardware item."))
        self.txtLCN.do_set_properties(
            tooltip=_("The Logistics Control Number (LCN) of the selected "
                      "hardware item."))
        self.txtName.do_set_properties(
            width=600, tooltip=_("The name of the selected hardware item."))
        self.txtNSN.do_set_properties(
            tooltip=_("The National Stock Number (NSN) of the selected "
                      "hardware item."))
        self.txtPageNumber.do_set_properties(
            tooltip=_("The page number in the governing specification for the "
                      "selected hardware item."))
        self.txtPartNumber.do_set_properties(
            tooltip=_("The part number of the selected hardware item."))
        self.txtQuantity.do_set_properties(
            width=50,
            tooltip=_(
                "The number of the selected hardware items in the design."))
        self.txtRefDes.do_set_properties(tooltip=_(
            "The reference designator of the selected hardware item."))
        self.txtRemarks.do_set_properties(
            height=150,
            width=600,
            tooltip=_("Enter any remarks associated with the selected "
                      "hardware item."))
        self.txtSpecification.do_set_properties(
            tooltip=_("The specification (if any) governing the selected "
                      "hardware item."))
        self.txtYearMade.do_set_properties(
            width=100,
            tooltip=_(
                "The year the the selected hardware item was manufactured."))

    def _do_clear_page(self) -> None:
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        self.chkRepairable.do_update(False, self._lst_handler_id[0])
        self.chkTagged.do_update(False, self._lst_handler_id[1])
        self.cmbCategory.do_update(0, self._lst_handler_id[2])
        self.cmbSubcategory.do_update(0, self._lst_handler_id[5])
        self.cmbCostType.do_update(0, self._lst_handler_id[3])
        self.cmbManufacturer.do_update(0, self._lst_handler_id[4])
        self.txtAltPartNum.do_update('', self._lst_handler_id[6])
        self.txtAttachments.do_update('', self._lst_handler_id[7])
        self.txtCAGECode.do_update('', self._lst_handler_id[8])
        self.txtCompRefDes.do_update('', self._lst_handler_id[9])
        self.txtCost.do_update('', self._lst_handler_id[10])
        self.txtDescription.do_update('', self._lst_handler_id[11])
        self.txtFigureNumber.do_update('', self._lst_handler_id[12])
        self.txtLCN.do_update('', self._lst_handler_id[13])
        self.txtName.do_update('', self._lst_handler_id[14])
        self.txtNSN.do_update('', self._lst_handler_id[15])
        self.txtPageNumber.do_update('', self._lst_handler_id[16])
        self.txtPartNumber.do_update('', self._lst_handler_id[17])
        self.txtQuantity.do_update('', self._lst_handler_id[18])
        self.txtRefDes.do_update('', self._lst_handler_id[19])
        self.txtRemarks.do_update('', self._lst_handler_id[20])
        self.txtSpecification.do_update('', self._lst_handler_id[21])
        self.txtYearMade.do_update('', self._lst_handler_id[22])

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Hardware General Data page.

        :param dict attributes: the Hardware attributes to load into the Work
            View widgets.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']
        self._record_id = attributes['hardware_id']

        # Disable the category RAMSTKCombo() if the hardware item is not a part.
        if attributes['part'] == 1:
            self.cmbCategory.set_button_sensitivity(Gtk.SensitivityType.ON)
            self.cmbSubcategory.set_button_sensitivity(Gtk.SensitivityType.ON)

            self.cmbCategory.set_active(int(attributes['category_id']))

            self._do_load_subcategory(int(attributes['category_id']))
            self.cmbSubcategory.do_update(int(attributes['subcategory_id']),
                                          self._lst_handler_id[5])

        else:
            self.cmbCategory.set_button_sensitivity(Gtk.SensitivityType.OFF)
            self.cmbSubcategory.set_button_sensitivity(Gtk.SensitivityType.OFF)

            # Clear the subcategory RAMSTKComboBox() always so it is empty
            # whenever an assembly is selected.
            _model = self.cmbSubcategory.get_model()
            _model.clear()

        self.chkRepairable.do_update(int(attributes['repairable']),
                                     self._lst_handler_id[0])
        self.chkTagged.do_update(int(attributes['tagged_part']),
                                 self._lst_handler_id[1])

        self.cmbCostType.do_update(int(attributes['cost_type_id']),
                                   self._lst_handler_id[3])
        self.cmbManufacturer.do_update(int(attributes['manufacturer_id']),
                                       self._lst_handler_id[4])
        self.txtAltPartNum.do_update(str(attributes['alt_part_number']),
                                     self._lst_handler_id[6])
        self.txtAttachments.do_update(str(attributes['attachments']),
                                      self._lst_handler_id[7])
        self.txtCAGECode.do_update(str(attributes['cage_code']),
                                   self._lst_handler_id[8])
        self.txtCompRefDes.do_update(str(attributes['comp_ref_des']),
                                     self._lst_handler_id[9])
        self.txtCost.do_update(str(locale.currency(attributes['cost'])),
                               self._lst_handler_id[10])
        self.txtDescription.do_update(str(attributes['description']),
                                      self._lst_handler_id[11])
        self.txtFigureNumber.do_update(str(attributes['figure_number']),
                                       self._lst_handler_id[12])
        self.txtLCN.do_update(str(attributes['lcn']), self._lst_handler_id[13])
        self.txtName.do_update(str(attributes['name']),
                               self._lst_handler_id[14])
        self.txtNSN.do_update(str(attributes['nsn']), self._lst_handler_id[15])
        self.txtPageNumber.do_update(str(attributes['page_number']),
                                     self._lst_handler_id[16])
        self.txtPartNumber.do_update(str(attributes['part_number']),
                                     self._lst_handler_id[17])
        self.txtQuantity.do_update(str(attributes['quantity']),
                                   self._lst_handler_id[18])
        self.txtRefDes.do_update(str(attributes['ref_des']),
                                 self._lst_handler_id[19])
        self.txtRemarks.do_update(str(attributes['remarks']),
                                  self._lst_handler_id[20])
        self.txtSpecification.do_update(
            str(attributes['specification_number']), self._lst_handler_id[21])
        self.txtYearMade.do_update(str(attributes['year_of_manufacture']),
                                   self._lst_handler_id[22])

    def _do_load_subcategory(self, category_id: int) -> None:
        """
        Load the component subcategory RAMSTKCombo().

        This method loads the component subcategory RAMSTKCombo() when the
        component category RAMSTKCombo() is changed.

        :param int category_id: the component category ID to load the
                                subcategory RAMSTKCombo() for.
        :return: None
        :rtype: None
        """
        _model = self.cmbSubcategory.get_model()
        _model.clear()

        if category_id > 0:
            _subcategory = SortedDict(self.RAMSTK_USER_CONFIGURATION.
                                      RAMSTK_SUBCATEGORIES[category_id])
            _data = []
            for _key in _subcategory:
                _data.append([_subcategory[_key]])

            self.cmbSubcategory.do_load_combo(_data)

    def _do_request_make_comp_ref_des(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to create the composite reference designator.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_make_comp_ref_des', node_id=self._record_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    # TODO: Make this public per convention 303.3.  Do this for all workviews.
    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save the currently selected Hardware.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_hardware', node_id=self._record_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    # TODO: Make this public per convention 303.3.  Do this for all workviews.
    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save all the Hardwares.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_hardware')
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _on_combo_changed(self, combo: RAMSTKComboBox, index: int) -> None:
        """
        Retrieve RAMSTKCombo() changes and assign to Hardware attribute.

        This method is called by:

            * Gtk.Combo() 'changed' signal

        This method sends the 'changedCategory', 'changedSubcategory',
        and 'wvw_editing_hardware' messages.

        :param combo: the RAMSTKComboBox() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.RAMSTKComboBox`
        :param int index: the position in the Requirement class Gtk.TreeModel()
            associated with the data from the calling Gtk.Entry().  Indices
            are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    2    | cmbCategory      |    4    | cmbManufacturer  |
            +---------+------------------+---------+------------------+
            |    3    | cmbCostType      |    5    | cmbSubcategory   |
            +---------+------------------+---------+------------------+

        :return: None
        :rtype: None
        """
        try:
            _key = self._dic_keys[index]
        except KeyError:
            _key = ''

        combo.handler_block(self._lst_handler_id[index])

        try:
            _new_text = int(combo.get_active())
        except ValueError:
            _new_text = 0

        if index == 2:
            pub.sendMessage('changed_category', category_id=_new_text)
        elif index == 4:
            _model = combo.get_model()
            _row = combo.get_active_iter()
            self.txtCAGECode.do_update(str(_model.get(_row, 2)[0]),
                                       self._lst_handler_id[8])
            pub.sendMessage('wvw_editing_hardware',
                            node_id=[self._record_id, -1],
                            package={'cage_code': str(_model.get(_row, 2)[0])})
        elif index == 5:
            pub.sendMessage('changed_subcategory', subcategory_id=_new_text)

        pub.sendMessage('wvw_editing_hardware',
                        node_id=[self._record_id, -1],
                        package={_key: _new_text})

        combo.handler_unblock(self._lst_handler_id[index])

    def _on_edit(self, node_id: List, package: Dict[str, Any]) -> None:
        """
        Update the Work View Gtk.Widgets() when Hardware attributes change.

        This method is called whenever an attribute is edited in a different
        view.

        :param int module_id: the ID of the Hardware being edited.  This
            parameter is required to allow the PyPubSub signals to call this
            method and the request_set_attributes() method in the
            RAMSTKDataController.
        :param int index: the index in the Hardware attributes list of the
            attribute that was edited.
        :param str value: the new text to update the Gtk.Widget() with.
        :return: None
        :rtype: None
        """
        _module_id = node_id[0]
        [[_key, _value]] = package.items()

        (_function, _id) = self._dic_switch.get(_key)
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

        This method sends the 'wvw_editing_hardware' message.

        :param entry: the Gtk.Entry() that called the method.
        :type entry: :class:`Gtk.Entry`
        :param __event: the Gdk.EventFocus that triggered the signal.
        :type __event: :class:`Gdk.EventFocus`
        :param int index: the position in the Hardware class Gtk.TreeModel()
            associated with the data from the calling Gtk.Entry().
        :return: None
        :rtype: None
        """
        try:
            _key = self._dic_keys[index]
        except KeyError as _error:
            _key = ''
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        entry.handler_block(self._lst_handler_id[index])

        try:
            if index in [7, 11, 20]:
                _new_text: str = str(entry.get_text(*entry.get_bounds(), True))
            else:
                _new_text = str(entry.get_text())
        except ValueError as _error:
            _new_text = ''
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        pub.sendMessage('wvw_editing_hardware',
                        node_id=[self._record_id, -1],
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
        super().on_toggled(checkbutton,
                           index,
                           message='wvw_editing_hardware',
                           keys=self._dic_keys)

        checkbutton.handler_unblock(self._lst_handler_id[index])
