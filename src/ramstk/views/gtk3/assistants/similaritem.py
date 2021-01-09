# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.assistants.similaritem.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RASMTK Similar Item Analysis Assistants Module."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton, RAMSTKDialog, RAMSTKEntry, RAMSTKLabel, RAMSTKTreeView
)


class EditFunction(RAMSTKDialog):
    """Assistant for editing similar item functions."""
    def __init__(self, treeview: RAMSTKTreeView, **kwargs: Dict[str,
                                                                Any]) -> None:
        """Initialize instance of the Similar Item Function Editor Assistant.

        :param treeview: the Similar Item Work View RAMSTKTreeView().
        :type treeview: :class:`ramstk.views.gtk3.RAMSTKTreeView`
        """
        _dlgparent = kwargs['dlgparent']
        super().__init__(
            _("RAMSTK Similar Item Analysis User Function Editing Assistant"),
            dlgparent=_dlgparent)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.chkApplyAll: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Apply to all assemblies."))
        self.txtFunction1: RAMSTKEntry = RAMSTKEntry()
        self.txtFunction2: RAMSTKEntry = RAMSTKEntry()
        self.txtFunction3: RAMSTKEntry = RAMSTKEntry()
        self.txtFunction4: RAMSTKEntry = RAMSTKEntry()
        self.txtFunction5: RAMSTKEntry = RAMSTKEntry()

        self.__make_ui()
        self._do_load_functions(treeview)

    def __make_ui(self) -> None:
        """Build the user interface.

        :return: None
        :rtype: None
        """
        self.set_default_size(610, -1)

        _label1: RAMSTKLabel = RAMSTKLabel(
            _("You can define up to five functions.  "
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
        Function result is res[1-5]\n\n"))
        _label1.do_set_properties(width=600, height=-1, wrap=True)
        _height1 = _label1.get_attribute('height')

        _label2: RAMSTKLabel = RAMSTKLabel(
            _("For example, pi1*pi2+pi3, multiplies "
              "the first two change factors and "
              "adds the value to the third change "
              "factor.\n\n"))
        _label2.do_set_properties(width=600, height=-1, wrap=True)
        _height2 = _label2.get_attribute('height')

        # Build the dialog assistant.
        _fixed = Gtk.Fixed()

        _y_pos = 10
        _fixed.put(_label1, 5, _y_pos)
        _y_pos += (_height1 + 50)
        _fixed.put(_label2, 5, _y_pos)
        _y_pos += (_height2 + 30)

        _separator = Gtk.HSeparator()
        _separator.props.width_request = 600
        _fixed.put(_separator, 5, _y_pos)
        _y_pos += 20

        _label = RAMSTKLabel(_("User function 1:"))
        _fixed.put(_label, 5, _y_pos)
        _fixed.put(self.txtFunction1, 195, _y_pos)
        _y_pos += 30

        _label = RAMSTKLabel(_("User function 2:"))
        _fixed.put(_label, 5, _y_pos)
        _fixed.put(self.txtFunction2, 195, _y_pos)
        _y_pos += 30

        _label = RAMSTKLabel(_("User function 3:"))
        _fixed.put(_label, 5, _y_pos)
        _fixed.put(self.txtFunction3, 195, _y_pos)
        _y_pos += 30

        _label = RAMSTKLabel(_("User function 4:"))
        _fixed.put(_label, 5, _y_pos)
        _fixed.put(self.txtFunction4, 195, _y_pos)
        _y_pos += 30

        _label = RAMSTKLabel(_("User function 5:"))
        _fixed.put(_label, 5, _y_pos)
        _fixed.put(self.txtFunction5, 195, _y_pos)
        _y_pos += 30

        _fixed.put(self.chkApplyAll, 5, _y_pos)

        _fixed.show_all()

        self.vbox.pack_start(_fixed, True, True, 0)

    def do_set_functions(self, treeview: RAMSTKTreeView) -> List[str]:
        """Set the user-defined functions.

        :return: functions; a tuple of the five user-defined functions.
        :rtype: list
        """
        (_model, _row) = treeview.get_selection().get_selected()
        if self.chkApplyAll.get_active():
            _row = _model.get_iter_first()
            while _row is not None:
                _hardware_id = _model.get_value(_row, 1)
                self._on_set_function(_hardware_id)
                _row = _model.iter_next(_row)
        else:
            _hardware_id = _model.get_value(_row, 1)
            self._on_set_function(_hardware_id)

        return [
            str(self.txtFunction1.get_text()),
            str(self.txtFunction2.get_text()),
            str(self.txtFunction3.get_text()),
            str(self.txtFunction4.get_text()),
            str(self.txtFunction5.get_text())
        ]

    def _cancel(self, __button: Gtk.Button) -> None:
        """Destroy the assistant when the 'Cancel' button is pressed.

        :param Gtk.Button __button: the Gtk.Button() that called this method.
        :return: None
        :rtype: None
        """
        self.destroy()

    def _do_load_functions(self, treeview: RAMSTKTreeView) -> None:
        """Load any existing user-defined functions.

        :param treeview: the Similar Item Work View RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.TreeView.RAMSTKTreeView`
        :return: None
        :rtype: None
        """
        (_model, _row) = treeview.get_selection().get_selected()
        try:
            self.txtFunction1.set_text(_model.get_value(_row, 30))
        except TypeError:
            self.txtFunction1.set_text("")
        try:
            self.txtFunction2.set_text(_model.get_value(_row, 31))
        except TypeError:
            self.txtFunction2.set_text("")
        try:
            self.txtFunction3.set_text(_model.get_value(_row, 32))
        except TypeError:
            self.txtFunction3.set_text("")
        try:
            self.txtFunction4.set_text(_model.get_value(_row, 33))
        except TypeError:
            self.txtFunction4.set_text("")
        try:
            self.txtFunction5.set_text(_model.get_value(_row, 34))
        except TypeError:
            self.txtFunction5.set_text("")

    def _on_set_function(self, hardware_id: int) -> None:
        """Send PyPubSub messages to update the similar item attributes.

        :param hardware_id: the Hardware ID for the Similar Item to update.
        :return: None
        :rtype: None
        """
        pub.sendMessage(
            'wvw_editing_similar_item',
            node_id=[hardware_id, -1],
            package={'function_1': str(self.txtFunction1.get_text())})
        pub.sendMessage(
            'wvw_editing_similar_item',
            node_id=[hardware_id, -1],
            package={'function_2': str(self.txtFunction2.get_text())})
        pub.sendMessage(
            'wvw_editing_similar_item',
            node_id=[hardware_id, -1],
            package={'function_3': str(self.txtFunction3.get_text())})
        pub.sendMessage(
            'wvw_editing_similar_item',
            node_id=[hardware_id, -1],
            package={'function_4': str(self.txtFunction4.get_text())})
        pub.sendMessage(
            'wvw_editing_similar_item',
            node_id=[hardware_id, -1],
            package={'function_5': str(self.txtFunction5.get_text())})
