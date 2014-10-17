#!/usr/bin/env python
"""
switch.py is the meta-class for all switch types.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       switch.py is part of The RTK Project
#
# All rights reserved.

import gettext
import locale
import pango

try:
    import rtk.configuration as _conf
    import rtk.widgets as _widg
except:
    import configuration as _conf
    import widgets as _widg

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Switch(object):
    """
    Switches meta class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 14.
    """

    def __init__(self):
        """
        Initializes the Switches Component Class.
        """

        self.category = 7                   # Category in the rtkcom database.
        self.reason = ''

        # Label text for input data.
        self._in_labels = [_(u"Application:"),
                           _(u"Cycling Rate (cycles/hour):"),
                           _(u"Rated Current (A):"),
                           _(u"Operating Current (A):")]

        # Label text for output data.
        self._out_labels = ["", u"\u03BB<sub>b</sub>:",
                            u"\u03C0<sub>E</sub>:"]

        # Derating points for the derating curve.  The list at position 0 is
        # for severe environments.  The list at position 1 is for benign
        # environments.
        self._derate_criteria = [[0.6, 0.6, 0.0], [0.9, 0.9, 0.0]]

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the widgets
        needed to select inputs for Switches Component Class prediction
        calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: (_x_pos, _y_pos); the x-coordinate and list of y-coordinates.
        :rtype: tuple
        """

        # Clear all the display widgets from the gtk.Fixed() except the
        # calculation model gtk.Label() and gtk.ComboBox().
        for _child in layout.get_children()[2:]:
            layout.remove(_child)

        # Create the input widgets.
        part.cmbApplication = _widg.make_combo(simple=True)
        part.txtCycleRate = _widg.make_entry(width=100)
        part.txtCurrentRated = _widg.make_entry(width=100)
        part.txtCurrentOper = _widg.make_entry(width=100)

        # Load the gtk.ComboBox().
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._in_labels, layout, 5, y_pos)

        # Place the input widgets.
        layout.put(part.cmbApplication, _x_pos, _y_pos[0])
        layout.put(part.txtCycleRate, _x_pos, _y_pos[1])
        layout.put(part.txtCurrentRated, _x_pos, _y_pos[2])
        layout.put(part.txtCurrentOper, _x_pos, _y_pos[3])

        # Connect to callback methods.
        part.cmbApplication.connect("changed", self._callback_combo, part, 5)
        part.txtCycleRate.connect("focus-out-event", self._callback_entry,
                                  part, "float", 19)
        part.txtCurrentRated.connect("focus-out-event", self._callback_entry,
                                     part, "float", 92)
        part.txtCurrentOper.connect("focus-out-event", self._callback_entry,
                                    part, "float", 62)

        layout.show_all()

        return _x_pos, _y_pos

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the widgets to
        display Switches Component Class calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: (_x_pos, _y_pos); the x-coordinate and list of y-coordinates.
        :rtype: tuple
        """

        # Clear all the display widgets from the gtk.Fixed().
        for _child in layout.get_children()[20:]:
            layout.remove(_child)

        # Create the reliability result display widgets.
        part.txtLambdaB = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        part.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)

        # Create and place all the labels.
        (_x_pos, _y_pos) = _widg.make_labels(self._out_labels,
                                             layout, x_pos, y_pos)
        _x_pos += x_pos
        _x_pos -= 30

        # Place the reliability result display widgets.
        layout.put(part.txtLambdaB, _x_pos, _y_pos[1])
        layout.put(part.txtPiE, _x_pos, _y_pos[2])

        layout.show_all()

        return _x_pos, _y_pos

    def stress_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook stress calculation results tab with the
        widgets to display Switch Component Class stress results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the widgets.
        :param int y_pos: the y position of the first widget.
        :return: (_x_pos, _y_pos); the x-coordinate and list of y-coordinates.
        :rtype: tuple
        """

        # Clear all the display widgets from the gtk.Fixed().
        for _child in layout.get_children()[16:]:
            layout.remove(_child)

        # Create and place all the labels.
        # (_x_pos, _y_pos) = _widg.make_labels(self._out_labels[:2], layout,
        #                                      5, y_pos)

        # Create the stress result display widgets.
        # part.txtTRise = _widg.make_entry(width=100, editable=False, bold=True)
        # part.txtTJunc = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the stress result display widgets.
        # layout.put(part.txtTRise, _x_pos, _y_pos[0])
        # layout.put(part.txtTJunc, _x_pos, _y_pos[1])

        part.graDerate.set_title(_(u"Derating Curve for %s at %s") %
                                 (part.txtPartNum.get_text(),
                                  part.txtRefDes.get_text()))
        part.graDerate.set_xlabel(_(u"Temperature (\u2070C)"))
        part.graDerate.set_ylabel(_(u"Voltage Derating Factor"))

        layout.show_all()

        # return _x_pos, _y_pos
        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with calculation input
        information.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: (_model, _row); the Parts List gtk.Treemodel and selected
                 gtk.TreeIter()
        :rtype: tuple
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        part.cmbApplication.set_active(int(_model.get_value(_row, 5)))
        part.txtCycleRate.set_text(str(fmt.format(_model.get_value(_row, 19))))
        part.txtCurrentRated.set_text(str(fmt.format(
            _model.get_value(_row, 92))))
        part.txtCurrentOper.set_text(str(fmt.format(
            _model.get_value(_row, 62))))

        return _model, _row

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with calculation
        results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: (_model, _row); the Parts List gtk.Treemodel and selected
                 gtk.TreeIter()
        :rtype: tuple
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        part.txtLambdaB.set_text(str(fmt.format(_model.get_value(_row, 46))))
        part.txtPiE.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 72))))

        part.txtOSReason.set_text(self.reason)

        part.graDerate.cla()

        return _model, _row

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Switches Component Class gtk.ComboBox()
        changes.

        :param gtk.ComboBox combo: the gtk.ComboBox() calling this method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param int idx: the user-defined index for the calling combobx.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        _index = combo.get_active()

        # Update the Component object property and the Parts List treeview.
        _model.set_value(_row, idx, int(_index))

        return False

    def _callback_entry(self, entry, event, part, convert, idx):
        """
        Callback function for handling Switches Component Class gtk.Entry()
        changes.

        :param gtk.Entry entry: the gtk.Entry() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param str convert: the data type to convert the gtk.Entry() contents.
        :param int idx: the position in the Component property array
                        associated with the data from the gtk.Entry() that
                        called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        # Update the Component object property.
        if convert == "text":
            _model.set_value(_row, idx, entry.get_text())

        elif convert == "int":
            _model.set_value(_row, idx, int(entry.get_text()))

        elif convert == "float":
            _model.set_value(_row, idx, float(entry.get_text()))

        # Commercial PiQ entry called the function.
        if idx == 79:
            CpiQ = float(entry.get_text())

            # Use this value for piQ if it is greater than zero.
            if CpiQ > 0:
                _model.set_value(_row, 79, CpiQ)

        return False
