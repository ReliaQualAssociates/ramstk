# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.workview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Hardware Work View."""

# Standard Library Imports
import locale
from typing import Any, Dict, List

# Third Party Imports
import treelib
from pubsub import pub
from sortedcontainers import SortedDict

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTK_ACTIVE_ENVIRONMENTS, RAMSTK_DORMANT_ENVIRONMENTS,
    RAMSTK_HR_DISTRIBUTIONS, RAMSTK_HR_MODELS, RAMSTK_HR_TYPES,
    RAMSTKUserConfiguration)
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton, RAMSTKComboBox, RAMSTKEntry, RAMSTKFrame, RAMSTKLabel,
    RAMSTKScrolledWindow, RAMSTKTextView, RAMSTKWorkView)

# RAMSTK Local Imports
from .components import (
    RAMSTKStressInputs, RAMSTKStressResults, capacitor, connection, inductor,
    integrated_circuit, meter, miscellaneous, relay, resistor)


def _do_get_attributes(dmtree: treelib.Tree, record_id: int) -> Dict[str, Any]:
    """
    Converts the treelib.Tree() holding hardware info into the standrd dict.

    The Hardware datamanager is a complex conglomerate of data.  The data is
    carried as data packages in the treelib.Tree() rather than a dict of
    attributes because it's easier to build the tree.  This function simply
    packs the tree data into a dict for consumption.

    :param dmtree: the hardware item treelib.Tree().
    :type dmtree: :class:`treelib.Tree`
    :param record_id: the hardware ID of the currently selected record.
    :return: _attributes; the attributes dict of the currently selected
        hardware item.
    :rtype: dict
    """
    _attributes = dmtree.get_node(
        record_id).data['design_electric'].get_attributes()
    _attributes = {
        **_attributes,
        **dmtree.get_node(record_id).data['reliability'].get_attributes()
    }
    _attributes = {
        **_attributes,
        **dmtree.get_node(record_id).data['hardware'].get_attributes()
    }
    _attributes = {
        **_attributes,
        **dmtree.get_node(record_id).data['mil_hdbk_217f'].get_attributes()
    }

    return _attributes


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
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/rollup.png')

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

        self._dic_switch: Dict[str, List[Any]] = {
            'category_id': [self.cmbCategory.do_update, 2],
            'cost_type_id': [self.cmbCostType.do_update, 3],
            'manufacturer_id': [self.cmbManufacturer.do_update, 4],
            'subcategory_id': [self.cmbSubcategory.do_update, 5],
            'alt_part_number': [self.txtAltPartNum.do_update, 6],
            'attachments': [self.txtAttachments.do_update, 7],
            'cage_code': [self.txtCAGECode.do_update, 8],
            'comp_ref_des': [self.txtCompRefDes.do_update, 9],
            'cost': [self.txtCost.do_update, 10],
            'description': [self.txtDescription.do_update, 11],
            'figure_number': [self.txtFigureNumber.do_update, 12],
            'lcn': [self.txtLCN.do_update, 13],
            'name': [self.txtName.do_update, 14],
            'nsn': [self.txtNSN.do_update, 15],
            'page_number': [self.txtPageNumber.do_update, 16],
            'part_number': [self.txtPartNumber.do_update, 17],
            'quantity': [self.txtQuantity.do_update, 18],
            'ref_des': [self.txtRefDes.do_update, 19],
            'remarks': [self.txtRemarks.do_update, 20],
            'specification_number': [self.txtSpecification.do_update, 21],
            'year_of_manufacture': [self.txtYearMade.do_update, 22]
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
        pub.subscribe(self.on_edit, 'mvw_editing_hardware')
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_hardware')

        pub.subscribe(self._do_clear_page, 'request_clear_workviews')
        pub.subscribe(self._do_load_page, 'selected_hardware')
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
        #                                      buttons -----+--> Gtk.HBox
        #                                                   |
        #                   RAMSTKFrame ---+-->Gtk.HPaned --+
        #                                  |
        # RAMSTKFrame ---+-->Gtk.VPaned ---+
        #                |
        # RAMSTKFrame ---+
        # Make the buttons.
        super().make_toolbuttons(
            icons=['comp_ref_des'],
            tooltips=[
                _("Creates the composite reference designator for the "
                  "selected hardware item.")
            ],
            callbacks=[self._do_request_make_comp_ref_des])

        _hpaned = Gtk.HPaned()
        self.pack_start(_hpaned, True, True, 0)

        # Make the left side of the page.
        # TODO: See issue #304.  Only _fixed will be returned in the future.
        # pylint: disable=unused-variable
        (__, __, _fixed) = super().make_ui(start=0, end=13)

        _scrollwindow = RAMSTKScrolledWindow(_fixed)
        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("General Information"))
        _frame.add(_scrollwindow)
        _hpaned.pack1(_frame, True, True)

        # Make the top right side of the page.
        _vpaned = Gtk.VPaned()
        _hpaned.pack2(_vpaned, True, True)
        # TODO: See issue #304.  Only _fixed will be returned in the future.
        # pylint: disable=unused-variable
        (__, __, _fixed) = super().make_ui(start=13, end=20)

        _scrollwindow = RAMSTKScrolledWindow(_fixed)
        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("Purchasing Information"))
        _frame.add(_scrollwindow)
        _vpaned.pack1(_frame, True, True)

        # Make the bottom right side of the page.
        # TODO: See issue #304.  Only _fixed will be returned in the future.
        # pylint: disable=unused-variable
        (__, __, _fixed) = super().make_ui(start=20)
        _scrollwindow = RAMSTKScrolledWindow(_fixed)
        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("Miscellaneous Information"))
        _frame.add(_scrollwindow)
        _vpaned.pack2(_frame, True, True)

        # Set the tab label.
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

            self.cmbCategory.do_update(int(attributes['category_id']),
                                       self._lst_handler_id[2])

            self._do_load_subcategory(int(attributes['category_id']))
            self.cmbSubcategory.do_update(int(attributes['subcategory_id']),
                                          self._lst_handler_id[5])

        else:
            self.cmbCategory.set_button_sensitivity(Gtk.SensitivityType.OFF)
            self.cmbSubcategory.set_button_sensitivity(Gtk.SensitivityType.OFF)

            self.cmbCategory.do_update(int(attributes['category_id']),
                                       self._lst_handler_id[2])

            self.cmbSubcategory.do_update(int(attributes['subcategory_id']),
                                          self._lst_handler_id[5])

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
        self.cmbSubcategory.do_load_combo([],
                                          handler_id=self._lst_handler_id[5])

        if category_id > 0:
            _subcategory = SortedDict(self.RAMSTK_USER_CONFIGURATION.
                                      RAMSTK_SUBCATEGORIES[category_id])
            _data = []
            for _key in _subcategory:
                _data.append([_subcategory[_key]])
            self.cmbSubcategory.do_load_combo(
                _data, handler_id=self._lst_handler_id[5])

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
        self.do_set_cursor_busy()
        pub.sendMessage('request_update_hardware', node_id=self._record_id)

    # TODO: Make this public per convention 303.3.  Do this for all workviews.
    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save all the Hardwares.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.do_set_cursor_busy()
        pub.sendMessage('request_update_all_hardware')

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
        # TODO: See issue #310.
        combo.handler_block(self._lst_handler_id[index])

        _package = super().on_combo_changed(combo, index,
                                            'wvw_editing_hardware')
        _new_text = list(_package.values())[0]

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

        combo.handler_unblock(self._lst_handler_id[index])

    # pylint: disable=unused-argument
    def _on_focus_out(self, entry: Gtk.Entry, __event: Gdk.EventFocus,
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
        # TODO: See issue #310.
        entry.handler_block(self._lst_handler_id[index])

        _package = super().on_focus_out(entry, index, 'wvw_editing_hardware')
        # pylint: disable=unused-variable
        [[_key, __]] = _package.items()

        try:
            if index == 7:
                _package[_key] = self.txtAttachments.do_get_text()
            elif index == 10:
                # Removes the currency symbol from the beginning of the
                # string.
                _package[_key] = float(str(entry.get_text())[1:])
            elif index == 11:
                _package[_key] = self.txtDescription.do_get_text()
            elif index == 20:
                _package[_key] = self.txtRemarks.do_get_text()
            elif index in [18, 22]:
                _package[_key] = int(entry.get_text())
        except ValueError as _error:
            _package[_key] = ''
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        pub.sendMessage('wvw_editing_hardware',
                        node_id=[self._record_id, -1],
                        package=_package)

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
        super().on_toggled(checkbutton, index, 'wvw_editing_hardware')

        checkbutton.handler_unblock(self._lst_handler_id[index])


class AssessmentInputs(RAMSTKWorkView):
    """
    Display Hardware assessment input attribute data in the RAMSTK Work Book.

    The Hardware assessment input view displays all the assessment inputs for
    the selected Hardware item.  This includes, currently, inputs for
    MIL-HDBK-217FN2 and NSWC-11.  The attributes of a Hardware assessment
    input view are:

    :cvar list _lst_labels: the text to use for the assessment input widget
        labels.

    :ivar dict _dic_assessment_input: dictionary of component-specific
        AssessmentInputs classes.
    :ivar int _hardware_id: the ID of the Hardware item currently being
        displayed.
    :ivar int _hazard_rate_method_id: the ID of the hazard rate method used for
        Hardware item.

    :ivar cmbActiveEnviron: the operating environment for the hardware item.
    :ivar cmbDormantEnviron: the storage environment for the hardware item.
    :ivar cmbFailureDist: the statistical failure distribution of the hardware
        item.
    :ivar cmbHRType: the type of reliability assessment for the selected
        hardware item.
    :ivar cmbHRMethod: the assessment method to use for the selected hardware
        item.
    :ivar fraDesignRatings: the container to embed the piece part design
        attributes Gtk.Fised().
    :ivar fraOperatingStress: the container to embed the piece part operating
        stresses Gtk.Fixed().
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

    Callbacks signals in RAMSTKBaseView._lst_handler_id:

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
    # Define private dict attributes.
    _dic_keys = {
        0: 'environment_active_id',
        1: 'environment_dormant_id',
        2: 'failure_distribution_id',
        3: 'hazard_rate_type_id',
        4: 'hazard_rate_method_id',
        5: 'temperature_active',
        6: 'add_adj_factor',
        7: 'temperature_dormant',
        8: 'scale_parameter',
        9: 'shape_parameter',
        10: 'location_parameter',
        11: 'mult_adj_factor',
        12: 'hazard_rate_specified',
        13: 'hr_specified_variance',
        14: 'mtbf_specified',
        15: 'mtbf_specified_variance',
        16: 'duty_cycle',
        17: 'mission_time'
    }

    # Define private list attributes.
    _lst_labels = [
        _("Assessment Type:"),
        _("Assessment Method:"),
        _("Stated Hazard Rate [h(t)]:"),
        _("Stated h(t) Variance:"),
        _("Stated MTBF:"),
        _("Stated MTBF Variance:"),
        _("Failure Distribution:"),
        _("Scale Parameter:"),
        _("Shape Parameter:"),
        _("Location Parameter:"),
        _("Additive Adjustment Factor:"),
        _("Multiplicative Adjustment Factor:"),
        _("Active Environment:"),
        _("Active Temperature (\u00B0C):"),
        _("Dormant Environment:"),
        _("Dormant Temperature (\u00B0C):"),
        _("Mission Time:"),
        _("Duty Cycle:")
    ]

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'hardware') -> None:
        """
        Initialize an instance of the Hardware assessment input view.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param str module: the name of the RAMSTK workflow module.
        """
        super().__init__(configuration, logger, module)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.
        self._dic_assessment_input: Dict[int, object] = {
            1: integrated_circuit.AssessmentInputs(configuration, logger),
            # 2: wvwSemiconductorAI(self.RAMSTK_CONFIGURATION),
            3: resistor.AssessmentInputs(configuration, logger),
            4: capacitor.AssessmentInputs(configuration, logger),
            5: inductor.AssessmentInputs(configuration, logger),
            6: relay.AssessmentInputs(configuration, logger),
            # 7: wvwSwitchAI(self.RAMSTK_CONFIGURATION),
            8: connection.AssessmentInputs(configuration, logger),
            9: meter.AssessmentInputs(configuration, logger),
            10: miscellaneous.AssessmentInputs(configuration, logger)
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hazard_rate_method_id: int = 0
        self._subcategory_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbActiveEnviron: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbDormantEnviron: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbFailureDist: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbHRType: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbHRMethod: RAMSTKComboBox = RAMSTKComboBox()

        self.scwDesignRatings: RAMSTKScrolledWindow = RAMSTKScrolledWindow(
            None)

        self.txtActiveTemp: RAMSTKEntry = RAMSTKEntry()
        self.txtAddAdjFactor: RAMSTKEntry = RAMSTKEntry()
        self.txtDormantTemp: RAMSTKEntry = RAMSTKEntry()
        self.txtDutyCycle: RAMSTKEntry = RAMSTKEntry()
        self.txtFailScale: RAMSTKEntry = RAMSTKEntry()
        self.txtFailShape: RAMSTKEntry = RAMSTKEntry()
        self.txtFailLocation: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionTime: RAMSTKEntry = RAMSTKEntry()
        self.txtMultAdjFactor: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecifiedHt: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecifiedHtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecifiedMTBF: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecifiedMTBFVar: RAMSTKEntry = RAMSTKEntry()

        self.wvwOperatingStress: RAMSTKStressInputs = RAMSTKStressInputs(
            configuration, logger)

        self._lst_widgets = [
            self.cmbHRType, self.cmbHRMethod, self.txtSpecifiedHt,
            self.txtSpecifiedHtVar, self.txtSpecifiedMTBF,
            self.txtSpecifiedMTBFVar, self.cmbFailureDist, self.txtFailScale,
            self.txtFailShape, self.txtFailLocation, self.txtAddAdjFactor,
            self.txtMultAdjFactor, self.cmbActiveEnviron, self.txtActiveTemp,
            self.cmbDormantEnviron, self.txtDormantTemp, self.txtMissionTime,
            self.txtDutyCycle
        ]

        self._dic_switch = {
            'add_adj_factor': [self.txtAddAdjFactor.do_update, 6],
            'scale_parameter': [self.txtFailScale.do_update, 8],
            'shape_parameter': [self.txtFailShape.do_update, 9],
            'location_parameter': [self.txtFailLocation.do_update, 10],
            'mult_adj_factor': [self.txtMultAdjFactor.do_update, 11],
            'hazard_rate_specified': [self.txtSpecifiedHt.do_update, 12],
            'hr_specified_variance': [self.txtSpecifiedHtVar.do_update, 13],
            'mtbf_specified': [self.txtSpecifiedMTBF.do_update, 14],
            'mtbf_spec_variance': [self.txtSpecifiedMTBFVar.do_update, 15],
            'duty_cycle': [self.txtDutyCycle.do_update, 16],
            'mission_time': [self.txtMissionTime.do_update, 17]
        }

        self.__set_properties()
        self.__load_combobox()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_hardware')

        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._do_request_hardware_tree, 'selected_hardware')
        pub.subscribe(self._do_load_page, 'succeed_get_hardware_tree')

    def __load_combobox(self) -> None:
        """
        Load the RAMSTK ComboBox widgets with lists of information.

        :return: None
        :rtype: None
        """
        self.cmbActiveEnviron.do_load_combo(RAMSTK_ACTIVE_ENVIRONMENTS)
        self.cmbDormantEnviron.do_load_combo(RAMSTK_DORMANT_ENVIRONMENTS)
        self.cmbHRType.do_load_combo(RAMSTK_HR_TYPES)
        self.cmbHRMethod.do_load_combo(RAMSTK_HR_MODELS)
        self.cmbFailureDist.do_load_combo(RAMSTK_HR_DISTRIBUTIONS)

    def __make_ui(self) -> None:
        """
        Make the Hardware class Gtk.Notebook() assessment input page.

        :return: None
        :rtype: None
        """
        # This page has the following layout:
        # +-----+-------------------+-------------------+
        # |  B  |      L. TOP       |      R. TOP       |
        # |  U  |                   |                   |
        # |  T  |                   |                   |
        # |  T  +-------------------+-------------------+
        # |  O  |     L. BOTTOM     |     R. BOTTOM     |
        # |  N  |                   |                   |
        # |  S  |                   |                   |
        # +-----+-------------------+-------------------+
        #                                        buttons -----+--> Gtk.HBox
        #                                                     |
        # RAMSTKFrame ---+--> Gtk.VPaned ---+--> Gtk.HPaned --+
        #                |                  |
        # RAMSTKFrame ---+                  |
        #                                   |
        # RAMSTKFrame ---+--> Gtk.VPaned ---+
        #                |
        # RAMSTKFrame ---+

        # Make the buttons.
        super().make_toolbuttons(
            icons=['calculate'],
            tooltips=[
                _("Calculate the currently selected Hardware item."),
            ],
            callbacks=[self._do_request_calculate_hardware])

        _hpaned = Gtk.HPaned()
        self.pack_start(_hpaned, True, True, 0)

        # Make the left side of the page.
        _vpn_left = Gtk.VPaned()
        _hpaned.pack1(_vpn_left, True, True)

        # Top left quadrant.
        # TODO: See issue #304.  Only _fixed will be returned in the future.
        # pylint: disable=unused-variable
        (__, __, _fixed) = super().make_ui(start=0, end=12)

        _scrollwindow = RAMSTKScrolledWindow(_fixed)
        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("Assessment Inputs"))
        _frame.add(_scrollwindow)
        _vpn_left.pack1(_frame, True, True)

        # Bottom left quadrant.  This is just an RAMSTKFrame() and will be the
        # container for component-specific design attributes.
        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("Design Ratings"))
        _frame.add(self.scwDesignRatings)
        _vpn_left.pack2(_frame, True, True)

        # Make the right side of the page.
        _vpn_right = Gtk.VPaned()
        _hpaned.pack2(_vpn_right, True, True)

        # Top right quadrant.
        # TODO: See issue #304.  Only _fixed will be returned in the future.
        # pylint: disable=unused-variable
        (__, __, _fixed) = super().make_ui(start=12)

        _scrollwindow = RAMSTKScrolledWindow(_fixed)
        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("Environmental Inputs"))
        _frame.add(_scrollwindow)
        _vpn_right.pack1(_frame, True, True)

        # Bottom right quadrant.  This is just an RAMSTKFrame() and will be the
        # container for component-specific design attributes.
        _scrollwindow = RAMSTKScrolledWindow(self.wvwOperatingStress)
        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("Operating Stresses"))
        _frame.add(_scrollwindow)
        _vpn_right.pack2(_frame, True, True)

        # Set the tab label.
        _label = RAMSTKLabel(_("Assessment\nInputs"))
        _label.do_set_properties(
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_("Displays reliability assessment inputs for the "
                      "selected hardware item."))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def __set_callbacks(self) -> None:
        """
        Set the callback methods and functions.

        :return: None
        :rtype: None
        """
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
            self.txtActiveTemp.connect('focus-out-event', self._on_focus_out,
                                       5))
        self._lst_handler_id.append(
            self.txtAddAdjFactor.connect('focus-out-event', self._on_focus_out,
                                         6))
        self._lst_handler_id.append(
            self.txtDormantTemp.connect('focus-out-event', self._on_focus_out,
                                        7))
        self._lst_handler_id.append(
            self.txtFailScale.connect('focus-out-event', self._on_focus_out,
                                      8))
        self._lst_handler_id.append(
            self.txtFailShape.connect('focus-out-event', self._on_focus_out,
                                      9))
        self._lst_handler_id.append(
            self.txtFailLocation.connect('focus-out-event', self._on_focus_out,
                                         10))
        self._lst_handler_id.append(
            self.txtMultAdjFactor.connect('focus-out-event',
                                          self._on_focus_out, 11))
        self._lst_handler_id.append(
            self.txtSpecifiedHt.connect('focus-out-event', self._on_focus_out,
                                        12))
        self._lst_handler_id.append(
            self.txtSpecifiedHtVar.connect('focus-out-event',
                                           self._on_focus_out, 13))
        self._lst_handler_id.append(
            self.txtSpecifiedMTBF.connect('focus-out-event',
                                          self._on_focus_out, 14))
        self._lst_handler_id.append(
            self.txtSpecifiedMTBFVar.connect('focus-out-event',
                                             self._on_focus_out, 15))
        self._lst_handler_id.append(
            self.txtDutyCycle.connect('focus-out-event', self._on_focus_out,
                                      16))
        self._lst_handler_id.append(
            self.txtMissionTime.connect('focus-out-event', self._on_focus_out,
                                        17))

    def __set_properties(self) -> None:
        """
        Set the properties of the General Data Work View and widgets.

        :return: None
        :rtype: None
        """

        self._lst_widgets = [
            self.cmbHRType, self.cmbHRMethod, self.txtSpecifiedHt,
            self.txtSpecifiedHtVar, self.txtSpecifiedMTBF,
            self.txtSpecifiedMTBFVar, self.cmbFailureDist, self.txtFailScale,
            self.txtFailShape, self.txtFailLocation, self.txtAddAdjFactor,
            self.txtMultAdjFactor, self.cmbActiveEnviron, self.txtActiveTemp,
            self.cmbDormantEnviron, self.txtDormantTemp, self.txtMissionTime,
            self.txtDutyCycle
        ]
        _lst_width = [
            200, 200, 125, 125, 125, 125, 200, 125, 125, 125, 125, 125, 200,
            125, 200, 125, 125, 125
        ]
        _lst_tooltips = [
            _("The type of reliability assessment for the "
              "selected hardware item."),
            _("The assessment method to use for the selected "
              "hardware item."),
            _("The stated hazard rate."),
            _("The variance of the stated hazard rate."),
            _("The stated mean time between failure (MTBF)."),
            _("The variance of the stated mean time between "
              "failure (MTBF)."),
            _("The statistical failure distribution of the "
              "hardware item."),
            _("The scale parameter of the statistical failure "
              "distribution."),
            _("The shape parameter of the statistical failure "
              "distribution."),
            _("The location parameter of the statistical failure "
              "distribution."),
            _("An adjustment factor to add to the assessed "
              "hazard rate or MTBF."),
            _("An adjustment factor to multiply the assessed "
              "hazard rate or MTBF by."),
            _("The operating environment for the hardware "
              "item."),
            _("The ambient temperature in the operating "
              "environment."),
            _("The storage environment for the hardware item."),
            _("The ambient temperature in the storage "
              "environment."),
            _("The mission time of the selected hardware item."),
            _("The duty cycle of the selected hardware item.")
        ]

        _idx = 0
        for _widget in self._lst_widgets:
            _widget.do_set_properties(width=_lst_width[_idx],
                                      tooltip=_lst_tooltips[_idx])
            _idx += 1

    def _do_clear_page(self) -> None:
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        # Clear the component-specific Gtk.ScrolledWindow()s.
        for _child in self.scwDesignRatings.get_children():
            self.scwDesignRatings.remove(_child)

        self.cmbActiveEnviron.do_update(0, self._lst_handler_id[0])
        self.cmbDormantEnviron.do_update(0, self._lst_handler_id[1])
        self.cmbFailureDist.do_update(0, self._lst_handler_id[2])
        self.cmbHRType.do_update(0, self._lst_handler_id[3])
        self.cmbHRMethod.do_update(0, self._lst_handler_id[4])
        self.txtActiveTemp.do_update('', self._lst_handler_id[5])
        self.txtAddAdjFactor.do_update('', self._lst_handler_id[6])
        self.txtDormantTemp.do_update('', self._lst_handler_id[7])
        self.txtFailScale.do_update('', self._lst_handler_id[8])
        self.txtFailShape.do_update('', self._lst_handler_id[9])
        self.txtFailLocation.do_update('', self._lst_handler_id[10])
        self.txtMultAdjFactor.do_update('', self._lst_handler_id[11])
        self.txtSpecifiedHt.do_update('', self._lst_handler_id[12])
        self.txtSpecifiedHtVar.do_update('', self._lst_handler_id[13])
        self.txtSpecifiedMTBF.do_update('', self._lst_handler_id[14])
        self.txtSpecifiedMTBFVar.do_update('', self._lst_handler_id[15])
        self.txtDutyCycle.do_update('', self._lst_handler_id[16])
        self.txtMissionTime.do_update('', self._lst_handler_id[17])

    def _do_load_page(self, dmtree: treelib.Tree) -> None:
        """
        Load the Hardware Assessment Inputs page.

        :param dict attributes: a dict of attribute key:value pairs for the
            selected Hardware.
        :return: None
        :rtype: None
        """
        attributes = _do_get_attributes(dmtree, self._record_id)

        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        # Operating stress information is only applicable to components,
        # not assemblies so we only show the information for components.
        if attributes['category_id'] > 0:
            self._do_load_component_inputs(attributes)
        else:
            self.scwDesignRatings.hide()
            self.wvwOperatingStress.hide()

        self.cmbActiveEnviron.do_update(
            int(attributes['environment_active_id']), self._lst_handler_id[0])
        self.cmbDormantEnviron.do_update(
            int(attributes['environment_dormant_id']), self._lst_handler_id[1])
        self.cmbFailureDist.do_update(
            int(attributes['failure_distribution_id']),
            self._lst_handler_id[2])
        self.cmbHRType.do_update(int(attributes['hazard_rate_type_id']),
                                 self._lst_handler_id[3])
        self.cmbHRMethod.do_update(int(attributes['hazard_rate_method_id']),
                                   self._lst_handler_id[4])
        self.txtActiveTemp.do_update(
            self.fmt.format(attributes['temperature_active']),
            self._lst_handler_id[5])
        self.txtAddAdjFactor.do_update(
            self.fmt.format(attributes['add_adj_factor']),
            self._lst_handler_id[6])
        self.txtDormantTemp.do_update(
            self.fmt.format(attributes['temperature_dormant']),
            self._lst_handler_id[7])
        self.txtFailScale.do_update(
            self.fmt.format(attributes['scale_parameter']),
            self._lst_handler_id[8])
        self.txtFailShape.do_update(
            self.fmt.format(attributes['shape_parameter']),
            self._lst_handler_id[9])
        self.txtFailLocation.do_update(
            self.fmt.format(attributes['location_parameter']),
            self._lst_handler_id[10])
        self.txtMultAdjFactor.do_update(
            self.fmt.format(attributes['mult_adj_factor']),
            self._lst_handler_id[11])
        self.txtSpecifiedHt.do_update(
            self.fmt.format(attributes['hazard_rate_specified']),
            self._lst_handler_id[12])
        self.txtSpecifiedHtVar.do_update(
            self.fmt.format(attributes['hr_specified_variance']),
            self._lst_handler_id[13])
        self.txtSpecifiedMTBF.do_update(
            self.fmt.format(attributes['mtbf_specified']),
            self._lst_handler_id[14])
        self.txtSpecifiedMTBFVar.do_update(
            self.fmt.format(attributes['mtbf_specified_variance']),
            self._lst_handler_id[15])
        self.txtDutyCycle.do_update(self.fmt.format(attributes['duty_cycle']),
                                    self._lst_handler_id[16])
        self.txtMissionTime.do_update(
            self.fmt.format(attributes['mission_time']),
            self._lst_handler_id[17])

        self._do_set_sensitive(type_id=attributes['hazard_rate_type_id'])

        # Send the PyPubSub message to let the component-specific widgets know
        # they can load.
        pub.sendMessage('loaded_hardware_inputs', attributes=attributes)

    def _do_load_component_inputs(self, attributes: Dict[str, Any]) -> None:
        """
        Load the widgets used to display component-specific input attributes.

        :param attributes: dict containing the attributes of the hardware
            item being loaded.
        :return: None
        :rtype: None
        """
        # Retrieve the appropriate component-specific work views.
        try:
            _component_ai = self._dic_assessment_input[
                attributes['category_id']]
        except KeyError as _error:
            _component_ai = None
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        # If there are already a component-specific work view object,
        # remove them.  Otherwise move along; these aren't the droids we're
        # looking for.
        try:
            self.scwDesignRatings.remove(self.scwDesignRatings.get_child())
        except TypeError as _error:
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        if _component_ai is not None:
            self.scwDesignRatings.add(_component_ai)

        self.scwDesignRatings.show_all()
        self.wvwOperatingStress.show_all()

    def _do_request_calculate_hardware(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to calculate the selected hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        try:
            pub.sendMessage('request_calculate_hardware',
                            node_id=self._record_id)
        except KeyError as _error:
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

    # noinspection PyUnusedLocal
    def _do_request_hardware_tree(self, attributes: Dict[str, Any]) -> None:
        """
        Request the Hardware module treelib Tree().

        :param attributes:
        :return:
        """
        self._record_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']

        pub.sendMessage('request_get_hardware_tree')

    # TODO: Make this public per convention 303.3.  Do this for all workviews.
    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to save the currently selected Hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor_busy()
        pub.sendMessage('request_update_hardware', node_id=self._record_id)

    # TODO: Make this public per convention 303.3.  Do this for all workviews.
    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to save all Hardware items.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor_busy()
        pub.sendMessage('request_update_all_hardware')

    def _do_set_assessed_sensitive(self, type_id: int) -> None:
        """
        Set the widgets used in handbook assessments sensitive.

        :param int type_id: the hazard rate type (source).
        :return: None
        :rtype: None
        """
        if type_id == 1:  # Assessed hazard rate using handbook models.
            self.cmbFailureDist.set_sensitive(False)
            self.cmbHRMethod.set_sensitive(True)
            self.txtFailLocation.set_sensitive(False)
            self.txtFailScale.set_sensitive(False)
            self.txtFailShape.set_sensitive(False)
            self.txtSpecifiedHt.set_sensitive(False)
            self.txtSpecifiedHtVar.set_sensitive(False)
            self.txtSpecifiedMTBF.set_sensitive(False)
            self.txtSpecifiedMTBFVar.set_sensitive(False)

    def _do_set_specified_ht_sensitive(self, type_id: int) -> None:
        """
        Set the widgets used for specifying a hazard rate sensitive.

        :param int type_id: the hazard rate type (source).
        :return: None
        :rtype: None
        """
        if type_id == 2:  # User specified hazard rate.
            self.cmbFailureDist.set_sensitive(False)
            self.cmbHRMethod.set_sensitive(False)
            self.txtFailLocation.set_sensitive(False)
            self.txtFailScale.set_sensitive(False)
            self.txtFailShape.set_sensitive(False)
            self.txtSpecifiedHt.set_sensitive(True)
            self.txtSpecifiedHtVar.set_sensitive(True)
            self.txtSpecifiedMTBF.set_sensitive(False)
            self.txtSpecifiedMTBFVar.set_sensitive(False)

    def _do_set_specified_mtbf_sensitive(self, type_id: int) -> None:
        """
        Set the widgets used for specifying an MTBF sensitive.

        :param int type_id: the hazard rate type (source).
        :return: None
        :rtype: None
        """
        if type_id == 3:  # User specified MTBF.
            self.cmbFailureDist.set_sensitive(False)
            self.cmbHRMethod.set_sensitive(False)
            self.txtFailLocation.set_sensitive(False)
            self.txtFailScale.set_sensitive(False)
            self.txtFailShape.set_sensitive(False)
            self.txtSpecifiedHt.set_sensitive(False)
            self.txtSpecifiedHtVar.set_sensitive(False)
            self.txtSpecifiedMTBF.set_sensitive(True)
            self.txtSpecifiedMTBFVar.set_sensitive(True)

    def _do_set_specified_distribution_sensitive(self, type_id: int) -> None:
        """
        Set the widgets used for specifying a failure distribution sensitive.

        :param int type_id: the hazard rate type (source).
        :return: None
        :rtype: None
        """
        if type_id == 4:
            self.cmbFailureDist.set_sensitive(True)
            self.cmbHRMethod.set_sensitive(False)
            self.txtFailLocation.set_sensitive(True)
            self.txtFailScale.set_sensitive(True)
            self.txtFailShape.set_sensitive(True)
            self.txtSpecifiedHt.set_sensitive(False)
            self.txtSpecifiedHtVar.set_sensitive(False)
            self.txtSpecifiedMTBF.set_sensitive(False)
            self.txtSpecifiedMTBFVar.set_sensitive(False)

    def _do_set_sensitive(self, **kwargs: Any) -> None:
        """
        Set certain widgets sensitive or insensitive.

        This method will set the sensitivity of various widgets depending on
        the hazard rate assessment type selected.

        :return: None
        :rtype: None
        """
        _type_id = kwargs['type_id']

        self._do_set_assessed_sensitive(_type_id)
        self._do_set_specified_ht_sensitive(_type_id)
        self._do_set_specified_mtbf_sensitive(_type_id)
        self._do_set_specified_distribution_sensitive(_type_id)

    def _on_combo_changed(self, combo: RAMSTKComboBox, index: int) -> None:
        """
        Retrieve RAMSTKCombo() changes and assign to Hardware attribute.

        This method is called by:

            * Gtk.Combo() 'changed' signal

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.RAMSTKCombo`
        :param int index: the position in the Hardware class Gtk.TreeModel()
            associated with the data from the calling Gtk.Entry().  Indices
            are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    0    | cmbActiveEnviron |    3    | cmbHRType        |
            +---------+------------------+---------+------------------+
            |    1    | cmbDormantEnviron|    4    | cmbHRMethod      |
            +---------+------------------+---------+------------------+
            |    2    | cmbFailureDist   |         |                  |
            +---------+------------------+---------+------------------+

        :return: None
        :rtype: None
        """
        # TODO: See issue #310.
        combo.handler_block(self._lst_handler_id[index])

        _package = super().on_combo_changed(combo, index,
                                            'wvw_editing_hardware')
        _new_text = list(_package.values())[0]

        # Hazard rate types are:
        #     1 = Assessed
        #     2 = Defined, Hazard Rate
        #     3 = Defined, MTBF
        #     4 = Defined, Distribution
        if index == 3:
            self._do_set_sensitive(type_id=_new_text)
        # Hazard rate methods are:
        #     1 = MIL-HDBK-217F Parts Count
        #     2 = MIL-HDNK-217F Parts Stress
        #     3 = NSWC (not yet implemented)
        elif index == 4:
            pub.sendMessage('changed_hazard_rate_method', method_id=_new_text)
            self._hazard_rate_method_id = _new_text

        combo.handler_unblock(self._lst_handler_id[index])

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
        # TODO: See issue #310.
        entry.handler_block(self._lst_handler_id[index])

        # TODO: See issue #309.
        super().on_focus_out(entry, index, 'wvw_editing_hardware')

        entry.handler_unblock(self._lst_handler_id[index])


class AssessmentResults(RAMSTKWorkView):
    """
    Display Hardware assessment results attribute data in the RAMSTK Work Book.

    The Hardware Assessment Results view displays all the assessment results
    for the selected Hardware.  The attributes of a Hardware Assessment Results
    View are:

    :cvar list _lst_labels: the text to use for the reliability assessment
        results widget labels.

    :ivar dict _dic_assessment_results: dictionary of component-specific
        AssessmentResults classes.
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
        selected hardware item.  This is the sum of the active, dormant, and
        software hazard rates.
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
        hardware item.  This includes preventive and corrective maintenance.
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
    _lst_labels = [
        _("Active Failure Intensity [\u03BB(t)]:"),
        _("Dormant \u03BB(t):"),
        _("Software \u03BB(t):"),
        _("Logistics \u03BB(t):"),
        _("Mission \u03BB(t):"),
        _("Percent \u03BB(t):"),
        _("Logistics MTBF:"),
        _("Mission MTBF:"),
        _("Logistics Reliability [R(t)]:"),
        _("Mission R(t):"),
        _("Logistics Availability [A(t)]:"),
        _("Mission A(t):"),
        _("Total Cost:"),
        _("Cost/Failure:"),
        _("Cost/Hour:"),
        _("Total # of Parts:")
    ]

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'hardware') -> None:
        """
        Initialize an instance of the Hardware assessment output view.

        :param configuration: the RAMSTK User Configuration class instance.
        :type configuration: :class:`ramstk.configuration.UserConfiguration`
        """
        super().__init__(configuration, logger, module)

        # Initialize private dictionary attributes.
        self._dic_assessment_results = {
            1: integrated_circuit.AssessmentResults(configuration, logger),
            # 2: wvwSemiconductorAR(self.RAMSTK_CONFIGURATION),
            3: resistor.AssessmentResults(configuration, logger),
            4: capacitor.AssessmentResults(configuration, logger),
            5: inductor.AssessmentResults(configuration, logger),
            6: relay.AssessmentResults(configuration, logger),
            # 7: wvwSwitchAR(self.RAMSTK_CONFIGURATION),
            8: connection.AssessmentResults(configuration, logger),
            9: meter.AssessmentResults(configuration, logger),
            10: miscellaneous.AssessmentResults(configuration, logger)
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._subcategory_id: int = 0
        self._hazard_rate_method_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.scwReliability: RAMSTKScrolledWindow = RAMSTKScrolledWindow(None)

        self.txtActiveHt: RAMSTKEntry = RAMSTKEntry()
        self.txtActiveHtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtCostFailure: RAMSTKEntry = RAMSTKEntry()
        self.txtCostHour: RAMSTKEntry = RAMSTKEntry()
        self.txtDormantHt: RAMSTKEntry = RAMSTKEntry()
        self.txtDormantHtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsAt: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsAtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsHt: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsHtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsMTBF: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsMTBFVar: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsRt: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsRtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtMCMT: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionAt: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionAtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionHt: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionHtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionMTBF: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionMTBFVar: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionRt: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionRtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtMMT: RAMSTKEntry = RAMSTKEntry()
        self.txtMPMT: RAMSTKEntry = RAMSTKEntry()
        self.txtMTTR: RAMSTKEntry = RAMSTKEntry()
        self.txtPartCount: RAMSTKEntry = RAMSTKEntry()
        self.txtPercentHt: RAMSTKEntry = RAMSTKEntry()
        self.txtSoftwareHt: RAMSTKEntry = RAMSTKEntry()
        self.txtTotalCost: RAMSTKEntry = RAMSTKEntry()

        self.wvwOperatingStress: RAMSTKStressResults = RAMSTKStressResults(
            configuration, logger)

        self._lst_widgets = [
            self.txtActiveHt, self.txtDormantHt, self.txtSoftwareHt,
            self.txtLogisticsHt, self.txtMissionHt, self.txtPercentHt,
            self.txtLogisticsMTBF, self.txtMissionMTBF, self.txtLogisticsRt,
            self.txtMissionRt, self.txtLogisticsAt, self.txtMissionAt,
            self.txtTotalCost, self.txtCostFailure, self.txtCostHour,
            self.txtPartCount
        ]

        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_hardware')

        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._do_request_hardware_tree, 'selected_hardware')
        pub.subscribe(self._do_load_page, 'succeed_get_hardware_tree')
        pub.subscribe(self._do_request_hardware_tree,
                      'succeed_calculate_hardware')

    def __make_ui(self) -> None:
        """
        Make the Hardware class Gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # This page has the following layout:
        # +-----+-------------------+-------------------+
        # |  B  |      L. TOP       |      R. TOP       |
        # |  U  |                   |                   |
        # |  T  |                   |                   |
        # |  T  +-------------------+-------------------+
        # |  O  |     L. BOTTOM     |     R. BOTTOM     |
        # |  N  |                   |                   |
        # |  S  |                   |                   |
        # +-----+-------------------+-------------------+
        #                                        buttons -----+--> Gtk.HBox
        #                                                     |
        # RAMSTKFrame ---+--> Gtk.VPaned ---+--> Gtk.HPaned --+
        #                |                  |
        # RAMSTKFrame ---+                  |
        #                                   |
        # RAMSTKFrame ---+--> Gtk.VPaned ---+
        #                |
        # RAMSTKFrame ---+

        # Make the buttons.
        super().make_toolbuttons(
            icons=['calculate'],
            tooltips=[
                _("Calculate the currently selected Hardware item."),
            ],
            callbacks=[self._do_request_calculate_hardware])

        _hpaned = Gtk.HPaned()
        self.pack_start(_hpaned, True, True, 0)

        # Make the left side of the page.
        _vpn_left = Gtk.VPaned()
        _hpaned.pack1(_vpn_left, True, True)

        # Top left quadrant.
        # TODO: See issue #304.  Only _fixed will be returned in the future.
        # pylint: disable=unused-variable
        (__, __, _fixed) = super().make_ui(start=0, end=10)

        _scrollwindow = RAMSTKScrolledWindow(_fixed)
        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("Reliability Results"))
        _frame.add(_scrollwindow)
        _vpn_left.pack1(_frame, True, True)

        # Bottom left quadrant.  This is just an RAMSTKFrame() and will be the
        # container for component-specific design attributes.
        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("Assessment Model Results"))
        _frame.add(self.scwReliability)
        _vpn_left.pack2(_frame, True, True)

        # Make the right side of the page.
        _vpn_right = Gtk.VPaned()
        _hpaned.pack2(_vpn_right, True, True)

        # Top right quadrant.
        # TODO: See issue #304.  Only _fixed will be returned in the future.
        # pylint: disable=unused-variable
        (__, __, _fixed) = super().make_ui(start=10)

        _scrollwindow = RAMSTKScrolledWindow(_fixed)
        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("Availability Results"))
        _frame.add(_scrollwindow)
        _vpn_right.pack1(_frame, True, True)

        # Bottom right quadrant.  This is just an RAMSTKFrame() and will be the
        # container for component-specific design attributes.
        _scrollwindow = RAMSTKScrolledWindow(self.wvwOperatingStress)
        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("Stress Results"))
        _frame.add(_scrollwindow)
        _vpn_right.pack2(_frame, True, True)

        # Set the tab label.
        _label = RAMSTKLabel(_("Assessment\nResults"))
        _label.do_set_properties(
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_("Displays reliability, maintainability, and "
                      "availability assessment results for the selected "
                      "{0:s}.").format(self._module))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def __set_properties(self) -> None:
        """
        Set the properties of the Assessment Results Work View and widgets.

        :return: None
        :rtype: None
        """
        self.__set_availability_properties()
        self.__set_miscellaneous_properties()
        self.__set_reliability_properties()

    def __set_availability_properties(self) -> None:
        """
        Set the properties of widgets displaying availability results.

        :return: None
        :rtype: None
        """
        _idx = 0
        for _widget in self._lst_widgets[10:12]:
            _widget.do_set_properties(
                width=125,
                editable=False,
                bold=True,
                tooltip=[
                    _("Displays the logistics availability for the selected "
                      "hardware item."),
                    _("Displays the mission availability for the selected "
                      "hardware item."),
                    _("Displays the variance on the logistics availability "
                      "for the selected hardware item."),
                    _("Displays the variance on the mission availability for "
                      "the selected hardware item."),
                    _("Displays the mean time to repair (MTTR) for the "
                      "selected hardware item."),
                    _("Displays the mean corrective maintenance time (MCMT) "
                      "for the selected hardware item."),
                    _("Displays the mean preventive maintenance time (MPMT) "
                      "for the selected hardware item."),
                    _("Displays the mean maintenance time (MMT) for the "
                      "selected hardware item.  This includes preventive and "
                      "corrective maintenance.")
                ][_idx])
            _idx += 1

    def __set_miscellaneous_properties(self) -> None:
        """
        Set the properties of widgets displaying miscellaneous results.

        :return: None
        :rtype: None
        """
        _idx = 0
        for _widget in self._lst_widgets[12:]:
            _widget.do_set_properties(
                width=125,
                editable=False,
                bold=True,
                tooltip=[
                    _("Displays the total cost of the selected hardware "
                      "item."),
                    _("Displays the cost per failure of the selected "
                      "hardware item."),
                    _("Displays the failure cost per operating hour for the "
                      "selected hardware item."),
                    _("Displays the total part count for the selected "
                      "hardware item.")
                ][_idx])
            _idx += 1

    def __set_reliability_properties(self) -> None:
        """
        Set the properties of widgets displaying reliability results.

        :return: None
        :rtype: None
        """
        _idx = 0
        for _widget in self._lst_widgets[0:10]:
            _widget.do_set_properties(
                width=125,
                editable=False,
                bold=True,
                tooltip=[
                    _("Displays the active failure intensity for the selected "
                      "hardware item."),
                    _("Displays the dormant failure intensity for the "
                      "selected hardware item."),
                    _("Displays the software failure intensity for the "
                      "selected hardware item."),
                    _("Displays the logistics failure intensity for the "
                      "selected hardware item.  This is the sum of the "
                      "active, dormant, and software hazard rates."),
                    _("Displays the mission failure intensity for the "
                      "selected hardware item."),
                    _("Displays the percentage of the system failure "
                      "intensity the selected hardware item represents."),
                    _("Displays the logistics mean time between failure "
                      "(MTBF) for the selected hardware item."),
                    _("Displays the mission mean time between failure (MTBF) "
                      "for the selected hardware item."),
                    _("Displays the logistics reliability for the selected "
                      "hardware item."),
                    _("Displays the mission reliability for the selected "
                      "hardware item."),
                    _("Displays the variance on the active failure intensity "
                      "for the selected hardware item."),
                    _("Displays the variance on the dormant failure intensity "
                      "for the selected hardware item."),
                    _("Displays the variance on the logistics failure "
                      "intensity for the selected hardware item."),
                    _("Displays the variance on the mission failure "
                      "intensity for the selected hardware item."),
                    _("Displays the variance on the logistics MTBF for the "
                      "selected hardware item."),
                    _("Displays the variance on the mission MTBF for the "
                      "selected hardware item."),
                    _("Displays the variance on the logistics reliability "
                      "for the selected hardware item."),
                    _("Displays the variance on the mission reliability for "
                      "the selected hardware item.")
                ][_idx])
            _idx += 1

    def _do_clear_page(self) -> None:
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        # TODO: See issue #310.
        self.txtTotalCost.set_text('')
        self.txtCostFailure.set_text('')
        self.txtCostHour.set_text('')
        self.txtPartCount.set_text('')
        self.txtActiveHt.set_text('')
        self.txtActiveHtVar.set_text('')
        self.txtDormantHt.set_text('')
        self.txtDormantHtVar.set_text('')
        self.txtSoftwareHt.set_text('')
        self.txtPercentHt.set_text('')
        self.txtLogisticsAt.set_text('')
        self.txtLogisticsAtVar.set_text('')
        self.txtLogisticsHt.set_text('')
        self.txtLogisticsHtVar.set_text('')
        self.txtLogisticsMTBF.set_text('')
        self.txtLogisticsMTBFVar.set_text('')
        self.txtLogisticsRt.set_text('')
        self.txtLogisticsRtVar.set_text('')
        self.txtMissionAt.set_text('')
        self.txtMissionAtVar.set_text('')
        self.txtMissionHt.set_text('')
        self.txtMissionHtVar.set_text('')
        self.txtMissionMTBF.set_text('')
        self.txtMissionMTBFVar.set_text('')
        self.txtMissionRt.set_text('')
        self.txtMissionRtVar.set_text('')

        # Clear the component-specific Gtk.ScrolledWindow()s.
        for _child in self.scwReliability.get_children():
            self.scwReliability.remove(_child)

        for _child in self.scwStress.get_children():
            self.scwStress.remove(_child)

    def _do_load_page(self, dmtree: treelib.Tree) -> None:
        """
        Load the assessment result page widgets with attribute values.

        :param dict attributes: a dict of attribute key:value pairs for the
            selected Hardware.
        :return: None
        :rtype: None
        """
        if self._record_id == -1:
            return

        attributes = _do_get_attributes(dmtree, self._record_id)

        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        # Operating stress information is only applicable to components,
        # not assemblies so we only show the information for components.
        if attributes['category_id'] > 0:
            self._do_load_component_results(attributes)
        else:
            self.wvwOperatingStress.hide()

        self._do_load_availability_results(attributes)
        self._do_load_hazard_rate_results(attributes)
        self._do_load_miscellaneous_results(attributes)
        self._do_load_mtbf_results(attributes)
        self._do_load_reliability_results(attributes)

        # Send the PyPubSub message to let the component-specific widgets know
        # they can load.
        pub.sendMessage('loaded_hardware_results', attributes=attributes)

    def _do_load_component_results(self, attributes: Dict[str, Any]) -> None:
        """
        Load the results specific to hardware components.

        :param dict attributes:
        :return: None
        :rtype: None
        """
        # Retrieve the appropriate component-specific work views.
        try:
            _component_ar = self._dic_assessment_results[
                attributes['category_id']]
        except KeyError as _error:
            _component_ar = None
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        # If there are already a component-specific work view object,
        # remove them.  Otherwise move along; these aren't the droids we're
        # looking for.
        try:
            self.scwReliability.remove(self.scwReliability.get_child())
        except TypeError as _error:
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        if _component_ar is not None:
            self.scwReliability.add(_component_ar)
            self.scwReliability.show_all()

        self.wvwOperatingStress.show_all()

    def _do_load_availability_results(self,
                                      attributes: Dict[str, Any]) -> None:
        """
        Load the widgets used to display availability results attributes.

        :param dict attributes: the dict of attributes for the hardware item
            being loaded.
        :return: None
        :rtype: None
        """
        # TODO: See issue #310.
        self.txtLogisticsAt.set_text(
            str(self.fmt.format(attributes['availability_logistics'])))
        self.txtLogisticsAtVar.set_text(
            str(self.fmt.format(attributes['avail_log_variance'])))
        self.txtMissionAt.set_text(
            str(self.fmt.format(attributes['availability_mission'])))
        self.txtMissionAtVar.set_text(
            str(self.fmt.format(attributes['avail_mis_variance'])))

    def _do_load_hazard_rate_results(self, attributes: Dict[str, Any]) -> None:
        """
        Load the widgets used to display hazard rate results attributes.

        :param dict attributes: the dict of attributes for the hardware item
            being loaded.
        :return: None
        :rtype: None
        """
        # TODO: See issue #310.
        self.txtActiveHt.set_text(
            str(self.fmt.format(attributes['hazard_rate_active'])))
        self.txtActiveHtVar.set_text(
            str(self.fmt.format(attributes['hr_active_variance'])))
        self.txtDormantHt.set_text(
            str(self.fmt.format(attributes['hazard_rate_dormant'])))
        self.txtDormantHtVar.set_text(
            str(self.fmt.format(attributes['hr_dormant_variance'])))
        self.txtSoftwareHt.set_text(
            str(self.fmt.format(attributes['hazard_rate_software'])))

        self.txtPercentHt.set_text(
            str(self.fmt.format(attributes['hazard_rate_percent'])))

        self.txtLogisticsHt.set_text(
            str(self.fmt.format(attributes['hazard_rate_logistics'])))
        self.txtLogisticsHtVar.set_text(
            str(self.fmt.format(attributes['hr_logistics_variance'])))
        self.txtMissionHt.set_text(
            str(self.fmt.format(attributes['hazard_rate_mission'])))
        self.txtMissionHtVar.set_text(
            str(self.fmt.format(attributes['hr_mission_variance'])))

    def _do_load_miscellaneous_results(self,
                                       attributes: Dict[str, Any]) -> None:
        """
        Load the widgets used to display miscellaneous results attributes.

        :param dict attributes: the dict of attributes for the hardware item
            being loaded.
        :return: None
        :rtype: None
        """
        # TODO: See issue #310.
        self.txtTotalCost.set_text(
            str(locale.currency(attributes['total_cost'])))
        self.txtCostFailure.set_text(
            str(locale.currency(attributes['cost_failure'])))
        self.txtCostHour.set_text(str(locale.currency(
            attributes['cost_hour'])))
        self.txtPartCount.set_text(
            str('{0:d}'.format(attributes['total_part_count'])))

    def _do_load_mtbf_results(self, attributes: Dict[str, Any]) -> None:
        """
        Load widgets used to display MTBF results attributes.

        :param dict attributes: the dict of attributes for the hardware item
            being loaded.
        :return: None
        :rtype: None
        """
        # TODO: See issue #310.
        self.txtLogisticsMTBF.set_text(
            str(self.fmt.format(attributes['mtbf_logistics'])))
        self.txtLogisticsMTBFVar.set_text(
            str(self.fmt.format(attributes['mtbf_logistics_variance'])))
        self.txtMissionMTBF.set_text(
            str(self.fmt.format(attributes['mtbf_mission'])))
        self.txtMissionMTBFVar.set_text(
            str(self.fmt.format(attributes['mtbf_mission_variance'])))

    def _do_load_reliability_results(self, attributes: Dict[str, Any]) -> None:
        """
        Load the widgets used to display reliability results attributes.

        :param dict attributes: the dict of attributes for the hardware item
            being loaded.
        :return: None
        :rtype: None
        """
        # TODO: See issue #310.
        self.txtLogisticsRt.set_text(
            str(self.fmt.format(attributes['reliability_logistics'])))
        self.txtLogisticsRtVar.set_text(
            str(self.fmt.format(attributes['reliability_log_variance'])))
        self.txtMissionRt.set_text(
            str(self.fmt.format(attributes['reliability_mission'])))
        self.txtMissionRtVar.set_text(
            str(self.fmt.format(attributes['reliability_miss_variance'])))

    def _do_request_calculate_hardware(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to calculate the selected Hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        pub.sendMessage('request_calculate_hardware', node_id=self._record_id)

    def _do_request_hardware_tree(self, attributes: Dict[str, Any]) -> None:
        """
        Request the Hardware module treelib Tree().

        :param attributes:
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']

        pub.sendMessage('request_get_hardware_tree')

    # TODO: Make this public per convention 303.3.  Do this for all workviews.
    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to save the currently selected Hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor_busy()
        pub.sendMessage('request_update_hardware', node_id=self._record_id)

    # TODO: Make this public per convention 303.3.  Do this for all workviews.
    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to save all Hardware items.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor_busy()
        pub.sendMessage('request_update_all_hardware')
