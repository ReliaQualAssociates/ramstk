# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.listviews.FailureDefinition.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2018 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Failure Definition List View Module."""

# Import third party modules.
from pubsub import pub

# Modules required for the GUI.
import pango

# Import other RAMSTK modules.
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _, gobject, gtk
from .ListView import RAMSTKListView


class ListView(RAMSTKListView):
    """
    Display all the Failure Definitions associated with the selected Revision.

    The attributes of the Failure Definition List View are:

    :ivar int _revision_id: the Revision ID whose failure definitions are being
                            displayed in the List View.
    :ivar int _definition_id: the Failure Definition ID of the definition being
                              displayed in the List View.
    """

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the List View for the Failure Definition package.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKListView.__init__(self, controller, module='failure_definition')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._revision_id = None
        self._definition_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self._make_treeview()
        self.treeview.set_rubber_banding(True)
        self.treeview.set_tooltip_text(
            _(u"Displays the list of failure definitions for the selected "
              u"revision."))
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._on_row_change))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Failure\nDefinitions") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays failure definitions for the "
              u"selected revision."))

        self.hbx_tab_label.pack_end(_label)
        self.hbx_tab_label.show_all()

        _scrolledwindow = gtk.ScrolledWindow()
        _scrolledwindow.add(self.treeview)

        self.pack_start(self._make_buttonbox(), expand=False, fill=False)
        self.pack_end(_scrolledwindow, expand=True, fill=True)

        self.show_all()

        pub.subscribe(self._do_load_tree, 'retrieved_definitions')
        pub.subscribe(self._do_load_tree, 'deleted_definition')
        pub.subscribe(self._do_load_tree, 'inserted_definition')

    def _do_load_tree(self, tree):
        """
        Load the Failure Defintion List View's gtk.TreeModel.

        :param tree: the Failure Definition treelib Tree().
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _model.clear()

        for _node in tree.nodes.values()[1:]:
            _entity = _node.data

            _attributes = []
            if _entity is not None:
                _attributes = [
                    _entity.revision_id, _entity.definition_id,
                    _entity.definition
                ]

            try:
                _row = _model.append(_attributes)
            except ValueError:
                _row = None

        _row = _model.get_iter_root()
        self.treeview.expand_all()
        if _row is not None:
            _column = self.treeview.get_column(0)
            self.treeview.set_cursor(_model.get_path(_row), None, False)
            self.treeview.row_activated(_model.get_path(_row), _column)

        return None

    def _do_request_delete(self, __button):
        """
        Request to delete the selected Failure Definition record.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _prompt = _(u"You are about to delete Failure Definition {0:d} and "
                    u"all data associated with it.  Is this really what you "
                    u"want to do?").format(self._definition_id)
        _dialog = ramstk.RAMSTKMessageDialog(
            _prompt, self._dic_icons['question'], 'question')
        _response = _dialog.do_run()

        if _response == gtk.RESPONSE_YES:
            pub.sendMessage('request_delete_definition', node_id=self._definition_id)

        _dialog.do_destroy()

        return None

    def _do_request_insert(self, **kwargs):
        """
        Request to add a Failure Definition record.

        :return: None
        :rtype: None
        """
        _sibling = kwargs['sibling']

        pub.sendMessage(
            'request_insert_definition', revision_id=self._revision_id)

        return None

    def _do_request_insert_sibling(self, __button, **kwargs):  # pylint: disable=unused-argument
        """
        Send request to insert a new Failure Definition.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._do_request_insert(sibling=True)

    def _do_request_update(self, __button):
        """
        Request to update the currently selected Failure Definition record.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.set_cursor(gtk.gdk.WATCH)
        pub.sendMessage(
            'request_update_definition', node_id=self._definition_id)
        self.set_cursor(gtk.gdk.LEFT_PTR)

        return None

    def _do_request_update_all(self, __button):
        """
        Request to update all Failure Definitions records.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(gtk.gdk.WATCH)
        pub.sendMessage('request_update_all_definitions')
        self.set_cursor(gtk.gdk.LEFT_PTR)

        return None

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the buttonbox for the Failure Definition List View.

        :return: _buttonbox; the gtk.ButtonBox() for the Failure Definition
                             List View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Add a new Failure Definition."),
            _(u"Remove the currently selected Failure Definition."),
        ]
        _callbacks = [self._do_request_insert_sibling, self._do_request_delete]
        _icons = ['add', 'remove']

        _buttonbox = ramstk.do_make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1)

        return _buttonbox

    def _make_treeview(self):
        """
        Set up the RAMSTKTreeView() for Failure Definitions.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_STRING)
        self.treeview.set_model(_model)

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('wrap-width', 250)
        _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _label = gtk.Label()
        _label.set_line_wrap(True)
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_markup("<span weight='bold'>Revision ID</span>")
        _label.set_use_markup(True)
        _label.show_all()
        _column = gtk.TreeViewColumn()
        _column.set_widget(_label)
        _column.set_visible(False)
        _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=0)
        self.treeview.append_column(_column)

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('wrap-width', 250)
        _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _label = gtk.Label()
        _label.set_line_wrap(True)
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_markup("<span weight='bold'>Definition\nNumber</span>")
        _label.set_use_markup(True)
        _label.show_all()
        _column = gtk.TreeViewColumn()
        _column.set_widget(_label)
        _column.set_visible(True)
        _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=1)
        self.treeview.append_column(_column)

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 1)
        _cell.set_property('wrap-width', 450)
        _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _cell.connect('edited', self._on_cell_edit, 2, _model)
        _label = gtk.Label()
        _label.set_line_wrap(True)
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_markup("<span weight='bold'>Failure Definition</span>")
        _label.set_use_markup(True)
        _label.show_all()
        _column = gtk.TreeViewColumn()
        _column.set_widget(_label)
        _column.set_visible(True)
        _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=2)
        self.treeview.append_column(_column)

        return _return

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Failure Definition List View RAMSTKTreeView().

        :param treeview: the Failure Definition ListView gtk.TreeView().
        :type treeview: :class:`ramstk.gui.ramstk.TreeView.RAMSTKTreeView`.
        :param event: the gtk.gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                      * 1 = left
                      * 2 = scrollwheel
                      * 3 = right
                      * 4 = forward
                      * 5 = backward
                      * 8 =
                      * 9 =
        :type event: :py:class:`gtk.gdk.Event`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            _menu = gtk.Menu()
            _menu.popup(None, None, None, event.button, event.time)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['add'])
            _menu_item.set_label(_(u"Add New Definition"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_insert)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['remove'])
            _menu_item.set_label(_(u"Remove Selected Definition"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_delete)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['save'])
            _menu_item.set_label(_(u"Save Selected Definition"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['save-all'])
            _menu_item.set_label(_(u"Save All Definitions"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update_all)
            _menu_item.show()
            _menu.append(_menu_item)

        treeview.handler_unblock(self._lst_handler_id[1])

        return False

    def _on_cell_edit(self, __cell, path, new_text, position, model):
        """
        Handle edits of the Failure Definition List View RAMSTKTreeview().

        :param __cell: the gtk.CellRenderer() that was edited.
        :type __cell: :class:`gtk.CellRenderer`
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param model: the gtk.TreeModel() the gtk.CellRenderer() belongs to.
        :type model: :class:`gtk.TreeModel`
        :return: None
        :rtype: None
        """
        if not RAMSTKListView._do_edit_cell(__cell, path, new_text, position,
                                            model):

            pub.sendMessage(
                'editing_definition',
                module_id=self._definition_id,
                key='definition',
                value=new_text)

        return None

    def _on_row_change(self, treeview):
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

        _attributes['revision_id'] = _model.get_value(_row, 0)
        _attributes['definition_id'] = _model.get_value(_row, 1)
        _attributes['definition'] = _model.get_value(_row, 2)

        self._definition_id = _attributes['definition_id']
        self._revision_id = _attributes['revision_id']

        treeview.handler_unblock(self._lst_handler_id[0])

        pub.sendMessage('selected_definition', attributes=_attributes)

        return None
