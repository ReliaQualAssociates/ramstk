#!/usr/bin/env python
"""
ic.py is the meta-class for all integrated circuit types.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       ic.py is part of The RTK Project
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


class IntegratedCircuit(object):
    """
    The Integrated Circuit meta class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.
    """

    _quality = ["", u"S", u"B", u"B-1", _(u"Commercial")]
    _technology = ["", _(u"Bipolar"), u"CMOS"]
    _package = ["", _(u"Hermetic DIP"), _(u"Flatpack"), _(u"Can"),
                _(u"Non-Hermetic DIP")]

    def __init__(self):
        """
        Initializes the Integrated Circuit Component Class.
        """

        self._ready = False
        self.category = 1                   # Category ID in rtkcom database.
        self.reason = ""

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self.pi_Q_specified = 0.0
        self._piE = [0.5, 2.0, 4.0, 4.0, 6.0, 4.0, 5.0, 5.0, 8.0, 8.0, 0.5,
                     5.0, 12.0, 220.0]
        self._piQ = [0, 0.25, 1.0, 2.0, 10.0]
        self._Tcase = [35, 45, 50, 45, 50, 60, 60, 75, 75, 60, 35, 50, 60, 45]
        self._thetaJC = [28, 20, 20, 28, 22, 70, 28, 20, 20]
        self._K5 = [0.00028, 0.00009, 0.00003, 0.00003, 0.00036]
        self._K6 = [1.08, 1.51, 1.82, 2.01, 1.08]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        # Label text for input data.
        self._in_labels = [_(u"Quality:"), _(u"\u03C0<sub>Q</sub> Override:"),
                           _(u"Technology:"), _(u"# of Elements:"),
                           _(u"Package Type:"), _(u"# of Pins:"),
                           _(u"Years in Production:")]

        # Label text for output data.
        self._out_labels = [_(u"Temp Rise (\u2070C):"),
                            _(u"Junction Temp (\u2070C):"), (""),
                            u"C<sub>1</sub>:", u"\u03C0<sub>T</sub>:",
                            u"C<sub>2</sub>:", u"\u03C0<sub>E</sub>:",
                            u"\u03C0<sub>Q</sub>:", u"\u03C0<sub>L</sub>:"]

        # Derating points for the derating curve.  The list at position 0 is
        # for severe environments.  The list at position 1 is for benign
        # environments.
        self._derate_criteria = [[0.6, 0.6, 0.0], [0.9, 0.9, 0.0]]

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Integrated Circuit prediction
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
        part.cmbQuality = _widg.make_combo(simple=True)
        part.txtCommercialPiQ = _widg.make_entry(width=100)
        part.cmbTechnology = _widg.make_combo(simple=True)
        part.cmbElements = _widg.make_combo(simple=True)
        part.cmbPackage = _widg.make_combo(simple=True)
        part.txtNumPins = _widg.make_entry(width=100)
        part.txtYears = _widg.make_entry(width=100)

        # Load all the gtk.ComboBox().
        for i in range(len(self._quality)):
            part.cmbQuality.insert_text(i, self._quality[i])
        for i in range(len(self._technology)):
            part.cmbTechnology.insert_text(i, self._technology[i])
        for i in range(len(self._package)):
            part.cmbPackage.insert_text(i, self._package[i])

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._in_labels, layout, 5, y_pos)

        # Place the input widgets.
        layout.put(part.cmbQuality, _x_pos, _y_pos[0])
        layout.put(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.put(part.cmbTechnology, _x_pos, _y_pos[2])
        layout.put(part.cmbElements, _x_pos, _y_pos[3])
        layout.put(part.cmbPackage, _x_pos, _y_pos[4])
        layout.put(part.txtNumPins, _x_pos, _y_pos[5])
        layout.put(part.txtYears, _x_pos, _y_pos[6])

        # Connect to callback methods.
        part.cmbQuality.connect("changed", self._callback_combo, part, 85)
        part.cmbTechnology.connect("changed", self._callback_combo, part, 104)
        part.cmbElements.connect("changed", self._callback_combo, part, 24)
        part.cmbPackage.connect("changed", self._callback_combo, part, 67)
        part.txtCommercialPiQ.connect("focus-out-event", self._callback_entry,
                                      part, "float", 79)
        part.txtNumPins.connect("focus-out-event", self._callback_entry,
                                part, "int", 60)
        part.txtYears.connect("focus-out-event", self._callback_entry,
                              part, "int", 112)

        layout.show_all()

        return _x_pos, _y_pos

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Integrated Circuit reliability calculation results.

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
        part.txtC1 = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiT = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtC2 = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiQ = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiL = _widg.make_entry(width=100, editable=False, bold=True)

        # Create and place all the labels.
        (_x_pos, _y_pos) = _widg.make_labels(self._out_labels[2:],
                                             layout, x_pos, y_pos)
        _x_pos += x_pos
        _x_pos -= 30

        # Place the reliability result display widgets.
        layout.put(part.txtC1, _x_pos, _y_pos[1])
        layout.put(part.txtPiT, _x_pos, _y_pos[2])
        layout.put(part.txtC2, _x_pos, _y_pos[3])
        layout.put(part.txtPiE, _x_pos, _y_pos[4])
        layout.put(part.txtPiQ, _x_pos, _y_pos[5])
        layout.put(part.txtPiL, _x_pos, _y_pos[6])

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

        # Create and place all the labels.
        (_x_pos, _y_pos) = _widg.make_labels(self._out_labels[:2], layout,
                                             5, y_pos)

        # Create the stress result display widgets.
        part.txtTRise = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtTJunc = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the stress result display widgets.
        layout.put(part.txtTRise, _x_pos, _y_pos[0])
        layout.put(part.txtTJunc, _x_pos, _y_pos[1])

        part.graDerate.set_title(_(u"Derating Curve for %s at %s") %
                                 (part.txtPartNum.get_text(),
                                  part.txtRefDes.get_text()))
        part.graDerate.set_xlabel(_(u"Temperature (\u2070C)"))
        part.graDerate.set_ylabel(_(u"Voltage Derating Factor"))

        layout.show_all()

        return _x_pos, _y_pos

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with reliability
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

        part.txtNumPins.set_text(str("{0:0.0f}".format(
            _model.get_value(_row, 60))))
        part.cmbPackage.set_active(int(_model.get_value(_row, 67)))
        part.cmbQuality.set_active(int(_model.get_value(_row, 85)))
        part.cmbTechnology.set_active(int(_model.get_value(_row, 104)))
        part.txtYears.set_text(str("{0:0.0f}".format(
            _model.get_value(_row, 112))))

        if int(_model.get_value(_row, 85)) <= 0:
            part.txtCommercialPiQ.set_text(str(fmt.format(
                _model.get_value(_row, 79))))
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

        part.txtC1.set_text(str("{0:0.3g}".format(_model.get_value(_row, 8))))
        part.txtC2.set_text(str(fmt.format(_model.get_value(_row, 9))))
        part.txtTJunc.set_text(str(fmt.format(_model.get_value(_row, 39))))
        part.txtPiE.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 72))))
        part.txtPiQ.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 79))))
        part.txtPiL.set_text(str(fmt.format(_model.get_value(_row, 80))))
        part.txtPiT.set_text(str(fmt.format(_model.get_value(_row, 82))))
        part.txtTRise.set_text(str(fmt.format(_model.get_value(_row, 107))))

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

        return _model, _row

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Integrated Circuit Class
        gtk.ComboBox() changes.

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

        # The Number of Elements combobox called the function.
        if idx == 24:
            _index2 = part.cmbTechnology.get_active()
            _model.set_value(_row, 8, self._C1[_index2 - 1][_index - 1])

        # The Package Type combobox called the function.
        elif idx == 67:
            _model.set_value(_row, 35, self._K5[_index - 1])
            _model.set_value(_row, 36, self._K6[_index - 1])

        # The Quality combobox called the function.
        elif idx == 85:
            if part.txtCommercialPiQ.get_text() == "":
                CpiQ = 0.0
            else:
                CpiQ = float(part.txtCommercialPiQ.get_text())

            # Use this value for piQ if not being over-ridden.
            if CpiQ <= 0:
                _model.set_value(_row, 79, self._piQ[_index])

        # The Technology combobox called the function.
        elif idx == 104:
            _index2 = part.cmbElements.get_active()
            _model.set_value(_row, 8, self._C1[_index - 1][_index2 - 1])

        return False

    def _callback_entry(self, entry, event, part, convert, idx):
        """
        Callback function for handling Integrated Circuit Class gtk.Entry()
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
