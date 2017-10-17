# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.Book.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
PyGTK Multi-Window Interface Book
===============================================================================
"""

import sys

# Import modules for localization support.
import gettext
import locale

# Import modules required for the GUI.
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

# Import other RTK modules.

_ = gettext.gettext


def destroy(__widget, __event=None):
    """
    Quits the RTK application when the X in the upper right corner is pressed
    or if this function is called as a callback.

    :param __widget: the gtk.Widget() that called this method.
    :type __widget: :py:class:`gtk.Widget`
    :keyword __event: the gtk.gdk.Event() that called this method.
    :type __event: :py:class:`gtk.gdk.Event`
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    gtk.main_quit()

    return False


class RTKBook(gtk.Window):               # pylint: disable=R0904
    """
    This is the base view for the pyGTK multiple window interface List Book,
    Module Book, and Work Book.  Attributes of the RTKBook are:

    :ivar list _lst_handler_id:
    :ivar _mdcRTK: the RTK master data controller.
    :type _mdcRTK: :py:class:`rtk.RTK.RTK`
    :ivar notebook: the gtk.Notebook() widget used to hold each of the RTK
                    module WorkViews.
    :type notebook: :py:class:`gtk.Notebook`
    :ivar menubar: the gtk.MenuBar() for the RTK ModuleBook menu.
    :type menubar: :py:class:`gtk.MenuBar`
    :ivar toolbar: the gtk.Toolbar() for the RTK ModuleBook tools.
    :type toolbar: :py:class:`gtk.Toolbar`
    :ivar statusbar: the gtk.Statusbar() for displaying messages.
    :type statusbar: :py:class:`gtk.Statusbar`
    :ivar progressbar: the gtk.Progressbar() for displaying progress counters.
    :type progressbar: :py:class:`gtk.Progressbar`
    """

    _left_tab = gtk.POS_LEFT
    _right_tab = gtk.POS_RIGHT
    _top_tab = gtk.POS_TOP
    _bottom_tab = gtk.POS_BOTTOM

    def __init__(self, controller):
        """
        Method to initialize an instance of the Module view class.

        :param controller: the RTK master data controller.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        gtk.Window.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._mdcRTK = controller
        self._n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        self._width = gtk.gdk.screen_width() / self._n_screens
        self._height = gtk.gdk.screen_height()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.notebook = gtk.Notebook()

        try:
            locale.setlocale(locale.LC_ALL,
                             controller.RTK_CONFIGURATION.RTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

        # Set the common properties for the Book and it's widgets.
        self.set_resizable(True)
        self.set_border_width(5)
        self.set_position(gtk.WIN_POS_NONE)

        self.connect('delete_event', destroy)

    def _on_module_change(self):
        """
        Method to load the correct List Views for the RTK module that was
        selected in the Module Book.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        # We remove any existing pages from the Book.  New pages will be added
        # by the List Book and the Work Book for the module that was just
        # selected.
        _n_pages = self.notebook.get_n_pages()
        if _n_pages > 0:
            for _page in list(xrange(_n_pages)):
                self.notebook.remove_page(-1)

        return _return
