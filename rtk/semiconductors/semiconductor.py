#!/usr/bin/env python
"""
semiconductor.py is the meta-class for all semiconductor types.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       semiconductor.py is part of The RTK Project
#
# All rights reserved.

import gettext
import locale

try:
    import rtk.configuration as _conf
    import rtk.widgets as _widg
except ImportError:
    import configuration as _conf
    import widgets as _widg

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Semiconductor(object):
    """
    Discrete Semiconductor meta class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.
    """

    _quality = ["", "JANTXV", "JANTX", "JAN", _(u"Lower"), _(u"Plastic")]
    _package = ["", "TO-1", "TO-3", "TO-5", "TO-8", "TO-9", "TO-12",
                "TO-18", "TO-28", "TO-33", "TO-39", "TO-41", "TO-44",
                "TO-46", "TO-52", "TO-53", "TO-57", "TO-59", "TO-60",
                "TO-61", "TO-63", "TO-66", "TO-71", "TO-72", "TO-83",
                "TO-89", "TO-92", "TO-94", "TO-99", "TO-126", "TO-127",
                "TO-204", "TO-204AA", "TO-205AD", "TO-205AF", "TO-220",
                "DO-4", "DO-5", "DO-7", "DO-8", "DO-9", "DO-13", "DO-14",
                "DO-29", "DO-35", "DO-41", "DO-45", "DO-204MB",
                "DO-205AB", "PA-42A", "PA-42B", "PD-36C", "PD-50",
                "PD-77", "PD-180", "PD-319", "PD-262", "PD-975", "PD-280",
                "PD-216", "PT-2G", "PT-6B", "PH-13", "PH-16", "PH-56",
                "PY-58", "PY-373"]

    def __init__(self):
        """
        Initializes the Semiconductor Component Class.
        """

        self._ready = False
        self.category = 2                   # Category in the rtkcom database.
        self.reason = ''

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._Tcase = [35, 45, 50, 45, 50, 60, 60, 75, 75, 60, 35, 50, 60, 45]
        self._thetaJC = [70, 10, 70, 70, 70, 70, 70, 5, 70, 70, 10, 70, 70, 70,
                         5, 5, 5, 5, 5, 5, 10, 70, 70, 5, 22, 70, 5, 70, 5, 5,
                         10, 10, 70, 70, 5, 5, 5, 10, 5, 5, 10, 5, 10, 10, 10,
                         5, 70, 5, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70,
                         70, 70, 70, 70, 70, 70]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        # Label text for input data.
        self._in_labels = [_(u"Quality:"), _(u"Package:"),
                           _(u"\u03C0<sub>Q</sub> Override:")]

        # Label text for output data.
        self._out_labels = [_(u"Temp Rise (\u2070C):"),
                            _(u"Junction Temp (\u2070C):"), (""),
                            u"\u03BB<sub>b</sub>:", u"\u03C0<sub>T</sub>:",
                            u"\u03C0<sub>Q</sub>:", u"\u03C0<sub>E</sub>:"]

        # Derating points for the derating curve.  The list at position 0 is
        # for severe environments.  The list at position 1 is for benign
        # environments.
        self._derate_criteria = [[0.6, 0.6, 0.0], [0.9, 0.9, 0.0]]

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Discrete Semiconductor
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
        part.cmbPackage = _widg.make_combo(simple=True)
        part.txtCommercialPiQ = _widg.make_entry(width=100)

        # Load all the gtk.ComboBox().
        for i in range(len(self._quality)):
            part.cmbQuality.insert_text(i, self._quality[i])
        for i in range(len(self._package)):
            part.cmbPackage.insert_text(i, self._package[i])

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._in_labels, layout, 5, y_pos)
        _x_pos = max(_x_pos, x_pos)

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.put(part.cmbQuality, _x_pos, _y_pos[0])
        layout.put(part.cmbPackage, _x_pos, _y_pos[1])
        layout.put(part.txtCommercialPiQ, _x_pos, _y_pos[2])

        # Connect to callback methods.
        part.cmbQuality.connect("changed", self._callback_combo, part, 85)
        part.cmbPackage.connect("changed", self._callback_combo, part, 67)
        part.txtCommercialPiQ.connect("focus-out-event", self._callback_entry,
                                      part, "float", 79)

        layout.show_all()

        return _x_pos, _y_pos

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Discrete Semicondutor calculation results.

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
        part.txtPiT = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiQ = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)

        # Create and place all the labels.
        (_x_pos, _y_pos) = _widg.make_labels(self._out_labels[2:],
                                             layout, x_pos, y_pos)
        _x_pos += x_pos
        _x_pos -= 30

        # Place the reliability result display widgets.
        layout.put(part.txtLambdaB, _x_pos, _y_pos[1])
        layout.put(part.txtPiT, _x_pos, _y_pos[2])
        layout.put(part.txtPiQ, _x_pos, _y_pos[3])
        layout.put(part.txtPiE, _x_pos, _y_pos[4])

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
        _x_pos = max(x_pos, _x_pos)

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

        part.cmbPackage.set_active(int(_model.get_value(_row, 67)))
        part.cmbQuality.set_active(int(_model.get_value(_row, 85)))
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

        part.txtPiQ.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 79))))
        part.txtPiT.set_text(str(fmt.format(_model.get_value(_row, 82))))
        part.txtLambdaB.set_text(str(fmt.format(_model.get_value(_row, 46))))
        part.txtTJunc.set_text(str(fmt.format(_model.get_value(_row, 39))))
        part.txtTRise.set_text(str(fmt.format(_model.get_value(_row, 107))))
        part.txtPiE.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 72))))

        part.txtOSReason.set_text(self.reason)

        part.graDerate.cla()

        return _model, _row

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Discrete Semicondutor Class
        ComboBox changes.

        :param gtk.ComboBox combo: the gtk.ComboBox() calling this method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param int idx: the user-defined index for the calling combobx.
        :return: (_model, _row); the Parts List gtk.Treemodel and selected
                 gtk.TreeIter()
        :rtype: tuple
        """

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        _index = combo.get_active()

        _model.set_value(_row, idx, int(_index))

        if idx == 85:                       # Quality
            if part.txtCommercialPiQ.get_text() == "":
                CpiQ = 0.0
            else:
                CpiQ = float(part.txtCommercialPiQ.get_text())

            # Use this value for piQ if not being over-ridden.
            if CpiQ <= 0.0:
                _model.set_value(_row, 79, self._piQ[_index - 1])

        return _model, _row

    def _callback_entry(self, entry, event, part, convert, idx):
        """
        Callback function for handling Discrete Semiconductor Device
        Class Entry changes.

        :param gtk.Entry entry: the gtk.Entry() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param str convert: the data type to convert the gtk.Entry() contents.
        :param int idx: the position in the Component property array
                        associated with the data from the gtk.Entry() that
                        called this method.
        :return: (_model, _row); the Parts List gtk.Treemodel and selected
                 gtk.TreeIter()
        :rtype: tuple
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

        return _model, _row
