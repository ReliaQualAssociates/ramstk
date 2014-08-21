#!/usr/bin/env python

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       variable.py is part of The RTK Project
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
from resistor import Resistor

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except ImportError:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class VarWirewound(Resistor):
    """
    Variable Value Wirewound Resistor Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.9
    """

    _quality = ["", "S", "R", "P", "M", "MIL-R-27208", _(u"Lower")]
    _range = ["", "10 - 2.0K", "2.0K - 5.0K", "5.0K - 20.0K"]
    _specification = ["", "MIL-R-39015 (RTR)", "MIL-R-27208 (RE)"]
    _specsheet = [["", "RTR12", "RTR22", "RTR24"],
                  ["", "RT12", "RT22", "RT26", "RT27"]]

    def __init__(self):
        """
        Initializes the Variable Value Wirewound Resistor Component Class.
        """

        Resistor.__init__(self)

        self.subcategory = 33               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piR = [1.0, 1.4, 2.0]
        self._piE = [1.0, 2.0, 12.0, 6.0, 20.0, 5.0, 8.0, 9.0, 15.0, 33.0, 0.5,
                     18.0, 48.0, 870.0]
        self._piQ = [0.02, 0.06, 0.2, 0.6, 3.0, 10.0]
        self._lambdab_count = [0.025, 0.055, 0.35, 0.15, 0.58, 0.16, 0.26,
                               0.35, 0.58, 1.1, 0.013, 0.52, 1.6, 24.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Nominal Resistance (\u03A9):"))
        self._in_labels.append(_(u"Specification:"))
        self._in_labels.append(_(u"Spec Sheet:"))
        self._in_labels.append(_(u"Number of Taps:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>TAPS</sub>")
        self._out_labels.append(u"\u03C0<sub>V</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Variable Value Wirewound
        Resistor Component Class prediction calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Resistor.assessment_inputs_create(self, part, layout,
                                                     x_pos, y_pos)

        # Create instance-specific input widgets.
        part.txtResistance = _widg.make_entry(width=100)
        part.cmbSpecification = _widg.make_combo(simple=True)
        part.cmbSpecSheet = _widg.make_combo(simple=True)
        part.txtNTaps = _widg.make_entry(width=100)

        # Load all gtk.ComboBox().
        for i in range(len(self._specification)):
            part.cmbSpecification.insert_text(i, self._specification[i])

        # Place the instance-specific input widgets.
        layout.put(part.txtResistance, _x_pos, _y_pos[4])
        layout.put(part.cmbSpecification, _x_pos, _y_pos[5])
        layout.put(part.cmbSpecSheet, _x_pos, _y_pos[6])
        layout.put(part.txtNTaps, _x_pos, _y_pos[7])

        part.txtResistance.connect("focus-out-event", self._callback_entry,
                                   part, "float", 95)
        part.cmbSpecification.connect("changed", self._callback_combo,
                                      part, 101)
        part.cmbSpecSheet.connect("changed", self._callback_combo, part, 102)
        part.txtNTaps.connect("focus-out-event", self._callback_entry,
                              part, "float", 57)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Variable Value Resistor Component Class
        calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos, _y_pos) = Resistor.reliability_results_create(self, part,
                                                               layout,
                                                               x_pos, y_pos)

        # Create the reliability result display widgets.
        # Create the Pi TAPS results entry.  We use the pi_u field
        # in the program database to the results.
        part.txtPiTAPS = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiV = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the reliability result display widgets.
        layout.put(part.txtPiTAPS, _x_pos, _y_pos[5])
        layout.put(part.txtPiV, _x_pos, _y_pos[6])

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with
        calculation input information.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Resistor.assessment_inputs_load(self, part)

        part.txtResistance.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 95))))
        part.cmbSpecification.set_active(int(_model.get_value(_row, 101)))
        part.cmbSpecSheet.set_active(int(_model.get_value(_row, 102)))
        part.txtNTaps.set_text(str("{0:0.0g}".format(
            _model.get_value(_row, 57))))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Resistor.assessment_results_load(self, part)

        part.txtPiTAPS.set_text(str(fmt.format(_model.get_value(_row, 82))))
        part.txtPiV.set_text(str(fmt.format(_model.get_value(_row, 83))))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Variable Value Resistor Component
        Class ComboBox changes.

        :param gtk.ComboBox combo: the gtk.ComboBox() calling this method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param int idx: the user-defined index for the calling combobx.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        Resistor._callback_combo(self, combo, part, idx)

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        _index = combo.get_active()

        if idx == 101:                      # Specification
            for i in range(len(self._specsheet[_index - 1])):
                part.cmbSpecSheet.insert_text(i,
                                              self._specsheet[_index - 1][i])

        elif idx == 102:                     # Specification sheet
            _index2 = _model.get_value(_row, 101)

            if _index2 == 1:                # RTR
                _model.set_value(_row, 94, 90.0)
            elif _index2 == 2:              # RT
                if _index == 1 or _index == 2:
                    _model.set_value(_row, 94, 90.0)
                elif _index == 3 or _index == 4:
                    _model.set_value(_row, 94, 40.0)
                else:
                    _model.set_value(_row, 94, 1.0)
            else:
                _model.set_value(_row, 94, 1.0)

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
            Variable Value Wirewound Resistor Component Class.

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
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

            # Calculate component hazard rate.
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
            the Variable Value Wirewound Resistor Component Class.

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
            _hrmodel['equation'] = "lambdab * piTAPS * piR * piV * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve junction temperature inputs.
            Tamb = partmodel.get_value(partrow, 37)
            P = partmodel.get_value(partrow, 64)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            Ntaps = partmodel.get_value(partrow, 57)
            Vapplied = partmodel.get_value(partrow, 66)
            _hrmodel['piR'] = partmodel.get_value(partrow, 80)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Prated = partmodel.get_value(partrow, 93)
            Vrated = partmodel.get_value(partrow, 94)
            R = partmodel.get_value(partrow, 95)

            # Base hazard rate
            S = P / Prated
            _hrmodel['lambdab'] = 0.0062 * exp(((Tamb + 273) / 298)**5.0) * exp(S * ((Tamb + 273) / 273))

            # Potentiometer taps correction factor.
            _hrmodel['piTAPS'] = ((Ntaps ** 1.5) / 25.0) + 0.792

            # Voltage correction factor.
            Vratio = Vapplied / Vrated
            if Vratio > 0.0 and Vratio <= 0.1:
                _hrmodel['piV'] = 1.00
            elif Vratio > 0.1 and Vratio <= 0.2:
                _hrmodel['piV'] = 1.05
            elif Vratio > 0.2 and Vratio <= 0.6:
                _hrmodel['piV'] = 1.00
            elif Vratio > 0.6 and Vratio <= 0.7:
                _hrmodel['piV'] = 1.10
            elif Vratio > 0.7 and Vratio <= 0.8:
                _hrmodel['piV'] = 1.22
            elif Vratio > 0.8 and Vratio <= 0.9:
                _hrmodel['piV'] = 1.40
            elif Vratio > 0.9 and Vratio <= 1.0:
                _hrmodel['piV'] = 2.00

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
            _lambdad = _lambdad * _quantity

            # Calculate the component predicted hazard rate.
            _lambdap = _lambdaa + _lambdad + _lambdas

            # Calculate overstresses.
            (_overstress,
             self.reason) = _calc.overstressed(partmodel, partrow,
                                               systemmodel, systemrow)

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 66, Vapplied)
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piR'])
            partmodel.set_value(partrow, 82, _hrmodel['piTAPS'])
            partmodel.set_value(partrow, 83, _hrmodel['piV'])
            partmodel.set_value(partrow, 111, Vratio)

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


