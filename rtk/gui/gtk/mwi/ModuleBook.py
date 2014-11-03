#!/usr/bin/env python
"""
This is the Module Book window for RTK.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       ModuleBook.py is part of The RTK Project
#
# All rights reserved.

import sys

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
try:
    import gobject
except ImportError:
    sys.exit(1)

import gettext
import locale

# Import other RTK modules.
import configuration as _conf
from ListBook import ListView
from WorkBook import WorkView

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ModuleView(gtk.Window):
    """
    This is the Module view for the pyGTK multiple window interface.
    """

    def __init__(self):
        """
        Initialize an instance of the Module view class.
        """

        # Create a new window and set its properties.
        gtk.Window.__init__(self)
        self.set_resizable(True)
        self.set_title(_(u"RTK Module Book"))

        _n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        _width = gtk.gdk.screen_width() / _n_screens
        _height = gtk.gdk.screen_height()

        if _conf.OS == 'Linux':
            _width = (2 * _width / 3) - 10
            _height = 2 * _height / 7
        elif _conf.OS == 'Windows':
            _width = (2 * _width / 3) - 30
            _height = 2 * _height / 7

        self.set_default_size(_width, _height)

        self.set_border_width(5)
        self.set_position(gtk.WIN_POS_NONE)
        self.move(0, 0)

        self.connect('delete_event', self.destroy)

        _vbox = gtk.VBox()

        self.menubar = self._create_menu()
        _vbox.pack_start(self.menubar, expand=False, fill=False)

        self.toolbar = self._create_toolbar()
        _vbox.pack_start(self.toolbar, expand=False, fill=False)

        # Find the user's preferred gtk.Notebook tab position.
        if _conf.TABPOS[0] == 'left':
            _position = gtk.POS_LEFT
        elif _conf.TABPOS[0] == 'right':
            _position = gtk.POS_RIGHT
        elif _conf.TABPOS[0] == 'top':
            _position = gtk.POS_TOP
        else:
            _position = gtk.POS_BOTTOM

        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(_position)
        self.notebook.connect('switch-page', self._on_switch_page)

        _vbox.pack_start(self.notebook, expand=True, fill=True)

        self.statusbar = gtk.Statusbar()
        self.statusbar.push(1, _(u"Ready"))

        self.progressbar = gtk.ProgressBar(adjustment=None)
        self.progressbar.set_pulse_step(0.25)
        self.statusbar.add(self.progressbar)

        _vbox.pack_start(self.statusbar, expand=False, fill=False)

        self.add(_vbox)

        self.show_all()

    def create_listview(self):

        self.listview = ListView()

        return self.listview

    def create_workview(self):

        self.workview = WorkView()

        return self.workview

    def _create_menu(self):
        """
        Creates the menu for the ModuleBook view.
        """

        _menu = gtk.Menu()

        _menu2 = gtk.Menu()
        _menu_item = gtk.MenuItem(label=_(u"_Project"), use_underline=True)
        #_menu_item.connect('activate', _util.create_project, self)
        _menu2.append(_menu_item)

        # Add assembly entry.
        _menu_item = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/insert_sibling.png')
        _menu_item.set_label(_(u"Sibling Assembly"))
        _menu_item.set_image(_image)
        #_menu_item.connect('activate', self._app.HARDWARE.add_hardware, 0)
        _menu2.append(_menu_item)

        _menu_item = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '16x16/insert_child.png')
        _menu_item.set_label(_(u"Child Assembly"))
        _menu_item.set_image(_image)
        #_menu_item.connect('activate', self._app.HARDWARE.add_hardware, 1)
        _menu2.append(_menu_item)

        # Add component entry.
        _menu_item = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '16x16/part.png')
        _menu_item.set_label(_(u"Component"))
        _menu_item.set_image(_image)
        #_menu_item.connect('activate', self._app.HARDWARE.add_hardware, 2)
        _menu2.append(_menu_item)

        # Add New menu.
        _mnuNew = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '16x16/new.png')
        _mnuNew.set_label(_(u"New"))
        _mnuNew.set_image(_image)

        _mnuNew.set_submenu(_menu2)
        _menu.append(_mnuNew)

        _menu_item = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '16x16/open.png')
        _menu_item.set_label(_("Open"))
        _menu_item.set_image(_image)
        #_menu_item.connect('activate', _util.open_project, self._app)
        _menu.append(_menu_item)

        _menu_item = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '16x16/save.png')
        _menu_item.set_label(_("Save"))
        _menu_item.set_image(_image)
        #_menu_item.connect('activate', _util.save_project, self._app)
        _menu.append(_menu_item)

        _menu_item = gtk.MenuItem(label=_("Save _As"), use_underline=True)
        #_menu_item.connect('activate', _util.save_project, self._app)
        _menu.append(_menu_item)
        #_menu_item = gtk.MenuItem(label=_("_Close"), use_underline=True)
        #_menu_item.connect('activate', _util.close)
        #_menu.append(_menu_item)

        _menu_item = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '16x16/exit.png')
        _menu_item.set_label(_("Exit"))
        _menu_item.set_image(_image)
        #_menu_item.connect('activate', self.quit_RTK)
        _menu.append(_menu_item)

        _mnuFile = gtk.MenuItem(label=_("_File"), use_underline=True)
        _mnuFile.set_submenu(_menu)

        _menu = gtk.Menu()
        _menu_item = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '16x16/undo.png')
        _menu_item.set_label(_("Undo"))
        _menu_item.set_image(_image)
        #_menu_item.connect('activate', _util.undo)
        _menu.append(_menu_item)
        _menu_item = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '16x16/redo.png')
        _menu_item.set_label(_("Redo"))
        _menu_item.set_image(_image)
        #_menu_item.connect('activate', _util.redo)
        _menu.append(_menu_item)
        _menu_item = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '16x16/cut.png')
        _menu_item.set_label(_("Cut"))
        _menu_item.set_image(_image)
        #_menu_item.connect('activate', _util.cut_copy_paste, 0)
        _menu.append(_menu_item)
        _menu_item = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '16x16/copy.png')
        _menu_item.set_label(_("Copy"))
        _menu_item.set_image(_image)
        #_menu_item.connect('activate', _util.cut_copy_paste, 1)
        _menu.append(_menu_item)
        _menu_item = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '16x16/paste.png')
        _menu_item.set_label(_("Paste"))
        _menu_item.set_image(_image)
        #_menu_item.connect('activate', _util.cut_copy_paste, 2)
        _menu.append(_menu_item)
        _menu_item = gtk.MenuItem(label=_("Select _All"), use_underline=True)
        #_menu_item.connect('activate', _util.select_all)
        _menu.append(_menu_item)

        _mnuEdit = gtk.MenuItem(label=_("_Edit"), use_underline=True)
        _mnuEdit.set_submenu(_menu)

        _menu = gtk.Menu()
        _menu_item = gtk.MenuItem(label=_("_Find"), use_underline=True)
        #_menu_item.connect('activate', _util.find, 0)
        _menu.append(_menu_item)
        _menu_item = gtk.MenuItem(label=_("Find _Next"), use_underline=True)
        #_menu_item.connect('activate', _util.find, 1)
        _menu.append(_menu_item)
        _menu_item = gtk.MenuItem(label=_("Find _Previous"),
                                  use_underline=True)
        #_menu_item.connect('activate', _util.find, 2)
        _menu.append(_menu_item)
        _menu_item = gtk.MenuItem(label=_("_Replace"), use_underline=True)
        #_menu_item.connect('activate', _util.find, 3)
        _menu.append(_menu_item)

        _mnuSearch = gtk.MenuItem(label=_("_Search"), use_underline=True)
        _mnuSearch.set_submenu(_menu)

        # Create the View menu.
        _menu = gtk.Menu()
        _menu_item = gtk.MenuItem(label=_(u"Pro_cess Map"), use_underline=True)
        #_menu_item.connect('activate', ProcessMap, self._app)
        _menu.append(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"_Design Reviews"),
                                  use_underline=True)
        #_menu_item.connect('activate', DesignReview, self._app)
        _menu.append(_menu_item)

        _mnuView = gtk.MenuItem(label=_(u"_Process"), use_underline=True)
        _mnuView.set_submenu(_menu)

        _menu = gtk.Menu()
        _menu_item = gtk.MenuItem(label=_("_Options"), use_underline=True)
        #_menu_item.connect('activate', _util.options, self._app)
        _menu.append(_menu_item)
        _menu_item = gtk.MenuItem(label=_("_Composite Ref Des"),
                                  use_underline=True)
        #_menu_item.connect('activate', _util.create_comp_ref_des, self._app)
        _menu.append(_menu_item)
        _menu_item = gtk.MenuItem(label=_("_Update Design Review Criteria"),
                                  use_underline=True)
        #_menu_item.connect('activate', ReviewCriteria, self._app)
        _menu.append(_menu_item)
        _menu_item = gtk.MenuItem(label=_("_Add Parts to System Hierarchy"),
                                  use_underline=True)
        #_menu_item.connect('activate', _util.add_parts_system_hierarchy, self._app)
        _menu.append(_menu_item)

        _mnuTools = gtk.MenuItem(label=_("_Tools"), use_underline=True)
        _mnuTools.set_submenu(_menu)

        _menubar = gtk.MenuBar()
        _menubar.append(_mnuFile)
        _menubar.append(_mnuEdit)
        _menubar.append(_mnuSearch)
        _menubar.append(_mnuView)
        _menubar.append(_mnuTools)

        _menubar.show_all()

        return _menubar

    def _create_toolbar(self):
        """
        Creates the toolbar for the ModuleBook view.
        """

        _toolbar = gtk.Toolbar()

        _position = 0

        # New file button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Create a new RTK Project Database."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/new.png')
        _button.set_icon_widget(_image)
        #_button.connect('clicked', _util.create_project, self._app)
        _toolbar.insert(_button, _position)
        _position += 1

        # Connect button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Connect to an existing RTK Project "
                                   u"Database."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/open.png')
        _button.set_icon_widget(_image)
        #_button.connect('clicked', _util.open_project, self._app)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Save the currently open RTK Project "
                                   u"Database."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        #_button.connect('clicked', _util.save_project, self._app)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save and quit button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Save the currently open RTK Program "
                                   u"Database then quits."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/save-exit.png')
        _button.set_icon_widget(_image)
        #_button.connect('clicked', self.save_quit_RTK)
        _toolbar.insert(_button, _position)
        _position += 1

        # Quit without saving button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Quits without saving the currently open "
                                   u"RTK Program Database."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/exit.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self.destroy)
        _toolbar.insert(_button, _position)

        _toolbar.show_all()

        return _toolbar

    def create_module_page(self, view, controller, position=-1):
        """
        Method to create a Module view page.

        :param view: instance of RTK module view class to add to the RTK Work
                     Book.
        :param controller: the RTK module data controller for the RTK module
                           view to use when communicating with the model.
        :keyword int position: the position in the RTK Work Book to add the
                               RTK module view.  Defaults to -1 (at the end).
        :return: RTK module view class instance.
        :rtype: object
        """

        return view(controller, self, position)

    def load_module_page(self, view, dao):
        """
        Method to request the RTK module data controller retrieve the data from
        the RTK model and load it into the RTK module view.

        :param view: the RTK module view class instance to load with data.
        :param rtk.dao.DAO dao: the data access object for the view to pass to
                                the data controller.
        :return:
        :rtype:
        """

        self.workview.add(view._workbook)
        self.workview.show_all()

        _page = view.request_load_data(dao)

        return _page

    def _on_switch_page(self, notebook, page, page_num):
        """
        Called whenever the Module Book gtk.Notebook() page is changed.

        :param gtk.Notebook notebook: the Tree Book notebook widget.
        :param gtk.Widget page: the newly selected page's child widget.
        :param int page_num: the newly selected page number.
                             0 = Revision Tree
                             1 = Function Tree
                             2 = Requirements Tree
                             3 = Hardware Tree
                             4 = Software Tree
                             5 = Validation Tree
                             6 = Reliability Testing Tree
                             7 = Field Incident Tree
                             8 = Survival Analyses Tree
        """

        # Remove the existing Work Book before adding the new one.
        if self.workview.get_child() is not None:
            self.workview.remove(self.workview.get_child())

        #if page_num == 0:
        #    print _conf.RTK_MODULES[page_num]
        #elif _conf.RTK_PAGE_NUMBER[page_num] == 1:
        #    pass
        #elif _conf.RTK_PAGE_NUMBER[page_num] == 2:
        #    pass
        #elif _conf.RTK_PAGE_NUMBER[page_num] == 3:
        #    pass
        #elif _conf.RTK_PAGE_NUMBER[page_num] == 4:
        #    pass
        #elif _conf.RTK_PAGE_NUMBER[page_num] == 5:
        #    pass
        #elif _conf.RTK_PAGE_NUMBER[page_num] == 6:
        #    pass
        #elif _conf.RTK_PAGE_NUMBER[page_num] == 7:
        #    pass
        #elif _conf.RTK_PAGE_NUMBER[page_num] == 8:
        #    pass

        return False

    def destroy(self, __widget, __event=None, data=None):
        """
        Method to quit the RTK application when the X in the upper
        right corner is pressed.

        :param gtk.Widget __widget: the gtk.Widget() that called this method.
        :keyword gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                        method.
        :keyword data: any user-supplied data.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        gtk.main_quit()

        return False
