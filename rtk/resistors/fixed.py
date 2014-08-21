#!/usr/bin/env python

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       fixed.py is part of The RTK Project
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


class Composition(Resistor):
    """
    Fixed Value Carbon Composition Resistor Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.1
    """

    _quality = ["", "S", "R", "P", "M", "MIL-R-11", _(u"Lower")]
    _range = ["", "<0.1M", "0.1M to 1.0M", "1.0M to 10.0M", "<10.0M"]

    def __init__(self):
        """
        Initializes the Fixed Value Carbon Composition Resistor Component
        Class.
        """

        Resistor.__init__(self)

        self.subcategory = 25               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piR = [1.0, 1.1, 1.6, 2.5]
        self._piE = [1.0, 3.0, 8.0, 5.0, 13.0, 4.0, 5.0, 7.0, 11.0, 19.0, 0.5,
                     11.0, 27.0, 490.0]
        self._piQ = [0.03, 0.1, 0.3, 1.0, 5.0, 15.0]
        self._lambdab_count = [0.0005, 0.0022, 0.0071, 0.0037, 0.012, 0.0052,
                               0.0065, 0.016, 0.025, 0.025, 0.00025, 0.0098,
                               0.035, 0.36]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

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
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

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
            the Fixed Value Carbon Composition Resistor Component Class.

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
            _hrmodel['equation'] = "lambdab * piR * piQ * piE"

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
            _hrmodel['piR'] = partmodel.get_value(partrow, 80)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Prated = partmodel.get_value(partrow, 93)

            # Base hazard rate.
            S = P / Prated
            _hrmodel['lambdab'] = 0.0000000045 * exp(12.0 * ((Tamb + 273.0) / 343.0)) * exp((S / 0.6) * ((Tamb + 273.0) / 273.0))

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
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piR'])

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


class Film(Resistor):
    """
    Fixed Value Film Resistor Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.2
    """

    _quality = ["", "S", "R", "P", "M", "MIL-R-10509", "MIL-R-22684",
                _("Lower")]
    _range = ["", "<0.1M", "0.1M to 1.0M", "1.0M to 10.0M", "<10.0M"]
    _spec = ["", "MIL-R-39017 (RLR)", "MIL-R-22684 (RL)",
             "MIL-R-55182 (RNR, RNC, RNN)", "MIL-R-10509 (RN)"]

    def __init__(self):
        """
        Initializes the Fixed Value Film Resistor Component Class.
        """

        Resistor.__init__(self)

        self.subcategory = 26               # Subcategory ID in the rtkit DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 8.0, 4.0, 14.0, 4.0, 8.0, 10.0, 18.0, 19.0, 0.2,
                     10.0, 28.0, 510.0]
        self._piQ = [0.03, 0.1, 0.3, 1.0, 5.0, 5.0, 15.0]
        self._piR = [1.0, 1.1, 1.6, 2.5]
        self._lambdab_count = [[0.0012, 0.0027, 0.011, 0.0054, 0.020, 0.0063,
                                0.013, 0.018, 0.033, 0.030, 0.00025, 0.014,
                                0.044, 0.69],
                               [0.0012, 0.0027, 0.011, 0.0054, 0.020, 0.0063,
                                0.013, 0.018, 0.033, 0.030, 0.00025, 0.014,
                                0.044, 0.69],
                               [0.0014, 0.0031, 0.013, 0.0061, 0.023, 0.0072,
                                0.014, 0.021, 0.038, 0.034, 0.00028, 0.016,
                                0.050, 0.78],
                               [0.0014, 0.0031, 0.013, 0.0061, 0.023, 0.0072,
                                0.014, 0.021, 0.038, 0.034, 0.00028, 0.016,
                                0.050, 0.78]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Specification/Type:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Fixed Value Film Resistor
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
        _x_pos = max(x_pos, _x_pos) + 35

        # Create display widgets specific to fixed film resistors.
        part.cmbSpecification = _widg.make_combo(simple=True)

        # Load all gtk.ComboBox().
        for i in range(len(self._spec)):
            part.cmbSpecification.insert_text(i, self._spec[i])

        # Place display widgets.
        layout.put(part.cmbSpecification, _x_pos, _y_pos[4])

        # Connect to callback methods.
        part.cmbSpecification.connect("changed", self._callback_combo,
                                      part, 101)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with
        calculation input information.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = Resistor.assessment_inputs_load(self, part)

        part.cmbSpecification.set_active(int(_model.get_value(_row, 101)))

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
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Sidx = partmodel.get_value(partrow, 101)        # Specification index
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Sidx - 1][Eidx - 1]

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
            the Fixed Value Film Resistor Component Class.

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
            _hrmodel['equation'] = "lambdab * piR * piQ * piE"

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
            _hrmodel['piR'] = partmodel.get_value(partrow, 80)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Prated = partmodel.get_value(partrow, 93)

            # Base hazard rate.
            S = P / Prated

            idx = partmodel.get_value(partrow, 101)
            if idx == 1 or idx == 2:
                _hrmodel['lambdab'] = 0.000325 * exp((Tamb + 273) / 343)**3 * exp(S * ((Tamb + 273) / 273))
            elif idx == 3 or idx == 4:
                _hrmodel['lambdab'] = 0.00005 * exp(3.5 * ((Tamb + 273) / 398)) * exp(S * ((Tamb + 273) / 273))
            else:
                _hrmodel['lambdab'] = 1.0

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
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piR'])

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


