# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.assistants.Preferences.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RAMSTK Configuration Preferences Module."""

from os.path import basename
import defusedxml.lxml as lxml

# Import other RAMSTK modules.
from rtk.dao import (RAMSTKCondition, RAMSTKGroup, RAMSTKLoadHistory,
                     RAMSTKMeasurement, RAMSTKRPN, RAMSTKUser)
from rtk.gui.gtk.rtk.Widget import _, gobject, gtk, pango
from rtk.gui.gtk import rtk

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007-2018 Andrew "weibullguy" Rowland'


class Preferences(gtk.Window, rtk.RAMSTKBaseView):
    """
    An assistant to provide a GUI to set various RAMSTK config preferences.

    RAMSTK preferences are stored in the RAMSTK Site database and the user's
    Site configuration file and Program configuration file.  Configurations
    preferences are stored in Site.conf or RAMSTK.conf in each user's
    $HOME/.config/RAMSTK directory and are applicable only to that specific
    user.  Configuration preferences are edited with the Preferences assistant.
    """

    def __init__(self, __widget, controller):
        """
        Initialize an instance of the Preferences assistant.

        :param gtk.Widget __widget: the gtk.Widget() that called this class.
        :param controller: the RAMSTK master data controller.
        :type controller: :class:`rtk.RAMSTK.RAMSTK`
        """
        gtk.Window.__init__(self)
        rtk.RAMSTKBaseView.__init__(self, controller, module='preferences')

        # Initialize private dictionary attributes.
        self._dic_icons['save-layout'] = (
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/save-layout.png')
        self._site_preferences = {}
        self._user_preferences = {}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtc_data_controller = self._mdcRAMSTK.dic_controllers[
            'preferences']
        self._fmt_file = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.notebook = gtk.Notebook()

        # Which modules are enabled for this RAMSTK program?
        self.chkFunctions = rtk.RAMSTKCheckButton(
            label=_(u"Function Module Active"),
            tooltip=_(
                u"Enables/disables the Function module for this program."))
        self.chkRequirements = rtk.RAMSTKCheckButton(
            label=_(u"Requirements Module Active"),
            tooltip=_(
                u"Enables/disables the Requirements module for this program."))
        self.chkHardware = rtk.RAMSTKCheckButton(
            label=_(u"Hardware Module Active"),
            tooltip=_(
                u"Enables/disables the Hardware module for this program."))
        self.chkValidation = rtk.RAMSTKCheckButton(
            label=_(u"Validation Module Active"),
            tooltip=_(
                u"Enables/disables the Validation module for this program."))
        self.chkFMEA = rtk.RAMSTKCheckButton(
            label=_(u"(D)FME(C)A Module Active"),
            tooltip=_(
                u"Enables/disables the (D)FME(C)A module for this program."))

        # What are the general user preferences?
        self.btnConfDir = gtk.FileChooserButton(
            _(u"RAMSTK Configuration File Directory"))
        self.btnDataDir = gtk.FileChooserButton(_(u"RAMSTK Data Directory"))
        self.btnIconDir = gtk.FileChooserButton(_(u"RAMSTK Icon Directory"))
        self.btnLogDir = gtk.FileChooserButton(_(u"RAMSTK Log Directory"))
        self.btnProgramDir = gtk.FileChooserButton(
            _(u"RAMSTK Program Directory"))

        self.cmbModuleBookTabPosition = rtk.RAMSTKComboBox(simple=True)
        self.cmbWorkBookTabPosition = rtk.RAMSTKComboBox(simple=True)
        self.cmbListBookTabPosition = rtk.RAMSTKComboBox(simple=True)
        self.cmbReportSize = rtk.RAMSTKComboBox(simple=True)

        self.txtFRMultiplier = rtk.RAMSTKEntry()
        self.txtDecimalPlaces = rtk.RAMSTKEntry(width=75)
        self.txtMissionTime = rtk.RAMSTKEntry(width=75)

        # What are the names and, optionally, paths to the format files and the
        # layout of each one?
        self.cmbFormatFiles = rtk.RAMSTKComboBox(
            tooltip=_(u"Select the Module View layout to edit."), simple=False)
        self.tvwFormatFile = gtk.TreeView()

        # What are the desired background and foreground colors for the
        # various RAMSTK rtk.TreeView()?
        self.btnRevisionBGColor = gtk.ColorButton()
        self.btnRevisionFGColor = gtk.ColorButton()
        self.btnFunctionBGColor = gtk.ColorButton()
        self.btnFunctionFGColor = gtk.ColorButton()
        self.btnRequirementsBGColor = gtk.ColorButton()
        self.btnRequirementsFGColor = gtk.ColorButton()
        self.btnHardwareBGColor = gtk.ColorButton()
        self.btnHardwareFGColor = gtk.ColorButton()
        self.btnSoftwareBGColor = gtk.ColorButton()
        self.btnSoftwareFGColor = gtk.ColorButton()
        self.btnValidationBGColor = gtk.ColorButton()
        self.btnValidationFGColor = gtk.ColorButton()
        self.btnIncidentBGColor = gtk.ColorButton()
        self.btnIncidentFGColor = gtk.ColorButton()
        self.btnTestingBGColor = gtk.ColorButton()
        self.btnTestingFGColor = gtk.ColorButton()

        # What RAMSTK global lists are available to edit?
        self.cmbLists = rtk.RAMSTKComboBox(
            tooltip=_(u"Select global RAMSTK list to edit."), simple=False)
        self.tvwListEditor = gtk.TreeView()

        _n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        _width = gtk.gdk.screen_width() / _n_screens
        _height = gtk.gdk.screen_height()

        self.set_default_size(_width - 450, (2 * _height / 7))
        self.set_resizable(True)
        self.set_border_width(5)
        self.set_position(gtk.WIN_POS_CENTER)

        self.btnConfDir.connect('file-set', self._do_select_path, 0)
        self.btnDataDir.connect('file-set', self._do_select_path, 1)
        self.btnIconDir.connect('file-set', self._do_select_path, 2)
        self.btnLogDir.connect('file-set', self._do_select_path, 3)
        self.btnProgramDir.connect('file-set', self._do_select_path, 4)

        self.btnRevisionBGColor.connect('color-set', self._do_set_color,
                                        'revisionbg')
        self.btnRevisionFGColor.connect('color-set', self._do_set_color,
                                        'revisionfg')
        self.btnFunctionBGColor.connect('color-set', self._do_set_color,
                                        'functionbg')
        self.btnFunctionFGColor.connect('color-set', self._do_set_color,
                                        'functionfg')
        self.btnRequirementsBGColor.connect('color-set', self._do_set_color,
                                            'requirementbg')
        self.btnRequirementsFGColor.connect('color-set', self._do_set_color,
                                            'requirementfg')
        self.btnHardwareBGColor.connect('color-set', self._do_set_color,
                                        'hardwarebg')
        self.btnHardwareFGColor.connect('color-set', self._do_set_color,
                                        'hardwarefg')
        self.btnSoftwareBGColor.connect('color-set', self._do_set_color,
                                        'softwarebg')
        self.btnSoftwareFGColor.connect('color-set', self._do_set_color,
                                        'softwarefg')
        self.btnValidationBGColor.connect('color-set', self._do_set_color,
                                          'validationbg')
        self.btnValidationFGColor.connect('color-set', self._do_set_color,
                                          'validationfg')
        self.btnIncidentBGColor.connect('color-set', self._do_set_color,
                                        'incidentbg')
        self.btnIncidentFGColor.connect('color-set', self._do_set_color,
                                        'incidentfg')
        self.btnTestingBGColor.connect('color-set', self._do_set_color,
                                       'testingbg')
        self.btnTestingFGColor.connect('color-set', self._do_set_color,
                                       'testingfg')

        self._lst_handler_id.append(
            self.cmbFormatFiles.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.cmbLists.connect('changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(
            self.cmbModuleBookTabPosition.connect('changed',
                                                  self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbWorkBookTabPosition.connect('changed',
                                                self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbListBookTabPosition.connect('changed',
                                                self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.cmbReportSize.connect('changed', self._on_combo_changed, 5))

        _buttonbox = rtk.RAMSTKBaseView._make_buttonbox(
            self,
            icons=[
                'cancel',
            ],
            tooltips=[
                _(u"Quit the RAMSTK preferences dialog without saving."),
            ],
            callbacks=[
                self._do_quit,
            ],
            orientation='horizontal',
            height=-1,
            width=-1)
        _buttonbox.set_layout(gtk.BUTTONBOX_END)

        _vbox = gtk.VBox()
        _vbox.pack_start(self.notebook, expand=True, fill=True)
        _vbox.pack_end(_buttonbox, expand=False, fill=False)

        self.add(_vbox)

        # if self._mdcRAMSTK.loaded:
        #    self._make_active_modules_page()
        self._make_general_preferences_page()
        self._make_look_and_feel_page()
        self._make_global_lists_page()

        self.show_all()

        self._do_load_page()

    @staticmethod
    def _do_edit_cell(__cell, path, new_text, position, model):
        """
        Handle gtk.CellRenderer() edits.

        :param __cell: the gtk.CellRenderer() that was edited.
        :type __cell: gtk.CellRenderer
        :param path: the gtk.TreeView() path of the gtk.CellRenderer() that was
                     edited.
        :type path: string
        :param new_text: the new text in the edited gtk.CellRenderer().
        :type new_text: string
        :param position: the column position of the edited gtk.CellRenderer().
        :type position: integer
        :param model: the gtk.TreeModel() the gtk.CellRenderer() belongs to.
        :type model: gtk.TreeModel
        """
        _type = gobject.type_name(model.get_column_type(position))

        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

        return False

    def _do_load_format(self, combo):
        """
        Load the selected Module View format file for editing.

        :return: None
        :rtype: None
        """
        _model = combo.get_model()
        _row = combo.get_active_iter()
        _module = _model.get_value(_row, 1)

        self._fmt_file = (
            self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_CONF_DIR + '/layouts/'
            + self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_FORMAT_FILE[_module])
        if _module == 'dfmeca':
            _fmt_path = "/root/tree[@name='DFMECA']/column"
        elif _module == 'ffmea':
            _fmt_path = "/root/tree[@name='FFMEA']/column"
        elif _module == 'hazops':
            _fmt_path = "/root/tree[@name='HazOps']/column"
        elif _module == 'pof':
            _fmt_path = "/root/tree[@name='PoF']/column"
        elif _module == 'similaritem':
            _fmt_path = "/root/tree[@name='SimilarItem']/column"
        else:
            _fmt_path = "/root/tree[@name='" + _module.title() + "']/column"

        # Retrieve the default heading text from the format file.
        _path = _fmt_path + '/defaulttitle'
        _default = lxml.parse(self._fmt_file).xpath(_path)

        # Retrieve the default heading text from the format file.
        _path = _fmt_path + '/usertitle'
        _user = lxml.parse(self._fmt_file).xpath(_path)

        # Retrieve the column position from the format file.
        _path = _fmt_path + '/position'
        _position = lxml.parse(self._fmt_file).xpath(_path)

        # Retrieve whether or not the column is editable from the format file.
        _path = _fmt_path + '/editable'
        _editable = lxml.parse(self._fmt_file).xpath(_path)

        # Retrieve whether or not the column is visible from the format file.
        _path = _fmt_path + '/visible'
        _visible = lxml.parse(self._fmt_file).xpath(_path)

        # Retrieve datatypes from the format file.
        _path = _fmt_path + '/datatype'
        _datatype = lxml.parse(self._fmt_file).xpath(_path)

        # Retrieve widget types from the format file.
        _path = _fmt_path + '/widget'
        _widget = lxml.parse(self._fmt_file).xpath(_path)

        # Retrieve attribute keys from the format file.
        _path = _fmt_path + '/key'
        _keys = lxml.parse(self._fmt_file).xpath(_path)

        _model = self.tvwFormatFile.get_model()
        _model.clear()
        for _index, __ in enumerate(_default):
            try:
                _key = _keys[_index]
            except IndexError:
                _key = ''
            _data = [
                _default[_index].text, _user[_index].text,
                int(_position[_index].text),
                int(_editable[_index].text),
                int(_visible[_index].text), _datatype[_index].text,
                _widget[_index].text, _key
            ]
            _model.append(_data)

        return None

    def _do_load_list(self, combo):
        """
        Load the selected global RAMSTK list for editing.

        :return: None
        :rtype: None
        """
        _dic_headers = {
            'damaging_conditions': [
                '',
                _(u"Condition Description"),
                '',
                '',
                '',
            ],
            'load_history': [
                '',
                _(u"History Description"),
                '',
                '',
                '',
            ],
            'measureable_parameters': [
                '',
                _(u"Parameter Code"),
                _(u"Parameter Description"),
                '',
                '',
            ],
            'rpn_detection': [
                '',
                _(u"Name"),
                _(u"Description"),
                _(u"Value"),
                '',
            ],
            'rpn_occurrence': [
                '',
                _(u"Name"),
                _(u"Description"),
                _(u"Value"),
                '',
            ],
            'rpn_severity': [
                '',
                _(u"Name"),
                _(u"Description"),
                _(u"Value"),
                '',
            ],
            'workgroups': [
                '',
                _(u"Description"),
                '',
                '',
                '',
            ],
            'users': [
                '',
                _(u"First Name"),
                _(u"Last Name"),
                _(u"User E-Mail"),
                _(u"User Phone"),
            ]
        }
        # Retrieve the name of the list to display; this name is the key for
        # the dict above.
        _model = combo.get_model()
        _row = combo.get_active_iter()
        _list = _model.get_value(_row, 1)
        try:
            _headers = _dic_headers[_list]
        except KeyError:
            _headers = ['', '', '', '', '']

        # Clear out any existing models and columns.
        i = 0
        for _column in self.tvwListEditor.get_columns():
            _label = rtk.RAMSTKLabel(
                _headers[i], width=-1, height=-1, justify=gtk.JUSTIFY_CENTER)
            _column.set_widget(_label)
            if _headers[i] == '':
                _column.set_visible(False)
            else:
                _column.set_visible(True)
            i += 1
        _model = self.tvwListEditor.get_model()
        _model.clear()

        i = 0
        _entities = self._site_preferences[_list]
        for _entity in _entities:
            if _list == 'users':
                _data = [
                    i,
                    _entity.get_attributes()['user_fname'],
                    _entity.get_attributes()['user_lname'],
                    _entity.get_attributes()['user_email'],
                    _entity.get_attributes()['user_phone']
                ]
            elif _list in ['rpn_detection', 'rpn_occurrence', 'rpn_severity']:
                _data = [
                    i,
                    _entity.get_attributes()[1],
                    _entity.get_attributes()[2],
                    _entity.get_attributes()[4], ''
                ]
            else:
                _data = [
                    i, _entity.get_attributes()['description'], '', '', ''
                ]
            _model.append(_data)
            i += 1

        return None

    def _do_load_page(self, **kwargs):  # pylint: disable=unused-argument
        """
        Load the current preference values.

        :return: (_error_code, _user_msg, _debug_msg); the error code, message
                 to be displayed to the user, and the message to be written to
                 the debug log.
        :rtype: (int, str, str)
        """
        _positions = {"bottom": 1, "left": 2, "right": 3, "top": 4}
        _papersize = {'a4': 1, 'letter': 2}

        self._site_preferences = self._dtc_data_controller.request_get_preferences(
            site=True, user=False)
        self._user_preferences = self._dtc_data_controller.request_get_preferences(
            site=False, user=True)

        # if self._mdcRAMSTK.loaded:
        # self.chkFunctions.set_active(_results[0][1])
        # self.chkRequirements.set_active(_results[0][2])
        # self.chkSoftware.set_active(_results[0][4])
        # self.chkValidation.set_active(_results[0][5])
        # self.chkRG.set_active(_results[0][6])
        # self.chkIncidents.set_active(_results[0][8])
        # self.chkSurvivalAnalysis.set_active(_results[0][10])

        self.cmbModuleBookTabPosition.set_active(
            _positions[self._user_preferences['tabpos']['modulebook'].lower()])
        self.cmbWorkBookTabPosition.set_active(
            _positions[self._user_preferences['tabpos']['workbook'].lower()])
        self.cmbListBookTabPosition.set_active(
            _positions[self._user_preferences['tabpos']['listbook'].lower()])
        self.cmbReportSize.set_active(
            _papersize[self._user_preferences['report_size'].lower()])

        self.txtFRMultiplier.set_text(self._user_preferences['hr_multiplier'])
        self.txtDecimalPlaces.set_text(self._user_preferences['decimal'])
        self.txtMissionTime.set_text(self._user_preferences['calcreltime'])

        self.btnConfDir.set_current_folder(self._user_preferences['sitedir'])
        self.btnDataDir.set_current_folder(self._user_preferences['datadir'])
        self.btnIconDir.set_current_folder(self._user_preferences['icondir'])
        self.btnLogDir.set_current_folder(self._user_preferences['logdir'])
        self.btnProgramDir.set_current_folder(
            self._user_preferences['progdir'])

        _color = gtk.gdk.color_parse(
            self._user_preferences['colors']['revisionbg'])
        self.btnRevisionBGColor.set_color(_color)
        _color = gtk.gdk.color_parse(
            self._user_preferences['colors']['revisionfg'])
        self.btnRevisionFGColor.set_color(_color)
        _color = gtk.gdk.color_parse(
            self._user_preferences['colors']['functionbg'])
        self.btnFunctionBGColor.set_color(_color)
        _color = gtk.gdk.color_parse(
            self._user_preferences['colors']['functionfg'])
        self.btnFunctionFGColor.set_color(_color)
        _color = gtk.gdk.color_parse(
            self._user_preferences['colors']['requirementbg'])
        self.btnRequirementsBGColor.set_color(_color)
        _color = gtk.gdk.color_parse(
            self._user_preferences['colors']['requirementfg'])
        self.btnRequirementsFGColor.set_color(_color)
        _color = gtk.gdk.color_parse(
            self._user_preferences['colors']['hardwarebg'])
        self.btnHardwareBGColor.set_color(_color)
        _color = gtk.gdk.color_parse(
            self._user_preferences['colors']['hardwarefg'])
        self.btnHardwareFGColor.set_color(_color)
        # self.btnSoftwareBGColor.set_color(_color)
        # self.btnSoftwareFGColor.set_color(_color)
        _color = gtk.gdk.color_parse(
            self._user_preferences['colors']['validationbg'])
        self.btnValidationBGColor.set_color(_color)
        _color = gtk.gdk.color_parse(
            self._user_preferences['colors']['validationfg'])
        self.btnValidationFGColor.set_color(_color)
        # self.btnIncidentBGColor.set_color(_color)
        # self.btnIncidentFGColor.set_color(_color)
        # self.btnTestingBGColor.set_color(_color)
        # self.btnTestingFGColor.set_color(_color)

        return None

    def _do_quit(self, __button):
        """
        Quit the preferences gtk.Assistant().

        :param __button: the gtk.Button() that called this method.
        :type __button: :class:`gtk.Button`
        :return: None
        :rtype: None
        """
        self.destroy()

        return False

    def _do_request_list_add(self, __button):
        """
        Add a new item to the global list.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton()`
        :return: None
        :rtype: None
        """
        _model = self.cmbLists.get_model()
        _row = self.cmbLists.get_active_iter()
        _list = _model.get_value(_row, 1)

        _id = len(self._site_preferences[_list])
        _data = [_id, '', '', '', '']

        _model = self.tvwListEditor.get_model()
        _model.append(_data)

        if _list == 'damaging_conditions':
            _entity = RAMSTKCondition()
            _entity.description = 'New Damaging Operating Condition'
            _entity.cond_type = 'operating'
        elif _list == 'load_history':
            _entity = RAMSTKLoadHistory()
            _entity.description = 'New Load History'
        elif _list == 'measureable_parameters':
            _entity = RAMSTKMeasurement()
            _entity.code = 'NMP'
            _entity.description = 'New Measureable Parameter'
            _entity.measurement_type = 'damage'
        elif _list == 'rpn_detection':
            _entity = RAMSTKRPN()
            _entity.name = 'New RPN Name'
            _entity.description = 'New RPN Description'
            _entity.rpn_type = 'detection'
        elif _list == 'rpn_occurrence':
            _entity = RAMSTKRPN()
            _entity.name = 'New RPN Name'
            _entity.description = 'New RPN Description'
            _entity.rpn_type = 'occurrence'
        elif _list == 'rpn_severity':
            _entity = RAMSTKRPN()
            _entity.name = 'New RPN Name'
            _entity.description = 'New RPN Description'
            _entity.rpn_type = 'severity'
        elif _list == 'workgroups':
            _entity = RAMSTKGroup()
            _entity.description = 'New RAMSTK Workgroup'
            _entity.group_type = 'workgroup'
        elif _list == 'users':
            _entity = RAMSTKUser()
            _entity.user_lname = 'New RAMSTK User Last Name'
            _entity.user_fname = 'New RAMSTK User First Name'
            _entity.user_email = 'new@ramstk.user'
            _entity.user_phane = '867.5309'

        self._site_preferences[_list].append(_entity)

        return None

    def _do_request_list_remove(self, __button):
        """
        Remove the seleced item from the global list.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton()`
        :return: None
        :rtype: None
        """
        _model = self.cmbLists.get_model()
        _row = self.cmbLists.get_active_iter()
        _list = _model.get_value(_row, 1)

        (_model, _row) = self.tvwListEditor.get_selection().get_selected()
        _id = _model.get_value(_row, 0)

        _record = self._site_preferences[_list].pop(_id)
        if self._dtc_data_controller.request_do_delete(_record):
            _prompt = _(u"There was an error removing an item from the {0:s} "
                        u"RAMSTK global list.").format(_list)
            _icon = self._dic_icons['error']
            _dialog = rtk.RAMSTKMessageDialog(
                _prompt, _icon, 'error', parent=self)

            if _dialog.run() == gtk.RESPONSE_OK:
                _dialog.destroy()
        else:
            self._do_load_list(self.cmbLists)

        return None

    def _do_request_update(self, button):
        """
        Request to update the user and program preferences.

        :param button: the gtk.Button() that called this method.
        :type button: :class:`gtk.Button`
        :return: None
        :rtype: None
        """
        from shutil import copyfile

        # Make a backup of the original configuration files.
        _conf_file = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_CONF_DIR + '/Site.conf'
        copyfile(_conf_file, _conf_file + '_bak')
        _conf_file = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_CONF_DIR + '/RAMSTK.conf'
        copyfile(_conf_file, _conf_file + '_bak')

        if button.get_property('name') == 'format':
            copyfile(self._fmt_file, self._fmt_file + '_bak')
            self._do_save_tree_layout()
        elif button.get_property('name') == 'globallists':
            self._dtc_data_controller.request_set_preferences(
                self._site_preferences, site=True, user=False)
        else:
            self._dtc_data_controller.request_set_preferences(
                self._user_preferences, site=False, user=True)

        if self._dtc_data_controller.request_do_update():
            _prompt = _(u"There was an error saving user and program "
                        u"preferences.")
            _icon = self._dic_icons['error']
            _dialog = rtk.RAMSTKMessageDialog(
                _prompt, _icon, 'error', parent=self)

            if _dialog.run() == gtk.RESPONSE_OK:
                _dialog.destroy()

        return None

    def _do_save_tree_layout(self):
        """
        Save the Module View rtk.RAMSTKTreeView() layout file.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Get the format file for the gtk.TreeView to be edited.  Strip the
        # last four (.xml) characters to variable _name.
        _basename = basename(self._fmt_file)
        _name = _basename[:-4]

        # Open the format file for writing.
        _file = open(self._fmt_file, 'w')

        # Create the new format file.
        _file.write("<!--\n")
        _file.write("-*- coding: utf-8 -*-\n\n")
        _file.write(
            "{0:s} is part of the RAMSTK Project\n\n".format(_basename))
        _file.write('Copyright 2011-2018 Doyle "weibullguy" Rowland '
                    '<doyle DOT rowland AT reliaqual DOT com>\n\n')
        _file.write("All rights reserved.-->\n\n")
        _file.write("<!-- This file contains information used by the RAMSTK "
                    "application to draw\n")
        _file.write("various widgets.  These values can be changed by the "
                    "user to personalize\n")
        _file.write("their experience. -->\n\n")

        _file.write("<root>\n")
        _file.write('<tree name="{0:s}">\n'.format(_name))

        _model = self.tvwFormatFile.get_model()
        _row = _model.get_iter_first()
        while _row is not None:
            _file.write("<column>\n")
            _file.write("<defaulttitle>{0:s}</defaulttitle>\n".format(
                _model.get_value(_row, 0)))
            _file.write("<usertitle>{0:s}</usertitle>\n".format(
                _model.get_value(_row, 1)))
            _file.write("<datatype>{0:s}</datatype>\n".format(
                _model.get_value(_row, 5)))
            _file.write("<position>{0:d}</position>\n".format(
                _model.get_value(_row, 2)))
            _file.write("<widget>{0:s}</widget>\n".format(
                _model.get_value(_row, 6)))
            _file.write("<editable>{0:d}</editable>\n".format(
                _model.get_value(_row, 3)))
            _file.write("<visible>{0:d}</visible>\n".format(
                _model.get_value(_row, 4)))
            _file.write("<key>{0:s}</key>\n".format(_model.get_value(_row, 7)))
            _file.write("</column>\n")

            _row = _model.iter_next(_row)

        _file.write("</tree>\n")
        _file.write("</root>")
        _file.close()

        return False

    def _do_select_path(self, button, index):
        """
        Select the path from the file chooser.

        :param button: the gtk.FileChooserButton() that called this method.
        :type button: :class:`gtk.FileChooserButton`
        :param int index: the index of the gtk.FileChooserButton() that called
                          this method.
        :return: None
        :rtyp: None
        """
        if index == 0:
            self._preferences['sitedir'] = button.get_current_folder()
        elif index == 1:
            self._preferences['datadir'] = button.get_current_folder()
        elif index == 2:
            self._preferences['icondir'] = button.get_current_folder()
        elif index == 3:
            self._preferences['logdir'] = button.get_current_folder()
        elif index == 4:
            self._preferences['progdir'] = button.get_current_folder()

        return None

    def _do_set_color(self, colorbutton, rtk_colors):
        """
        Set the selected color.

        :param gtk.ColorButton colorbutton: the gtk.ColorButton() that called
                                            this method.
        :param int rtk_colors: the position in the RAMSTK_COLORS global variable.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Retrieve the six digit hexidecimal version of the selected color.
        _color = colorbutton.get_color()
        try:
            _red = "{0:#0{1}}".format('%X' % int(_color.red / 255), 2)
        except ValueError:
            _red = '%X' % int(_color.red / 255)
        try:
            _green = "{0:#0{1}}".format('%X' % int(_color.green / 255), 2)
        except ValueError:
            _green = '%X' % int(_color.green / 255)
        try:
            _blue = "{0:#0{1}}".format('%X' % int(_color.blue / 255), 2)
        except ValueError:
            _blue = '%X' % int(_color.blue / 255)
        _color = '#%s%s%s' % (_red, _green, _blue)

        # Set the color variable.
        self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_COLORS[rtk_colors] = _color

        return False

    @staticmethod
    def _do_toggle_cell(cell, path, position, model):
        """
        Handle gtk.CellRendererToggle() edits.

        :param cell: the gtk.CellRenderer() that was edited.
        :param path: the gtk.TreeView() path of the gtk.CellRenderer() that
                     was edited.
        :param position: the column position of the edited gtk.CellRenderer().
        :param model: the gtk.TreeModel() the gtk.CellRenderer() belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        model[path][position] = not cell.get_active()

        return False

    def _make_active_modules_page(self):
        """
        Make the Option class gtk.Notebook() active modules page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _tooltips = [
            _(u"Save the active modules used in this RAMSTK "
              u"program."),
        ]
        _callbacks = [
            self._do_request_update,
        ]
        _icons = [
            'save',
        ]
        _buttonbox = rtk.RAMSTKBaseView._make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1)
        _button = _buttonbox.get_children()[0]
        _button.set_property('name', 'modules')

        _hbox = gtk.HBox()
        _fixed = gtk.Fixed()
        _hbox.pack_start(_buttonbox, False, True)
        _hbox.pack_end(_fixed, True, True)

        _fixed.put(self.chkFunctions, 5, 5)
        _fixed.put(self.chkRequirements, 5, 35)
        _fixed.put(self.chkHardware, 5, 65)
        _fixed.put(self.chkValidation, 5, 95)
        _fixed.put(self.chkFMEA, 5, 125)

        _label = rtk.RAMSTKLabel(
            _(u"Active RAMSTK Modules"), justify=gtk.JUSTIFY_CENTER)
        _label.set_tooltip_text(_(u"Select active RAMSTK modules."))
        self.notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return None

    def _make_general_preferences_page(self):
        """
        Make the Preferences class gtk.Notebook() general preferences page.

        :return: None
        :rtype: None
        """
        _tooltips = [
            _(u"Save the user's general preferences."),
        ]
        _callbacks = [
            self._do_request_update,
        ]
        _icons = [
            'save',
        ]
        _buttonbox = rtk.RAMSTKBaseView._make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1)
        _button = _buttonbox.get_children()[0]
        _button.set_property('name', 'general')

        _hbox = gtk.HBox()
        _fixed = gtk.Fixed()
        _hbox.pack_start(_buttonbox, False, True)
        _hbox.pack_end(_fixed, True, True)

        _positions = [["Bottom"], ["Left"], ["Right"], ["Top"]]
        self.cmbModuleBookTabPosition.do_load_combo(_positions)
        self.cmbWorkBookTabPosition.do_load_combo(_positions)
        self.cmbListBookTabPosition.do_load_combo(_positions)

        _sizes = [["A4"], ["Letter"]]
        self.cmbReportSize.do_load_combo(_sizes)

        _label = rtk.RAMSTKLabel(
            _(u"Module Book tab position:"),
            tooltip=_(u"Set the position of the RAMSTK Module Book tabs."),
            width=-1)
        _fixed.put(_label, 5, 5)
        _fixed.put(self.cmbModuleBookTabPosition, 310, 5)
        _label = rtk.RAMSTKLabel(
            _(u"Work Book tab position:"),
            tooltip=_(u"Set the position of the RAMSTK Work Book tabs."),
            width=-1)
        _fixed.put(_label, 5, 35)
        _fixed.put(self.cmbWorkBookTabPosition, 310, 35)
        _label = rtk.RAMSTKLabel(
            _(u"List Book tab position:"),
            tooltip=_(u"Set the position of the RAMSTK List Book tabs."),
            width=-1)
        _fixed.put(_label, 5, 65)
        _fixed.put(self.cmbListBookTabPosition, 310, 65)
        _label = rtk.RAMSTKLabel(
            _(u"Report size:"),
            tooltip=_(u"Set the default paper size of RAMSK reports."),
            width=-1)
        _fixed.put(_label, 5, 125)
        _fixed.put(self.cmbReportSize, 310, 125)
        _label = rtk.RAMSTKLabel(
            _(u"Failure rate multiplier:"),
            tooltip=_(u"Set the failure rate multiplier."),
            width=-1)
        _fixed.put(_label, 5, 155)
        _fixed.put(self.txtFRMultiplier, 310, 155)
        _label = rtk.RAMSTKLabel(
            _(u"Decimal places:"),
            tooltip=_(u"Set the default number of decimal places displayed "
                      u"in RAMSTK."),
            width=-1)
        _fixed.put(_label, 5, 185)
        _fixed.put(self.txtDecimalPlaces, 310, 185)
        _label = rtk.RAMSTKLabel(
            _(u"Reliability estimation time:"),
            tooltip=_(u"Set the time at which reliabilities are calculated."),
            width=-1)
        _fixed.put(_label, 5, 215)
        _fixed.put(self.txtMissionTime, 310, 215)
        _label = rtk.RAMSTKLabel(
            _(u"Path to RAMSTK configuration files:"),
            tooltip=_(u"Set the path to the directory where RAMSTK looks for "
                      u"configuration files."),
            width=-1)
        _fixed.put(_label, 5, 245)
        _fixed.put(self.btnConfDir, 310, 245)
        _label = rtk.RAMSTKLabel(
            _(u"Path to RAMSTK data files:"),
            tooltip=_(u"Set the path to the directory where RAMSTK looks for "
                      u"data files (e.g., layout formats, icons, etc.)."),
            width=-1)
        _fixed.put(_label, 5, 275)
        _fixed.put(self.btnDataDir, 310, 275)
        _label = rtk.RAMSTKLabel(
            _(u"Path to RAMSTK log files:"),
            tooltip=_(u"Set the path to the directory where RAMSTK writes "
                      u"log files."),
            width=-1)
        _fixed.put(_label, 5, 305)
        _fixed.put(self.btnLogDir, 310, 305)
        _label = rtk.RAMSTKLabel(
            _(u"Path to RAMSTK analyses:"),
            tooltip=_(u"Set the path to the directory where RAMSTK stores "
                      u"analyses databases."),
            width=-1)
        _fixed.put(_label, 5, 335)
        _fixed.put(self.btnProgramDir, 310, 335)

        self.btnConfDir.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        self.btnDataDir.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        self.btnIconDir.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        self.btnLogDir.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        self.btnProgramDir.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)

        _label = rtk.RAMSTKLabel(
            _(u"General\nPreferences"), height=-1, justify=gtk.JUSTIFY_CENTER)
        _label.set_tooltip_text(
            _(u"Allows setting general user preferences for RAMSTK."))
        self.notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return None

    def _make_global_lists_page(self):
        """
        Make the page used to edit global RAMSTK lists.

        :return: None
        :rtype: None
        """
        _tooltips = [
            _(u"Add an entry to the currently selected global list."),
            _(u"Remove the currently selected item from the global list."),
            _(u"Save the RAMSTK global lists."),
        ]
        _callbacks = [
            self._do_request_list_add, self._do_request_list_remove,
            self._do_request_update
        ]
        _icons = [
            'add',
            'remove',
            'save',
        ]
        _buttonbox = rtk.RAMSTKBaseView._make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1)
        _button = _buttonbox.get_children()[0]
        _button.set_property('name', 'globallists')

        _hbox = gtk.HBox()
        _vbox = gtk.VBox()
        _frame = rtk.RAMSTKFrame(_(u"Edit RAMSTK Lists"))
        _frame.add(_vbox)
        _fixed = gtk.Fixed()
        _scrollwindow = gtk.ScrolledWindow()
        _hbox.pack_start(_buttonbox, False, True)
        _hbox.pack_end(_frame, True, True)
        _vbox.pack_start(_fixed, False, True)
        _vbox.pack_end(_scrollwindow, True, True)

        _label = rtk.RAMSTKLabel(_(u"Select RAMSTK list to load:"), width=-1)
        _fixed.put(_label, 5, 5)
        _fixed.put(self.cmbLists, 225, 5)
        _scrollwindow.add(self.tvwListEditor)

        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING)
        for _idx in [0, 1, 2, 3]:
            _cell = gtk.CellRendererText()
            _cell.set_property('cell-background', '#FFFFFF')
            _cell.set_property('editable', True)
            _cell.set_property('foreground', '#000000')
            _cell.set_property('wrap-width', 250)
            _cell.set_property('wrap-mode', pango.WRAP_WORD)
            _cell.set_property('yalign', 0.1)
            _cell.connect('edited', self._do_edit_cell, _idx, _model)
            _column = gtk.TreeViewColumn("")
            _column.set_alignment(0.5)
            _column.set_visible(True)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=_idx)
            self.tvwListEditor.append_column(_column)
        self.tvwListEditor.set_model(_model)

        _lists = [[
            _(u"Damaging Operating Conditions"), 'damaging_conditions', ''
        ], [_(u"Means for Classifying Load Histories"), 'load_history',
            ''], [_(u"Measureable Parameters"), 'measureable_parameters',
                  ''], [_(u"RPN Detection"), 'rpn_detection',
                        ''], [_(u"RPN Occurrence"), 'rpn_occurrence',
                              ''], [_(u"RPN Severity"), 'rpn_severity', ''],
                  [_(u"RAMSTK Work Groups"), 'workgroups',
                   ''], [_(u"RAMSTK Users"), 'users', '']]
        self.cmbLists.do_load_combo(_lists, simple=False)

        _label = rtk.RAMSTKLabel(
            _(u"Global RAMSTK Lists"), justify=gtk.JUSTIFY_CENTER)
        _label.set_tooltip_text(
            _(u"Edit global RAMSTK lists; lists available "
              u"to all RAMSTK Programs."))
        self.notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return None

    def _make_look_and_feel_page(self):
        """
        Make the Preferences class gtk.Notebook() look and feel page.

        :return: None
        :rtype: None
        """
        _tooltips = [
            _(u"Save the layout format."),
            _(u"Save the look &amp; feel preferences."),
        ]
        _callbacks = [
            self._do_request_update,
            self._do_request_update,
        ]
        _icons = [
            'save-layout',
            'save',
        ]
        _buttonbox = rtk.RAMSTKBaseView._make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1)
        _button = _buttonbox.get_children()[0]
        _button.set_property('name', 'format')
        _button = _buttonbox.get_children()[1]
        _button.set_property('name', 'looknfeel')

        _hbox_outer = gtk.HBox()
        _hbox_inner = gtk.HBox()
        _frame = rtk.RAMSTKFrame(
            label=_(u"Edit Module View Layout and Colors"))
        _frame.add(_hbox_inner)
        _fixed = gtk.Fixed()
        _scrollwindow = gtk.ScrolledWindow()
        _hbox_outer.pack_start(_buttonbox, False, True)
        _hbox_outer.pack_end(_frame, True, True)
        _hbox_inner.pack_start(_fixed, False, True)
        _hbox_inner.pack_end(_scrollwindow, True, True)

        _formats = [[_(u"Allocation"), 'allocation',
                     ''], [_("(D)FME(C)A"), 'dfmeca',
                           ''], [_(u"Functional FMEA"), 'ffmea',
                                 ''], [_(u"Function"), 'function',
                                       ''], [_(u"Hardware"), 'hardware',
                                             ''], [_(u"HazOps"), 'hazops', ''],
                    [_(u"Physics of Failure Analysis"), 'pof',
                     ''], [_(u"Requirement"), 'requirement',
                           ''], [_(u"Revision"), 'revision', ''],
                    [_(u"Similar Item Analysis"), 'similaritem',
                     ''], [_(u"Stakeholder Input"), 'stakeholder',
                           ''], [_(u"Validation"), 'validation', '']]
        self.cmbFormatFiles.do_load_combo(_formats, 0, False)

        _label = rtk.RAMSTKLabel(_(u"Select format file to edit:"), width=350)
        _fixed.put(_label, 5, 5)
        _fixed.put(self.cmbFormatFiles, 310, 5)
        _label = rtk.RAMSTKLabel(
            _(u"Revision Tree Background Color:"), width=350)
        _fixed.put(_label, 5, 95)
        _fixed.put(self.btnRevisionBGColor, 340, 95)
        _label = rtk.RAMSTKLabel(
            _(u"Revision Tree Foreground Color:"), width=350)
        _fixed.put(_label, 5, 125)
        _fixed.put(self.btnRevisionFGColor, 340, 125)
        _label = rtk.RAMSTKLabel(
            _(u"Function Tree Background Color:"), width=350)
        _fixed.put(_label, 5, 155)
        _fixed.put(self.btnFunctionBGColor, 340, 155)
        _label = rtk.RAMSTKLabel(
            _(u"Function Tree Foreground Color:"), width=350)
        _fixed.put(_label, 5, 185)
        _fixed.put(self.btnFunctionFGColor, 340, 185)
        _label = rtk.RAMSTKLabel(
            _(u"Requirements Tree Background Color:"), width=350)
        _fixed.put(_label, 5, 215)
        _fixed.put(self.btnRequirementsBGColor, 340, 215)
        _label = rtk.RAMSTKLabel(
            _(u"Requirements Tree Foreground Color:"), width=350)
        _fixed.put(_label, 5, 245)
        _fixed.put(self.btnRequirementsFGColor, 340, 245)
        _label = rtk.RAMSTKLabel(
            _(u"Hardware Tree Background Color:"), width=350)
        _fixed.put(_label, 5, 275)
        _fixed.put(self.btnHardwareBGColor, 340, 275)
        _label = rtk.RAMSTKLabel(
            _(u"Hardware Tree Foreground Color:"), width=350)
        _fixed.put(_label, 5, 305)
        _fixed.put(self.btnHardwareFGColor, 340, 305)
        # _label = rtk.RAMSTKLabel(_(u"Software Tree Background Color:"), width=350)
        # _fixed.put(_label, 5, 335)
        # _fixed.put(self.btnSoftwareBGColor, 340, 335)
        # _label = rtk.RAMSTKLabel(_(u"Software Tree Foreground Color:"), width=350)
        # _fixed.put(_label, 5, 365)
        # _fixed.put(self.btnSoftwareFGColor, 340, 365)
        _label = rtk.RAMSTKLabel(
            _(u"Validation  Tree Background Color:"), width=350)
        _fixed.put(_label, 5, 335)
        _fixed.put(self.btnValidationBGColor, 340, 335)
        _label = rtk.RAMSTKLabel(
            _(u"Validation Tree Foreground Color:"), width=350)
        _fixed.put(_label, 5, 365)
        _fixed.put(self.btnValidationFGColor, 340, 365)
        # _label = rtk.RAMSTKLabel(_(u"Incident Tree Background Color:"), width=350)
        # _fixed.put(_label, 5, 455)
        # _fixed.put(self.btnIncidentBGColor, 340, 455)
        # _label = rtk.RAMSTKLabel(_(u"Incident Tree Foreground Color:"), width=350)
        # _fixed.put(_label, 5, 485)
        # _fixed.put(self.btnIncidentFGColor, 340, 485)
        # _label = rtk.RAMSTKLabel(_(u"Testing Tree Background Color:"), width=350)
        # _fixed.put(_label, 5, 515)
        # _fixed.put(self.btnTestingBGColor, 340, 515)
        # _label = rtk.RAMSTKLabel(_(u"Testing Tree Foreground Color:"), width=350)
        # _fixed.put(_label, 5, 545)
        # _fixed.put(self.btnTestingFGColor, 340, 545)

        _labels = [
            _(u"Default\nTitle"),
            _(u"User\nTitle"),
            _(u"Column\nPosition"),
            _(u"Can\nEdit?"),
            _(u"Is\nVisible?")
        ]

        self.tvwFormatFile = gtk.TreeView()
        _model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING)
        self.tvwFormatFile.set_model(_model)

        for i in range(5):
            if i == 0:
                _cell = gtk.CellRendererText()
                _cell.set_property('background', 'light gray')
                _cell.set_property('editable', 0)
                _cell.set_property('foreground', '#000000')
                _cell.set_property('weight', 700)
                _cell.set_property('weight-set', True)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD)
            elif i > 0 and i < 3:
                _cell = gtk.CellRendererText()
                _cell.set_property('background', '#FFFFFF')
                _cell.set_property('editable', 1)
                _cell.set_property('foreground', '#000000')
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD)
                _cell.connect('edited', self._do_edit_cell, i, _model)
            elif i > 4:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
            else:
                _cell = gtk.CellRendererToggle()
                _cell.set_property('activatable', 1)
                _cell.connect('toggled', self._do_toggle_cell, i, _model)

            _label = gtk.Label()
            _label.set_line_wrap(True)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_markup("<span weight='bold'>" + _labels[i] + "</span>")
            _label.show_all()

            _column = gtk.TreeViewColumn()
            _column.set_widget(_label)
            _column.set_alignment(0.5)
            _column.pack_start(_cell, True)
            if i < 3:
                _column.set_attributes(_cell, text=i)
            elif i > 4:
                _column.set_visible(False)
            else:
                _column.set_attributes(_cell, active=i)

            self.tvwFormatFile.append_column(_column)

        _scrollwindow.add(self.tvwFormatFile)

        _label = rtk.RAMSTKLabel(
            _(u"Look &amp; Feel"), justify=gtk.JUSTIFY_CENTER)
        _label.set_tooltip_text(
            _(u"Allows setting user interface preferences for RAMSTK."))
        self.notebook.insert_page(_hbox_outer, tab_label=_label, position=-1)

        return None

    def _on_combo_changed(self, combo, index):
        """
        Edit rtk.RAMSTKTreeView() layouts.

        :param combo: the rtk.RAMSTKCombo() that called this method.
        :type combo: :class:`rtk.gui.gtk.rtk.RAMSTKCombo`
        :param int index: the index in the signal handler list associated with
                          the rtk.RAMSTKCombo() calling this method.
        :return: None
        :rtype: None
        """
        combo.handler_block(self._lst_handler_id[index])

        if index == 0:
            self._do_load_format(combo)
        elif index == 1:
            self._do_load_list(combo)
        elif index == 2:
            self._user_preferences['tabpos'][
                'modulebook'] = combo.get_active_text()
        elif index == 3:
            self._user_preferences['tabpos'][
                'workbook'] = combo.get_active_text()
        elif index == 4:
            self._user_preferences['tabpos'][
                'listbook'] = combo.get_active_text()
        elif index == 5:
            self._user_preferences['report_size'] = combo.get_active_text()

        combo.handler_unblock(self._lst_handler_id[index])

        return None
