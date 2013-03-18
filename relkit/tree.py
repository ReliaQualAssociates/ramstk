#!/usr/bin/env python
""" This is the System Tree window for RelKit. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       tree.py is part of The RelKit Project
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

# Add localization support.
import locale
import gettext
_ = gettext.gettext

# Import other RelKit modules.
import calculations as _calc
import configuration as _conf
import imports as _impt
import utilities as _util


class TreeWindow(gtk.Window):
    """
    This class is the window containing the various gtk.Treeviews.
    """

    #TODO: Create GUI to set/edit user-defined column headings for all trees.

    def __init__(self, application):
        """
        Initializes the TreeBook Object.

        Keyword Arguments:
        application -- the RelKit application.
        """

        self._app = application

        self.n_units = 0

        # Create a new window and set its properties.
        gtk.Window.__init__(self)
        self.set_resizable(True)
        self.set_title(_("RelKit"))

        n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        width = gtk.gdk.screen_width() / n_screens
        height = gtk.gdk.screen_height()

        self.set_default_size((2 * width / 3) - 10, (2 * height / 7))
        self.set_border_width(5)
        self.set_position(gtk.WIN_POS_NONE)
        self.move(0, 0)

        self.connect('delete_event', self.delete_event)

        vbox = gtk.VBox()

        self.menubar = self._menu_create()
        vbox.pack_start(self.menubar, expand=False, fill=False)

        self.toolbar = self._toolbar_create()
        vbox.pack_start(self.toolbar, expand=False, fill=False)

        # Find the user's preferred gtk.Notebook tab position.
        if(_conf.TABPOS[0] == 'left'):
            _position = gtk.POS_LEFT
        elif(_conf.TABPOS[0] == 'right'):
            _position = gtk.POS_RIGHT
        elif(_conf.TABPOS[0] == 'top'):
            _position = gtk.POS_TOP
        else:
            _position = gtk.POS_BOTTOM

        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(_position)
        self.notebook.connect('switch-page', self._notebook_page_switched)

        self.scwRevision = self._app.REVISION.create_tree()
        self.scwFunction = self._app.FUNCTION.create_tree()
        self.scwRequirement = self._app.REQUIREMENT.create_tree()
        self.scwHardware = self._app.HARDWARE.create_tree()
        self.scwSoftware = self._app.SOFTWARE.create_tree()
        # TODO: Implement Maintenance Policy tree.
        # This is just a placeholder for now.
        # self.scwMaintenance = self._app.MAINTENANCE.create_tree()
        # TODO: Implement Reliability Testing tree.
        # This is just a placeholder for now.
        #self.scwTesting = self._app.TESTING.create_tree()
        self.scwValidation = self._app.VALIDATION.create_tree()
        self.scwIncidents = self._app.INCIDENT.create_tree()
        # TODO: Implement Survival Data Set tree.
        # This is just a placeholder for now.
        self.scwDatasets = self._app.DATASET.create_tree()

        vbox.pack_start(self.notebook, expand=True, fill=True)

        self.statusbar = gtk.Statusbar()
        self.statusbar.push(1, _("Ready"))

        self.progressbar = gtk.ProgressBar(adjustment=None)
        self.progressbar.set_pulse_step(0.25)
        self.statusbar.add(self.progressbar)

        vbox.pack_start(self.statusbar, expand=False, fill=False)

        self.add(vbox)
        self.show_all()

        _title = _("RelKit Work Book")
        self._app.winWorkBook.set_title(_title)

        self.notebook.set_current_page(0)

    def load_trees(self, _app):
        """
        Method to load the trees needed depending on the analyses set as
        active for the project being opened.
        """

        if(_conf.RELIAFREE_MODULES[0] == 1):
            label = gtk.Label()
            _heading = _("Revisions")
            label.set_markup("<span weight='bold'>" + _heading + "</span>")
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.show_all()
            label.set_tooltip_text(_("Displays the program revisions."))
            self.notebook.insert_page(self.scwRevision, tab_label=label, position=-1)
            _app.REVISION.load_tree()

        if(_conf.RELIAFREE_MODULES[2] == 1):
            label = gtk.Label()
            _heading = _("Functions")
            label.set_markup("<span weight='bold'>" + _heading + "</span>")
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.show_all()
            label.set_tooltip_text(_("Displays the system functional hierarchy."))
            self.notebook.insert_page(self.scwFunction, tab_label=label, position=-1)
            _app.FUNCTION.load_tree()

        if(_conf.RELIAFREE_MODULES[1] == 1):
            label = gtk.Label()
            _heading = _("Requirements")
            label.set_markup("<span weight='bold'>" + _heading + "</span>")
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.show_all()
            label.set_tooltip_text(_("Displays the system requirement hierarchy."))
            self.notebook.insert_page(self.scwRequirement, tab_label=label, position=-1)
            _app.REQUIREMENT.load_tree()

        if(_conf.RELIAFREE_MODULES[3] == 1):
            label = gtk.Label()
            _heading = _("Hardware")
            label.set_markup("<span weight='bold'>" + _heading + "</span>")
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.show_all()
            label.set_tooltip_text(_("Displays the system hardware hierarchy."))
            self.notebook.insert_page(self.scwHardware, tab_label=label, position=-1)
            _app.HARDWARE.load_tree()

        if(_conf.RELIAFREE_MODULES[4] == 1):
            label = gtk.Label()
            _heading = _("Software")
            label.set_markup("<span weight='bold'>" + _heading + "</span>")
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.show_all()
            label.set_tooltip_text(_("Displays the system software hierarchy."))
            self.notebook.insert_page(self.scwSoftware, tab_label=label, position=-1)
            _app.SOFTWARE.load_tree()

        if(_conf.RELIAFREE_MODULES[5] == 1):
            label = gtk.Label()
            _heading = _("V &amp; V Tasks")
            label.set_markup("<span weight='bold'>" + _heading + "</span>")
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.show_all()
            label.set_tooltip_text(_("Displays the system verification and validation activities."))
            self.notebook.insert_page(self.scwValidation, tab_label=label, position=-1)

        if(_conf.RELIAFREE_MODULES[6] == 1):
            label = gtk.Label()
            _heading = _("Reliability\nTesting")
            label.set_markup("<span weight='bold'>" + _heading + "</span>")
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.show_all()
            label.set_tooltip_text(_("Displays the system reliability testing plans and results."))
            self.notebook.insert_page(self.scwRGIncidents, tab_label=label, position=-1)

        #if(_conf.RELIAFREE_MODULES[7] == 1):
            #label = gtk.Label(_("Maintenance Analysis"))
            #label.set_tooltip_text(_("Displays the system maintenance packages."))
            #self.notebook.insert_page(scrollwindow, tab_label=label, position=-1)

        if(_conf.RELIAFREE_MODULES[8] == 1):
            label = gtk.Label()
            _heading = _("Program\nIncidents")
            label.set_markup("<span weight='bold'>" + _heading + "</span>")
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.show_all()
            label.set_tooltip_text(_("Displays the system field incidents."))
            self.notebook.insert_page(self.scwIncidents, tab_label=label, position=-1)

            # Find the current revision if using the revision module, otherwise
            # set this to the default value.
            if(_conf.RELIAFREE_MODULES[0] == 1):
                values = (self._app.REVISION.revision_id,)
            else:
                values = (0, )

            # Select all the unaccepted field incidents from the open RelKit
            # Program database.
            if(_conf.BACKEND == 'mysql'):
                query = "SELECT * FROM tbl_incident \
                         WHERE fld_revision_id=%d \
                         ORDER BY fld_incident_id"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "SELECT * FROM tbl_incident \
                         WHERE fld_revision_id=? \
                         ORDER BY fld_incident_id"

            _app.INCIDENT.load_tree(query, values)

        # TODO: Add index to RELKIT_MODULES array for data sets.
        if(_conf.RELIAFREE_MODULES[8] == 1):
            label = gtk.Label()
            _heading = _("Survival\nAnalyses")
            label.set_markup("<span weight='bold'>" + _heading + "</span>")
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.show_all()
            label.set_tooltip_text(_("Displays the program survival data sets."))
            self.notebook.insert_page(self.scwDatasets, tab_label=label,
                                      position=-1)
            _app.DATASET.load_tree()

        #if(_conf.RELIAFREE_MODULES[9] == 1):
            # This determines whether the FMECA will be active for functions
            # and hardware.

        #if(_conf.RELIAFREE_MODULES[10] == 1):
            # This determines whether the Maintainability analysis will be
            # available for hardware.

        #if(_conf.RELIAFREE_MODULES[11] == 1):
            # This determines whether RBDs are active.

        #if(_conf.RELIAFREE_MODULES[12] == 1):
            # This determines whether FTAs are active.


        self.notebook.show_all()

        return False

    def _menu_create(self):
        """ Creates the menu for the TreeBook. """

        menu = gtk.Menu()

        menu2 = gtk.Menu()
        menu_item = gtk.MenuItem(label=_("_Project"), use_underline=True)
        menu_item.connect('activate', _util.create_project, self)
        menu2.append(menu_item)
        menu_item = gtk.MenuItem(label=_("_Revision"), use_underline=True)
        menu_item.connect('activate', self._app.REVISION.revision_add, self)
        menu2.append(menu_item)

        # Add assembly entry.
        menu_item = gtk.ImageMenuItem()
        image = gtk.Image()
        image.show()
        image.set_from_file(_conf.ICON_DIR + '16x16/assembly.png')
        menu_item.set_label(_("Assembly"))
        menu_item.set_image(image)
        menu_item.connect('activate', self._app.ASSEMBLY.assembly_add)
        menu2.append(menu_item)

        # Add component entry.
        menu_item = gtk.ImageMenuItem()
        image = gtk.Image()
        image.show()
        image.set_from_file(_conf.ICON_DIR + '16x16/part.png')
        menu_item.set_label(_("Component"))
        menu_item.set_image(image)
        menu_item.connect('activate', self._app.COMPONENT.component_add, None)
        menu2.append(menu_item)

        # Add New menu.
        mnuNew = gtk.ImageMenuItem()
        image = gtk.Image()
        image.show()
        image.set_from_file(_conf.ICON_DIR + '16x16/new.png')
        mnuNew.set_label(_("New"))
        mnuNew.set_image(image)

        mnuNew.set_submenu(menu2)
        menu.append(mnuNew)

        menu_item = gtk.ImageMenuItem()
        image = gtk.Image()
        image.show()
        image.set_from_file(_conf.ICON_DIR + '16x16/open.png')
        menu_item.set_label(_("Open"))
        menu_item.set_image(image)
        menu_item.connect('activate', _util.open_project, self._app)
        menu.append(menu_item)
        menu_item = gtk.ImageMenuItem()
        image = gtk.Image()
        image.show()
        image.set_from_file(_conf.ICON_DIR + '16x16/save.png')
        menu_item.set_label(_("Save"))
        menu_item.set_image(image)
        menu_item.connect('activate', _util.save_project, self._app)
        menu.append(menu_item)
        menu_item = gtk.MenuItem(label=_("Save _As"), use_underline=True)
        menu_item.connect('activate', _util.save_project, self._app)
        menu.append(menu_item)
        #menu_item = gtk.MenuItem(label=_("_Close"), use_underline=True)
        #menu_item.connect('activate', _util.close)
        #menu.append(menu_item)
        menu_item = gtk.ImageMenuItem()
        image = gtk.Image()
        image.show()
        image.set_from_file(_conf.ICON_DIR + '16x16/exit.png')
        menu_item.set_label(_("Exit"))
        menu_item.set_image(image)
        menu_item.connect('activate', self.quit_reliafree)
        menu.append(menu_item)

        mnuFile = gtk.MenuItem(label=_("_File"), use_underline=True)
        mnuFile.show()
        mnuFile.set_submenu(menu)

        menu = gtk.Menu()
        menu_item = gtk.ImageMenuItem()
        image = gtk.Image()
        image.show()
        image.set_from_file(_conf.ICON_DIR + '16x16/undo.png')
        menu_item.set_label(_("Undo"))
        menu_item.set_image(image)
        menu_item.connect('activate', _util.undo)
        menu.append(menu_item)
        menu_item = gtk.ImageMenuItem()
        image = gtk.Image()
        image.show()
        image.set_from_file(_conf.ICON_DIR + '16x16/redo.png')
        menu_item.set_label(_("Redo"))
        menu_item.set_image(image)
        menu_item.connect('activate', _util.redo)
        menu.append(menu_item)
        menu_item = gtk.ImageMenuItem()
        image = gtk.Image()
        image.show()
        image.set_from_file(_conf.ICON_DIR + '16x16/cut.png')
        menu_item.set_label(_("Cut"))
        menu_item.set_image(image)
        menu_item.connect('activate', _util.cut_copy_paste, 0)
        menu.append(menu_item)
        menu_item = gtk.ImageMenuItem()
        image = gtk.Image()
        image.show()
        image.set_from_file(_conf.ICON_DIR + '16x16/copy.png')
        menu_item.set_label(_("Copy"))
        menu_item.set_image(image)
        menu_item.connect('activate', _util.cut_copy_paste, 1)
        menu.append(menu_item)
        menu_item = gtk.ImageMenuItem()
        image = gtk.Image()
        image.show()
        image.set_from_file(_conf.ICON_DIR + '16x16/paste.png')
        menu_item.set_label(_("Paste"))
        menu_item.set_image(image)
        menu_item.connect('activate', _util.cut_copy_paste, 2)
        menu.append(menu_item)
        menu_item = gtk.MenuItem(label=_("Select _All"), use_underline=True)
        menu_item.connect('activate', _util.select_all)
        menu.append(menu_item)

        mnuEdit = gtk.MenuItem(label=_("_Edit"), use_underline=True)
        mnuEdit.show()
        mnuEdit.set_submenu(menu)

        menu = gtk.Menu()
        menu_item = gtk.MenuItem(label=_("_Find"), use_underline=True)
        menu_item.connect('activate', _util.find, 0)
        menu.append(menu_item)
        menu_item = gtk.MenuItem(label=_("Find _Next"), use_underline=True)
        menu_item.connect('activate', _util.find, 1)
        menu.append(menu_item)
        menu_item = gtk.MenuItem(label=_("Find _Previous"), use_underline=True)
        menu_item.connect('activate', _util.find, 2)
        menu.append(menu_item)
        menu_item = gtk.MenuItem(label=_("_Replace"), use_underline=True)
        menu_item.connect('activate', _util.find, 3)
        menu.append(menu_item)

        mnuSearch = gtk.MenuItem(label=_("_Search"), use_underline=True)
        mnuSearch.show()
        mnuSearch.set_submenu(menu)

        menu = gtk.Menu()
        menu_item = gtk.MenuItem(label=_("_Options"), use_underline=True)
        menu_item.connect('activate', _util.options, self._app)
        menu.append(menu_item)
        menu_item = gtk.MenuItem(label=_("_Composite Ref Des"), use_underline=True)
        menu_item.connect('activate', _util.create_comp_ref_des, self._app)
        menu.append(menu_item)
        menu_item = gtk.MenuItem(label=_("_Import Project"), use_underline=True)
        menu_item.connect('activate', _util.import_project, self._app)
        menu.append(menu_item)

        mnuTools = gtk.MenuItem(label=_("_Tools"), use_underline=True)
        mnuTools.show()
        mnuTools.set_submenu(menu)

        menubar = gtk.MenuBar()
        menubar.show()
        menubar.append(mnuFile)
        menubar.append(mnuEdit)
        menubar.append(mnuSearch)
        menubar.append(mnuTools)

        return menubar

    def _toolbar_create(self):
        """ Creates the toolbar for the TreeBook. """

        toolbar = gtk.Toolbar()

        _pos = 0
        # New file button.
        button = gtk.ToolButton(stock_id = gtk.STOCK_NEW)
        button.set_tooltip_text(_("Create a new RelKit Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/new.png')
        button.set_icon_widget(image)
        button.connect('clicked', _util.create_project, self._app)
        toolbar.insert(button, _pos)
        _pos += 1

        # Connect button
        button = gtk.ToolButton(stock_id = gtk.STOCK_OPEN)
        button.set_tooltip_text(_("Connect to an existing RelKit Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/open.png')
        button.set_icon_widget(image)
        button.connect('clicked', _util.open_project, self._app)
        toolbar.insert(button, _pos)
        _pos += 1

        # Save button
        button = gtk.ToolButton(stock_id = gtk.STOCK_SAVE)
        button.set_tooltip_text(_("Save the currently open RelKit Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        button.set_icon_widget(image)
        button.connect('clicked', _util.save_project, self._app)
        toolbar.insert(button, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

        # Import data button
        button = gtk.ToolButton(label=_("Import"))
        button.set_tooltip_text(_("Imports data to the currently open RelKit Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/import.png')
        button.set_icon_widget(image)
        button.connect('clicked', self._import_data)
        toolbar.insert(button, _pos)
        _pos += 1

        # Insert item button
        button = gtk.MenuToolButton(stock_id = gtk.STOCK_ADD)
        button.set_tooltip_text(_("Add an item to the current product structure."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        button.set_icon_widget(image)
        menu = gtk.Menu()
        menu_item = gtk.MenuItem(label=_("Revision"))
        menu_item.set_tooltip_text(_("Add a new revision."))
        menu_item.connect('activate', self._app.REVISION.revision_add)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_("Sibling Function"))
        menu_item.set_tooltip_text(_("Add a new function at the same level as the selected function."))
        menu_item.connect('activate', self._app.FUNCTION.function_add, 0)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_("Child Function"))
        menu_item.set_tooltip_text(_("Add a new function subordinate to the selected function."))
        menu_item.connect('activate', self._app.FUNCTION.function_add, 1)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_("Sibling Requirement"))
        menu_item.set_tooltip_text(_("Add a new requirement at the same level as the selected requirement."))
        menu_item.connect('activate', self._app.REQUIREMENT.requirement_add, 0)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_("Derived Requirement"))
        menu_item.set_tooltip_text(_("Add a new requirement subordinate to the selected requirement."))
        menu_item.connect('activate', self._app.REQUIREMENT.requirement_add, 1)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_("Sibling Assembly"))
        menu_item.set_tooltip_text(_("Add a new hardware assembly at the same level as the selected hardware assembly."))
        menu_item.connect('activate', self._app.ASSEMBLY.assembly_add, 0)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_("Child Assembly"))
        menu_item.set_tooltip_text(_("Add a new hardware assembly subordinate to the selected hardware assembly."))
        menu_item.connect('activate', self._app.ASSEMBLY.assembly_add, 1)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_("Component"))
        menu_item.set_tooltip_text(_("Add a new component to the selected hardware assembly."))
        menu_item.connect('activate', self._app.COMPONENT.component_add, None)
        menu.add(menu_item)
        #menu_item = gtk.MenuItem(label="Failure Cause")
        #menu_item.connect('activate', self._app.FMEA.add_cause)
        #menu.add(menu_item)
        #menu_item = gtk.MenuItem(label="Recommended Action")
        #menu_item.connect('activate', self._app.FMEA.add_action)
        #menu.add(menu_item)
        button.set_menu(menu)
        menu.show_all()
        toolbar.insert(button, _pos)
        _pos += 1

        # Delete item button
        button = gtk.MenuToolButton(stock_id = gtk.STOCK_DELETE)
        button.set_tooltip_text(_("Delete the currently selected item."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/delete.png')
        button.set_icon_widget(image)
        menu = gtk.Menu()
        menu_item = gtk.MenuItem(label=_("Project"))
        menu_item.set_tooltip_text(_("Delete the currently open RelKit project."))
        menu_item.connect('activate', _util.delete_project, self._app)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_("Revision"))
        menu_item.set_tooltip_text(_("Delete the currently selected revision."))
        menu_item.connect('activate', self._app.REVISION.revision_delete, None)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_("Function"))
        menu_item.set_tooltip_text(_("Delete the currently selected function."))
        menu_item.connect('activate', self._app.FUNCTION.function_delete)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_("Requirement"))
        menu_item.set_tooltip_text(_("Delete the currently selected requirement."))
        menu_item.connect('activate', self._app.REQUIREMENT.requirement_delete)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_("Assembly"))
        menu_item.set_tooltip_text(_("Delete the currently selected hardware assembly."))
        menu_item.connect('activate', self._app.ASSEMBLY.assembly_delete)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_("Component"))
        menu_item.set_tooltip_text(_("Delete the currently selected component."))
        menu_item.set_property("name", "tree")
        menu_item.connect('activate', self._app.COMPONENT.component_delete)
        menu.add(menu_item)
        button.set_menu(menu)
        menu.show_all()
        toolbar.insert(button, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

        # Cut button
        button = gtk.ToolButton(stock_id = gtk.STOCK_CUT)
        button.set_tooltip_text(_("Cut the currently selected item."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/cut.png')
        button.set_icon_widget(image)
        button.set_label(_("Cut"))
        button.connect('clicked', _util.cut_copy_paste, 0)
        button.show()
        toolbar.insert(button, _pos)
        _pos += 1

        # Copy button
        button = gtk.ToolButton(stock_id = gtk.STOCK_COPY)
        button.set_tooltip_text(_("Copy the currently selected item."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/copy.png')
        button.set_icon_widget(image)
        button.set_label(_("Copy"))
        button.connect('clicked', _util.cut_copy_paste, 1)
        button.show()
        toolbar.insert(button, _pos)
        _pos += 1

        # Paste button
        button = gtk.ToolButton(stock_id = gtk.STOCK_PASTE)
        button.set_tooltip_text(_("Paste the clipboard contents."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/paste.png')
        button.set_icon_widget(image)
        button.set_label(_("Paste"))
        button.connect('clicked', _util.cut_copy_paste, 2)
        button.show()
        toolbar.insert(button, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

        # Undo button
        button = gtk.ToolButton(stock_id = gtk.STOCK_UNDO)
        button.set_tooltip_text(_("Undo the last change."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/undo.png')
        button.set_icon_widget(image)
        button.set_label(_("Undo"))
        button.connect('clicked', _util.undo, self)
        button.show()
        toolbar.insert(button, _pos)
        _pos += 1

        # Redo button
        button = gtk.ToolButton(stock_id = gtk.STOCK_REDO)
        button.set_tooltip_text(_("Redo the last change."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/redo.png')
        button.set_icon_widget(image)
        button.set_label(_("Redo"))
        button.connect('clicked', _util.redo, self)
        button.show()
        toolbar.insert(button, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

        # Calculate button
        button = gtk.MenuToolButton(None, label = "Calculate")
        button.set_tooltip_text(_("Perform various calculations on the system."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        button.set_icon_widget(image)
        button.set_label(_("Calculate"))
        menu = gtk.Menu()
        menu_item = gtk.MenuItem(label=_("Project"))
        menu_item.set_tooltip_text(_("Calculate the currently open RelKit project."))
        menu_item.connect('activate', _calc.calculate_project, self._app, 0)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_("Revision"))
        menu_item.set_tooltip_text(_("Calculate the revisions only."))
        menu_item.connect('activate', _calc.calculate_project, self._app, 1)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_("Function"))
        menu_item.set_tooltip_text(_("Calculate the functions only."))
        menu_item.connect('activate', _calc.calculate_project, self._app, 2)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_("System"))
        menu_item.set_tooltip_text(_("Calculate the hardware assemblies only."))
        menu_item.connect('activate', _calc.calculate_project, self._app, 3)
        menu.add(menu_item)
        button.set_menu(menu)
        menu.show_all()
        button.show()
        toolbar.insert(button, _pos)
        _pos += 1

        # Graphs button
        # TODO: Functions to create charts and graphs.
        button = gtk.ToolButton(label=_("Charts & Graphs"))
        button.set_tooltip_text(_("Create charts and graphs"))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/charts.png')
        button.set_icon_widget(image)
        button.set_label(_("Graphs"))
        button.show()
        toolbar.insert(button, _pos)
        _pos += 1

        # Reports button
        # TODO: Functions to create reports.
        button = gtk.ToolButton(label=_("Reports"))
        button.set_tooltip_text(_("Create text reports"))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/reports.png')
        button.set_icon_widget(image)
        button.set_label(_("Reports"))
        button.show()
        toolbar.insert(button, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

        # Save and quit button
        button = gtk.ToolButton(label=_("Save & Quit"))
        button.set_tooltip_text(_("Save the currently open RelKit Program Database then quit"))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save-exit.png')
        button.set_icon_widget(image)
        button.show()
        button.connect('clicked', self.save_quit_reliafree)
        toolbar.insert(button, _pos)
        _pos += 1

        # Quit without saving button
        button = gtk.ToolButton(stock_id = gtk.STOCK_QUIT)
        button.set_tooltip_text(_("Quit without saving the currently open RelKit Program Database"))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/exit.png')
        button.set_icon_widget(image)
        button.show()
        button.connect('clicked', self.quit_reliafree)
        toolbar.insert(button, _pos)

        toolbar.show()

        return(toolbar)

    def _notebook_page_switched(self, notebook, page, page_num):
        """
        Called whenever the Tree Book notebook page is changed.

        Keyword Arguments:
        notebook -- the Tree Book notebook widget.
        page     -- the newly selected page widget.
        page_num -- the newly selected page number.
                    0 = Revision Tree
                    1 = Function Tree
                    2 = Requirements Tree
                    3 = Hardware Tree
                    4 = Software Tree
                    4 = Validation Tree
                    5 = Reliability Testing Tree
                    6 = Field Incident Tree
        """

        if(page_num == 0):
            try:
                self._app.REVISION.treeview.grab_focus()
                model = self._app.REVISION.model
                path = model.get_path(model.get_iter_root())
                column = self._app.REVISION.treeview.get_column(0)
                self._app.REVISION.treeview.row_activated(path, column)
            except TypeError:               # There are no revisions.
                pass
        elif(page_num == 1):
            try:
                self._app.FUNCTION.treeview.grab_focus()
                model = self._app.FUNCTION.model
                path = model.get_path(model.get_iter_root())
                column = self._app.FUNCTION.treeview.get_column(0)
                self._app.FUNCTION.treeview.row_activated(path, column)
            except TypeError:               # There are no functions.
                self._app.FUNCTION.load_notebook()
        elif(page_num == 2):
            try:
                self._app.REQUIREMENT.treeview.grab_focus()
                model = self._app.REQUIREMENT.model
                path = model.get_path(model.get_iter_root())
                column = self._app.REQUIREMENT.treeview.get_column(0)
                self._app.REQUIREMENT.treeview.row_activated(path, column)
            except TypeError:               # There are no requirements.
                self._app.REQUIREMENT.load_notebook()
        elif(page_num == 3):
            try:
                self._app.HARDWARE.treeview.grab_focus()
                model = self._app.HARDWARE.model
                path = model.get_path(model.get_iter_root())
                column = self._app.HARDWARE.treeview.get_column(0)
                self._app.HARDWARE.treeview.row_activated(path, column)
            except TypeError:               # There is no hardware.
                pass
        elif(page_num == 4):
            try:
                self._app.SOFTWARE.treeview.grab_focus()
                model = self._app.SOFTWARE.model
                self._app.winParts.tvwPartsList.set_model(None)
                path = model.get_path(model.get_iter_root())
                column = self._app.SOFTWARE.treeview.get_column(0)
                self._app.SOFTWARE.treeview.row_activated(path, column)
                self._app.SOFTWARE.load_notebook()
            except:                         # There are no software modules.
                pass
        elif(page_num == 5):
            try:
                self._app.VALIDATION.treeview.grab_focus()
                model = self._app.VALIDATION.model
                self._app.winParts.tvwPartsList.set_model(None)
                path = model.get_path(model.get_iter_root())
                column = self._app.VALIDATION.treeview.get_column(0)
                self._app.VALIDATION.treeview.row_activated(path, column)
            except:                         # There are no V&V tasks.
                pass
        elif(page_num == 6):
            try:
                self._app.INCIDENT.treeview.grab_focus()
                model = self._app.INCIDENT.model
                self._app.winParts.tvwPartsList.set_model(None)
                path = model.get_path(model.get_iter_root())
                column = self._app.INCIDENT.treeview.get_column(0)
                self._app.INCIDENT.treeview.row_activated(path, column)
            except:                         # There are no field incidents.
                self._app.INCIDENT.load_notebook()
        elif(page_num == 7):
            try:
                self._app.DATASET.treeview.grab_focus()
                model = self._app.DATASET.model
                #self._app.winParts.tvwPartsList.set_model(None)
                #path = model.get_path(model.get_iter_root())
                column = self._app.DATASET.treeview.get_column(0)
                self._app.DATASET.treeview.row_activated(path, column)
            except:                         # There are no datasets.
                self._app.DATASET.load_notebook()

        return False

    def _import_data(self, button):
        """
        Function to call the data import assistant.

        Keyword Arguments:
        button -- the toolbar button that called this function.
        """

        if(_conf.RELIAFREE_PROG_INFO[2] == ''):
            _util.application_error(_("There is no active RelKit Project.  You must open a Project before importing data."),
                                    _image_='warning')
            return True
        else:
            assistant = _impt.ImportAssistant(self._app)
            return False

    def delete_event(self, widget, event, data=None):
        """
        Used to quit the RelKit application when the X in the upper
        right corner is pressed.

        Keyword Arguments:
        winmain -- the RelKit application main window widget.
        event   -- the gdk event (GDK_DELETE in this case).
        data    -- any data to pass when exiting the application.
        """

        _util.save_project(widget, self)

        gtk.main_quit()

        return False

    def save_quit_reliafree(self, button):
        """
        Used to save, then quit the RelKit application.

        Keyword Arguments:
        button -- the toolbar button that was pressed.
        """

        _util.save_project(button, self._app)

        gtk.main_quit()

        return False

    def quit_reliafree(self, button):
        """
        Used to quit the RelKit application without saving the open
        database.

        Keyword Arguments:
        button -- the toolbar button that was pressed.
        """

        gtk.main_quit()

        return False
