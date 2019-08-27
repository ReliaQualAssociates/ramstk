# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.revision.listview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Failure Definition GTK3List View Module."""

# Standard Library Imports
from typing import Any, Tuple

# Third Party Imports
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, GObject, Gtk, Pango, _
from ramstk.views.gtk3.widgets import (
    RAMSTKListView, RAMSTKMessageDialog, RAMSTKTreeView, do_make_buttonbox
)


class FailureDefinition(RAMSTKListView):
    """
    Display all the Failure Definitions associated with the selected Revision.

    The attributes of the Failure Definition List View are:

    :ivar int _definition_id: the Failure Definition ID of the definition
        selected in the List View.
    """
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager, **kwargs: Any) -> None:
        """
        Initialize the List View for the Failure Definition package.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        RAMSTKListView.__init__(self,
                                configuration,
                                logger,
                                module='failure_definition')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._definition_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_treeview()
        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_tree, 'deleted_definition')
        pub.subscribe(self._do_load_tree, 'inserted_definition')
        pub.subscribe(self._do_load_tree, 'retrieved_definitions')

    def __make_buttonbox(self, **kwargs: Any) -> Gtk.ButtonBox:  # pylint: disable=unused-argument
        """
        Make the buttonbox for the Failure Definition List View.

        :return: _buttonbox; the Gtk.ButtonBox() for the Failure Definition
            List View.
        :rtype: :class:`Gtk.ButtonBox`
        """
        _tooltips = [
            _("Add a new Failure Definition."),
            _("Remove the currently selected Failure Definition.")
        ]
        _callbacks = [self.do_request_insert_sibling, self._do_request_delete]
        _icons = ['add', 'remove']

        _buttonbox = do_make_buttonbox(self,
                                       icons=_icons,
                                       tooltips=_tooltips,
                                       callbacks=_callbacks,
                                       orientation='vertical',
                                       height=-1,
                                       width=-1)

        return _buttonbox

    def __make_treeview(self) -> None:
        """
        Set up the RAMSTKTreeView() for Failure Definitions.

        :return: None
        :rtype: None
        """
        _model = Gtk.ListStore(GObject.TYPE_INT, GObject.TYPE_INT,
                               GObject.TYPE_STRING)
        self.treeview.set_model(_model)

        _cell = Gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('wrap-width', 250)
        _cell.set_property('wrap-mode', Pango.WrapMode.WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _label = Gtk.Label()
        _label.set_line_wrap(True)
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(Gtk.Justification.CENTER)
        _label.set_markup("<span weight='bold'>Revision ID</span>")
        _label.set_use_markup(True)
        _label.show_all()
        _column = Gtk.TreeViewColumn()
        _column.set_widget(_label)
        _column.set_visible(False)
        _column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=0)
        self.treeview.append_column(_column)

        _cell = Gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('wrap-width', 250)
        _cell.set_property('wrap-mode', Pango.WrapMode.WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _label = Gtk.Label()
        _label.set_line_wrap(True)
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(Gtk.Justification.CENTER)
        _label.set_markup("<span weight='bold'>Definition\nNumber</span>")
        _label.set_use_markup(True)
        _label.show_all()
        _column = Gtk.TreeViewColumn()
        _column.set_widget(_label)
        _column.set_visible(True)
        _column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=1)
        self.treeview.append_column(_column)

        _cell = Gtk.CellRendererText()
        _cell.set_property('editable', 1)
        _cell.set_property('wrap-width', 450)
        _cell.set_property('wrap-mode', Pango.WrapMode.WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _cell.connect('edited', self._on_cell_edit, 2, _model)
        _label = Gtk.Label()
        _label.set_line_wrap(True)
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(Gtk.Justification.CENTER)
        _label.set_markup("<span weight='bold'>Failure Definition</span>")
        _label.set_use_markup(True)
        _label.show_all()
        _column = Gtk.TreeViewColumn()
        _column.set_widget(_label)
        _column.set_visible(True)
        _column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=2)
        self.treeview.append_column(_column)

    def __make_ui(self) -> None:
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        self.tab_label.set_markup("<span weight='bold'>"
                                  + _("Failure\nDefinitions") + "</span>")
        self.tab_label.set_alignment(xalign=0.5, yalign=0.5)
        self.tab_label.set_justify(Gtk.Justification.CENTER)
        self.tab_label.show_all()
        self.tab_label.set_tooltip_text(
            _("Displays failure definitions for the "
              "selected revision."))

        self.pack_start(self.__make_buttonbox(), False, False, 0)
        RAMSTKListView._make_ui(self)

    def __set_properties(self) -> None:
        """
        Set properties of the Failure Definition ListView and widgets.

        :return: None
        :rtype: None
        """
        RAMSTKListView._set_properties(self)
        self.treeview.set_tooltip_text(
            _("Displays the list of failure definitions for the selected "
              "revision."))

    def _do_load_tree(self, tree: Tree) -> None:
        """
        Load the Failure Defintion List View's Gtk.TreeModel.

        :param tree: the Failure Definition treelib Tree().
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _model.clear()

        for _node in list(tree.nodes.values())[1:]:
            _entity = _node.data

            _attributes: Tuple[int, int, str] = (0, 0, '')
            if _entity is not None:
                _attributes = (
                    _entity.revision_id, _entity.definition_id,
                    _entity.definition
                )

            try:
                _row = _model.append(_attributes)
            except ValueError:
                _row = None

        _row = _model.get_iter_first()
        self.treeview.expand_all()
        if _row is not None:
            _column = self.treeview.get_column(0)
            self.treeview.set_cursor(_model.get_path(_row), None, False)
            self.treeview.row_activated(_model.get_path(_row), _column)

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """
        Request to delete the selected Failure Definition record.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _prompt = _("You are about to delete Failure Definition {0:d} and "
                    "all data associated with it.  Is this really what you "
                    "want to do?").format(self._definition_id)
        _dialog = RAMSTKMessageDialog(_prompt, self._dic_icons['question'],
                                      'question')
        _response = _dialog.do_run()

        if _response == Gtk.ResponseType.YES:
            pub.sendMessage('request_delete_definition',
                            node_id=self._definition_id)

        _dialog.do_destroy()

    def _do_request_insert(self, **kwargs: Any) -> None:  # pylint: disable=unused-argument
        """
        Request to add a Failure Definition record.

        :return: None
        :rtype: None
        """
        pub.sendMessage('request_insert_definition',
                        revision_id=self._revision_id)

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to update the currently selected Failure Definition record.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_definition',
                        node_id=self._definition_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to update all Failure Definitions records.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_definitions')
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _on_button_press(self, treeview: RAMSTKTreeView,
                         event: Gdk.Event) -> None:
        """
        Handle mouse clicks on Failure Definition List View RAMSTKTreeView().

        :param treeview: the Failure Definition ListView Gtk.TreeView().
        :type treeview: :class:`ramstk.gui.ramstk.TreeView.RAMSTKTreeView`.
        :param event: the Gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                      * 1 = left
                      * 2 = scrollwheel
                      * 3 = right
                      * 4 = forward
                      * 5 = backward
                      * 8 =
                      * 9 =
        :type event: :py:class:`Gdk.Event`
        :return: None
        :rtype: None
        """
        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            _icons = ['add', 'remove', 'save', 'save-all']
            _labels = [
                _("Add New Definition"),
                _("Remove Selected Definition"),
                _("Save Selected Definition"),
                _("Save All Definitions")
            ]
            _callbacks = [
                self._do_request_insert, self._do_request_delete,
                self._do_request_update, self._do_request_update_all
            ]

            self.on_button_press(event,
                                 icons=_icons,
                                 labels=_labels,
                                 callbacks=_callbacks)

        treeview.handler_unblock(self._lst_handler_id[1])

    def _on_cell_edit(self, __cell: Gtk.CellRenderer, path: str, new_text: str,
                      position: int, model: Gtk.TreeModel) -> None:
        """
        Handle edits of the Failure Definition List View RAMSTKTreeview().

        :param __cell: the Gtk.CellRenderer() that was edited.
        :type __cell: :class:`Gtk.CellRenderer`
        :param str path: the Gtk.TreeView() path of the Gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited Gtk.CellRenderer().
        :param int position: the column position of the edited
                             Gtk.CellRenderer().
        :param model: the Gtk.TreeModel() the Gtk.CellRenderer() belongs to.
        :type model: :class:`Gtk.TreeModel`
        :return: None
        :rtype: None
        """
        if not RAMSTKListView._do_edit_cell(__cell, path, new_text, position,
                                            model):

            pub.sendMessage('lvw_editing_definition',
                            module_id=self._definition_id,
                            key='definition',
                            value=new_text)

    def _on_row_change(self, treeview: RAMSTKTreeView) -> None:
        """
        Handle row changes for the Failure Definition package List View.

        This method is called whenever a Failure Definition List View
        RAMSTKTreeView() row is activated or changed.

        :param treeview: the Failure Definition List View RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`
        :return: None
        :rtype: None
        """
        _attributes = {}

        treeview.handler_block(self._lst_handler_id[0])

        (_model, _row) = treeview.get_selection().get_selected()

        if _row is not None:
            _attributes['revision_id'] = _model.get_value(_row, 0)
            _attributes['definition_id'] = _model.get_value(_row, 1)
            _attributes['definition'] = _model.get_value(_row, 2)

            self._definition_id = _attributes['definition_id']

            pub.sendMessage('selected_definition', attributes=_attributes)

        treeview.handler_unblock(self._lst_handler_id[0])
