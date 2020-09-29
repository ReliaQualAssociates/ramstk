# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 panel Module."""

# Standard Library Imports
from typing import Any, Dict, List, Union

# Third Party Imports
# pylint: disable=ungrouped-imports
# noinspection PyPackageValidations
from pandas.plotting import register_matplotlib_converters
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gdk, Gtk
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton, RAMSTKComboBox, RAMSTKEntry, RAMSTKFrame, RAMSTKPlot,
    RAMSTKScrolledWindow, RAMSTKTextView, RAMSTKTreeView, do_make_label_group
)

register_matplotlib_converters()


class RAMSTKPanel(RAMSTKFrame):
    """The RAMSTKPanel class.

    Implementations of the RAMSTKPanel() class should provide the following
    methods:

    __do_set_callbacks() to set the callback method for the widgets in the
        panel.  The use of the public methods on_changed_combo(),
        on_changed_text(), on_focus_out(), and on_toggled() in this
        meta-class shall be the preferred callback methods.
    __do_set_properties() to set the properties of the widgets in the panel.

    Implementations of the RAMSTKPanel() class may provide the following
    methods:

    _do_clear_panel() to clear the contents of the widgets in the panel.
        Connect this as a listener for the 'closed_program' signal.
    _do_load_panel() to load the attribute data into the widgets in the
        panel.  Connect this as a listener for the 'selected_<module>' for
        the work stream module the panel is associated with.

    There are three types of panels that can be created.  These are:

        * fixed: a panel containing a Gtk.Fixed() populated with labels
            and widgets.
        * plot: a panel containing a RAMSTKPlot().
        * treeview: a panel containing a RAMSTKTreeView().

    The attributes of a RAMSTKPanel are:

    :ivar dict _dic_attribute_keys: contains key:value pairs where the key is
    the index of the widget displaying the associated attribute and the value
    is a list with the name of the attribute in position 0 and the attribute's
    data type in position 1.  An example entry in this dict might be:

        0: ['name', 'string']

    :ivar dict _dic_attribute_updater: contains key:value pairs where the
        key is the name of the attribute and the value is a list with the
        method used to update a widget's display in position 0 and the name of
        the signal to block while updating the widget in position 1.  An
        example entry in this dict might be:

        'name': [self.txtName.do_update, 'changed']

    :ivar list _lst_labels: the list of text to display in the labels
        for each widget in a panel.
    :ivar list _lst_widgets: the list of widgets to display in a panel.
    :ivar int _record_id: the work stream module ID whose attributes
        this panel is displaying.
    :ivar str _title: the title to place on the RAMSTKFrame() that is
        this panel's container.

    :ivar tvwTreeView: a RAMSTKTreeView() for the panels that embed a
        treeview.
    :ivar pltPlot: a RAMSTPlot() for the panels that embed a plot.
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKPanel.

        :return: None
        :rtype: None
        """
        super().__init__()

        # Initialize private dict instance attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {}
        self._dic_attribute_updater: Dict[str, Union[object, str]] = {}

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = []
        self._lst_widgets: List[object] = []

        # Initialize private scalar instance attributes.
        self._record_id: int = -1
        self._title: str = ''

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.fmt: str = '{0:0.6}'

        self.pltPlot: RAMSTKPlot = RAMSTKPlot()
        self.tvwTreeView: RAMSTKTreeView = RAMSTKTreeView()

    def do_make_panel_fixed(self, **kwargs: Dict[str, Any]) -> None:
        """Create a panel with the labels and widgets on a Gtk.Fixed().

        :return: None
        :rtype: None
        """
        _justify = kwargs.get('justify', Gtk.Justification.RIGHT)

        _fixed: Gtk.Fixed = Gtk.Fixed()

        _y_pos: int = 5
        (_x_pos, _labels) = do_make_label_group(self._lst_labels,
                                                bold=False,
                                                justify=_justify,
                                                x_pos=5,
                                                y_pos=5)
        for _idx, _label in enumerate(_labels):
            _fixed.put(_label, 5, _y_pos)

            _minimum: Gtk.Requisition = self._lst_widgets[  # type: ignore
                _idx].get_preferred_size()[0]
            if _minimum.height == 0:
                _minimum.height = self._lst_widgets[  # type: ignore
                    _idx].height

            # RAMSTKTextViews are placed inside a scrollwindow so that's
            # what needs to be placed on the container.
            if isinstance(self._lst_widgets[_idx], RAMSTKTextView):
                _fixed.put(
                    self._lst_widgets[_idx].scrollwindow,  # type: ignore
                    _x_pos + 5,
                    _y_pos)
                _y_pos += _minimum.height + 30
            else:
                _fixed.put(self._lst_widgets[_idx], _x_pos + 5, _y_pos)
                _y_pos += _minimum.height + 5

        _scrollwindow: RAMSTKScrolledWindow = RAMSTKScrolledWindow(_fixed)

        self.add(_scrollwindow)

    def do_make_panel_plot(self) -> None:
        """Create a panel with a RAMSTKPlot().

        :return: None
        :rtype: None
        """
        self._lst_widgets.append(self.pltPlot)

        _scrollwindow: Gtk.ScrolledWindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                 Gtk.PolicyType.AUTOMATIC)
        _scrollwindow.add(self.pltPlot.canvas)

        self.add(_scrollwindow)

    def do_make_panel_treeview(self) -> None:
        """Create a panel with a RAMSTKTreeView().

        :param treeview: the RAMSTKTreeView() to embed in the panel.
        :type treeview: :class:`ramstk.views.gtk3.widgets.RAMSTKTreeView`
        :return: None
        :rtype: None
        """
        self._lst_widgets.append(self.tvwTreeView)

        _scrollwindow: Gtk.ScrolledWindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                 Gtk.PolicyType.AUTOMATIC)
        _scrollwindow.add(self.tvwTreeView)

        self.add(_scrollwindow)

    def on_cell_edit(self, cell: Gtk.CellRenderer, path: str, new_text: str,
                     position: int, message: str) -> None:
        """Handle edits of the RAMSTKTreeview() in a treeview panel.

        :param cell: the Gtk.CellRenderer() that was edited.
        :type cell: :class:`Gtk.CellRenderer`
        :param str path: the RAMSTKTreeView() path of the Gtk.CellRenderer()
            that was edited.
        :param str new_text: the new text in the edited Gtk.CellRenderer().
        :param int position: the column position of the edited
            Gtk.CellRenderer().
        :param str message: the PyPubSub message to publish.
        :return: None
        :rtype: None
        """
        _lst_column_order: List[int] = list(self.tvwTreeView.position.values())

        try:
            _key = self._dic_attribute_keys[_lst_column_order[position]]
            if not self.tvwTreeView.do_edit_cell(cell, path, new_text,
                                                 position):
                pub.sendMessage(message,
                                node_id=[self.parent_id, self._record_id, ''],
                                package={_key: new_text})
        except KeyError:
            pass

    def on_changed_combo(self, combo: RAMSTKComboBox, index: int,
                         message: str) -> Dict[Union[str, Any], Any]:
        """Retrieve changes made in RAMSTKComboBox() widgets.

        This method publishes the PyPubSub message that it is passed.  This
        is usually sufficient to ensure the attributes are updated by the
        datamanager.  This method also return a dict with {_key: _new_text}
        if this information is needed by the child class.

        :param combo: the RAMSTKComboBox() that called the method.
        :type combo: :class:`ramstk.views.gtk3.widgets.RAMSTKComboBox`
        :param int index: the position in the class' Gtk.TreeModel() associated
            with the attribute from the calling Gtk.Widget().
        :param str message: the PyPubSub message to publish.
        :return: {_key: _new_text}; the work stream module's attribute name
            and the new value from the RAMSTKComboBox().  The value {'': -1}
            will be returned when a KeyError or ValueError is raised by this
            method.
        :rtype: dict
        """
        _key: str = ''
        _new_text: int = -1

        combo.handler_block(combo.dic_handler_id['changed'])

        try:
            _key = self._dic_attribute_keys[index][0]

            _new_text = int(combo.get_active())

            # Only if something is selected should we send the message.
            # Otherwise attributes get updated to a value of -1 which isn't
            # correct.  And it sucks trying to figure out why, so leave the
            # conditional unless you have a more elegant (and there prolly
            # is) solution.
            if _new_text > -1:
                pub.sendMessage(message,
                                node_id=[self._record_id, -1],
                                package={_key: _new_text})

        except (KeyError, ValueError):
            pass

        combo.handler_unblock(combo.dic_handler_id['changed'])

        return {_key: _new_text}

    def on_changed_text(self, entry: RAMSTKEntry, index: int,
                        message: str) -> Dict[Union[str, Any], Any]:
        """Retrieve changes made in RAMSTKEntry() widgets.

        This method is called by:

            * RAMSTKEntry() 'changed' signal

        This method publishes the PyPubSub message that it is passed.  This
        is usually sufficient to ensure the attributes are updated by the
        datamanager.  This method also return a dict with {_key: _new_text}
        if this information is needed by the child class.

        :param entry: the RAMSTKEntry() that called the method.
        :type entry: :class:`ramstk.views.gtk3.widgets.RAMSTKEntry` or
        :class:`ramstk.views.gtk3.widgets.RAMSTKTextView`
        :param int index: the position in the class' Gtk.TreeModel() associated
            with the data from the calling RAMSTKEntry() or RAMSTKTextView().
        :param str message: the PyPubSub message to publish.
        :return: {_key: _new_text}; the child module attribute name and the
            new value from the RAMSTKEntry() or RAMSTKTextView(). The value
            {'': ''} will be returned when a KeyError or ValueError is raised
            by this method.
        :rtype: dict
        """
        _key: str = ''
        _new_text: Any = ''
        _type: str = 'string'

        entry.handler_block(entry.dic_handler_id['changed'])

        try:
            _key = self._dic_attribute_keys[index][0]
            _type = self._dic_attribute_keys[index][1]

            _new_text = {
                'float': float(entry.do_get_text()),
                'integer': int(entry.do_get_text()),
                'string': str(entry.do_get_text()),
            }[_type]

            pub.sendMessage(message,
                            node_id=[self._record_id, -1, -1],
                            package={_key: _new_text})
        except (KeyError, ValueError):
            pass

        entry.handler_unblock(entry.dic_handler_id['changed'])

        return {_key: _new_text}

    # pylint: disable=unused-argument
    def on_edit(self, node_id: List[int], package: Dict[str, Any]) -> None:
        """Update the panel's Gtk.Widgets() when attributes are changed.

        This method is called whenever an attribute is edited in the module
        view.

        :param list node_id: the list of IDs of the work stream module item
            being edited.  This unused parameter is part of the PyPubSub
            message data package that this method responds to so it must
            remain in the argument list.
        :param dict package: a dict containing the attribute name as key and
            the new attribute value as the value.
        :return: None
        :rtype: None
        """
        [[_key, _value]] = package.items()

        (_function,
         _signal) = self._dic_attribute_updater.get(_key)  # type: ignore
        _function(_value, _signal)  # type: ignore

    # pylint: disable=unused-argument
    def on_focus_out(self, entry: object, __event: Gdk.EventFocus, index: int,
                     message: str) -> Dict[Union[str, Any], Any]:
        """Retrieve changes made in RAMSTKTextView() widgets.

        This method is called by:

            * RAMSTKTextView() 'focus-out-event' signal

        :param entry: the Gtk.TextBuffer() calling this method.
        :param __event: the Gdk.Event() that occurred in the RAMSTKTextView().
        :param index: the position in the class' Gtk.TreeModel() associated
            with the data from the calling RAMSTKTextView().
        :param message: the pypubsub message to broadcast.
        :return: {_key: _new_text}; the child module attribute name and the
            new value from the RAMSTKTextView(). The value {'': ''} will be
            returned when a KeyError or ValueError is raised by this method.
        :rtype: dict
        """
        return self.on_changed_text(entry, index, message)

    def on_toggled(self, checkbutton: RAMSTKCheckButton, index: int,
                   message: str) -> Dict[Union[str, Any], Any]:
        """Retrieve changes made in RAMSTKCheckButton() widgets.

        :param checkbutton: the RAMSTKCheckButton() that was toggled.
        :type checkbutton: :class:`ramstk.views.gtk3.widgets.RAMSTKCheckButton`
        :param int index: the position in the class' Gtk.TreeModel() associated
            with the data from the calling RAMSTKCheckButton().
        :param str message: the PyPubSub message to broadcast.
        :return: {_key: _new_text}; the child module attribute name and the
            new value from the RAMSTKEntry() or RAMSTKTextView(). The value
            {'': -1} will be returned when a KeyError is raised by this method.
        :rtype: dict
        """
        _key: str = ''
        _new_text: int = -1

        try:
            _key = self._dic_attribute_keys[index][0]

            _new_text = int(checkbutton.get_active())
            checkbutton.do_update(_new_text, signal='toggled')

            pub.sendMessage(message,
                            node_id=[self._record_id, -1, ''],
                            package={_key: _new_text})

        except KeyError:
            pass

        return {_key: _new_text}
