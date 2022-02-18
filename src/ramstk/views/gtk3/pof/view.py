# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.pof.view.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 PoF Views."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.assistants import AddStressTestMethod
from ramstk.views.gtk3.widgets import RAMSTKPanel, RAMSTKWorkView

# RAMSTK Local Imports
from . import PoFTreePanel


class PoFWorkView(RAMSTKWorkView):
    """Display PoF attribute data in the Work Book.

    The WorkView displays all the attributes for the Physics of Failure
    Analysis (PoF). The attributes of a PoF Work View are:

    :cvar dict _dic_column_masks: dict with the list of masking values for
        the PoF worksheet.  Key is the PoF indenture level, value is a
        list of True/False values for each column in the worksheet.
    :cvar dict _dic_headings: the dict with the variable headings for the
        first two columns.  Key is the name of the PoF indenture level,
        value is a list of heading text.
    :cvar dict _dic_keys:
    :cvar dict _dic_column_keys:
    :cvar list _lst_labels: the list of labels for the widgets on the work
        view.  The PoF work stream module has no labels, but an empty list
        is required to prevent an AttributeError when creating the UI.
    :cvar str _tag: the name of the module.
    :cvar bool _pixbuf: indicates whether or icons are displayed in the
        RAMSTKTreeView.  If true, a GDKPixbuf column will be appended when
        creating the RAMSTKTreeView.  Default is True.

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

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag: str = "pof"
    _pixbuf: bool = True
    _tablabel = _("PoF")
    _tabtooltip = _(
        "Displays the Physics of Failure (PoF) Analysis for "
        "the selected hardware item."
    )

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the Work View for the PoF.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dict attributes.

        # Initialize private list attributes.
        self._lst_callbacks.insert(0, self._do_request_insert_sibling)
        self._lst_callbacks.insert(1, self._do_request_insert_child)
        self._lst_callbacks.insert(2, super().do_request_delete)
        self._lst_icons.insert(0, "insert_sibling")
        self._lst_icons.insert(1, "insert_child")
        self._lst_icons.insert(2, "remove")
        self._lst_mnu_labels.insert(0, _("Insert Sibling"))
        self._lst_mnu_labels.insert(1, _("Insert Child"))
        self._lst_mnu_labels.insert(2, _("Delete Selected"))
        self._lst_tooltips: List[str] = [
            _(
                "Add a new PoF entity at the same level as the currently selected "
                "entity."
            ),
            _("Add a new PoF entity one level below the currently selected entity."),
            _("Remove the selected entity from the PoF."),
            _("Save changes to the currently selected PoF line."),
            _("Save changes to all PoF lines."),
        ]

        # Initialize private scalar attributes.
        self._hardware_id: int = 0

        self._pnlPanel: RAMSTKPanel = PoFTreePanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_set_record_id, f"selected_{self._tag}")

        pub.subscribe(
            self._on_get_hardware_attributes, "succeed_get_hardware_attributes"
        )

    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> None:
        """Request to insert a new child entity to the PoF.

        :return: None
        :rtype: None
        """
        _attributes = self.__do_get_pof_ids()

        if self._pnlPanel.level == "opload":
            _level, _no_keys = self.__on_request_insert_opstress_method()
        elif self._pnlPanel.level == "mechanism":
            _level = "opload"
            _no_keys = ["opstress_id", "test_method_id"]
        else:
            print("Raise dialog 'cause can't add child to opstress or test.")
            return

        for _key in _no_keys:
            _attributes.pop(_key)

        super().do_set_cursor_busy()

        pub.sendMessage(f"request_insert_{_level}", attributes=_attributes)

    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> None:
        """Request to insert a new sibling entity to the PoF.

        :return: None
        :rtype: None
        """
        _attributes = self.__do_get_pof_ids()
        _level = self._pnlPanel.level

        if _level in ["opstress", "test_method"]:
            _level, _no_keys = self.__on_request_insert_opstress_method()
        elif _level == "opload":
            _no_keys = ["opstress_id", "test_method_id"]
        else:
            _no_keys = ["opload_id", "opstress_id", "test_method_id"]

        for _key in _no_keys:
            _attributes.pop(_key)

        super().do_set_cursor_busy()

        pub.sendMessage(f"request_insert_{_level}", attributes=_attributes)

    def _on_get_hardware_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the hardware ID.

        :param attributes:
        :return: None
        :rtype: None
        """
        self._hardware_id = attributes["hardware_id"]

    def __do_get_pof_ids(self) -> Dict[str, int]:
        """Read each of the ID columns.

        :return: _attributes
        :rtype: dict
        """
        _attributes = {
            "revision_id": self._revision_id,
            "hardware_id": self._hardware_id,
            "mode_id": 0,
            "mechanism_id": 0,
            "opload_id": 0,
            "opstress_id": 0,
            "test_method_id": 0,
        }

        (
            _model,
            _row,
        ) = self._pnlPanel.tvwTreeView.get_selection().get_selected()

        _attributes["mode_id"] = _model.get_value(_row, 1)
        _attributes["mechanism_id"] = _model.get_value(_row, 2)
        _attributes["opload_id"] = _model.get_value(_row, 3)
        _attributes["opstress_id"] = _model.get_value(_row, 4)
        _attributes["test_method_id"] = _model.get_value(_row, 5)

        return _attributes

    def __do_load_pof_lists(self):
        """Load the Gtk.CellRendererCombo()s associated with test methods.

        :return: None
        :rtype: None
        """
        self._pnlPanel.lst_damage_models = [
            x[1] for x in self.RAMSTK_USER_CONFIGURATION.RAMSTK_DAMAGE_MODELS.items()
        ]
        self._pnlPanel.lst_load_history = [
            x[1] for x in self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOAD_HISTORY.items()
        ]
        self._pnlPanel.lst_measurable_parameters = [
            x[1][1]
            for x in self.RAMSTK_USER_CONFIGURATION.RAMSTK_MEASURABLE_PARAMETERS.items()
        ]

    def __make_ui(self) -> None:
        """Build the user interface for the PoF tab.

        :return: None
        :rtype: None
        """
        super().do_make_layout()

        self._pnlPanel.dic_icons = self._dic_icons

        super().do_embed_treeview_panel()
        self.__do_load_pof_lists()
        self._pnlPanel.do_load_comboboxes()

        self.show_all()

    def __on_request_insert_opstress_method(self) -> Tuple[str, List[str]]:
        """Raise dialog to select whether to add a stress or test method.

        :return: _level; the level to add, opstress or testmethod.
        :rtype: str
        """
        _level = ""
        _no_keys = []

        _dialog = AddStressTestMethod(
            parent=self.get_parent().get_parent().get_parent().get_parent()
        )

        if _dialog.do_run() == Gtk.ResponseType.OK:
            if _dialog.rdoOpStress.get_active():
                _level = "opstress"
                _no_keys = ["test_method_id"]
            elif _dialog.rdoTestMethod.get_active():
                _level = "test_method"
                _no_keys = ["opstress_id"]

        _dialog.do_destroy()

        return _level, _no_keys
