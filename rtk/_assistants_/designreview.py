#!/usr/bin/env python
"""
This is the class used to display and interact with the Design Reviews.
"""
# TODO: Create this as a new class.
__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       designreview.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
try:
    import Configuration as _conf
    import Utilities as _util
    import gui.gtk.Widgets as _widg
except ImportError:
    import rtk.Configuration as _conf
    import rtk.Utilities as _util
    import rtk.gui.gtk.Widgets as _widg

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
    This is the Design Review class.
    """

    def __init__(self, __menuitem, application):

        # Define private dictionary attributes.

        # Define private list attrtibutes.
        self._lst_concern_id = []

        # Define public scalar attributes.
        self.gateway_id = 1

        gtk.Window.__init__(self)
        self.set_title(_(u"Design Review Navigator"))

        _n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        _width = gtk.gdk.screen_width() / _n_screens
        _height = gtk.gdk.screen_height()

        self.set_default_size((_width / 2) - 10, (2 * _height / 5))
        self.set_border_width(5)

        self.connect("destroy", lambda w: self.destroy())

        self._app = application

        # Toolbar widgets.
        self.btnAddSibling = gtk.ToolButton()
        self.btnAddChild = gtk.ToolButton()
        self.btnRemoveCriteria = gtk.ToolButton()
        _list = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_STRING)
        self.cmbGateways = gtk.ComboBoxEntry(_list, 1)
        self.cmbGateways.props.width_request = 200
        self.cmbGateways.props.height_request = 30

        self.treeview = gtk.TreeView()

        _toolbar = self._create_toolbar()
        _scrollwindow = self._create_tree()

        _vbox = gtk.VBox()
        _vbox.pack_start(_toolbar, expand=False)
        _vbox.pack_end(_scrollwindow)

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

        # Save review button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(
            _(u"Saves the review gateways to the open "
              u"RTK program database."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._save_review)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        self.cmbGateways.set_tooltip_text(
            _(u"List of existing Program review "
              u"gateways."))
        _alignment = gtk.Alignment(xalign=0.5, yalign=0.5)
        _alignment.add(self.cmbGateways)
        _toolitem = gtk.ToolItem()
        _toolitem.add(_alignment)
        _toolbar.insert(_toolitem, _position)

        _toolbar.show_all()

        return _toolbar

    def _create_tree(self):
        """
        Method to create the gtk.TreeView() for the Design Review class.  This
        gtk.TreeView() is used to display the review criteria for the selected
        design review.

        :return: _scrollwindow
        :rtype: gtk.ScrolledWindow()
        """

        self._load_gateways()
        self.cmbGateways.connect('changed', self._load_design_review)

        # Create the gtk.TreeView() used to display the review criteria.
        _model = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_INT,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING)
        self.treeview.set_model(_model)
        self.treeview.set_enable_tree_lines(True)
        self.treeview.set_grid_lines(True)
        self.treeview.set_reorderable(True)
        self.treeview.set_search_column(0)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.treeview)

        # Get the list of groups.
        _query = "SELECT fld_group_name, fld_group_id FROM tbl_groups"
        _owners = self._app.COMDB.execute_query(_query, None, self._app.ComCnx)

        _headers = [
            _(u"Criteria ID"),
            _(u"Criteria"),
            _(u"Rationale"),
            _(u"Satisfied"),
            _(u"Remarks"),
            _(u"Actions"),
            _(u"Due Date"),
            _(u"Owner")
        ]
        for j in range(len(_headers)):
            _column = gtk.TreeViewColumn()
            _label = _widg.make_column_heading(_headers[j])
            _column.set_widget(_label)

            if j == 0:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _cell.set_property('background', 'light gray')
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=j)
            elif j == 3:
                _cell = gtk.CellRendererToggle()
                _cell.set_property('activatable', 1)
                _cell.connect('toggled', _design_review_edit, '', j, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, active=j)
            elif j == 7:
                _cell = gtk.CellRendererCombo()
                _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
                _cellmodel.append([""])
                for i in range(len(_owners)):
                    _cellmodel.append([_owners[i][0]])
                _cell.set_property('editable', 1)
                _cell.set_property('has-entry', True)
                _cell.set_property('model', _cellmodel)
                _cell.set_property('text-column', 0)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', _design_review_edit, j, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=j)
            else:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('background', 'white')
                _cell.set_property('width-chars', 45)
                _cell.set_property('wrap-width', 50)
                _cell.set_property('wrap-mode', pango.WRAP_WORD)
                _cell.connect('edited', _design_review_edit, j, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=j)

            _column.set_resizable(True)

            _column.connect('notify::width', _widg.resize_wrap, _cell)
            self.treeview.append_column(_column)

        return _scrollwindow

    def _load_gateways(self):
        """
        Method to load the gtk.ComboBox() with a list of program review
        gateways.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _query = "SELECT * FROM tbl_gateways"
        _results = self._app.COMDB.execute_query(_query, None,
                                                 self._app.ComCnx)
        try:
            _n_gateways = len(_results)
        except:
            _n_gateways = 0

        _model = self.cmbGateways.get_model()
        _model.clear()
        _model.append(None, [-1, ""])
        for i in range(_n_gateways):
            _model.append(None, [_results[i][0], _results[i][1]])

        return False

    def _load_design_review(self, __combobox):
        """
        Method to select the design review criteria to load into the
        gtk.TreeView().

        :param gtk.ComboBox __combobox: the gtk.ComboBox() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Clear the list of concern IDs.
        self._lst_concern_id[:] = []

        # Retrieve the ID of the selected gateway.
        _model = self.cmbGateways.get_model()
        _row = self.cmbGateways.get_active_iter()
        try:
            self.gateway_id = int(_model.get_value(_row, 0))
        except TypeError:
            self.gateway_id = -1

        # Retrieve the review criteria for the selected gateway.
        _query = "SELECT fld_concern_id, fld_concern, fld_rationale, \
                         fld_remarks, fld_parent_id \
                  FROM tbl_reviews \
                  WHERE fld_gateway_id=%d \
                  ORDER BY fld_concern_id" % self.gateway_id
        _criteria = self._app.COMDB.execute_query(_query, None,
                                                  self._app.ComCnx)
        try:
            _n_criteria = len(_criteria)
        except TypeError:
            _n_criteria = 0

        # Retrieve the status of each criteria for the open RTK program.
        _query = "SELECT fld_satisfied, fld_concern_id, fld_action, \
                         fld_due_date, fld_owner \
                  FROM tbl_reviews \
                  WHERE fld_revision_id=%d \
                  AND fld_gateway_id=%d \
                  ORDER BY fld_concern_id" % (self._app.REVISION.revision_id,
                                              self.gateway_id)
        _status = self._app.DB.execute_query(_query, None, self._app.ProgCnx)

        # If not already loaded into the current RTK Program database, load the
        # concern ID's from the common RTK database.
        if not _status:
            for i in range(_n_criteria):
                _query = "INSERT INTO tbl_reviews \
                          (fld_revision_id, fld_gateway_id, fld_concern_id) \
                          VALUES (%d, %d, %d)"                                               % \
                         (self._app.REVISION.revision_id, self.gateway_id,
                          _criteria[i][0])
                self._app.DB.execute_query(
                    _query, None, self._app.ProgCnx, commit=True)

            _query = "SELECT fld_satisfied, fld_concern_id, fld_action, \
                             fld_due_date, fld_owner \
                      FROM tbl_reviews \
                      WHERE fld_revision_id=%d \
                      AND fld_gateway_id=%d \
                      ORDER BY fld_concern_id"                                               % \
                     (self._app.REVISION.revision_id, self.gateway_id)
            _status = self._app.DB.execute_query(_query, None,
                                                 self._app.ProgCnx)

        # Load the criteria for the selected review gateway into the
        # gtk.TreeView()
        _model = self.treeview.get_model()
        _model.clear()
        for j in range(_n_criteria):
            if _criteria[j][4] == '-':
                _parent = None
            else:
                _parent = _model.get_iter_from_string(_criteria[j][4])

            try:
                _stat = _status[j][0]
            except IndexError:
                _stat = 0
            _data = [
                _criteria[j][0],
                _util.none_to_string(_criteria[j][1]),
                _util.none_to_string(_criteria[j][2]), _stat,
                _util.none_to_string(_criteria[j][3]),
                _util.none_to_string(_status[j][2]),
                _util.ordinal_to_date(_status[j][3]), _status[j][4]
            ]
            _model.append(_parent, _data)

            # Add the RTK program database concern ID to the list.
            try:
                self._lst_concern_id.append(_status[j][1])
            except IndexError:
                pass

        if _model.get_iter_root() is not None:
            _path = _model.get_path(_model.get_iter_root())
            self.treeview.set_cursor(_path, None, False)
            self.treeview.row_activated(_path, self.treeview.get_column(0))
            self.treeview.expand_all()

        return False

    def _save_review(self, __toolbutton):
        """
        Method to save the currently selected gateway review.

        :param gtk.ToolButton __toolbutton: the gtk.ToolButton() that called
                                            this method.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        def _save_line(model, __path, row, self):
            """
            Function to save each row in the Design Review class gtk.TreeView()
            model to the open RTK Program database.

            :param gtk.TreeModel model: the Design Review class
                                        gtk.TreeModel().
            :param str__path: the path of the active row in the Design Review
                              class gtk.Treemodel().
            :param gtk.TreeIter row: the selected gtk.TreeIter() in the Design
                                     Review class gtk.TreeView().
            """

            _concern_id = model.get_value(row, 0)
            _satisfied = model.get_value(row, 3)
            _action = model.get_value(row, 5)
            _due_date = _util.date_to_ordinal(model.get_value(row, 6))
            _owner = model.get_value(row, 7)

            # Update the review criteria in the open RTK Program database if
            # the criteria already exists.  Otherwise add the new criteria to
            # the open RTK Program database.
            if _concern_id in self._lst_concern_id:
                _query = "UPDATE tbl_reviews \
                          SET fld_satisfied=%d, fld_action='%s', \
                              fld_due_date='%s', fld_owner='%s' \
                          WHERE fld_revision_id=%d \
                          AND fld_gateway_id=%d \
                          AND fld_concern_id=%d"                                                 % \
                         (_satisfied, _action, _due_date, _owner,
                          self._app.REVISION.revision_id, self.gateway_id,
                          _concern_id)
            else:
                _query = "INSERT INTO tbl_reviews \
                          (fld_revision_id, fld_gateway_id, \
                           fld_concern_id, fld_satisfied, fld_action, \
                           fld_due_date, fld_owner) \
                          VALUES (%d, %d, %d, %d, '%s', '%s', '%s')"                                                                     % \
                         (self._app.REVISION.revision_id,
                          self.gateway_id, _concern_id, _satisfied, _action,
                          _due_date, _owner)
            if not self._app.DB.execute_query(
                    _query, None, self._app.ProgCnx, commit=True):
                _util.rtk_error(
                    _(u"Error saving review criteria %d for "
                      u"review gateway %d.") % (_concern_id, self.gateway_id))
                return True

            return False

        _model = self.treeview.get_model()
        _model.foreach(_save_line, self)

        return True


