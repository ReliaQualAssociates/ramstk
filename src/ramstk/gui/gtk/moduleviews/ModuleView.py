# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.moduleviews.ModuleView.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKModuleView Module."""

# Import other RAMSTK modules.
from ramstk.gui.gtk.assistants import ExportModule
from ramstk.gui.gtk.ramstk.Widget import gobject, gtk
from ramstk.gui.gtk import ramstk


class RAMSTKModuleView(gtk.HBox, ramstk.RAMSTKBaseView):
    """
    Display data in the RAMSTK Module Book.

    This is the meta class for all RAMSTK Module View classes.  Attributes of the
    RAMSTKModuleView are:

    :ivar _img_tab: the :class:`gtk.Image` to display on the tab.
    :ivar _lst_col_order: list containing the order of the columns in the
                          Module View gtk.TreeView().
    :ivar hbx_tab_label: the :class:`gtk.HBox` used for the label in the
                         ModuleBook.
    :ivar treeview: the :class:`gtk.TreeView` displaying the list of items
                    in the selected module.
    """

    def __init__(self, controller, **kwargs):
        """
        Initialize the Module View.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :py:class:`ramstk.RAMSTK.RAMSTK`
        :param str module: the module that is being loaded.
        """
        gtk.HBox.__init__(self)
        ramstk.RAMSTKBaseView.__init__(self, controller, **kwargs)

        # Initialize private dictionary attributes.
        self._dic_icons['insert_part'] = \
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/insert_part.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._img_tab = gtk.Image()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        _scrolledwindow = gtk.ScrolledWindow()
        _scrolledwindow.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        _scrolledwindow.add_with_viewport(self._make_buttonbox())
        self.pack_start(_scrolledwindow, expand=False, fill=False)

        _scrolledwindow = gtk.ScrolledWindow()
        _scrolledwindow.add(self.treeview)
        self.pack_end(_scrolledwindow, expand=True, fill=True)

        self.hbx_tab_label.pack_start(self._img_tab)
        self.hbx_tab_label.show_all()

        self.show_all()

    @staticmethod
    def _do_edit_cell(__cell, path, new_text, position, model):
        """
        Handle edits of the Module View gtk.Treeview().

        :param __cell: the gtk.CellRenderer() that was edited.
        :type __cell: :py:class:`gtk.CellRenderer`
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param model: the gtk.TreeModel() the gtk.CellRenderer() belongs to.
        :type model: :py:class:`gtk.TreeModel`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _type = gobject.type_name(model.get_column_type(position))

        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

        return _return

    def do_request_export(self, module):
        """
        Launch the Export assistant.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _tree = self._dtc_data_controller.request_do_select_all(
            revision_id=self._revision_id)
        ExportModule(self._mdcRAMSTK, module, _tree)

        return None

    def make_treeview(self, **kwargs):
        """
        Set up the Module View RAMSTKTreeView().

        :param list editable: list of editable column numbers.
        :return: None
        :rtype: None
        """
        try:
            _editable = kwargs['editable']
        except KeyError:
            _editable = []
        _index = 0

        for _column in self.treeview.get_columns():
            _cell = _column.get_cell_renderers()[0]
            if _index in _editable:
                _color = gtk.gdk.color_parse('#FFFFFF')
                try:
                    _cell.set_property('editable', True)
                    _cell.connect('edited', self._on_cell_edit, _index,
                                  self.treeview.get_model())
                except TypeError:
                    _cell.set_property('activatable', True)
                    _cell.connect('toggled', self._on_cell_edit, _index,
                                  self.treeview.get_model())
            else:
                _color = gtk.gdk.color_parse('#EEEEEE')
                try:
                    _cell.set_property('editable', False)
                except TypeError:
                    _cell.set_property('activatable', False)
            _cell.set_property('cell-background-gdk', _color)
            _index += 1

        return None
