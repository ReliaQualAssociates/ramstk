# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.moduleviews.Function.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
Function Package Module View
###############################################################################
"""

import sys

# Import modules for localization support.
import gettext
import locale

from pubsub import pub                              # pylint: disable=E0401
from sortedcontainers import SortedDict             # pylint: disable=E0401

# Modules required for the GUI.
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)

# Import other RTK modules.
from gui.gtk import rtk                             # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

_ = gettext.gettext


class ModuleView(gtk.ScrolledWindow):
    """
    The Module Book view displays all the Functions associated with the RTK
    Project in a flat list.  The attributes of a Module Book view are:

    :ivar _mdcRTK: the :py:class:`rtk.RTK.RTK` data controller instance.
    :ivar _dtc_function: the :py:class:`rtk.function.Function.Function` data
                         controller to use for accessing the Function data
                         models.
    :ivar _lst_col_order: list containing the order of the columns in the
                          Module View gtk.TreeView().
    :ivar hbx_tab_label: the gtk.HBox() used for the label in the ModuleBook.
    :ivar tvw_function: the gtk.TreeView() displaying the list of Functions.
    """

    def __init__(self, controller):
        """
        Method to initialize the Module Book view for the Function package.

        :param controller: the RTK Master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        gtk.ScrolledWindow.__init__(self)

        # Initialize private dictionary attributes.
        self._dic_icons = {'tab':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/function.png'}

        # Initialize private list attributes.
        self._lst_col_order = []
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._mdcRTK = controller
        self._dtc_function = None
        self._dtm_rtkfunction = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.hbx_tab_label = gtk.HBox()
        self.tvw_function = None

        try:
            locale.setlocale(locale.LC_ALL,
                             controller.RTK_CONFIGURATION.RTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

        # Create the main Function class treeview.
        _bg_color = controller.RTK_CONFIGURATION.RTK_COLORS['functionbg']
        _fg_color = controller.RTK_CONFIGURATION.RTK_COLORS['functionfg']
        _fmt_file = controller.RTK_CONFIGURATION.RTK_CONF_DIR + \
            '/' + controller.RTK_CONFIGURATION.RTK_FORMAT_FILE['function']
        _fmt_path = "/root/tree[@name='Function']/column"
        self.tvw_function = rtk.RTKTreeView(_fmt_path, 0, _fmt_file,
                                            _bg_color, _fg_color)
        self._lst_col_order = self.tvw_function.order

        self.tvw_function.set_tooltip_text(
            _(u"Displays the list of functions."))
        self._lst_handler_id.append(
            self.tvw_function.connect('cursor_changed',
                                      self._do_change_row))
        self._lst_handler_id.append(
            self.tvw_function.connect('button_press_event',
                                      self._on_button_press))

        # Connect the cells to the callback function.
        for i in [5, 15, 17]:
            _cell = self.tvw_function.get_column(
                self._lst_col_order[i]).get_cell_renderers()
            _cell[0].connect('edited', self._do_edit_function, i,
                             self.tvw_function.get_model())

        _icon = gtk.gdk.pixbuf_new_from_file_at_size(self._dic_icons['tab'],
                                                     22, 22)
        _image = gtk.Image()
        _image.set_from_pixbuf(_icon)

        _label = rtk.RTKLabel(_(u"Functions"), width=-1, height=-1,
                              tooltip=_(u"Displays the program functions."))

        self.hbx_tab_label.pack_start(_image)
        self.hbx_tab_label.pack_end(_label)
        self.hbx_tab_label.show_all()

        self.add(self.tvw_function)

        self.show_all()

        pub.subscribe(self._on_select_revision, 'selectedRevision')
        pub.subscribe(self._on_delete_function, 'deletedFunction')
        pub.subscribe(self._on_insert_function, 'insertedFunction')
        pub.subscribe(self._on_edit_function, 'wvwEditedFunction')

    def _do_change_row(self, treeview):
        """
        Method to handle events for the Function package Module Book
        gtk.TreeView().  It is called whenever a Module Book gtk.TreeView()
        row is activated.

        :param gtk.TreeView treeview: the Function class gtk.TreeView().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()

        _function_id = _model.get_value(_row, 1)
        self._dtm_rtkfunction = self._dtc_function.request_select(_function_id)

        treeview.handler_unblock(self._lst_handler_id[0])

        pub.sendMessage('selectedFunction', function_id=_function_id)

        return _return

    def _do_edit_function(self, __cell, path, new_text, position, model):
        """
        Method to handle edits of the Function package Module Book
        gtk.Treeview().

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param gtk.TreeModel model: the gtk.TreeModel() the gtk.CellRenderer()
                                    belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Update the gtk.TreeModel() with the new value.
        _type = gobject.type_name(model.get_column_type(position))

        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

        # Now update the Function data model.
        if self._lst_col_order[position] == 5:
            self._dtm_rtkfunction.function_code = str(new_text)
        elif self._lst_col_order[position] == 15:
            self._dtm_rtkfunction.name = str(new_text)
        elif self._lst_col_order[position] == 17:
            self._dtm_rtkfunction.remarks = str(new_text)

        pub.sendMessage('mvwEditedFunction',
                        function_id=self._dtm_rtkfunction.function_id)

        return False

    def _do_load_tree(self, tree, row=None):
        """
        Method to recursively load the Function Module View's gtk.TreeModel
        with the Function tree.

        :param tree: the Function treelib Tree().
        :type tree: :py:class:`treelib.Tree`
        :param row: the parent row in the Function gtk.TreeView() to add the
                    new item.
        :type row: :py:class:`gtk.TreeIter`
        :return: None
        :rtype: None
        """

        _row = None
        _model = self.tvw_function.get_model()

        _node = tree.nodes[SortedDict(tree.nodes).keys()[0]]
        _entity = _node.data

        try:
            _data = _entity.get_attributes()
            try:
                _row = _model.append(row, _data)
            except TypeError:
                print "FIXME: Handle TypeError in " \
                      "gtk.gui.moduleviews.Function._load_tree"
        except AttributeError:
            _row = None

        for _n in tree.children(_node.identifier):
            _child_tree = tree.subtree(_n.identifier)
            self._do_load_tree(_child_tree, _row)

        return None

    def _on_button_press(self, treeview, event):
        """
        Method for handling mouse clicks on the Function package Module Book
        gtk.TreeView().

        :param gtk.TreeView treeview: the Function class gtk.TreeView().
        :param gtk.gdk.Event event: the gtk.gdk.Event() that called this method
                                    (the important attribute is which mouse
                                    button was clicked).

                                    * 1 = left
                                    * 2 = scrollwheel
                                    * 3 = right
                                    * 4 = forward
                                    * 5 = backward
                                    * 8 =
                                    * 9 =

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            print "FIXME: Rick clicking should launch a pop-up menu with " \
                  "options to insert sibling, insert child, delete " \
                  "(selected), save (selected), and save all in " \
                  "rtk.gui.gtk.moduleviews.Function._on_button_press."

        treeview.handler_unblock(self._lst_handler_id[1])

        return False

    def _on_delete_function(self):
        """
        Method to remove a function from the RTKTreeView after it's been
        deleted from the RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _model, _row = self.tvw_function.get_selection().get_selected()
        _path = _model.get_path(_row)
        _revision_id = _model.get_value(_row, 0)

        _model.remove(_row)
        _model.row_deleted(_path)

        self._on_select_revision(_revision_id)

        return _return

    def _on_edit_function(self, position, new_text):
        """
        Method to update the Module View RTKTreeView with changes to the
        Function data model attributes.

        :ivar int position: the ordinal position in the Module Book
                            gtk.TreeView() of the data being updated.
        :ivar new_text: the new value of the attribute to be updated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _model, _row = self.tvw_function.get_selection().get_selected()

        _model.set(_row, self._lst_col_order[position], new_text)

        return False

    def _on_insert_function(self, function_id=None, parent_id=0,
                            level='sibling'):
        """
        Method to add a Function to the Function RTKTreeView after a successful
        insert into the RTK Program database.

        :param int function_id: the Function ID of the newly inserted Function.
        :param int parent_id: the Function ID of the parent Function.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        # Get the currently selected row, the level of the currently selected
        # item, and it's parent row in the Function tree.
        _model, _row = self.tvw_function.get_selection().get_selected()
        _prow = _model.iter_parent(_row)

        _function = self._dtc_function.request_select(function_id)
        _data = _function.get_attributes()
        if parent_id == 0:
            _model.append(None, _data)
        elif parent_id != 0 and level == 'sibling':
            _model.append(_prow, _data)
        else:
            _model.append(_row, _data)

        return _return

    def _on_select_revision(self, revision_id):
        """
        Method to load the Function Module Book view gtk.TreeModel() with
        Function information when an RTK Program database is opened.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _model = self.tvw_function.get_model()
        _model.clear()

        self._dtc_function = self._mdcRTK.dic_controllers['function']
        _functions = self._dtc_function.request_select_all(revision_id)

        self._do_load_tree(_functions)

        _row = _model.get_iter_root()
        self.tvw_function.expand_all()
        self.tvw_function.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.tvw_function.get_column(0)
            self.tvw_function.row_activated(_path, _column)

        _module = self._mdcRTK.RTK_CONFIGURATION.RTK_PAGE_NUMBER[1]
        pub.sendMessage('mvw_switchedPage', module=_module)

        return _return
