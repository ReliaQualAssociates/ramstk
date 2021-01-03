# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.workview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Hardware Work View."""

# Standard Library Imports
import locale
from typing import Any, Dict, List, Tuple

# Third Party Imports
from pubsub import pub
# noinspection PyPackageRequirements
from sortedcontainers import SortedDict

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTK_ACTIVE_ENVIRONMENTS, RAMSTK_DORMANT_ENVIRONMENTS,
    RAMSTK_HR_DISTRIBUTIONS, RAMSTK_HR_MODELS,
    RAMSTK_HR_TYPES, RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton, RAMSTKComboBox, RAMSTKEntry, RAMSTKPanel,
    RAMSTKScrolledWindow, RAMSTKTextView, RAMSTKWorkView
)

# RAMSTK Local Imports
from . import ATTRIBUTE_KEYS
from .components import (
    capacitor, connection, inductor, integrated_circuit, meter,
    miscellaneous, relay, resistor, semiconductor, switch
)
from .components.panels import RAMSTKStressInputPanel, RAMSTKStressResultPanel


class GeneralDataPanel(RAMSTKPanel):
    """Panel to display general data about the selected Hardware item."""
    def __init__(self) -> None:
        """Initialize an instance of the Hardware General Date panel."""
        super().__init__()

        # Initialize private dictionary instance attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = ATTRIBUTE_KEYS

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
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
            _("LCN:"),
            "",
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("General Information")

        # Initialize public dictionary instance attributes.
        self.dicSubcategories: Dict[int, Dict[int, str]] = {}

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.chkRepairable: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Repairable"))

        self.cmbCategory: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbSubcategory: RAMSTKComboBox = RAMSTKComboBox()

        self.txtAltPartNum: RAMSTKEntry = RAMSTKEntry()
        self.txtCompRefDes: RAMSTKEntry = RAMSTKEntry()
        self.txtDescription: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())
        self.txtFigureNumber: RAMSTKEntry = RAMSTKEntry()
        self.txtLCN: RAMSTKEntry = RAMSTKEntry()
        self.txtName: RAMSTKEntry = RAMSTKEntry()
        self.txtPageNumber: RAMSTKEntry = RAMSTKEntry()
        self.txtPartNumber: RAMSTKEntry = RAMSTKEntry()
        self.txtRefDes: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecification: RAMSTKEntry = RAMSTKEntry()

        self._dic_attribute_updater = {
            'category_id': [self.cmbCategory.do_update, 'changed', 32],
            'subcategory_id': [self.cmbSubcategory.do_update, 'changed', 33],
            'alt_part_number': [self.txtAltPartNum.do_update, 'changed', 2],
            'comp_ref_des': [self.txtCompRefDes.do_update, 'changed', 4],
            'description': [self.txtDescription.do_update, 'changed', 8],
            'figure_number': [self.txtFigureNumber.do_update, 'changed', 10],
            'lcn': [self.txtLCN.do_update, 'changed', 11],
            'name': [self.txtName.do_update, 'changed', 15],
            'page_number': [self.txtPageNumber.do_update, 'changed', 17],
            'part_number': [self.txtPartNumber.do_update, 'changed', 20],
            'ref_des': [self.txtRefDes.do_update, 'changed', 22],
            'specification_number':
            [self.txtSpecification.do_update, 'changed', 25],
        }

        self._lst_widgets = [
            self.txtRefDes,
            self.txtCompRefDes,
            self.txtName,
            self.txtDescription,
            self.txtPartNumber,
            self.txtAltPartNum,
            self.cmbCategory,
            self.cmbSubcategory,
            self.txtSpecification,
            self.txtPageNumber,
            self.txtFigureNumber,
            self.txtLCN,
            self.chkRepairable,
        ]

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_fixed()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().on_edit, 'mvw_editing_hardware')

        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_panel, 'selected_hardware')
        pub.subscribe(self._do_load_panel, 'succeed_create_comp_ref_des')
        pub.subscribe(self._do_load_subcategories, 'changed_category')

    def do_load_categories(self, category: Dict[int, str]) -> None:
        """Load the category RAMSTKComboBox().

        :param category: the dictionary of hardware categories to load.
        :return: None
        :rtype: None
        """
        _model = self.cmbCategory.get_model()
        _model.clear()

        _categories = []
        # pylint: disable=unused-variable
        for __, _key in enumerate(category):
            _categories.append([category[_key]])
        self.cmbCategory.do_load_combo(entries=_categories)

    def _do_clear_panel(self) -> None:
        """Clear the contents of the panel widgets.

        :return: None
        :rtype: None
        """
        # ----- CHECKBUTTONS
        self.chkRepairable.do_update(False, signal='toggled')

        # ----- COMBOBOXES
        self.cmbCategory.do_update(0, signal='changed')
        self.cmbSubcategory.do_update(0, signal='changed')

        # ----- ENTRIES
        self.txtAltPartNum.do_update('', signal='changed')
        self.txtCompRefDes.do_update('', signal='changed')
        self.txtDescription.do_update('', signal='changed')
        self.txtFigureNumber.do_update('', signal='changed')
        self.txtLCN.do_update('', signal='changed')
        self.txtName.do_update('', signal='changed')
        self.txtPageNumber.do_update('', signal='changed')
        self.txtPartNumber.do_update('', signal='changed')
        self.txtRefDes.do_update('', signal='changed')
        self.txtSpecification.do_update('', signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load data into the Hardware General Data page widgets.

        :param attributes: the Hardware attributes to load into the
            Work View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']

        # Disable the category RAMSTKCombo() if the hardware item is not a
        # part.
        if attributes['part'] == 1:
            self.cmbCategory.set_sensitive(True)
            self.cmbSubcategory.set_sensitive(True)

            self.cmbCategory.do_update(int(attributes['category_id']),
                                       signal='changed')

            self._do_load_subcategories(int(attributes['category_id']))
            self.cmbSubcategory.do_update(int(attributes['subcategory_id']),
                                          signal='changed')

        else:
            self.cmbCategory.set_sensitive(False)
            self.cmbCategory.do_update(int(attributes['category_id']),
                                       signal='changed')
            self.cmbSubcategory.set_sensitive(False)
            self.cmbSubcategory.do_update(int(attributes['subcategory_id']),
                                          signal='changed')

        self.chkRepairable.do_update(int(attributes['repairable']),
                                     signal='toggled')
        self.txtAltPartNum.do_update(str(attributes['alt_part_number']),
                                     signal='changed')
        self.txtCompRefDes.do_update(str(attributes['comp_ref_des']),
                                     signal='changed')
        self.txtDescription.do_update(str(attributes['description']),
                                      signal='changed')
        self.txtFigureNumber.do_update(str(attributes['figure_number']),
                                       signal='changed')
        self.txtLCN.do_update(str(attributes['lcn']), signal='changed')
        self.txtName.do_update(str(attributes['name']), signal='changed')
        self.txtPageNumber.do_update(str(attributes['page_number']),
                                     signal='changed')
        self.txtPartNumber.do_update(str(attributes['part_number']),
                                     signal='changed')
        self.txtRefDes.do_update(str(attributes['ref_des']), signal='changed')
        self.txtSpecification.do_update(str(
            attributes['specification_number']),
                                        signal='changed')  # noqa

    def _do_load_subcategories(self, category_id: int) -> None:
        """Load the subcategory RAMSTKComboBox().

        :param category_id: the ID of the selected category.
        :return: None
        """
        _model = self.cmbSubcategory.get_model()
        _model.clear()

        if category_id > 0:
            _subcategories = SortedDict(self.dicSubcategories[category_id])
            _subcategory = []
            for _key in _subcategories:
                _subcategory.append([_subcategories[_key]])
            self.cmbSubcategory.do_load_combo(entries=_subcategory,
                                              signal='changed')

    @staticmethod
    def _request_load_component(combo: RAMSTKComboBox) -> None:
        """Request to load the component widgets.

        :param combo: the RAMSTKComboBox() that called this method.
        :return: None
        """
        pub.sendMessage('changed_subcategory',
                        subcategory_id=combo.get_active())

    def _request_load_subcategories(self, combo: RAMSTKComboBox) -> None:
        """Request to have the subcategory RAMSTKComboBox() loaded.

        :param combo: the RAMSTKComboBox() that called this method.
        :return: None
        """
        self._do_load_subcategories(category_id=combo.get_active())

    def __do_set_callbacks(self) -> None:
        """Set the callback methods and functions for the panel widgets.

        :return: None
        :rtype: None
        """
        # ----- CHECKBUTTONS
        self.chkRepairable.dic_handler_id['toggled'] = (
            self.chkRepairable.connect('toggled',
                                       super().on_toggled, 24,
                                       'wvw_editing_hardware'))

        # ----- COMBOBOXES
        self.cmbCategory.dic_handler_id['changed'] = self.cmbCategory.connect(
            'changed',
            super().on_changed_combo, 32, 'wvw_editing_hardware')
        self.cmbCategory.connect('changed', self._request_load_subcategories)
        self.cmbSubcategory.dic_handler_id[
            'changed'] = self.cmbSubcategory.connect('changed',
                                                     super().on_changed_combo,
                                                     33,
                                                     'wvw_editing_hardware')
        self.cmbSubcategory.connect('changed', self._request_load_component)

        # ----- ENTRIES
        self.txtAltPartNum.dic_handler_id[
            'changed'] = self.txtAltPartNum.connect('changed',
                                                    super().on_changed_entry,
                                                    2, 'wvw_editing_hardware')
        self.txtCompRefDes.dic_handler_id[
            'changed'] = self.txtCompRefDes.connect('changed',
                                                    super().on_changed_entry,
                                                    4, 'wvw_editing_hardware')
        _buffer: Gtk.TextBuffer = self.txtDescription.do_get_buffer()
        self.txtDescription.dic_handler_id['changed'] = _buffer.connect(
            'changed',
            super().on_changed_textview, 8, 'wvw_editing_hardware',
            self.txtDescription)
        self.txtFigureNumber.dic_handler_id[
            'changed'] = self.txtFigureNumber.connect('changed',
                                                      super().on_changed_entry,
                                                      10,
                                                      'wvw_editing_hardware')
        self.txtLCN.dic_handler_id['changed'] = self.txtLCN.connect(
            'changed',
            super().on_changed_entry, 11, 'wvw_editing_hardware')
        self.txtName.dic_handler_id['changed'] = self.txtName.connect(
            'changed',
            super().on_changed_entry, 15, 'wvw_editing_hardware')
        self.txtPageNumber.dic_handler_id[
            'changed'] = self.txtPageNumber.connect('changed',
                                                    super().on_changed_entry,
                                                    17, 'wvw_editing_hardware')
        self.txtPartNumber.dic_handler_id[
            'changed'] = self.txtPartNumber.connect('changed',
                                                    super().on_changed_entry,
                                                    20, 'wvw_editing_hardware')
        self.txtRefDes.dic_handler_id['changed'] = self.txtRefDes.connect(
            'changed',
            super().on_changed_entry, 22, 'wvw_editing_hardware')
        self.txtSpecification.dic_handler_id[
            'changed'] = self.txtSpecification.connect(
                'changed',
                super().on_changed_entry, 25, 'wvw_editing_hardware')

    def __do_set_properties(self) -> None:
        """Set the properties of the panel widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        self.chkRepairable.do_set_properties(
            tooltip=_("Indicates whether or not the selected hardware item is "
                      "repairable."))

        self.txtAltPartNum.do_set_properties(
            tooltip=_("The alternate part number (if any) of the selected "
                      "hardware item."))
        self.txtCompRefDes.do_set_properties(
            tooltip=_("The composite reference designator of the selected "
                      "hardware item."))
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
        self.txtPageNumber.do_set_properties(
            tooltip=_("The page number in the governing specification for the "
                      "selected hardware item."))
        self.txtPartNumber.do_set_properties(
            tooltip=_("The part number of the selected hardware item."))
        self.txtRefDes.do_set_properties(tooltip=_(
            "The reference designator of the selected hardware item."))
        self.txtSpecification.do_set_properties(
            tooltip=_("The specification (if any) governing the selected "
                      "hardware item."))


class LogisticsPanel(RAMSTKPanel):
    """Panel to display general data about the selected Hardware task."""
    def __init__(self) -> None:
        """Initialize an instance of the Hardware Task Description panel."""
        super().__init__()

        # Initialize private dict instance attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = ATTRIBUTE_KEYS

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
            _("Manufacturer:"),
            _("CAGE Code:"),
            _("NSN:"),
            _("Year Made:"),
            _("Quantity:"),
            _("Unit Cost:"),
            _("Cost Method:"),
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("Logistics Information")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.cmbCostType: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbManufacturer: RAMSTKComboBox = RAMSTKComboBox(simple=False)

        self.txtCAGECode: RAMSTKEntry = RAMSTKEntry()
        self.txtCost: RAMSTKEntry = RAMSTKEntry()
        self.txtNSN: RAMSTKEntry = RAMSTKEntry()
        self.txtQuantity: RAMSTKEntry = RAMSTKEntry()
        self.txtYearMade: RAMSTKEntry = RAMSTKEntry()

        self._dic_attribute_updater = {
            'cage_code': [self.txtCAGECode.do_update, 'changed', 3],
            'cost_type_id': [self.cmbCostType.do_update, 'changed', 30],
            'manufacturer_id': [self.cmbManufacturer.do_update, 'changed', 13],
            'cost': [self.txtCost.do_update, 'changed', 5],
            'nsn': [self.txtNSN.do_update, 'changed', 16],
            'quantity': [self.txtQuantity.do_update, 'changed', 21],
            'year_of_manufacture': [self.txtYearMade.do_update, 'changed', 29],
        }

        self._lst_widgets = [
            self.cmbManufacturer,
            self.txtCAGECode,
            self.txtNSN,
            self.txtYearMade,
            self.txtQuantity,
            self.txtCost,
            self.cmbCostType,
        ]

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_fixed()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.on_edit, 'mvw_editing_hardware')

        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_panel, 'selected_hardware')
        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    def do_load_cost_types(self) -> None:
        """Load the category RAMSTKComboBox().

        :return: None
        """
        self.cmbCostType.do_load_combo([['Assessed'], ['Specified']])

    def do_load_manufacturers(
            self, manufacturers: Dict[int, Tuple[str, str, str]]) -> None:
        """Load the manufacturer RAMSTKComboBox().

        :param manufacturers: the dictionary with manufacturer information.
            The key is the index from the database table.  The value is a tuple
            with the manufacturer's name, office location, and CAGE code.  An
            example might be:

            ('Sprague', 'New Hampshire', '13606')

        :return: None
        """
        _manufacturer = []
        for _key in manufacturers:
            _manufacturer.append(manufacturers[_key])
        self.cmbManufacturer.do_load_combo(entries=_manufacturer, simple=False)

    def _do_clear_panel(self) -> None:
        """Clear the contents of the panel widgets.

        :return: None
        :rtype: None
        """
        # ----- COMBOBOXES
        self.cmbCostType.do_update(0, signal='changed')
        self.cmbManufacturer.do_update(0, signal='changed')

        # ----- ENTRIES
        self.txtCAGECode.do_update('', signal='changed')
        self.txtCost.do_update('', signal='changed')
        self.txtNSN.do_update('', signal='changed')
        self.txtQuantity.do_update('', signal='changed')
        self.txtYearMade.do_update('', signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load data into the Hardware General Data page widgets.

        :param attributes: the Hardware attributes to load into the
            Work View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']

        # ----- COMBOBOXES
        self.cmbCostType.do_update(int(attributes['cost_type_id']),
                                   signal='changed')
        self.cmbManufacturer.do_update(int(attributes['manufacturer_id']),
                                       signal='changed')

        # ----- ENTRIES
        self.txtCAGECode.do_update(str(attributes['cage_code']),
                                   signal='changed')
        self.txtCost.do_update(str(locale.currency(attributes['cost'])),
                               signal='changed')
        self.txtNSN.do_update(str(attributes['nsn']), signal='changed')
        self.txtQuantity.do_update(str(attributes['quantity']),
                                   signal='changed')
        self.txtYearMade.do_update(str(attributes['year_of_manufacture']),
                                   signal='changed')

    def _do_load_cage_code(self, combo: RAMSTKComboBox) -> None:
        """Load the CAGE code whenever the manufacturer is changed.

        :param combo: the RAMSTKComboBox() that called this method.
        :return: None
        :rtype: None
        """
        _model = combo.get_model()
        _row = combo.get_active_iter()
        self.txtCAGECode.do_update(str(_model.get(_row, 2)[0]),
                                   signal='changed')
        pub.sendMessage('wvw_editing_hardware',
                        node_id=[self._record_id, -1],
                        package={'cage_code': str(_model.get(_row, 2)[0])})

    def __do_set_callbacks(self) -> None:
        """Set the callback methods and functions for the panel widgets.

        :return: None
        :rtype: None
        """
        # ----- COMBOBOXES
        self.cmbCostType.dic_handler_id['changed'] = self.cmbCostType.connect(
            'changed',
            super().on_changed_combo, 30, 'wvw_editing_hardware')
        self.cmbManufacturer.dic_handler_id[
            'changed'] = self.cmbManufacturer.connect('changed',
                                                      super().on_changed_combo,
                                                      13,
                                                      'wvw_editing_hardware')
        self.cmbManufacturer.connect('changed', self._do_load_cage_code)

        # ----- ENTRIES
        self.txtCAGECode.dic_handler_id['changed'] = self.txtCAGECode.connect(
            'changed',
            super().on_changed_entry, 3, 'wvw_editing_hardware')
        self.txtCost.dic_handler_id['changed'] = self.txtCost.connect(
            'changed',
            super().on_changed_entry, 5, 'wvw_editing_hardware')
        self.txtNSN.dic_handler_id['changed'] = self.txtNSN.connect(
            'changed',
            super().on_changed_entry, 16, 'wvw_editing_hardware')
        self.txtQuantity.dic_handler_id['changed'] = self.txtQuantity.connect(
            'changed',
            super().on_changed_entry, 21, 'wvw_editing_hardware')
        self.txtYearMade.dic_handler_id['changed'] = self.txtYearMade.connect(
            'changed',
            super().on_changed_entry, 29, 'wvw_editing_hardware')

    def __do_set_properties(self) -> None:
        """Set the properties of the panel widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        # ----- ENTRIES
        self.txtCAGECode.do_set_properties(
            tooltip=_("The Commercial and Government Entity (CAGE) Code of "
                      "the selected hardware item."))
        self.txtCost.do_set_properties(
            width=100,
            tooltip=_("The unit cost of the selected hardware item."))
        self.txtNSN.do_set_properties(
            tooltip=_("The National Stock Number (NSN) of the selected "
                      "hardware item."))
        self.txtQuantity.do_set_properties(
            width=50,
            tooltip=_(
                "The number of the selected hardware items in the design."))
        self.txtYearMade.do_set_properties(
            width=100,
            tooltip=_(
                "The year the the selected hardware item was manufactured."))


class MiscellaneousPanel(RAMSTKPanel):
    """Panel to display general data about the selected Hardware task."""
    def __init__(self) -> None:
        """Initialize an instance of the Hardware Task Description panel."""
        super().__init__()

        # Initialize private dict instance attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = ATTRIBUTE_KEYS

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
            _("Attachments:"),
            _("Remarks:"),
            "",
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("Miscellaneous Information")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.chkTagged: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Tagged Part"))
        self.txtAttachments: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())
        self.txtRemarks: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())

        self._dic_attribute_updater = {
            'attachments': [self.txtAttachments.do_update, 'changed', 31],
            'remarks': [self.txtRemarks.do_update, 'changed', 23],
        }
        self._lst_widgets = [
            self.txtAttachments,
            self.txtRemarks,
            self.chkTagged,
        ]

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_fixed()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.on_edit, 'mvw_editing_hardware')

        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_panel, 'selected_hardware')
        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    def _do_clear_panel(self) -> None:
        """Clear the contents of the panel widgets.

        :return: None
        :rtype: None
        """
        # ----- CHECKBUTTONS
        self.chkTagged.do_update(False, signal='toggled')

        # ----- ENTRIES
        self.txtAttachments.do_update('', signal='changed')
        self.txtRemarks.do_update('', signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load data into the Hardware General Data page widgets.

        :param attributes: the Hardware attributes to load into the
            Work View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']

        # ----- CHECKBUTTONS
        self.chkTagged.do_update(int(attributes['tagged_part']),
                                 signal='toggled')

        # ----- ENTRIES
        self.txtAttachments.do_update(str(attributes['attachments']),
                                      signal='changed')
        self.txtRemarks.do_update(str(attributes['remarks']), signal='changed')

    def __do_set_callbacks(self) -> None:
        """Set the callback methods and functions for the panel widgets.

        :return: None
        :rtype: None
        """
        # ----- CHECKBUTTONS
        self.chkTagged.dic_handler_id['toggled'] = (self.chkTagged.connect(
            'toggled',
            super().on_toggled, 26, 'wvw_editing_hardware'))

        # ----- ENTRIES
        _buffer: Gtk.TextBuffer = self.txtAttachments.do_get_buffer()
        self.txtAttachments.dic_handler_id['changed'] = _buffer.connect(
            'changed',
            super().on_changed_textview, 31, 'wvw_editing_hardware',
            self.txtAttachments)
        _buffer = self.txtRemarks.do_get_buffer()
        self.txtRemarks.dic_handler_id['changed'] = _buffer.connect(
            'changed',
            super().on_changed_textview, 23, 'wvw_editing_hardware',
            self.txtRemarks)

    def __do_set_properties(self) -> None:
        """Set the properties of the panel widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        # ----- ENTRIES
        self.txtAttachments.do_set_properties(
            width=600,
            tooltip=_("Hyperlinks to any documents associated with the "
                      "selected hardware item."))
        self.txtRemarks.do_set_properties(
            height=150,
            width=600,
            tooltip=_("Enter any remarks associated with the selected "
                      "hardware item."))


class AssessmentInputPanel(RAMSTKPanel):
    """Panel to display hazard rate inputs about the selected Hardware item."""
    def __init__(self) -> None:
        """Initialize an instance of the Assessment Input panel."""
        super().__init__()

        # Initialize private dict instance attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
            0: ['failure_distribution_id', 'integer'],
            1: ['hazard_rate_type_id', 'integer'],
            2: ['hazard_rate_method_id', 'integer'],
            3: ['add_adj_factor', 'float'],
            4: ['scale_parameter', 'float'],
            5: ['shape_parameter', 'float'],
            6: ['location_parameter', 'float'],
            7: ['mult_adj_factor', 'float'],
            8: ['hazard_rate_specified', 'float'],
            9: ['hr_specified_variance', 'float'],
            10: ['mtbf_specified', 'float'],
            11: ['mtbf_specified_variance', 'float'],
        }

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
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
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("Assessment Inputs")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.cmbFailureDist: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbHRMethod: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbHRType: RAMSTKComboBox = RAMSTKComboBox()

        self.txtAddAdjFactor: RAMSTKEntry = RAMSTKEntry()
        self.txtFailLocation: RAMSTKEntry = RAMSTKEntry()
        self.txtFailScale: RAMSTKEntry = RAMSTKEntry()
        self.txtFailShape: RAMSTKEntry = RAMSTKEntry()
        self.txtMultAdjFactor: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecifiedHt: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecifiedHtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecifiedMTBF: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecifiedMTBFVar: RAMSTKEntry = RAMSTKEntry()

        self._dic_attribute_updater = {
            'add_adj_factor': [self.txtAddAdjFactor.do_update, 'changed', 3],
            'scale_parameter': [self.txtFailScale.do_update, 'changed', 4],
            'shape_parameter': [self.txtFailShape.do_update, 'changed', 5],
            'location_parameter':
            [self.txtFailLocation.do_update, 'changed', 6],
            'mult_adj_factor': [self.txtMultAdjFactor.do_update, 'changed', 7],
            'hazard_rate_specified':
            [self.txtSpecifiedHt.do_update, 'changed', 8],
            'hr_specified_variance':
            [self.txtSpecifiedHtVar.do_update, 'changed', 9],
            'mtbf_specified': [self.txtSpecifiedMTBF.do_update, 'changed', 10],
            'mtbf_spec_variance':
            [self.txtSpecifiedMTBFVar.do_update, 'changed', 11],
        }
        self._lst_widgets = [
            self.cmbHRType,
            self.cmbHRMethod,
            self.txtSpecifiedHt,
            self.txtSpecifiedHtVar,
            self.txtSpecifiedMTBF,
            self.txtSpecifiedMTBFVar,
            self.cmbFailureDist,
            self.txtFailScale,
            self.txtFailShape,
            self.txtFailLocation,
            self.txtAddAdjFactor,
            self.txtMultAdjFactor,
        ]

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_fixed()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    def do_load_hr_distributions(self, distributions: List[str]) -> None:
        """Load the hazard rate distribution RAMSTKComboBox().

        :param distributions: the list of s-distribution names RAMSTK
            currently supports.
        :return: None
        """
        self.cmbFailureDist.do_load_combo(entries=distributions)

    def do_load_hr_methods(self, methods: List[str]) -> None:
        """Load the hazard rate method RAMSTKComboBox().

        The hazard rate methods are:

            * MIL-HDBK-217F Parts Count
            * MIL-HDBK-217F Parts Stress
            * NSWC-11

        :param methods: the list of methods for assessing the hazard rate.
        :return: None
        """
        self.cmbHRMethod.do_load_combo(entries=methods)

    def do_load_hr_types(self, hr_types: List[str]) -> None:
        """Load the hazard rate type RAMSTKComboBox().

        The hazard rate types are:

            * Assessed
            * Defined, Hazard Rate
            * Defined, MTBF
            * Defined, Distribution

        :param hr_types: the types (or ways) of establishing the hazard rate
            for a hardware item.
        :return: None
        """
        self.cmbHRType.do_load_combo(entries=hr_types)

    def _do_clear_panel(self) -> None:
        """Clear the contents of the panel widgets.

        :return: None
        :rtype: None
        """
        # ----- CHECKBUTTONS
        self.cmbFailureDist.do_update(0, signal='changed')
        self.cmbHRMethod.do_update(0, signal='changed')
        self.cmbHRType.do_update(0, signal='changed')

        # ----- ENTRIES
        self.txtAddAdjFactor.do_update('', signal='changed')
        self.txtFailScale.do_update('', signal='changed')
        self.txtFailShape.do_update('', signal='changed')
        self.txtFailLocation.do_update('', signal='changed')
        self.txtMultAdjFactor.do_update('', signal='changed')
        self.txtSpecifiedHt.do_update('', signal='changed')
        self.txtSpecifiedHtVar.do_update('', signal='changed')
        self.txtSpecifiedMTBF.do_update('', signal='changed')
        self.txtSpecifiedMTBFVar.do_update('', signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load data into the Hardware General Data page widgets.

        :param attributes: the Hardware attributes to load into the
            Work View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']

        # ----- COMBOBOXES
        self.cmbFailureDist.do_update(int(
            attributes['failure_distribution_id']),
                                      signal='changed')  # noqa
        self.cmbHRMethod.do_update(int(attributes['hazard_rate_method_id']),
                                   signal='changed')
        self.cmbHRType.do_update(int(attributes['hazard_rate_type_id']),
                                 signal='changed')

        # ----- ENTRIES
        self.txtAddAdjFactor.do_update(self.fmt.format(
            attributes['add_adj_factor']),
                                       signal='changed')  # noqa
        self.txtFailScale.do_update(self.fmt.format(
            attributes['scale_parameter']),
                                    signal='changed')  # noqa
        self.txtFailShape.do_update(self.fmt.format(
            attributes['shape_parameter']),
                                    signal='changed')  # noqa
        self.txtFailLocation.do_update(self.fmt.format(
            attributes['location_parameter']),
                                       signal='changed')  # noqa
        self.txtMultAdjFactor.do_update(self.fmt.format(
            attributes['mult_adj_factor']),
                                        signal='changed')  # noqa
        self.txtSpecifiedHt.do_update(self.fmt.format(
            attributes['hazard_rate_specified']),
                                      signal='changed')  # noqa
        self.txtSpecifiedHtVar.do_update(self.fmt.format(
            attributes['hr_specified_variance']),
                                         signal='changed')  # noqa
        self.txtSpecifiedMTBF.do_update(self.fmt.format(
            attributes['mtbf_specified']),
                                        signal='changed')  # noqa
        self.txtSpecifiedMTBFVar.do_update(self.fmt.format(
            attributes['mtbf_specified_variance']),
                                           signal='changed')  # noqa

        self._do_set_sensitive(type_id=attributes['hazard_rate_type_id'])

    def _do_set_sensitive_assessed(self, type_id: int) -> None:
        """Set the widgets used in handbook assessments sensitive.

        :param type_id: the hazard rate type (source).
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

    def _do_set_sensitive_specified_ht(self, type_id: int) -> None:
        """Set the widgets used for specifying a hazard rate sensitive.

        :param type_id: the hazard rate type (source).
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

    def _do_set_sensitive_specified_mtbf(self, type_id: int) -> None:
        """Set the widgets used for specifying an MTBF sensitive.

        :param type_id: the hazard rate type (source).
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

    def _do_set_sensitive_specified_distribution(self, type_id: int) -> None:
        """Set widgets used for specifying a failure distribution sensitive.

        :param type_id: the hazard rate type (source).
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
        """Set certain widgets sensitive or insensitive.

        This method will set the sensitivity of various widgets depending on
        the hazard rate assessment type selected.

        :return: None
        :rtype: None
        """
        _type_id = kwargs['type_id']

        self._do_set_sensitive_assessed(_type_id)
        self._do_set_sensitive_specified_ht(_type_id)
        self._do_set_sensitive_specified_mtbf(_type_id)
        self._do_set_sensitive_specified_distribution(_type_id)

    def __do_set_callbacks(self) -> None:
        """Set the callback methods and functions for the panel widgets.

        :return: None
        :rtype: None
        """
        # ----- COMBOBOXES
        self.cmbFailureDist.dic_handler_id[
            'changed'] = self.cmbFailureDist.connect('changed',
                                                     super().on_changed_combo,
                                                     0, 'wvw_editing_hardware')
        self.cmbHRType.dic_handler_id['changed'] = self.cmbHRType.connect(
            'changed',
            super().on_changed_combo, 1, 'wvw_editing_hardware')
        self.cmbHRMethod.dic_handler_id['changed'] = self.cmbHRMethod.connect(
            'changed',
            super().on_changed_combo, 2, 'wvw_editing_hardware')

        # ----- ENTRIES
        self.txtAddAdjFactor.dic_handler_id[
            'changed'] = self.txtAddAdjFactor.connect('changed',
                                                      super().on_changed_entry,
                                                      3,
                                                      'wvw_editing_hardware')
        self.txtFailScale.dic_handler_id[
            'changed'] = self.txtFailScale.connect('changed',
                                                   super().on_changed_entry, 4,
                                                   'wvw_editing_hardware')
        self.txtFailShape.dic_handler_id[
            'changed'] = self.txtFailShape.connect('changed',
                                                   super().on_changed_entry, 5,
                                                   'wvw_editing_hardware')
        self.txtFailLocation.dic_handler_id[
            'changed'] = self.txtFailLocation.connect('changed',
                                                      super().on_changed_entry,
                                                      6,
                                                      'wvw_editing_hardware')
        self.txtMultAdjFactor.dic_handler_id[
            'changed'] = self.txtMultAdjFactor.connect(
                'changed',
                super().on_changed_entry, 7, 'wvw_editing_hardware')
        self.txtSpecifiedHt.dic_handler_id[
            'changed'] = self.txtSpecifiedHt.connect('changed',
                                                     super().on_changed_entry,
                                                     8, 'wvw_editing_hardware')
        self.txtSpecifiedHtVar.dic_handler_id[
            'changed'] = self.txtSpecifiedHtVar.connect(
                'changed',
                super().on_changed_entry, 9, 'wvw_editing_hardware')
        self.txtSpecifiedMTBF.dic_handler_id[
            'changed'] = self.txtSpecifiedMTBF.connect(
                'changed',
                super().on_changed_entry, 10, 'wvw_editing_hardware')
        self.txtSpecifiedMTBFVar.dic_handler_id[
            'changed'] = self.txtSpecifiedMTBFVar.connect(
                'changed',
                super().on_changed_entry, 11, 'wvw_editing_hardware')

    def __do_set_properties(self) -> None:
        """Set the properties of the panel widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        # _____ COMBOBOXES
        self.cmbFailureDist.do_set_properties(tooltip=_(
            "The statistical failure distribution of the selected hardware "
            "item."),
                                              width=200)  # noqa
        self.cmbHRMethod.do_set_properties(tooltip=_(
            "The assessment method to use for the selected hardware item."),
                                           width=200)  # noqa
        self.cmbHRType.do_set_properties(tooltip=_(
            "The type of reliability assessment for the selected hardware "
            "item."),
                                         width=200)  # noqa

        # ----- ENTRIES
        self.txtAddAdjFactor.do_set_properties(tooltip=_(
            "An adjustment factor to add to the assessed hazard rate or "
            "MTBF."),
                                               width=125)  # noqa
        self.txtFailLocation.do_set_properties(tooltip=_(
            "The location parameter of the statistical failure distribution."),
                                               width=125)  # noqa
        self.txtFailScale.do_set_properties(tooltip=_(
            "The scale parameter of the statistical failure distribution."),
                                            width=125)  # noqa
        self.txtFailShape.do_set_properties(tooltip=_(
            "The shape parameter of the statistical failure distribution."),
                                            width=125)  # noqa
        self.txtMultAdjFactor.do_set_properties(tooltip=_(
            "An adjustment factor to multiply the assessed hazard rate or "
            "MTBF."),
                                                width=125)  # noqa
        self.txtSpecifiedHt.do_set_properties(tooltip=_("The stated hazard "
                                                        "rate."),
                                              width=125)  # noqa
        self.txtSpecifiedHtVar.do_set_properties(tooltip=_("The variance of "
                                                           "the stated "
                                                           "hazard rate."),
                                                 width=125)  # noqa
        self.txtSpecifiedMTBF.do_set_properties(tooltip=_("The stated mean "
                                                          "time between "
                                                          "failure ("
                                                          "MTBF)."),
                                                width=125)  # noqa
        self.txtSpecifiedMTBFVar.do_set_properties(tooltip=_(
            "The variance of the stated mean time between failure (MTBF)."),
                                                   width=125)  # noqa


class EnvironmentalInputPanel(RAMSTKPanel):
    """Panel to display environmental data about the selected Hardware item."""
    def __init__(self) -> None:
        """Initialize an instance of the Environmental Input panel."""
        super().__init__()

        # Initialize private dict instance attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
            0: ['environment_active_id', 'integer'],
            1: ['environment_dormant_id', 'integer'],
            2: ['temperature_active', 'float'],
            3: ['temperature_dormant', 'float'],
            4: ['duty_cycle', 'float'],
            5: ['mission_time', 'float'],
        }

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
            _("Active Environment:"),
            _("Active Temperature (\u00B0C):"),
            _("Dormant Environment:"),
            _("Dormant Temperature (\u00B0C):"),
            _("Mission Time:"),
            _("Duty Cycle:"),
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("Environmental Inputs")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.cmbActiveEnviron: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbDormantEnviron: RAMSTKComboBox = RAMSTKComboBox()

        self.scwDesignRatings: RAMSTKScrolledWindow = RAMSTKScrolledWindow(
            None)

        self.txtActiveTemp: RAMSTKEntry = RAMSTKEntry()
        self.txtDormantTemp: RAMSTKEntry = RAMSTKEntry()
        self.txtDutyCycle: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionTime: RAMSTKEntry = RAMSTKEntry()

        self._dic_attribute_updater = {
            'temperature_active': [self.txtActiveTemp.do_update, 'changed', 2],
            'temperature_dormant':
            [self.txtDormantTemp.do_update, 'changed', 3],
            'duty_cycle': [self.txtDutyCycle.do_update, 'changed', 4],
            'mission_time': [self.txtMissionTime.do_update, 'changed', 5],
        }
        self._lst_widgets = [
            self.cmbActiveEnviron,
            self.txtActiveTemp,
            self.cmbDormantEnviron,
            self.txtDormantTemp,
            self.txtMissionTime,
            self.txtDutyCycle,
        ]

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_fixed()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    def do_load_environment_active(self, environments: List[str]) -> None:
        """Load the active environments RAMSTKComboBox().

        :param environments: the list of active environments.
        :return: None
        """
        self.cmbActiveEnviron.do_load_combo(entries=environments)

    def do_load_environment_dormant(self, environments: List[str]) -> None:
        """Load the dormant environments RAMSTKComboBox().

        :param environments: the list of dormant environments.
        :return: None
        """
        self.cmbDormantEnviron.do_load_combo(entries=environments)

    def _do_clear_panel(self) -> None:
        """Clear the contents of the panel widgets.

        :return: None
        :rtype: None
        """
        # ----- COMBOBOXES
        self.cmbActiveEnviron.do_update(0, signal='changed')
        self.cmbDormantEnviron.do_update(0, signal='changed')

        # ----- ENTRIES
        self.txtActiveTemp.do_update('', signal='changed')
        self.txtDormantTemp.do_update('', signal='changed')
        self.txtDutyCycle.do_update('', signal='changed')
        self.txtMissionTime.do_update('', signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load data into the Hardware General Data page widgets.

        :param attributes: the Hardware attributes to load into the
            Work View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']

        # ----- COMBOBOXES
        self.cmbActiveEnviron.do_update(int(
            attributes['environment_active_id']),
                                        signal='changed')  # noqa
        self.cmbDormantEnviron.do_update(int(
            attributes['environment_dormant_id']),
                                         signal='changed')  # noqa

        # ----- ENTRIES
        self.txtActiveTemp.do_update(self.fmt.format(
            attributes['temperature_active']),
                                     signal='changed')  # noqa
        self.txtDormantTemp.do_update(self.fmt.format(
            attributes['temperature_dormant']),
                                      signal='changed')  # noqa
        self.txtDutyCycle.do_update(self.fmt.format(attributes['duty_cycle']),
                                    signal='changed')
        self.txtMissionTime.do_update(self.fmt.format(
            attributes['mission_time']),
                                      signal='changed')  # noqa

    def __do_set_callbacks(self) -> None:
        """Set the callback methods and functions for the panel widgets.

        :return: None
        :rtype: None
        """
        # ----- COMBOBOXES
        self.cmbActiveEnviron.dic_handler_id[
            'changed'] = self.cmbActiveEnviron.connect(
                'changed',
                super().on_changed_combo, 0, 'wvw_editing_hardware')
        self.cmbDormantEnviron.dic_handler_id[
            'changed'] = self.cmbDormantEnviron.connect(
                'changed',
                super().on_changed_combo, 1, 'wvw_editing_hardware')

        # ----- ENTRIES
        self.txtActiveTemp.dic_handler_id[
            'changed'] = self.txtActiveTemp.connect('changed',
                                                    super().on_changed_entry,
                                                    2, 'wvw_editing_hardware')
        self.txtDormantTemp.dic_handler_id[
            'changed'] = self.txtDormantTemp.connect('changed',
                                                     super().on_changed_entry,
                                                     3, 'wvw_editing_hardware')
        self.txtDutyCycle.dic_handler_id[
            'changed'] = self.txtDutyCycle.connect('changed',
                                                   super().on_changed_entry, 4,
                                                   'wvw_editing_hardware')
        self.txtMissionTime.dic_handler_id[
            'changed'] = self.txtMissionTime.connect('changed',
                                                     super().on_changed_entry,
                                                     5, 'wvw_editing_hardware')

    def __do_set_properties(self) -> None:
        """Set the properties of the panel widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        # _____ COMBOBOXES
        self.cmbActiveEnviron.do_set_properties(
            tooltip=_("The operating environment for the hardware item."),
            width=200)
        self.cmbDormantEnviron.do_set_properties(
            tooltip=_("The storage environment for the hardware item."),
            width=200)

        # ----- ENTRIES
        self.txtActiveTemp.do_set_properties(
            tooltip=_("The ambient temperature in the operating environment."),
            width=125)
        self.txtDormantTemp.do_set_properties(
            tooltip=_("The ambient temperature in the storage environment."),
            width=125)
        self.txtMissionTime.do_set_properties(
            tooltip=_("The mission time of the selected hardware item."),
            width=125)
        self.txtDutyCycle.do_set_properties(
            tooltip=_("The duty cycle of the selected hardware item."),
            width=125)


class ReliabilityResultsPanel(RAMSTKPanel):
    """Panel to display reliability results for the selected Hardware item."""
    def __init__(self) -> None:
        """Initialize an instance of the Reliability Results panel."""
        super().__init__()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
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
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("Reliability Results")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.txtActiveHt: RAMSTKEntry = RAMSTKEntry()
        self.txtActiveHtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtDormantHt: RAMSTKEntry = RAMSTKEntry()
        self.txtDormantHtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsHt: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsHtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsMTBF: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsMTBFVar: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsRt: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsRtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionHt: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionHtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionMTBF: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionMTBFVar: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionRt: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionRtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtPercentHt: RAMSTKEntry = RAMSTKEntry()
        self.txtSoftwareHt: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets = [
            self.txtActiveHt,
            self.txtDormantHt,
            self.txtSoftwareHt,
            self.txtLogisticsHt,
            self.txtMissionHt,
            self.txtPercentHt,
            self.txtLogisticsMTBF,
            self.txtMissionMTBF,
            self.txtLogisticsRt,
            self.txtMissionRt,
        ]

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_fixed()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    def _do_clear_panel(self) -> None:
        """Clear the contents of the panel widgets.

        :return: None
        :rtype: None
        """
        # ----- ENTRIES
        self.txtActiveHt.do_update('', signal='changed')
        self.txtActiveHtVar.do_update('', signal='changed')
        self.txtDormantHt.do_update('', signal='changed')
        self.txtDormantHtVar.do_update('', signal='changed')
        self.txtSoftwareHt.do_update('', signal='changed')
        self.txtPercentHt.do_update('', signal='changed')
        self.txtLogisticsHt.do_update('', signal='changed')
        self.txtLogisticsHtVar.do_update('', signal='changed')
        self.txtLogisticsMTBF.do_update('', signal='changed')
        self.txtLogisticsMTBFVar.do_update('', signal='changed')
        self.txtLogisticsRt.do_update('', signal='changed')
        self.txtLogisticsRtVar.do_update('', signal='changed')
        self.txtMissionHt.do_update('', signal='changed')
        self.txtMissionHtVar.do_update('', signal='changed')
        self.txtMissionMTBF.do_update('', signal='changed')
        self.txtMissionMTBFVar.do_update('', signal='changed')
        self.txtMissionRt.do_update('', signal='changed')
        self.txtMissionRtVar.do_update('', signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load data into the Hardware General Data page widgets.

        :param attributes: the Hardware attributes to load into the
            Work View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']

        # ----- ENTRIES
        self.txtActiveHt.do_update(str(
            self.fmt.format(attributes['hazard_rate_active'])),
                                   signal='changed')  # noqa
        self.txtActiveHtVar.do_update(str(
            self.fmt.format(attributes['hr_active_variance'])),
                                      signal='changed')  # noqa
        self.txtDormantHt.do_update(str(
            self.fmt.format(attributes['hazard_rate_dormant'])),
                                    signal='changed')  # noqa
        self.txtDormantHtVar.do_update(str(
            self.fmt.format(attributes['hr_dormant_variance'])),
                                       signal='changed')  # noqa
        self.txtLogisticsHt.do_update(str(
            self.fmt.format(attributes['hazard_rate_logistics'])),
                                      signal='changed')  # noqa
        self.txtLogisticsHtVar.do_update(str(
            self.fmt.format(attributes['hr_logistics_variance'])),
                                         signal='changed')  # noqa
        self.txtLogisticsMTBF.do_update(str(
            self.fmt.format(attributes['mtbf_logistics'])),
                                        signal='changed')  # noqa
        self.txtLogisticsMTBFVar.do_update(str(
            self.fmt.format(attributes['mtbf_logistics_variance'])),
                                           signal='changed')  # noqa
        self.txtLogisticsRt.do_update(str(
            self.fmt.format(attributes['reliability_logistics'])),
                                      signal='changed')  # noqa
        self.txtLogisticsRtVar.do_update(str(
            self.fmt.format(attributes['reliability_log_variance'])),
                                         signal='changed')  # noqa
        self.txtMissionHt.do_update(str(
            self.fmt.format(attributes['hazard_rate_mission'])),
                                    signal='changed')  # noqa
        self.txtMissionHtVar.do_update(str(
            self.fmt.format(attributes['hr_mission_variance'])),
                                       signal='changed')  # noqa
        self.txtMissionMTBF.do_update(str(
            self.fmt.format(attributes['mtbf_mission'])),
                                      signal='changed')  # noqa
        self.txtMissionMTBFVar.do_update(str(
            self.fmt.format(attributes['mtbf_mission_variance'])),
                                         signal='changed')  # noqa
        self.txtMissionRt.do_update(str(
            self.fmt.format(attributes['reliability_mission'])),
                                    signal='changed')  # noqa
        self.txtMissionRtVar.do_update(str(
            self.fmt.format(attributes['reliability_miss_variance'])),
                                       signal='changed')  # noqa
        self.txtPercentHt.do_update(str(
            self.fmt.format(attributes['hazard_rate_percent'])),
                                    signal='changed')  # noqa
        self.txtSoftwareHt.do_update(str(
            self.fmt.format(attributes['hazard_rate_software'])),
                                     signal='changed')  # noqa

    def __do_set_properties(self) -> None:
        """Set the properties of the panel widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        # ----- ENTRIES
        self.txtActiveHt.do_set_properties(tooltip=_(
            "Displays the active failure intensity for the selected "
            "hardware item."),
                                           width=125)  # noqa
        self.txtActiveHtVar.do_set_properties(tooltip=_(
            "Displays the variance on the active failure intensity "
            "for the selected hardware item."),
                                              width=125)  # noqa
        self.txtDormantHt.do_set_properties(tooltip=_(
            "Displays the dormant failure intensity for the "
            "selected hardware item."),
                                            width=125)  # noqa
        self.txtDormantHtVar.do_set_properties(tooltip=_(
            "Displays the variance on the dormant failure intensity "
            "for the selected hardware item."),
                                               width=125)  # noqa
        self.txtLogisticsHt.do_set_properties(tooltip=_(
            "Displays the logistics failure intensity for the "
            "selected hardware item.  This is the sum of the "
            "active, dormant, and software hazard rates."),
                                              width=125)  # noqa
        self.txtLogisticsHtVar.do_set_properties(tooltip=_(
            "Displays the variance on the logistics failure "
            "intensity for the selected hardware item."),
                                                 width=125)  # noqa
        self.txtLogisticsMTBF.do_set_properties(tooltip=_(
            "Displays the logistics mean time between failure "
            "(MTBF) for the selected hardware item."),
                                                width=125)  # noqa
        self.txtLogisticsMTBFVar.do_set_properties(tooltip=_(
            "Displays the variance on the logistics MTBF for the "
            "selected hardware item."),
                                                   width=125)  # noqa
        self.txtLogisticsRt.do_set_properties(tooltip=_(
            "Displays the logistics reliability for the selected "
            "hardware item."),
                                              width=125)  # noqa
        self.txtLogisticsRtVar.do_set_properties(tooltip=_(
            "Displays the variance on the logistics reliability "
            "for the selected hardware item."),
                                                 width=125)  # noqa
        self.txtMissionHt.do_set_properties(tooltip=_(
            "Displays the mission failure intensity for the "
            "selected hardware item."),
                                            width=125)  # noqa
        self.txtMissionHtVar.do_set_properties(tooltip=_(
            "Displays the variance on the mission failure "
            "intensity for the selected hardware item."),
                                               width=125)  # noqa
        self.txtMissionMTBF.do_set_properties(tooltip=_(
            "Displays the mission mean time between failure (MTBF) "
            "for the selected hardware item."),
                                              width=125)  # noqa
        self.txtMissionMTBFVar.do_set_properties(tooltip=_(
            "Displays the variance on the mission MTBF for the "
            "selected hardware item."),
                                                 width=125)  # noqa
        self.txtMissionRt.do_set_properties(tooltip=_(
            "Displays the mission reliability for the selected "
            "hardware item."),
                                            width=125)  # noqa
        self.txtMissionRtVar.do_set_properties(tooltip=_(
            "Displays the variance on the mission reliability for "
            "the selected hardware item."),
                                               width=125)  # noqa
        self.txtPercentHt.do_set_properties(tooltip=_(
            "Displays the percentage of the system failure "
            "intensity the selected hardware item represents."),
                                            width=125)  # noqa
        self.txtSoftwareHt.do_set_properties(tooltip=_(
            "Displays the software failure intensity for the "
            "selected hardware item."),
                                             width=125)  # noqa


class AvailabilityResultsPanel(RAMSTKPanel):
    """Panel to display availability results for the selected Hardware item."""
    def __init__(self) -> None:
        """Initialize an instance of the Availability Results panel."""
        super().__init__()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
            _("Logistics Availability [A(t)]:"),
            _("Mission A(t):"),
            _("Total Cost:"),
            _("Cost/Failure:"),
            _("Cost/Hour:"),
            _("Total # of Parts:"),
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("Availability Results")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.txtCostFailure: RAMSTKEntry = RAMSTKEntry()
        self.txtCostHour: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsAt: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsAtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtMCMT: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionAt: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionAtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtMMT: RAMSTKEntry = RAMSTKEntry()
        self.txtMPMT: RAMSTKEntry = RAMSTKEntry()
        self.txtMTTR: RAMSTKEntry = RAMSTKEntry()
        self.txtPartCount: RAMSTKEntry = RAMSTKEntry()
        self.txtTotalCost: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets = [
            self.txtLogisticsAt,
            self.txtMissionAt,
            self.txtTotalCost,
            self.txtCostFailure,
            self.txtCostHour,
            self.txtPartCount,
        ]

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_fixed()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.on_edit, 'mvw_editing_hardware')

        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    def _do_clear_panel(self) -> None:
        """Clear the contents of the panel widgets.

        :return: None
        :rtype: None
        """
        # ----- ENTRIES
        self.txtTotalCost.do_update('', signal='changed')
        self.txtCostFailure.do_update('', signal='changed')
        self.txtCostHour.do_update('', signal='changed')
        self.txtPartCount.do_update('', signal='changed')
        self.txtLogisticsAt.do_update('', signal='changed')
        self.txtLogisticsAtVar.do_update('', signal='changed')
        self.txtMissionAt.do_update('', signal='changed')
        self.txtMissionAtVar.do_update('', signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load data into the Hardware General Data page widgets.

        :param attributes: the Hardware attributes to load into the
            Work View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']

        # ----- ENTRIES
        self.txtLogisticsAt.do_update(str(
            self.fmt.format(attributes['availability_logistics'])),
                                      signal='changed')  # noqa
        self.txtLogisticsAtVar.do_update(str(
            self.fmt.format(attributes['avail_log_variance'])),
                                         signal='changed')  # noqa
        self.txtMissionAt.do_update(str(
            self.fmt.format(attributes['availability_mission'])),
                                    signal='changed')  # noqa
        self.txtMissionAtVar.do_update(str(
            self.fmt.format(attributes['avail_mis_variance'])),
                                       signal='changed')  # noqa
        self.txtTotalCost.do_update(str(
            locale.currency(attributes['total_cost'])),
                                    signal='changed')  # noqa
        self.txtCostFailure.do_update(str(
            locale.currency(attributes['cost_failure'])),
                                      signal='changed')  # noqa
        self.txtCostHour.do_update(str(locale.currency(
            attributes['cost_hour'])),
                                   signal='changed')  # noqa
        self.txtPartCount.do_update(str('{0:d}'.format(
            attributes['total_part_count'])),
                                    signal='changed')  # noqa

    def __do_set_properties(self) -> None:
        """Set the properties of the panel widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        # ----- ENTRIES
        self.txtCostFailure.do_set_properties(tooltip=_(
            "Displays the cost per failure of the selected "
            "hardware item."),
                                              width=125)  # noqa
        self.txtCostHour.do_set_properties(tooltip=_(
            "Displays the failure cost per operating hour for the "
            "selected hardware item."),
                                           width=125)  # noqa
        self.txtLogisticsAt.do_set_properties(tooltip=_(
            "Displays the logistics availability for the selected "
            "hardware item."),
                                              width=125)  # noqa
        self.txtLogisticsAtVar.do_set_properties(tooltip=_(
            "Displays the variance on the logistics availability "
            "for the selected hardware item."),
                                                 width=125)  # noqa
        self.txtMCMT.do_set_properties(tooltip=_(
            "Displays the mean corrective maintenance time (MCMT) "
            "for the selected hardware item."),
                                       width=125)  # noqa
        self.txtMissionAt.do_set_properties(tooltip=_(
            "Displays the mission availability for the selected "
            "hardware item."),
                                            width=125)  # noqa
        self.txtMissionAtVar.do_set_properties(tooltip=_(
            "Displays the variance on the mission availability for "
            "the selected hardware item."),
                                               width=125)  # noqa
        self.txtMMT.do_set_properties(tooltip=_(
            "Displays the mean maintenance time (MMT) for the "
            "selected hardware item.  This includes preventive and "
            "corrective maintenance."),
                                      width=125)  # noqa
        self.txtMPMT.do_set_properties(tooltip=_(
            "Displays the mean preventive maintenance time (MPMT) "
            "for the selected hardware item."),
                                       width=125)  # noqa
        self.txtMTTR.do_set_properties(tooltip=_(
            "Displays the mean time to repair (MTTR) for the "
            "selected hardware item."),
                                       width=125)  # noqa
        self.txtPartCount.do_set_properties(tooltip=_(
            "Displays the total part count for the selected "
            "hardware item."),
                                            width=125)  # noqa
        self.txtTotalCost.do_set_properties(tooltip=_(
            "Displays the total cost of the selected hardware "
            "item."),
                                            width=125)  # noqa


class GeneralData(RAMSTKWorkView):
    """Display general Hardware attribute data in the RAMSTK Work Book.

    The Hardware Work View displays all the general data attributes for the
    selected Hardware.  The attributes of a Hardware General Data Work View
    are:

    :cvar _module: the name of the module.

    :ivar _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """
    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = 'hardware'
    _tablabel: str = _("General\nData")
    _tabtooltip: str = _(
        "Displays general information for the selected Hardware")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the Hardware Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration:
            :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.
        self._dic_icons['comp_ref_des'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/rollup.png')

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self._pnlGeneralData: RAMSTKPanel = GeneralDataPanel()
        self._pnlLogistics: RAMSTKPanel = LogisticsPanel()
        self._pnlMiscellaneous: RAMSTKPanel = MiscellaneousPanel()

        self._lst_callbacks = [
            self._do_request_make_comp_ref_des,
            super().do_request_update,
            super().do_request_update_all,
        ]
        self._lst_icons = [
            'comp_ref_des',
            'save',
            'save-all',
        ]
        self._lst_mnu_labels = [
            _("Comp. Ref. Des."),
            _("Save"),
            _("Save All"),
        ]
        self._lst_tooltips = [
            _("Creates the composite reference designator for the "
              "selected hardware item."),
            _("Save changes to the currently selected hardware item."),
            _("Save changes to all hardware items."),
        ]

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, 'selected_hardware')

    def _do_request_make_comp_ref_des(self, __button: Gtk.ToolButton) -> None:
        """Send request to create the composite reference designator.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_make_comp_ref_des', node_id=self._record_id)
        super().do_set_cursor_active()

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the work stream module's record ID and, if any, parent ID.

        :param attributes: the attributes dict for the selected work stream
            module item.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._parent_id = attributes['parent_id']

    def __make_ui(self) -> None:
        """Build the user interface for the Hardware General Data tab.

        :return: None
        :rtype: None
        """
        _hpaned, _vpaned_right = super().do_make_layout_lrr()

        self._pnlGeneralData.fmt = self.fmt
        self._pnlGeneralData.dicSubcategories = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_SUBCATEGORIES)
        self._pnlGeneralData.do_load_categories(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_CATEGORIES)
        _hpaned.pack1(self._pnlGeneralData, True, True)

        self._pnlLogistics.do_load_cost_types()
        self._pnlLogistics.do_load_manufacturers(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_MANUFACTURERS)
        _vpaned_right.pack1(self._pnlLogistics, True, True)

        _vpaned_right.pack2(self._pnlMiscellaneous, True, True)

        self.show_all()


