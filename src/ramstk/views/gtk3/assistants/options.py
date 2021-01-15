# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.assistants.options.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Configuration Options Module."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton, RAMSTKDialog, RAMSTKEntry, RAMSTKPanel
)


class EditOptionsPanel(RAMSTKPanel):
    """The panel to display options to be edited."""
    def __init__(self) -> None:
        """Initialize an instance of the Edit Options panel."""
        super().__init__()

        # Initialize private dict instance attributes.
        self._dic_attribute_keys: Dict[int, str] = {
            0: 'site_id',
            1: 'site_name',
            2: 'product_key',
            3: 'expire_on',
            4: 'function_enabled',
            5: 'requirement_enabled',
            6: 'hardware_enabled',
            7: 'software_enabled',
            8: 'rcm_enabled',
            9: 'testing_enabled',
            10: 'incident_enabled',
            11: 'survival_enabled',
            12: 'vandv_enabled',
            13: 'hazard_enabled',
            14: 'stakeholder_enabled',
            15: 'allocation_enabled',
            16: 'similar_item_enabled',
            17: 'fmea_enabled',
            18: 'pof_enabled',
            19: 'rbd_enabled',
            20: 'fta_enabled',
        }

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
            _("Site ID:"),
            _("Site Name:"),
            _("Product Key:"),
            _("Expire Date:"), '', '', '', '', '', '', '', '', '', ''
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("General Information")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.chkFunctions: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Function Module Enabled"))
        self.chkRequirements: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Requirements Module Enabled"))
        self.chkHardware: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Hardware Module Enabled"))
        self.chkSoftware: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Software Module Enabled"))
        self.chkRCM: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("RCM Module Enabled"))
        self.chkTesting: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Engineering Test Module Enabled"))
        self.chkIncident: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Incidents Module Enabled"))
        self.chkSurvival: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Survival Analysis Module Enabled"))
        self.chkValidation: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Validation Module Enabled"))
        self.chkHazards: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Hazards Analysis Module Enabled"))
        self.chkStakeholder: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Stakeholder Analysis Module Enabled"))
        self.chkAllocation: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("R(t) Allocation Module Enabled"))
        self.chkSimilarItem: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Similar Item Analysis Module Enabled"))
        self.chkFMEA: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("(D)FME(C)A Module Enabled"))
        self.chkPoF: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Physics of Failure (PoF) Module Enabled"))
        self.chkRBD: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("RBD Module Enabled"))
        self.chkFTA: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("FTA Module Enabled"))

        self.txtSiteID: RAMSTKEntry = RAMSTKEntry()
        self.txtSiteName: RAMSTKEntry = RAMSTKEntry()
        self.txtProductKey: RAMSTKEntry = RAMSTKEntry()
        self.txtExpireDate: RAMSTKEntry = RAMSTKEntry()

        # Only add the widgets for RAMSTK modules that are ready to be
        # released.
        self._lst_widgets = [
            self.txtSiteID, self.txtSiteName, self.txtProductKey,
            self.txtExpireDate, self.chkFunctions, self.chkRequirements,
            self.chkHardware, self.chkValidation, self.chkHazards,
            self.chkStakeholder, self.chkAllocation, self.chkSimilarItem,
            self.chkFMEA, self.chkPoF
        ]

        self.__do_set_properties()
        super().do_make_panel_fixed()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_panel, 'succeed_get_siteinfo_attributes')

        pub.sendMessage('request_get_option_attributes',
                        node_id=1,
                        table='siteinfo')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the current options.

        :return: None
        :rtype: None
        """
        self.txtSiteID.do_update(str(attributes['site_id']), signal='changed')
        self.txtSiteName.do_update(str(attributes['site_name']),
                                   signal='changed')
        self.txtProductKey.do_update(str(attributes['product_key']),
                                     signal='changed')
        self.txtExpireDate.do_update(str(attributes['expire_on']),
                                     signal='changed')

        self.chkFunctions.do_update(int(attributes['function_enabled']),
                                    signal='toggled')
        self.chkRequirements.do_update(int(attributes['requirement_enabled']),
                                       signal='toggled')
        self.chkHardware.do_update(int(attributes['hardware_enabled']),
                                   signal='toggled')
        self.chkValidation.do_update(int(attributes['vandv_enabled']),
                                     signal='toggled')
        self.chkHazards.do_update(int(attributes['hazard_enabled']),
                                  signal='toggled')
        self.chkStakeholder.do_update(int(attributes['stakeholder_enabled']),
                                      signal='toggled')
        self.chkAllocation.do_update(int(attributes['allocation_enabled']),
                                     signal='toggled')
        self.chkSimilarItem.do_update(int(attributes['similar_item_enabled']),
                                      signal='toggled')
        self.chkFMEA.do_update(int(attributes['fmea_enabled']),
                               signal='toggled')
        self.chkPoF.do_update(int(attributes['pof_enabled']), signal='toggled')

    def __do_set_callbacks(self) -> None:
        """Set EditOption widgets callback methods.

        :return: None
        :rtype: None
        """
        self.chkFunctions.dic_handler_id[
            'toggled'] = self.chkFunctions.connect(
                'toggled',
                super().on_toggled, 4, 'request_set_option_attributes')
        self.chkRequirements.dic_handler_id[
            'toggled'] = self.chkRequirements.connect(
                'toggled',
                super().on_toggled, 5, 'request_set_option_attributes')
        self.chkHardware.dic_handler_id['toggled'] = self.chkHardware.connect(
            'toggled',
            super().on_toggled, 6, 'request_set_option_attributes')
        self.chkHazards.dic_handler_id['toggled'] = self.chkHazards.connect(
            'toggled',
            super().on_toggled, 13, 'request_set_option_attributes')
        self.chkStakeholder.dic_handler_id['toggled'] = \
            self.chkStakeholder.connect(
            'toggled', super().on_toggled, 14, 'request_set_option_attributes')
        self.chkAllocation.dic_handler_id[
            'toggled'] = self.chkAllocation.connect(
                'toggled',
                super().on_toggled, 15, 'request_set_option_attributes')
        self.chkSimilarItem.dic_handler_id[
            'toggled'] = self.chkSimilarItem.connect(
                'toggled',
                super().on_toggled, 16, 'request_set_option_attributes')
        self.chkValidation.dic_handler_id[
            'toggled'] = self.chkValidation.connect(
                'toggled',
                super().on_toggled, 12, 'request_set_option_attributes')
        self.chkFMEA.dic_handler_id['toggled'] = self.chkFMEA.connect(
            'toggled',
            super().on_toggled, 17, 'request_set_option_attributes')
        self.chkPoF.dic_handler_id['toggled'] = self.chkPoF.connect(
            'toggled',
            super().on_toggled, 18, 'request_set_option_attributes')

    def __do_set_properties(self) -> None:
        """Set the widget properties.

        :return: None
        :rtype: None
        """
        self.txtSiteID.do_set_properties(can_focus=False,
                                         editable=False,
                                         width=100)
        self.txtSiteName.do_set_properties(can_focus=False,
                                           editable=False,
                                           width=300)
        self.txtProductKey.do_set_properties(can_focus=False,
                                             editable=False,
                                             width=300)
        self.txtExpireDate.do_set_properties(can_focus=False,
                                             editable=False,
                                             width=100)


class EditOptions(RAMSTKDialog):
    """Provide a GUI to set various RAMSTK configuration options.

    RAMSTK options are stored in the RAMSTK Common database and the RAMSTK
    Program database.  RAMSTK options are site-specific or program-specific and
    apply to all users.  Options should not be confused with user-specific
    configurations preferences which are stored in RAMSTK.conf in each user's
    $HOME/.config/RAMSTK directory and are applicable only to that specific
    user.  Configuration preferences are edited with the Preferences assistant.

    Attributes of the EditOptions are:
    """

    # Define private dict class attributes.

    def __init__(self, parent: object = None) -> None:
        """Initialize an instance of the Options assistant.

        :param parent: the parent window for this assistant.
        """
        super().__init__(_("RAMSTK Program Options Assistant"),
                         dlgparent=parent)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._pnlPanel: RAMSTKPanel = EditOptionsPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.

    def _cancel(self, __button: Gtk.Button):
        """Destroy the assistant when the 'Cancel' button is pressed.

        :param __button: the Gtk.Button() that called this method.
        :type __button: :class:`Gtk.Button`
        """
        self.do_destroy()

    def __make_ui(self) -> None:
        """Build the user interface.

        :return: None
        :rtype: None
        """
        self.set_default_size(800, 500)

        self.vbox.pack_start(self._pnlPanel, True, True, 0)

        self.show_all()