class VarWirewoundPower(Resistor):
    """
    Variable Value Wirewound Power Resistor Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.12
    """

    _construction = ["", _(u"Enclosed"), _(u"Unenclosed")]
    _quality = ["", "MIL-SPEC", _(u"Lower")]
    _range = ["", "1 - 2.0K", ">2.0K - 5.0K", ">5.0K - 10.0K"]
    _specsheet = ["", "RR0900", "RR1000", "RR1100", "RR1300", "RR1400",
                  "RR2000", "RR2100", "RR3000", "RR3100", "RR3200", "RR3300",
                  "RR3400", "RR3500", "RR3600", "RR3700", "RR3800", "RR3900"]

    def __init__(self):
        """
        Initializes the Variable Value Wirewound Power Resistor Component
        Class.
        """

        Resistor.__init__(self)

        self.subcategory = 33               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piC = [2.0, 1.0]
        self._piR = [1.0, 1.4, 2.0]
        self._piE = [1.0, 3.0, 16.0, 7.0, 28.0, 8.0, 12.0, 0.0, 0.0, 38.0,
                     0.5, 0.0, 0.0, 0.0]
        self._piQ = [2.0, 4.0]
        self._lambdab_count = [0.15, 0.34, 2.9, 1.2, 5.0, 1.6, 2.4, 0.0, 0.0,
                               7.6, 0.076, 0.0, 0.0, 0.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Nominal Resistance (\u03A9):"))
        self._in_labels.append(_(u"Construction:"))
        self._in_labels.append(_(u"Number of Taps:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>C</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>TAPS</sub>")
        self._out_labels.append(u"\u03C0<sub>C</sub>")
        self._out_labels.append(u"\u03C0<sub>V</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Variable Value Wirewound Power
        Resistor Component Class prediction calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Resistor.assessment_inputs_create(self, part, layout,
                                                     x_pos, y_pos)

        # Create input widgets.
        part.txtResistance = _widg.make_entry(width=100)
        part.cmbConstruction = _widg.make_combo(simple=True)
        part.txtNTaps = _widg.make_entry(width=100)

        # Load all gtk.ComboBox().
        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])

        # Place the input widgets.
        layout.put(part.txtResistance, _x_pos, _y_pos[4])
        layout.put(part.cmbConstruction, _x_pos, _y_pos[5])
        layout.put(part.txtNTaps, _x_pos, _y_pos[6])

        # Connect widgets to callback methods.
        part.txtResistance.connect("focus-out-event", self._callback_entry,
                                   part, "float", 95)
        part.cmbConstruction.connect("changed", self._callback_combo, part, 16)
        part.txtNTaps.connect("focus-out-event", self._callback_entry,
                              part, "float", 57)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Variable Value Wirewound Power Resistor
        Component Class calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos, _y_pos) = Resistor.reliability_results_create(self, part,
                                                               layout,
                                                               x_pos, y_pos)

        # Create the reliability result display widgets.
        # Create the Pi TAPS results entry.  We use the pi_u field
        # in the program database to the results.
        part.txtPiTAPS = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiC = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiV = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the reliability result display widgets.
        layout.put(part.txtPiTAPS, _x_pos, _y_pos[5])
        layout.put(part.txtPiC, _x_pos, _y_pos[6])
        layout.put(part.txtPiV, _x_pos, _y_pos[7])

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with
        calculation input information.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Resistor.assessment_inputs_load(self, part)

        part.txtResistance.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 95))))
        part.cmbConstruction.set_active(int(_model.get_value(_row, 16)))
        part.txtNTaps.set_text(str("{0:0.0g}".format(
            _model.get_value(_row, 57))))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Resistor.assessment_results_load(self, part)

        part.txtPiC.set_text(str("{0:0.2e}".format(
            _model.get_value(_row, 69))))
        part.txtPiTAPS.set_text(str(fmt.format(_model.get_value(_row, 82))))
        part.txtPiV.set_text(str(fmt.format(_model.get_value(_row, 83))))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Variable Value Wirewound Power
        Resistor Component Class ComboBox changes.

        :param gtk.ComboBox combo: the gtk.ComboBox() calling this method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param int idx: the user-defined index for the calling combobx.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        Resistor._callback_combo(self, combo, part, idx)

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        _index = combo.get_active()

        if idx == 16:                       # Construction
            _model.set_value(_row, 69, self._piC[_index - 1])

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
            Variable Value Wirewound Power Resistor Component Class.

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
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

            # Calculate component hazard rate.
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
            the Variable Value Wirewound Power Resistor Component Class.

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
            _hrmodel['equation'] = "lambdab * piTAPS * piR * piV * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve junction temperature inputs.
            Tamb = partmodel.get_value(partrow, 37)
            P = partmodel.get_value(partrow, 64)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            Ntaps = partmodel.get_value(partrow, 57)
            Vapplied = partmodel.get_value(partrow, 66)
            _hrmodel['piC'] = partmodel.get_value(partrow, 69)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            _hrmodel['piR'] = partmodel.get_value(partrow, 80)
            Prated = partmodel.get_value(partrow, 93)
            Vrated = partmodel.get_value(partrow, 94)
            R = partmodel.get_value(partrow, 95)

            # Base hazard rate
            S = P / Prated
            _hrmodel['lambdab'] = 0.0481 * exp(0.334 * ((Tamb + 273) / 298)**4.66) * exp((S / 1.47) * ((Tamb + 273) / 273)**2.83)

            # Potentiometer taps correction factor.
            _hrmodel['piTAPS'] = ((Ntaps ** 1.5) / 25.0) + 0.792

            # Voltage correction factor.
            Vratio = Vapplied / Vrated
            if Vratio > 0.0 and Vratio <= 0.1:
                _hrmodel['piV'] = 1.10
            elif Vratio > 0.1 and Vratio <= 0.2:
                _hrmodel['piV'] = 1.05
            elif Vratio > 0.2 and Vratio <= 0.6:
                _hrmodel['piV'] = 1.00
            elif Vratio > 0.6 and Vratio <= 0.7:
                _hrmodel['piV'] = 1.10
            elif Vratio > 0.7 and Vratio <= 0.8:
                _hrmodel['piV'] = 1.22
            elif Vratio > 0.8 and Vratio <= 0.9:
                _hrmodel['piV'] = 1.40
            elif Vratio > 0.9 and Vratio <= 1.0:
                _hrmodel['piV'] = 2.00

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
            _lambdad = _lambdad * _quantity

            # Calculate the component predicted hazard rate.
            _lambdap = _lambdaa + _lambdad + _lambdas

            # Calculate overstresses.
            (_overstress,
             self.reason) = _calc.overstressed(partmodel, partrow,
                                               systemmodel, systemrow)

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 66, Vapplied)
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piR'])
            partmodel.set_value(partrow, 82, _hrmodel['piTAPS'])
            partmodel.set_value(partrow, 83, _hrmodel['piV'])
            partmodel.set_value(partrow, 111, Vratio)

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


