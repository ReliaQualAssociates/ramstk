#!/usr/bin/env python
"""
#############################
Multiline CellRenderer Module
#############################
"""

# -*- coding: utf-8 -*-
#
#       gui.gtk.CellRendererML.py is part of The RTK Project
#
# All rights reserved.

import gettext
import sys

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

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2016 Andrew "weibullguy" Rowland'

_ = gettext.gettext


class CellRendererML(gtk.CellRendererText):
    """
    Class to create a multi-line cell renderer.  It is based on the base class
    gtk.CellRendererText().
    """

    def __init__(self):

        gtk.CellRendererText.__init__(self)

        self.textedit_window = None
        self.selection = None
        self.treestore = None
        self.treeiter = None

        self.textedit = gtk.TextView()
        self.textbuffer = self.textedit.get_buffer()

    def do_get_size(self, widget, cell_area):
        """
        Method to get the size of the CellRendererML.
        """

        size_tuple = gtk.CellRendererText.do_get_size(self, widget, cell_area)

        return size_tuple

    def do_start_editing(self, __event, treeview, path, __background_area,
                         cell_area, __flags):
        """


        :param __event:
        :param treeview:
        :param path:
        :param __background_area:
        :param cell_area:
        :param __flags:
        """

        if not self.get_property('editable'):
            return

        self.selection = treeview.get_selection()
        self.treestore, self.treeiter = self.selection.get_selected()

        self.textedit_window = gtk.Dialog(parent=treeview.get_toplevel())
        self.textedit_window.action_area.hide()
        self.textedit_window.set_decorated(False)
        self.textedit_window.set_property('skip-taskbar-hint', True)
        self.textedit_window.set_transient_for(None)

        self.textedit.set_editable(True)
        self.textedit.set_property('visible', True)
        self.textbuffer.set_property('text', self.get_property('text'))

        self.textedit_window.connect('key-press-event', self._keyhandler)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.set_property('visible', True)
        # self.textedit_window.vbox.pack_start(scrolled_window)

        scrolled_window.add(self.textedit)
        self.textedit_window.vbox.add(scrolled_window)
        self.textedit_window.realize()

        # Position the popup below the edited cell (and try hard to keep the
        # popup within the toplevel window)
        (tree_x, tree_y) = treeview.get_bin_window().get_origin()
        (tree_w, tree_h) = treeview.window.get_geometry()[2:4]
        (t_w, t_h) = self.textedit_window.window.get_geometry()[2:4]
        x_pos = tree_x + min(cell_area.x,
                             tree_w - t_w + treeview.get_visible_rect().x)
        y_pos = tree_y + min(cell_area.y,
                             tree_h - t_h + treeview.get_visible_rect().y)
        self.textedit_window.move(x_pos, y_pos)
        self.textedit_window.resize(cell_area.width, cell_area.height)

        # Run the dialog, get response by tracking keypresses
        response = self.textedit_window.run()

        if response == gtk.RESPONSE_OK:
            self.textedit_window.destroy()

            (iter_first, iter_last) = self.textbuffer.get_bounds()
            text = self.textbuffer.get_text(iter_first, iter_last)

            # self.treestore[path][2] = text

            treeview.set_cursor(path, None, False)

            self.emit('edited', path, text)

        elif response == gtk.RESPONSE_CANCEL:
            self.textedit_window.destroy()
        else:
            print "response %i received" % response
            self.textedit_window.destroy()

    def _keyhandler(self, __widget, event):
        """


        :param __widget:
        :param event:
        """

        _keyname = gtk.gdk.keyval_name(event.keyval)
        if event.state & (gtk.gdk.SHIFT_MASK | gtk.gdk.CONTROL_MASK) and \
                _keyname == 'Return':
            self.textedit_window.response(gtk.RESPONSE_OK)

# Register the new widget types.
gobject.type_register(CellRendererML)
