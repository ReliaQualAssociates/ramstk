#!/usr/bin/env python
"""
#################################
Testing Package Assistants Module
#################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.testing.Assistants.py is part of The RTK Project
#
# All rights reserved.

import gettext
import locale
import sys
from datetime import datetime

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

# Modules used for mathematics.
from scipy.stats import norm

# Import other RTK modules.
try:
    import Configuration
    import Utilities
    import gui.gtk.Widgets as Widgets
    import analyses.statistics.growth.CrowAMSAA as CrowAMSAA
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    import rtk.gui.gtk.Widgets as Widgets
    import rtk.analyses.statistics.growth.CrowAMSAA as CrowAMSAA

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class MTBFICalculator(gtk.Dialog):
    """
    This is the assistant that calculate the average first phase MTBF for a
    Reliability Growth program.
    """

    def __init__(self, entry, model):
        """
        Method to initialize an instance of the MTFBI Assistant.

        :param gtk.Entry entry: the gtk.Entry() to put the results of the
                                calculation in.
        :param model: the :py:class:`rtk.testing.growth.Growth.Model` whose
                      average first phase MTBF is being calculated.
        """

        gtk.Dialog.__init__(self, title=_(u"RTK Mean Time to First Fix "
                                          u"Assistant"),
                            parent=None,
                            flags=(gtk.DIALOG_MODAL |
                                   gtk.DIALOG_DESTROY_WITH_PARENT),
                            buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                                     gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._entry = entry
        self._model = model

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        fmt = '{0:0.' + str(Configuration.PLACES) + 'g}'

        self.txtMTBFI = Widgets.make_entry(width=100)
        self.txtMTBFF = Widgets.make_entry(width=100)
        self.txtTestTime = Widgets.make_entry(width=100)
        self.txtNFailures = Widgets.make_entry(width=100)

        # Connect the buttons to callback methods.
        self.get_action_area().get_children()[0].connect('button-release-event',
                                                         self._cancel)
        self.get_action_area().get_children()[1].connect('button-release-event',
                                                         self._calculate)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the dialog.                       #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()
        self.vbox.pack_start(_fixed)        # pylint: disable=E1101

        _labels = [_(u"Please enter either the initial and final MTBF or the "
                     u"test time and expected number of failures."),
                   _(u"Phase 1 Initial MTBF:"), _(u"Phase 1 Final MTBF:"),
                   _(u"Phase 1 Test Time:"),
                   _(u"Expected Number of Failures During Phase 1:")]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, 5)
        _x_pos += 55

        _fixed.put(self.txtMTBFI, _x_pos, _y_pos[1])
        _fixed.put(self.txtMTBFF, _x_pos, _y_pos[2])
        _fixed.put(self.txtTestTime, _x_pos, _y_pos[3])
        _fixed.put(self.txtNFailures, _x_pos, _y_pos[4])

        self.txtMTBFI.set_text(str(fmt.format(self._model.lst_i_mtbfi[0])))
        self.txtMTBFF.set_text(str(fmt.format(self._model.lst_i_mtbff[0])))
        self.txtTestTime.set_text(
            str(fmt.format(self._model.lst_p_test_time[0])))
        self.txtNFailures.set_text(
            str(fmt.format(self._model.lst_i_n_failures[0])))

        self.show_all()

        self.run()

    def _calculate(self, __button, __event):
        """
        Method to calculate the lower and upper bounds on the mean time to
        first fix.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() associated with the
                                      gtk.Button() that was pressed.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'g}'

        _mtbfi = float(self.txtMTBFI.get_text())
        _mtbff = float(self.txtMTBFF.get_text())
        _test_time = float(self.txtTestTime.get_text())
        _n_failures = float(self.txtNFailures.get_text())

        _mtbfa = CrowAMSAA.calculate_average_mtbf(_test_time, _n_failures,
                                                  _mtbfi, _mtbff)
        self._entry.set_text(str(fmt.format(_mtbfa)))

        self._model.lst_i_mtbfi[0] = _mtbfi
        self._model.lst_i_mtbfa[0] = _mtbfa
        self._model.lst_i_mtbff[0] = _mtbff
        self._model.lst_p_test_time[0] = _test_time
        self._model.lst_i_n_failures[0] = _n_failures

        self.destroy()

        return False

    def _cancel(self, __button, __event):
        """
        Method to destroy the assistant when the 'Cancel' button is
        pressed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() associated with the
                                      gtk.Button() that was pressed.
        """

        self.destroy()


