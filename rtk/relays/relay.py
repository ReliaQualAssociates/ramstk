#!/usr/bin/env python

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       relay.py is part of The RTK Project
#
# All rights reserved.

import gettext
import locale
import pango

from math import exp, sqrt

try:
    import rtk.calculations as _calc
    import rtk.configuration as _conf
    import rtk.widgets as _widg
except:
    import calculations as _calc
    import configuration as _conf
    import widgets as _widg

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Mechanical(object):
    """
    Mechanical Relay Component Class.
    Covers specifications MIL-R-5757, MIL-R-6106, MIL-R-19523, and
    MIL-R-39016.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 13.1
    """

    _application = [["", _(u"Dry Circuit")],
                    ["", _(u"General Purpose"), _(u"Sensitive (0-100 mW)"),
                     _(u"Polarized"), _(u"Vibrating Reed"), _(u"High Speed"),
                     _(u"Thermal Time Delay"), _(u"Electronic Time Delay"),
                     _(u"Magnetic Latching")],
                    ["",  _(u"High Voltage"), _(u"Medium Power")],
                    ["", _(u"Contactor")]]
    _construction = [[["", _(u"Long Armature"), _(u"Dry Reed"),
                       _(u"Mercury Wetted"), _(u"Magnetic Latching"),
                       _(u"Balanced Armature"), _(u"Solenoid")]],
                     [["", _(u"Long Armature"), _(u"Balanaced Armature"),
                       _(u"Solenoid")],
                      ["", _(u"Long Armature"), _(u"Short Armature"),
                       _(u"Mercury Wetted"), _(u"Magnetic Latching"),
                       _(u"Meter Movement"), _(u"Balanced Armature")],
                      ["", _(u"Short Armature"), _(u"Meter Movement")],
                      ["", _(u"Dry Reed"), _(u"Mecury Wetted")],
                      ["", _(u"Balanced Armature"), _(u"Short Armature"),
                       _(u"Dry Reed")],
                      ["", _(u"Bimetal")],
                      [""],
                      ["", _(u"Dry Reed"), _(u"Mercury Wetted"),
                       _(u"Balanced Armature")]],
                     [["", _(u"Vacuum, Glass"), _(u"Vacuum, Ceramic")],
                      ["", _(u"Long Armature"), _(u"Short Armature"),
                       _(u"Mercury Wetted"), _(u"Magnetic Latching"),
                       _(u"Mechanical Latching"), _(u"Balanced Armature"),
                       _(u"Solenoid")]],
                     [["", _(u"Short Armature"), _(u"Mechanical Latching"),
                       _(u"Balanced Armature"), _(u"Solenoid")]]]
    _form = ["", "SPST", "DPST", "SPDT", "3PST", "4PST", "DPDT", "3PDT",
             "4PDT", "6PDT"]
    _insulation = ["", u"85\u00B0C", u"125\u00B0C"]
    _load = ["", _(u"Resistive"), _(u"Inductive"), _(u"Lamp")]
    _quality = ["", "R", "P", "X", "U", "M", "L", _(u"Non-Est. Reliability"),
                _(u"Lower")]
    _rating = ["", _(u"Signal Current (Low mV and mA)"), "0-5 Amp", "5-20 Amp",
               "20-600 Amp"]

    def __init__(self):
        """
        Initializes the Mechanical Relay Component Class.
        """

        self._ready = False
        self.category = 6                   # Category in the rtkcom database.
        self.subcategory = 64               # Subcategory in the rtkcom DB.
        self.reason = ''

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piC = [1.0, 1.5, 1.75, 2.0, 2.5, 3.0, 4.25, 5.5, 8.0]
        self._piE = [[1.0, 2.0, 15.0, 8.0, 27.0, 7.0, 9.0, 11.0, 12.0, 46.0,
                      0.50, 25.0, 66.0, 0.0],
                     [2.0, 5.0, 44.0, 24.0, 78.0,
                      15.0, 20.0, 28.0, 38.0, 140.0, 1.0, 72.0, 200.0, 0.0]]
        self._piQ = [0.10, 0.30, 0.45, 0.60, 1.0, 1.5, 3.0, 3.0]
        self._lambdab_count =[[0.13, 0.28, 2.1, 1.1, 3.8, 1.1, 1.4, 1.9, 2.0,
                               7.0, 0.66, 3.5, 10.0, 0.0],
                              [0.43, 0.89, 6.9, 3.6, 12.0, 3.4, 4.4, 6.2, 6.7,
                               22.0, 0.21, 11.0, 32.0, 0.0],
                              [0.13, 0.26, 2.1, 1.1, 3.8, 1.1, 1.4, 1.9, 2.0,
                               7.0, 0.66, 3.5, 10.0, 0.0],
                              [0.11, 0.23, 1.8, 0.92, 3.3, 0.96, 1.2, 2.1, 2.3,
                               6.5, 0.54, 3.0, 9.0, 0.0],
                              [0.29, 0.60, 4.8, 2.4, 8.2, 2.3, 2.9, 4.1, 4.5,
                               15.0, 0.14, 7.6, 22.0, 0.0],
                              [0.88, 1.8, 14.0, 7.4, 26.0, 7.1, 9.1, 13.0,
                               14.0, 46.0, 0.44, 24.0, 67.0, 0.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        # Label text for input data.
        self._in_labels = [_(u"Quality:"), _(u"\u03C0<sub>Q</sub> Override:"),
                           _(u"Rated Temperature (\u00B0C):"),
                           _(u"Load Type:"), _(u"Rated Current (A):"),
                           _(u"Operating Current (A):"), _(u"Cycling Rate:"),
                           _(u"Contact Form:"), _(u"Contact Rating:"),
                           _(u"Application:"), _(u"Construction:")]

        # Label text for output data.
        self._out_labels = [u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>L</sub>\u03C0<sub>C</sub>\u03C0<sub>CYC</sub>\u03C0<sub>F</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
                            u"\u03BB<sub>b</sub>:", u"\u03C0<sub>L</sub>:",
                            u"\u03C0<sub>C</sub>:", u"\u03C0<sub>CYC</sub>:",
                            u"\u03C0<sub>F</sub>:", u"\u03C0<sub>Q</sub>:",
                            u"\u03C0<sub>E</sub>:"]

        # Derating points for the derating curve.  The list at position 0 is
        # for severe environments.  The list at position 1 is for benign
        # environments.
        self._derate_criteria = [[0.6, 0.6, 0.0], [0.9, 0.9, 0.0]]

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Mechanical Relay Component
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

        # Create the input widgets.
        part.cmbQuality = _widg.make_combo(simple=True)
        part.txtCommercialPiQ = _widg.make_entry(width=100)
        part.cmbInsulation = _widg.make_combo(simple=True)
        # Create the load type combobox.  We store this in the func_id field
        # in the program database.
        part.cmbLoad = _widg.make_combo(simple=True)
        part.txtRatedCurrent = _widg.make_entry(width=100)
        part.txtOperCurrent = _widg.make_entry(width=100)
        part.txtCycleRate = _widg.make_entry(width=100)
        # Create the contact form combobox.  We store this in the family_id
        # field in the program database.
        part.cmbForm = _widg.make_combo(simple=True)
        # Create the contact rating combobox.  We store this in the
        # resistance_id field in the program database.
        part.cmbRating = _widg.make_combo(simple=True)
        part.cmbApplication = _widg.make_combo(simple=True)
        part.cmbConstruction = _widg.make_combo(simple=True)

        # Load all the gtk.ComboBox().
        for i in range(len(self._quality)):
            part.cmbQuality.insert_text(i, self._quality[i])
        for i in range(len(self._insulation)):
            part.cmbInsulation.insert_text(i, self._insulation[i])
        for i in range(len(self._load)):
            part.cmbLoad.insert_text(i, self._load[i])
        for i in range(len(self._form)):
            part.cmbForm.insert_text(i, self._form[i])
        for i in range(len(self._rating)):
            part.cmbRating.insert_text(i, self._rating[i])

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._in_labels, layout, 5, y_pos)
        _x_pos += 35

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.put(part.cmbQuality, _x_pos, _y_pos[0])
        layout.put(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.put(part.cmbInsulation, _x_pos, _y_pos[2])
        layout.put(part.cmbLoad, _x_pos, _y_pos[3])
        layout.put(part.txtRatedCurrent, _x_pos, _y_pos[4])
        layout.put(part.txtOperCurrent, _x_pos, _y_pos[5])
        layout.put(part.txtCycleRate, _x_pos, _y_pos[6])
        layout.put(part.cmbForm, _x_pos, _y_pos[7])
        layout.put(part.cmbRating, _x_pos, _y_pos[8])
        layout.put(part.cmbApplication, _x_pos, _y_pos[9])
        layout.put(part.cmbConstruction, _x_pos, _y_pos[10])

        # Connect to callback methods.
        part.cmbQuality.connect("changed", self._callback_combo, part, 85)
        part.txtCommercialPiQ.connect("focus-out-event", self._callback_entry,
                                      part, "float", 79)
        part.cmbInsulation.connect("changed", self._callback_combo, part, 38)
        part.cmbLoad.connect("changed", self._callback_combo, part, 30)
        part.txtRatedCurrent.connect("focus-out-event", self._callback_entry,
                                     part, "float", 92)
        part.txtOperCurrent.connect("focus-out-event", self._callback_entry,
                                    part, "float", 62)
        part.txtCycleRate.connect("focus-out-event", self._callback_entry,
                                  part, "float", 19)
        part.cmbForm.connect("changed", self._callback_combo, part, 28)
        part.cmbRating.connect("changed", self._callback_combo, part, 96)
        part.cmbApplication.connect("changed", self._callback_combo, part, 5)
        part.cmbConstruction.connect("changed", self._callback_combo, part, 16)

        layout.show_all()

        return _x_pos, _y_pos

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Mechanical Relay Component Class calculation
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

        # Create the reliability result display widgets.
        part.txtLambdaB = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        # Create the Pi L results entry.  We store this in the pi_m field
        # in the program database.
        part.txtPiL = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiC = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiCYC = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiF = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiQ = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)

        # Create and place all the labels.
        (_x_pos, _y_pos) = _widg.make_labels(self._out_labels,
                                             layout, x_pos, y_pos)
        _x_pos += x_pos
        _x_pos -= 30

        # Place the reliability result display widgets.
        layout.put(part.txtLambdaB, _x_pos, _y_pos[1])
        layout.put(part.txtPiL, _x_pos, _y_pos[2])
        layout.put(part.txtPiC, _x_pos, _y_pos[3])
        layout.put(part.txtPiCYC, _x_pos, _y_pos[4])
        layout.put(part.txtPiF, _x_pos, _y_pos[5])
        layout.put(part.txtPiQ, _x_pos, _y_pos[6])
        layout.put(part.txtPiE, _x_pos, _y_pos[7])

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
        #(_x_pos, _y_pos) = _widg.make_labels(self._out_labels[:2], layout,
        #                                     5, y_pos)

        # Create the stress result display widgets.
        #part.txtTRise = _widg.make_entry(editable=False, bold=True)
        #part.txtTJunc = _widg.make_entry(editable=False, bold=True)

        # Place the stress result display widgets.
        #layout.put(part.txtTRise, 155, 305)
        #layout.put(part.txtTJunc, 155, 335)

        #layout.show_all()

        return False

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
        part.cmbInsulation.set_active(int(_model.get_value(_row, 38)))
        part.cmbLoad.set_active(int(_model.get_value(_row, 30)))
        part.txtRatedCurrent.set_text(str(fmt.format(
            _model.get_value(_row, 92))))
        part.txtOperCurrent.set_text(str(fmt.format(
            _model.get_value(_row, 62))))
        part.txtCycleRate.set_text(str(fmt.format(_model.get_value(_row, 19))))
        part.cmbForm.set_active(int(_model.get_value(_row, 28)))
        part.cmbRating.set_active(int(_model.get_value(_row, 96)))
        part.cmbApplication.set_active(int(_model.get_value(_row, 5)))
        part.cmbConstruction.set_active(int(_model.get_value(_row, 16)))
        if int(_model.get_value(_row, 85)) <= 0:
            part.txtCommercialPiQ.set_text(str(_model.get_value(_row, 79)))
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

        part.txtLambdaB.set_text(str(fmt.format(_model.get_value(_row, 46))))
        part.txtPiL.set_text(str(fmt.format(_model.get_value(_row, 76))))
        part.txtPiC.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 69))))
        part.txtPiCYC.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 71))))
        part.txtPiF.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 74))))
        part.txtPiQ.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 79))))
        part.txtPiE.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 72))))

        part.txtOSReason.set_text(self.reason)

        part.graDerate.cla()

        return _model, _row

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Mechanical Relay Component Class
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

        _model.set_value(_row, idx, int(_index))

        if idx == 5:                        # Application
            _index2 = part.cmbRating.get_active()
            part.cmbConstruction.get_model().clear()
            for i in range(len(self._construction[_index2 - 1][_index - 1])):
                part.cmbConstruction.insert_text(i,
                    self._construction[_index2 - 1][_index - 1][i])


        elif idx == 85:                     # Quality
            if part.txtCommercialPiQ.get_text() == "":
                CpiQ = 0.0
            else:
                CpiQ = float(part.txtCommercialPiQ.get_text())

            # Use this value for piQ if not being over-ridden.
            if CpiQ <= 0.0:
                _model.set_value(_row, 79, self._piQ[_index])

        elif idx == 96:                     # Contact rating
            part.cmbApplication.get_model().clear()
            for i in range(len(self._application[_index - 1])):
                part.cmbApplication.insert_text(i,
                    self._application[_index - 1][i])

        return False

    def _callback_entry(self, entry, event, part, convert, idx):
        """
        Callback function for handling Mechanical Relay Component Class
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

    def calculate(self, partmodel, partrow, systemmodel, systemrow):
        """
        Performs hazard rate calculations for the Fixed Paper Bypass Capacitor
        class.

        :param gtk.TreeModel partmodel: the RTK List class gtk.TreeModel().
        :param gtk.TreeIter partrow: the currently selected gtk.TreeIter()
                                     in List class gtk.TreeModel().
        :param gtk.TreeModel systemmodel: the RTK Hardware class
                                          gtk.TreeModel().
        :param gtk.TreeIter systemrow: the currently selected
                                       gtk.TreeIter() in the RTK Hardware
                                       class gtk.TreeModel().
        :return: False if succussful or True if an error is encountered.
        :rtype: boolean
        """

        def _calculate_mil_217_count(partmodel, partrow,
                                     systemmodel, systemrow):
            """
            Performs MIL-HDBK-217F part count hazard rate calculations for the
            Linear Integrated Circuit Class.

            :param gtk.TreeModel partmodel: the RTK List class gtk.TreeModel().
            :param gtk.TreeIter partrow: the currently selected gtk.TreeIter()
                                         in List class gtk.TreeModel().
            :param gtk.TreeModel systemmodel: the RTK Hardware class
                                              gtk.TreeModel().
            :param gtk.TreeIter systemrow: the currently selected
                                           gtk.TreeIter() in the RTK Hardware
                                           class gtk.TreeModel().
            :return: False if succussful or True if an error is encountered.
            :rtype: boolean
            """

            _hrmodel = {}
            _hrmodel['equation'] = "lambdab * piQ"

            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hazard rate inputs.
            Aidx = partmodel.get_value(partrow, 5)      # Application index
            Cidx = partmodel.get_value(partrow, 16)     # Construction index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Ridx = partmodel.get_value(partrow, 96)     # Rating index
            Eidx = systemmodel.get_value(systemrow, 22) # Environment index

            if Ridx == 1:
                if Cidx == 2:
                    Sidx = 3
                else:
                    Sidx = 0
            elif Ridx == 2:
                if Aidx == 2:
                    if Cidx == 4:
                        Sidx = 2
                    elif Cidx == 5:
                        Sidx = 5
                    else:
                        Sidx = 0
                elif Aidx == 3:
                    if Cidx == 2:
                        Sidx = 5
                    else:
                        Sidx = 0
                elif Aidx == 4:
                    Sidx = 3
                elif Aidx == 5:
                    if Cidx == 3:
                        Sidx = 3
                    else:
                        Sidx = 0
                elif Aidx == 6:
                    Sidx = 4
                elif Aidx == 8:
                    if Cidx == 2 or Cidx == 3:
                        Sidx = 2
                    else:
                        Sidx = 0
                else:
                    Sidx = 0
            elif Ridx == 4:
                if Cidx == 2:
                    Sidx = 2
                else:
                    Sidx = 0
            else:
                Sidx = 0

            _hrmodel['lambdab'] = self._lambdab_count[Sidx][Eidx - 1]

            # Calculate component active hazard rate.
            _lambdaa = _calc.calculate_part(_hrmodel)
            _lambdaa = _lambdaa * _quantity / 1000000.0

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

            systemmodel.set_value(systemrow, 28, _lambdaa)
            systemmodel.set_value(systemrow, 32, _lambdaa)
            systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

            return False

        def _calculate_mil_217_stress(partmodel, partrow,
                                      systemmodel, systemrow):
            """
            Performs MIL-HDBK-217F part stress hazard rate calculations for
            the Mechanical Relay Component Class.

            :param gtk.TreeModel partmodel: the RTK List class gtk.TreeModel().
            :param gtk.TreeIter partrow: the currently selected gtk.TreeIter()
                                         in List class gtk.TreeModel().
            :param gtk.TreeModel systemmodel: the RTK Hardware class
                                              gtk.TreeModel().
            :param gtk.TreeIter systemrow: the currently selected
                                           gtk.TreeIter() in the RTK Hardware
                                           class gtk.TreeModel().
            :return: False if succussful or True if an error is encountered.
            :rtype: boolean
            """

            _hrmodel = {}
            _hrmodel['equation'] = "lambdab * piL * piC * piCYC * piF * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hazard rate inputs.
            Cyc = partmodel.get_value(partrow, 19)
            Tamb = partmodel.get_value(partrow, 37)
            Ioper = partmodel.get_value(partrow, 62)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Irated = partmodel.get_value(partrow, 92)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Irated = partmodel.get_value(partrow, 92)

            # Base hazard rate.
            idx = partmodel.get_value(partrow, 38)
            if idx == 1:                    # 85C
                Tref = 352.0
                K1 = 0.00555
                K2 = 15.7
            elif idx == 2:                  # 125C
                Tref = 377.0
                K1 = 0.0054
                K2 = 10.4
            else:                           # Default
                Tref = 352.0
                K1 = 0.00555
                K2 = 15.7

            _hrmodel['lambdab'] = K1 * exp(((Tamb + 273) / Tref)**K2)

            # Load stress correction factor.
            idx = partmodel.get_value(partrow, 30)
            S = Ioper / Irated
            if idx == 1:                    # Resistive
                K = 0.8
            elif idx == 2:                  # Inductive
                K = 0.4
            elif idx == 3:                  # Lamp
                K = 0.2
            else:                           # Default
                K = 0.2

            _hrmodel['piL'] = exp(S / K)**2

            # Contact form correction factor.
            idx = partmodel.get_value(partrow, 28)
            _hrmodel['piC'] = self._piC[idx - 1]

            # Cycling rate correction factor.
            idx = partmodel.get_value(partrow, 85)
            if idx == 8:                    # Non MIL-SPEC
                if Cyc >= 1000:
                    _hrmodel['piCYC'] = (Cyc / 100.0)**2.0
                elif Cyc >= 10 and Cyc < 1000.0:
                    _hrmodel['piCYC'] = Cyc / 10.0

            # Application and construction correction factor.
            _hrmodel['piF'] = 1.0
            idx2 = partmodel.get_value(partrow, 96) # Contact rating
            idx3 = partmodel.get_value(partrow, 5)  # Application
            idx4 = partmodel.get_value(partrow, 16) # Construction
            if idx2 == 1:                   # Signal Current
                if idx3 == 1:               # Dry Contact
                    if idx4 == 1:           # Long Armature
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 8.0
                        else:
                            _hrmodel['piF'] = 4.0
                    elif idx4 == 2:         # Dry Reed
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 18.0
                        else:
                            _hrmodel['piF'] = 6.0
                    elif idx4 == 3:         # Mercury Wetted
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 3.0
                        else:
                            _hrmodel['piF'] = 1.0
                    elif idx4 == 4:         # Magnetic Latching
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 8.0
                        else:
                            _hrmodel['piF'] = 4.0
                    elif idx4 == 5:         # Balanced Armature
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 14.0
                        else:
                            _hrmodel['piF'] = 7.0
                    elif idx4 == 6:         # Solenoid
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 4.0
                        else:
                            _hrmodel['piF'] = 7.0
            elif idx2 == 2:                 # 0-5 Amp
                if idx3 == 1:               # General Purpose
                    if idx4 == 1:           # Long Armature
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 6.0
                        else:
                            _hrmodel['piF'] = 3.0
                    elif idx4 == 2:         # Balanced Armature
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 10.0
                        else:
                            _hrmodel['piF'] = 5.0
                    elif idx4 == 3:         # Solenoid
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 12.0
                        else:
                            _hrmodel['piF'] = 6.0
                elif idx3 == 2:             # Sensitive
                    if idx4 == 1:           # Long Armature
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 10.0
                        else:
                            _hrmodel['piF'] = 5.0
                    elif idx4 == 2:         # Short Armature
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 10.0
                        else:
                            _hrmodel['piF'] = 5.0
                    elif idx4 == 3:         # Mercury Wetted
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 6.0
                        else:
                            _hrmodel['piF'] = 2.0
                    elif idx4 == 4:         # Magnetic Latching
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 12.0
                        else:
                            _hrmodel['piF'] = 6.0
                    elif idx4 == 5:         # Meter Movement
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 100.0
                        else:
                            _hrmodel['piF'] = 100.0
                    elif idx4 == 6:         # Balanced Armature
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 20.0
                        else:
                            _hrmodel['piF'] = 10.0
                elif idx3 == 3:             # Polarized
                    if idx4 == 1:           # Short Armature
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 20.0
                        else:
                            _hrmodel['piF'] = 10.0
                    elif idx4 == 2:         # Meter Movement
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 100.0
                        else:
                            _hrmodel['piF'] = 100.0
                elif idx3 == 4:             # Vibrating Reed
                    if idx4 == 1:           # Dry Reed
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 12.0
                        else:
                            _hrmodel['piF'] = 6.0
                    elif idx4 == 2:         # Mecury Wetted
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 3.0
                        else:
                            _hrmodel['piF'] = 1.0
                elif idx3 == 5:             # High Speed
                    if idx4 == 1:           # Balanced Armature
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 0.0
                        else:
                            _hrmodel['piF'] = 25.0
                    elif idx4 == 2:         # Short Armature
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 0.0
                        else:
                            _hrmodel['piF'] = 25.0
                    elif idx4 == 3:         # Dry Reed
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 0.0
                        else:
                            _hrmodel['piF'] = 6.0
                elif idx3 == 6:             # Thermal Time Delay
                    if idx4 == 1:           # Bimetal
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 20.0
                        else:
                            _hrmodel['piF'] = 10.0
                elif idx3 == 7:             # Electronic Time Delay
                    if idx == 8:            # Non MIL-SPEC
                        _hrmodel['piF'] = 12.0
                    else:
                        _hrmodel['piF'] = 9.0
                elif idx3 == 8:             # Magnetic Latching
                    if idx4 == 1:           # Dry Reed
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 20.0
                        else:
                            _hrmodel['piF'] = 10.0
                    elif idx4 == 2:         # Mercury Wetted
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 10.0
                        else:
                            _hrmodel['piF'] = 5.0
                    elif idx4 == 3:         # Balanced Armature
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 10.0
                        else:
                            _hrmodel['piF'] = 5.0
            elif idx2 == 3:                 # 5-20 Amp
                if idx3 == 1:               # High Voltage
                    if idx4 == 1:           # Vacuum, Glass
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 40.0
                        else:
                            _hrmodel['piF'] = 20.0
                    elif idx4 == 2:         # Vacuum, Ceramic
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 10.0
                        else:
                            _hrmodel['piF'] = 5.0
                elif idx3 == 2:             # Medium Power
                    if idx4 == 1:           # Long Armature
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 6.0
                        else:
                            _hrmodel['piF'] = 3.0
                    elif idx4 == 2:         # Short Armature
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 6.0
                        else:
                            _hrmodel['piF'] = 3.0
                    elif idx4 == 3:         # Mercury Wetted
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 3.0
                        else:
                            _hrmodel['piF'] = 1.0
                    elif idx4 == 4:         # Magnetic Latching
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 6.0
                        else:
                            _hrmodel['piF'] = 2.0
                    elif idx4 == 5:         # Mechanical Latching
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 6.0
                        else:
                            _hrmodel['piF'] = 3.0
                    elif idx4 == 6:         # Balanced Armature
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 6.0
                        else:
                            _hrmodel['piF'] = 2.0
                    elif idx4 == 7:         # Solenoid
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 6.0
                        else:
                            _hrmodel['piF'] = 2.0
            elif idx2 == 4:                 # 20-600 Amp
                if idx3 == 1:               # Contactor
                    if idx4 == 1:           # Short Armature
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 14.0
                        else:
                            _hrmodel['piF'] = 7.0
                    elif idx4 == 2:         # Mechanical Latching
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 24.0
                        else:
                            _hrmodel['piF'] = 12.0
                    elif idx4 == 3:         # Balanced Armature
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 20.0
                        else:
                            _hrmodel['piF'] = 10.0
                    elif idx4 == 4:         # Solenoid
                        if idx == 8:        # Non MIL-SPEC
                            _hrmodel['piF'] = 10.0
                        else:
                            _hrmodel['piF'] = 5.0
            else:
                _hrmodel['piF'] = 1.0

            # Environmental correction factor.
            idx2 = systemmodel.get_value(systemrow, 22)
            if idx == 8:                    # Non MIL-SPEC
                _hrmodel['piE'] = self._piE[1][idx2 - 1]
            else:
                _hrmodel['piE'] = self._piE[0][idx2 - 1]

            # Calculate component active hazard rate.
            _lambdaa = _calc.calculate_part(_hrmodel)
            _lambdaa = _lambdaa * _quantity / 1000000.0

            # Calculate the component dormant hazard rate.
            _lambdad = _calc.dormant_hazard_rate(_category_id, _subcategory_id,
                                                 _active_env, _dormant_env,
                                                 _lambdaa)

            # Calculate the component predicted hazard rate.
            _lambdap = _lambdaa + _lambdad + _lambdas

            # Calculate overstresses.
            (_overstress,
             self.reason) = _calc.overstressed(partmodel, partrow,
                                               systemmodel, systemrow)

            # Calculate operating point ratios.
            _i_ratio = Iapplied / Irated

            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 69, _hrmodel['piC'])
            partmodel.set_value(partrow, 71, _hrmodel['piCYC'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 74, _hrmodel['piF'])
            partmodel.set_value(partrow, 76, _hrmodel['piL'])

            systemmodel.set_value(systemrow, 28, _lambdaa)
            systemmodel.set_value(systemrow, 29, _lambdad)
            systemmodel.set_value(systemrow, 32, _lambdap)
            systemmodel.set_value(systemrow, 60, _overstress)
            systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

            return False

        _calc_model = systemmodel.get_value(systemrow, 10)

        if _calc_model == 1:
            _calculate_mil_217_stress(partmodel, partrow,
                                      systemmodel, systemrow)
        elif _calc_model == 2:
            _calculate_mil_217_count(partmodel, partrow,
                                     systemmodel, systemrow)

        return False


class SolidState(object):
    """
    Solid State Relay Component Class.
    Covers specifications MIL-R-28750 and MIL-R-83726.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 13.2
    """

    _quality = ["", "MIL-SPEC", _(u"Lower")]
    _type = ["", _(u"Solid State"), _(u"Solid State Time Delay"), _(u"Hybrid")]

    def __init__(self):
        """
        Initializes the Solid State Relay Component Class.
        """

        self._ready = False
        self.category = 6                   # Category in the rtkcom database.
        self.subcategory = 65               # Subcategory in the rtkcom DB.
        self.reason = ''

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 3.0, 12.0, 6.0, 17.0, 12.0, 19.0, 21.0, 32.0, 23.0,
                     0.4, 12.0, 33.0, 590.0]
        self._piQ = [1.0, 4.0]
        self._lambdab_count = [[0.40, 1.2, 4.8, 2.4, 6.8, 4.8, 7.6, 8.4, 13.0,
                                9.2, 0.16, 4.8, 13.0, 240.0],
                               [0.40, 1.2, 4.8, 2.4, 6.8, 4.8, 7.6, 8.4, 13.0,
                                9.2, 0.16, 4.8, 13.0, 240.0],
                               [0.50, 1.5, 6.0, 3.0, 8.5, 5.0, 9.5, 11.0, 16.0,
                                12.0, 0.20, 5.0, 17.0, 300.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        # Label text for input data.
        self._in_labels = [_(u"Quality:"), _(u"\u03C0<sub>Q</sub> Override:"),
                           _(u"Relay Type:")]

        # Label text for output data.
        self._out_labels = [u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
                            u"\u03BB<sub>b</sub>:", u"\u03C0<sub>Q</sub>:",
                            u"\u03C0<sub>E</sub>:"]

        # Derating points for the derating curve.  The list at position 0 is
        # for severe environments.  The list at position 1 is for benign
        # environments.
        self._derate_criteria = [[0.6, 0.6, 0.0], [0.9, 0.9, 0.0]]

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Solid State Relay Component
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

        # Create the input widgets.
        part.cmbQuality = _widg.make_combo(simple=True)
        part.txtCommercialPiQ = _widg.make_entry(width=100)
        # Create and populate the relay type combobox.  We store this in the
        # construction id field in the program database.
        part.cmbType = _widg.make_combo(simple=True)

        # Load all the gtk.ComboBox().
        for i in range(len(self._quality)):
            part.cmbQuality.insert_text(i, self._quality[i])
        for i in range(len(self._type)):
            part.cmbType.insert_text(i, self._type[i])

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._in_labels, layout, 5, y_pos)
        _x_pos = max(_x_pos, x_pos)

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.put(part.cmbQuality, _x_pos, _y_pos[0])
        layout.put(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.put(part.cmbType, _x_pos, _y_pos[2])

        # Connect to callback methods.
        part.cmbQuality.connect("changed", self._callback_combo, part, 85)
        part.txtCommercialPiQ.connect("focus-out-event", self._callback_entry,
                                      part, "float", 79)
        part.cmbType.connect("changed", self._callback_combo, part, 16)

        layout.show_all()

        return _x_pos, _y_pos

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Solid State Relay Component Class calculation
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

        # Create the reliability result display widgets.
        part.txtLambdaB = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        part.txtPiQ = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)

        # Create and place all the labels.
        (_x_pos, _y_pos) = _widg.make_labels(self._out_labels,
                                             layout, x_pos, y_pos)
        _x_pos += x_pos
        _x_pos -= 30

        # Place the reliability result display widgets.
        layout.put(part.txtLambdaB, _x_pos, _y_pos[1])
        layout.put(part.txtPiQ, _x_pos, _y_pos[2])
        layout.put(part.txtPiE, _x_pos, _y_pos[3])

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
        # (_x_pos, _y_pos) = _widg.make_labels(self._out_labels[:2], layout,
        #                                      5, y_pos)

        # Create the stress result display widgets.
        # part.txtTRise = _widg.make_entry(editable=False, bold=True)
        # part.txtTJunc = _widg.make_entry(editable=False, bold=True)

        # Place the stress result display widgets.
        # layout.put(part.txtTRise, 155, 305)
        # layout.put(part.txtTJunc, 155, 335)

        # layout.show_all()

        # Place the reliability result display widgets.
        layout.put(part.txtLambdaB, _x_pos, _y_pos[1])
        layout.put(part.txtPiQ, _x_pos, _y_pos[2])
        layout.put(part.txtPiE, _x_pos, _y_pos[3])

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
        part.cmbType.set_active(int(_model.get_value(_row, 16)))
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

        part.txtLambdaB.set_text(str(fmt.format(_model.get_value(_row, 46))))
        part.txtPiQ.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 79))))
        part.txtPiE.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 72))))

        part.txtOSReason.set_text(self.reason)

        part.graDerate.cla()

        return _model, _row

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Solid State Relay Component Class
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

        _model.set_value(_row, idx, int(_index))

        if idx == 85:                       # Quality
            if part.txtCommercialPiQ.get_text() == "":
                CpiQ = 0.0
            else:
                CpiQ = float(part.txtCommercialPiQ.get_text())

            # Use this value for piQ if not being over-ridden.
            if CpiQ <= 0.0:
                _model.set_value(_row, 79, self._piQ[_index])

        return False

    def _callback_entry(self, entry, event, part, convert, idx):
        """
        Callback function for handling Solid State Relay Component Class
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
        if convert == "text":
            _model.set_value(_row, idx, entry.get_text())

        elif convert == "int":
            _model.set_value(_row, idx, int(entry.get_text()))

        elif convert == "float":
            _model.set_value(_row, idx, float(entry.get_text()))

        # Commercial PiQ entry called the function.
        if _index_ == 79:
            CpiQ = float(entry.get_text())

            # Use this value for piQ if it is greater than zero.
            if CpiQ > 0:
                _model.set_value(_row, 79, CpiQ)

        return False

    def calculate(self, partmodel, partrow, systemmodel, systemrow):
        """
        Performs hazard rate calculations for the Fixed Paper Bypass Capacitor
        class.

        :param gtk.TreeModel partmodel: the RTK List class gtk.TreeModel().
        :param gtk.TreeIter partrow: the currently selected gtk.TreeIter()
                                     in List class gtk.TreeModel().
        :param gtk.TreeModel systemmodel: the RTK Hardware class
                                          gtk.TreeModel().
        :param gtk.TreeIter systemrow: the currently selected
                                       gtk.TreeIter() in the RTK Hardware
                                       class gtk.TreeModel().
        :return: False if succussful or True if an error is encountered.
        :rtype: boolean
        """

        def _calculate_mil_217_count(partmodel, partrow,
                                     systemmodel, systemrow):
            """
            Performs MIL-HDBK-217F part count hazard rate calculations for the
            Linear Integrated Circuit Class.

            :param gtk.TreeModel partmodel: the RTK List class gtk.TreeModel().
            :param gtk.TreeIter partrow: the currently selected gtk.TreeIter()
                                         in List class gtk.TreeModel().
            :param gtk.TreeModel systemmodel: the RTK Hardware class
                                              gtk.TreeModel().
            :param gtk.TreeIter systemrow: the currently selected
                                           gtk.TreeIter() in the RTK Hardware
                                           class gtk.TreeModel().
            :return: False if succussful or True if an error is encountered.
            :rtype: boolean
            """

            _hrmodel = {}
            _hrmodel['equation'] = "lambdab * piQ"

            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hazard rate inputs.
            Cidx = partmodel.get_value(partrow, 16)         # Construction (type) index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Cidx - 1][Eidx - 1]

            # Calculate component active hazard rate.
            _lambdaa = _calc.calculate_part(_hrmodel)
            _lambdaa = _lambdaa * _quantity / 1000000.0

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

            systemmodel.set_value(systemrow, 28, _lambdaa)
            systemmodel.set_value(systemrow, 32, _lambdaa)
            systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

            return False

        def _calculate_mil_217_stress(partmodel, partrow,
                                      systemmodel, systemrow):
            """
            Performs MIL-HDBK-217F part stress hazard rate calculations for
            the Solid State Relay Component Class.

            :param gtk.TreeModel partmodel: the RTK List class gtk.TreeModel().
            :param gtk.TreeIter partrow: the currently selected gtk.TreeIter()
                                         in List class gtk.TreeModel().
            :param gtk.TreeModel systemmodel: the RTK Hardware class
                                              gtk.TreeModel().
            :param gtk.TreeIter systemrow: the currently selected
                                           gtk.TreeIter() in the RTK Hardware
                                           class gtk.TreeModel().
            :return: False if succussful or True if an error is encountered.
            :rtype: boolean
            """

            _hrmodel = {}
            _hrmodel['equation'] = "lambdab * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hazard rate inputs.
            Cyc = partmodel.get_value(partrow, 19)
            Tamb = partmodel.get_value(partrow, 37)
            Iapplied = partmodel.get_value(partrow, 62)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Irated = partmodel.get_value(partrow, 92)

            # Base hazard rate.
            idx = partmodel.get_value(partrow, 16)
            if idx == 1:                    # Solid State
                _hrmodel['lambdab'] = 0.40
            elif idx == 2:                  # Solid State Time Delay
                _hrmodel['lambdab'] = 0.50
            elif idx == 3:                  # Hybrid
                _hrmodel['lambdab'] = 0.50

            # Environmental correction factor.
            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

            # Calculate component active hazard rate.
            _lambdaa = _calc.calculate_part(_hrmodel)
            _lambdaa = _lambdaa * _quantity / 1000000.0

            # Calculate the component dormant hazard rate.
            _lambdad = _calc.dormant_hazard_rate(_category_id, _subcategory_id,
                                                 _active_env, _dormant_env,
                                                 _lambdaa)

            # Calculate the component predicted hazard rate.
            _lambdap = _lambdaa + _lambdad + _lambdas

            # Calculate overstresses.
            (_overstress,
             self.reason) = _calc.overstressed(partmodel, partrow,
                                               systemmodel, systemrow)

            # Calculate operating point ratios.
            _i_ratio = Iapplied / Irated

            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])

            systemmodel.set_value(systemrow, 28, _lambdaa)
            systemmodel.set_value(systemrow, 29, _lambdad)
            systemmodel.set_value(systemrow, 32, _lambdap)
            systemmodel.set_value(systemrow, 60, _overstress)
            systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

            return False

        _calc_model = systemmodel.get_value(systemrow, 10)

        if _calc_model == 1:
            _calculate_mil_217_stress(partmodel, partrow,
                                      systemmodel, systemrow)
        elif _calc_model == 2:
            _calculate_mil_217_count(partmodel, partrow,
                                     systemmodel, systemrow)

        return False
