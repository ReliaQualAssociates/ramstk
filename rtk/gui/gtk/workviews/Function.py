# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.Function.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
################################################################################
Function Package WorkView
################################################################################
"""

import sys

# Import modules for localization support.
import gettext
import locale

from pubsub import pub                              # pylint: disable=E0401

# Modules required for the GUI.
try:
    # noinspection PyUnresolvedReferences
    from pygtk import require
    require('2.0')
except ImportError:
    sys.exit(1)
try:
    # noinspection PyUnresolvedReferences
    import gtk
except ImportError:
    sys.exit(1)
try:
    # noinspection PyUnresolvedReferences
    import gtk.glade
except ImportError:
    sys.exit(1)

# Import other RTK modules.
from gui.gtk import rtk                                 # pylint: disable=E0401
from gui.gtk.workviews.FMEA import WorkView as FMEA     # pylint: disable=E0401
from gui.gtk.assistants.Function import AddFunction     # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

_ = gettext.gettext


class WorkView(gtk.VBox):
    """
    The Work View displays all the attributes for the selected Function. The
    attributes of a Work View are:

    :ivar _lst_handler_id: list containing the ID's of the callback signals for
                           each gtk.Widget() associated with an editable
                           Function attribute.

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |      0   | txtCode `focus_out_event`                 |
    +----------+-------------------------------------------+
    |      1   | txtName `focus_out_event`                 |
    +----------+-------------------------------------------+
    |      2   | txtRemarks `focus_out_event`              |
    +----------+-------------------------------------------+
    |      3   | Mission gtk.CellRendererCombo() `edited`  |
    +----------+-------------------------------------------+
    |      4   | Phase gtk.CellRendererCombo() `edited`    |
    +----------+-------------------------------------------+
    |      5   | btnAddMode `clicked`                      |
    +----------+-------------------------------------------+
    |      6   | btnRemoveMode `clicked`                   |
    +----------+-------------------------------------------+
    |      7   | btnSaveFMEA `clicked`                     |
    +----------+-------------------------------------------+

    :ivar _dtc_function: the :class:`rtk.function.Function.Function` data
                         controller to use with this Work Book.

    :ivar chkSafetyCritical: the :class:`gtk.CheckButton` to display/edit the
                             Function's safety criticality.

    :ivar txtCode: the :class:`gtk.Entry` to display/edit the Function code.
    :ivar txtName: the :class:`gtk.Entry` to display/edit the Function name.
    :ivar txtTotalCost: the :class:`gtk.Entry` to display the Function cost.
    :ivar txtModeCount: the :class:`gtk.Entry` to display the number of
                        hardware failure modes the Function is susceptible to.
    :ivar txtPartCount: the :class:`gtk.Entry` to display the number of
                        hardware components comprising the Function.
    :ivar txtRemarks: the :class:`gtk.Entry` to display/edit the Function
                      remarks.
    :ivar txtPredictedHt: the :class:`gtk.Entry` to display the Function
                          logistics hazard rate.
    :ivar txtMissionHt: the :class:`gtk.Entry` to display the Function mission
                        hazard rate.
    :ivar txtMTBF: the :class:`gtk.Entry` to display the Function logistics
                   MTBF.
    :ivar txtMissionMTBF: the :class:`gtk.Entry` to display the Function
                          mission MTBF.
    :ivar txtMPMT: the :class:`gtk.Entry` to display the Function mean
                   preventive maintenance time.
    :ivar txtMCMT: the :class:`gtk.Entry` to display the Function mean
                   corrective maintenance time.
    :ivar txtMTTR: the :class:`gtk.Entry` to display the Function mean time to
                   repair.
    :ivar txtMMT: the :class:`gtk.Entry` to display the Function mean
                  maintenance time.
    :ivar txtAvailability: the :class:`gtk.Entry` to display the Function
                           logistics availability.
    :ivar txtMissionAt: the :class:`gtk.Entry` to display the Function mission
                        availability.
    """

    def __init__(self, controller):
        """
        Method to initialize the Work View for the Function package.

        :param controller: the RTK master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        gtk.VBox.__init__(self)

        # Initialize private dictionary attributes.
        self._dic_icons = {'tab':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/function.png',
                           'calculate':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/calculate.png',
                           'add':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/add.png',
                           'remove':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/remove.png',
                           'reports':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/reports.png',
                           'save':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/save.png',
                           'error':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/error.png',
                           'question':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/question.png',
                           'insert_sibling':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/insert_sibling.png',
                           'insert_child':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/insert_child.png'}

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._mdcRTK = controller
        self._mission_time = controller.RTK_CONFIGURATION.RTK_MTIME
        self._dtc_function = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = '{0:0.' + \
                   str(controller.RTK_CONFIGURATION.RTK_DEC_PLACES) + 'g}'
        self.function_id = None

        # General data page widgets.
        self.chkSafetyCritical = rtk.RTKCheckButton(
            label=_(u"Function is safety critical."),
            tooltip=_(u"Indicates whether or not the selected function is "
                      u"safety critical."))

        self.txtCode = rtk.RTKEntry(tooltip=_(u"Enter a unique code for the "
                                              u"selected function."))
        self.txtTotalCost = rtk.RTKEntry(width=75, editable=False, bold=True,
                                         tooltip=_(u"Displays the total cost "
                                                   u"of the selected "
                                                   u"function."))
        self.txtName = rtk.RTKEntry(width=400, tooltip=_(u"Enter the name of "
                                                         u"the selected "
                                                         u"function."))
        self.txtModeCount = rtk.RTKEntry(width=75, editable=False, bold=True,
                                         tooltip=_(u"Displays the total "
                                                   u"number of failure modes "
                                                   u"associated with the "
                                                   u"selected function."))
        self.txtPartCount = rtk.RTKEntry(width=75, editable=False, bold=True,
                                         tooltip=_(u"Displays the total "
                                                   u"number of components "
                                                   u"associated with the "
                                                   u"selected function."))
        self.txtRemarks = rtk.RTKTextView(txvbuffer=gtk.TextBuffer(),
                                          width=400,
                                          tooltip=_(u"Enter any remarks "
                                                    u"related to the selected "
                                                    u"function."))

        # Assessment results page widgets.
        self.txtPredictedHt = rtk.RTKEntry(width=100, editable=False,
                                           bold=True,
                                           tooltip=_(u"Displays the logistics "
                                                     u"failure intensity for "
                                                     u"the selected "
                                                     u"function."))
        self.txtMissionHt = rtk.RTKEntry(width=100, editable=False, bold=True,
                                         tooltip=_(u"Displays the mission "
                                                   u"failure intensity for "
                                                   u"the selected function."))
        self.txtMTBF = rtk.RTKEntry(width=100, editable=False, bold=True,
                                    tooltip=_(u"Displays the logistics mean "
                                              u"time between failure (MTBF) "
                                              u"for the selected function."))
        self.txtMissionMTBF = rtk.RTKEntry(width=100, editable=False,
                                           bold=True,
                                           tooltip=_(u"Displays the mission "
                                                     u"mean time between "
                                                     u"failure (MTBF) for the "
                                                     u"selected function."))
        self.txtMPMT = rtk.RTKEntry(width=100, editable=False, bold=True,
                                    tooltip=_(u"Displays the mean preventive "
                                              u"maintenance time (MPMT) for "
                                              u"the selected function."))
        self.txtMCMT = rtk.RTKEntry(width=100, editable=False, bold=True,
                                    tooltip=_(u"Displays the mean corrective "
                                              u"maintenance time (MCMT) for "
                                              u"the selected function."))
        self.txtMTTR = rtk.RTKEntry(width=100, editable=False, bold=True,
                                    tooltip=_(u"Displays the mean time to "
                                              u"repair (MTTR) for the "
                                              u"selected function."))
        self.txtMMT = rtk.RTKEntry(width=100, editable=False, bold=True,
                                   tooltip=_(u"Displays the mean maintenance "
                                             u"time (MMT) for the selected "
                                             u"function."))
        self.txtAvailability = rtk.RTKEntry(width=100, editable=False,
                                            bold=True,
                                            tooltip=_(u"Displays the lgistics "
                                                      u"availability for the "
                                                      u"selected function."))
        self.txtMissionAt = rtk.RTKEntry(width=100, editable=False, bold=True,
                                         tooltip=_(u"Displays the mission "
                                                   u"availability for the "
                                                   u"selected function."))

        _notebook = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if controller.RTK_CONFIGURATION.RTK_TABPOS['workbook'] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif controller.RTK_CONFIGURATION.RTK_TABPOS['workbook'] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif controller.RTK_CONFIGURATION.RTK_TABPOS['workbook'] == 'top':
            _notebook.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook.set_tab_pos(gtk.POS_BOTTOM)

        self._make_general_data_page(_notebook)
        self._make_fmea_page(_notebook)
        self._make_assessment_results_page(_notebook)

        try:
            locale.setlocale(locale.LC_ALL,
                             controller.RTK_CONFIGURATION.RTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

        # Connect to callback functions for editable gtk.Widgets().
        self._lst_handler_id.append(
            self.txtCode.connect('changed', self._do_edit_function, 0))
        self._lst_handler_id.append(
            self.txtName.connect('changed', self._do_edit_function, 1))
        self._lst_handler_id.append(
            self.txtRemarks.do_get_buffer().connect(
                'changed', self._do_edit_function, 2))

        # Put it all together.
        self.pack_start(self._make_toolbar(), expand=False)
        self.pack_start(_notebook)

        self.show_all()

        pub.subscribe(self._on_select_function, 'selectedFunction')
        pub.subscribe(self._on_edit_function, 'mvwEditedFunction')
        pub.subscribe(self._on_edit_function, 'calculatedFunction')

    def do_add_function(self, level):
        """
        Method to actually add the function.  This method is called by the
        AddFunction gtk.Assistant() when the Apply button is pressed.

        :param str level: the level the new Function should have relative to
                          the currently selected Function.  Values are:

                          * sibling
                          * child

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _function = self._dtc_function.request_select(self.function_id)
        _revision_id = _function.revision_id

        if level == 'sibling':
            _parent_id = _function.parent_id
        else:
            _parent_id = _function.function_id

        # By default we add the new function as a top-level function.
        if _parent_id is None:
            _parent_id = 0

        if not self._dtc_function.request_insert(_revision_id,
                                                 _parent_id,
                                                 level):
            # TODO: Add code to the Matrix Class to respond to the 'insertedFunction' pubsub message and insert a record into each of the Function-X matrices.

            self._mdcRTK.RTK_CONFIGURATION.RTK_PREFIX['function'][1] += 1
        else:
            _msg = _(u"An error occurred while attempting to add one or more "
                     u"functions.")
            _error_dialog = rtk.RTKMessageDialog(_msg,
                                                 self._dic_icons['error'],
                                                 'error',
                                                 self.get_parent())
            self._mdcRTK.debug_log.error(_msg)

            if _error_dialog.do_run() == gtk.RESPONSE_OK:
                _error_dialog.do_destroy()

            _return = True

        return _return

    def _do_edit_function(self, entry, index):
        """
        Method to retrieve changes made to Function attributes through the
        various gtk.Widgets() and assign the new data to the appropriate
        Function data model attribute.  This method is called by:

            * gtk.Entry() 'changed' signal
            * gtk.TextView() 'changed' signal

        This method sends the 'wvwEditedFunction' message.

        :param gtk.Entry entry: the gtk.Entry() that called the method.
        :param int index: the position in the Function class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Widget().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False
        _position = None
        _text = None

        entry.handler_block(self._lst_handler_id[index])

        if index == 0:
            _text = str(entry.get_text())
            _position = 5
        elif index == 1:
            _text = str(entry.get_text())
            _position = 15
        elif index == 2:
            _text = self.txtRemarks.do_get_text()
            _position = 17

        entry.handler_unblock(self._lst_handler_id[index])

        pub.sendMessage('wvwEditedFunction', position=_position,
                        new_text=_text)

        return _return

    def _do_request_calculate(self, __button):
        """
        Method to send request to calculate the selected function to the
        Function data controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code = 0
        _msg = ['', '']

        if self._dtc_function.request_calculate_reliability(self.function_id):
            _error_code = 1
            _msg[0] = 'Error calculating reliability attributes.'

        if self._dtc_function.request_calculate_availability(self.function_id):
            _error_code = 1
            _msg[1] = 'Error calculating availability attributes.'

        if _error_code != 0:
            _prompt = _(u"An error occurred when attempting to calculate "
                        u"Function {0:d}. \n\n\t" + _msg[0] + "\n\t" +
                        _msg[1] + "\n\n").format(self.function_id)
            _error_dialog = rtk.RTKMessageDialog(_prompt,
                                                 self._dic_icons['error'],
                                                 'error')
            if _error_dialog.do_run() == gtk.RESPONSE_OK:
                _error_dialog.do_destroy()

            _return = True

        return _return

    def _do_request_delete(self, __button):
        """
        Method to send request to delete the selected function from the
        Function data controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _prompt = _(u"You are about to delete Function {0:d} and all data "
                    u"associated with it.  Is this really what you want "
                    u"to do?").format(self.function_id)
        _dialog = rtk.RTKMessageDialog(_prompt, self._dic_icons['question'],
                                       'question')
        _response = _dialog.do_run()

        if _response == gtk.RESPONSE_YES:
            _dialog.do_destroy()
            if self._dtc_function.request_delete(self.function_id):
                _prompt = _(u"An error occurred when attempting to delete "
                            u"Function {0:d}.").format(self.function_id)
                _error_dialog = rtk.RTKMessageDialog(_prompt,
                                                     self._dic_icons['error'],
                                                     'error')
                if _error_dialog.do_run() == gtk.RESPONSE_OK:
                    _error_dialog.do_destroy()

                _return = True
        else:
            _dialog.do_destroy()

        return _return

    def _do_request_insert(self, __button, level):
        """
        Method to send request to insert a new Function into the RTK Program
        database.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :param str level: the level the new Function should have relative to
                          the currently selected Function.  Values are:

                          * sibling
                          * child

        :return: None
        :rtype: None
        """

        AddFunction(self, level=level)

        return None

    def _do_request_update(self, __button):
        """
        Method to save all the Functions.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self._dtc_function.request_update_all()

    def _make_assessment_results_page(self, notebook):
        """
        Method to create the Function class gtk.Notebook() page for
        displaying assessment results for teh selected Function.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _hbox = gtk.HBox()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build the left half of the page.                                    #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame = rtk.RTKFrame(label=_(u"Reliability Results"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_start(_frame)

        _labels = [_(u"Predicted h(t):"), _(u"Mission h(t):"), _(u"MTBF:"),
                   _(u"Mission MTBF:")]
        _x_pos, _y_pos = rtk.make_label_group(_labels, _fixed, 5, 5)
        _x_pos += 50

        _fixed.put(self.txtPredictedHt, _x_pos, _y_pos[0])
        _fixed.put(self.txtMissionHt, _x_pos, _y_pos[1])
        _fixed.put(self.txtMTBF, _x_pos, _y_pos[2])
        _fixed.put(self.txtMissionMTBF, _x_pos, _y_pos[3])

        _fixed.show_all()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build the right half of the page.                                   #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame = rtk.RTKFrame(label=_(u"Maintainability Results"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame)

        _labels = [_(u"MPMT:"), _(u"MCMT:"), _(u"MTTR:"), _(u"MMT:"),
                   _(u"Availability:"), _(u"Mission Availability:")]
        _x_pos, _y_pos = rtk.make_label_group(_labels, _fixed, 5, 5)
        _x_pos += 50

        _fixed.put(self.txtMPMT, _x_pos, _y_pos[0])
        _fixed.put(self.txtMCMT, _x_pos, _y_pos[1])
        _fixed.put(self.txtMTTR, _x_pos, _y_pos[2])
        _fixed.put(self.txtMMT, _x_pos, _y_pos[3])
        _fixed.put(self.txtAvailability, _x_pos, _y_pos[4])
        _fixed.put(self.txtMissionAt, _x_pos, _y_pos[5])

        _fixed.show_all()

        # Insert the tab.
        _label = rtk.RTKLabel(_(u"Assessment\nResults"), width=-1,
                              justify=gtk.JUSTIFY_CENTER,
                              tooltip=_(u"Displays reliability, "
                                        u"maintainability, and availability "
                                        u"assessment results for the selected "
                                        u"function."))
        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _make_fmea_page(self, notebook):
        """
        Method to create the Function class gtk.Notebook() page for displaying
        the FMEA for the selected Function.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: false if successful or True if an error is encountered.
        :rtype: bool
        """

        _label = rtk.RTKLabel(_(u"FMEA"), width=-1,
                              justify=gtk.JUSTIFY_CENTER,
                              tooltip=_(u"Displays the Failure Mode and "
                                        u"Effects Analysis (FMEA) for "
                                        u"the selected Function."))

        notebook.insert_page(FMEA(self._mdcRTK), tab_label=_label,
                             position=-1)

        return False

    def _make_general_data_page(self, notebook):
        """
        Method to create the Function class gtk.Notebook() page for
        displaying general data about the selected Function.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _frame = rtk.RTKFrame(label=_(u"General Information"))

        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                 gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame.add(_scrollwindow)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information about   #
        # the function.                                                 #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _labels = [_(u"Function Code:"), _(u"Function Name:"),
                   _(u"Total Cost:"), _(u"Total Mode Count:"),
                   _(u"Total Part Count:"), _(u"Remarks:")]
        _x_pos, _y_pos = rtk.make_label_group(_labels, _fixed, 5, 5)
        _x_pos = _x_pos + 50

        # Place the widgets.
        _fixed.put(self.txtCode, _x_pos, _y_pos[0])
        _fixed.put(self.txtName, _x_pos, _y_pos[1])
        _fixed.put(self.txtTotalCost, _x_pos, _y_pos[2])
        _fixed.put(self.txtModeCount, _x_pos, _y_pos[3])
        _fixed.put(self.txtPartCount, _x_pos, _y_pos[4])
        _fixed.put(self.txtRemarks.scrollwindow, _x_pos, _y_pos[5])
        _fixed.put(self.chkSafetyCritical, 5, _y_pos[5] + 110)

        _fixed.show_all()

        # Insert the tab.
        _label = rtk.RTKLabel(_(u"General\nData"), width=-1,
                              justify=gtk.JUSTIFY_CENTER,
                              tooltip=_(u"Displays general information for "
                                        u"the selected Function."))
        notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _make_toolbar(self):
        """
        Method to create the toolbar for the Function class work book.
        """

        _toolbar = gtk.Toolbar()

        _position = 0

        # Add sibling function button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Adds a new function at the same "
                                   u"hierarchy level as the selected function "
                                   u"(i.e., a sibling function)."))
        _image = gtk.Image()
        _image.set_from_file(self._dic_icons['insert_sibling'])
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._do_request_insert, 'sibling')
        _toolbar.insert(_button, _position)
        _position += 1

        # Add child function button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Adds a new function one level "
                                   u"subordinate to the selected function "
                                   u"(i.e., a child function)."))
        _image = gtk.Image()
        _image.set_from_file(self._dic_icons['insert_child'])
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._do_request_insert, 'child')
        _toolbar.insert(_button, _position)
        _position += 1

        # Delete function button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Removes the currently selected "
                                   u"function."))
        _image = gtk.Image()
        _image.set_from_file(self._dic_icons['remove'])
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._do_request_delete)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Calculate function button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Calculate the functions."))
        _image = gtk.Image()
        _image.set_from_file(self._dic_icons['calculate'])
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._do_request_calculate)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save function button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Saves changes to the selected function."))
        _image = gtk.Image()
        _image.set_from_file(self._dic_icons['save'])
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._do_request_update)
        _toolbar.insert(_button, _position)

        _toolbar.show()

        return _toolbar

    def _on_edit_function(self, function_id):
        """
        Method to update the Work View gtk.Widgets() with changes to the
        Function data model attributes.

        :param int function_id: the ID of the Function that was edited.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _function = self._dtc_function.request_select(function_id)

        self.txtCode.handler_block(self._lst_handler_id[0])
        self.txtCode.set_text(str(_function.function_code))
        self.txtCode.handler_unblock(self._lst_handler_id[0])

        self.txtName.handler_block(self._lst_handler_id[1])
        self.txtName.set_text(_function.name)
        self.txtName.handler_unblock(self._lst_handler_id[1])

        _textbuffer = self.txtRemarks.do_get_buffer()
        _textbuffer.handler_block(self._lst_handler_id[2])
        _textbuffer.set_text(_function.remarks)
        _textbuffer.handler_unblock(self._lst_handler_id[2])

        return _return

    def _on_select_function(self, function_id):
        """
        Method to load the Function Work View class gtk.Notebook() widgets.

        :param int function_id: the Function ID of the selected/edited
                                Function.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _return = False

        self._dtc_function = self._mdcRTK.dic_controllers['function']
        _function = self._dtc_function.request_select(function_id)

        self.function_id = _function.function_id

        # ----- ----- ----- LOAD GENERAL DATA PAGE ----- ----- ----- #
        self.txtCode.handler_block(self._lst_handler_id[0])
        self.txtCode.set_text(str(_function.function_code))
        self.txtCode.handler_unblock(self._lst_handler_id[0])

        self.txtName.handler_block(self._lst_handler_id[1])
        self.txtName.set_text(_function.name)
        self.txtName.handler_unblock(self._lst_handler_id[1])

        _textbuffer = self.txtRemarks.do_get_buffer()
        _textbuffer.handler_block(self._lst_handler_id[2])
        _textbuffer.set_text(_function.remarks)
        _textbuffer.handler_unblock(self._lst_handler_id[2])

        self.txtTotalCost.set_text(
            str(locale.currency(_function.cost)))
        self.txtModeCount.set_text(
            str('{0:d}'.format(_function.total_mode_count)))
        self.txtPartCount.set_text(
            str('{0:d}'.format(_function.total_part_count)))

        # ----- ----- ----- LOAD ASSESSMENT RESULTS PAGE ----- ----- ----- #
        self.txtAvailability.set_text(
            str(self.fmt.format(_function.availability_logistics)))
        self.txtMissionAt.set_text(
            str(self.fmt.format(_function.availability_mission)))
        self.txtMissionHt.set_text(
            str(self.fmt.format(_function.hazard_rate_mission)))
        self.txtPredictedHt.set_text(
            str(self.fmt.format(_function.hazard_rate_logistics)))

        self.txtMMT.set_text(str(self.fmt.format(_function.mmt)))
        self.txtMCMT.set_text(str(self.fmt.format(_function.mcmt)))
        self.txtMPMT.set_text(str(self.fmt.format(_function.mpmt)))

        self.txtMissionMTBF.set_text(
            str(self.fmt.format(_function.mtbf_mission)))
        self.txtMTBF.set_text(
            str(self.fmt.format(_function.mtbf_logistics)))
        self.txtMTTR.set_text(str(self.fmt.format(_function.mttr)))

        return _return
