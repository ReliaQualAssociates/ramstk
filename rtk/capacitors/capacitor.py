#!/usr/bin/env python
"""
Capacitor is the meta class for all capacitor types.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       capacitor.py is part of the RTK Project
#
# All rights reserved.

import pango
import locale
import gettext

try:
    import rtk.configuration as _conf
    import rtk.widgets as _widg
except:
    import configuration as _conf
    import widgets as _widg

# Add localization support.
_ = gettext.gettext

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')


class Capacitor(object):
    """
    This is the Capacitor meta class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.
    """

    def __init__(self):
        """
        Initializes the Capacitor Class.
        """

        self._ready = False
        self.category = 4                   # Category in rtkcom database.
        self.reason = ""

        # Label text for input data.
        self._in_labels = [_(u"Quality:"), (u"\u03C0<sub>Q</sub> Override:"),
                           _(u"Specification:"), _(u"Spec. Sheet:"),
                           _(u"Rated Voltage:"), _(u"Applied DC Voltage:"),
                           _(u"Applied AC Voltage:"), _(u"Capacitance (F):")]

        # Label text for output data.
        self._out_labels = [_(u"Temp Rise (\u2070C):"),
                            _(u"Junction Temp (\u2070C):"), (""),
                            u"\u03BB<sub>b</sub>:", u"\u03C0<sub>Q</sub>:",
                            u"\u03C0<sub>E</sub>:", u"\u03C0<sub>CV</sub>:"]

        # Derating points for the derating curve.  The list at position 0 is
        # for severe environments.  The list at position 1 is for benign
        # environments.
        self._derate_criteria = [[0.6, 0.6, 0.0], [0.9, 0.9, 0.0]]

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the widgets
        needed to select inputs for Capacitor Component Class prediction
        calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Create the input widgets.
        part.cmbQuality = _widg.make_combo(simple=True)
        part.cmbSpecification = _widg.make_combo(simple=True)
        part.cmbSpecSheet = _widg.make_combo(simple=True)

        part.txtCommercialPiQ = _widg.make_entry(width=100)
        part.txtVoltRated = _widg.make_entry(width=100)
        part.txtVoltApplied = _widg.make_entry(width=100)
        # Create the applied voltage entry.  We store this in the
        # Operating power field in the program database.
        part.txtACVoltApplied = _widg.make_entry(width=100)
        part.txtCapacitance = _widg.make_entry(width=100)

        # Populate the gtk.ComboBox().
        for i in range(len(self._quality)):
            part.cmbQuality.insert_text(i, self._quality[i])
        for i in range(len(self._specification)):
            part.cmbSpecification.insert_text(i, self._specification[i])

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._in_labels, layout, 5, y_pos)

        # Place the input widgets.
        layout.put(part.cmbQuality, x_pos, _y_pos[0])
        layout.put(part.txtCommercialPiQ, x_pos, _y_pos[1])
        layout.put(part.cmbSpecification, x_pos, _y_pos[2])
        layout.put(part.cmbSpecSheet, x_pos, _y_pos[3])
        layout.put(part.txtVoltRated, x_pos, _y_pos[4])
        layout.put(part.txtVoltApplied, x_pos, _y_pos[5])
        layout.put(part.txtACVoltApplied, x_pos, _y_pos[6])
        layout.put(part.txtCapacitance, x_pos, _y_pos[7])

        # Connect signals to callback functions.
        part.cmbQuality.connect('changed', self._callback_combo, part, 85)
        part.cmbSpecification.connect('changed', self._callback_combo, part,
                                      101)
        part.cmbSpecSheet.connect('changed', self._callback_combo, part, 102)

        part.txtCommercialPiQ.connect('focus-out-event', self._callback_entry,
                                      part, 'float', 79)
        part.txtVoltRated.connect('focus-out-event', self._callback_entry,
                                  part, 'float', 94)
        part.txtVoltApplied.connect('focus-out-event', self._callback_entry,
                                    part, 'float', 66)
        part.txtACVoltApplied.connect('focus-out-event', self._callback_entry,
                                      part, 'float', 64)
        part.txtCapacitance.connect('focus-out-event', self._callback_entry,
                                    part, 'float', 15)

        layout.show_all()

        return _y_pos[2]

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with calculation
        input information.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        part.cmbQuality.set_active(int(_model.get_value(_row, 85)))
        part.cmbSpecification.set_active(int(_model.get_value(_row, 101)))
        part.cmbSpecSheet.set_active(int(_model.get_value(_row, 102)))
        part.txtVoltRated.set_text(str(fmt.format(_model.get_value(_row, 94))))
        part.txtVoltApplied.set_text(str(fmt.format(_model.get_value(_row, 66))))
        part.txtACVoltApplied.set_text(str(fmt.format(_model.get_value(_row, 64))))
        part.txtCapacitance.set_text(str(fmt.format(_model.get_value(_row, 15))))

        if int(_model.get_value(_row, 85)) != 0:
            part.txtCommercialPiQ.set_text(str(fmt.format(_model.get_value(_row, 79))))
        else:
            part.txtCommercialPiQ.set_text("0.0")

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook reliability calculation results tab with
        the widgets to display Capacitor Component Class results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Create and place all the labels.
        (_x_pos, _y_pos) = _widg.make_labels(self._out_labels[2:],
                                             layout, x_pos, y_pos)
        _x_pos += x_pos
        _x_pos -= 30

        part.txtLambdaB = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        part.txtPiQ = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)
        # Create the Pi CV results entry.  We store the Pi CV value in the
        # pi_cf field in the program database.
        part.txtPiCV = _widg.make_entry(width=100, editable=False, bold=True)

        layout.put(part.txtLambdaB, _x_pos, _y_pos[1])
        layout.put(part.txtPiQ, _x_pos, _y_pos[2])
        layout.put(part.txtPiE, _x_pos, _y_pos[3])
        layout.put(part.txtPiCV, _x_pos, _y_pos[4])

        layout.show_all()

        return _y_pos[4]

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
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Create and place all the labels.
        (__, _y_pos) = _widg.make_labels(self._out_labels[:2], layout,
                                         5, y_pos)

        part.txtTRise = _widg.make_entry(width=100, editable=False, bold=True)
        layout.put(part.txtTRise, x_pos, _y_pos[0])

        part.txtTJunc = _widg.make_entry(width=100, editable=False, bold=True)
        layout.put(part.txtTJunc, x_pos, _y_pos[1])

        part.graDerate.set_title(_(u"Derating Curve for %s at %s") %
                                 (part.txtPartNum.get_text(),
                                  part.txtRefDes.get_text()))
        part.graDerate.set_xlabel(_(u"Temperature (\u2070C)"))
        part.graDerate.set_ylabel(_(u"Voltage Derating Factor"))

        layout.show_all()

        self._ready = True

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with calculation
        results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        part.txtCurrentRatio.set_text(str(fmt.format(_model.get_value(_row, 17))))
        part.txtTJunc.set_text(str(fmt.format(_model.get_value(_row, 39))))
        part.txtLambdaB.set_text(str(fmt.format(_model.get_value(_row, 46))))
        part.txtPiCV.set_text(str(fmt.format(_model.get_value(_row, 70))))
        part.txtPiE.set_text(str('{0:0.2g}'.format(_model.get_value(_row, 72))))
        part.txtPiQ.set_text(str('{0:0.2g}'.format(_model.get_value(_row, 79))))
        part.txtTRise.set_text(str(fmt.format(_model.get_value(_row, 107))))
        part.txtVoltageRatio.set_text(str(fmt.format(_model.get_value(_row, 111))))

        part.txtOSReason.set_text(self.reason)

        part.graDerate.cla()

        # Plot the derating curve and operating point.
        _x_ = [float(part.min_temp), float(part.knee_temp),
               float(part.max_temp)]

        _voltage_ratio = part.op_voltage / part.rated_voltage
        part.graDerate.plot(_x_, self._derate_criteria[0], 'r.-', linewidth=2)
        part.graDerate.plot(_x_, self._derate_criteria[1], 'b.-', linewidth=2)
        part.graDerate.plot(part.temperature_active, _voltage_ratio, 'go')
        if(_x_[0] != _x_[2] and
           self._derate_criteria[1][0] != self._derate_criteria[1][2]):
            part.graDerate.axis([0.95 * _x_[0],
                                 1.05 * _x_[2],
                                 self._derate_criteria[1][2],
                                 1.05 * self._derate_criteria[1][0]])
        else:
            part.graDerate.axis([0.95, 1.05, 0.0, 1.05])

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Capacitor Class gtk.ComboBox() changes.

        :param gtk.ComboBox combo: the gtk.ComboBox() calling this method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param int idx: the user-defined index for the calling combobx.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        _index = combo.get_active()

        # Update the Component class property and the Parts List treeview.
        _model.set_value(_row, idx, int(_index))

        if idx == 85:                       # Quality
            if part.txtCommercialPiQ.get_text() == "":
                CpiQ = 0.0
            else:
                CpiQ = float(part.txtCommercialPiQ.get_text())
                _model.set_value(_row, 79, CpiQ)

            # Use this value for piQ if not being over-ridden.
            if CpiQ <= 0.0:
                _model.set_value(_row, 79, self._piQ[_index - 1])

        elif idx == 101:                    # Specification
            part.cmbSpecSheet.get_model().clear()
            for i in range(len(self._specsheet[_index - 1])):
                part.cmbSpecSheet.insert_text(i,
                                              self._specsheet[_index - 1][i])

        return False

    def _callback_entry(self, entry, __event, part, convert, idx):
        """
        Callback function for handling Capacitor Class gtk.Entry() changes.

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
        :rtype: bool
        """

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        # Update the Component object property.
        if convert == 'text':
            _model.set_value(_row, idx, entry.get_text())

        elif convert == 'int':
            _model.set_value(_row, idx, int(entry.get_text()))

        elif convert == 'float':
            _model.set_value(_row, idx, float(entry.get_text()))

        # Commercial PiQ entry called the function.
        if idx == 79:
            CpiQ = float(entry.get_text())

            # Use this value for piQ if it is greater than zero.
            if CpiQ > 0:
                _model.set_value(_row, 79, CpiQ)

        return False