class ReviewCriteria(gtk.Window):
    """
    This is the Review Criteria class.
    """

    def __init__(self, __menuitem, application):

        gtk.Window.__init__(self)
        self.set_title(_(u"Edit Design Review Criteria"))

        _n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        _width = gtk.gdk.screen_width() / _n_screens
        _height = gtk.gdk.screen_height()

        self.set_default_size((_width / 2) - 10, (2 * _height / 5))
        self.set_border_width(5)

        self.connect("destroy", lambda w: self.destroy())

        self._app = application

        # Toolbar widgets.
        self.btnAddSibling = gtk.ToolButton()
        self.btnAddChild = gtk.ToolButton()
        self.btnRemoveCriteria = gtk.ToolButton()
        _list = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_STRING)
        self.cmbGateways = gtk.ComboBoxEntry(_list, 1)
        self.cmbGateways.props.width_request = 200
        self.cmbGateways.props.height_request = 30

        self.treeview = gtk.TreeView()

        _toolbar = self._create_toolbar()
        _scrollwindow = self._create_tree()

        _vbox = gtk.VBox()
        _vbox.pack_start(_toolbar, expand=False)
        _vbox.pack_end(_scrollwindow)

        self.add(_vbox)

        self.show_all()

    def _create_toolbar(self):
        """
        Method to create the toolbar for the Design Review class.

        :return: _toolbar
        :rtype: gtk.ToolBar
        """

        _toolbar = gtk.Toolbar()

        _position = 0

        # Add gateway button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(
            _(u"Adds a new review gateway to the "
              u"development program."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._add_gateway)
        _toolbar.insert(_button, _position)
        _position += 1

        # Remove gateway button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(
            _(u"Deletes the currently selected review "
              u"gateway from the development program."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._delete_gateway)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Add sibling criteria button.
        self.btnAddSibling.set_tooltip_text(
            _(u"Adds a new review criteria "
              u"to the active review gateway "
              u"at the same level as the "
              u"currently selected review "
              u"criteria."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/insert_sibling.png')
        self.btnAddSibling.set_icon_widget(_image)
        self.btnAddSibling.connect('clicked', self._add_criteria, 0)
        _toolbar.insert(self.btnAddSibling, _position)
        _position += 1

        # Add child criteria button.
        self.btnAddChild.set_tooltip_text(
            _(u"Adds a new review criteria "
              u"to the active review gateway "
              u"one level subordinate to the "
              u"currently selected review "
              u"criteria."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/insert_child.png')
        self.btnAddChild.set_icon_widget(_image)
        self.btnAddChild.connect('clicked', self._add_criteria, 1)
        _toolbar.insert(self.btnAddChild, _position)
        _position += 1

        # Remove criteria button.
        self.btnRemoveCriteria.set_tooltip_text(
            _(u"Deletes the currently "
              u"selected review "
              u"criteria."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        self.btnRemoveCriteria.set_icon_widget(_image)
        self.btnRemoveCriteria.connect('clicked', self._delete_criteria)
        _toolbar.insert(self.btnRemoveCriteria, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save review criteria button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(
            _(u"Saves the review criteria for the "
              u"selected review gateway."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._save_criteria)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        self.cmbGateways.set_tooltip_text(
            _(u"List of existing Program review "
              u"gateways."))
        _alignment = gtk.Alignment(xalign=0.5, yalign=0.5)
        _alignment.add(self.cmbGateways)
        _toolitem = gtk.ToolItem()
        _toolitem.add(_alignment)
        _toolbar.insert(_toolitem, _position)

        _toolbar.show_all()

        return _toolbar

    def _create_tree(self):
        """
        Method to create the gtk.TreeView() for the Design Review Criteria
        class.  This gtk.TreeView() is used to display the review criteria for
        the selected design review and add/delete existing criteria.

        :return: _scrollwindow
        :rtype: gtk.ScrolledWindow()
        """

        self._load_gateways()
        self.cmbGateways.connect('changed', self._load_review_criteria)

        # Create the gtk.TreeView() used to display the review criteria.
        _model = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_STRING)
        self.treeview.set_model(_model)
        self.treeview.set_enable_tree_lines(True)
        self.treeview.set_grid_lines(True)
        self.treeview.set_reorderable(True)
        self.treeview.set_search_column(0)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.treeview)

        _headers = [_(u"Criteria ID"), _(u"Criteria"), _(u"Rationale")]
        for j in range(len(_headers)):
            _column = gtk.TreeViewColumn()
            _label = _widg.make_column_heading(_headers[j])
            _column.set_widget(_label)

            _cell = gtk.CellRendererText()
            if j == 0:
                _cell.set_property('editable', 0)
                _cell.set_property('background', 'light gray')
            else:
                _cell.set_property('editable', 1)
                _cell.set_property('background', 'white')
                _cell.set_property('width-chars', 45)
            _cell.set_property('wrap-width', 50)
            _cell.set_property('wrap-mode', pango.WRAP_WORD)
            _cell.connect('edited', _design_review_edit, j, _model)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=j)

            _column.set_resizable(True)

            _column.connect('notify::width', _widg.resize_wrap, _cell)
            self.treeview.append_column(_column)

        return _scrollwindow

    def _load_gateways(self):
        """
        Method to load the gtk.ComboBox() with a list of program review
        gateways.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _query = "SELECT * FROM tbl_gateways"
        _results = self._app.COMDB.execute_query(_query, None,
                                                 self._app.ComCnx)
        try:
            _n_gateways = len(_results)
        except:
            _n_gateways = 0

        _model = self.cmbGateways.get_model()
        _model.clear()
        _model.append(None, [-1, ""])
        for i in range(_n_gateways):
            _model.append(None, [_results[i][0], _results[i][1]])

        return False

    def _load_review_criteria(self, __combobox):
        """
        Method to select the design review criteria to load into the
        gtk.TreeView().

        :param gtk.ComboBox __combobox: the gtk.ComboBox() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Retrieve the ID of the selected gateway.
        _model = self.cmbGateways.get_model()
        _row = self.cmbGateways.get_active_iter()
        try:
            self.gateway_id = int(_model.get_value(_row, 0))
        except TypeError:
            self.gateway_id = -1

        # Retrieve the review criteria for the selected gateway.
        _query = "SELECT fld_concern_id, fld_concern, fld_rationale, \
                         fld_parent_id \
                  FROM tbl_reviews \
                  WHERE fld_gateway_id=%d" % self.gateway_id
        _criteria = self._app.COMDB.execute_query(_query, None,
                                                  self._app.ComCnx)
        try:
            _n_criteria = len(_criteria)
        except TypeError:
            _n_criteria = 0

        # Load the criteria into the gtk.TreeView()
        _model = self.treeview.get_model()
        _model.clear()
        for j in range(_n_criteria):
            if _criteria[j][3] == '-':
                _parent = None
            else:
                _parent = _model.get_iter_from_string(_criteria[j][3])
            _data = [
                _criteria[j][0],
                _util.none_to_string(_criteria[j][1]),
                _util.none_to_string(_criteria[j][2])
            ]
            _model.append(_parent, _data)

        if _model.get_iter_root() is not None:
            _path = _model.get_path(_model.get_iter_root())
            self.treeview.set_cursor(_path, None, False)
            self.treeview.row_activated(_path, self.treeview.get_column(0))
            self.treeview.expand_all()

        return False

    def _add_gateway(self, __toolbutton):
        """
        Method to add a new review gateway to the open RTK program database.

        :param gtk.Toolbutton __toolbutton: the gtk.ToolButton() that called
                                            this method.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _query = "INSERT INTO tbl_gateways \
                  (fld_gateway_name, fld_gateway_description) \
                  VALUES ('New Review Gateway', \
                          'This is a new gateway for the development program')"

        if not self._app.COMDB.execute_query(
                _query, None, self._app.ComCnx, commit=True):
            _util.rtk_error(_(u"Error creating new program review gateway."))
            return True

        self._load_gateways()

        return False

    def _add_criteria(self, __toolbutton, kind):
        """
        Method to add a new review criteria for the currently selected review
        gateway to the common RTK database.

        :param gtk.Toolbutton __toolbutton: the gtk.ToolButton() that called
                                            this method.
        :param int kind: the kind of criteria to add.
                         * 0 = sibling criteria
                         * 1 = child criteria
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _txtConcern = _widg.make_text_view()
        _txtRationale = _widg.make_text_view()

        _dialog = _widg.make_dialog(_(u"Add Review Criteria"))

        _fixed = gtk.Fixed()

        _label = _widg.make_label(_(u"Criterion:"))
        _x_pos = _label.size_request()[0]
        _fixed.put(_label, 5, 5)

        _label = _widg.make_label(_(u"Rationale:"))
        _x_pos = max(_x_pos, _label.size_request()[0])
        _fixed.put(_label, 5, 110)

        _fixed.put(_txtConcern, _x_pos, 5)
        _fixed.put(_txtRationale, _x_pos, 110)

        _fixed.show_all()

        _dialog.vbox.pack_start(_fixed)  # pylint: disable=E1101

        # Run the dialog and apply the changes if the 'OK' button is pressed.
        if _dialog.run() == gtk.RESPONSE_ACCEPT:
            _util.set_cursor(self._app, gtk.gdk.WATCH)

            _textbuffer = _txtConcern.get_child().get_child().get_buffer()
            _concern = _textbuffer.get_text(*_textbuffer.get_bounds())
            _textbuffer = _txtRationale.get_child().get_child().get_buffer()
            _rationale = _textbuffer.get_text(*_textbuffer.get_bounds())

            # Add the new criteria to the gtk.TreeView().  It will be added to
            # the common database and program database when the design review
            # is saved.
            (_model, _row) = self.treeview.get_selection().get_selected()

            if kind == 0:
                _parent = _model.get_string_from_iter(_model.iter_parent(_row))
            elif kind == 1:
                _parent = _model.get_string_from_iter(_row)

            _query = "INSERT INTO tbl_reviews \
                      (fld_gateway_id, fld_concern, fld_rationale, \
                       fld_parent_id) \
                      VALUES (%d, '%s', '%s', '%s')"                                                     % \
                     (self.gateway_id, _concern, _rationale, _parent)
            _util.set_cursor(self._app, gtk.gdk.LEFT_PTR)
            _dialog.destroy()
            if not self._app.COMDB.execute_query(
                    _query, None, self._app.ComCnx, commit=True):
                _util.rtk_error(
                    _(u"Error creating new program review "
                      u"gateway."))
                return True

            self._load_review_criteria(None)

        else:
            _dialog.destroy()

        return False

    def _delete_gateway(self, __toolbutton):
        """
        Method to delete an existing gateway from the common RTK database.

        :param gtk.Toolbutton __toolbutton: the gtk.ToolButton() that called
                                            this method.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _query = "DELETE FROM tbl_gateways \
                  WHERE fld_gateway_id=%d" % self.gateway_id
        if not self._app.COMDB.execute_query(
                _query, None, self._app.ComCnx, commit=True):
            _util.rtk_error(
                _(u"Error removing review gateway %d.") % self.gateway_id)
            return True

        self._load_gateways()
        self.cmbGateways.set_active(0)

        return False

    def _delete_criteria(self, __toolbutton):
        """
        Method to delete the selected review criteria from the common RTK
        database.

        :param gtk.ToolButton __toolbutton: the gtk.ToolButton() that called
                                            this method.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = self.treeview.get_selection().get_selected()
        _concern_id = _model.get_value(_row, 0)

        _query = "DELETE FROM tbl_reviews \
                  WHERE fld_gateway_id=%d \
                  AND fld_concern_id=%d" % (self.gateway_id, _concern_id)
        if not self._app.COMDB.execute_query(
                _query, None, self._app.ComCnx, commit=True):
            _util.rtk_error(
                _(u"Error removing review criteria %d from "
                  u"review gateway %d.") % (_concern_id, self.gateway_id))
            return True

        self._load_review_criteria(None)

        return False

    def _save_criteria(self, __toolbutton):
        """
        Method to save changes to the review criteria to the common RTK
        database.

        :param gtk.ToolButton __toolbutton: the gtk.ToolButton() that called
                                            this method.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        def _save_line(model, __path, row, self):
            """
            Function to save an individual line in the review criteria
            gtk.TreeView().

            """

            _concern_id = _model.get_value(row, 0)
            _concern = _model.get_value(row, 1)
            _rationale = _model.get_value(row, 2)

            _query = "UPDATE tbl_reviews \
                      SET fld_concern='%s', fld_rationale='%s' \
                      WHERE fld_concern_id=%d"                                               % \
                     (_concern, _rationale, _concern_id)
            if not self._app.COMDB.execute_query(
                    _query, None, self._app.ComCnx, commit=True):
                _util.rtk_error(
                    _(u"Error saving review gateway %d criteria "
                      u"%d.") % (self.gateway_id, _concern_id))
                return True

            return False

        _model = self.treeview.get_model()
        _model.foreach(_save_line, self)

        return False
