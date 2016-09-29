#!/usr/bin/env python
"""
###############################
Software Package List Book View
###############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.software.ListBook.py is part of the RTK Project
#
# All rights reserved.

import sys

# Import modules for localization support.
import gettext
import locale

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

# Import other RTK modules.
try:
    import Configuration
    import Utilities
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    import rtk.gui.gtk.Widgets as Widgets
import __gui.gtk.TestSelection as TestSelection

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2016 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _set_risk_icon(risk, module):          # pylint: disable=R0912
    """
    Function to find the hexadecimal code for the risk level colors.

    :param dict risk: dictionary containing the Software class risk factors.
    :param int module: the Software ID used as a key for accessing the correct
                       risk factors from the risk dictionary.
    :return: a dictionary containing the icon for each risk factor.
    :rtype: dict
    """

    _lst_risk_icons = []

    _icon = Configuration.ICON_DIR + '32x32/none.png'
    _lst_risk_icons.append(gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22))
    _icon = Configuration.ICON_DIR + '32x32/low.png'
    _lst_risk_icons.append(gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22))
    _icon = Configuration.ICON_DIR + '32x32/medium.png'
    _lst_risk_icons.append(gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22))
    _icon = Configuration.ICON_DIR + '32x32/high.png'
    _lst_risk_icons.append(gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22))

    _icon = {'A': _lst_risk_icons[0], 'D': _lst_risk_icons[0],
             'SA': _lst_risk_icons[0], 'ST': _lst_risk_icons[0],
             'SQ': _lst_risk_icons[0], 'SL': _lst_risk_icons[0],
             'SX': _lst_risk_icons[0], 'SM': _lst_risk_icons[0],
             'Risk': _lst_risk_icons[0]}

    # Find the Application risk level.
    _icon['A'] = _lst_risk_icons[_set_application_risk_icon(risk[module][0])]

    # Find the Development risk level.
    _icon['D'] = _lst_risk_icons[_set_development_risk_icon(risk[module][1])]

    # Find the Anomaly Management risk level.
    _icon['SA'] = _lst_risk_icons[_set_anomaly_management_risk_icon(
        risk[module][2])]

    # Find the Requirement Traceability risk level.
    _icon['ST'] = _lst_risk_icons[_set_traceability_risk_icon(risk[module][3])]

    # Find the Software Quality risk level.
    _icon['SQ'] = _lst_risk_icons[_set_quality_risk_icon(risk[module][4])]

    # Find the Language Type risk level.
    _icon['SL'] = _lst_risk_icons[_set_language_risk_icon(risk[module][5])]

    # Find the Complexity risk level.
    _icon['SX'] = _lst_risk_icons[_set_complexity_risk_icon(risk[module][6])]

    # Find the Modularity risk level.
    _icon['SM'] = _lst_risk_icons[_set_modularity_risk_icon(risk[module][7])]

    # Find the overall risk level.
    if risk[module][8] > 0.0 and risk[module][8] <= 1.5:
        _icon['Risk'] = _lst_risk_icons[1]
    elif risk[module][8] > 1.5 and risk[module][8] < 3.5:
        _icon['Risk'] = _lst_risk_icons[2]
    elif risk[module][8] >= 3.5:
        _icon['Risk'] = _lst_risk_icons[3]

    return _icon


def _set_application_risk_icon(risk):
    """
    Function to find the index risk level icon for application risk.

    :param float risk: the Software application risk factor.
    :return: _index
    :rtype: int
    """

    _index = int(risk)

    return _index


def _set_development_risk_icon(risk):
    """
    Function to find the index risk level icon for development environment
    risk.

    :param float risk: the Software development environment risk factor.
    :return: _index
    :rtype: int
    """

    _index = 0

    if risk == 0.5:
        _index = 1
    elif risk == 1.0:
        _index = 2
    elif risk == 2.0:
        _index = 3

    return _index


def _set_anomaly_management_risk_icon(risk):
    """
    Function to find the index risk level icon for anomaly management risk.

    :param float risk: the Software anomaly management risk factor.
    :return: _index
    :rtype: int
    """

    _index = 0

    if risk == 0.9:
        _index = 1
    elif risk == 1.1:
        _index = 2
    elif risk == 1.0:
        _index = 3

    return _index


def _set_traceability_risk_icon(risk):
    """
    Function to find the index risk level icon for requirements traceability
    risk.

    :param float risk: the Software requirements traceability risk factor.
    :return: _index
    :rtype: int
    """

    _index = 0

    if risk == 0.9:
        _index = 1
    elif risk == 1.0:
        _index = 2
    elif risk == 1.1:
        _index = 3

    return _index


def _set_quality_risk_icon(risk):
    """
    Function to find the index risk level icon for software quality risk.

    :param float risk: the Software quality risk factor.
    :return: _index
    :rtype: int
    """

    _index = 0

    if risk == 1.0:
        _index = 1
    elif risk == 1.1:
        _index = 2

    return _index


def _set_language_risk_icon(risk):
    """
    Function to find the index risk level icon for language type risk.

    :param float risk: the Software language type risk factor.
    :return: _index
    :rtype: int
    """

    _index = 0

    if risk == 1.0:
        _index = 1
    elif risk > 1.0 and risk <= 1.2:
        _index = 2
    elif risk > 1.2:
        _index = 3

    return _index


def _set_complexity_risk_icon(risk):
    """
    Function to find the index risk level icon for complexity risk.

    :param float risk: the Software complexity risk factor.
    :return: _index
    :rtype: int
    """

    _index = 0

    if risk >= 0.8 and risk < 1.0:
        _index = 1
    elif risk >= 1.0 and risk <= 1.2:
        _index = 2
    elif risk > 1.2:
        _index = 3

    return _index


def _set_modularity_risk_icon(risk):
    """
    Function to find the index risk level icon for modularity risk.

    :param float risk: the Software modularity risk factor.
    :return: _index
    :rtype: int
    """

    _index = 0

    if risk >= 0.9 and risk < 1.2:
        _index = 1
    elif risk >= 1.2 and risk <= 1.5:
        _index = 2
    elif risk > 1.5:
        _index = 3

    return _index


class ListView(gtk.VBox):
    """
    The List Book view displays all the matrices and lists associated with the
    Software Class.  The attributes of a Software List Book view are:

    :ivar list _lst_handler_id: list containing the ID's of the callback
                                signals for each gtk.Widget() associated with
                                an editable Software attribute.

    +----------+--------------------------------------------+
    | Position | Widget - Signal                            |
    +==========+============================================+
    |     0    | btnCalcRisk - 'clicked'                    |
    +----------+--------------------------------------------+
    |     1    | btnSaveTest - 'clicked'                    |
    +----------+--------------------------------------------+

    :ivar _mdcRTK: the :py:class:`rtk.RTK.RTK` master data controller.
    :ivar _model: the :py:class:`rtk.software.Software.Model` data model to
                  display.
    :ivar gtk.Button btnCalcRisk: the gtk.Button() to request the Software risk
                                  matrix be calculated.
    :ivar gtk.Button btnSaveTest: the gtk.Button() to request the Software test
                                  technique selections be saved.
    :ivar gtk.Frame fraTestSelection: the gtk.Frame() to hold the Software test
                                      technique selection gtk.ScrolledWindow()
                                      for the selected Software module.
    :ivar gtk.ScrolledWindow scwCSCITestSelection: the gtk.ScrolledWindow() to
                                                   hold the gtk.TreeView() for
                                                   the Software CSCI test
                                                   selection matrix.
    :ivar gtk.ScrolledWindow scwUnitTestSelection: the gtk.ScrolledWindow() to
                                                   hold the gtk.TreeView() for
                                                   the Software unit test
                                                   selection matrix.
    :ivar gtk.TreeView tvwRiskMap: the gtk.TreeView() to display the Software
                                   risk matrix.
    """

    def __init__(self, modulebook):
        """
        Method to initialize the List Book view for the Software package.

        :param modulebook: the :py:class:`rtk.software.ModuleBook` to associate
                           with this List Book.
        """

        gtk.VBox.__init__(self)

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_handler_id = []

        # Define private scalar attributes.
        self._mdcRTK = modulebook.mdcRTK
        self._dtcBoM = modulebook.mdcRTK.dtcSoftwareBoM
        self._model = None

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.btnCalcRisk = Widgets.make_button(width=35, image='calculate')
        self.btnSaveTest = Widgets.make_button(width=35, image='save')

        self.fraTestSelection = Widgets.make_frame(
            label=_(u"Test Technique Selection"))
        self.fraTestSelection.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        self.scwCSCITestSelection = TestSelection.CSCITestSelection()
        self.scwCSCITestSelection.create_test_planning_matrix()

        self.scwUnitTestSelection = TestSelection.UnitTestSelection()
        self.scwUnitTestSelection.create_test_planning_matrix()

        self.tvwRiskMap = gtk.TreeView()

        # Set tooltips for the gtk.Widgets().
        self.btnCalcRisk.set_tooltip_text(_(u"Calculate the reliability "
                                            u"risk assessment."))
        self.tvwRiskMap.set_tooltip_markup(_(u"Displays the risk associated "
                                             u"with the software system."))

        # Connect widget signals to callback methods.
        self._lst_handler_id.append(
            self.btnCalcRisk.connect('clicked',
                                     self._on_button_clicked, 0))
        self._lst_handler_id.append(
            self.btnSaveTest.connect('clicked',
                                     self._on_button_clicked, 1))

        # Put it all together.
        _notebook = self._create_notebook()
        self.pack_start(_notebook)

        self.show_all()

    def _create_notebook(self):
        """
        Method to create the Software class List View gtk.Notebook().

        :return: _notebook
        :rtype: gtk.Notebook
        """

        _notebook = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if Configuration.TABPOS[1] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif Configuration.TABPOS[1] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif Configuration.TABPOS[1] == 'top':
            _notebook.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook.set_tab_pos(gtk.POS_BOTTOM)

        self._create_risk_matrix_page(_notebook)
        self._create_testing_matrix_page(_notebook)

        return _notebook

    def _create_risk_matrix_page(self, notebook):
        """
        Method to create the Software Risk matrix page in the List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Build up the containers for the Software Risk matrix page.
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)
        _bbox.pack_start(self.btnCalcRisk, False, False)

        _hbox.pack_start(_bbox, False, False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwRiskMap)

        _frame = Widgets.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)

        # Add the risk map.
        _headings = [_(u"Software\nModule"), _(u"Application\nRisk"),
                     _(u"Organization\nRisk"), _(u"Anomaly\nManagement\nRisk"),
                     _(u"Traceability\nRisk"), _(u"Quality\nAssurance\nRisk"),
                     _(u"Language\nRisk"), _(u"Code\nComplexity\nRisk"),
                     _(u"Modularity\nRisk"), _(u"Overall\nRisk")]

        _model = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gtk.gdk.Pixbuf, gtk.gdk.Pixbuf, gtk.gdk.Pixbuf,
                               gtk.gdk.Pixbuf, gtk.gdk.Pixbuf, gtk.gdk.Pixbuf,
                               gtk.gdk.Pixbuf, gtk.gdk.Pixbuf, gtk.gdk.Pixbuf)
        self.tvwRiskMap.set_model(_model)
        self.tvwRiskMap.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        _cell = gtk.CellRendererText()
        _cell.set_property('visible', False)
        _column = gtk.TreeViewColumn()
        _column.set_visible(False)
        _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=0)

        self.tvwRiskMap.append_column(_column)

        _label = gtk.Label()
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_property('angle', 90)
        _label.set_markup("<span weight='bold'>" + _headings[0] + "</span>")
        _label.set_use_markup(True)
        _label.show_all()
        _column = gtk.TreeViewColumn()
        _column.set_widget(_label)
        _column.set_visible(True)
        _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        _cell = gtk.CellRendererText()
        _cell.set_property('visible', True)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=1)

        self.tvwRiskMap.append_column(_column)

        for i in range(2, 11):
            _label = gtk.Label()
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_property('angle', 90)
            _label.set_markup("<span weight='bold'>" +
                              _headings[i - 1] +
                              "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _column = gtk.TreeViewColumn()
            _column.set_widget(_label)
            _column.set_visible(True)
            _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
            _cell = gtk.CellRendererPixbuf()
            _cell.set_property('xalign', 0.5)
            _cell.set_property('yalign', 0.5)
            _column.pack_start(_cell, False)
            _column.set_attributes(_cell, pixbuf=i)

            self.tvwRiskMap.append_column(_column)

        # Add the Software Risk Matrix page to the gtk.Notebook().
        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Risk\nMatrix</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the matrix showing risk "
                                  u"between system functions and system "
                                  u"software items."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_testing_matrix_page(self, notebook):
        """
        Method to create the Software/Testing matrix page in the List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Build up the containers for the Software/Testing matrix page.
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)
        _bbox.pack_start(self.btnSaveTest, False, False)

        _hbox.pack_start(_bbox, False, True)
        _hbox.pack_end(self.fraTestSelection, True, True)

        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Testing\nMatrix</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the matrix showing relationships "
                                  u"between system software and system "
                                  u"tests."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Method to load the Software List Book.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._model = model

        _model = self.tvwRiskMap.get_model()
        _model.clear()

        _software = self._dtcBoM.dicSoftware.values()
        _top_module = [_s for _s in _software if _s.software_id == 0]

        self._load_risk_map(_top_module, _software, _model)
        self._load_testing_matrix_page()

        return False

    def _load_risk_map(self, parents, software, model, row=None):
        """
        Method to load the Software class Risk Map.

        :param list parents: list of parent Software modules.
        :param list software: list of Software modules.
        :param gtk.TreeModel model: the gtk.TreeModel() displaying the Software
                                    risk map.
        :keyword gtk.TreeIter row: the selected gtk.TreeIter() in the Software
                                   risk map.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _dicRisk = {}

        for _software in parents:
            _data = [_software.software_id, _software.description]
            _dicRisk[_software.software_id] = [_software.a_risk,
                                               _software.d_risk, _software.sa,
                                               _software.st, _software.sq,
                                               _software.sl, _software.sx,
                                               _software.sm, _software.rpfom]

            # Get the hexidecimal color code for each risk factor.
            _color = _set_risk_icon(_dicRisk, _software.software_id)

            if _software.parent_id == -1:   # It's the top level element.
                row = None

            _data.append(_color['A'])
            _data.append(_color['D'])
            _data.append(_color['SA'])
            _data.append(_color['ST'])
            _data.append(_color['SQ'])
            _data.append(_color['SL'])
            _data.append(_color['SX'])
            _data.append(_color['SM'])
            _data.append(_color['Risk'])

            _piter = model.append(row, _data)

            _parents = [_s for _s in software
                        if _s.parent_id == _software.software_id]
            self._load_risk_map(_parents, software, model, _piter)

        self.tvwRiskMap.expand_all()

        return False

    def _load_testing_matrix_page(self):
        """
        Method to load the Software/Testing matrix page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _child in self.fraTestSelection.get_children():
            self.fraTestSelection.remove(_child)
        if self._model.level_id == 2:       # CSCI
            self.scwCSCITestSelection.load_test_selections(self._model)
            self.fraTestSelection.add(self.scwCSCITestSelection)
        elif self._model.level_id == 3:     # Unit
            self.scwUnitTestSelection.load_test_selections(self._model)
            self.fraTestSelection.add(self.scwUnitTestSelection)

        self.fraTestSelection.resize_children()

        return False

    def _on_button_clicked(self, button, index):
        """
        Callback method to respond to button clicks.

        :param gtk.Button button: the gtk.Button() that called this method.
        :param int index: the index in the signal handler list associated with
                          the Matrix calling this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# WARNING: Refactor _on_button_clicked; current McCabe Complexity metric = 14.
        _return = False

        button.handler_block(self._lst_handler_id[index])

        if index == 0:
            self._dtcBoM.request_calculate()

            for __, _key in enumerate(self._dtcBoM.dicSoftware[0].dicErrors):
                if sum(self._dtcBoM.dicSoftware[0].dicErrors[_key]) != 0:
                    _error = self._dtcBoM.dicSoftware[0].dicErrors[_key][0]
                    if _error != 0:
                        _content = "rtk.software.ListBook._on_button_clicked: " \
                                   "Received error {0:d} while attempting " \
                                   "to calculate anomaly management factor " \
                                   "for {1:d}.".format(_error, _key)
                        self._mdcRTK.debug_log.error(_content)

                    _error = self._dtcBoM.dicSoftware[0].dicErrors[_key][1]
                    if _error != 0:
                        _content = "rtk.software.ListBook._on_button_clicked: " \
                                   "Received error {0:d} while attempting " \
                                   "to calculate software quality factor " \
                                   "for {1:d}.".format(_error, _key)
                        self._mdcRTK.debug_log.error(_content)

                    _error = self._dtcBoM.dicSoftware[0].dicErrors[_key][2]
                    if _error != 0:
                        _content = "rtk.software.ListBook._on_button_clicked: " \
                                   "Received error {0:d} while attempting " \
                                   "to calculate language type factor " \
                                   "for {1:d}.".format(_error, _key)
                        self._mdcRTK.debug_log.error(_content)

                    _error = self._dtcBoM.dicSoftware[0].dicErrors[_key][3]
                    if _error != 0:
                        _content = "rtk.software.ListBook._on_button_clicked: " \
                                   "Received error {0:d} while attempting " \
                                   "to calculate the risk reduction for " \
                                   "{1:d}.".format(_error, _key)
                        self._mdcRTK.debug_log.error(_content)

                    _error = self._dtcBoM.dicSoftware[0].dicErrors[_key][4]
                    if _error != 0:
                        _content = "rtk.software.ListBook._on_button_clicked: " \
                                   "Received error {0:d} while attempting " \
                                   "to calculate the reliability estimation " \
                                   "number for {1:d}.".format(_error, _key)
                        self._mdcRTK.debug_log.error(_content)

                    _return = True

            if _return:
                _prompt = _(u"One or more errors occurred while attempting to "
                            u"calculate software reliability.")
                Widgets.rtk_error(_prompt)
            else:
                # Load the risk map.
                _software = self._dtcBoM.dicSoftware.values()
                _top_module = [_s for _s in _software if _s.software_id == 0]

                _model = self.tvwRiskMap.get_model()
                _model.clear()

                self._load_risk_map(_top_module, _software, _model)

        elif index == 1:
            self._dtcBoM.save_test_selections(self._model.software_id)

        button.handler_unblock(self._lst_handler_id[index])

        return _return
