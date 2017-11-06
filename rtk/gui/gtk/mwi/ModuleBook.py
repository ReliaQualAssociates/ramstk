# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.mwi.ModuleBook.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
RTKModuleBook Module
-------------------------------------------------------------------------------
"""

import sys

# Import modules for localization support.
import gettext

from pubsub import pub                              # pylint: disable=E0401

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
# pylint: disable=E0401
from gui.gtk.rtk import RTKBook, destroy
from gui.gtk.moduleviews import mvwRevision
from gui.gtk.moduleviews import mvwFunction
from gui.gtk.moduleviews import mvwRequirement
from gui.gtk.assistants import CreateProject, OpenProject, DeleteProject, \
    Options

_ = gettext.gettext


class ModuleBook(RTKBook):               # pylint: disable=R0904
    """
    This is the Module view for the pyGTK multiple window interface.
    Attributes of the ModuleView are:

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

    def __init__(self, controller):
        """
        Method to initialize an instance of the Module view class.

        :param controller: the RTK master data controller.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        RTKBook.__init__(self, controller)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.dic_module_views = {'revision':[mvwRevision(controller), 0],
                                 'function':[mvwFunction(controller), 1],
                                 'requirement':[mvwRequirement(controller), 2]}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.progressbar = gtk.ProgressBar(adjustment=None)
        self.statusbar = gtk.Statusbar()

        # Set the properties for the ModuleBook and it's widgets.
        self.set_title(_(u"RTK Module Book"))

        if self._mdcRTK.RTK_CONFIGURATION.RTK_OS == 'Linux':
            _width = (2 * self._width / 3) - 10
            _height = 2 * self._height / 7
        elif self._mdcRTK.RTK_CONFIGURATION.RTK_OS == 'Windows':
            _width = (2 * self._width / 3) - 30
            _height = 2 * self._height / 7

        self.set_default_size(_width, _height)
        self.move(0, 0)

        if self._mdcRTK.RTK_CONFIGURATION.RTK_TABPOS['modulebook'] == 'left':
            self.notebook.set_tab_pos(self._left_tab)
        elif self._mdcRTK.RTK_CONFIGURATION.RTK_TABPOS['modulebook'] == 'right':
            self.notebook.set_tab_pos(self._right_tab)
        elif self._mdcRTK.RTK_CONFIGURATION.RTK_TABPOS['modulebook'] == 'top':
            self.notebook.set_tab_pos(self._top_tab)
        else:
            self.notebook.set_tab_pos(self._bottom_tab)

        self.progressbar.set_pulse_step(0.25)
        self.statusbar.add(self.progressbar)

        self._lst_handler_id.append(
            self.notebook.connect('select-page', self._on_switch_page))
        self._lst_handler_id.append(
            self.notebook.connect('switch-page', self._on_switch_page))

        # Insert a page for each of the active RTK Modules.
        for _page in self.dic_module_views:
            _object = self.dic_module_views[_page]
            self.notebook.insert_page(_object[0],
                                      tab_label=_object[0].hbx_tab_label,
                                      position=_object[1])

        _vbox = gtk.VBox()
        _vbox.pack_start(self._make_menu(), expand=False, fill=False)
        _vbox.pack_start(self._make_toolbar(), expand=False, fill=False)
        _vbox.pack_start(self.notebook, expand=True, fill=True)
        _vbox.pack_start(self.statusbar, expand=False, fill=False)

        self.add(_vbox)

        self.show_all()
        self.notebook.set_current_page(0)

        self.statusbar.push(1, _(u"Ready"))

        pub.subscribe(self._on_request_open, 'requestOpen')
        pub.subscribe(self._on_open, 'openedProgram')

    def _make_menu(self):
        """
        Method to create the menu for the ModuleBook view.

        :return _menubar: the gtk.MenuBar() for the RTK ModuleBook.
        :type _menubar: :py:class:`gtk.MenuBar`
        """

        _icon_dir = self._mdcRTK.RTK_CONFIGURATION.RTK_ICON_DIR

        _menu = gtk.Menu()

        _menu_item = gtk.MenuItem(label=_(u"New _Project"), use_underline=True)
        _menu_item.connect('activate', CreateProject, self._mdcRTK)
        _menu.append(_menu_item)

        _menu_item = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/open.png')
        _menu_item.set_label(_(u"_Open"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        _menu_item.connect('activate', OpenProject, self._mdcRTK)
        _menu.append(_menu_item)

        _menu_item = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/save.png')
        _menu_item.set_label(_(u"_Save"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        _menu_item.connect('activate', self._request_save_project)
        _menu.append(_menu_item)

        _menu_item = gtk.MenuItem(label=_(u"_Close"), use_underline=True)
        _menu_item.connect('activate', self._request_close_project)
        _menu.append(_menu_item)

        _menu_item = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/exit.png')
        _menu_item.set_label(_(u"E_xit"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        _menu_item.connect('activate', destroy)
        _menu.append(_menu_item)

        _mnuFile = gtk.MenuItem(label=_(u"_File"), use_underline=True)
        _mnuFile.set_submenu(_menu)

        _menu = gtk.Menu()
        _menu_item = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/undo.png')
        _menu_item.set_label(_(u"Undo"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        # _menu_item.connect('activate', Utilities.undo)
        _menu.append(_menu_item)
        _menu_item = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/redo.png')
        _menu_item.set_label(_(u"Redo"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        # _menu_item.connect('activate', Utilities.redo)
        _menu.append(_menu_item)
        _menu_item = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/cut.png')
        _menu_item.set_label(_(u"Cut"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        # _menu_item.connect('activate', Utilities.cut_copy_paste, 0)
        _menu.append(_menu_item)
        _menu_item = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/copy.png')
        _menu_item.set_label(_(u"Copy"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        # _menu_item.connect('activate', Utilities.cut_copy_paste, 1)
        _menu.append(_menu_item)
        _menu_item = gtk.ImageMenuItem()
        _image = gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/paste.png')
        _menu_item.set_label(_(u"Paste"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        # _menu_item.connect('activate', Utilities.cut_copy_paste, 2)
        _menu.append(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"Select _All"), use_underline=True)
        # _menu_item.connect('activate', Utilities.select_all)
        _menu.append(_menu_item)

        _mnuEdit = gtk.MenuItem(label=_(u"_Edit"), use_underline=True)
        _mnuEdit.set_submenu(_menu)

        _menu = gtk.Menu()
        _menu_item = gtk.MenuItem(label=_(u"_Find"), use_underline=True)
        # _menu_item.connect('activate', Utilities.find, 0)
        _menu.append(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"Find _Next"), use_underline=True)
        # _menu_item.connect('activate', Utilities.find, 1)
        _menu.append(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"Find _Previous"),
                                  use_underline=True)
        # _menu_item.connect('activate', Utilities.find, 2)
        _menu.append(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"_Replace"), use_underline=True)
        # _menu_item.connect('activate', Utilities.find, 3)
        _menu.append(_menu_item)

        _mnuSearch = gtk.MenuItem(label=_(u"_Search"), use_underline=True)
        _mnuSearch.set_submenu(_menu)

        # Create the View menu.
        _menu = gtk.Menu()
        _menu_item = gtk.MenuItem(label=_(u"Pro_cess Map"), use_underline=True)
        # _menu_item.connect('activate', ProcessMap, self._app)
        _menu.append(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"_Design Reviews"),
                                  use_underline=True)
        # _menu_item.connect('activate', DesignReview, self._app)
        _menu.append(_menu_item)

        _mnuView = gtk.MenuItem(label=_(u"_Process"), use_underline=True)
        _mnuView.set_submenu(_menu)

        _menu = gtk.Menu()
        _menu_item = gtk.MenuItem(label=_(u"_Options"), use_underline=True)
        _menu_item.connect('activate', Options, self._mdcRTK)
        _menu.append(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"_Composite Ref Des"),
                                  use_underline=True)
        _menu_item.connect('activate', self._create_comp_ref_des)
        _menu.append(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"_Update Design Review Criteria"),
                                  use_underline=True)
        # _menu_item.connect('activate', ReviewCriteria, self._app)

        _mnuTools = gtk.MenuItem(label=_(u"_Tools"), use_underline=True)
        _mnuTools.set_submenu(_menu)

        _menubar = gtk.MenuBar()
        _menubar.append(_mnuFile)
        _menubar.append(_mnuEdit)
        _menubar.append(_mnuSearch)
        _menubar.append(_mnuView)
        _menubar.append(_mnuTools)

        _menubar.show_all()

        return _menubar

    def _make_toolbar(self):
        """
        Method to create the toolbar for the ModuleBook view.

        :return _toolbar: the gtk.Toolbar() for the RTK ModuleBook.
        :type _toolbar: :py:class:`gtk.Toolbar`
        """

        _icon_dir = self._mdcRTK.RTK_CONFIGURATION.RTK_ICON_DIR

        _toolbar = gtk.Toolbar()

        _position = 0

        # New file button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Create a new RTK Project Database."))
        _image = gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/new.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', CreateProject, self._mdcRTK)
        _toolbar.insert(_button, _position)
        _position += 1

        # Connect button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Connect to an existing RTK Project "
                                   u"Database."))
        _image = gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/open.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', OpenProject, self._mdcRTK)
        _toolbar.insert(_button, _position)
        _position += 1

        # Delete button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Deletes an existing RTK Program "
                                   u"Database."))
        _image = gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/delete.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', DeleteProject, self._mdcRTK)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Save the currently open RTK Project "
                                   u"Database."))
        _image = gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/save.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_save_project)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save and quit button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Save the currently open RTK Program "
                                   u"Database then quits."))
        _image = gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/save-exit.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_save_project, True)
        _toolbar.insert(_button, _position)
        _position += 1

        # Quit without saving button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Quits without saving the currently open "
                                   u"RTK Program Database."))
        _image = gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/exit.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', destroy)
        _toolbar.insert(_button, _position)

        _toolbar.show_all()

        return _toolbar

    def _on_request_open(self):
        """
        Method to set the status bar and update the progress bar when opening
        an RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _message = _(u"Opening Program Database {0:s}"). \
            format(self._mdcRTK.RTK_CONFIGURATION.RTK_PROG_INFO['database'])
        self.statusbar.push(1, _message)
        self.set_title(_(u"RTK - Analyzing {0:s}").format(
            self._mdcRTK.RTK_CONFIGURATION.RTK_PROG_INFO['database']))

        return _return

    def _on_open(self):
        """
        Method to update the status bar and clear the progress bar when the
        RTK Program database has opened.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        self.statusbar.pop(1)

        return _return

    def _on_switch_page(self, __notebook, __page, page_num):
        """
        Called whenever the Module Book gtk.Notebook() page is changed.

        :param __notebook: the Tree Book notebook widget.
        :type __notebook: :py:class:`gtk.Notebook`
        :param __page: the newly selected page's child widget.
        :type __page: :py:class:`gtk.Widget`
        :param int page_num: the newly selected page number.

                             0 = Revision Tree
                             1 = Function Tree
                             2 = Requirements Tree
                             3 = Hardware Tree
                             4 = Software Tree
                             5 = Testing Tree
                             6 = Validation Tree
                             7 = Incident Tree
                             8 = Survival Analyses Tree

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Key errors occur when no RTK Program database has been loaded.  In
        # that case, select the Revision page to load.
        try:
            _module = self._mdcRTK.RTK_CONFIGURATION.RTK_PAGE_NUMBER[page_num]
        except KeyError:
            if page_num == 0:
                _module = 'revision'
            elif page_num == 1:
                _module = 'function'
            elif page_num == 2:
                _module = 'requirement'

        pub.sendMessage('mvwSwitchedPage', module=_module)

        return False

    def _request_save_project(self, __widget, end=False):
        """
        Method to request the RTK master data controller save the open Project.

        :param gtk.Widget __widget: the gtk.Widget() that called this method.
        :keyword bool close: indicates whether or not to quit RTK after saving
                             the project.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._mdcRTK.save_project()

        if end:
            destroy(__widget)

        return False

    def _request_close_project(self, __widget):
        """
        Method to request the RTK master data controller close the open
        Project.

        :param gtk.Widget __widget: the gtk.Widget() that called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._mdcRTK.close_project()

        return False

    def _create_comp_ref_des(self, __widget):
        """
        Method to iterively create composite reference designators.

        :param gtk.Widget __widget: the gtk.Widget() that called this function.
        :return: False if successful or True if an error is encounterd.
        """
        # TODO: Move this to the Hardware module.
        _hardware = self._mdcRTK.RTK_CONFIGURATION.RTK_MODULES[3]
        _model = _hardware.treeview.get_model()

        _model.foreach(self._build_composite_ref_des)

        return False

    def _build_composite_ref_des(self, model, __path, row):
        """
        Method to build the composite reference designator.

        :return: False if successful or True if an error is encountered
        :rtype: bool
        """
        # TODO: Move this to the Hardware class.
        _hardware_id = model.get_value(row, 1)
        _hardware_model = self._mdcRTK.dtcHardwareBoM.dicHardware[_hardware_id]

        _ref_des = model.get_value(row, 27)

        # If the currently selected row has no parent, the composite reference
        # designator is the same as the reference designator.  Otherwise, build
        # the composite reference designator by appending the current row's
        # reference designator to the parent's composite reference designator.
        if not model.iter_parent(row):
            _comp_ref_des = _ref_des
        else:
            _p_row = model.iter_parent(row)
            _p_comp_ref_des = model.get_value(_p_row, 5)
            _comp_ref_des = _p_comp_ref_des + ":" + _ref_des

        model.set_value(row, 5, _comp_ref_des)
        _hardware_model.comp_ref_des = _comp_ref_des

        return False
