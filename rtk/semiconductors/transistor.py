#!/usr/bin/env python
"""
transistor.py contains the classes for all transistor types.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       transistor.py is part of The RTK Project
#
# All rights reserved.

import gettext
import locale

from math import exp

try:
    import rtk.calculations as _calc
    import rtk.configuration as _conf
    import rtk.widgets as _widg
except ImportError:
    import calculations as _calc
    import configuration as _conf
    import widgets as _widg
from semiconductor import Semiconductor

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except ImportError:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class LFBipolar(Semiconductor):
    """
    Low Frequency Bipolar Transistor Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 6.3
    """

    _application = ["", _(u"Linear Amplification"), _(u"Switching")]

    def __init__(self):
        """
        Initializes the Low Frequency Bipolar Transistor Component Class.
        """

        Semiconductor.__init__(self)

        self.subcategory = 14               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piA = [1.5, 0.7]
        self._piE = [1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0,
                     0.5, 14.0, 32.0, 320.0]
        self._piQ = [0.5, 1.0, 2.0, 5.0, 8.0]
        self._lambdab_count = [[0.00015, 0.0011, 0.0017, 0.0017, 0.0037,
                                0.0030, 0.0067, 0.0060, 0.013, 0.0056,
                                0.000073, 0.0027, 0.0074, 0.056],
                               [0.0057, 0.042, 0.069, 0.063, 0.15, 0.12, 0.26,
                                0.23, 0.50, 0.22, 0.0029, 0.11, 0.29, 1.1]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Application:"))
        self._in_labels.append(_(u"Rated Power:"))
        self._in_labels.append(_(u"Applied CE Voltage:"))
        self._in_labels.append(_(u"Rated CE Voltage:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>R</sub>\u03C0<sub>S</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>A</sub>:")
        self._out_labels.append(u"\u03C0<sub>R</sub>:")
        self._out_labels.append(u"\u03C0<sub>S</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Low Frequency Bipolar
        Transistor Component Class prediction calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Semiconductor.assessment_inputs_create(self, part, layout,
                                                          x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 35

        # Create component specific input widgets.
        part.cmbApplication = _widg.make_combo(simple=True)
        part.txtPrated = _widg.make_entry(width=100)
        part.txtOpVolts = _widg.make_entry(width=100)
        part.txtRatedVolts = _widg.make_entry(width=100)

        # Load the gtk.ComboBox().
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.cmbPackage, _x_pos, _y_pos[1])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[2])
        layout.put(part.cmbApplication, _x_pos, _y_pos[3])
        layout.put(part.txtPrated, _x_pos, _y_pos[4])
        layout.put(part.txtOpVolts, _x_pos, _y_pos[5])
        layout.put(part.txtRatedVolts, _x_pos, _y_pos[6])

        # Connect component specific widgets to callback methods.
        part.cmbApplication.connect("changed", self._callback_combo, part, 5)
        part.txtPrated.connect("focus-out-event", self._callback_entry,
                               part, "float", 93)
        part.txtOpVolts.connect("focus-out-event", self._callback_entry,
                                part, "float", 66)
        part.txtRatedVolts.connect("focus-out-event", self._callback_entry,
                                   part, "float", 94)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Low Frequency Bipolar Transistor Component
        Class calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Semiconductor.reliability_results_create(self, part, layout,
                                                            x_pos, y_pos)

        # Create component specific reliability result display widgets.
        part.txtPiA = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiR = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiS = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the component specifci reliability result display widgets.
        layout.put(part.txtPiA, _x_pos, _y_pos[5])
        layout.put(part.txtPiR, _x_pos, _y_pos[6])
        layout.put(part.txtPiS, _x_pos, _y_pos[7])

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

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Semiconductor.assessment_inputs_load(self, part)

        part.cmbApplication.set_active(int(_model.get_value(_row, 5)))
        part.txtOpVolts.set_text(str(fmt.format(_model.get_value(_row, 66))))
        part.txtPrated.set_text(str(fmt.format(_model.get_value(_row, 93))))
        part.txtRatedVolts.set_text(str(fmt.format(
            _model.get_value(_row, 94))))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Semiconductor.assessment_results_load(self, part)

        part.txtPiA.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 68))))
        part.txtPiR.set_text(str(fmt.format(_model.get_value(_row, 80))))
        part.txtPiS.set_text(str(fmt.format(_model.get_value(_row, 81))))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Low Frequency Bipolar Transistor
        Component Class ComboBox changes.

        :param gtk.ComboBox combo: the gtk.ComboBox() calling this method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param int idx: the user-defined index for the calling combobx.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _index = combo.get_active()

        (_model, _row) = Semiconductor._callback_combo(self, combo, part, idx)

        if idx == 5:                        # Application
            _model.set_value(_row, 68, self._piA[_index - 1])

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
            Low Frequency Bipolar Transistor Component Class.

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
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

            # TODO: Validate index 64 is operating power.
            if partmodel.get_value(partrow, 64) <= 0.1:
                Pidx = 0
            else:
                Pidx = 1

            _hrmodel['lambdab'] = self._lambdab_count[Pidx][Eidx - 1]

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
            the Low Frequency Bipolar Transistor Component Class.

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
            _hrmodel['equation'] = "lambdab * piT * piR * piS * piQ * piE"

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
            Poper = partmodel.get_value(partrow, 64)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            Vapplied = partmodel.get_value(partrow, 66)
            _hrmodel['piA'] = partmodel.get_value(partrow, 68)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Prated = partmodel.get_value(partrow, 93)
            Vrated = partmodel.get_value(partrow, 94)

            # Calculate junction temperature.  If ambient temperature and
            # temperature rise are not set (i.e., equal to zero), use the
            # default case temperature values that are based on the active
            # environment.  Otherwise calculate case temperature.
            if Tamb == 0 and Trise == 0:
                idx = int(systemmodel.get_value(systemrow, 22))
                Tcase = self._Tcase[idx - 1]
            else:
                Tcase = Tamb + Trise

            # Determine the junction-case thermal resistance.  If thetaJC is
            # not set (i.e., equal to zero), use the default value which is
            # based on the package type.
            if thetaJC == 0:
                idx = int(partmodel.get_value(partrow, 67))
                thetaJC = self._thetaJC[idx - 1]
                partmodel.set_value(partrow, 109, thetaJC)

            # Junction temperature.
            Tj = Tcase + thetaJC * Poper

            # Base hazard rate.
            _hrmodel['lambdab'] = 0.00074

            # Temperature correction factor.  We store this in the pi_u
            # field in the Program Database.
            _hrmodel['piT'] = exp(-2114.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

            # Power rating correction factor.
            if Prated <= 0.1:
                _hrmodel['piR'] = 0.43
            else:
                _hrmodel['piR'] = Prated**0.37

            # Voltage stress correction factor.
            try:
                Vs = Vapplied / Vrated
            except ZeroDivisionError:
                Vs = 1

            _hrmodel['piS'] = 0.045 * exp(3.1 * Vs)

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

            partmodel.set_value(partrow, 39, Tj)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 68, _hrmodel['piA'])
            partmodel.set_value(partrow, 80, _hrmodel['piE'])
            partmodel.set_value(partrow, 81, _hrmodel['piS'])
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


class LFSiFET(Semiconductor):
    """
    Low Frequency Silicon Field Effect Transistor (FET) Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.4
    """

    _application = ["", _(u"Linear Amplification"),
                    _(u"Small-Signal Switching"), _(u"Power")]
    _technology = ["", "MOSFET", "JFET"]

    def __init__(self):
        """
        Initializes the Low Frequency Silicon FET Transistor Component Class.
        """

        Semiconductor.__init__(self)

        self.subcategory = 15               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._lambdab = [0.012, 0.0045]
        self._piE = [1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0,
                     0.5, 14.0, 32.0, 320.0]
        self._piQ = [0.7, 1.0, 2.4, 5.5, 8.0]
        self._lambdab_count = [[0.014, 0.099, 0.16, 0.15, 0.34, 0.28, 0.62,
                                0.53, 1.1, 0.51, 0.0069, 0.25, 0.68, 5.3]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Application:"))
        self._in_labels.append(_(u"Transistor Type:"))
        self._in_labels.append(_(u"Rated Power:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>A</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Low Frequency Silicon FET
        prediction calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Semiconductor.assessment_inputs_create(self, part, layout,
                                                          x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 35

        # Create component specific input widgets.
        part.cmbApplication = _widg.make_combo(simple=True)
        part.cmbTechnology = _widg.make_combo(simple=True)
        part.txtPrated = _widg.make_entry(width=100)

        # Load the gtk.ComboBox().
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])
        for i in range(len(self._technology)):
            part.cmbTechnology.insert_text(i, self._technology[i])

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.cmbPackage, _x_pos, _y_pos[1])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[2])
        layout.put(part.cmbApplication, _x_pos, _y_pos[3])
        layout.put(part.cmbTechnology, _x_pos, _y_pos[4])
        layout.put(part.txtPrated, _x_pos, _y_pos[5])

        # Connect component specific widgets to callback methods.
        part.cmbApplication.connect("changed", self._callback_combo, part, 5)
        part.cmbTechnology.connect("changed", self._callback_combo, part, 104)
        part.txtPrated.connect("focus-out-event", self._callback_entry,
                               part, "float", 93)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Low Frequency Silicon FET calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Semiconductor.reliability_results_create(self, part, layout,
                                                            x_pos, y_pos)

        # Create component specific reliability result display widgets.
        part.txtPiA = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the component specific reliability result display widgets.
        layout.put(part.txtPiA, _x_pos, _y_pos[5])

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

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Semiconductor.assessment_inputs_load(self, part)

        part.cmbApplication.set_active(int(_model.get_value(_row, 5)))
        part.txtPrated.set_text(str(fmt.format(_model.get_value(_row, 93))))
        part.cmbTechnology.set_active(int(_model.get_value(_row, 104)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = Semiconductor.assessment_results_load(self, part)

        part.txtPiA.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 68))))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Low Frequency Silicon FET Component
        Class ComboBox changes.

        :param gtk.ComboBox combo: the gtk.ComboBox() calling this method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param int idx: the user-defined index for the calling combobx.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _index = combo.get_active()

        (_model, _row) = Semiconductor._callback_combo(self, combo, part, idx)

        if idx == 104:                      # Technology
            _model.set_value(_row, 46, self._lambdab[_index - 1])

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
            Low Frequency Silicon FET Component Class.

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
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

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
            the Low Frequency Silicon FET Component Class.

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
            _hrmodel['equation'] = "lambdab * piT * piA * piQ * piE"

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
            Poper = partmodel.get_value(partrow, 64)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            _hrmodel['lambdab'] = partmodel.get_value(partrow, 46)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Prated = partmodel.get_value(partrow, 93)

            # Calculate junction temperature.  If ambient temperature and
            # temperature rise are not set (i.e., equal to zero), use the
            # default case temperature values that are based on the active
            # environment.  Otherwise calculate case temperature.
            if Tamb == 0 and Trise == 0:
                idx = int(systemmodel.get_value(systemrow, 22))
                Tcase = self._Tcase[idx - 1]
            else:
                Tcase = Tamb + Trise

            # Determine the junction-case thermal resistance.  If thetaJC is
            # not set (i.e., equal to zero), use the default value which is
            # based on the package type.
            if thetaJC == 0:
                idx = int(partmodel.get_value(partrow, 67))
                thetaJC = self._thetaJC[idx - 1]
                partmodel.set_value(partrow, 109, thetaJC)

            # Junction temperature.
            Tj = Tcase + thetaJC * Poper

            # Temperature correction factor.  We store this in the pi_u
            # field in the Program Database.
            _hrmodel['piT'] = exp(-1925.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

            # Application correction factor.
            idx = partmodel.get_value(partrow, 5)
            if idx == 2:
                _hrmodel['piA'] = 0.7
            elif Prated < 2.0:
                _hrmodel['piA'] = 1.5
            elif Prated >= 2.0 and Prated < 5.0:
                _hrmodel['piA'] = 2.0
            elif Prated >= 5.0 and Prated < 50.0:
                _hrmodel['piA'] = 4.0
            elif Prated >= 50.0 and Prated < 250.0:
                _hrmodel['piA'] = 8.0
            elif Prated >= 250.0:
                _hrmodel['piA'] = 10.0
            else:
                _hrmodel['piA'] = 1.0

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

            partmodel.set_value(partrow, 39, Tj)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 68, _hrmodel['piA'])
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


class Unijunction(Semiconductor):
    """
    Unijunction Transistor Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.5
    """

    def __init__(self):
        """
        Initializes the Unijunction Transistor Component Class.
        """

        Semiconductor.__init__(self)

        self.subcategory = 16               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0,
                     0.5, 14.0, 32.0, 320.0]
        self._piQ = [0.7, 1.0, 2.4, 5.5, 8.0]
        self._lambdab_count = [[0.016, 0.12, 0.20, 0.18, 0.42, 0.35, 0.80,
                                0.74, 1.6, 0.66, 0.0079, 0.31, 0.88, 6.4]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

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
            Unijunction Transistor Component Class.

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
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

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
            the Unijunction Transistor Component Class.

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
            _hrmodel['equation'] = "lambdab * piT * piQ * piE"

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
            Poper = partmodel.get_value(partrow, 64)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            _hrmodel['lambdab'] = partmodel.get_value(partrow, 46)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Prated = partmodel.get_value(partrow, 93)

            # Calculate junction temperature.  If ambient temperature and
            # temperature rise are not set (i.e., equal to zero), use the
            # default case temperature values that are based on the active
            # environment.  Otherwise calculate case temperature.
            if Tamb == 0 and Trise == 0:
                idx = int(systemmodel.get_value(systemrow, 22))
                Tcase = self._Tcase[idx - 1]
            else:
                Tcase = Tamb + Trise

            # Determine the junction-case thermal resistance.  If thetaJC is
            # not set (i.e., equal to zero), use the default value which is
            # based on the package type.
            if thetaJC == 0:
                idx = int(partmodel.get_value(partrow, 67))
                thetaJC = self._thetaJC[idx - 1]
                partmodel.set_value(partrow, 109, thetaJC)

            # Junction temperature.
            Tj = Tcase + thetaJC * Poper

            # Temperature correction factor.  We store this in the pi_u
            # field in the Program Database.
            _hrmodel['piT'] = exp(-2483.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

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

            partmodel.set_value(partrow, 39, Tj)
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


class HFLNBipolar(Semiconductor):
    """
    High Frequency, Low Noise Bipolar Transistor Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.6
    """

    _quality = ["", "JANTXV", "JANTX", "JAN", _(u"Lower")]

    def __init__(self):
        """
        Initializes the High Frequency, Low Noise Bipolar Transistor
        Component Class.
        """

        Semiconductor.__init__(self)

        self.subcategory = 17               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5,
                     9.0, 24.0, 250.0]
        self._piQ = [0.5, 1.0, 2.0, 5.0]
        self._lambdab_count = [[0.094, 0.23, 0.63, 0.46, 1.4, 0.60, 0.75, 1.3,
                                2.3, 2.4, 0.047, 1.1, 3.6, 28.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Rated Power:"))
        self._in_labels.append(_(u"Applied CE Voltage:"))
        self._in_labels.append(_(u"Rated CE Voltage:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>R</sub>\u03C0<sub>S</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>R</sub>:")
        self._out_labels.append(u"\u03C0<sub>S</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for High Frequency, Low Noise
        Bipolar Transistor Component Class prediction calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Semiconductor.assessment_inputs_create(self, part, layout,
                                                          x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 35

        # Create component specific input widgets.
        part.txtPrated = _widg.make_entry(width=100)
        part.txtOpVolts = _widg.make_entry(width=100)
        part.txtRatedVolts = _widg.make_entry(width=100)

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.cmbPackage, _x_pos, _y_pos[1])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[2])
        layout.put(part.txtPrated, _x_pos, _y_pos[3])
        layout.put(part.txtOpVolts, _x_pos, _y_pos[4])
        layout.put(part.txtRatedVolts, _x_pos, _y_pos[5])

        # Connect component specific widgets to callback methods.
        part.txtPrated.connect("focus-out-event", self._callback_entry,
                               part, "float", 93)
        part.txtOpVolts.connect("focus-out-event", self._callback_entry,
                                part, "float", 66)
        part.txtRatedVolts.connect("focus-out-event", self._callback_entry,
                                   part, "float", 94)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display High Frequency, Low Noise Bipolar Transistor
        Component Class calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Semiconductor.reliability_results_create(self, part, layout,
                                                            x_pos, y_pos)

        # Create component specific reliability result display widgets.
        part.txtPiR = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiS = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the component specific reliability result display widgets.
        layout.put(part.txtPiR, _x_pos, _y_pos[5])
        layout.put(part.txtPiS, _x_pos, _y_pos[6])

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

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Semiconductor.assessment_inputs_load(self, part)

        part.txtOpVolts.set_text(str(fmt.format(_model.get_value(_row, 66))))
        part.txtPrated.set_text(str(fmt.format(_model.get_value(_row, 93))))
        part.txtRatedVolts.set_text(str(fmt.format(
            _model.get_value(_row, 94))))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Semiconductor.assessment_results_load(self, part)

        part.txtPiR.set_text(str(fmt.format(_model.get_value(_row, 80))))
        part.txtPiS.set_text(str(fmt.format(_model.get_value(_row, 81))))

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
            High Frequency, Low Noise Bipolar Transistor Component Class.

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
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

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
            the High Frequency, Low Noise Bipolar Transistor Component Class.

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
            _hrmodel['equation'] = "lambdab * piT * piR * piS * piQ * piE"

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
            Poper = partmodel.get_value(partrow, 64)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            Vapplied = partmodel.get_value(partrow, 66)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Prated = partmodel.get_value(partrow, 93)
            Vrated = partmodel.get_value(partrow, 94)

            # Calculate junction temperature.  If ambient temperature and
            # temperature rise are not set (i.e., equal to zero), use the
            # default case temperature values that are based on the active
            # environment.  Otherwise calculate case temperature.
            if Tamb == 0 and Trise == 0:
                idx = int(systemmodel.get_value(systemrow, 22))
                Tcase = self._Tcase[idx - 1]
            else:
                Tcase = Tamb + Trise

            # Determine the junction-case thermal resistance.  If thetaJC is
            # not set (i.e., equal to zero), use the default value which is
            # based on the package type.
            if thetaJC == 0:
                idx = int(partmodel.get_value(partrow, 67))
                thetaJC = self._thetaJC[idx - 1]
                partmodel.set_value(partrow, 109, thetaJC)

            # Junction temperature.
            Tj = Tcase + thetaJC * Poper

            # Base hazard rate.
            _hrmodel['lambdab'] = 0.18

            # Temperature correction factor.  We store this in the pi_u
            # field in the Program Database.
            _hrmodel['piT'] = exp(-2114.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

            # Power rating correction factor.
            if Prated <= 0.1:
                _hrmodel['piR'] = 0.43
            else:
                _hrmodel['piR'] = Prated**0.37

            # Voltage stress correction factor.
            try:
                Vs = Vapplied / Vrated
            except ZeroDivisionError:
                Vs = 1

            _hrmodel['piS'] = 0.45 * exp(3.1 * Vs)

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

            partmodel.set_value(partrow, 39, Tj)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piR'])
            partmodel.set_value(partrow, 81, _hrmodel['piS'])
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


class HFHPBipolar(Semiconductor):
    """
    High Frequency, High Power Bipolar Transistor Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.7
    """

    _application = ["", _(u"Pulsed"), "CW"]
    _construction = ["", _(u"Gold Metallization"),
                     _(u"Aluminum Metallization")]
    _matching = ["", _(u"Input and Output"), _(u"Input Only"), _(u"None")]
    _quality = ["", "JANTXV", "JANTX", "JAN", "Lower"]

    def __init__(self):
        """
        Initializes the High Frequency, High Power Bipolar Transistor
        Component Class.
        """

        Semiconductor.__init__(self)

        self.subcategory = 18               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5,
                     9.0, 24.0, 250.0]
        self._piM = [1.0, 2.0, 4.0]
        self._piQ = [0.5, 1.0, 2.0, 5.0]
        self._lambdab_count = [[0.074, 0.15, 0.37, 0.29, 0.81, 0.29, 0.37,
                                0.52, 0.88, 0.037, 0.33, 0.66, 1.8, 18.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Application:"))
        self._in_labels.append(_(u"Duty Cycle:"))
        self._in_labels.append(_(u"Construction:"))
        self._in_labels.append(_(u"CE Operating Voltage:"))
        self._in_labels.append(_(u"CE Breakdown Voltage:"))
        self._in_labels.append(_(u"Operating Frequency:"))
        self._in_labels.append(_(u"Network Matching:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>M</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>A</sub>:")
        self._out_labels.append(u"\u03C0<sub>M</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for High Frequency, High Power
        Bipolar Transistor Component Class prediction calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Semiconductor.assessment_inputs_create(self, part, layout,
                                                          x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 35

        # Create component specific input widgets.
        part.cmbApplication = _widg.make_combo(simple=True)
        part.txtDutyCycle = _widg.make_entry(width=100)
        part.cmbConstruction = _widg.make_combo(simple=True)
        part.txtOpVolts = _widg.make_entry(width=100)
        part.txtBDVolts = _widg.make_entry(width=100)
        part.txtOpFreq = _widg.make_entry(width=100)
        # Create the network matching combo.  We store this in the
        # technology_id field in the Program Database.
        part.cmbMatching = _widg.make_combo(simple=True)

        # Load the gtk.ComboBox()
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])
        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])
        for i in range(len(self._matching)):
            part.cmbMatching.insert_text(i, self._matching[i])

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.cmbPackage, _x_pos, _y_pos[1])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[2])
        layout.put(part.cmbApplication, _x_pos, _y_pos[3])
        layout.put(part.txtDutyCycle, _x_pos, _y_pos[4])
        layout.put(part.cmbConstruction, _x_pos, _y_pos[5])
        layout.put(part.txtOpVolts, _x_pos, _y_pos[6])
        layout.put(part.txtBDVolts, _x_pos, _y_pos[7])
        layout.put(part.txtOpFreq, _x_pos, _y_pos[8])
        layout.put(part.cmbMatching, _x_pos, _y_pos[9])

        # Connect component specific widgets to callback methods.
        part.cmbApplication.connect("changed", self._callback_combo, part, 5)
        part.txtDutyCycle.connect("focus-out-event", self._callback_entry,
                                  part, "float", 19)
        part.cmbConstruction.connect("changed", self._callback_combo, part, 16)
        part.txtOpVolts.connect("focus-out-event", self._callback_entry,
                                part, "float", 66)
        part.txtBDVolts.connect("focus-out-event", self._callback_entry,
                                part, "float", 94)
        part.txtOpFreq.connect("focus-out-event", self._callback_entry,
                               part, "float", 63)
        part.cmbMatching.connect("changed", self._callback_combo, part, 104)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display High Frequency, High Power Bipolar Transistor
        Component Class calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Semiconductor.reliability_results_create(self, part, layout,
                                                            x_pos, y_pos)

        # Create component specific reliability result display widgets.
        part.txtPiA = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiM = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the component specific reliability result display widgets.
        layout.put(part.txtPiA, _x_pos, _y_pos[5])
        layout.put(part.txtPiM, _x_pos, _y_pos[6])

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

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Semiconductor.assessment_inputs_load(self, part)

        part.cmbApplication.set_active(int(_model.get_value(_row, 5)))
        part.cmbConstruction.set_active(int(_model.get_value(_row, 16)))
        part.txtDutyCycle.set_text(str(fmt.format(_model.get_value(_row, 19))))
        part.txtOpFreq.set_text(str(fmt.format(_model.get_value(_row, 63))))
        part.txtOpVolts.set_text(str(fmt.format(_model.get_value(_row, 66))))
        part.txtBDVolts.set_text(str(fmt.format(_model.get_value(_row, 94))))
        part.cmbMatching.set_active(int(_model.get_value(_row, 104)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = Semiconductor.assessment_results_load(self, part)

        part.txtPiA.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 68))))
        part.txtPiM.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 76))))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling High Frequency, High Power Bipolar
        Transistor Class ComboBox changes.

        :param gtk.ComboBox combo: the gtk.ComboBox() calling this method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param int idx: the user-defined index for the calling combobx.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _index = combo.get_active()

        (_model, _row) = Semiconductor._callback_combo(self, combo, part, idx)

        if idx == 5:                        # Application
            if _index == 1:
                part.txtDutyCycle.show()
            else:
                part.txtDutyCycle.hide()

        elif idx == 104:                    # Network matching
            _model.set_value(_row, 76, self._piM[_index - 1])

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
            High Frequency, High Power Bipolar Transistor Component Class.

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
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

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
            the High Frequency, High Power Bipolar Transistor Component Class.

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
            _hrmodel['equation'] = "lambdab * piT * piA * piM * piQ * piE"

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
            Poper = partmodel.get_value(partrow, 64)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            DC = partmodel.get_value(partrow, 19)
            Fop = partmodel.get_value(partrow, 63)
            Vop = partmodel.get_value(partrow, 66)
            _hrmodel['piM'] = partmodel.get_value(partrow, 76)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            VBD = partmodel.get_value(partrow, 94)

            # Calculate junction temperature.  If ambient temperature and
            # temperature rise are not set (i.e., equal to zero), use the
            # default case temperature values that are based on the active
            # environment.  Otherwise calculate case temperature.
            if Tamb == 0 and Trise == 0:
                idx = int(systemmodel.get_value(systemrow, 22))
                Tcase = self._Tcase[idx - 1]
            else:
                Tcase = Tamb + Trise

            # Determine the junction-case thermal resistance.  If thetaJC is
            # not set (i.e., equal to zero), use the default value which is
            # based on the package type.
            if thetaJC == 0:
                idx = int(partmodel.get_value(partrow, 67))
                thetaJC = self._thetaJC[idx - 1]
                partmodel.set_value(partrow, 109, thetaJC)

            # Junction temperature.
            Tj = Tcase + thetaJC * Poper

            # Base hazard rate.
            _hrmodel['lambdab'] = 0.032 * exp(0.354 * Fop + 0.00558 * Poper)

            # Temperature correction factor.  We store this in the pi_u
            # field in the Program Database.
            try:
                Vs = Vop / VBD
            except ZeroDivisionError:
                Vs = 0.0

            if Vs <= 0.4 and partmodel.get_value(partrow, 16) == 1:
                _hrmodel['piT'] = 0.1 * exp(-2903.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 373.0)))
            elif Vs > 0.4 and partmodel.get_value(partrow, 16) == 1:
                _hrmodel['piT'] = 2 * (0.35 * Vs) * exp(-2903.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 373.0)))
            elif Vs <= 0.4 and partmodel.get_value(partrow, 16) == 2:
                _hrmodel['piT'] = 0.38 * exp(-5794.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 373.0)))
            elif Vs > 0.4 and partmodel.get_value(partrow, 16) == 2:
                _hrmodel['piT'] = 7.55 * (0.35 * Vs) * exp(-5794.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 373.0)))
            else:
                _hrmodel['piT'] = 0.0

            # Application correction factor.
            if partmodel.get_value(partrow, 5) == 1:
                _hrmodel['piA'] = 0.06 * DC + 0.4
            elif partmodel.get_value(partrow, 5) == 2:
                _hrmodel['piA'] = 7.6
            else:
                _hrmodel['piA'] = 0.0

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

            partmodel.set_value(partrow, 39, Tj)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 68, _hrmodel['piA'])
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


class HFGaAsFET(Semiconductor):
    """
    High Frequency Gallium Arsenide (GaAs) Field Effect Transistor (FET)
    Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.8
    """

    _application = ["", _(u"Low Power and Pulsed"), "CW"]
    _matching = ["", _(u"Input and Output"), _(u"Input Only"), _(u"None")]
    _quality = ["", "JANTXV", "JANTX", "JAN", _(u"Lower")]

    def __init__(self):
        """ Initializes the High Frequency GaAs FET Component Class. """

        Semiconductor.__init__(self)

        self.subcategory = 19               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piA = [1.0, 4.0]
        self._piE = [1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5,
                     7.5, 24.0, 250.0]
        self._piM = [1.0, 2.0, 4.0]
        self._piQ = [0.5, 1.0, 2.0, 5.0]
        self._lambdab_count = [[0.17, 0.51, 1.5, 1.0, 3.4, 1.8, 2.3, 5.4, 9.2,
                                7.2, 0.083, 2.8, 11.0, 63.0],
                               [0.42, 1.3, 3.8, 2.5, 8.5, 4.5, 5.6, 13.0, 23.0,
                                18.0, 0.21, 6.9, 27.0, 160.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Application:"))
        self._in_labels.append(_(u"Operating Frequency (GHz):"))
        self._in_labels.append(_(u"Network Matching:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>M</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>A</sub>:")
        self._out_labels.append(u"\u03C0<sub>M</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for High Frequency GaAs FET
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
         _y_pos) = Semiconductor.assessment_inputs_create(self, part, layout,
                                                          x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 35

        # Create component specific input widgets.
        part.cmbApplication = _widg.make_combo(simple=True)
        part.txtOpFreq = _widg.make_entry(width=100)
        # Create the network matching combo.  We store this in the
        # technology_id field in the Program Database.
        part.cmbMatching = _widg.make_combo(simple=True)

        # Load the gtk.ComboBox()
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])
        for i in range(len(self._matching)):
            part.cmbMatching.insert_text(i, self._matching[i])

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.cmbPackage, _x_pos, _y_pos[1])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[2])
        layout.put(part.cmbApplication, _x_pos, _y_pos[3])
        layout.put(part.txtOpFreq, _x_pos, _y_pos[4])
        layout.put(part.cmbMatching, _x_pos, _y_pos[5])

        # Connect component specific widgets to callback methods.
        part.cmbApplication.connect("changed", self._callback_combo, part, 5)
        part.txtOpFreq.connect("focus-out-event", self._callback_entry,
                               part, "float", 63)
        part.cmbMatching.connect("changed", self._callback_combo, part, 104)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display High Frequency GaAs FET Component Class
        calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Semiconductor.reliability_results_create(self, part, layout,
                                                            x_pos, y_pos)

        # Create component specific reliability result display widgets.
        part.txtPiA = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiM = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the component specific reliability result display widgets.
        layout.put(part.txtPiA, _x_pos, _y_pos[5])
        layout.put(part.txtPiM, _x_pos, _y_pos[6])

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

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Semiconductor.assessment_inputs_load(self, part)

        part.cmbApplication.set_active(int(_model.get_value(_row, 5)))
        part.txtOpFreq.set_text(str(fmt.format(_model.get_value(_row, 63))))
        part.cmbMatching.set_active(int(_model.get_value(_row, 104)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Semiconductor.assessment_results_load(self, part)

        part.txtPiA.set_text(str(fmt.format(_model.get_value(_row, 68))))
        part.txtPiM.set_text(str(fmt.format(_model.get_value(_row, 76))))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling High Frequency GaAs FET Component

        :param gtk.ComboBox combo: the gtk.ComboBox() calling this method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param int idx: the user-defined index for the calling combobx.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _index = combo.get_active()

        (_model, _row) = Semiconductor._callback_combo(self, combo, part, idx)

        if idx == 5:                        # Application
            _model.set_value(_row, 68, self._piA[_index - 1])

        elif idx == 104:                    # Network matching
            _model.set_value(_row, 76, self._piM[_index - 1])

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
            High Frequency GaAs FET Component Class.

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
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

            # TODO: Validate index 64 is operating power.
            if partmodel.get_value(partrow, 64) <= 0.1:
                Pidx = 0
            else:
                Pidx = 1

            _hrmodel['lambdab'] = self._lambdab_count[Pidx][Eidx - 1]

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
            the High Frequency GaAs FET Component Class.

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
            _hrmodel['equation'] = "lambdab * piT * piA * piM * piQ * piE"

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
            Poper = partmodel.get_value(partrow, 64)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            Fop = partmodel.get_value(partrow, 63)
            _hrmodel['piA'] = partmodel.get_value(partrow, 68)
            _hrmodel['piM'] = partmodel.get_value(partrow, 76)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

            # Calculate junction temperature.  If ambient temperature and
            # temperature rise are not set (i.e., equal to zero), use the
            # default case temperature values that are based on the active
            # environment.  Otherwise calculate case temperature.
            if Tamb == 0 and Trise == 0:
                idx = int(systemmodel.get_value(systemrow, 22))
                Tcase = self._Tcase[idx - 1]
            else:
                Tcase = Tamb + Trise

            # Determine the junction-case thermal resistance.  If thetaJC is
            # not set (i.e., equal to zero), use the default value which is
            # based on the package type.
            if thetaJC == 0:
                idx = int(partmodel.get_value(partrow, 67))
                thetaJC = self._thetaJC[idx - 1]
                partmodel.set_value(partrow, 109, thetaJC)

            # Junction temperature.
            Tj = Tcase + thetaJC * Poper

            # Base hazard rate.
            if Fop >= 1.0 and Fop <= 10.0 and Poper < 0.1:
                _hrmodel['lambdab'] = 0.052
            elif Fop >= 4.0 and Fop <= 10.0 and Poper >= 0.1 and Poper <= 6:
                _hrmodel['lambdab'] = 0.0093 * exp(0.429 * Fop + 0.486 * Poper)
            else:
                _hrmodel['lambdab'] = 0.0

            # Temperature correction factor.  We store this in the pi_u
            # field in the Program Database.
            _hrmodel['piT'] = exp(-4485.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

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

            partmodel.set_value(partrow, 39, Tj)
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


class HFSiFET(Semiconductor):
    """
    High Frequency Silicon Field Effect Transistor (FET) Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.9
    """

    _quality = ["", "JANTXV", "JANTX", "JAN", _(u"Lower")]
    _technology = ["", "MOSFET", "JFET"]

    def __init__(self):
        """
        Initializes the High Frequency Silicon FET Component Class.
        """

        Semiconductor.__init__(self)

        self.subcategory = 20               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._lambdab = [0.06, 0.023]
        self._piE = [1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5,
                     9.0, 24.0, 250.0]
        self._piQ = [0.5, 1.0, 2.0, 5.0]
        self._lambdab_count = [[0.099, 0.24, 0.64, 0.47, 1.4, 0.61, 0.76, 1.3,
                                2.3, 2.4, 0.049, 1.2, 3.6, 30.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Transistor Type:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for High Frequency Silicon FET
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
         _y_pos) = Semiconductor.assessment_inputs_create(self, part, layout,
                                                          x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 35

        # Create component specific input widgets.
        # Create and populate the technology combobox.  We store this
        # in the application_id field in the program database.
        part.cmbTechnology = _widg.make_combo(simple=True)

        # Load the gtk.ComboBox()
        for i in range(len(self._technology)):
            part.cmbTechnology.insert_text(i, self._technology[i])

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.cmbPackage, _x_pos, _y_pos[1])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[2])
        layout.put(part.cmbTechnology, _x_pos, _y_pos[3])

        # Connect component specific widgets to callback methods.
        part.cmbTechnology.connect("changed", self._callback_combo, part, 104)

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

        (_model, _row) = Semiconductor.assessment_inputs_load(self, part)

        part.cmbTechnology.set_active(int(_model.get_value(_row, 104)))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling High Frequency Silicon FET Component
        Class ComboBox changes.

        :param gtk.ComboBox combo: the gtk.ComboBox() calling this method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param int idx: the user-defined index for the calling combobx.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _index = combo.get_active()

        (_model, _row) = Semiconductor._callback_combo(self, combo, part, idx)

        if idx == 104:                      # Technology
            _model.set_value(_row, 46, self._lambdab[_index - 1])

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
            High Frequency Silicon FET Component Class.

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
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

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
            the High Frequency Silicon FET Component Class.

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
            _hrmodel['equation'] = "lambdab * piT * piQ * piE"

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
            Poper = partmodel.get_value(partrow, 64)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            _hrmodel['lambdab'] = partmodel.get_value(partrow, 46)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

            # Calculate junction temperature.  If ambient temperature and
            # temperature rise are not set (i.e., equal to zero), use the
            # default case temperature values that are based on the active
            # environment.  Otherwise calculate case temperature.
            if Tamb == 0 and Trise == 0:
                idx = int(systemmodel.get_value(systemrow, 22))
                Tcase = self._Tcase[idx - 1]
            else:
                Tcase = Tamb + Trise

            # Determine the junction-case thermal resistance.  If thetaJC is
            # not set (i.e., equal to zero), use the default value which is
            # based on the package type.
            if thetaJC == 0:
                idx = int(partmodel.get_value(partrow, 67))
                thetaJC = self._thetaJC[idx - 1]
                partmodel.set_value(partrow, 109, thetaJC)

            # Junction temperature.
            Tj = Tcase + thetaJC * Poper

            # Temperature correction factor.  We store this in the pi_u
            # field in the Program Database.
            _hrmodel['piT'] = exp(-1925.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

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

            partmodel.set_value(partrow, 39, Tj)
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
