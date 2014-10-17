#!/usr/bin/env python
"""
resistor.py is the meta-class for all resistor types.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       resistor.py is part of The RTK Project
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


class Resistor(object):
    """
    Resistor meta class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.
    """

    def __init__(self):
        """
        Initializes the Resistor Component Class.
        """

        self._ready = False
        self.category = 3                   # Category in the rtkcom database.
        self.reason = ""

        # Label text for input data.
        self._in_labels = [_(u"Quality:"), _(u"\u03C0<sub>Q</sub> Override:"),
                           _(u"Resistance Range (\u03A9):"),
                           _(u"Rated Power (W):")]

        # Label text for output data.
        self._out_labels = [_(u"Temp Rise (\u2070C):"),
                            _(u"Junction Temp (\u2070C):"), "",
                            u"\u03BB<sub>b</sub>:", u"\u03C0<sub>Q</sub>:",
                            u"\u03C0<sub>E</sub>:", u"\u03C0<sub>R</sub>:"]

        # Derating points for the derating curve.  The list at position 0 is
        # for severe environments.  The list at position 1 is for benign
        # environments.
        self._derate_criteria = [[0.6, 0.6, 0.0], [0.9, 0.9, 0.0]]

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Resistor Component Class
        prediction calculations.

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
        part.cmbQuality = _widg.make_combo(simple=True)
        part.txtCommercialPiQ = _widg.make_entry(width=100)
        part.cmbRRange = _widg.make_combo(simple=True)
        part.txtPwrRated = _widg.make_entry(width=100)

        # Load all the gtk.ComboBox().
        for i in range(len(self._quality)):
            part.cmbQuality.insert_text(i, self._quality[i])
        for i in range(len(self._range)):
            part.cmbRRange.insert_text(i, self._range[i])

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._in_labels, layout, 5, y_pos)
        _x_pos = max(x_pos, _x_pos)
        _x_pos += 35

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.put(part.cmbQuality, _x_pos, _y_pos[0])
        layout.put(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.put(part.cmbRRange, _x_pos, _y_pos[2])
        layout.put(part.txtPwrRated, _x_pos, _y_pos[3])

        # Connect to callback methods.
        part.cmbQuality.connect("changed", self._callback_combo, part, 85)
        part.txtCommercialPiQ.connect("focus-out-event", self._callback_entry,
                                      part, "float", 79)
        part.cmbRRange.connect("changed", self._callback_combo, part, 96)
        part.txtPwrRated.connect("focus-out-event", self._callback_entry,
                                 part, "float", 93)

        layout.show_all()

        return _x_pos, _y_pos

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Resistor Component Class calculation results.

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
        part.txtPiQ = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiR = _widg.make_entry(width=100, editable=False, bold=True)

        # Create and place all the labels.
        (_x_pos, _y_pos) = _widg.make_labels(self._out_labels[2:],
                                             layout, x_pos, y_pos)
        _x_pos += x_pos
        _x_pos -= 30

        # Place the reliability result display widgets.
        layout.put(part.txtLambdaB, _x_pos, _y_pos[1])
        layout.put(part.txtPiQ, _x_pos, _y_pos[2])
        layout.put(part.txtPiE, _x_pos, _y_pos[3])
        layout.put(part.txtPiR, _x_pos, _y_pos[4])

        layout.show_all()

        return _x_pos, _y_pos

    def stress_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook stress calculation results tab with the
        widgets to display Capacitor Component Class stress results.

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

        # Create the stress resluts display widgets.
        part.txtTRise = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtTJunc = _widg.make_entry(width=100, editable=False, bold=True)

        # Create and place all the labels.
        (_x_pos, _y_pos) = _widg.make_labels(self._out_labels[:2],
                                             layout, 5, y_pos)
        _x_pos += x_pos
        _x_pos -= 30

        # Place the reliability result display widgets.
        layout.put(part.txtTRise, _x_pos, _y_pos[0])
        layout.put(part.txtTJunc, _x_pos, _y_pos[1])

        return _x_pos, _y_pos

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with
        calculation input information.

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

        part.cmbQuality.set_active(int(_model.get_value(_row, 85)))
        part.txtPwrRated.set_text(str(fmt.format(_model.get_value(_row, 93))))
        part.cmbRRange.set_active(int(_model.get_value(_row, 96)))
        if int(_model.get_value(_row, 85)) <= 0:
            part.txtCommercialPiQ.set_text(str(
                fmt.format(_model.get_value(_row, 79))))
        else:
            part.txtCommercialPiQ.set_text("0.0")

        return _model, _row

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

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

        part.txtTJunc.set_text(str(fmt.format(_model.get_value(_row, 39))))
        part.txtLambdaB.set_text(str(fmt.format(_model.get_value(_row, 46))))
        part.txtPiE.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 72))))
        part.txtPiQ.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 79))))
        part.txtPiR.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 80))))
        part.txtTRise.set_text(str(fmt.format(_model.get_value(_row, 107))))

        part.txtOSReason.set_text(self.reason)

        part.graDerate.cla()

        return _model, _row

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Resistor Component Class ComboBox
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

        if idx == 85:                       # Quality
            if part.txtCommercialPiQ.get_text() == "":
                CpiQ = 0.0
            else:
                CpiQ = float(part.txtCommercialPiQ.get_text())

            # Use this value for piQ if not being over-ridden.
            if CpiQ <= 0.0:
                _model.set_value(_row, 79, self._piQ[_index - 1])

        elif idx == 96:                     # Resistance range
            _model.set_value(_row, 80, self._piR[_index - 1])

        return False

    def _callback_entry(self, entry, event, part, convert, idx):
        """
        Callback function for handling Inductive Device Class Entry
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