class AssessmentInputs(RAMSTKWorkView):
    """Display Hardware assessment input attribute data.

    The Hardware assessment input view displays all the assessment inputs for
    the selected Hardware item.  This includes, currently, inputs for
    MIL-HDBK-217FN2 and NSWC-11.  The attributes of a Hardware assessment
    input view are:

    :cvar list _lst_labels: the text to use for the assessment input widget
        labels.
    :cvar str _module: the name of the module.

    :ivar dict _dic_assessment_input: dictionary of component-specific
        AssessmentInputs classes.
    :ivar int _hardware_id: the ID of the Hardware item currently being
        displayed.
    :ivar int _hazard_rate_method_id: the ID of the hazard rate method used for
        Hardware item.
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
    # Define private dict attributes.

    # Define private list attributes.
    _lst_title: List[str] = [_("Operating Stresses")]

    # Define private scalar class attributes.
    _module: str = 'hardware'
    _tablabel: str = _("Assessment\nInputs")
    _tabtooltip: str = _("Displays reliability assessment inputs "
                         "for the selected hardware item.")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize an instance of the Hardware assessment input view.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.
        self._dic_component_panels: Dict[int, RAMSTKPanel] = {
            1: integrated_circuit.AssessmentInputPanel(),
            2: semiconductor.AssessmentInputPanel(),
            3: resistor.AssessmentInputPanel(),
            4: capacitor.AssessmentInputPanel(),
            5: inductor.AssessmentInputPanel(),
            6: relay.AssessmentInputPanel(),
            7: switch.AssessmentInputPanel(),
            8: connection.AssessmentInputPanel(),
            9: meter.AssessmentInputPanel(),
            10: miscellaneous.AssessmentInputPanel(),
        }

        # Initialize private list attributes.
        self._lst_callbacks = [
            self._do_request_calculate,
            super().do_request_update,
            super().do_request_update_all,
        ]
        self._lst_icons = [
            'calculate',
            'save',
            'save-all',
        ]
        self._lst_tooltips = [
            _("Calculate the currently selected hardware item and all of "
              "it's children."),
            _("Save changes to the currently selected hardware item."),
            _("Save changes to all hardware items."),
        ]

        # Initialize private scalar attributes.
        self._pnlAssessmentInput: RAMSTKPanel = AssessmentInputPanel()
        self._pnlEnvironmentalInput: RAMSTKPanel = EnvironmentalInputPanel()
        self._pnlStressInput: RAMSTKStressInputPanel = RAMSTKStressInputPanel()

        # We need to carry these as an attribute for this view because the
        # lower part of each is dynamically loaded with the component panels.
        self._vpnLeft: Gtk.VPaned = Gtk.VPaned()
        self._vpnRight: Gtk.VPaned = Gtk.VPaned()

        self._hazard_rate_method_id: int = 0
        self._subcategory_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_set_cursor_active,
                      'succeed_calculate_hardware')

        pub.subscribe(self._do_pack_component_panel, 'selected_hardware')
        pub.subscribe(self._do_set_record_id, 'selected_hardware')

    def _do_pack_component_panel(self, attributes: Dict[str, Any]) -> None:
        """Pack panel used to display component-specific input attributes.

        :param attributes: dict containing the attributes of the hardware
            item being loaded.
        :return: None
        :rtype: None
        """
        # If there was a component selected, hide it's widgets.  We get an
        # attribute error if no parts have been selected in the current
        # session.
        if self._vpnLeft.get_child2() is not None:
            self._vpnLeft.remove(self._vpnLeft.get_child2())

        # Retrieve the appropriate component-specific view.
        if attributes['category_id'] > 0:
            _panel: RAMSTKPanel = self._dic_component_panels[
                attributes['category_id']]
            _panel.fmt = self.fmt
            self._vpnLeft.pack2(_panel, True, True)
            self.show_all()
        else:
            self._vpnRight.get_child2().hide()

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """Send request to calculate the selected hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        try:
            super().do_set_cursor_busy()
            pub.sendMessage(
                'request_calculate_hardware',
                node_id=self._record_id,
            )
        except KeyError as _error:
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the work stream module's record ID and, if any, parent ID.

        :param attributes: the attributes dict for the selected work stream
            module item.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._parent_id = attributes['parent_id']

    def __make_ui(self) -> None:
        """Build the user interface for the Hardware Assessment Input tab.

        :return: None
        :rtype: None
        """
        self._vpnLeft, self._vpnRight = super().do_make_layout_llrr()

        # Top left quadrant.
        self._pnlAssessmentInput.fmt = self.fmt
        self._pnlAssessmentInput.do_load_hr_distributions(
            RAMSTK_HR_DISTRIBUTIONS)
        self._pnlAssessmentInput.do_load_hr_methods(RAMSTK_HR_MODELS)
        self._pnlAssessmentInput.do_load_hr_types(RAMSTK_HR_TYPES)
        self._vpnLeft.pack1(self._pnlAssessmentInput, True, True)

        # Top right quadrant.
        self._pnlEnvironmentalInput.fmt = self.fmt
        self._pnlEnvironmentalInput.do_load_environment_active(
            RAMSTK_ACTIVE_ENVIRONMENTS)
        self._pnlEnvironmentalInput.do_load_environment_dormant(
            RAMSTK_DORMANT_ENVIRONMENTS)
        self._vpnRight.pack1(self._pnlEnvironmentalInput, True, True)

        # Bottom right quadrant.
        self._pnlStressInput.fmt = self.fmt
        self._vpnRight.pack2(self._pnlStressInput, True, True)

        self.show_all()