class FilmNetwork(Resistor):
    """
    Fixed Value Film Network Resistor Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.4
    """

    _quality = ["", "MIL-SPEC", _(u"Lower")]
    _range = ["", _(u"Any")]

    def __init__(self):
        """
        Initializes the Fixed Value Film Network Resistor Component Class.
        """

        Resistor.__init__(self)

        self.subcategory = 28               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 10.0, 5.0, 17.0, 6.0, 8.0, 14.0, 18.0, 25.0,
                     0.5, 14.0, 36.0, 660.0]
        self._piQ = [1.0, 3.0]
        self._piR = [1.0]
        self._lambdab_count = [0.0023, 0.0066, 0.031, 0.013, 0.055, 0.022,
                               0.043, 0.077, 0.15, 0.10, 0.0011, 0.055, 0.15,
                               1.7]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Number of Elements:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>NR</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels[4] = u"\u03C0<sub>T</sub>:"
        self._out_labels.append(u"\u03C0<sub>NR</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Fixed Value Film Network
        Resistor prediction calculations.

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
        _x_pos = max(x_pos, _x_pos) + 35

        # Create the number of resistors in the network entry.
        part.txtNumber = _widg.make_entry(width=100)

        # Place the network film resistor widgets.
        layout.put(part.txtNumber, _x_pos, _y_pos[4])

        # Connect to callback methods.
        part.txtNumber.connect("focus-out-event", self._callback_entry,
                               part, "float", 58)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Fixed Values Film Network Resistor Component
        Class calculation results.

        Keyword Arguments:
        part   -- the RTK COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        (_x_pos, _y_pos) = Resistor.reliability_results_create(self, part,
                                                               layout,
                                                               x_pos, y_pos)

        # Create the pi NR results entry.  This is the same value as the
        # number of elements in the program database.
        part.txtPiNR = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the pi NR results.
        layout.put(part.txtPiNR, _x_pos, _y_pos[5])

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with
        calculation input information.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = Resistor.assessment_inputs_load(self, part)

        part.txtNumber.set_text(str("{0:0.0g}".format(
            _model.get_value(_row, 58))))

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

        (_model, _row) = Resistor.assessment_results_load(self, part)

        part.txtPiNR.set_text(str("{0:0.0g}".format(
            _model.get_value(_row, 58))))

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
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Eidx = systemmodel.get_value(systemrow, 22)              # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

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
            the Fixed Value Film Network Resistor Component Class.

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
            _hrmodel['equation'] = "lambdab * piT * piNR * piQ * piE"

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
            Tcase = partmodel.get_value(partrow, 105)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            _hrmodel['piNR'] = partmodel.get_value(partrow, 58)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            _hrmodel['piR'] = partmodel.get_value(partrow, 80)
            Prated = partmodel.get_value(partrow, 93)

            # Base hazard rate.
            _hrmodel['lambdab'] = 0.00006

            # Temperature correction factor.  We store this value in the pi_u
            # field in the program database.
            S = P / Prated
            if Tcase == 0:
                Tcase = Tamb + 55 * S

            _hrmodel['piT'] = exp(-4056 * ((1 / (Tcase + 273)) - (1 / 298)))

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
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 82, _hrmodel['piT'])

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