class WirewoundPrecision(Resistor):
    """
    Variable Value Precision Wirewound Resistor Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.10
    """

    _construction = ["", _(u"Class 2"), _(u"Class 3"), _(u"Class 4"),
                     _(u"Class 5")]
    _quality = ["", "MIL-SPEC", _(u"Lower")]
    _range = ["", "100 - 10.0K", "10.0K - 20.0K", "20.0K - 50.0K",
              "50.0K - 100.0K", "100.0K - 200.0K", "200.0K - 500.0K"]
    _specsheet = ["", "RR0900", "RR1000", "RR1100", "RR1300", "RR1400",
                  "RR2000", "RR2100", "RR3000", "RR3100", "RR3200", "RR3300",
                  "RR3400", "RR3500", "RR3600", "RR3700", "RR3800", "RR3900"]

    def __init__(self):
        """
        Initializes the Variable Value Precision Wirewound Resistor Component
        Class.
        """

        Resistor.__init__(self)

        self.subcategory = 33               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piC = [2.0, 1.0, 3.0, 1.5]
        self._piR = [1.0, 1.1, 1.4, 2.0, 2.5, 3.5]
        self._piE = [1.0, 2.0, 18.0, 8.0, 30.0, 8.0, 12.0, 13.0, 18.0, 53.0,
                     0.5, 29.0, 76.0, 1400.0]
        self._piQ = [2.5, 5.0]
        self._lambdab_count = [0.33, 0.73, 7.0, 2.9, 12.0, 3.5, 5.3, 7.1, 9.8,
                               23.0, 0.16, 11.0, 33.0, 510.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Nominal Resistance (\u03A9):"))
        self._in_labels.append(_(u"Spec Sheet:"))
        self._in_labels.append(_(u"Construction:"))
        self._in_labels.append(_(u"Number of Taps:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>C</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>TAPS</sub>")
        self._out_labels.append(u"\u03C0<sub>C</sub>")
        self._out_labels.append(u"\u03C0<sub>V</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Variable Value Precision
        Wirewound Resistor Component Class prediction calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Resistor.assessment_inputs_create(self, part, layout,
                                                     x_pos, y_pos)

        # Create input widgets.
        part.txtResistance = _widg.make_entry(width=100)
        part.cmbSpecSheet = _widg.make_combo(simple=True)
        part.cmbConstruction = _widg.make_combo(simple=True)
        part.txtNTaps = _widg.make_entry(width=100)

        # Load all gtk.ComboBox().
        for i in range(len(self._specsheet)):
            part.cmbSpecSheet.insert_text(i, self._specsheet[i])
        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])

        # Place the input widgets.
        layout.put(part.txtResistance, _x_pos, _y_pos[4])
        layout.put(part.cmbSpecSheet, _x_pos, _y_pos[5])
        layout.put(part.cmbConstruction, _x_pos, _y_pos[6])
        layout.put(part.txtNTaps, _x_pos, _y_pos[7])

        # Connect widgets to callback methods.
        part.txtResistance.connect("focus-out-event", self._callback_entry,
                                   part, "float", 95)
        part.cmbSpecSheet.connect("changed", self._callback_combo, part, 102)
        part.cmbConstruction.connect("changed", self._callback_combo, part, 16)
        part.txtNTaps.connect("focus-out-event", self._callback_entry,
                              part, "float", 57)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Variable Value Precision Wirewound Resistor
        Component Class calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos, _y_pos) = Resistor.reliability_results_create(self, part,
                                                               layout,
                                                               x_pos, y_pos)

        # Create the reliability result display widgets.
        # Create the Pi TAPS results entry.  We use the pi_u field
        # in the program database to the results.
        part.txtPiTAPS = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiC = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiV = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the reliability result display widgets.
        layout.put(part.txtPiTAPS, _x_pos, _y_pos[5])
        layout.put(part.txtPiC, _x_pos, _y_pos[6])
        layout.put(part.txtPiV, _x_pos, _y_pos[7])

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with
        calculation input information.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Resistor.assessment_inputs_load(self, part)

        part.cmbConstruction.set_active(int(_model.get_value(_row, 16)))
        part.txtNTaps.set_text(str("{0:0.0g}".format(
            _model.get_value(_row, 57))))
        part.txtResistance.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 95))))
        part.cmbSpecSheet.set_active(int(_model.get_value(_row, 102)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Resistor.assessment_results_load(self, part)

        part.txtPiC.set_text(str("{0:0.2e}".format(
            _model.get_value(_row, 69))))
        part.txtPiTAPS.set_text(str(fmt.format(_model.get_value(_row, 82))))
        part.txtPiV.set_text(str(fmt.format(_model.get_value(_row, 83))))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Variable Value Precision Wirewound
        Resistor Component Class ComboBox changes.

        :param gtk.ComboBox combo: the gtk.ComboBox() calling this method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param int idx: the user-defined index for the calling combobx.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        Resistor._callback_combo(self, combo, part, idx)

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        _index = combo.get_active()

        if idx == 16:                       # Construction
            _model.set_value(_row, 69, self._piC[_index - 1])

        elif idx == 102:                    # Specification sheet
            if(_index == 1 or _index == 3 or _index == 4 or _index == 6 or
               _index == 8 or _index == 9 or _index == 10 or _index == 11 or
               _index == 12 or _index == 13):
                _model.set_value(_row, 94, 250.0)
            elif _index == 14 or _index == 15:
                _model.set_value(_row, 94, 423.0)
            elif(_index == 2 or _index == 5 or _index == 7 or _index == 16 or
                 _index == 17):
                _model.set_value(_row, 94, 500.0)
            else:
                _model.set_value(_row, 94, 1.0)

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
            Variable Value Precision Wirewound Resistor Component Class.

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
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

            # Calculate component hazard rate.
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
            the Variable Value Precision Wirewound Resistor Component Class.

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
            _hrmodel['equation'] = "lambdab * piQ * piC * piR * piTAPS * piE * piV"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve junction temperature inputs.
            Tamb = partmodel.get_value(partrow, 37)
            P = partmodel.get_value(partrow, 64)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            Ntaps = partmodel.get_value(partrow, 57)
            Vapplied = partmodel.get_value(partrow, 66)
            _hrmodel['piC'] = partmodel.get_value(partrow, 69)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            _hrmodel['piR'] = partmodel.get_value(partrow, 80)
            Prated = partmodel.get_value(partrow, 93)
            Vrated = partmodel.get_value(partrow, 94)
            R = partmodel.get_value(partrow, 95)

            # Base hazard rate
            S = P / Prated
            _hrmodel['lambdab'] = 0.0735 * exp(1.03 * ((Tamb + 273.0) / 298.0)**4.45) * exp((S / 2.74) * ((Tamb + 273.0) / 273.0)**3.51)

            # Potentiometer taps correction factor.
            _hrmodel['piTAPS'] = ((Ntaps ** 1.5) / 25.0) + 0.792

            # Voltage correction factor.
            try:
                Vratio = Vapplied / Vrated
            except:
                Vratio = 1.0

            if Vratio > 0.0 and Vratio <= 0.1:
                _hrmodel['piV'] = 1.10
            elif Vratio > 0.1 and Vratio <= 0.2:
                _hrmodel['piV'] = 1.05
            elif Vratio > 0.2 and Vratio <= 0.6:
                _hrmodel['piV'] = 1.00
            elif Vratio > 0.6 and Vratio <= 0.7:
                _hrmodel['piV'] = 1.10
            elif Vratio > 0.7 and Vratio <= 0.8:
                _hrmodel['piV'] = 1.22
            elif Vratio > 0.8 and Vratio <= 0.9:
                _hrmodel['piV'] = 1.40
            elif Vratio > 0.9 and Vratio <= 1.0:
                _hrmodel['piV'] = 2.00

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
            _lambdad = _lambdad * _quantity

            # Calculate the component predicted hazard rate.
            _lambdap = _lambdaa + _lambdad + _lambdas

            # Calculate overstresses.
            (_overstress,
             self.reason) = _calc.overstressed(partmodel, partrow,
                                               systemmodel, systemrow)

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 66, Vapplied)
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piR'])
            partmodel.set_value(partrow, 82, _hrmodel['piTAPS'])
            partmodel.set_value(partrow, 83, _hrmodel['piV'])
            partmodel.set_value(partrow, 111, Vratio)

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


class WirewoundSemiPrecision(Resistor):
    """
    Variable Value Semiprecision Wirewound Resistor Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.11
    """

    _quality = ["", "MIL-SPEC", _(u"Lower")]
    _range = ["", "10 - 2.0K", ">2.0K - 5.0K", ">5.0K - 10.0K"]
    _specsheet = ["", "RA10", "RA20X-XA", "RA20X-XC, F", "RA30X-XA",
                  "RA30X-XC, F", "RK09"]

    def __init__(self):

        Resistor.__init__(self)

        self.subcategory = 35               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piR = [1.0, 1.4, 2.0]
        self._piE = [1.0, 2.0, 16.0, 7.0, 28.0, 8.0, 12.0, 0.0, 0.0, 38.0,
                     0.5, 0.0, 0.0, 0.0]
        self._piQ = [2.0, 4.0]
        self._lambdab_count = [0.15, 0.35, 3.1, 1.2, 5.4, 1.9, 2.8, 0.0, 0.0,
                               9.0, 0.075, 0.0, 0.0, 0.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Nominal Resistance (\u03A9):"))
        self._in_labels.append(_(u"Spec Sheet:"))
        self._in_labels.append(_(u"Number of Taps:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>TAPS</sub>")
        self._out_labels.append(u"\u03C0<sub>V</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Variable Value Semiprecision
        Wirewound Resistor Component Class prediction calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Resistor.assessment_inputs_create(self, part, layout,
                                                     x_pos, y_pos)

        # Create input widgets.
        part.txtResistance = _widg.make_entry(width=100)
        part.cmbSpecSheet = _widg.make_combo(simple=True)
        part.txtNTaps = _widg.make_entry(width=100)

        # Load all gtk.ComboBox().
        for i in range(len(self._specsheet)):
            part.cmbSpecSheet.insert_text(i, self._specsheet[i])

        # Place the input widgets.
        layout.put(part.txtResistance, _x_pos, _y_pos[4])
        layout.put(part.cmbSpecSheet, _x_pos, _y_pos[5])
        layout.put(part.txtNTaps, _x_pos, _y_pos[6])

        # Connect widgets to callback methods.
        part.txtResistance.connect("focus-out-event", self._callback_entry,
                                   part, "float", 95)
        part.cmbSpecSheet.connect("changed", self._callback_combo, part, 102)
        part.txtNTaps.connect("focus-out-event", self._callback_entry,
                              part, "float", 57)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Variable Value Semiprecision Wirewound Resistor
        Component Class calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos, _y_pos) = Resistor.reliability_results_create(self, part,
                                                               layout,
                                                               x_pos, y_pos)

        # Create the reliability result display widgets.
        # Create the Pi TAPS results entry.  We use the pi_u field
        # in the program database to the results.
        part.txtPiTAPS = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiV = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the reliability result display widgets.
        layout.put(part.txtPiTAPS, _x_pos, _y_pos[5])
        layout.put(part.txtPiV, _x_pos, _y_pos[6])

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with
        calculation input information.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Resistor.assessment_inputs_load(self, part)

        part.txtNTaps.set_text(str("{0:0.0g}".format(
            _model.get_value(_row, 57))))
        part.txtResistance.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 95))))
        part.cmbSpecSheet.set_active(int(_model.get_value(_row, 102)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Resistor.assessment_results_load(self, part)

        part.txtPiTAPS.set_text(str(fmt.format(_model.get_value(_row, 82))))
        part.txtPiV.set_text(str(fmt.format(_model.get_value(_row, 83))))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Variable Value Semiprecision
        Wirewound Resistor Component Class ComboBox changes.

        :param gtk.ComboBox combo: the gtk.ComboBox() calling this method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param int idx: the user-defined index for the calling combobx.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        Resistor._callback_combo(self, combo, part, idx)

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        _index = combo.get_active()

        if idx == 102:                      # Specification sheet
            if _index == 1:
                _model.set_value(_row, 94, 50.0)
            elif _index == 2:
                _model.set_value(_row, 94, 175.0)
            elif _index == 3:
                _model.set_value(_row, 94, 75.0)
            elif _index == 4:
                _model.set_value(_row, 94, 320.0)
            elif _index == 5:
                _model.set_value(_row, 94, 130.0)
            elif _index == 6:
                _model.set_value(_row, 94, 275.0)
            else:
                _model.set_value(_row, 94, 1.0)

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
            Variable Value Semiprecision Wirewound Resistor Component Class.

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
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

            # Calculate component hazard rate.
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
            the Variable Value Semiprecision Wirewound Resistor Component Class.

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
            _hrmodel['equation'] = "lambdab * piTAPS * piR * piV * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve junction temperature inputs.
            Tamb = partmodel.get_value(partrow, 37)
            P = partmodel.get_value(partrow, 64)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            Ntaps = partmodel.get_value(partrow, 57)
            _hrmodel['piC'] = partmodel.get_value(partrow, 69)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            _hrmodel['piR'] = partmodel.get_value(partrow, 80)
            Prated = partmodel.get_value(partrow, 93)
            Vrated = partmodel.get_value(partrow, 94)
            R = partmodel.get_value(partrow, 95)

            # Base hazard rate
            S = P / Prated
            _hrmodel['lambdab'] = 0.0398 * exp(0.514 * ((Tamb + 273) / 313)**5.28) * exp((S / 1.44) * ((Tamb + 273) / 273)**4.46)

            # Potentiometer taps correction factor.
            _hrmodel['piTAPS'] = ((Ntaps ** 1.5) / 25.0) + 0.792

            # Voltage correction factor.
            Vapplied = sqrt(R * P)
            Vratio = Vapplied / Vrated
            if Vratio > 0.0 and Vratio <= 0.1:
                _hrmodel['piV'] = 1.10
            elif Vratio > 0.1 and Vratio <= 0.2:
                _hrmodel['piV'] = 1.05
            elif Vratio > 0.2 and Vratio <= 0.6:
                _hrmodel['piV'] = 1.00
            elif Vratio > 0.6 and Vratio <= 0.7:
                _hrmodel['piV'] = 1.10
            elif Vratio > 0.7 and Vratio <= 0.8:
                _hrmodel['piV'] = 1.22
            elif Vratio > 0.8 and Vratio <= 0.9:
                _hrmodel['piV'] = 1.40
            elif Vratio > 0.9 and Vratio <= 1.0:
                _hrmodel['piV'] = 2.00

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
            _lambdad = _lambdad * _quantity

            # Calculate the component predicted hazard rate.
            _lambdap = _lambdaa + _lambdad + _lambdas

            # Calculate overstresses.
            (_overstress,
             self.reason) = _calc.overstressed(partmodel, partrow,
                                               systemmodel, systemrow)

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 66, Vapplied)
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piR'])
            partmodel.set_value(partrow, 82, _hrmodel['piTAPS'])
            partmodel.set_value(partrow, 83, _hrmodel['piV'])
            partmodel.set_value(partrow, 111, Vratio)

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


class NonWirewound(Resistor):
    """
    Variable Value Nonwirewound Resistor Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.15
    """

    _quality = ["", "S", "R", "P", "M", "MIL-R-22097", _(u"Lower")]
    _range = ["", "10 - 50.0K", ">50.0K - 100.0K", ">100.0K - 200.0K",
              ">200.0K - 500.0K", ">500.0K - 1.0M"]
    _specsheet = ["", "RJ28", "RJ50", "RJR28", "RJR50", "Other"]

    def __init__(self):
        """
        Initializes the Variable Value NonWirewound Resistor Component Class.
        """

        Resistor.__init__(self)

        self.subcategory = 37               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piR = [1.0, 1.1, 1.2, 1.4, 1.8]
        self._piE = [1.0, 3.0, 14.0, 6.0, 24.0, 5.0, 7.0, 12.0, 18.0, 39.0,
                     0.5, 22.0, 57.0, 1000.0]
        self._piQ = [0.02, 0.06, 0.2, 0.6, 3.0, 10.0]
        self._lambdab_count = [0.043, 0.15, 0.75, 0.35, 1.3, 0.39, 0.78, 1.8,
                               2.8, 2.5, 0.21, 1.2, 3.7, 49.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Nominal Resistance (\u03A9):"))
        self._in_labels.append(_(u"Spec Sheet:"))
        self._in_labels.append(_(u"Number of Taps:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>TAPS</sub>")
        self._out_labels.append(u"\u03C0<sub>V</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Variable Value Nonwirewound
        Resistor Component Class prediction calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Resistor.assessment_inputs_create(self, part, layout,
                                                     x_pos, y_pos)

        # Create input widgets.
        part.txtResistance = _widg.make_entry(width=100)
        part.cmbSpecSheet = _widg.make_combo(simple=True)
        part.txtNTaps = _widg.make_entry(width=100)

        # Load all gtk.ComboBox().
        for i in range(len(self._specsheet)):
            part.cmbSpecSheet.insert_text(i, self._specsheet[i])

        # Place the input widgets.
        layout.put(part.txtResistance, _x_pos, _y_pos[4])
        layout.put(part.cmbSpecSheet, _x_pos, _y_pos[5])
        layout.put(part.txtNTaps, _x_pos, _y_pos[6])

        # Connect widgets to callback methods.
        part.txtResistance.connect("focus-out-event", self._callback_entry,
                                   part, 'float', 95)
        part.cmbSpecSheet.connect("changed", self._callback_combo, part, 102)
        part.txtNTaps.connect("focus-out-event", self._callback_entry,
                              part, "float", 57)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Variable Value Nonwirewound Resistor Component
        Class calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos, _y_pos) = Resistor.reliability_results_create(self, part,
                                                               layout,
                                                               x_pos, y_pos)

        # Create the reliability result display widgets.
        # Create the Pi TAPS results entry.  We use the pi_u field
        # in the program database to the results.
        part.txtPiTAPS = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiV = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the reliability result display widgets.
        layout.put(part.txtPiTAPS, _x_pos, _y_pos[5])
        layout.put(part.txtPiV, _x_pos, _y_pos[6])

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with
        calculation input information.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Resistor.assessment_inputs_load(self, part)

        part.txtResistance.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 95))))
        part.cmbSpecSheet.set_active(int(_model.get_value(_row, 102)))
        part.txtNTaps.set_text(str("{0:0.0g}".format(
            _model.get_value(_row, 57))))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Resistor.assessment_results_load(self, part)

        part.txtPiTAPS.set_text(str(fmt.format(_model.get_value(_row, 82))))
        part.txtPiV.set_text(str(fmt.format(_model.get_value(_row, 83))))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Variable Value Nonwirewound Resistor
        Component Class ComboBox changes.

        :param gtk.ComboBox combo: the gtk.ComboBox() calling this method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param int idx: the user-defined index for the calling combobx.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        Resistor._callback_combo(self, combo, part, idx)

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        _index = combo.get_active()

        if idx == 102:                  # Specification sheet
            if _index == 1 or _index == 2 or _index == 3 or _index == 4:
                _model.set_value(_row, 94, 200.0)
            else:
                _model.set_value(_row, 94, 300.0)

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
            Variable Value Nonwirewound Resistor Component Class.

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
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

            # Calculate component hazard rate.
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
            the Variable Value Nonwirewound Resistor Component Class.

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
            _hrmodel['equation'] = "lambdab * piTAPS * piR * piV * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve junction temperature inputs.
            Tamb = partmodel.get_value(partrow, 37)
            P = partmodel.get_value(partrow, 64)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            Ntaps = partmodel.get_value(partrow, 57)
            Vapplied = partmodel.get_value(partrow, 66)
            _hrmodel['piR'] = partmodel.get_value(partrow, 80)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Prated = partmodel.get_value(partrow, 93)
            Vrated = partmodel.get_value(partrow, 94)
            R = partmodel.get_value(partrow, 95)

            # Base hazard rate
            S = P / Prated
            _hrmodel['lambdab'] = 0.019 * exp(0.445 * ((Tamb + 273) / 358)**7.3) * exp((S / 2.69) * ((Tamb + 273) / 273)**2.46)

            # Potentiometer taps correction factor.
            _hrmodel['piTAPS'] = ((Ntaps ** 1.5) / 25.0) + 0.792

            # Voltage correction factor.
            try:
                Vratio = Vapplied / Vrated
            except:
                Vratio = 1.0

            if Vratio > 0.0 and Vratio <= 0.8:
                _hrmodel['piV'] = 1.00
            elif Vratio > 0.8 and Vratio <= 0.9:
                _hrmodel['piV'] = 1.05
            elif Vratio > 0.9 and Vratio <= 1.0:
                _hrmodel['piV'] = 1.20
            else:
                _hrmodel['piV'] = 0.0

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
            _lambdad = _lambdad * _quantity

            # Calculate the component predicted hazard rate.
            _lambdap = _lambdaa + _lambdad + _lambdas

            # Calculate overstresses.
            (_overstress,
             self.reason) = _calc.overstressed(partmodel, partrow,
                                               systemmodel, systemrow)

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 66, Vapplied)
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piR'])
            partmodel.set_value(partrow, 82, _hrmodel['piTAPS'])
            partmodel.set_value(partrow, 83, _hrmodel['piV'])
            partmodel.set_value(partrow, 111, Vratio)

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