class AssessmentResults(RAMSTKWorkView):
    """Display Hardware assessment results data in the RAMSTK Work View.

    The Hardware Assessment Results view displays all the assessment results
    for the selected Hardware.  The attributes of a Hardware Assessment Results
    View are:

    :cvar list _lst_labels: the text to use for the reliability assessment
        results widget labels.
    :cvar str _module: the name of the module.

    :ivar dict _dic_assessment_results: dictionary of component-specific
        AssessmentResults classes.
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

    # Define private list class attributes.
    _lst_title = [_("Assessment Model Results"), _("Stress Results")]

    # Define private scalar class attributes.
    _module: str = 'hardware'
    _tablabel: str = _("Assessment\nResults")
    _tabtooltip: str = _("Displays reliability, maintainability, "
                         "and availability assessment results for "
                         "the selected Hardware item.")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize an instance of the Hardware assessment output view.

        :param configuration: the RAMSTK User Configuration class instance.
        :type configuration: :class:`ramstk.configuration.UserConfiguration`
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.
        self._dic_component_results: Dict[int, RAMSTKPanel] = {
            1: integrated_circuit.AssessmentResultPanel(),
            2: semiconductor.AssessmentResultPanel(),
            3: resistor.AssessmentResultPanel(),
            4: capacitor.AssessmentResultPanel(),
            5: inductor.AssessmentResultPanel(),
            6: relay.AssessmentResultPanel(),
            7: switch.AssessmentResultPanel(),
            8: connection.AssessmentResultPanel(),
            9: meter.AssessmentResultPanel(),
            10: miscellaneous.AssessmentResultPanel(),
        }

        # Initialize private list attributes.
        self._lst_callbacks = [
            self._do_request_calculate,
            super().do_request_update,
            super().do_request_update_all,
        ]
        self._lst_icons = [
            'calculate',
            'save',
            'save-all',
        ]
        self._lst_tooltips = [
            _("Calculate the currently selected Hardware item."),
            _("Save changes to the currently selected Hardware item."),
            _("Save changes to all Hardware items."),
        ]

        # Initialize private scalar attributes.
        self._hazard_rate_method_id: int = 0
        self._subcategory_id: int = 0

        self._pnlAvailabilityResults: RAMSTKPanel = AvailabilityResultsPanel()
        self._pnlReliabilityResults: RAMSTKPanel = ReliabilityResultsPanel()
        self._pnlStressResults: RAMSTKStressResultPanel = \
            RAMSTKStressResultPanel()

        # We need to carry these as an attribute for this view because the
        # lower part of each is dynamically loaded with the component panels.
        self._vpnLeft: Gtk.VPaned = Gtk.VPaned()
        self._vpnRight: Gtk.VPaned = Gtk.VPaned()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_pack_component_panel, 'selected_hardware')
        pub.subscribe(self._do_set_record_id, 'selected_hardware')

    def _do_pack_component_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the results specific to hardware components.

        :param attributes:
        :return: None
        :rtype: None
        """
        # If there was a component selected, hide it's widgets.  We get an
        # attribute error if no parts have been selected in the current
        # session.
        if self._vpnLeft.get_child2() is not None:
            self._vpnLeft.remove(self._vpnLeft.get_child2())

        # Retrieve the appropriate component-specific view.
        if attributes['category_id'] > 0:
            _panel: RAMSTKPanel = self._dic_component_results[
                attributes['category_id']]
            _panel.fmt = self.fmt
            self._vpnLeft.pack2(_panel, True, True)
            self.show_all()
        else:
            self._vpnRight.get_child2().hide()

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """Send request to calculate the selected Hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        try:
            super().do_set_cursor_busy()
            pub.sendMessage(
                'request_calculate_hardware',
                node_id=self._record_id,
            )
        except KeyError as _error:
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the work stream module's record ID and, if any, parent ID.

        :param attributes: the attributes dict for the selected work stream
            module item.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._parent_id = attributes['parent_id']

    def __make_ui(self) -> None:
        """Build the user interface for the Hardware Assessment Results tab.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._vpnLeft, self._vpnRight = super().do_make_layout_llrr()

        # Top left quadrant.
        self._pnlReliabilityResults.fmt = self.fmt
        self._vpnLeft.pack1(self._pnlReliabilityResults, True, True)

        # Top right quadrant.
        self._pnlAvailabilityResults.fmt = self.fmt
        self._vpnRight.pack1(self._pnlAvailabilityResults, True, True)

        # Bottom right quadrant.
        self._pnlStressResults.fmt = self.fmt
        self._vpnRight.pack2(self._pnlStressResults, True, True)

        self.show_all()
