# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.Hardware.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Work View."""

import locale
from datetime import date

# Import third party modules.
from pubsub import pub
from sortedcontainers import SortedDict

# Import other RAMSTK modules.
from ramstk.Configuration import (
    RAMSTK_ACTIVE_ENVIRONMENTS, RAMSTK_DORMANT_ENVIRONMENTS, RAMSTK_HR_TYPES,
    RAMSTK_HR_MODELS, RAMSTK_HR_DISTRIBUTIONS, RAMSTK_COST_TYPES)
from ramstk.Utilities import boolean_to_integer
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _, gtk
from ramstk.gui.gtk.workviews.components import Component
from .WorkView import RAMSTKWorkView
from .components import (
    wvwCapacitorAI, wvwCapacitorAR, wvwConnectionAI, wvwConnectionAR,
    wvwInductorAI, wvwInductorAR, wvwIntegratedCircuitAI,
    wvwIntegratedCircuitAR, wvwMeterAI, wvwMeterAR, wvwMiscellaneousAI,
    wvwMiscellaneousAR, wvwRelayAI, wvwRelayAR, wvwResistorAI, wvwResistorAR,
    wvwSemiconductorAI, wvwSemiconductorAR, wvwSwitchAI, wvwSwitchAR)


class GeneralData(RAMSTKWorkView):
    """
    Display Hardware attribute data in the RAMSTK Work Book.

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
    ],
                   [
                       _(u"Manufacturer:"),
                       _(u"CAGE Code:"),
                       _(u"NSN:"),
                       _(u"Year Made:"),
                       _(u"Quantity:"),
                       _(u"Unit Cost:"),
                       _(u"Cost Method:")
                   ], ["", _(u"Attachments:"),
                       _(u"Remarks:")]]

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the Hardware package.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKWorkView.__init__(self, controller, module='Hardware')

        # Initialize private dictionary attributes.
        self._dic_icons[
            'comp_ref_des'] = controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/rollup.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hardware_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # General data page widgets.

        # General Data page widgets.
        self.chkRepairable = ramstk.RAMSTKCheckButton(
            label=_(u"Repairable"),
            tooltip=_(u"Indicates whether or not the selected hardware item "
                      u"is repairable."))
        self.chkTagged = ramstk.RAMSTKCheckButton(label=_(u"Tagged Part"))

        self.cmbCategory = ramstk.RAMSTKComboBox()
        self.cmbCostType = ramstk.RAMSTKComboBox()
        self.cmbManufacturer = ramstk.RAMSTKComboBox(simple=False)
        self.cmbSubcategory = ramstk.RAMSTKComboBox()

        self.txtAltPartNum = ramstk.RAMSTKEntry(
            tooltip=_(u"The alternate part "
                      u"number (if any) of the "
                      u"selected hardware item."))
        self.txtAttachments = ramstk.RAMSTKTextView(
            gtk.TextBuffer(),
            width=600,
            tooltip=_(u"Hyperlinks to any documents associated with the "
                      u"selected hardware item."))
        self.txtCAGECode = ramstk.RAMSTKEntry(
            tooltip=_(u"The Commerical and "
                      u"Government Entity (CAGE) "
                      u"Code of the selected "
                      u"hardware item."))
        self.txtCompRefDes = ramstk.RAMSTKEntry(
            tooltip=_(u"The composite reference "
                      u"designator of the "
                      u"selected hardware item."))
        self.txtCost = ramstk.RAMSTKEntry(
            width=100,
            tooltip=_(u"The unit cost of the selected hardware item."))
        self.txtDescription = ramstk.RAMSTKTextView(
            gtk.TextBuffer(),
            width=600,
            tooltip=_(u"The description of the selected hardware item."))
        self.txtFigureNumber = ramstk.RAMSTKEntry(
            tooltip=_(u"The figure number in "
                      u"the governing "
                      u"specification for the "
                      u"selected hardware "
                      u"item."))
        self.txtLCN = ramstk.RAMSTKEntry(
            tooltip=_(u"The Logistics Control Number "
                      u"(LCN) of the selected hardware "
                      u"item."))
        self.txtName = ramstk.RAMSTKEntry(
            width=600, tooltip=_(u"The name of the selected hardware item."))
        self.txtNSN = ramstk.RAMSTKEntry(
            tooltip=_(u"The National Stock Number (NSN) of the selected "
                      u"hardware item."))
        self.txtPageNumber = ramstk.RAMSTKEntry(
            tooltip=_(u"The page number in the "
                      u"governing specification "
                      u"for the selected "
                      u"hardware item."))
        self.txtPartNumber = ramstk.RAMSTKEntry(
            tooltip=_(u"The part number of the selected hardware item."))
        self.txtQuantity = ramstk.RAMSTKEntry(
            width=50,
            tooltip=_(
                u"The number of the selected hardware items in the design."))
        self.txtRefDes = ramstk.RAMSTKEntry(
            tooltip=_(
                u"The reference designator of the selected hardware item."))
        self.txtRemarks = ramstk.RAMSTKTextView(
            gtk.TextBuffer(),
            width=600,
            tooltip=_(u"Enter any remarks associated with the selected "
                      u"hardware item."))
        self.txtSpecification = ramstk.RAMSTKEntry(
            tooltip=_(u"The specification (if any) governing the selected "
                      u"hardware item."))
        self.txtYearMade = ramstk.RAMSTKEntry(
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
        self._lst_handler_id.append(
            self.txtAttachments.do_get_buffer().connect(
                'changed', self._on_focus_out, 7))
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
        self.pack_start(self._make_page(), expand=True, fill=True)
        self.show_all()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._do_load_page, 'selected_hardware')
        pub.subscribe(self._do_load_subcategory, 'changed_category')
        pub.subscribe(self._on_edit, 'mvw_editing_hardware')

    def _do_clear_page(self):
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        self.cmbCategory.set_active(0)
        self.cmbSubcategory.handler_block(self._lst_handler_id[5])
        self.cmbSubcategory.set_active(0)
        self.cmbSubcategory.handler_unblock(self._lst_handler_id[5])

        self.chkRepairable.handler_block(self._lst_handler_id[0])
        self.chkRepairable.set_active(False)
        self.chkRepairable.handler_unblock(self._lst_handler_id[0])

        self.chkTagged.handler_block(self._lst_handler_id[1])
        self.chkTagged.set_active(False)
        self.chkTagged.handler_unblock(self._lst_handler_id[1])

        self.cmbCostType.handler_block(self._lst_handler_id[3])
        self.cmbCostType.set_active(0)
        self.cmbCostType.handler_unblock(self._lst_handler_id[3])

        self.cmbManufacturer.handler_block(self._lst_handler_id[4])
        self.cmbManufacturer.set_active(0)
        self.cmbManufacturer.handler_unblock(self._lst_handler_id[4])

        self.txtAltPartNum.handler_block(self._lst_handler_id[6])
        self.txtAltPartNum.set_text('')
        self.txtAltPartNum.handler_unblock(self._lst_handler_id[6])

        _textbuffer = self.txtAttachments.do_get_buffer()
        _textbuffer.handler_block(self._lst_handler_id[7])
        _textbuffer.set_text('')
        _textbuffer.handler_unblock(self._lst_handler_id[7])

        self.txtCAGECode.handler_block(self._lst_handler_id[8])
        self.txtCAGECode.set_text('')
        self.txtCAGECode.handler_unblock(self._lst_handler_id[8])

        self.txtCompRefDes.handler_block(self._lst_handler_id[9])
        self.txtCompRefDes.set_text('')
        self.txtCompRefDes.handler_unblock(self._lst_handler_id[9])

        self.txtCost.handler_block(self._lst_handler_id[10])
        self.txtCost.set_text('')
        self.txtCost.handler_unblock(self._lst_handler_id[10])

        _textbuffer = self.txtDescription.do_get_buffer()
        _textbuffer.handler_block(self._lst_handler_id[11])
        _textbuffer.set_text('')
        _textbuffer.handler_unblock(self._lst_handler_id[11])

        self.txtFigureNumber.handler_block(self._lst_handler_id[12])
        self.txtFigureNumber.set_text('')
        self.txtFigureNumber.handler_unblock(self._lst_handler_id[12])

        self.txtLCN.handler_block(self._lst_handler_id[13])
        self.txtLCN.set_text('')
        self.txtLCN.handler_unblock(self._lst_handler_id[13])

        self.txtName.handler_block(self._lst_handler_id[14])
        self.txtName.set_text('')
        self.txtName.handler_unblock(self._lst_handler_id[14])

        self.txtNSN.handler_block(self._lst_handler_id[15])
        self.txtNSN.set_text('')
        self.txtNSN.handler_unblock(self._lst_handler_id[15])

        self.txtPageNumber.handler_block(self._lst_handler_id[16])
        self.txtPageNumber.set_text('')
        self.txtPageNumber.handler_unblock(self._lst_handler_id[16])

        self.txtPartNumber.handler_block(self._lst_handler_id[17])
        self.txtPartNumber.set_text('')
        self.txtPartNumber.handler_unblock(self._lst_handler_id[17])

        self.txtQuantity.handler_block(self._lst_handler_id[18])
        self.txtQuantity.set_text('')
        self.txtQuantity.handler_unblock(self._lst_handler_id[18])

        self.txtRefDes.handler_block(self._lst_handler_id[19])
        self.txtRefDes.set_text('')
        self.txtRefDes.handler_unblock(self._lst_handler_id[19])

        _textbuffer = self.txtRemarks.do_get_buffer()
        _textbuffer.handler_block(self._lst_handler_id[20])
        _textbuffer.set_text('')
        _textbuffer.handler_unblock(self._lst_handler_id[20])

        self.txtSpecification.handler_block(self._lst_handler_id[21])
        self.txtSpecification.set_text('')
        self.txtSpecification.handler_unblock(self._lst_handler_id[21])

        self.txtYearMade.handler_block(self._lst_handler_id[22])
        self.txtYearMade.set_text('')
        self.txtYearMade.handler_unblock(self._lst_handler_id[22])

        return None

    def _do_load_page(self, attributes):
        """
        Load the Hardware General Data page.

        :param dict attributes: a dict of attribute key:value pairs for the
                                selected Hardware.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']
        self._hardware_id = attributes['hardware_id']
        RAMSTKWorkView.on_select(
            self,
            title=_(u"Analyzing Hardware {0:s} - {1:s}").format(
                str(attributes['ref_des']), str(attributes['name'])))

        # Disable the category RAMSTKCombo() if the hardware item is not a part.
        if attributes['part'] == 1:
            self.cmbCategory.set_button_sensitivity(gtk.SENSITIVITY_ON)
            self.cmbSubcategory.set_button_sensitivity(gtk.SENSITIVITY_ON)

            self.cmbCategory.set_active(int(attributes['category_id']))

            self.cmbSubcategory.handler_block(self._lst_handler_id[5])
            self._do_load_subcategory(int(attributes['category_id']))
            self.cmbSubcategory.set_active(int(attributes['subcategory_id']))
            self.cmbSubcategory.handler_unblock(self._lst_handler_id[5])

        else:
            self.cmbCategory.set_button_sensitivity(gtk.SENSITIVITY_OFF)
            self.cmbSubcategory.set_button_sensitivity(gtk.SENSITIVITY_OFF)

            # Clear the subcategory RAMSTKComboBox() always so it is empty
            # whenever an assembly is selected.
            _model = self.cmbSubcategory.get_model()
            _model.clear()

        self.chkRepairable.handler_block(self._lst_handler_id[0])
        self.chkRepairable.set_active(int(attributes['repairable']))
        self.chkRepairable.handler_unblock(self._lst_handler_id[0])

        self.chkTagged.handler_block(self._lst_handler_id[1])
        self.chkTagged.set_active(int(attributes['tagged_part']))
        self.chkTagged.handler_unblock(self._lst_handler_id[1])

        self.cmbCostType.handler_block(self._lst_handler_id[3])
        self.cmbCostType.set_active(int(attributes['cost_type_id']))
        self.cmbCostType.handler_unblock(self._lst_handler_id[3])

        self.cmbManufacturer.handler_block(self._lst_handler_id[4])
        self.cmbManufacturer.set_active(int(attributes['manufacturer_id']))
        self.cmbManufacturer.handler_unblock(self._lst_handler_id[4])

        self.txtAltPartNum.handler_block(self._lst_handler_id[6])
        self.txtAltPartNum.set_text(str(attributes['alt_part_num']))
        self.txtAltPartNum.handler_unblock(self._lst_handler_id[6])

        _textbuffer = self.txtAttachments.do_get_buffer()
        _textbuffer.handler_block(self._lst_handler_id[7])
        _textbuffer.set_text(str(attributes['attachments']))
        _textbuffer.handler_unblock(self._lst_handler_id[7])

        self.txtCAGECode.handler_block(self._lst_handler_id[8])
        self.txtCAGECode.set_text(str(attributes['cage_code']))
        self.txtCAGECode.handler_unblock(self._lst_handler_id[8])

        self.txtCompRefDes.handler_block(self._lst_handler_id[9])
        self.txtCompRefDes.set_text(str(attributes['comp_ref_des']))
        self.txtCompRefDes.handler_unblock(self._lst_handler_id[9])

        self.txtCost.handler_block(self._lst_handler_id[10])
        self.txtCost.set_text(str(locale.currency(attributes['cost'])))
        self.txtCost.handler_unblock(self._lst_handler_id[10])

        _textbuffer = self.txtDescription.do_get_buffer()
        _textbuffer.handler_block(self._lst_handler_id[11])
        _textbuffer.set_text(str(attributes['description']))
        _textbuffer.handler_unblock(self._lst_handler_id[11])

        self.txtFigureNumber.handler_block(self._lst_handler_id[12])
        self.txtFigureNumber.set_text(str(attributes['figure_number']))
        self.txtFigureNumber.handler_unblock(self._lst_handler_id[12])

        self.txtLCN.handler_block(self._lst_handler_id[13])
        self.txtLCN.set_text(str(attributes['lcn']))
        self.txtLCN.handler_unblock(self._lst_handler_id[13])

        self.txtName.handler_block(self._lst_handler_id[14])
        self.txtName.set_text(str(attributes['name']))
        self.txtName.handler_unblock(self._lst_handler_id[14])

        self.txtNSN.handler_block(self._lst_handler_id[15])
        self.txtNSN.set_text(str(attributes['nsn']))
        self.txtNSN.handler_unblock(self._lst_handler_id[15])

        self.txtPageNumber.handler_block(self._lst_handler_id[16])
        self.txtPageNumber.set_text(str(attributes['page_number']))
        self.txtPageNumber.handler_unblock(self._lst_handler_id[16])

        self.txtPartNumber.handler_block(self._lst_handler_id[17])
        self.txtPartNumber.set_text(str(attributes['part_number']))
        self.txtPartNumber.handler_unblock(self._lst_handler_id[17])

        self.txtQuantity.handler_block(self._lst_handler_id[18])
        self.txtQuantity.set_text(str(attributes['quantity']))
        self.txtQuantity.handler_unblock(self._lst_handler_id[18])

        self.txtRefDes.handler_block(self._lst_handler_id[19])
        self.txtRefDes.set_text(str(attributes['ref_des']))
        self.txtRefDes.handler_unblock(self._lst_handler_id[19])

        _textbuffer = self.txtRemarks.do_get_buffer()
        _textbuffer.handler_block(self._lst_handler_id[20])
        _textbuffer.set_text(str(attributes['remarks']))
        _textbuffer.handler_unblock(self._lst_handler_id[20])

        self.txtSpecification.handler_block(self._lst_handler_id[21])
        self.txtSpecification.set_text(str(attributes['specification_number']))
        self.txtSpecification.handler_unblock(self._lst_handler_id[21])

        self.txtYearMade.handler_block(self._lst_handler_id[22])
        self.txtYearMade.set_text(str(attributes['year_of_manufacture']))
        self.txtYearMade.handler_unblock(self._lst_handler_id[22])

        return None

    def _do_load_subcategory(self, category_id):
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
            _subcategory = SortedDict(self._mdcRAMSTK.RAMSTK_CONFIGURATION.
                                      RAMSTK_SUBCATEGORIES[category_id])
            _data = []
            for _key in _subcategory:
                _data.append([_subcategory[_key]])

            self.cmbSubcategory.do_load_combo(_data)

        return None

    def _do_request_make_comp_ref_des(self, __button):
        """
        Send request to create the composite reference designator.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(gtk.gdk.WATCH)
        pub.sendMessage('request_make_comp_ref_des', node_id=self._hardware_id)
        self.do_set_cursor(gtk.gdk.LEFT_PTR)

        return None

    def _do_request_update(self, __button):
        """
        Send request to save the currently selected Hardware item.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(gtk.gdk.WATCH)
        pub.sendMessage('request_update_hardware', node_id=self._hardware_id)
        self.do_set_cursor(gtk.gdk.LEFT_PTR)

        return None

    def _do_request_update_all(self, __button):
        """
        Send request to save all Hardware items.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(gtk.gdk.WATCH)
        pub.sendMessage('request_update_all_hardware')
        self.do_set_cursor(gtk.gdk.LEFT_PTR)

        return None

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the gtk.ButtonBox() for the Hardware class Work View.

        :return: _buttonbox; the gtk.ButtonBox() for the Hardware class Work
                 View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Creates the composite reference designator for the selected "
              u"hardware item.")
        ]
        _callbacks = [self._do_request_make_comp_ref_des]
        _icons = ['comp_ref_des']

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
        Make the Hardware class gtk.Notebook() general data page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Load the gtk.ComboBox() widgets.
        self.cmbCostType.do_load_combo(RAMSTK_COST_TYPES)

        _data = []
        for _key in self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_CATEGORIES:
            _data.append(
                [self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_CATEGORIES[_key]])
        self.cmbCategory.do_load_combo(_data)

        _data = []
        for _key in self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_MANUFACTURERS:
            _data.append(self._mdcRAMSTK.RAMSTK_CONFIGURATION.
                         RAMSTK_MANUFACTURERS[_key])
        self.cmbManufacturer.do_load_combo(_data, simple=False)

        # Build the General Data page starting with the left half.
        _hbox = gtk.HBox()
        _fixed = gtk.Fixed()

        _scrollwindow = ramstk.RAMSTKScrolledWindow(_fixed)
        _frame = ramstk.RAMSTKFrame(label=_(u"Hardware Description"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = ramstk.make_label_group(self._lst_labels[0], _fixed,
                                                 5, 5)
        _x_pos += 50

        _hbox.pack_start(_frame, expand=True, fill=True)

        # Move the labels after the description to account for the extra
        # vertical space needed by the description RAMSTKTextView().
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

        _scrollwindow = ramstk.RAMSTKScrolledWindow(_fixed)
        _frame = ramstk.RAMSTKFrame(label=_(u"Purchasing Information"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = ramstk.make_label_group(self._lst_labels[1], _fixed,
                                                 5, 5)
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

        _scrollwindow = ramstk.RAMSTKScrolledWindow(_fixed)
        _frame = ramstk.RAMSTKFrame(label=_(u"Miscellaneous Information"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = ramstk.make_label_group(self._lst_labels[2], _fixed,
                                                 5, 5)
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
        _label = ramstk.RAMSTKLabel(
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
        Retrieve RAMSTKCombo() changes and assign to Hardware attribute.

        This method is called by:

            * gtk.Combo() 'changed' signal

        This method emits the 'changedCategory' and 'changedSubcategory'
        messages.

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.RAMSTKCombo`
        :param int index: the position in the Requirement class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Entry().
        :return: None
        :rtype: None
        """
        _dic_keys = {
            2: 'category_id',
            3: 'cost_type_id',
            4: 'manufacturer_id',
            5: 'subcategory_id'
        }
        try:
            _key = _dic_keys[index]
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
            self.txtCAGECode.set_text(_model.get(_row, 2)[0])
        elif index == 5:
            pub.sendMessage('changed_subcategory', subcategory_id=_new_text)

        pub.sendMessage(
            'wvw_editing_hardware',
            module_id=self._hardware_id,
            key=_key,
            value=_new_text)

        combo.handler_unblock(self._lst_handler_id[index])

        return None

    def _on_edit(self, module_id, key, value):  # pylint: disable=unused-argument
        """
        Update the Work View gtk.Widgets() when Hardware attributes change.

        This method is called whenever an attribute is edited in a different
        view.

        :param int module_id: the ID of the Hardware being edited.  This
                              parameter is required to allow the PyPubSub
                              signals to call this method and the
                              request_set_attributes() method in the
                              RAMSTKDataController.
        :param int index: the index in the Hardware attributes list of the
                          attribute that was edited.
        :param str value: the new text to update the gtk.Widget() with.
        :return: None
        :rtype: None
        """
        if key == 'description':
            self.txtDescription.handler_block(self._lst_handler_id[5])
            self.txtDescription.set_text(str(value))
            self.txtDescription.handler_unblock(self._lst_handler_id[5])
        elif key == 'name':
            self.txtName.handler_block(self._lst_handler_id[15])
            self.txtName.set_text(str(value))
            self.txtName.handler_unblock(self._lst_handler_id[15])
        elif key == 'remarks':
            _textbuffer = self.txtRemarks.do_get_buffer()
            _textbuffer.handler_block(self._lst_handler_id[17])
            _textbuffer.set_text(str(value))
            _textbuffer.handler_unblock(self._lst_handler_id[17])

        return None

    def _on_focus_out(self, entry, index):
        """
        Retrieve changes made in RAMSTKEntry() widgets..

        This method is called by:

            * RAMSTKEntry() 'changed' signal
            * RAMSTKTextView() 'changed' signal

        This method sends the 'wvwEditedHardware' message.

        :param entry: the RAMSTKEntry() or RAMSTKTextView() that called the method.
        :type entry: :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` or
                     :class:`ramstk.gui.gtk.ramstk.RAMSTKTextView`
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

        :return: None
        :rtype: None
        """
        _dic_keys = {
            6: 'alt_part_num',
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
        try:
            _key = _dic_keys[index]
        except KeyError:
            _key = ''

        _new_text = ''

        entry.handler_block(self._lst_handler_id[index])

        if index == 6:
            _new_text = str(entry.get_text())
        elif index == 7:
            _new_text = self.txtAttachments.do_get_text()
        elif index == 8:
            _new_text = str(entry.get_text())
        elif index == 9:
            _new_text = str(entry.get_text())
        elif index == 10:
            try:
                _new_text = float(entry.get_text())
            except ValueError:
                _new_text = 0.0
        elif index == 11:
            _new_text = self.txtDescription.do_get_text()
        elif index == 12:
            _new_text = str(entry.get_text())
        elif index == 13:
            _new_text = str(entry.get_text())
        elif index == 14:
            _new_text = str(entry.get_text())
        elif index == 15:
            _new_text = str(entry.get_text())
        elif index == 16:
            _new_text = str(entry.get_text())
        elif index == 17:
            _new_text = str(entry.get_text())
        elif index == 18:
            try:
                _new_text = int(entry.get_text())
            except ValueError:
                _new_text = 1
        elif index == 19:
            _new_text = str(entry.get_text())
        elif index == 20:
            _new_text = self.txtRemarks.do_get_text()
        elif index == 21:
            _new_text = str(entry.get_text())
        elif index == 22:
            try:
                _new_text = int(entry.get_text())
            except ValueError:
                _new_text = date.today().year

        pub.sendMessage(
            'wvw_editing_hardware',
            module_id=self._hardware_id,
            key=_key,
            value=_new_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return None

    def _on_toggled(self, togglebutton, index):
        """
        Handle RAMSTKCheckButton() 'toggle' signals.

        :param togglebutton: the RAMSTKToggleButton() that called this method.
        :type: :class:`ramstk.gui.gtk.ramstk.Button.RAMSTKToggleButton`
        :param int index: the index in the signal handler ID list.
        :return: None
        :rtype: None
        """
        _dic_keys = {0: 'repairable', 1: 'tagged_part'}
        _key = _dic_keys[index]

        togglebutton.handler_block(self._lst_handler_id[index])

        try:
            _new_text = boolean_to_integer(togglebutton.get_active())
        except ValueError:
            _new_text = 0

        pub.sendMessage(
            'wvw_editing_hardware',
            module_id=self._hardware_id,
            key=_key,
            value=_new_text)

        togglebutton.handler_unblock(self._lst_handler_id[index])

        return None


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
    ],
                   [
                       _(u"Active Environment:"),
                       _(u"Dormant Environment:"),
                       _(u"Active Temperature (\u00B0C):"),
                       _(u"Dormant Temperature (\u00B0C):"),
                       _(u"Mission Time:"),
                       _(u"Duty Cycle:")
                   ]]

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize an instance of the Hardware assessment input view.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKWorkView.__init__(self, controller, module='Hardware')

        # Initialize private dictionary attributes.
        #self._dic_assessment_input = {1: wvwIntegratedCircuitAI(),
        #                        2: wvwSemiconductorAI(),
        #                       3: wvwResistorAI(),
        #                     5: wvwInductorAI(),
        #                    6: wvwRelayAI(),
        #                   7: wvwSwitchAI(),
        #                  8: wvwConnectionAI(),
        #                 9: wvwMeterAI(),
        #               10: wvwMiscellaneousAI(),
        #              }
        self._dic_assessment_input = {
            4: wvwCapacitorAI(),
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hardware_id = None
        self._hazard_rate_method_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbActiveEnviron = ramstk.RAMSTKComboBox(
            tooltip=_(u"The operating environment for the hardware item."))
        self.cmbDormantEnviron = ramstk.RAMSTKComboBox(
            tooltip=_(u"The storage environment for the hardware item."))
        self.cmbFailureDist = ramstk.RAMSTKComboBox(
            tooltip=_(
                u"The statistical failure distribution of the hardware item."))
        self.cmbHRType = ramstk.RAMSTKComboBox(
            tooltip=_(u"The type of reliability assessment for the selected "
                      u"hardware item."))
        self.cmbHRMethod = ramstk.RAMSTKComboBox(
            tooltip=_(
                u"The assessment method to use for the selected hardware item."
            ))

        self.scwDesignRatings = ramstk.RAMSTKScrolledWindow(None)
        self.scwOperatingStress = ramstk.RAMSTKScrolledWindow(None)

        self.txtActiveTemp = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(
                u"The ambient temperature in the operating environment."))
        self.txtAddAdjFactor = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(
                u"An adjustment factor to add to the assessed hazard rate or "
                u"MTBF."))
        self.txtDormantTemp = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The ambient temperature in the storage environment."))
        self.txtDutyCycle = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The duty cycle of the selected hardware item."))
        self.txtFailScale = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(
                u"The scale parameter of the statistical failure distribution."
            ))
        self.txtFailShape = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(
                u"The shape parameter of the statistical failure distribution."
            ))
        self.txtFailLocation = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The location parameter of the statistical failure "
                      u"distribution."))
        self.txtMissionTime = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The mission time of the selected hardware item."))
        self.txtMultAdjFactor = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(
                u"An adjustment factor to multiply the assessed hazard rate "
                u"or MTBF by."))
        self.txtSpecifiedHt = ramstk.RAMSTKEntry(
            width=125, tooltip=_(u"The stated hazard rate."))
        self.txtSpecifiedHtVar = ramstk.RAMSTKEntry(
            width=125, tooltip=_(u"The variance of the stated hazard rate."))
        self.txtSpecifiedMTBF = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The stated mean time between failure (MTBF)."))
        self.txtSpecifiedMTBFVar = ramstk.RAMSTKEntry(
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
        self.pack_start(self._make_page(), expand=True, fill=True)
        self.show_all()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._do_load_page, 'selected_hardware')
        pub.subscribe(self._do_set_sensitive, 'changed_hazard_rate_type')
        pub.subscribe(self._on_edit, 'mvw_editing_hardware')

    def _do_clear_page(self):
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        self.txtDutyCycle.handler_block(self._lst_handler_id[16])
        self.txtDutyCycle.set_text('')
        self.txtDutyCycle.handler_unblock(self._lst_handler_id[16])

        self.txtMissionTime.handler_block(self._lst_handler_id[17])
        self.txtMissionTime.set_text('')
        self.txtMissionTime.handler_unblock(self._lst_handler_id[17])

        # Clear the component-specific gtk.ScrolledWindow()s.
        for _child in self.scwDesignRatings.get_children():
            self.scwDesignRatings.remove(_child)

        for _child in self.scwOperatingStress.get_children():
            self.scwOperatingStress.remove(_child)

        self.cmbActiveEnviron.handler_block(self._lst_handler_id[0])
        self.cmbActiveEnviron.set_active(0)
        self.cmbActiveEnviron.handler_unblock(self._lst_handler_id[0])

        self.cmbDormantEnviron.handler_block(self._lst_handler_id[1])
        self.cmbDormantEnviron.set_active(0)
        self.cmbDormantEnviron.handler_unblock(self._lst_handler_id[1])

        self.txtActiveTemp.handler_block(self._lst_handler_id[5])
        self.txtActiveTemp.set_text('')
        self.txtActiveTemp.handler_unblock(self._lst_handler_id[5])

        self.txtDormantTemp.handler_block(self._lst_handler_id[7])
        self.txtDormantTemp.set_text('')
        self.txtDormantTemp.handler_unblock(self._lst_handler_id[7])

        self.cmbFailureDist.handler_block(self._lst_handler_id[2])
        self.cmbFailureDist.set_active(0)
        self.cmbFailureDist.handler_unblock(self._lst_handler_id[2])

        self.cmbHRType.handler_block(self._lst_handler_id[3])
        self.cmbHRType.set_active(0)
        self.cmbHRType.handler_unblock(self._lst_handler_id[3])

        self.cmbHRMethod.handler_block(self._lst_handler_id[4])
        self.cmbHRMethod.set_active(0)
        self.cmbHRMethod.handler_unblock(self._lst_handler_id[4])

        self.txtAddAdjFactor.handler_block(self._lst_handler_id[6])
        self.txtAddAdjFactor.set_text('')
        self.txtAddAdjFactor.handler_unblock(self._lst_handler_id[6])

        self.txtFailScale.handler_block(self._lst_handler_id[8])
        self.txtFailScale.set_text('')
        self.txtFailScale.handler_unblock(self._lst_handler_id[8])

        self.txtFailShape.handler_block(self._lst_handler_id[9])
        self.txtFailShape.set_text('')
        self.txtFailShape.handler_unblock(self._lst_handler_id[9])

        self.txtFailLocation.handler_block(self._lst_handler_id[10])
        self.txtFailLocation.set_text('')
        self.txtFailLocation.handler_unblock(self._lst_handler_id[10])

        self.txtMultAdjFactor.handler_block(self._lst_handler_id[11])
        self.txtMultAdjFactor.set_text('')
        self.txtMultAdjFactor.handler_unblock(self._lst_handler_id[11])

        self.txtSpecifiedHt.handler_block(self._lst_handler_id[12])
        self.txtSpecifiedHt.set_text('')
        self.txtSpecifiedHt.handler_unblock(self._lst_handler_id[12])

        self.txtSpecifiedHtVar.handler_block(self._lst_handler_id[13])
        self.txtSpecifiedHtVar.set_text('')
        self.txtSpecifiedHtVar.handler_unblock(self._lst_handler_id[13])

        self.txtSpecifiedMTBF.handler_block(self._lst_handler_id[14])
        self.txtSpecifiedMTBF.set_text('')
        self.txtSpecifiedMTBF.handler_unblock(self._lst_handler_id[14])

        self.txtSpecifiedMTBFVar.handler_block(self._lst_handler_id[15])
        self.txtSpecifiedMTBFVar.set_text('')
        self.txtSpecifiedMTBFVar.handler_unblock(self._lst_handler_id[15])

        return None

    def _do_load_page(self, attributes):
        """
        Load the Hardware Assessment Inputs page.

        :param dict attributes: a dict of attribute key:value pairs for the
                                selected Hardware.
        :return: None
        :rtype: None
        """
        self._hardware_id = attributes['hardware_id']

        # Retrieve the appropriate component-specific work views.
        try:
            _component_ai = self._dic_assessment_input[
                attributes['category_id']]
        except KeyError:
            _component_ai = None

        _component_si = Component.StressInputs()

        self.txtDutyCycle.handler_block(self._lst_handler_id[16])
        self.txtDutyCycle.set_text(self.fmt.format(attributes['duty_cycle']))
        self.txtDutyCycle.handler_unblock(self._lst_handler_id[16])

        self.txtMissionTime.handler_block(self._lst_handler_id[17])
        self.txtMissionTime.set_text(
            self.fmt.format(attributes['mission_time']))
        self.txtMissionTime.handler_unblock(self._lst_handler_id[17])

        # Clear the component-specific gtk.ScrolledWindow()s if there are
        # already a component-specific work view objects.
        _child = self.scwDesignRatings.get_child().get_children()[0]
        try:
            _child.remove(_child.get_child())
        except TypeError:
            pass

        # Load the component-specific widgets.
        if _component_ai is not None:
            _component_ai.fmt = self.fmt
            _child.add(_component_ai)

        _child = self.scwOperatingStress.get_child().get_children()[0]
        try:
            _child.remove(_child.get_child())
        except TypeError:
            pass

        if _component_si is not None:
            _component_si.fmt = self.fmt
            _component_si.do_load_page(attributes)
            _child.add(_component_si)

        self.cmbActiveEnviron.handler_block(self._lst_handler_id[0])
        self.cmbActiveEnviron.set_active(
            int(attributes['environment_active_id']))
        self.cmbActiveEnviron.handler_unblock(self._lst_handler_id[0])

        self.cmbDormantEnviron.handler_block(self._lst_handler_id[1])
        self.cmbDormantEnviron.set_active(
            int(attributes['environment_dormant_id']))
        self.cmbDormantEnviron.handler_unblock(self._lst_handler_id[1])

        self.txtActiveTemp.handler_block(self._lst_handler_id[5])
        self.txtActiveTemp.set_text(
            self.fmt.format(attributes['temperature_active']))
        self.txtActiveTemp.handler_unblock(self._lst_handler_id[5])

        self.txtDormantTemp.handler_block(self._lst_handler_id[7])
        self.txtDormantTemp.set_text(
            self.fmt.format(attributes['temperature_dormant']))
        self.txtDormantTemp.handler_unblock(self._lst_handler_id[7])

        self.cmbFailureDist.handler_block(self._lst_handler_id[2])
        self.cmbFailureDist.set_active(
            int(attributes['failure_distribution_id']))
        self.cmbFailureDist.handler_unblock(self._lst_handler_id[2])

        self.cmbHRType.handler_block(self._lst_handler_id[3])
        self.cmbHRType.set_active(int(attributes['hazard_rate_type_id']))
        self.cmbHRType.handler_unblock(self._lst_handler_id[3])

        self.cmbHRMethod.handler_block(self._lst_handler_id[4])
        self.cmbHRMethod.set_active(int(attributes['hazard_rate_method_id']))
        self.cmbHRMethod.handler_unblock(self._lst_handler_id[4])

        self.txtAddAdjFactor.handler_block(self._lst_handler_id[6])
        self.txtAddAdjFactor.set_text(
            self.fmt.format(attributes['add_adj_factor']))
        self.txtAddAdjFactor.handler_unblock(self._lst_handler_id[6])

        self.txtFailScale.handler_block(self._lst_handler_id[8])
        self.txtFailScale.set_text(
            self.fmt.format(attributes['scale_parameter']))
        self.txtFailScale.handler_unblock(self._lst_handler_id[8])

        self.txtFailShape.handler_block(self._lst_handler_id[9])
        self.txtFailShape.set_text(
            self.fmt.format(attributes['shape_parameter']))
        self.txtFailShape.handler_unblock(self._lst_handler_id[9])

        self.txtFailLocation.handler_block(self._lst_handler_id[10])
        self.txtFailLocation.set_text(
            self.fmt.format(attributes['location_parameter']))
        self.txtFailLocation.handler_unblock(self._lst_handler_id[10])

        self.txtMultAdjFactor.handler_block(self._lst_handler_id[11])
        self.txtMultAdjFactor.set_text(
            self.fmt.format(attributes['mult_adj_factor']))
        self.txtMultAdjFactor.handler_unblock(self._lst_handler_id[11])

        self.txtSpecifiedHt.handler_block(self._lst_handler_id[12])
        self.txtSpecifiedHt.set_text(
            self.fmt.format(attributes['hazard_rate_specified']))
        self.txtSpecifiedHt.handler_unblock(self._lst_handler_id[12])

        self.txtSpecifiedHtVar.handler_block(self._lst_handler_id[13])
        self.txtSpecifiedHtVar.set_text(
            self.fmt.format(attributes['hr_specified_variance']))
        self.txtSpecifiedHtVar.handler_unblock(self._lst_handler_id[13])

        self.txtSpecifiedMTBF.handler_block(self._lst_handler_id[14])
        self.txtSpecifiedMTBF.set_text(
            self.fmt.format(attributes['mtbf_specified']))
        self.txtSpecifiedMTBF.handler_unblock(self._lst_handler_id[14])

        self.txtSpecifiedMTBFVar.handler_block(self._lst_handler_id[15])
        self.txtSpecifiedMTBFVar.set_text(
            self.fmt.format(attributes['mtbf_spec_variance']))
        self.txtSpecifiedMTBFVar.handler_unblock(self._lst_handler_id[15])

        self._do_set_sensitive(type_id=attributes['hazard_rate_type_id'])

        # Set the calculate button sensitive only if the selected hardware
        # item is a part.
        if attributes['part'] == 1:
            self.get_children()[0].get_children()[0].set_sensitive(True)
        else:
            self.get_children()[0].get_children()[0].set_sensitive(False)

        self.scwDesignRatings.show_all()
        self.scwOperatingStress.show_all()

        # Send the PyPubSub message to let the component-specific widgets know
        # they can load.
        pub.sendMessage('loaded_hardware_inputs', attributes=attributes)

        return None

    def _do_request_calculate(self, __button):
        """
        Send request to calculate the selected hardware.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _multiplier = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_HR_MULTIPLIER
        pub.sendMessage(
            'request_calculate_hardware',
            node_id=self._hardware_id,
            hr_multiplier=_multiplier)

        return None

    def _do_request_update(self, __button):
        """
        Send request to save the currently selected Hardware item.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(gtk.gdk.WATCH)
        pub.sendMessage('request_update_hardware', node_id=self._hardware_id)
        self.do_set_cursor(gtk.gdk.LEFT_PTR)

        return None

    def _do_request_update_all(self, __button):
        """
        Send request to save all Hardware items.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(gtk.gdk.WATCH)
        pub.sendMessage('request_update_all_hardware')
        self.do_set_cursor(gtk.gdk.LEFT_PTR)

        return None

    def _do_set_sensitive(self, type_id):
        """
        Set certain widgets sensitive or insensitive.

        This method will set the sensitivity of various widgets depending on
        the hazard rate assessment type selected.

        :param int type_id: the type of hazard rate that was selected.
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
        elif type_id == 2:  # User specified hazard rate.
            self.cmbFailureDist.set_sensitive(False)
            self.cmbHRMethod.set_sensitive(False)
            self.txtFailLocation.set_sensitive(False)
            self.txtFailScale.set_sensitive(False)
            self.txtFailShape.set_sensitive(False)
            self.txtSpecifiedHt.set_sensitive(True)
            self.txtSpecifiedHtVar.set_sensitive(True)
            self.txtSpecifiedMTBF.set_sensitive(False)
            self.txtSpecifiedMTBFVar.set_sensitive(False)
        elif type_id == 3:  # User specified MTBF.
            self.cmbFailureDist.set_sensitive(False)
            self.cmbHRMethod.set_sensitive(False)
            self.txtFailLocation.set_sensitive(False)
            self.txtFailScale.set_sensitive(False)
            self.txtFailShape.set_sensitive(False)
            self.txtSpecifiedHt.set_sensitive(False)
            self.txtSpecifiedHtVar.set_sensitive(False)
            self.txtSpecifiedMTBF.set_sensitive(True)
            self.txtSpecifiedMTBFVar.set_sensitive(True)
        elif type_id == 4:  # User specified failure distribution.
            self.cmbFailureDist.set_sensitive(True)
            self.cmbHRMethod.set_sensitive(False)
            self.txtFailLocation.set_sensitive(True)
            self.txtFailScale.set_sensitive(True)
            self.txtFailShape.set_sensitive(True)
            self.txtSpecifiedHt.set_sensitive(False)
            self.txtSpecifiedHtVar.set_sensitive(False)
            self.txtSpecifiedMTBF.set_sensitive(False)
            self.txtSpecifiedMTBFVar.set_sensitive(False)

        return None

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the gtk.ButtonBox() for the Hardware class Work View.

        :return: _buttonbox; the gtk.ButtonBox() for the Hardware class Work
                 View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [_(u"Calculate the currently selected Hardware item.")]
        _callbacks = [self._do_request_calculate]

        _icons = ['calculate']

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
        Make the Hardware class gtk.Notebook() assessment input page.

        :return: a gtk.HBox() instance.
        :rtype: :class:`gtk.HBox`
        """
        # Load the gtk.ComboBox() widgets.
        self.cmbActiveEnviron.do_load_combo(RAMSTK_ACTIVE_ENVIRONMENTS)
        self.cmbDormantEnviron.do_load_combo(RAMSTK_DORMANT_ENVIRONMENTS)
        self.cmbHRType.do_load_combo(RAMSTK_HR_TYPES)
        self.cmbHRMethod.do_load_combo(RAMSTK_HR_MODELS)
        self.cmbFailureDist.do_load_combo(RAMSTK_HR_DISTRIBUTIONS)

        # Build the assessment input page starting with the top left half.
        _hbox = gtk.HBox()
        _vpaned = gtk.VPaned()
        _fixed = gtk.Fixed()

        _scrollwindow = ramstk.RAMSTKScrolledWindow(_fixed)
        _frame = ramstk.RAMSTKFrame(label=_(u"Assessment Inputs"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = ramstk.make_label_group(self._lst_labels[0], _fixed,
                                                 5, 5)
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

        # Now add the bottom left pane.  This is just an RAMSTKFrame() and will
        # be the container for component-specific design attributes.
        _frame = ramstk.RAMSTKFrame(label=_(u"Design Ratings"))
        _frame.add(self.scwDesignRatings)
        _vpaned.pack2(_frame, True, True)

        # Now add the top right pane.
        _vpaned = gtk.VPaned()
        _fixed = gtk.Fixed()

        _scrollwindow = ramstk.RAMSTKScrolledWindow(_fixed)
        _frame = ramstk.RAMSTKFrame(label=_(u"Environmental Inputs"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = ramstk.make_label_group(self._lst_labels[1], _fixed,
                                                 5, 5)
        _x_pos += 50

        _fixed.put(self.cmbActiveEnviron, _x_pos, _y_pos[0])
        _fixed.put(self.cmbDormantEnviron, _x_pos, _y_pos[1])
        _fixed.put(self.txtActiveTemp, _x_pos, _y_pos[2])
        _fixed.put(self.txtDormantTemp, _x_pos, _y_pos[3])
        _fixed.put(self.txtMissionTime, _x_pos, _y_pos[4])
        _fixed.put(self.txtDutyCycle, _x_pos, _y_pos[5])

        _fixed.show_all()

        _vpaned.pack1(_frame, True, True)

        # Finally, add the bottom right pane.  This is just an RAMSTKFrame()
        # and will be the container for component-specific design attributes.
        _frame = ramstk.RAMSTKFrame(label=_(u"Operating Stresses"))
        _frame.add(self.scwOperatingStress)
        _vpaned.pack2(_frame, True, True)

        _hbox.pack_end(_vpaned, expand=True, fill=True)

        _frame = gtk.Frame()
        self.scwDesignRatings.add_with_viewport(_frame)

        _frame = gtk.Frame()
        self.scwOperatingStress.add_with_viewport(_frame)

        # Create the label for the gtk.Notebook() tab.
        _label = ramstk.RAMSTKLabel(
            _(u"Assessment\nInputs"),
            height=30,
            width=-1,
            justify=gtk.JUSTIFY_CENTER,
            tooltip=_(u"Displays reliability assessment inputs for the "
                      u"selected hardware item."))
        self.hbx_tab_label.pack_start(_label)

        return _hbox

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RAMSTKCombo() changes and assign to Hardware attribute.

        This method is called by:

            * gtk.Combo() 'changed' signal

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.RAMSTKCombo`
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

        :return: None
        :rtype: None
        """
        _dic_keys = {
            0: 'environment_active_id',
            1: 'environment_dormant_id',
            2: 'failure_distribution_id',
            3: 'hazard_rate_type_id',
            4: 'hazard_rate_method_id'
        }
        try:
            _key = _dic_keys[index]
        except KeyError:
            _key = ''

        combo.handler_block(self._lst_handler_id[index])

        try:
            _new_text = int(combo.get_active())
        except ValueError:
            _new_text = 0

        # Hazard rate types are:
        #     1 = Assessed
        #     2 = Defined, Hazard Rate
        #     3 = Defined, MTBF
        #     4 = Defined, Distribution
        if index == 3:
            pub.sendMessage('changed_hazard_rate_type', type_id=_new_text)
        # Hazard rate methods are:
        #     1 = MIL-HDBK-217F Parts Count
        #     2 = MIL-HDNK-217F Parts Stress
        #     3 = NSWC (not yet implemented)
        elif index == 4:
            pub.sendMessage('changed_hazard_rate_method', method_id=_new_text)
            self._hazard_rate_method_id = _new_text

        # Only publish the message if something is selected in the ComboBox.
        if _new_text != -1:
            pub.sendMessage(
                'wvw_editing_hardware',
                module_id=self._hardware_id,
                key=_key,
                value=_new_text)

        combo.handler_unblock(self._lst_handler_id[index])

        return None

    def _on_edit(self, module_id, key, value):  # pylint: disable=unused-argument
        """
        Update Hardware Assessment Input gtk.Widgets() when attributes change.

        This method is called whenever an attribute is edited in a different
        view.

        :param int module_id: the ID of the Hardware being edited.  This
                              parameter is required to allow the PyPubSub
                              signals to call this method and the
                              request_set_attributes() method in the
                              RAMSTKDataController.
        :param int index: the index in the Hardware attributes list of the
                          attribute that was edited.
        :param str value: the new text to update the gtk.Widget() with.
        :return: None
        :rtype: None
        """
        if key == 'add_adj_factor':
            self.txtAddAdjFactor.handler_block(self._lst_handler_id[6])
            self.txtAddAdjFactor.set_text(self.fmt.format(value))
            self.txtAddAdjFactor.handler_unblock(self._lst_handler_id[6])
        elif key == 'scale_parameter':
            self.txtFailScale.handler_block(self._lst_handler_id[8])
            self.txtFailScale.set_text(self.fmt.format(value))
            self.txtFailScale.handler_unblock(self._lst_handler_id[8])
        elif key == 'shape_parameter':
            self.txtFailShape.handler_block(self._lst_handler_id[9])
            self.txtFailShape.set_text(self.fmt.format(value))
            self.txtFailShape.handler_unblock(self._lst_handler_id[9])
        elif key == 'location_parameter':
            self.txtFailLocation.handler_block(self._lst_handler_id[10])
            self.txtFailLocation.set_text(self.fmt.format(value))
            self.txtFailLocation.handler_unblock(self._lst_handler_id[10])
        elif key == 'mult_adj_factor':
            self.txtMultAdjFactor.handler_block(self._lst_handler_id[11])
            self.txtMultAdjFactor.set_text(self.fmt.format(value))
            self.txtMultAdjFactor.handler_unblock(self._lst_handler_id[11])
        elif key == 'hazard_rate_specified':
            self.txtSpecifiedHt.handler_block(self._lst_handler_id[12])
            self.txtSpecifiedHt.set_text(self.fmt.format(value))
            self.txtSpecifiedHt.handler_unblock(self._lst_handler_id[12])
        elif key == 'hr_specified_variance':
            self.txtSpecifiedHtVar.handler_block(self._lst_handler_id[13])
            self.txtSpecifiedHtVar.set_text(self.fmt.format(value))
            self.txtSpecifiedHtVar.handler_unblock(self._lst_handler_id[13])
        elif key == 'mtbf_specified':
            self.txtSpecifiedMTBF.handler_block(self._lst_handler_id[14])
            self.txtSpecifiedMTBF.set_text(self.fmt.format(value))
            self.txtSpecifiedMTBF.handler_unblock(self._lst_handler_id[14])
        elif key == 'mtbf_spec_variance':
            self.txtSpecifiedMTBFVar.handler_block(self._lst_handler_id[15])
            self.txtSpecifiedMTBFVar.set_text(self.fmt.format(value))
            self.txtSpecifiedMTBFVar.handler_unblock(self._lst_handler_id[15])
        elif key == 'duty_cycle':
            self.txtDutyCycle.handler_block(self._lst_handler_id[16])
            self.txtDutyCycle.set_text(self.fmt.format(value))
            self.txtDutyCycle.handler_unblock(self._lst_handler_id[16])
        elif key == 'mission_time':
            self.txtMissionTime.handler_block(self._lst_handler_id[17])
            self.txtMissionTime.set_text(self.fmt.format(value))
            self.txtMissionTime.handler_unblock(self._lst_handler_id[17])

        return None

    def _on_focus_out(self, entry, index):
        """
        Retrieve changes made in RAMSTKEntry() widgets..

        This method is called by:

            * RAMSTKEntry() 'changed' signal
            * RAMSTKTextView() 'changed' signal

        This method sends the 'wvwEditedHardware' message.

        :param entry: the RAMSTKEntry() or RAMSTKTextView() that called the
                      method.
        :type entry: :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` or
                     :class:`ramstk.gui.gtk.ramstk.RAMSTKTextView`
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

        :return: None
        :rtype: None
        """
        _dic_keys = {
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
            15: 'mtbf_spec_variance',
            16: 'duty_cycle',
            17: 'mission_time'
        }
        try:
            _key = _dic_keys[index]
        except KeyError:
            _key = ''

        entry.handler_block(self._lst_handler_id[index])

        try:
            _new_text = float(entry.get_text())
        except ValueError:
            _new_text = 0.0

        pub.sendMessage(
            'wvw_editing_hardware',
            module_id=self._hardware_id,
            key=_key,
            value=_new_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return None


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
    ],
                   [
                       _(u"Logistics Availability [A(t)]:"),
                       _(u"Mission A(t):"),
                       _(u"Total Cost:"),
                       _(u"Cost/Failure:"),
                       _(u"Cost/Hour:"),
                       _(u"Total # of Parts:")
                   ]]

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the Hardware package.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKWorkView.__init__(self, controller, module='Hardware')

        # Initialize private dictionary attributes.
        #self._dic_assessment_results = {1: wvwIntegratedCircuitAI(),
        #                        2: wvwSemiconductorAI(),
        #                       3: wvwResistorAI(),
        #                     5: wvwInductorAI(),
        #                    6: wvwRelayAI(),
        #                   7: wvwSwitchAI(),
        #                  8: wvwConnectionAI(),
        #                 9: wvwMeterAI(),
        #               10: wvwMiscellaneousAI(),
        #              }
        self._dic_assessment_results = {
            4: wvwCapacitorAR(),
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hardware_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.scwReliability = ramstk.RAMSTKScrolledWindow(None)
        self.scwStress = ramstk.RAMSTKScrolledWindow(None)

        self.txtActiveHt = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the active failure intensity for the "
                      u"selected hardware item."))
        self.txtActiveHtVar = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the variance on the active failure intensity "
                      u"for the selected hardware item."))
        self.txtCostFailure = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            tooltip=_(u"Displays the cost per failure of the selected "
                      u"hardware item."))
        self.txtCostHour = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            tooltip=_(u"Displays the failure cost per operating hour for the "
                      u"selected hardware item."))
        self.txtDormantHt = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the dormant failure intensity for the "
                      u"selected hardware item."))
        self.txtDormantHtVar = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(
                u"Displays the variance on the dormant failure intensity "
                u"for the selected hardware item."))
        self.txtLogisticsAt = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the logistics availability for the selected "
                      u"hardware item."))
        self.txtLogisticsAtVar = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the variance on the logistics availability "
                      u"for the selected hardware item."))
        self.txtLogisticsHt = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the logistics failure intensity for the "
                      u"selected hardware item.  This is the sum of the "
                      u"active, dormant, and software hazard rates."))
        self.txtLogisticsHtVar = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the variance on the logistics failure "
                      u"intensity for the selected hardware item."))
        self.txtLogisticsMTBF = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the logistics mean time between failure "
                      u"(MTBF) for the selected hardware item."))
        self.txtLogisticsMTBFVar = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the variance on the logistics MTBF for the "
                      u"selected hardware item."))
        self.txtLogisticsRt = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the logistics reliability for the selected "
                      u"hardware item."))
        self.txtLogisticsRtVar = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the variance on the logistics reliability "
                      u"for the selected hardware item."))
        self.txtMCMT = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mean corrective maintenance time (MCMT) "
                      u"for the selected hardware item."))
        self.txtMissionAt = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mission availability for the selected "
                      u"hardware item."))
        self.txtMissionAtVar = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the variance on the mission availability for "
                      u"the selected hardware item."))
        self.txtMissionHt = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mission failure intensity for the "
                      u"selected hardware item."))
        self.txtMissionHtVar = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the variance on the mission failure "
                      u"intensity for the selected hardware item."))
        self.txtMissionMTBF = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mission mean time between failure (MTBF) "
                      u"for the selected hardware item."))
        self.txtMissionMTBFVar = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the variance on the mission MTBF for the "
                      u"selected hardware item."))
        self.txtMissionRt = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mission reliability for the selected "
                      u"hardware item."))
        self.txtMissionRtVar = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the variance on the mission reliability for "
                      u"the selected hardware item."))
        self.txtMMT = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mean maintenance time (MMT) for the "
                      u"selected hardware item.  This includes preventive and "
                      u"corrective maintenance."))
        self.txtMPMT = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mean preventive maintenance time (MPMT) "
                      u"for the selected hardware item."))
        self.txtMTTR = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mean time to repair (MTTR) for the "
                      u"selected hardware item."))
        self.txtPartCount = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            tooltip=_(u"Displays the total part count for the selected "
                      u"hardware item."))
        self.txtPercentHt = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            tooltip=_(u"Displays the percentage of the system failure "
                      u"intensity the selected hardware item represents."))
        self.txtSoftwareHt = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the software failure intensity for the "
                      u"selected hardware item."))
        self.txtTotalCost = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            tooltip=_(u"Displays the total cost of the selected hardware "
                      u"item."))

        self.pack_start(self._make_buttonbox(), expand=False, fill=False)
        self.pack_start(self._make_page(), expand=True, fill=True)
        self.show_all()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._do_load_page, 'selected_hardware')
        pub.subscribe(self._do_load_page, 'calculated_hardware')

    def _do_clear_page(self):
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
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

        # Clear the component-specific gtk.ScrolledWindow()s.
        for _child in self.scwReliability.get_children():
            self.scwReliability.remove(_child)

        for _child in self.scwStress.get_children():
            self.scwStress.remove(_child)

        return None

    def _do_load_page(self, attributes):
        """
        Load the assessment result page widgets with attribute values.

        :param dict attributes: a dict of attribute key:value pairs for the
                                selected Hardware.
        :return: None
        :rtype: None
        """
        self._hardware_id = attributes['hardware_id']

        # Retrieve the appropriate component-specific work views and add them
        # to the gtk.ScrolledWindow()s.
        try:
            _component_ar = self._dic_assessment_results[
                attributes['category_id']]
        except KeyError:
            _component_ar = None

        _component_sr = Component.StressResults()

        self.txtTotalCost.set_text(
            str(locale.currency(attributes['total_cost'])))
        self.txtCostFailure.set_text(
            str(locale.currency(attributes['cost_failure'])))
        self.txtCostHour.set_text(
            str(locale.currency(attributes['cost_hour'])))
        self.txtPartCount.set_text(
            str('{0:d}'.format(attributes['total_part_count'])))

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

        self.txtLogisticsAt.set_text(
            str(self.fmt.format(attributes['availability_logistics'])))
        self.txtLogisticsAtVar.set_text(
            str(self.fmt.format(attributes['avail_log_variance'])))
        self.txtLogisticsHt.set_text(
            str(self.fmt.format(attributes['hazard_rate_logistics'])))
        self.txtLogisticsHtVar.set_text(
            str(self.fmt.format(attributes['hr_logistics_variance'])))
        self.txtLogisticsMTBF.set_text(
            str(self.fmt.format(attributes['mtbf_logistics'])))
        self.txtLogisticsMTBFVar.set_text(
            str(self.fmt.format(attributes['mtbf_log_variance'])))
        self.txtLogisticsRt.set_text(
            str(self.fmt.format(attributes['reliability_logistics'])))
        self.txtLogisticsRtVar.set_text(
            str(self.fmt.format(attributes['reliability_log_variance'])))

        self.txtMissionAt.set_text(
            str(self.fmt.format(attributes['availability_mission'])))
        self.txtMissionAtVar.set_text(
            str(self.fmt.format(attributes['avail_mis_variance'])))
        self.txtMissionHt.set_text(
            str(self.fmt.format(attributes['hazard_rate_mission'])))
        self.txtMissionHtVar.set_text(
            str(self.fmt.format(attributes['hr_mission_variance'])))
        self.txtMissionMTBF.set_text(
            str(self.fmt.format(attributes['mtbf_mission'])))
        self.txtMissionMTBFVar.set_text(
            str(self.fmt.format(attributes['mtbf_miss_variance'])))
        self.txtMissionRt.set_text(
            str(self.fmt.format(attributes['reliability_mission'])))
        self.txtMissionRtVar.set_text(
            str(self.fmt.format(attributes['reliability_miss_variance'])))

        # Clear the component-specific gtk.ScrolledWindow()s if it already
        # contains a component-specific work view objects.  Then load the new
        # component-specific work view object.
        _child = self.scwReliability.get_child().get_children()[0]
        try:
            _child.remove(_child.get_child())
        except TypeError:
            pass

        if _component_ar is not None:
            _child.add(_component_ar)

        _child = self.scwStress.get_child().get_children()[0]
        try:
            _child.remove(_child.get_child())
        except TypeError:
            pass

        if _component_sr is not None:
            _child.add(_component_sr)

        # Set the calculate button sensitive only if the selected hardware
        # item is a part.
        if attributes['part'] == 1:
            self.get_children()[0].get_children()[0].set_sensitive(True)
        else:
            self.get_children()[0].get_children()[0].set_sensitive(False)

        self.scwReliability.show_all()
        self.scwStress.show_all()

        # Send the PyPubSub message to let the component-specific widgets know
        # they can load.
        pub.sendMessage(
            'loaded_hardware_results', fmt=self.fmt, attributes=attributes)

        return None

    def _do_request_calculate(self, __button):
        """
        Send request to calculate the selected Hardware item.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _multiplier = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_HR_MULTIPLIER
        pub.sendMessage(
            'request_calculate_hardware',
            node_id=self._hardware_id,
            hr_multiplier=_multiplier)

        return None

    def _do_request_update(self, __button):
        """
        Send request to save the currently selected Hardware item.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(gtk.gdk.WATCH)
        pub.sendMessage('request_update_hardware', node_id=self._hardware_id)
        self.do_set_cursor(gtk.gdk.LEFT_PTR)

        return None

    def _do_request_update_all(self, __button):
        """
        Send request to save all Hardware items.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(gtk.gdk.WATCH)
        pub.sendMessage('request_update_all_hardware')
        self.do_set_cursor(gtk.gdk.LEFT_PTR)

        return None

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the gtk.ButtonBox() for the Hardware class Work View.

        :return: _buttonbox; the gtk.ButtonBox() for the Hardware class Work
                 View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [_(u"Calculate the currently selected Hardware item.")]
        _callbacks = [self._do_request_calculate]

        _icons = ['calculate']

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
        Make the Hardware class gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _hbox = gtk.HBox()

        # Build the assessment results page starting with the top left half.
        _vpaned = gtk.VPaned()

        _frame = ramstk.RAMSTKFrame(label=_(u"Reliability Results"))
        _vpaned.pack1(_frame, True, True)

        _fixed = gtk.Fixed()
        _scrollwindow = ramstk.RAMSTKScrolledWindow(_fixed)
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = ramstk.make_label_group(self._lst_labels[0], _fixed,
                                                 5, 5)
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

        # Now add the bottom left pane.  This is just an RAMSTKScrolledwindow()
        # and will be the container for component-specific reliability results.
        _frame = ramstk.RAMSTKFrame(label=_(u"Assessment Model Results"))
        _frame.add(self.scwReliability)

        _vpaned.pack2(_frame, True, True)

        _hbox.pack_start(_vpaned, expand=True, fill=True)

        # Now add the top right pane.
        _vpaned = gtk.VPaned()
        _fixed = gtk.Fixed()

        _scrollwindow = ramstk.RAMSTKScrolledWindow(_fixed)
        _frame = ramstk.RAMSTKFrame(label=_(u"Availability Results"))
        _frame.add(_scrollwindow)

        _vpaned.pack1(_frame, True, True)

        _x_pos, _y_pos = ramstk.make_label_group(self._lst_labels[1], _fixed,
                                                 5, 5)
        _x_pos += 50

        _fixed.put(self.txtLogisticsAt, _x_pos, _y_pos[0])
        _fixed.put(self.txtLogisticsAtVar, _x_pos + 135, _y_pos[0])
        _fixed.put(self.txtMissionAt, _x_pos, _y_pos[1])
        _fixed.put(self.txtMissionAtVar, _x_pos + 135, _y_pos[1])
        _fixed.put(self.txtTotalCost, _x_pos, _y_pos[2])
        _fixed.put(self.txtCostFailure, _x_pos, _y_pos[3])
        _fixed.put(self.txtCostHour, _x_pos, _y_pos[4])
        _fixed.put(self.txtPartCount, _x_pos, _y_pos[5])

        # Finally, add the bottom right pane.  This is just an RAMSTKFrame() and
        # will be the container for component-specific design attributes.
        _frame = ramstk.RAMSTKFrame(label=_(u"Stress Results"))
        _frame.add(self.scwStress)
        _vpaned.pack2(_frame, True, True)

        _hbox.pack_end(_vpaned, expand=True, fill=True)

        _frame = gtk.Frame()
        self.scwReliability.add_with_viewport(_frame)

        _frame = gtk.Frame()
        self.scwStress.add_with_viewport(_frame)

        _label = ramstk.RAMSTKLabel(
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