class Composition(Resistor):
    """
    Variable Value Carbon Composition Resistor Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.14
    """

    _quality = ["", "MIL-SPEC", _(u"Lower")]
    _range = ["", "50 - 50.0K", ">50.0K - 100.0K", ">100.0K - 200.0K",
              ">200.0K - 500.0K", ">500.0K - 1.0M"]
    _specsheet = ["", "RV1X-XA, XB", "RV2X-XA, XB", "RV3X-XA, XB",
                  "RV4X-XA, XB", "RV5X-XA, XB", "RV6X-XA, XB", "RV7X-XA, XB",
                  "Other"]

    def __init__(self):
        """
        Initializes the Variable Value Carbon Composition Resistor Component
        Class.
        """

        Resistor.__init__(self)

        self.subcategory = 37               # Subcategory ID in the rtkit DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piR = [1.0, 1.1, 1.2, 1.4, 1.8]
        self._piE = [1.0, 2.0, 19.0, 8.0, 29.0, 40.0, 65.0, 48.0, 78.0,
                     46.0, 0.5, 25.0, 66.0, 1200.0]
        self._piQ = [2.5, 5.0]
        self._lambdab_count = [0.05, 0.11, 1.1, 0.45, 1.7, 2.8, 4.6, 4.6, 7.5,
                               3.3, 0.025, 1.5, 4.7, 67.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Nominal Resistance (\u03A9):"))
        self._in_labels.append(_(u"Spec Sheet:"))
        self._in_labels.append(_(u"Number of Taps:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>TAPS</sub>")
        self._out_labels.append(u"\u03C0<sub>V</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Variable Value Carbon
        Composition Resistor Component Class prediction calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Resistor.assessment_inputs_create(self, part, layout,
                                                     x_pos, y_pos)

        # Create input widgets.
        part.txtResistance = _widg.make_entry()
        part.cmbSpecSheet = _widg.make_combo(simple=True)
        part.txtNTaps = _widg.make_entry(width=100)

        # Load all gtk.ComboBox().
        for i in range(len(self._specsheet)):
            part.cmbSpecSheet.insert_text(i, self._specsheet[i])

        # Place the input widgets.
        layout.put(part.txtResistance, _x_pos, _y_pos[4])
        layout.put(part.cmbSpecSheet, _x_pos, _y_pos[5])
        layout.put(part.txtNTaps, _x_pos, _y_pos[6])

        # Connect widgets to callback methods.
        part.txtResistance.connect("focus-out-event", self._callback_entry,
                                   part, "float", 95)
        part.cmbSpecSheet.connect("changed", self._callback_combo, part, 102)
        part.txtNTaps.connect("focus-out-event", self._callback_entry,
                              part, "float", 57)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Variable Value Carbon Composition Resistor
        Component Class calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos, _y_pos) = Resistor.reliability_results_create(self, part,
                                                               layout,
                                                               x_pos, y_pos)

        # Create the reliability result display widgets.
        # Create the Pi TAPS results entry.  We use the pi_u field
        # in the program database to the results.
        part.txtPiTAPS = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiV = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the reliability result display widgets.
        layout.put(part.txtPiTAPS, _x_pos, _y_pos[5])
        layout.put(part.txtPiV, _x_pos, _y_pos[6])

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with
        calculation input information.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Resistor.assessment_inputs_load(self, part)

        part.txtNTaps.set_text(str("{0:0.0g}".format(
            _model.get_value(_row, 57))))
        part.txtResistance.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 95))))
        part.cmbSpecSheet.set_active(int(_model.get_value(_row, 102)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Resistor.assessment_results_load(self, part)

        part.txtPiTAPS.set_text(str(fmt.format(_model.get_value(_row, 82))))
        part.txtPiV.set_text(str(fmt.format(_model.get_value(_row, 83))))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Variable Value Carbon Composition
        Resistor Component Class ComboBox changes.

        :param gtk.ComboBox combo: the gtk.ComboBox() calling this method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param int idx: the user-defined index for the calling combobx.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        Resistor._callback_combo(self, combo, part, idx)

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        _index = combo.get_active()

        if idx == 102:                      # Specification sheet
            if _index == 1:
                _model.set_value(_row, 94, 250.0)
            elif _index == 2 or _index == 4 or _index == 5 or _index == 6:
                _model.set_value(_row, 94, 350.0)
            elif _index == 3 or _index == 7:
                _model.set_value(_row, 94, 500.0)
            else:
                _model.set_value(_row, 94, 200.0)

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
            Variable Value Carbon Composition Resistor Component Class.

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
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

            # Calculate component hazard rate.
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
            the Variable Value Carbon Composition Resistor Component Class.

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
            _hrmodel['equation'] = "lambdab * piTAPS * piR * piV * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve junction temperature inputs.
            Tamb = partmodel.get_value(partrow, 37)
            P = partmodel.get_value(partrow, 64)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            Ntaps = partmodel.get_value(partrow, 57)
            Vapplied = partmodel.get_value(partrow, 66)
            _hrmodel['piR'] = partmodel.get_value(partrow, 80)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Prated = partmodel.get_value(partrow, 93)
            Vrated = partmodel.get_value(partrow, 94)
            R = partmodel.get_value(partrow, 95)

            # Base hazard rate
            S = P / Prated
            _hrmodel['lambdab'] = 0.0246 * exp(0.459 * ((Tamb + 273) / 343)**9.3) * exp((S / 2.32) * ((Tamb + 273) / 273)**5.3)

            # Potentiometer taps correction factor.
            _hrmodel['piTAPS'] = ((Ntaps ** 1.5) / 25.0) + 0.792

            # Voltage correction factor.
            Vratio = Vapplied / Vrated
            if(Vratio > 0.0 and Vratio <= 0.8):
                _hrmodel['piV'] = 1.00
            elif(Vratio > 0.8 and Vratio <= 0.9):
                _hrmodel['piV'] = 1.05
            elif(Vratio > 0.9 and Vratio <= 1.0):
                _hrmodel['piV'] = 1.20
            else:
                _hrmodel['piV'] = 1.00

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
            _lambdad = _lambdad * _quantity

            # Calculate the component predicted hazard rate.
            _lambdap = _lambdaa + _lambdad + _lambdas

            # Calculate overstresses.
            (_overstress,
             self.reason) = _calc.overstressed(partmodel, partrow,
                                               systemmodel, systemrow)

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 66, Vapplied)
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piR'])
            partmodel.set_value(partrow, 82, _hrmodel['piTAPS'])
            partmodel.set_value(partrow, 83, _hrmodel['piV'])
            partmodel.set_value(partrow, 111, Vratio)

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


class VarFilm(Resistor):
    """
    Variable Value Film Resistor Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.15
    """

    _quality = ["", "MIL-SPEC", _(u"Lower")]
    _range = ["", "Up - 10.0K", ">10.0K - 50.0K", ">50.0K - 200.0K",
              ">200.0K - 1.0M"]
    _specification = ["", "MIL-R-39023 (RQ)", "MIL-R-23285 (RVC)"]
    _specsheet = [["", "RQ090", "RQ100", "RQ110", "RQ150", "RQ160",
                   "RQ200", "RQ210", "RQ300"], ["", "RVC5", "RVC6"]]

    def __init__(self):
        """
        Initializes the Variable Value Film Resistor Component Class.
        """

        Resistor.__init__(self)

        self.subcategory = 37               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piR = [1.0, 1.1, 1.2, 1.4, 1.8]
        self._piE = [1.0, 3.0, 14.0, 7.0, 24.0, 6.0, 12.0, 20.0, 30.0,
                     39.0, 0.5, 22.0, 57.0, 1000.0]
        self._piQ = [2.0, 4.0]
        self._lambdab_count = [0.048, 0.16, 0.76, 0.36, 1.3, 0.36, 0.72, 1.4,
                               2.2, 2.3, 0.024, 1.2, 3.4, 52.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Nominal Resistance (\u03A9):"))
        self._in_labels.append(_(u"Specification:"))
        self._in_labels.append(_(u"Spec Sheet:"))
        self._in_labels.append(_(u"Number of Taps:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>TAPS</sub>")
        self._out_labels.append(u"\u03C0<sub>V</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Variable Value Film Resistor
        Component Class prediction calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Resistor.assessment_inputs_create(self, part, layout,
                                                     x_pos, y_pos)

        # Create input widgets.
        part.txtResistance = _widg.make_entry()
        part.cmbSpecification = _widg.make_combo(simple=True)
        part.cmbSpecSheet = _widg.make_combo(simple=True)
        part.txtNTaps = _widg.make_entry(width=100)

        # Load all gtk.ComboBox().
        for i in range(len(self._specification)):
            part.cmbSpecification.insert_text(i, self._specification[i])

        # Place the input widgets.
        layout.put(part.txtResistance, _x_pos, _y_pos[4])
        layout.put(part.cmbSpecification, _x_pos, _y_pos[5])
        layout.put(part.cmbSpecSheet, _x_pos, _y_pos[6])
        layout.put(part.txtNTaps, _x_pos, _y_pos[7])

        # Connect widgets to callback methods.
        part.txtResistance.connect("focus-out-event", self._callback_entry,
                                   part, "float", 95)
        part.cmbSpecification.connect("changed", self._callback_combo,
                                      part, 101)
        part.cmbSpecSheet.connect("changed", self._callback_combo, part, 102)
        part.txtNTaps.connect("focus-out-event", self._callback_entry,
                              part, "float", 57)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Variable Value Film Resistor Component Class
        calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos, _y_pos) = Resistor.reliability_results_create(self, part,
                                                               layout,
                                                               x_pos, y_pos)

        # Create the reliability result display widgets.
        # Create the Pi TAPS results entry.  We use the pi_u field
        # in the program database to the results.
        part.txtPiTAPS = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiV = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the reliability result display widgets.
        layout.put(part.txtPiTAPS, _x_pos, _y_pos[5])
        layout.put(part.txtPiV, _x_pos, _y_pos[6])

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with
        calculation input information.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Resistor.assessment_inputs_load(self, part)

        part.txtResistance.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 95))))
        part.cmbSpecification.set_active(int(_model.get_value(_row, 101)))
        part.cmbSpecSheet.set_active(int(_model.get_value(_row, 102)))
        part.txtNTaps.set_text(str("{0:0.0g}".format(
            _model.get_value(_row, 57))))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Resistor.assessment_results_load(self, part)

        part.txtPiTAPS.set_text(str(fmt.format(_model.get_value(_row, 82))))
        part.txtPiV.set_text(str(fmt.format(_model.get_value(_row, 83))))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Variable Value Film Resistor
        Component Class ComboBox changes.

        :param gtk.ComboBox combo: the gtk.ComboBox() calling this method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param int idx: the user-defined index for the calling combobx.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        Resistor._callback_combo(self, combo, part, idx)

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        _index = combo.get_active()

        if idx == 101:                      # Specification
            for i in range(len(self._specsheet[_index - 1])):
                part.cmbSpecSheet.insert_text(i,
                                              self._specsheet[_index - 1][i])

        elif idx == 102:                    # Specification sheet
            if _index == 1:
                _model.set_value(_row, 94, 250.0)
            elif _index == 2 or _index == 4 or _index == 5 or _index == 6:
                _model.set_value(_row, 94, 350.0)
            elif _index == 3 or _index == 7:
                _model.set_value(_row, 94, 500.0)
            else:
                _model.set_value(_row, 94, 200.0)

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
            Variable Value Film Resistor Component Class.

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
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Sidx = partmodel.get_value(partrow, 101)        # Specification index
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Sidx - 1][Eidx - 1]

            # Calculate component hazard rate.
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
            the Variable Value Film Resistor Component Class.

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
            _hrmodel['equation'] = "lambdab * piTAPS * piR * piV * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve junction temperature inputs.
            Tamb = partmodel.get_value(partrow, 37)
            P = partmodel.get_value(partrow, 64)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            Ntaps = partmodel.get_value(partrow, 57)
            Vapplied = partmodel.get_value(partrow, 66)
            _hrmodel['piR'] = partmodel.get_value(partrow, 80)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Prated = partmodel.get_value(partrow, 93)
            Vrated = partmodel.get_value(partrow, 94)
            R = partmodel.get_value(partrow, 95)

            # Base hazard rate
            idx = partmodel.get_value(partrow, 101)
            S = P / Prated
            if(idx == 1):
                _hrmodel['lambdab'] = 0.018 * exp(((Tamb + 273.0) / 343.0)**7.4) * exp((S / 2.55) * ((Tamb + 273.0) / 273.0)**3.6)
            elif(idx == 2):
                _hrmodel['lambdab'] = 0.0257 * exp(((Tamb + 273.0) / 398.0)**7.9) * exp((S / 2.45) * ((Tamb + 273.0) / 273.0)**4.3)
            else:
                _hrmodel['lambdab'] = 0.0

            # Potentiometer taps correction factor.
            _hrmodel['piTAPS'] = ((Ntaps ** 1.5) / 25.0) + 0.792

            # Voltage correction factor.
            Vratio = Vapplied / Vrated
            if Vratio >= 0.0 and Vratio <= 0.8:
                _hrmodel['piV'] = 1.00
            elif Vratio > 0.8 and Vratio <= 0.9:
                _hrmodel['piV'] = 1.05
            elif Vratio > 0.9 and Vratio <= 1.0:
                _hrmodel['piV'] = 1.20
            else:
                _hrmodel['piV'] = 0.0

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
            _lambdad = _lambdad * _quantity

            # Calculate the component predicted hazard rate.
            _lambdap = _lambdaa + _lambdad + _lambdas

            # Calculate overstresses.
            (_overstress,
             self.reason) = _calc.overstressed(partmodel, partrow,
                                               systemmodel, systemrow)

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 66, Vapplied)
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piR'])
            partmodel.set_value(partrow, 82, _hrmodel['piTAPS'])
            partmodel.set_value(partrow, 83, _hrmodel['piV'])
            partmodel.set_value(partrow, 111, Vratio)

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
