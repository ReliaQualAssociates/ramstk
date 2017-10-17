# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.moduleviews.ModuleView.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
RTK List View Package Meta Class
###############################################################################
"""

from sortedcontainers import SortedDict         # pylint: disable=E0401

# Import other RTK modules.
from gui.gtk.rtk.Widget import _, gobject, gtk  # pylint: disable=E0401,W0611
from gui.gtk import rtk                         # pylint: disable=E0401,W0611


class RTKModuleView(gtk.VBox, rtk.RTKBaseView):
    """
    This is the meta class for all RTK Module View classes.  Attributes of the
    RTKModuleView are:

    :ivar _img_tab: the :py:class:`gtk.Image` to display on the tab.
    :ivar _lst_col_order: list containing the order of the columns in the
                          Module View gtk.TreeView().
    :ivar hbx_tab_label: the :py:class:`gtk.HBox` used for the label in the
                         ModuleBook.
    :ivar treeview: the :py:class:`gtk.TreeView` displaying the list of items
                    in the selected module.
    """

    def __init__(self, controller, module=''):
        """
        Method to initialize the List View.

        :param controller: the RTK master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        :param str module: the module that is being loaded.
        """

        gtk.VBox.__init__(self)
        rtk.RTKBaseView.__init__(self, controller)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_col_order = []

        # Initialize private scalar attributes.
        self._img_tab = gtk.Image()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.hbx_tab_label = gtk.HBox()
        self.treeview = None

        _bg_color = controller.RTK_CONFIGURATION.RTK_COLORS[module + 'bg']
        _fg_color = controller.RTK_CONFIGURATION.RTK_COLORS[module + 'fg']
        _fmt_file = controller.RTK_CONFIGURATION.RTK_CONF_DIR + \
            '/' + controller.RTK_CONFIGURATION.RTK_FORMAT_FILE[module]
        _fmt_path = "/root/tree[@name='" + module.title() + "']/column"

        self.treeview = rtk.RTKTreeView(_fmt_path, 0, _fmt_file,
                                        _bg_color, _fg_color)
        self._lst_col_order = self.treeview.order

        _scrolledwindow = gtk.ScrolledWindow()
        _scrolledwindow.add(self.treeview)

        self.pack_end(_scrolledwindow, expand=True, fill=True)

    @staticmethod
    def _do_edit_cell(__cell, path, new_text, position, model):
        """
        Method to handle edits of the Module View gtk.Treeview().

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

    def _do_load_tree(self, tree, row=None):
        """
        Method to recursively load the Module View's gtk.TreeModel with the
        Module's tree.

        :param tree: the Module's treelib Tree().
        :type tree: :py:class:`treelib.Tree`
        :param row: the parent row in the gtk.TreeView() to add the new item.
        :type row: :py:class:`gtk.TreeIter`
        :return: None
        :rtype: None
        """

        _row = None
        _model = self.treeview.get_model()

        _node = tree.nodes[SortedDict(tree.nodes).keys()[0]]
        _entity = _node.data

        try:
            _data = _entity.get_attributes()
            try:
                _row = _model.append(row, _data)
            except TypeError:
                print "FIXME: Handle TypeError in " \
                      "gtk.gui.moduleviews.ModuleView._do_load_tree"
        except AttributeError:
            _row = None

        for _n in tree.children(_node.identifier):
            _child_tree = tree.subtree(_n.identifier)
            self._do_load_tree(_child_tree, _row)

        return None

    def _on_select_revision(self, tree):
        """
        Method to load the Module View gtk.TreeModel() with information when an
        RTK Program database is opened.

        :param tree: the Treelib tree that should be loaded into the Module
                     View.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _model = self.treeview.get_model()
        _model.clear()

        self._do_load_tree(tree)

        _row = _model.get_iter_root()
        self.treeview.expand_all()
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.set_cursor(_path, None, False)
            self.treeview.row_activated(_path, _column)

        return _return
