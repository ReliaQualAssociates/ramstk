#!/usr/bin/env python
"""
This is the List Book view for RTK.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       ListBook.py is part of the RTK Project
#
# All rights reserved.

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

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import configuration as _conf
    import utilities as _util
    import widgets as _widg
except ImportError:
    import rtk.configuration as _conf
    import rtk.utilities as _util
    import rtk.widgets as _widg

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ListView(gtk.Window):
    """
    This is the List view class for the pyGTK multiple window interface.
    """

    def __init__(self):
        """
        Initialize an instance of the List view class.
        """

        # Define private dictionary variables.
        # Dictionary to hold the Assembly ID/Hardware Tree treemodel paths.
        # This is used to keep the Hardware Tree and the Parts List in sync.
        self._treepaths = {}

        # Define private list variables.
        self._VISIBLE_PARTS_ = []

        # Define private scalar variables.
        self._assembly_id = 0

        # Define public dictionary variables.
        self.parttreepaths = {}
        self.dicPartValues = {}

        # Define public object variables.
        self.objPartModel = None

        # Create a new window and set its properties.
        gtk.Window.__init__(self)
        self.set_title(_(u"RTK Lists"))
        self.set_resizable(True)
        self.set_deletable(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)

        _n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        _width = gtk.gdk.screen_width() / _n_screens
        _height = gtk.gdk.screen_height()

        self.set_default_size((_width / 3) - 10, (2 * _height / 7))
        self.set_border_width(5)
        self.set_position(gtk.WIN_POS_NONE)
        self.move((2 * _width / 3), 0)

        #self.connect('delete_event', self.delete_event)

        # Create the gtk.Notebook widget to hold the parts list, RG tests list,
        # program incidents, and survival analyses list.
        self.notebook = gtk.Notebook()

        # Find the user's preferred gtk.Notebook() tab position.
        if _conf.TABPOS[1] == 'left':
            self.notebook.set_tab_pos(gtk.POS_LEFT)
        elif _conf.TABPOS[1] == 'right':
            self.notebook.set_tab_pos(gtk.POS_RIGHT)
        elif _conf.TABPOS[1] == 'top':
            self.notebook.set_tab_pos(gtk.POS_TOP)
        else:
            self.notebook.set_tab_pos(gtk.POS_BOTTOM)

        #self.notebook.connect('switch-page', self.notebook_page_switched)

        # Create the parts list tab for the LIST Object.
        (self.tvwPartsList,
         self._col_order) = _widg.make_treeview('Parts', 7, None,
                                                None, _conf.RTK_COLORS[14],
                                                _conf.RTK_COLORS[15])
        self._create_parts_list_page()

        # Create the reliability testing tab for the List class.
        (self.tvwTesting,
         self._rg_col_order) = _widg.make_treeview('Testing', 11, None,
                                                   None, _conf.RTK_COLORS[14],
                                                   _conf.RTK_COLORS[15])
        self._create_testing_page()

        # Create the program incidents tab for the LIST object.
        (self.tvwIncidents,
         self._incident_col_order) = _widg.make_treeview('Incidents', 14,
                                                         None, None,
                                                         _conf.RTK_COLORS[12],
                                                         _conf.RTK_COLORS[13])
        self._create_incidents_page()
        #self.tvwIncidents.connect('row_activated',
        #                          self._treeview_row_changed, 1)

        # Create the dataset tab for the LIST object.
        (self.tvwDatasets,
         self._dataset_col_order) = _widg.make_treeview('Dataset', 16,
                                                        None, None,
                                                        _conf.RTK_COLORS[12],
                                                        _conf.RTK_COLORS[13])
        self._create_survival_analysis_page()
        #self.tvwDatasets.connect('row_activated',
        #                         self._treeview_row_changed, 2)

        # Create a statusbar for the list/matrix window.
        self.statusbar = gtk.Statusbar()

        _vbox = gtk.VBox()
        _vbox.pack_start(self.notebook, expand=True, fill=True)
        _vbox.pack_start(self.statusbar, expand=False, fill=False)

        self.add(_vbox)
        self.show_all()

        self.statusbar.push(1, _(u"Ready"))

    def create_list_page(self, view, controller):
        """
        Method to create a Module view page.

        :param view:
        :param controller:
        :return:
        :rtype:
        """

        pass

    def _create_parts_list_page(self):
        """
        Method to create the parts list page in the List view.
        """

        #self.tvwPartsList.connect('button_release_event', self._tree_clicked)
        #self.tvwPartsList.connect('row_activated', self._row_activated)

        # Create the Parts list.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwPartsList)

        _frame = _widg.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Parts List</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the list of parts for the "
                                  u"selected Revision, Function, or "
                                  u"Hardware item."))

        self.notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _create_testing_page(self):
        """
        Method to create the tab containing the list of reliability growth
        and reliability demonstration plans for the Program.
        """

        # Create the Reliability Test list.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self.tvwTesting)

        _frame = _widg.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Reliability\nTests</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the list of HALT, HASS, ALT, "
                                  u"ESS, reliability growth and reliability "
                                  u"demonstration tests for the selected "
                                  u"Revision or Hardware item."))

        self.notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _create_incidents_page(self):
        """
        Method to create the tab containing the list of program incidents.
        """

        # Create the Program Incidents list.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self.tvwIncidents)

        _frame = _widg.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Program\nIncidents</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the list of program incidents "
                                  u"for the selected Revision, Hardware item, "
                                  u"or Software item."))

        self.notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _create_survival_analysis_page(self):
        """
        Method to create the tab containing the list of survival analyses.
        """

        # Create the Program Incidents list.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self.tvwDatasets)

        _frame = _widg.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Survival\nAnalyses</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the list of survival (Weibull) "
                                  u"analyses for the selected Revision or "
                                  u"Hardware item."))

        self.notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False