class MTTFFCalculator(gtk.Dialog):
    """
    This is the assistant that calculate the mean time to first failure for
    a Reliability Growth program.
    """

    def __init__(self):
        """
        Initialize on instance of the MTTFF Assistant.

        :param :py:class:`rtk.testing.growth.Growth` controller: the Growth
                                                                 data
                                                                 controller.
        """

        gtk.Dialog.__init__(self, title=_(u"RTK Mean Time to First Fix "
                                          u"Assistant"),
                            parent=None,
                            flags=(gtk.DIALOG_MODAL |
                                   gtk.DIALOG_DESTROY_WITH_PARENT),
                            buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                                     gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        self.txtMTBFI = Widgets.make_entry(width=100)
        self.txtNItems = Widgets.make_entry(width=100)
        self.txtHrsWkItem = Widgets.make_entry(width=100)
        self.txtA = Widgets.make_entry(width=100)
        self.txtM = Widgets.make_entry(width=100)
        self.txtB = Widgets.make_entry(width=100)
        self.txtConfidence = Widgets.make_entry(width=100)

        self.txtMTTFF = Widgets.make_entry(width=100, editable=False)
        self.txtTTFFLL = Widgets.make_entry(width=100, editable=False)
        self.txtTTFFUL = Widgets.make_entry(width=100, editable=False)

        # Connect the buttons to callback methods.
        self.get_action_area().get_children()[0].connect('button-release-event',
                                                         self._cancel)
        self.get_action_area().get_children()[1].connect('button-release-event',
                                                         self._calculate)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the dialog.                       #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()
        self.vbox.pack_start(_fixed)        # pylint: disable=E1101

        _labels = [_(u"Starting MTBF:"), _(u"No. of Test Articles:"),
                   _(u"Average Hours/Week/Article:"),
                   _(u"Min. Time to Implement First Fix:"),
                   _(u"Likely Time to Implement First Fix:"),
                   _(u"Max. Time to Implement First Fix:"),
                   _(u"Confidence:"), _(u"Expected Time to First Failure:"),
                   _(u"Cumulative Test Time to First Fix:")]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, 5)
        _x_pos += 55

        _fixed.put(self.txtMTBFI, _x_pos, _y_pos[0])
        _fixed.put(self.txtNItems, _x_pos, _y_pos[1])
        _fixed.put(self.txtHrsWkItem, _x_pos, _y_pos[2])
        _fixed.put(self.txtA, _x_pos, _y_pos[3])
        _fixed.put(self.txtM, _x_pos, _y_pos[4])
        _fixed.put(self.txtB, _x_pos, _y_pos[5])
        _fixed.put(self.txtConfidence, _x_pos, _y_pos[6])

        _fixed.put(self.txtMTTFF, _x_pos, _y_pos[7])
        _fixed.put(self.txtTTFFLL, _x_pos, _y_pos[8])
        _fixed.put(self.txtTTFFUL, _x_pos + 105, _y_pos[8])

        self.show_all()

        self.run()

    def _calculate(self, __button, __event):
        """
        Method to calculate the lower and upper bounds on the mean time to
        first fix.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() associated with the
                                      gtk.Button() that was pressed.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'g}'

        _mtbfi = float(self.txtMTBFI.get_text())
        _n_items = float(self.txtNItems.get_text())
        _hrs_wk_item = float(self.txtHrsWkItem.get_text())
        _a = float(self.txtA.get_text())
        _m = float(self.txtM.get_text())
        _b = float(self.txtB.get_text())
        _confidence = float(self.txtConfidence.get_text())

        if _confidence > 1.0:
            _conf = 1.0 - ((100.0 - _confidence) / 200.0)
        else:
            _conf = 1.0 - ((1.0 - _confidence) / 2.0)

        _mean_fix_time = (_a + 4.0 * _m + _b) / 6.0
        _sd_fix_time = (_b - _a) / 6.0
        _fix_timell = _mean_fix_time - norm.ppf(_conf) * _sd_fix_time
        _fix_timeul = _mean_fix_time + norm.ppf(_conf) * _sd_fix_time

        _mttff = _mtbfi / _n_items
        _ttffll = ((_fix_timell + (7.0 * _mtbfi) /
                    (_n_items * _hrs_wk_item)) *
                   _hrs_wk_item * _n_items) / 7.0
        _ttfful = ((_fix_timeul + (7.0 * _mtbfi) /
                    (_n_items * _hrs_wk_item)) *
                   _hrs_wk_item * _n_items) / 7.0

        self.txtMTTFF.set_text(str(fmt.format(_mttff)))
        self.txtTTFFLL.set_text(str(fmt.format(_ttffll)))
        self.txtTTFFUL.set_text(str(fmt.format(_ttfful)))

        return False

    def _cancel(self, __button, __event):
        """
        Method to destroy the assistant when the 'Cancel' button is
        pressed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() associated with the
                                      gtk.Button() that was pressed.
        """

        self.destroy()


class AddRGRecord(gtk.Assistant):
    """
    This is the gtk.Assistant() that walks the user through the process of
    adding a test record to the currently selected test plan in the open
    RTK Program database.
    """

    _labels = [_(u"Date:"), _(u"Test Time:"), _(u"Number of Failures:")]

    def __init__(self, controller, model, listview):
        """
        Method to initialize the Reliability Growth Record Add Assistant.
        """

        gtk.Assistant.__init__(self)

        self.set_position(gtk.WIN_POS_CENTER)

        self.set_title(_(u"RTK Reliability Growth Record Assistant"))
        self.connect('apply', self._add_test_record)
        self.connect('cancel', self._cancel)
        self.connect('close', self._cancel)

        self._dtcGrowth = controller
        self._testing_model = model
        self._listview = listview

        # ----------------------------------------------------------------- #
        # Create the introduction page.                                     #
        # ----------------------------------------------------------------- #
        _fixed = gtk.Fixed()
        _label = Widgets.make_label(_(u"This is the RTK reliability growth "
                                      u"record assistant.  It will help you "
                                      u"add a record for tracking against the "
                                      u"currently selected reliability growth "
                                      u"plan.  Press 'Forward' to continue or "
                                      u"'Cancel' to quit the assistant."),
                                    width=600, height=-1, wrap=True)
        _fixed.put(_label, 5, 5)
        self.append_page(_fixed)
        self.set_page_type(_fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.set_page_title(_fixed, _(u"Introduction"))
        self.set_page_complete(_fixed, True)

        # ----------------------------------------------------------------- #
        # Create the page to gather the necessary inputs.                   #
        # ----------------------------------------------------------------- #
        _fixed = gtk.Fixed()

        _frame = Widgets.make_frame(label=_(""))
        _frame.set_shadow_type(gtk.SHADOW_NONE)
        _frame.add(_fixed)

        # Create the gtk.Combo that allow one of multiple selections.
        self.txtDate = Widgets.make_entry(width=100)
        self.txtDate.set_tooltip_text(_(u"Date test record was generated.  "
                                        u"This is not necessarily the date "
                                        u"the record is being added."))
        self.btnDate = Widgets.make_button(height=25, width=25, label="...",
                                           image=None)
        self.btnDate.connect('button-release-event', Utilities.date_select,
                             self.txtDate)
        self.txtTime = Widgets.make_entry()
        self.txtTime.set_tooltip_text(_(u"Test time."))
        self.chkAdditional = Widgets.make_check_button(_(u"Additional"))
        self.chkAdditional.set_tooltip_text(_(u"If checked, the test time is "
                                              u"additional test time.  If "
                                              u"unchecked, the test time is "
                                              u"cumulative since the start of "
                                              u"testing."))
        self.chkAdditional.set_active(False)
        self.txtNumFails = Widgets.make_entry()
        self.txtNumFails.set_tooltip_text(_(u"Number of failures observed."))
        self.txtNumFails.set_text("1")

        _label = Widgets.make_label(self._labels[0], 150, 25)
        _fixed.put(_label, 5, 5)
        _fixed.put(self.txtDate, 160, 5)
        _fixed.put(self.btnDate, 260, 5)

        _label = Widgets.make_label(self._labels[1], 150, 25)
        _fixed.put(_label, 5, 40)
        _fixed.put(self.txtTime, 160, 40)
        _fixed.put(self.chkAdditional, 365, 40)

        _label = Widgets.make_label(self._labels[2], 150, 25)
        _fixed.put(_label, 5, 75)
        _fixed.put(self.txtNumFails, 160, 75)

        self.append_page(_frame)
        self.set_page_type(_frame, gtk.ASSISTANT_PAGE_CONTENT)
        self.set_page_title(_frame, _(u"Enter Reliability Growth Data"))
        self.set_page_complete(_frame, True)

        # ----------------------------------------------------------------- #
        # Create the page to apply the import criteria.                     #
        # ----------------------------------------------------------------- #
        _fixed = gtk.Fixed()
        _text = _(u"Press 'Apply' to add the record or 'Cancel' to quit the "
                  u"assistant without adding the record.")
        _label = Widgets.make_label(_text, width=500, height=-1, wrap=True)
        _fixed.put(_label, 5, 5)
        self.append_page(_fixed)
        self.set_page_type(_fixed, gtk.ASSISTANT_PAGE_CONFIRM)
        self.set_page_title(_fixed, _(u"Add Reliability Growth Record"))
        self.set_page_complete(_fixed, True)

        self.show_all()

    def _add_test_record(self, __button):
        """
        Method to add a new test record for the selected test plan to the
        open RTK Program.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _test_id = self._testing_model.test_id
        _date = datetime.strptime(self.txtDate.get_text(),
                                  '%Y-%m-%d').toordinal()
        _time = float(self.txtTime.get_text())
        _n_failures = int(self.txtNumFails.get_text())
        _additional = self.chkAdditional.get_active()

        (_results,
         _error_code) = self._dtcGrowth.add_test_record(_test_id, _date, _time,
                                                        _n_failures,
                                                        _additional)

        if _results:
            self._listview.load_rg_assessment_details()

        return False

    def _cancel(self, __button):
        """
        Method to destroy the gtk.Assistant() when the 'Cancel' button is
        pressed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        """

        self.destroy()
