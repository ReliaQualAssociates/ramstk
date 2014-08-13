#!/usr/bin/env python
"""
This is the Inductor meta-class.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       inductor.py is part of The RTK Project
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


class Inductor(object):
    """
    Inductive Devices meta class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 11.
    """

    def __init__(self):
        """
        Initializes the Inductive Devices Component Class.
        """

        self._ready = False
        self.category = 5                   # Category in rtkcom database.
        self.reason = ""

        # Label text for input data.
        self._in_labels = [_(u"Quality:"), _(u"\u03C0<sub>Q</sub> Override:"),
                           _(u"Insulation Class:"), _(u"Power Loss(W):"),
                           _(u"Input Power (W):"),
                           _(u"Radiating Surface Area (in\u00B2):"),
                           _(u"Transformer Weight (lbs):")]

        # Label text for output data.
        self._out_labels = [_(u"Temp. Rise (\u2070C):"),
                            _(u"Hot Spot Temp.:"), "",
                            u"\u03BB<sub>b</sub>:", u"\u03C0<sub>Q</sub>:",
                            u"\u03C0<sub>E</sub>:"]

        # Derating points for the derating curve.  The list at position 0 is
        # for severe environments.  The list at position 1 is for benign
        # environments.
        self._derate_criteria = [[0.6, 0.6, 0.0], [0.9, 0.9, 0.0]]

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Inductive Devices Component
        Class prediction calculations.

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

        # Create the input display widgets.
        part.cmbQuality = _widg.make_combo(simple=True)
        part.txtCommercialPiQ = _widg.make_entry(width=100)
        part.cmbInsulation = _widg.make_combo(simple=True)
        part.txtOperPwr = _widg.make_entry(width=100)
        # Create the input power entry.  We store this in the rated power
        # field in the program database.
        part.txtInputPwr = _widg.make_entry(width=100)
        # Create the transformer surface area entry.  We store this in the
        # L1 field in the program database.
        part.txtArea = _widg.make_entry(width=100)
        # Create the transformer weight entry.  We store this in the L2 field
        # in the program database.
        part.txtWeight = _widg.make_entry(width=100)

        # Populate all the gtk.ComboBox()
        for i in range(len(self._quality)):
            part.cmbQuality.insert_text(i, self._quality[i])
        for i in range(len(self._insulation)):
            part.cmbInsulation.insert_text(i, self._insulation[i])

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._in_labels, layout, 5, y_pos)

        layout.put(part.cmbQuality, _x_pos, _y_pos[0])
        layout.put(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.put(part.cmbInsulation, _x_pos, _y_pos[2])
        layout.put(part.txtOperPwr, _x_pos, _y_pos[3])
        layout.put(part.txtInputPwr, _x_pos, _y_pos[4])
        layout.put(part.txtArea, _x_pos, _y_pos[5])
        layout.put(part.txtWeight, _x_pos, _y_pos[6])

        part.cmbQuality.connect("changed", self._callback_combo, part, 85)
        part.txtCommercialPiQ.connect("focus-out-event", self._callback_entry,
                                      part, "float", 79)
        part.cmbInsulation.connect("changed", self._callback_combo, part, 38)
        part.txtOperPwr.connect("focus-out-event", self._callback_entry,
                                part, "float", 64)
        part.txtInputPwr.connect("focus-out-event", self._callback_entry,
                                 part, "float", 93)
        part.txtArea.connect("focus-out-event", self._callback_entry,
                             part, "float", 44)
        part.txtWeight.connect("focus-out-event", self._callback_entry,
                               part, "float", 45)

        layout.show_all()

        return _x_pos, _y_pos

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Inductive Devices Component Class calculation
        results.

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

        # Create and place all the labels.
        (_x_pos, _y_pos) = _widg.make_labels(self._out_labels[2:],
                                             layout, x_pos, y_pos)
        _x_pos += x_pos
        _x_pos -= 30

        # Create the reliability result display widgets.
        part.txtLambdaB = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        part.txtPiQ = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the reliability result display widgets.
        layout.put(part.txtLambdaB, _x_pos, _y_pos[1])
        layout.put(part.txtPiQ, _x_pos, _y_pos[2])
        layout.put(part.txtPiE, _x_pos, _y_pos[3])

        layout.show_all()

        return _x_pos, _y_pos

    def stress_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook stress calculation results tab with the
        widgets to display Inductor Component Class stress results.

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

        part.cmbQuality.set_active(int(_model.get_value(_row, 85)))
        part.cmbInsulation.set_active(int(_model.get_value(_row, 38)))
        part.txtOperPwr.set_text(str(fmt.format(_model.get_value(_row, 64))))
        part.txtInputPwr.set_text(str(fmt.format(_model.get_value(_row, 93))))
        part.txtArea.set_text(str(fmt.format(_model.get_value(_row, 44))))
        part.txtWeight.set_text(str(fmt.format(_model.get_value(_row, 45))))

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

        part.txtTRise.set_text(str(fmt.format(_model.get_value(_row, 107))))
        part.txtTJunc.set_text(str(fmt.format(_model.get_value(_row, 39))))
        part.txtLambdaB.set_text(str(fmt.format(_model.get_value(_row, 46))))
        part.txtPiQ.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 79))))
        part.txtPiE.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 72))))

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
        Callback function for handling Inductive Devices Component Class
        ComboBox changes.

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
            if part.txtCommercialPiQ.get_text() == '':
                CpiQ = 0.0
            else:
                CpiQ = float(part.txtCommercialPiQ.get_text())

            # Use this value for piQ if not being over-ridden.
            if CpiQ <= 0.0:
                _model.set_value(_row, 79, self._piQ[_index - 1])

        return False

    def _callback_entry(self, entry, event, part, convert, idx):
        """
        Callback function for handling Inductive Device Component Class
        Entry changes.

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
