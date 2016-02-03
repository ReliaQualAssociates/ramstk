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
    import Configuration as _conf
    import Utilities as _util
    import gui.gtk.Widgets as _widg
except ImportError:
    import rtk.Configuration as _conf
    import rtk.Utilities as _util
    import rtk.gui.gtk.Widgets as _widg

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


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

        self.txtMTBFI = _widg.make_entry(width=100)
        self.txtNItems = _widg.make_entry(width=100)
        self.txtHrsWkItem = _widg.make_entry(width=100)
        self.txtA = _widg.make_entry(width=100)
        self.txtM = _widg.make_entry(width=100)
        self.txtB = _widg.make_entry(width=100)
        self.txtConfidence = _widg.make_entry(width=100)

        self.txtMTTFF = _widg.make_entry(width=100, editable=False)
        self.txtTTFFLL = _widg.make_entry(width=100, editable=False)
        self.txtTTFFUL = _widg.make_entry(width=100, editable=False)

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
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5)
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

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

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

    def __init__(self, controller, model):
        """
        Method to initialize the Reliability Growth Record Add Assistant.
        """

        gtk.Assistant.__init__(self)

        self.set_position(gtk.WIN_POS_CENTER)

        self.set_title(_(u"RTK Reliability Growth Record Assistant"))
        self.connect('apply', self._add_test_record)
        self.connect('cancel', self._cancel)
        self.connect('close', self._cancel)

        self._dao = controller._dao
        self._testing_model = model

        # ----------------------------------------------------------------- #
        # Create the introduction page.                                     #
        # ----------------------------------------------------------------- #
        _fixed = gtk.Fixed()
        _label = _widg.make_label(_(u"This is the RTK reliability growth "
                                    u"record assistant.  It will help you add "
                                    u"a record for tracking against the "
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

        _frame = _widg.make_frame(label=_(""))
        _frame.set_shadow_type(gtk.SHADOW_NONE)
        _frame.add(_fixed)

        # Create the gtk.Combo that allow one of multiple selections.
        self.txtDate = _widg.make_entry(width=100)
        self.txtDate.set_tooltip_text(_(u"Date test record was generated.  "
                                        u"This is not necessarily the date "
                                        u"the record is being added."))
        self.btnDate = _widg.make_button(height=25, width=25, label="...",
                                         image=None)
        self.btnDate.connect('button-release-event', _util.date_select,
                             self.txtDate)
        self.txtTime = _widg.make_entry()
        self.txtTime.set_tooltip_text(_(u"Test time."))
        self.chkAdditional = _widg.make_check_button(_(u"Additional"))
        self.chkAdditional.set_tooltip_text(_(u"If checked, the test time is "
                                              u"additional test time.  If "
                                              u"unchecked, the test time is "
                                              u"cumulative since the start of "
                                              u"testing."))
        self.chkAdditional.set_active(False)
        self.txtNumFails = _widg.make_entry()
        self.txtNumFails.set_tooltip_text(_(u"Number of failures observed."))
        self.txtNumFails.set_text("1")

        _label = _widg.make_label(self._labels[0], 150, 25)
        _fixed.put(_label, 5, 5)
        _fixed.put(self.txtDate, 160, 5)
        _fixed.put(self.btnDate, 260, 5)

        _label = _widg.make_label(self._labels[1], 150, 25)
        _fixed.put(_label, 5, 40)
        _fixed.put(self.txtTime, 160, 40)
        _fixed.put(self.chkAdditional, 365, 40)

        _label = _widg.make_label(self._labels[2], 150, 25)
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
        _label = _widg.make_label(_text, width=500, height=-1, wrap=True)
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

        _query = "SELECT MAX(fld_record_id), MAX(fld_right_interval) \
                  FROM rtk_survival_data \
                  WHERE fld_dataset_id=%d \
                  AND fld_source=1" % self._testing_model.test_id
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        if _results[0][0] is None or _results[0][0] == '':
            _last_id = 0
        else:
            _last_id = _results[0][0] + 1

        if _results[0][1] is None or _results[0][1] == '':
            _last_time = 0.0
        else:
            _last_time = float(_results[0][1])

        # Read the test time entered by the user.  If this is entered as
        # additional test time, calculate the cumulative test time.
        _time = float(self.txtTime.get_text())
        if self.chkAdditional.get_active():
            _time = _time + _last_time
        _n_fails = int(self.txtNumFails.get_text())

        _date = datetime.strptime(self.txtDate.get_text(),
                                  '%Y-%m-%d').toordinal()
        _query = "INSERT INTO rtk_survival_data \
                  (fld_record_id, fld_dataset_id, fld_left_interval, \
                   fld_right_interval, fld_quantity, fld_mode_type, \
                   fld_assembly_id, fld_failure_date, fld_source) \
                  VALUES ({0:d}, {1:d}, {2:f}, {3:f}, {4:d}, {5:d}, {6:d}, \
                          {7:d}, 1)".format(_last_id,
                                            self._testing_model.test_id, 0.0,
                                            _time, _n_fails, 0,
                                            self._testing_model.assembly_id,
                                            _date)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        self._testing_model.dic_test_data[_last_id] = [_date, 0.0, _time,
                                                       _n_fails]

        return False

    def _cancel(self, __button):
        """
        Method to destroy the gtk.Assistant() when the 'Cancel' button is
        pressed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        """

        self.destroy()
