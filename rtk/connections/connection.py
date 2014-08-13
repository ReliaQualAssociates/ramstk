#!/usr/bin/env python
"""
This is the electrical connection meta-class.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       connection.py is part of The RTK Project
#
# All rights reserved.

import locale
import gettext
import pango

try:
    import rtk.configuration as _conf
    import rtk.widgets as _widg
except ImportError:
    import configuration as _conf
    import widgets as _widg

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except ImportError:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Connection(object):
    """
    Connections meta class.

    Hazard Rate Models:
        # MIL-HDBK-217F, sections 15, 16, and 17.
    """

    def __init__(self):
        """
        Initializes the Connection Class.
        """

        self._ready = False
        self.category = 8                   # Category in the rtkcom database.
        self.reason = ""

        # Label text for input data.
        self._in_labels = [_(u"Quality:"), _(u"\u03C0<sub>Q</sub> Override:")]

        # Label text for output data.
        self._out_labels = ["", u"\u03BB<sub>b</sub>:", u"\u03C0<sub>E</sub>:"]

        # Derating points for the derating curve.  The list at position 0 is
        # for severe environments.  The list at position 1 is for benign
        # environments.
        self._derate_criteria = [[0.7, 0.7, 0.0], [0.9, 0.9, 0.0]]

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Connections Component Class
        prediction calculations.

        :param rtk.Component part: the current instance of the Component class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Clear all the display widgets from the gtk.Fixed() except the
        # calculation model gtk.Label() and gtk.ComboBox().
        for _child in layout.get_children()[2:]:
            layout.remove(_child)

        # Create the input widgets.
        part.cmbQuality = _widg.make_combo(simple=True)
        part.txtCommercialPiQ = _widg.make_entry(width=100)

        # Load the gtk.ComboBox().
        for i in range(len(self._quality)):
            part.cmbQuality.insert_text(i, self._quality[i])

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._in_labels, layout, 5, y_pos)
        _x_pos = max(x_pos, _x_pos)

        # Place the input widgets.
        layout.put(part.cmbQuality, _x_pos, _y_pos[0])
        layout.put(part.txtCommercialPiQ, _x_pos, _y_pos[1])

        # Connect to callback methods.
        part.cmbQuality.connect('changed', self._callback_combo,
                                part, 85)
        part.txtCommercialPiQ.connect('focus-out-event', self._callback_entry,
                                      part, 'float', 79)

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

        part.cmbQuality.set_active(int(_model.get_value(_row, 85)))
        if int(_model.get_value(_row, 85)) <= 0:
            _commercial_piq = _model.get_value(_row, 79)
            part.txtCommercialPiQ.set_text(str(fmt.format(_commercial_piq)))
        else:
            part.txtCommercialPiQ.set_text("0.0")

        return(_model, _row)

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Connections Component Class calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Clear all the display widgets from the gtk.Fixed().
        for _child in layout.get_children()[20:]:
            layout.remove(_child)

        # Create and place all the labels.
        (_x_pos,
         _y_pos) = _widg.make_labels(self._out_labels, layout, x_pos, y_pos)
        _x_pos = x_pos + _x_pos

        # Create the reliability result display widgets.
        part.txtLambdaB = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        part.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the reliability result display widgets.
        layout.put(part.txtLambdaB, _x_pos, _y_pos[1])
        layout.put(part.txtPiE, _x_pos, _y_pos[2])

        layout.show_all()

        self._ready = True

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
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Clear all the display widgets from the gtk.Fixed().
        for _child in layout.get_children()[16:]:
            layout.remove(_child)

        part.graDerate.set_title(_(u"Derating Curve for %s at %s") %
                                 (part.txtPartNum.get_text(),
                                  part.txtRefDes.get_text()))
        part.graDerate.set_xlabel(_(u"Temperature [\u2070C]"))
        part.graDerate.set_ylabel(_(u"Current Ratio"))

        layout.show_all()

        self._ready = True

        return False

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

        part.txtLambdaB.set_text(str(fmt.format(_model.get_value(_row, 46))))
        part.txtPiE.set_text(str('{0:0.2g}'.format(
            _model.get_value(_row, 72))))

        part.txtOSReason.set_text(self.reason)

        part.graDerate.cla()
        part.graDerate.set_xlabel(_(u"Temperature [\u2070C]"))
        part.graDerate.set_ylabel(_(u"Current Ratio"))

        # Plot the derating curve and operating point.
        _x_vals = [float(part.min_temp), float(part.knee_temp),
                   float(part.max_temp)]

        _current_ratio = part.op_current / part.rated_current
        part.graDerate.plot(_x_vals, self._derate_criteria[0], 'r.-',
                            linewidth=2)
        part.graDerate.plot(_x_vals, self._derate_criteria[1], 'b.-',
                            linewidth=2)
        part.graDerate.plot(part.temperature_active, _current_ratio, 'go')
        if(_x_vals[0] != _x_vals[2] and
           self._derate_criteria[1][0] != self._derate_criteria[1][2]):
            part.graDerate.axis([0.95 * _x_vals[0],
                                 1.05 * _x_vals[2],
                                 self._derate_criteria[1][2],
                                 1.05 * self._derate_criteria[1][0]])
        else:
            part.graDerate.axis([0.95, 1.05, 0.0, 1.05])

        return(_model, _row)

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Connections Component Class ComboBox
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

        # Update the Parts List.
        _model.set_value(_row, idx, int(_index))

        return False

    def _callback_entry(self, entry, event, part, convert, idx):
        """
        Callback function for handling Connections Component Class
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