class FilmPower(Resistor):
    """
    Fixed Value Film Power Resistor Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.3
    """

    _quality = ["", "MIL-SPEC", _(u"Lower")]
    _range = ["", "10 - 100", ">100 - 100K", ">100K - 1M", ">1M"]

    def __init__(self):
        """
        Initializes the Fixed Value Film Power Resistor Component Class.
        """

        Resistor.__init__(self)

        self.subcategory = 27               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 10.0, 5.0, 17.0, 6.0, 8.0, 14.0, 18.0, 25.0,
                     0.5, 14.0, 36.0, 660.0]
        self._piQ = [1.0, 3.0]
        self._piR = [1.0, 1.2, 1.3, 3.5]
        self._lambdab_count = [0.012, 0.025, 0.13, 0.062, 0.21, 0.078, 0.10,
                               0.19, 0.24, 0.32, 0.0060, 0.18, 0.47, 8.2]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

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
            Fixed Value Film Power Resistor Component Class.

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
            the Fixed Value Film Power Resistor Component Class.

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
            _hrmodel['equation'] = "lambdab * piR * piQ * piE"

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
            _hrmodel['piR'] = partmodel.get_value(partrow, 80)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Prated = partmodel.get_value(partrow, 93)

            # Base hazard rate.
            S = P / Prated
            _hrmodel['lambdab'] = 0.00733 * exp(0.202 * ((Tamb + 273) / 298))**2.6 * exp((S / 1.45) * ((Tamb + 273) / 273)**0.89)**1.3

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
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piR'])

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


class Wirewound(Resistor):
    """
    Fixed Value Wirewound Resistor Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.5
    """

    _quality = ["", "S", "R", "P", "M", "MIL-R-93", _(u"Lower")]
    _range = ["", "<10K", "10K - 100K", "100K - 1M", ">1M"]

    def __init__(self):
        """
        Initializes the Fixed Value Wirewound Resistor Component Class.
        """

        Resistor.__init__(self)

        self.subcategory = 29               # Subcategory ID in the rtkcom SB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 11.0, 5.0, 18.0, 15.0, 18.0, 28.0, 35.0, 27.0,
                     0.8, 14.0, 38.0, 610.0]
        self._piQ = [0.03, 0.1, 0.3, 1.0, 5.0, 15.0]
        self._piR = [1.0, 1.7, 3.0, 5.0]
        self._lambdab_count = [0.0085, 0.018, 0.10, 0.045, 0.16, 0.15, 0.17,
                               0.30, 0.38, 0.26, 0.0068, 0.13, 0.37, 5.4]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

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
            Fixed Value Wirewound Resistor Component Class.

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
            the Fixed Value Wirewound Resistor Component Class.

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
            _hrmodel['equation'] = "lambdab * piR * piQ * piE"

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
            _hrmodel['piR'] = partmodel.get_value(partrow, 80)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Prated = partmodel.get_value(partrow, 93)

            # Base hazard rate.
            S = P / Prated
            _hrmodel['lambdab'] = 0.0031 * exp(((Tamb + 273) / 398)**10) * exp((S * ((Tamb + 273) / 273))**1.5)

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
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piR'])

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


