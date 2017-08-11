#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.moduleviews.Revision.py is part of The RTK Project
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

"""
############################
Revision Package ModuleView
############################
"""

import sys

# Import modules for localization support.
import gettext
import locale

from pubsub import pub

# Modules required for the GUI.
try:
    # noinspection PyUnresolvedReferences
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    # noinspection PyUnresolvedReferences
    import gtk
except ImportError:
    sys.exit(1)
try:
    # noinspection PyUnresolvedReferences
    import gtk.glade
except ImportError:
    sys.exit(1)
try:
    # noinspection PyUnresolvedReferences
    import gobject
except ImportError:
    sys.exit(1)

# Import other RTK modules.
try:
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.gui.gtk.Widgets as Widgets

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

_ = gettext.gettext


class ModuleView(gtk.ScrolledWindow):

    """
    The Module Book view displays all the Revisions associated with the RTK
    Project in a flat list.  The attributes of a Module Book view are:

    :ivar _mdcRTK: the :py:class:`rtk.RTK.RTK` data controller instance.
    :ivar _configuration: the :py:class:`rtk.Configuration.Configuration`
                          instance for the currently running RTK.
    :ivar _dtc_revision: the :py:class:`rtk.revision.Revision.Revision` data
                         controller to use for accessing the Revision data
                         models.
    :ivar _lst_col_order: list containing the order of the columns in the
                          Module View gtk.TreeView().
    :ivar hbx_tab_label: the gtk.HBox() used for the label in the ModuleBook.
    :ivar tvw_revision: the gtk.TreeView() displaying the list of Revisions.
    """

    def __init__(self, controller):
        """
        Method to initialize the Module Book view for the Revision package.

        :param controller: the RTK Master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        gtk.ScrolledWindow.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_col_order = []

        # Initialize private scalar attributes.
        self._mdcRTK = controller
        self._configuration = controller.RTK_CONFIGURATION
        self._dtc_revision = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.hbx_tab_label = gtk.HBox()
        self.tvw_revision = None

        try:
            locale.setlocale(locale.LC_ALL, self._configuration.RTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

        # Create the main Revision class treeview.
        _bg_color = self._configuration.RTK_COLORS['revisionbg']
        _fg_color = self._configuration.RTK_COLORS['revisionfg']
        _fmt_file = self._configuration.RTK_CONF_DIR + \
            '/' + self._configuration.RTK_FORMAT_FILE['revision']
        (self.tvw_revision,
         self._lst_col_order) = Widgets.make_treeview('Revision', 0, _fmt_file,
                                                      _bg_color, _fg_color)

        self.tvw_revision.set_tooltip_text(
                _(u"Displays the list of revisions."))
        self.tvw_revision.connect('cursor_changed', self._on_row_changed,
                                  None, None)
        self.tvw_revision.connect('button_press_event', self._on_button_press)

        # Connect the cells to the callback function.
        for i in [17, 20, 22]:
            _cell = self.tvw_revision.get_column(
                self._lst_col_order[i]).get_cell_renderers()
            _cell[0].connect('edited', self._on_cell_edited, i,
                             self.tvw_revision.get_model())

        _icon = self._configuration.RTK_ICON_DIR + '/32x32/revision.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        _image = gtk.Image()
        _image.set_from_pixbuf(_icon)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Revisions") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the program revisions."))

        self.hbx_tab_label.pack_start(_image)
        self.hbx_tab_label.pack_end(_label)
        self.hbx_tab_label.show_all()

        self.add(self.tvw_revision)
        self.show_all()

        pub.subscribe(self._on_program_open, 'openedProgram')
        pub.subscribe(self.on_edit, 'wvw_editedRevision')

    def _on_program_open(self):
        """
        Method to load the Revision Module Book view gtk.TreeModel() with
        Revision information when an RTK Program database is opened.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        self._dtc_revision = self._mdcRTK.dic_controllers['revision']
        _revisions = self._dtc_revision.request_select_all()

        _model = self.tvw_revision.get_model()
        _model.clear()
        for _key in _revisions.nodes.keys():
            if _key != 0:
                _model.append(None, _revisions[_key].data.get_attributes())
            else:
                _return = True

        _row = _model.get_iter_root()
        self.tvw_revision.expand_all()
        self.tvw_revision.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.tvw_revision.get_column(0)
            self.tvw_revision.row_activated(_path, _column)

        _module = self._mdcRTK.RTK_CONFIGURATION.RTK_PAGE_NUMBER[0]
        pub.sendMessage('mvw_switchedPage', module=_module)

        return _return

    def on_edit(self, position, new_text):
        """
        Method to update the Module Book gtk.TreeView() with changes to the
        Revision data model attributes.  Called by other views when the
        Revision data model attributes are edited via their gtk.Widgets().

        :ivar int position: the ordinal position in the Module Book
                            gtk.TreeView() of the data being updated.
        :ivar new_text: the new value of the attribute to be updated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_model, _row) = self.tvw_revision.get_selection().get_selected()

        _model.set(_row, self._lst_col_order[position], new_text)

        return False

    def _on_button_press(self, treeview, event):
        """
        Method for handling mouse clicks on the Revision package Module Book
        gtk.TreeView().

        :param gtk.TreeView treeview: the Revision class gtk.TreeView().
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

        if event.button == 1:
            self._on_row_changed(treeview, '', gtk.TreeViewColumn())
        elif event.button == 3:
            # FIXME: See bug 190.
            pass

        return False

    def _on_cell_edited(self, __cell, path, new_text, position, model):
        """
        Method to handle edits of the Revision package Module Book
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

        # Now update the Revision data model.
        if self._lst_col_order[position] == 17:
            self._dtm_revision.name = str(new_text)
        elif self._lst_col_order[position] == 20:
            self._dtm_revision.remarks = str(new_text)
        elif self._lst_col_order[position] == 22:
            self._dtm_revision.code = str(new_text)

        pub.sendMessage('mvw_editedRevision',
                        revision_id=self._dtm_revision.revision_id)

        return False

    def _on_row_changed(self, treeview, __path, __column):
        """
        Method to handle events for the Revision package Module Book
        gtk.TreeView().  It is called whenever a Module Book gtk.TreeView()
        row is activated.

        :param gtk.TreeView treeview: the Revision class gtk.TreeView().
        :param str __path: the actived row gtk.TreeView() path.
        :param gtk.TreeViewColumn __column: the actived gtk.TreeViewColumn().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        (_model, _row) = treeview.get_selection().get_selected()

        _revision_id = _model.get_value(_row, 0)
        self._dtm_revision = self._dtc_revision.request_select(_revision_id)

        pub.sendMessage('selectedRevision', revision_id=_revision_id)

        return _return
