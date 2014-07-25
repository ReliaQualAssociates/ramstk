#!/usr/bin/env python
"""
This is the class used to display and interact with the Design Reviews.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       designreview.py is part of The RTK Project
#
# All rights reserved.

import gettext
import locale
import operator
import string
import sys
import time

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
import pango

# Import other RTK modules.
import configuration as _conf
import utilities as _util
import widgets as _widg

_ = gettext.gettext


def _design_review_edit(cell, path, new_text, position, model):
    """
    Function to respond to design review list gtk.TreeView() gtk.CellRenderer()
    editing.

    :param gtk.CellRenderer cell: the gtk.CellRenderer() that was edited.
    :param str path: the gtk.TreeView() path of the gtk.CellRenderer() that was
                     edited.
    :param str new_text: the new text in the edited gtk.CellRenderer().
    :param int position: the column position of the edited gtk.CellRenderer().
    :param gtk.TreeModel model: the gtk.TreeModel() the edited
                                gtk.CellRenderer() belongs to.
    :return: False if successful or True if an error is encountered.
    :rtype: boolean
    """

    if position == 3:
        new_text = not cell.get_active()

    model[path][position] = new_text

    return False


class DesignReview(gtk.Window):
    """
    This is the base class for the Design Review.
    """

    def __init__(self, __menuitem, application):

        self._steps = {}

        gtk.Window.__init__(self)
        self.set_title(_(u"Design Review Navigator"))

        _n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        _width = gtk.gdk.screen_width() / _n_screens
        _height = gtk.gdk.screen_height()

        self.set_default_size((_width / 3) - 10, (2 * _height / 7))
        self.set_border_width(5)

        self.connect("destroy", lambda w: self.destroy())

        self._app = application

        # Toolbar widgets.
        self.btnAddGateway = gtk.ToolButton()
        self.btnAddSibling = gtk.ToolButton()
        self.btnAddChild = gtk.ToolButton()
        self.btnRemoveGateway = gtk.ToolButton()
        self.btnRemoveCriteria = gtk.ToolButton()

        _toolbar = self._create_toolbar()
        self.notebook = self._create_notebook()

        _vbox = gtk.VBox()
        _vbox.pack_start(_toolbar, expand=False)
        _vbox.pack_end(self.notebook)

        self.add(_vbox)

        self.show_all()

    def _create_toolbar(self):
        """
        Method to create the toolbar for the Design Review class.

        :return: _toolbar
        :rtype: gtk.ToolBar()
        """

        _toolbar = gtk.Toolbar()

        _position = 0

        # Add gateway button.
        self.btnAddGateway.set_tooltip_text(_(u"Adds a new review gateway "
                                              u"to the development program."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        self.btnAddGateway.set_icon_widget(_image)
        #self.btnAddGateway.connect('clicked', self._add_gateway)
        _toolbar.insert(self.btnAddGateway, _position)
        _position += 1

        # Remove gateway button.
        self.btnRemoveGateway.set_tooltip_text(_(u"Deletes the currently "
                                                 u"selected review gateway "
                                                 u"from the development "
                                                 u"program."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        self.btnRemoveGateway.set_icon_widget(_image)
        #self.btnRemoveGateway.connect('clicked', self._delete_gateway)
        _toolbar.insert(self.btnRemoveGateway, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Add sibling criteria button.
        self.btnAddSibling.set_tooltip_text(_(u"Adds a new review criteria "
                                              u"to the active review gateway "
                                              u"at the same level as the "
                                              u"currently selected review "
                                              u"criteria."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/insert_sibling.png')
        self.btnAddSibling.set_icon_widget(_image)
        #self.btnAddSibling.connect('clicked', self._add_criteria, 0)
        _toolbar.insert(self.btnAddSibling, _position)
        _position += 1

        # Add child criteria button.
        self.btnAddChild.set_tooltip_text(_(u"Adds a new review criteria "
                                            u"to the active review gateway "
                                            u"one level subordinate to the "
                                            u"currently selected review "
                                            u"criteria."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/insert_child.png')
        self.btnAddChild.set_icon_widget(_image)
        #self.btnAddChild.connect('clicked', self._add_criteria, 1)
        _toolbar.insert(self.btnAddChild, _position)
        _position += 1

        # Remove criteria button.
        self.btnRemoveCriteria.set_tooltip_text(_(u"Deletes the currently "
                                                  u"selected review "
                                                  u"criteria."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        self.btnRemoveCriteria.set_icon_widget(_image)
        #self.btnRemoveCriteria.connect('clicked', self._delete_criteria)
        _toolbar.insert(self.btnRemoveCriteria, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save review button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Saves the review gateways to the open "
                                   u"RTK program database."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        #_button.connect('clicked', self._save_reviews)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.show_all()

        return _toolbar

    def _create_notebook(self):
        """
        Method to create the notebook for the Design Review class.

        :return: _notebook
        :rtype: gtk.Notebook()
        """

        _query = "SELECT * FROM tbl_gateways"
        _results = self._app.COMDB.execute_query(_query, None,
                                                 self._app.ComCnx)

        try:
            _n_gateways = len(_results)
        except:
            _n_gateways = 0

        # Create a notebook with one page for each gateway.
        _notebook = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if _conf.TABPOS[1] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif _conf.TABPOS[1] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif _conf.TABPOS[1] == 'top':
            _notebook.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook.set_tab_pos(gtk.POS_BOTTOM)

        for i in range(_n_gateways):
            # Create the gtk.TreeView() used to display the review criteria.
            _model = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                                   gobject.TYPE_STRING, gobject.TYPE_INT,
                                   gobject.TYPE_STRING)
            _treeview = gtk.TreeView(_model)

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.add(_treeview)

            _headers = [_(u"Criteria ID"), _(u"Criteria"), _(u"Rationale"),
                        _(u"Satisfied"), _(u"Remarks")]
            for j in range(len(_headers)):
                _column = gtk.TreeViewColumn()
                _label = _widg.make_column_heading(_headers[j])
                _column.set_widget(_label)

                if j == 3:
                    _cell = gtk.CellRendererToggle()
                    _cell.set_property('activatable', 1)
                    _cell.connect('toggled', _design_review_edit, '', j,
                                  _model)
                    _column.pack_start(_cell, True)
                    _column.set_attributes(_cell, active=j)
                else:
                    _cell = gtk.CellRendererText()
                    _cell.set_property('editable', 1)
                    _cell.set_property('background', 'white')
                    _cell.set_property('wrap-width', 250)
                    _cell.set_property('wrap-mode', pango.WRAP_WORD)
                    _cell.connect('edited', _design_review_edit, j, _model)
                    _column.pack_start(_cell, True)
                    _column.set_attributes(_cell, text=j)

                _column.set_resizable(True)

                _column.connect('notify::width', _widg.resize_wrap, _cell)
                _treeview.append_column(_column)

            # Load the treeview with the review criteria.
            _query = "SELECT fld_concern_id, fld_concern, fld_rationale, \
                             fld_satisfied, fld_remarks \
                      FROM tbl_reviews \
                      WHERE fld_gateway_id=%d" % _results[i][0]
            _criteria = self._app.COMDB.execute_query(_query, None,
                                                      self._app.ComCnx)

            try:
                _n_criteria = len(_criteria)
            except TypeError:
                _n_criteria = 0

            for j in range(_n_criteria):
                _data = [_criteria[j][0],
                         _util.none_to_string(_criteria[j][1]),
                         _util.none_to_string(_criteria[j][2]),
                         _criteria[j][3],
                         _util.none_to_string(_criteria[j][4])]
                _model.append(None, _data)

            # Insert the tab.
            _label = gtk.Label()
            _label.set_markup("<span weight='bold'>" +
                              _results[i][1] + "</span>")
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.show_all()
            _label.set_tooltip_text(_(u""))

            _notebook.insert_page(_scrollwindow, tab_label=_label, position=-1)

        return _notebook

    def _add_gateway(self, __toolbutton):
        """
        Method to add a new gateway to the open RTK program database.

        :param gtk.Toolbutton __toolbutton: the gtk.ToolButton() that called
                                            this method.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _query = "INSERT INTO tbl_gateways \
                              (fld_gateway_name, fld_gateway_description) \
                  VALUES ('New Review Gateway', \
                          'This is a new gateway for the development program')"
        if not self._app..COMDB.execute_query(_query, None, self._app.ComCnx,
                                              commit=True):
            _util.rtk_error(_(u"Error creating new program review gateway."))
            return True

        return False
