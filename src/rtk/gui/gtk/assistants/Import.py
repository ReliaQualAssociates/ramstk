    #!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.assistants.Import.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007, 2018 Doyle "weibullguy" Rowland
"""Import Assistant Module."""

# Import other RAMSTK modules.
from rtk import Utilities
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _, gobject, gtk, set_cursor

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007, 2018 Doyle "weibullguy" Rowland'


class RAMSTKImport(gtk.Assistant):
    """Assistant to walk user through the process of importing records."""

    def __init__(self, __widget, controller):
        """
        Initialize an instance of the Import Assistant.

        :param __widget: the gtk.Widget() that called this class.
        :type __widget: :class:`gtk.Widget`
        :param controller: the RAMSTK master data controller.
        :type controller: :class:`rtk.RAMSTK.RAMSTK`
        """
        gtk.Assistant.__init__(self)

        # Initialize private dict variables.
        self._dic_icons = {
            'error':
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/error.png',
            'information':
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/information.png',
        }

        # Initialize private list variables.

        # Initialize private scalar variables.
        self._mdcRAMSTK = controller
        self._dtc_data_controller = self._mdcRAMSTK.dic_controllers['imports']
        self._cmb_select_module = rtk.RAMSTKComboBox(
            tooltip=_(u"Select the RAMSTK module to map."))
        self._module = None

        # Initialize public dict variables.

        # Initialize public list variables.

        # Initialize public scalar variables.
        self._tvw_field_map = gtk.TreeView()

        # Build the assistant.
        _page = self._make_introduction_page()
        self.append_page(_page)
        self.set_page_type(_page, gtk.ASSISTANT_PAGE_INTRO)
        self.set_page_title(_page, _(u"RAMSTK Import Assistant"))
        self.set_page_complete(_page, True)
        _page = self._make_input_file_select_page()
        self.append_page(_page)
        self.set_page_type(_page, gtk.ASSISTANT_PAGE_CONTENT)
        self.set_page_title(_page, _(u"Select Input File"))
        _page = self._make_map_field_page()
        self.append_page(_page)
        self.set_page_type(_page, gtk.ASSISTANT_PAGE_CONTENT)
        self.set_page_title(
            _page, _(u"Map Input File Fields to RAMSTK Database Fields"))
        _page = self._make_confirm_page()
        self.append_page(_page)
        self.set_page_type(_page, gtk.ASSISTANT_PAGE_CONFIRM)
        self.set_page_complete(_page, True)

        self.set_property('title', _(u"RAMSTK Import Assistant"))

        self.resize(800, 400)
        self.move(200, 100)

        self.connect('cancel', self._do_quit)
        self.connect('close', self._do_quit)
        self.connect('apply', self._do_request_insert)

        self.show_all()

    def _do_edit_cell(self, __cell, path, new_text, model):
        """
        Handle gtk.CellRenderer() edits.

        :param gtk.CellRenderer cell: the gtk.CellRenderer() that was edited.
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer() that
                         was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param gtk.TreeModel model: the gtk.TreeModel() the gtk.CellRenderer()
                                    belongs to.
        :return: None
        :rtype: None
        """
        _page = self.get_nth_page(2)

        _db_field = model[path][0]
        model[path][1] = new_text

        self._dtc_data_controller.request_do_map_to_field(
            self._module, new_text, _db_field)

        self.set_page_complete(_page, True)

        return None

    def _do_quit(self, __widget):
        """
        Quit the RAMSTK Import Assistant.

        :param __widget: the gtk.Widget() that called this method.
        :type __widget: :class:`gtk.Widget`
        :return: None
        :rtype: None
        """
        self.destroy()

        return None

    def _do_request_insert(self, __assistant):
        """
        Request the data controller insert new records.

        :param __assistant: this gtk.Assistant() instance.
        :type __assistant: :class:`gtk.Assistant`
        :return: None
        :rtype: None
        """
        set_cursor(self._mdcRAMSTK, gtk.gdk.WATCH)

        (_count, _error_code,
         _msg) = self._dtc_data_controller.request_do_insert(self._module)

        set_cursor(self._mdcRAMSTK, gtk.gdk.LEFT_PTR)

        if _error_code == 2:
            _msg_type = 'error'
            _user_msg = _(u"A RAMSTK Program database must be connected to "
                          u"import the data into from an external file.  "
                          u"Please create or open a RAMSTK Program database "
                          u"and try again.")
        elif _error_code == 3:
            _msg_type = 'error'
            _user_msg = _(u"One or more import records violated PRIMARY KEY "
                          u"constraints.  Check your import file data and try "
                          u"again.")
        elif _error_code == 4:
            _msg_type = 'error'
            _user_msg = _(
                u"One or more import records contains a field with "
                u"a value that is incompatible with the required "
                u"data type for the RAMSTK Program database field it "
                u"was mapped to.")
        else:
            _msg_type = 'information'
            _user_msg = _(u"Successfully imported {0:d} {1:s} "
                          u"records.").format(_count, self._module)

        _dialog = rtk.RAMSTKMessageDialog(
            _user_msg, self._dic_icons[_msg_type], _msg_type)
        if _dialog.do_run() == gtk.RESPONSE_OK:
            _dialog.destroy()

        return None

    def _do_select_file(self, filechooser):
        """
        Select the input file to be read.

        :param filechooser: the gtk.FileChooser() that called this method.
        :type filechooser: :class:`gtk.FileChooser`
        :return: None
        :rtype: None
        """
        _page = self.get_nth_page(1)

        _file_type = filechooser.get_filter().get_name()
        if _file_type == 'Delimited Text Files':
            _file_type = 'csv'
        elif _file_type == 'Excel Files':
            _file_type = 'excel'
        _file = filechooser.get_filename()
        print _file
        if _file is not None:
            self._dtc_data_controller.request_do_read_input(
                _file_type, _file)

        # Load the field map treeview.
        self._module = self._cmb_select_module.get_active_text()

        _model = self._tvw_field_map.get_model()
        _model.clear()

        _cell = self._tvw_field_map.get_column(1).get_cell_renderers()[0]
        _cellmodel = _cell.get_property('model')
        _cellmodel.clear()
        _cellmodel.append([''])
        (_db_fields,
         _file_fields) = self._dtc_data_controller.request_get_db_fields(
             self._module)
        for __, _field in enumerate(_file_fields):
            _cellmodel.append([_field])
        for _field in _db_fields:
            _model.append(None, [_field, ''])

        self.set_page_complete(_page, True)

        return None

    @staticmethod
    def _make_introduction_page():
        """
        Make the Import Assistant introduction page.

        :return: _page
        :rtype: :class:`gtk.Fixed`
        """
        _page = gtk.Fixed()

        _label = rtk.RAMSTKLabel(
            _(u"This is the RAMSTK Import Assistant.  It "
              u"will guide you through the process of "
              u"importing RAMSTK Program module data from "
              u"an external file.  Press 'Forward' to continue "
              u"or 'Cancel' to quit."),
            height=300,
            width=-1,
            wrap=True)
        _label.set_alignment(0.05, 0.05)

        _page.put(_label, 25, 5)

        return _page

    def _make_input_file_select_page(self):
        """
        Make the Import Assistant page to select the input file.

        :return: _page
        :rtype: :class:`gtk.ScrolledWindow`
        """
        # TODO: Implement NSWC (add Design Mechanic to this list).
        self._cmb_select_module.do_load_combo(
            [[_(u"Function")], [_(u"Requirement")], [_(u"Hardware")],
             [_(u"Validation")]])

        _page = gtk.HBox()

        _fixed = gtk.Fixed()
        _label = rtk.RAMSTKLabel(_(u"Select the RAMSTK module to import:"))
        _fixed.put(_label, 5, 5)
        _fixed.put(self._cmb_select_module, 55, 5)
        _page.pack_start(_fixed, False, False)

        _scrollwindow = gtk.ScrolledWindow()
        _file_chooser = gtk.FileChooserWidget(
            action=gtk.FILE_CHOOSER_ACTION_OPEN)
        _scrollwindow.add_with_viewport(_file_chooser)
        _page.pack_end(_scrollwindow, True, True)

        _file_filter = gtk.FileFilter()
        _file_filter.set_name(_(u"Delimited Text Files"))
        _file_filter.add_pattern('*.csv')
        _file_filter.add_pattern('*.txt')
        _file_chooser.add_filter(_file_filter)
        _file_filter = gtk.FileFilter()
        _file_filter.set_name(_(u"Excel Files"))
        _file_filter.add_pattern('*.xls*')
        _file_chooser.add_filter(_file_filter)

        _file_chooser.connect('selection_changed', self._do_select_file)

        return _page

    def _make_map_field_page(self):
        """
        Make the Import Assistant page to map fields.

        This method allows the user to map input file fields to RAMSTK
        database table fields.

        :return: _page
        :rtype: :class:`gtk.ScrolledWindow`
        """
        _page = gtk.ScrolledWindow()
        _page.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _page.add(self._tvw_field_map)

        _model = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_STRING)

        _column = gtk.TreeViewColumn()
        _label = rtk.RAMSTKLabel(
            _(u"Import File Column"), justify=gtk.JUSTIFY_CENTER)
        _column.set_widget(_label)

        _cell = gtk.CellRendererText()
        _cell.set_property('foreground', '#000000')
        _cell.set_property('cell-background', 'light gray')
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=0)
        _column.set_visible(True)
        self._tvw_field_map.append_column(_column)

        _column = gtk.TreeViewColumn()
        _label = rtk.RAMSTKLabel(
            _(u"RAMSTK Field"), justify=gtk.JUSTIFY_CENTER)
        _column.set_widget(_label)

        _cell = gtk.CellRendererCombo()
        _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
        _cellmodel.append([""])
        _cell.set_property('editable', True)
        _cell.set_property('foreground', '#000000')
        _cell.set_property('has-entry', False)
        _cell.set_property('model', _cellmodel)
        _cell.set_property('text-column', 0)
        _cell.connect('edited', self._do_edit_cell, _model)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=1)
        _column.set_visible(True)
        self._tvw_field_map.append_column(_column)

        self._tvw_field_map.set_model(_model)

        return _page

    @staticmethod
    def _make_confirm_page():
        """
        Make the Import Assistant confimation page.

        :return: _page
        :rtype: :class:`gtk.Fixed`
        """
        _page = gtk.Fixed()

        _label = rtk.RAMSTKLabel(
            _(u"RAMSTK is all set and ready to import your "
              u"data.  Press 'Apply' to import or 'Cancel' "
              u"to abort the import."),
            height=300,
            width=-1,
            wrap=True)
        _label.set_alignment(0.05, 0.05)

        _page.put(_label, 25, 5)

        return _page
