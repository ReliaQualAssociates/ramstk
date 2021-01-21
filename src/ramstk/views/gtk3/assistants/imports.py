#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.assistants.imports.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle "weibullguy" Rowland
"""Import Assistant Module."""

# Standard Library Imports
import os
from typing import List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.views.gtk3 import GObject, Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKLabel


class ImportProject(Gtk.Assistant):
    """Assistant to walk user through the process of importing records."""

    RAMSTK_USER_CONFIGURATION = RAMSTKUserConfiguration()

    def __init__(self, __button: Gtk.ToolButton,
                 configuration: RAMSTKUserConfiguration, parent: object):
        """Initialize an instance of the Import Assistant.

        :param __button: the Gtk.ToolButton() that launched an instance of this
            class.
        :param configuration: the RAMSTKUserConfiguration class instance.
        :param parent: the parent window to associate this dialog with.
        """
        super().__init__()
        self.set_transient_for(parent)

        # Initialize private dict variables.

        # Initialize private list variables.

        # Initialize private scalar variables.
        self.cmbSelectModule: RAMSTKComboBox = RAMSTKComboBox()
        self._filechooser: Gtk.FileChooserButton = Gtk.FileChooserButton(
            action=Gtk.FileChooserAction.OPEN)
        self._module: str = ''
        self.tvwFieldMap: Gtk.TreeView = Gtk.TreeView()

        # Initialize public dict variables.

        # Initialize public list variables.

        # Initialize public scalar variables.
        self.RAMSTK_USER_CONFIGURATION = configuration

        self.__do_set_properties()
        self.__make_ui()
        self.__do_load_combobox()
        self.__do_set_callbacks()

        pub.subscribe(self._do_load_db_fields, 'succeed_read_db_fields')
        pub.subscribe(self._do_load_import_fields, 'succeed_read_import_file')

    def _do_edit_cell(self, __cell: Gtk.CellRenderer, path: str, new_text: str,
                      model: Gtk.TreeModel) -> None:
        """Handle Gtk.CellRenderer() edits.

        :param __cell: the Gtk.CellRenderer() that was edited.
        :param path: the Gtk.TreeView() path of the Gtk.CellRenderer() that
                         was edited.
        :param new_text: the new text in the edited Gtk.CellRenderer().
        :param model: the Gtk.TreeModel() the Gtk.CellRenderer() belongs to.
        :return: None
        :rtype: None
        """
        _page = self.get_nth_page(2)

        _db_field = model[path][0]
        model[path][1] = new_text

        pub.sendMessage('request_map_to_field',
                        module=self._module,
                        import_field=new_text,
                        format_field=_db_field)

        self.set_page_complete(_page, True)

    def _do_load_db_fields(self, db_fields: List[str]) -> None:
        """Load the Rosetta stone with the names of database fields.

        :param list db_fields: the list of database field names.
        :return: None
        :rtype: None
        """
        _model = self.tvwFieldMap.get_model()
        _model.clear()

        for _field in db_fields:
            _model.append(None, [_field, ''])

    def _do_load_import_fields(self, import_fields: List[str]) -> None:
        """Load the Rosetta stone with the import file field names.

        :param list import_fields: the list of field names found in the
            import file.
        :return: None
        :rtype: None
        """
        _cell = self.tvwFieldMap.get_column(1).get_cells()[0]
        _cellmodel = _cell.get_property('model')
        _cellmodel.clear()
        _cellmodel.append([''])

        # pylint: disable=unused-variable
        for __, _field in enumerate(import_fields):
            _cellmodel.append([_field])

    def _do_quit(self, __widget: Gtk.Widget) -> None:
        """Quit the RAMSTK Import Assistant.

        :param __widget: the Gtk.Widget() that called this method.
        :return: None
        :rtype: None
        """
        self.destroy()

    def _do_request_import(self, __assistant: Gtk.Assistant) -> None:
        """Request the data controller import new records.

        :param __assistant: this Gtk.Assistant() instance.
        :return: None
        :rtype: None
        """
        pub.sendMessage(
            'request_import',
            module=self._module,
        )

    def _do_select_file(self, filechooser: Gtk.FileChooser) -> None:
        """Select the input file to be read.

        :param filechooser: the Gtk.FileChooser() that called this method.
        :return: None
        :rtype: None
        """
        _file_type = ''
        _page = self.get_nth_page(1)

        _file = filechooser.get_filename()
        # pylint: disable=unused-variable
        __, _extension = os.path.splitext(_file)

        if _extension == '.csv':
            _file_type = 'csv'
        elif _extension == '.txt':
            _file_type = 'text'
        elif _extension in ['.xls', '.xlsx', '.xlsm']:
            _file_type = 'excel'

        if _file is not None:
            pub.sendMessage('request_read_import_file',
                            file_type=_file_type,
                            file_name=_file)

        self.set_page_complete(_page, True)

    def _on_combo_changed(self, combo: RAMSTKComboBox) -> None:
        """Respond to Gtk.ComboBox() 'changed' signals.

        :param Gtk.ComboBox combo: the Gtk.ComboBox() that called this method.
        :return: None
        :rtype: None
        """
        self._module = combo.get_value()

        pub.sendMessage(
            'request_db_fields',
            module=self._module,
        )

    def __do_load_combobox(self) -> None:
        """Load the RAMSTKComboBox() widgets.

        :return: None
        :rtype: None
        """
        self.cmbSelectModule.do_load_combo([[""], [_("Function")],
                                            [_("Requirement")],
                                            [_("Hardware")],
                                            [_("Validation")]])
        self.cmbSelectModule.set_active(1)

    def __do_set_callbacks(self) -> None:
        """Set the callback methods and functions.

        :return: None
        :rtype: None
        """
        self.connect('cancel', self._do_quit)
        self.connect('close', self._do_quit)
        self.connect('apply', self._do_request_import)

        # ----- COMBOBOX
        self.cmbSelectModule.dic_handler_id[
            'changed'] = self.cmbSelectModule.connect('changed',
                                                      self._on_combo_changed)

        # ----- FILECHOOSER
        self._filechooser.connect('selection_changed', self._do_select_file)

    def __do_set_properties(self) -> None:
        """Set the properties of the Import Assistant and widgets.

        :return: None
        :rtype: None
        """
        self.set_property('title', _("RAMSTK Import Assistant"))
        self.resize(800, 400)
        self.move(200, 100)

        # ----- FILECHOOSER
        _filefilter = Gtk.FileFilter()
        _filefilter.set_name(_("Delimited Text Files"))
        _filefilter.add_pattern('*.csv')
        _filefilter.add_pattern('*.txt')
        self._filechooser.add_filter(_filefilter)

        _filefilter = Gtk.FileFilter()
        _filefilter.set_name(_("Excel Files"))
        _filefilter.add_pattern('*.xls*')
        self._filechooser.add_filter(_filefilter)
        self._filechooser.set_current_folder(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_DIR)

    def __make_confirm_page(self):
        """Make the Import Assistant confirmation page.

        :return: _page
        :rtype: :class:`Gtk.Fixed`
        """
        _page: Gtk.Fixed = Gtk.Fixed()

        _label: RAMSTKLabel = RAMSTKLabel(
            _("RAMSTK is all set and ready to import your "
              "data.  Press 'Apply' to import or 'Cancel' "
              "to abort the import."))
        _label.do_set_properties(height=300, width=400, wrap=True)

        _page.put(_label, 25, 5)
        self.append_page(_page)
        self.set_page_type(_page, Gtk.AssistantPageType.CONFIRM)
        self.set_page_complete(_page, True)

    def __make_input_file_select_page(self) -> None:
        """Make the Import Assistant page to select the input file.

        :return: _page
        :rtype: :class:`Gtk.ScrolledWindow`
        """
        _page: Gtk.Fixed = Gtk.Fixed()

        _label = RAMSTKLabel(_("Select the RAMSTK module to import:"))
        _page.put(_label, 5, 5)
        _page.put(self.cmbSelectModule, _label.get_attribute('width') + 10, 5)

        _page.put(self._filechooser, _label.get_attribute('width') + 10, 65)

        self.append_page(_page)
        self.set_page_type(_page, Gtk.AssistantPageType.CONTENT)
        self.set_page_title(_page, _("Select Input File"))

    def __make_introduction_page(self) -> None:
        """Make the Import Assistant introduction page.

        :return: _page
        :rtype: :class:`Gtk.Fixed`
        """
        _page: Gtk.Fixed = Gtk.Fixed()

        _label = RAMSTKLabel(
            _("This is the RAMSTK Import Assistant.  It "
              "will guide you through the process of "
              "importing RAMSTK Program module data from "
              "an external file.  Press 'Forward' to continue "
              "or 'Cancel' to quit."))
        _label.do_set_properties(height=300, width=400, wrap=True)

        _page.put(_label, 25, 5)

        self.append_page(_page)
        self.set_page_type(_page, Gtk.AssistantPageType.INTRO)
        self.set_page_title(_page, _("RAMSTK Import Assistant"))
        self.set_page_complete(_page, True)

    def __make_map_field_page(self):
        """Make the Import Assistant page to map fields.

        This method allows the user to map input file fields to RAMSTK
        database table fields.

        :return: _page
        :rtype: :class:`Gtk.ScrolledWindow`
        """
        _page = Gtk.ScrolledWindow()
        _page.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        _page.add(self.tvwFieldMap)

        _model = Gtk.TreeStore(GObject.TYPE_STRING, GObject.TYPE_STRING)

        _column = Gtk.TreeViewColumn()
        _label = RAMSTKLabel(_("Import File Column"))
        _label.do_set_properties(justify=Gtk.Justification.CENTER)
        _column.set_widget(_label)

        _cell = Gtk.CellRendererText()
        _cell.set_property('foreground', '#000000')
        _cell.set_property('cell-background', 'light gray')
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=0)
        _column.set_visible(True)
        self.tvwFieldMap.append_column(_column)

        _column = Gtk.TreeViewColumn()
        _label = RAMSTKLabel(_("RAMSTK Field"))
        _label.do_set_properties(justify=Gtk.Justification.CENTER)
        _column.set_widget(_label)

        _cell = Gtk.CellRendererCombo()
        _cellmodel = Gtk.ListStore(GObject.TYPE_STRING)
        _cellmodel.append([""])
        _cell.set_property('editable', True)
        _cell.set_property('foreground', '#FFFFFF')
        _cell.set_property('has-entry', False)
        _cell.set_property('model', _cellmodel)
        _cell.set_property('text-column', 0)
        _cell.connect('edited', self._do_edit_cell, _model)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=1)
        _column.set_visible(True)
        self.tvwFieldMap.append_column(_column)

        self.tvwFieldMap.set_model(_model)

        self.append_page(_page)
        self.set_page_type(_page, Gtk.AssistantPageType.CONTENT)
        self.set_page_title(
            _page, _("Map Input File Fields to RAMSTK Database Fields"))

    def __make_ui(self):
        """Build the user interface.

        :return: None
        :rtype: None
        """
        # Build the assistant.
        self.__make_introduction_page()
        self.__make_input_file_select_page()
        self.__make_map_field_page()
        self.__make_confirm_page()

        self.show_all()
