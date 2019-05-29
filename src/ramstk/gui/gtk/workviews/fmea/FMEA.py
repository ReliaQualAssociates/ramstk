# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.fmea.FMEA.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK base FME(C)A Work View."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk.assistants import AddControlAction
from ramstk.gui.gtk.ramstk import RAMSTKMessageDialog, RAMSTKTreeView
from ramstk.gui.gtk.ramstk.Widget import Gdk, Gtk, _
from ramstk.gui.gtk.workviews.WorkView import RAMSTKWorkView


class FMEA(RAMSTKWorkView):
    """
    Display FMEA attribute data in the Work Book.

    The WorkView displays all the attributes for the Failure Mode and Effects
    Analysis (FMEA). The attributes of a FMEA Work View are:

    :cvar list _lst_control_type: list containing the types of controls that
                                  can be implemented.
    :cvar list _lst_fmea_data: list containing the FMEA row data.

    :ivar dict _dic_missions: a dict containing all this missions associated
    with the selected Revision.
    :ivar dict _dic_mission_phases: a dict containing all the mission phases
    associated with each mission in _dic_missions.
    :ivar float _item_hazard_rate: the hazard rate of the Function or Hardware
    item associated with the FMEA.
    """

    # Define private dict attributes.
    _dic_headings = {
        "mode": [""] * 42,
        "mechanism": [""] * 42,
        "cause": [""] * 42,
        "control": [""] * 42,
        "action": [""] * 42,
    }

    # Define private list attributes.
    _lst_control_type = [_("Prevention"), _("Detection")]
    _lst_fmea_data = [
        0,
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        "",
        "",
        "",
        "",
        0,
        "",
        "",
        "",
        "",
        "",
        0,
        "",
        0,
        "",
        "",
        "",
        "",
        0,
        0,
        0,
        0,
        "",
        None,
        "",
    ]

    def __init__(self, configuration, **kwargs):
        """
        Initialize the Work View for the FMEA.

        :param configuration: the RAMSTK configuration instance.
        :type configuration: :class:`ramstk.RAMSTK.Configuration`
        """
        _module = kwargs["module"]
        RAMSTKWorkView.__init__(self, configuration, module=_module)

        # Initialize private dictionary attributes.
        self._dic_icons["mode"] = (
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            "/32x32/mode.png"
        )
        self._dic_icons["mechanism"] = (
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + "/32x32/mechanism.png"
        )
        self._dic_icons["cause"] = (
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            "/32x32/cause.png"
        )
        self._dic_icons["control"] = (
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + "/32x32/control.png"
        )
        self._dic_icons["action"] = (
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + "/32x32/action.png"
        )

        self._dic_missions = {}
        self._dic_mission_phases = {"": []}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._item_hazard_rate = 0.0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        _module = kwargs["module"]
        if _module == "FFMEA":
            _fmt_file = (
                self.RAMSTK_CONFIGURATION.RAMSTK_CONF_DIR +
                "/layouts/" +
                self.RAMSTK_CONFIGURATION.RAMSTK_FORMAT_FILE["ffmea"]
            )
            _fmt_path = "/root/tree[@name='FFMEA']/column"
        elif _module == "DFMECA":
            _fmt_file = (
                self.RAMSTK_CONFIGURATION.RAMSTK_CONF_DIR + "/layouts/" +
                self.RAMSTK_CONFIGURATION.RAMSTK_FORMAT_FILE["dfmeca"]
            )
            _fmt_path = "/root/tree[@name='DFMECA']/column"

        self.treeview = RAMSTKTreeView(
            _fmt_path,
            0,
            _fmt_file,
            "#FFFFFF",
            "#000000",
            pixbuf=True,
            indexed=True,
        )
        self._lst_col_order = self.treeview.order

        # Subscribe to PyPubSub messages.

    def _do_clear_page(self):
        """
        Clear the contents of the FMEA.

        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _columns = self.treeview.get_columns()

        for _column in _columns:
            self.treeview.remove_column(_column)

        _model.clear()

    def _do_refresh_view(self, model, __path, row):
        """
        Refresh the (D)FME(C)A Work View after a successful calculation.

        :return: None
        :rtype: None
        """
        if row is not None:
            if self._functional:
                _node_id = model.get_value(row, 18)
            else:
                _node_id = model.get_value(row, 43)
            _level = self._get_level(_node_id)
            _node = self._dtc_data_controller.request_do_select(_node_id)

            if _level == "mode":
                model.set_value(
                    row, self._lst_col_order[17],
                    _node.mode_hazard_rate,
                )
                model.set_value(
                    row, self._lst_col_order[19],
                    _node.mode_criticality,
                )
            elif _level in ["mechanism", "cause"]:
                model.set_value(row, self._lst_col_order[24], _node.rpn)
                model.set_value(row, self._lst_col_order[37], _node.rpn_new)

    def _do_request_calculate(self, __button):
        """
        Calculate the FFMEA RPN or criticality.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _criticality = self.chkCriticality.get_active()
        _rpn = self.chkRPN.get_active()

        if not self._dtc_data_controller.request_do_calculate(
                None,
                item_hr=self._item_hazard_rate,
                criticality=_criticality,
                rpn=_rpn,
        ):
            _model = self.treeview.get_model()
            _model.foreach(self._do_refresh_view)
        else:
            _return = True

        # For hardware FMECA needs to display the item criticality.

        if not self._functional:
            _str_item_crit = ""
            _dic_item_crit = self._dtc_data_controller.request_item_criticality(
            )

            for _key in _dic_item_crit:
                _str_item_crit = _str_item_crit + _("{0:s}: {1:g}\n").format(
                    _key, _dic_item_crit[_key],
                )

            self.txtItemCriticality.do_get_buffer().set_text(
                str(_str_item_crit),
            )

        return _return

    def _do_request_delete(self, __button):
        """
        Request to delete the selected entity from the FMEA.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _model, _row = self.treeview.get_selection().get_selected()

        if self._functional:
            _node_id = _model.get_value(_row, 18)
        else:
            _node_id = _model.get_value(_row, 43)

        # Delete the selected entity from the RAMSTK Program database and then
        # refresh the TreeView.

        if not self._dtc_data_controller.request_do_delete(_node_id):
            if self._functional:
                self._on_select(module_id=self._function_id)
            else:
                self._on_select(module_id=self._hardware_id)
        else:
            _return = True

        return _return

    def do_request_insert(self, **kwargs):
        """
        Request to insert a new entity to the FMEA.

        :return: None
        :rtype: None
        """
        _entity_id = kwargs["entity_id"]
        _parent_id = kwargs["parent_id"]
        _level = kwargs["level"]
        _choose = kwargs["choose"]
        _undefined = kwargs["undefined"]

        if _undefined:
            _prompt = _(
                "A FMEA control or an action cannot have a "
                "child entity.",
            )
            _dialog = RAMSTKMessageDialog(
                _prompt, self._dic_icons["error"],
                "error",
            )

            if _dialog.do_run() == Gtk.ResponseType.OK:
                _dialog.do_destroy()

        if _choose:
            _dialog = AddControlAction()

            if _dialog.do_run() == Gtk.ResponseType.OK:
                _control = _dialog.rdoControl.get_active()
                _action = _dialog.rdoAction.get_active()

                if _control:
                    _level = "control"
                elif _action:
                    _level = "action"

            _dialog.do_destroy()

        if not _undefined:
            pub.sendMessage(
                "request_insert_fmea",
                entity_id=_entity_id,
                parent_id=_parent_id,
                level=_level,
            )

    def _do_request_update(self, __button):
        """
        Request to save the currently selected entity in the FMEA.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _model, _row = self.treeview.get_selection().get_selected()

        if self._functional:
            _node_id = _model.get_value(_row, 18)
        else:
            _node_id = _model.get_value(_row, 43)

        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage("request_update_fmea", node_id=_node_id)
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button):
        """
        Request to save all the entities in the FMEA.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        _return = self._dtc_data_controller.request_do_update_all()
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

    def _get_cell_model(self, column):
        """
        Retrieve the Gtk.CellRendererCombo() Gtk.TreeModel().

        :param int column: the column number to retrieve the cell from.
        :return: _model
        :rtype: :class:`Gtk.TreeModel`
        """
        _column = self.treeview.get_column(column)
        _cell = _column.get_cells()[0]
        _model = _cell.get_property("model")
        _model.clear()

        return _model

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the FMEA Work View RAMSTKTreeView().

        :param treeview: the FMEA TreeView RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`.
        :param event: the Gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                      * 1 = left
                      * 2 = scrollwheel
                      * 3 = right
                      * 4 = forward
                      * 5 = backwards
                      * 8 =
                      * 9 =

        :type event: :class:`Gdk.Event`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.

        if event.button == 3:
            _icons = [
                "insert_sibling", "insert_child", "remove", "calculate", "save",
            ]
            _labels = [
                _("Insert Sibling"),
                _("Insert Child"),
                _("Remove"),
                _("Calculate"),
                _("Save"),
            ]
            _callbacks = [
                self._do_request_insert_sibling,
                self._do_request_insert_child,
                self._do_request_delete,
                self._do_request_calculate,
                self._do_request_update_all,
            ]
            RAMSTKWorkView.on_button_press(
                self,
                event,
                icons=_icons,
                labels=_labels,
                callbacks=_callbacks,
            )

        treeview.handler_unblock(self._lst_handler_id[1])

        return _return