class WirewoundPower(Resistor):
    """
    Fixed Value Wirewound Power Resistor Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.6
    """

    _quality = ["", "S", "R", "P", "M", "MIL-R-26", _(u"Lower")]
    _range = [""]
    _ranges = [["", "<500", "500 - 1K", "1K - 5K", "5K - 7.5K",
                "7.5K - 10K", "10K - 15K", "15K - 20K", ">20K"],
               ["", "<100", "100 - 1K", "1K - 10K", "10K - 100K",
                "100K - 150K", "150K - 200K"]]
    _spec = ["", "MIL-R-39007 (RWR)", "MIL-R-26 (RW)"]
    _specsheet = [["", "RWR 71", "RWR 74", "RWR 78", "RWR 80", "RWR 81",
                   "RWR 82", "RWR 84", "RWR 89"],
                  ["", "RW 10", "RW 11", "RW 12", "RW 13", "RW 14", "RW 15",
                   "RW 16", "RW 20", "RW 21", "RW 22", "RW 23", "RW 24",
                   "RW 29", "RW 30", "RW 31", "RW 32", "RW 33", "RW 34",
                   "RW 35", "RW 36", "RW 37", "RW 38", "RW 39", "RW 47",
                   "RW 55", "RW 56", "RW 67", "RW 68", "RW 69", "RW 70",
                   "RW 74", "RW 78", "RW 79", "RW 80", "RW 81"]]

    def __init__(self):
        """
        Initializes the Fixed Value Wirewound Power Resistor Component
        Class.
        """

        Resistor.__init__(self)

        self.subcategory = 30               # Subcategory ID in rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 10.0, 5.0, 16.0, 4.0, 8.0, 9.0, 18.0, 23.0,
                     0.3, 13.0, 34.0, 610.0]
        self._piQ = [0.03, 0.1, 0.3, 1.0, 5.0, 15.0]
        self._piR = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self._piR_RWR = [[1.0, 1.0, 1.2, 1.2, 1.6, 1.6, 1.6, 0.0],
                         [1.0, 1.0, 1.0, 1.2, 1.6, 1.6, 0.0, 0.0],
                         [1.0, 1.0, 1.0, 1.0, 1.2, 1.2, 1.2, 1.6],
                         [1.0, 1.2, 1.6, 1.6, 0.0, 0.0, 0.0, 0.0],
                         [1.0, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                         [1.0, 1.6, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0],
                         [1.0, 1.0, 1.1, 1.2, 1.2, 1.6, 0.0, 0.0],
                         [1.0, 1.0, 1.4, 0.0, 0.0, 0.0, 0.0, 0.0]]
        self._piR_RW = [[1.0, 1.0, 1.0, 1.0, 1.2, 1.6],
                        [1.0, 1.0, 1.0, 1.2, 1.6, 0.0],
                        [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 2.0, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 2.0, 0.0, 0.0],
                        [1.0, 1.0, 1.2, 2.0, 0.0, 0.0],
                        [1.0, 1.2, 1.4, 0.0, 0.0, 0.0],
                        [1.0, 1.0, 1.6, 0.0, 0.0, 0.0],
                        [1.0, 1.0, 1.2, 2.0, 0.0, 0.0],
                        [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 1.2, 0.0, 0.0],
                        [1.0, 1.0, 1.4, 0.0, 0.0, 0.0],
                        [1.0, 1.2, 1.6, 0.0, 0.0, 0.0],
                        [1.0, 1.0, 1.4, 0.0, 0.0, 0.0],
                        [1.0, 1.0, 1.2, 0.0, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
                        [1.0, 1.0, 1.2, 1.5, 0.0, 0.0],
                        [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 1.4, 1.6, 0.0],
                        [1.0, 1.0, 1.0, 1.4, 1.6, 2.0],
                        [1.0, 1.0, 1.0, 1.4, 1.6, 2.0],
                        [1.0, 1.0, 1.4, 2.4, 0.0, 0.0],
                        [1.0, 1.0, 1.2, 2.6, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                        [1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                        [1.0, 1.2, 1.4, 0.0, 0.0, 0.0],
                        [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 1.6, 0.0, 0.0],
                        [1.0, 1.0, 1.4, 0.0, 0.0, 0.0],
                        [1.0, 1.2, 1.5, 0.0, 0.0, 0.0],
                        [1.0, 1.2, 0.0, 0.0, 0.0, 0.0]]
        self._Lambdab_count = [[0.014, 0.031, 0.16, 0.077, 0.26, 0.073, 0.15,
                                0.19, 0.39, 0.42, 0.0042, 0.21, 0.62, 9.4],
                               [0.013, 0.028, 0.15, 0.070, 0.24, 0.065, 0.13,
                                0.18, 0.35, 0.38, 0.0038, 0.19, 0.56, 8.6]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Specification:"))
        self._in_labels.append(_(u"Spec Sheet:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Fixed Value Wirewound Power
        Resistor prediction calculations.

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
        part.cmbSpecification = _widg.make_combo(simple=True)
        part.cmbSpecSheet = _widg.make_combo(simple=True)

        # Load all gtk.ComboBox().
        for i in range(len(self._spec)):
            part.cmbSpecification.insert_text(i, self._spec[i])

        # Place the instance-specific input widgets.
        layout.put(part.cmbSpecification, _x_pos, _y_pos[4])
        layout.put(part.cmbSpecSheet, _x_pos, _y_pos[5])

        # Connect instance-specific widgets to callback methods.
        part.cmbSpecification.connect("changed", self._callback_combo,
                                      part, 101)
        part.cmbSpecSheet.connect("changed", self._callback_combo, part, 102)

        layout.show_all()

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

        (_model, _row) = Resistor.assessment_inputs_load(self, part)

        part.cmbSpecification.set_active(int(_model.get_value(_row, 101)))
        part.cmbSpecSheet.set_active(int(_model.get_value(_row, 102)))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Fixed Value Wirewound Power
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

        if idx == 101:                      # Specification
            part.cmbSpecSheet.get_model().clear()

            if _index == 1:
                for i in range(len(self._ranges[_index - 1])):
                    part.cmbRRange.insert_text(i, self._ranges[_index - 1][i])
            elif _index == 2:
                for i in range(len(self._ranges[_index - 1])):
                    part.cmbRRange.insert_text(i, self._ranges[_index - 1][i])

            for i in range(len(self._specsheet[_index - 1])):
                part.cmbSpecSheet.insert_text(i,
                                              self._specsheet[_index - 1][i])

        elif idx == 102:                    # Specification sheet
            _index2 = part.cmbRRange.get_active()

            if _index == 1:
                S = self._piR_RWR[_index - 1][_index2 - 1]
            elif _index == 2:
                S = self._piR_RW[_index - 1][_index2 - 1]
            else:
                S = 1.0

            _model.set_value(_row, 80, S)

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
            Fixed Value Wirewound Power Resistor Component Class.

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
            Sidx = partmodel.get_value(partrow, 101)        # Specification

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
            the Fixed Value Wirewound Power Resistor Component Class.

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
            _hrmodel['equation'] = "lambdab * piR * piQ * piE"

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
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Prated = partmodel.get_value(partrow, 93)

            # Base hazard rate.
            S = P / Prated
            _hrmodel['lambdab'] = 0.00148 * exp(((Tamb + 273) / 298)**2) * exp((S / 0.5) * (Tamb + 273) / 273)

            # Retrieve the resistance correction factor using the selected
            # specification sheet and selected resistance range.
            _spec_idx = partmodel.get_value(partrow, 102)
            _resistance_idx = partmodel.get_value(partrow, 95)

            if _spec_idx == 1:
                _hrmodel['piR'] = self._piR_RWR[_spec_idx - 1][_resistance_idx - 1]
            elif _spec_idx == 2:
                _hrmodel['piR'] = self._piR_RW[_spec_idx - 1][_resistance_idx - 1]
            else:
                _hrmodel['piR'] = 1.0

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
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piR'])

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


class WirewoundPowerChassis(Resistor):
    """
    Fixed Value Wirewound Chassis-Mounted Power Resistor Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.7
    """

    _quality = ["", "S", "R", "P", "M", "MIL-R-18546", _(u"Lower")]
    _range = ["", "<500", "500 - 1K", "1K - 5K", "5K - 10K",
              "10K - 20K", ">20K"]
    _spec = ["", "MIL-R-18546 (RER)", "MIL-R-39009 (RE)"]
    _specsheet = [["", "RER 60", "RER 65", "RER 70", "RER 75"],
                  ["", "RE 60", "RE 65", "RE 70", "RE 77", "RE 80"]]
    _type = [["", _(u"Type G (Inductive)"), _(u"Type N (Non-Inductive)")],
             ["", _(u"Inductively Wound"), _(u"Non-Inductively Wound")]]

    def __init__(self):
        """
        Initializes the Fixed Value Wirewound Chassis-Mounted Power Resistor
        Component Class.
        """

        Resistor.__init__(self)

        self.subcategory = 31               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 10.0, 5.0, 16.0, 4.0, 8.0, 9.0, 18.0, 23.0,
                     0.5, 13.0, 34.0, 610.0]
        self._piQ = [0.03, 0.1, 0.3, 1.0, 5.0, 15.0]
        self._piR = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self._piR_RER = [[1.0, 1.2, 1.2, 1.6, 0.0, 0.0],
                         [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
                         [1.0, 1.0, 1.2, 1.2, 1.6, 0.0],
                         [1.0, 1.0, 1.0, 1.1, 1.2, 0.0]]
        self._piR_RE = [[1.0, 1.2, 1.6, 0.0, 0.0, 0.0],
                        [1.0, 1.2, 1.6, 0.0, 0.0, 0.0],
                        [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
                        [1.0, 1.0, 1.1, 1.2, 1.4, 0.0],
                        [1.0, 1.0, 1.0, 1.2, 1.6, 0.0],
                        [1.0, 1.0, 1.0, 1.1, 1.6, 0.0]]
        self._lambdab_count = [0.008, 0.18, 0.096, 0.045, 0.15, 0.044, 0.088,
                               0.12, 0.24, 0.25, 0.004, 0.13, 0.37, 5.5]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Specification:"))
        self._in_labels.append(_(u"Spec Sheet:"))
        self._in_labels.append(_(u"Construction:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Fixed Value Wirewound Chassis-
        Mounted Power Resistor prediction calculations.

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
        part.cmbSpecification = _widg.make_combo(simple=True)
        part.cmbSpecSheet = _widg.make_combo(simple=True)
        part.cmbConstruction = _widg.make_combo(simple=True)

        # Load all gtk.ComboBox().
        for i in range(len(self._spec)):
            part.cmbSpecification.insert_text(i, self._spec[i])

        # Place the input widgets.
        layout.put(part.cmbSpecification, _x_pos, _y_pos[4])
        layout.put(part.cmbSpecSheet, _x_pos, _y_pos[5])
        layout.put(part.cmbConstruction, _x_pos, _y_pos[6])

        # Connect widgets to callback methods.
        part.cmbSpecification.connect("changed", self._callback_combo,
                                      part, 101)
        part.cmbSpecSheet.connect("changed", self._callback_combo, part, 102)
        part.cmbConstruction.connect("changed", self._callback_combo, part, 16)

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

        part.cmbSpecification.set_active(int(_model.get_value(_row, 101)))
        part.cmbSpecSheet.set_active(int(_model.get_value(_row, 102)))
        part.cmbConstruction.set_active(int(_model.get_value(_row, 16)))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Fixed Value Wirewound Chassis-
        Mounted Power Resistor Component Class ComboBox changes.

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
            _index = part.cmbSpecSheet.get_active()
            _index2 = part.cmbRRange.get_active()

            if _index == 1:                 # Inductive
                C = self._piR_RER[_index - 1][_index2 - 1]
            elif _index == 2:               # Non-Inductive
                C = self._piR_RE[_index - 1][_index2 - 1]
            else:
                C = 1.0

            _model.set_value(_row, 80, C)

        elif idx == 101:                    # Specification
            part.cmbSpecSheet.get_model().clear()

            for i in range(len(self._specsheet[_index - 1])):
                part.cmbSpecSheet.insert_text(i,
                                              self._specsheet[_index - 1][i])

            for i in range(len(self._type[_index - 1])):
                part.cmbConstruction.insert_text(i, self._type[_index - 1][i])

            part.cmbConstruction.set_active(int(_model.get_value(_row, 16)))
            part.cmbSpecSheet.set_active(int(_model.get_value(_row, 102)))

        elif idx == 102:                    # Specification sheet
            _index2 = part.cmbRRange.get_active()

            if _index == 1:
                S = self._piR_RER[_index - 1][_index2 - 1]
            elif _index == 2:
                S = self._piR_RE[_index - 1][_index2 - 1]
            else:
                S = 1.0

            _model.set_value(_row, 80, S)

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
            Fixed Value Wirewound Chassis-Mounted Power Resistor Component
            Class.

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
            the Fixed Value Wirewound Chassis-Mounted Power Resistor Component
            Class.

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
            _hrmodel['equation'] = "lambdab * piR * piQ * piE"

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
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Prated = partmodel.get_value(partrow, 93)

            # Base hazard rate.
            S = P / Prated
            _hrmodel['lambdab'] = 0.00015 * exp(2.64 * ((Tamb + 273) / 298)) * exp((S / 0.466) * (Tamb + 273) / 273)

            # Resistance correction factor.
            idx = partmodel.get_value(partrow, 102)
            idx2 = partmodel.get_value(partrow, 95)

            if idx == 1:                # Inductive
                _hrmodel['piR'] = self._piR_RER[idx - 1][idx2 - 1]
            elif idx == 2:              # Non-Inductive
                _hrmodel['piR'] = self._piR_RE[idx - 1][idx2 - 1]
            else:
                _hrmodel['piR'] = 1.0

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
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piR'])

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
