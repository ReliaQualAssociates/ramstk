# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.similar_item.view.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Similar Item Views."""

# Standard Library Imports
from typing import Dict, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.assistants import EditFunction
from ramstk.views.gtk3.widgets import RAMSTKPanel, RAMSTKWorkView

# RAMSTK Local Imports
from . import SimilarItemMethodPanel, SimilarItemTreePanel


class SimilarItemWorkView(RAMSTKWorkView):
    """Display Similar Item attribute data in the Work Book.

    The WorkView displays all the attributes for the Similar Item Analysis. The
    attributes of a SimilarItem Work View are:

    :cvar str _tag: the name of the module.

    :ivar dict _dic_hardware: dict to hold information from the Hardware
        module.
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
    :ivar int _hardware_id: the Hardware ID of the selected Similar Item.
    :ivar int _method_id: the ID of the similar item method to use.
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag: str = "similar_item"
    _tablabel: str = _("Similar Item")
    _tabtooltip: str = _(
        "Displays the Similar Item analysis for the selected hardware item."
    )

    # Define public dictionary class attributes.

    # Define public dictionary list attributes.

    # Define public dictionary scalar attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the Hardware Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration:
            :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks.insert(0, self._do_request_edit_function)
        self._lst_callbacks.insert(1, self._do_request_rollup)
        self._lst_callbacks.insert(2, self._do_request_calculate)
        self._lst_icons.insert(0, "edit")
        self._lst_icons.insert(1, "rollup")
        self._lst_icons.insert(2, "calculate")
        self._lst_mnu_labels = [
            _("Edit User Functions"),
            _("Roll-Up Descriptions"),
            _("Calculate Similar Item"),
            _("Save"),
            _("Save All"),
        ]
        self._lst_tooltips = [
            _("Edit the similar item analysis user defined functions."),
            _("Roll up descriptions to next higher level assembly."),
            _("Calculate the similar item analysis."),
            _("Save changes to the selected similar item analysis line item."),
            _("Save changes to all similar item analysis line items."),
        ]

        # Initialize private scalar attributes.
        self._pnlMethod: RAMSTKPanel = SimilarItemMethodPanel()
        self._pnlPanel: RAMSTKPanel = SimilarItemTreePanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            super().do_set_cursor_active,
            "succeed_roll_up_change_descriptions",
        )

        pub.subscribe(
            self._do_set_record_id,
            "selected_hardware",
        )

    def _do_set_record_id(self, attributes: Dict[str, Union[float, int, str]]) -> None:
        """Set the Similar Items's record ID.

        :param attributes: the attribute dict for the selected Similar Item record.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["parent_id"] = attributes["parent_id"]
        self.dic_pkeys["record_id"] = attributes["hardware_id"]

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """Request to iteratively calculate the Similar Item metrics.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        _model = self._pnlPanel.tvwTreeView.get_model()
        _row = _model.get_iter_first()

        # Iterate through the assemblies and calculate the Similar Item hazard
        # intensities.
        super().do_set_cursor_busy()
        _node_ids = []
        while _row is not None:
            _node_ids.append(_model.get_value(_row, 1))
            _row = _model.iter_next(_row)

        for _node_id in _node_ids:
            pub.sendMessage("request_calculate_similar_item", node_id=_node_id)

    def _do_request_edit_function(self, __button: Gtk.ToolButton) -> None:
        """Request to edit the Similar Item analysis user-defined functions.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        (
            _model,
            _row,
        ) = self._pnlPanel.tvwTreeView.get_selection().get_selected()  # noqa

        _dialog = EditFunction(
            self._pnlPanel.tvwTreeView,
            dlgparent=self.get_parent().get_parent().get_parent().get_parent(),
            module="Similar Item",
            labels=[
                _(
                    "You can define up to five functions.  "
                    "You can use the system failure rate, "
                    "selected assembly failure rate, the "
                    "change factor, the user float, the "
                    "user integer values, and results of "
                    "other functions.\n\n \
        System hazard rate is hr_sys\n \
        Assembly hazard rate is hr\n \
        Change factor is pi[1-8]\n \
        User float is uf[1-3]\n \
        User integer is ui[1-3]\n \
        Function result is res[1-5]\n\n"
                ),
                _(
                    "For example, pi1*pi2+pi3, multiplies "
                    "the first two change factors and "
                    "adds the value to the third change "
                    "factor.\n\n"
                ),
            ],
            edit_message="wvw_editing_similar_item",
            id_column=1,
            func_columns=[30, 31, 32, 33, 34],
        )

        if _dialog.do_run() == Gtk.ResponseType.OK:
            _functions = _dialog.do_set_functions(self._pnlPanel.tvwTreeView)
            if _dialog.chkApplyAll.get_active():
                _row = _model.get_iter_first()
                while _row is not None:
                    self._pnlPanel.do_refresh_functions(_row, _functions)
                    _row = _model.iter_next(_row)
            else:
                self._pnlPanel.do_refresh_functions(_row, _functions)

        _dialog.do_destroy()

    def _do_request_rollup(self, __button: Gtk.ToolButton) -> None:
        """Request to roll-up the Similar Item change descriptions.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage(
            "request_roll_up_change_descriptions",
            node=self._pnlPanel.tree.get_node(self.dic_pkeys["record_id"]),
        )

    def __make_ui(self) -> None:
        """Build the user interface for the Similar Item tab.

        :return: None
        :rtype: None
        """
        _hpaned: Gtk.HPaned = super().do_make_layout_lr()

        super().do_embed_treeview_panel()
        self._pnlPanel.do_load_comboboxes()
        self._pnlMethod.do_load_comboboxes()

        self.remove(self.get_children()[-1])
        _hpaned.pack1(self._pnlMethod, True, True)
        _hpaned.pack2(self._pnlPanel, True, True)

        self.show_all()
