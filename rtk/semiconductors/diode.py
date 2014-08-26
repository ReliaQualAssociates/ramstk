#!/usr/bin/env python

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       diode.py is part of The RTK Project
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
from semiconductor import Semiconductor

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except ImportError:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class LowFrequency(Semiconductor):
    """
    Low Frequency Diode Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.1
    """

    _application = ["", _(u"General Purpose Analog"), _(u"Switching"),
                    _(u"Power Rectifier, Fast Recovery"),
                    _(u"Power Rectifier, Schottky"),
                    _(u"Power Rectifier, Stacked"), _(u"Transient Suppressor"),
                    _(u"Current Regulator"), _(u"Voltage Regulator/Reference")]

    _construction = ["", _(u"Metallurgically Bonded"), _(u"Spring Loaded")]

    def __init__(self):
        """
        Initializes the Low Frequency Diode Component Class.
        """

        Semiconductor.__init__(self)

        self.subcategory = 12               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._I4 = [3091, 3091, 3091, 3091, 3091, 3091, 1925, 1925]
        self._lambdab = [0.0038, 0.0010, 0.069, 0.003, 0.005, 0.0013, 0.0034,
                         0.002]
        self._piC = [1.0, 2.0]
        self._piE = [1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0,
                     0.5, 14.0, 32.0, 320.0]
        self._piQ = [0.7, 1.0, 2.4, 5.5, 8.0]
        self._lambdab_count = [[0.00360, 0.0280, 0.049, 0.043, 0.100, 0.092,
                                0.210, 0.200, 0.44, 0.170, 0.00180, 0.076,
                                0.23, 1.50],
                               [0.00094, 0.0075, 0.013, 0.011, 0.027, 0.024,
                                0.054, 0.054, 0.12, 0.045, 0.00047, 0.020,
                                0.06, 0.40],
                               [0.06500, 0.5200, 0.890, 0.780, 1.900, 1.700,
                                3.700, 3.700, 8.00, 3.100, 0.03200, 1.400,
                                4.10, 28.0],
                               [0.00280, 0.0220, 0.039, 0.034, 0.062, 0.073,
                                0.160, 0.160, 0.35, 0.130, 0.00140, 0.060,
                                0.18, 1.20],
                               [0.00290, 0.0230, 0.040, 0.035, 0.084, 0.075,
                                0.170, 0.170, 0.36, 0.140, 0.00150, 0.062,
                                0.18, 1.20],
                               [0.00330, 0.0240, 0.039, 0.035, 0.082, 0.066,
                                0.150, 0.130, 0.27, 0.120, 0.00160, 0.060,
                                0.16, 1.30],
                               [0.00560, 0.0400, 0.066, 0.060, 0.140, 0.110,
                                0.250, 0.220, 0.460, 0.21, 0.00280, 0.100,
                                0.28, 2.10]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Application:"))
        self._in_labels.append(_(u"Contact Construction:"))
        self._in_labels.append(_(u"Applied Voltage (V<sub>Applied</sub>):"))
        self._in_labels.append(_(u"Rated Voltage (V<sub>Rated</sub>):"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>S</sub>\u03C0<sub>C</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>S</sub>:")
        self._out_labels.append(u"\u03C0<sub>C</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Low Frequency Diode
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
        _x_pos = max(x_pos, _x_pos) + 45

        # Create component specific input widgets.
        part.cmbApplication = _widg.make_combo(simple=True)
        part.cmbConstruction = _widg.make_combo(simple=True)
        part.txtVApplied = _widg.make_entry(width=100)
        part.txtVRated = _widg.make_entry(width=100)

        # Load gtk.ComboBox().
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])
        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.cmbPackage, _x_pos, _y_pos[1])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[2])
        layout.put(part.cmbApplication, _x_pos, _y_pos[3])
        layout.put(part.cmbConstruction, _x_pos, _y_pos[4])
        layout.put(part.txtVApplied, _x_pos, _y_pos[5])
        layout.put(part.txtVRated, _x_pos, _y_pos[6])

        # Connect component specific widgets to callback methods.
        part.cmbApplication.connect("changed", self._callback_combo, part, 5)
        part.cmbConstruction.connect("changed", self._callback_combo, part, 16)
        part.txtVApplied.connect("focus-out-event", self._callback_entry, part,
                                 "float", 66)
        part.txtVRated.connect("focus-out-event", self._callback_entry, part,
                               "float", 94)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Low Frequency Diode calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Semiconductor.reliability_results_create(self, part, layout,
                                                            x_pos, y_pos)

        # Create component specific reliability result display widgets.
        part.txtPiS = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiC = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the component specifci reliability result display widgets.
        layout.put(part.txtPiS, _x_pos, _y_pos[5])
        layout.put(part.txtPiC, _x_pos, _y_pos[6])

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
        part.txtVApplied.set_text(str(fmt.format(_model.get_value(_row, 66))))
        part.txtVRated.set_text(str(fmt.format(_model.get_value(_row, 94))))

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

        part.txtPiC.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 69))))
        part.txtPiS.set_text(str(fmt.format(_model.get_value(_row, 81))))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Low Frequency Diode Semicondutor
        Class ComboBox changes.

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

        Semiconductor._callback_combo(self, combo, part, idx)

        if idx == 5:                        # Application
            _model.set_value(_row, 34, self._I4[_index - 1])
            _model.set_value(_row, 46, self._lambdab[_index - 1])

        elif idx == 16:                     # Construction
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
            Low Frequency Diode Class.

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
            Aidx = partmodel.get_value(partrow, 5)          # Application index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Aidx - 1][Eidx - 1]

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
            the Low Frequency Diode Component Class.

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
            _hrmodel['equation'] = "lambdab * piT * piS * piC * piQ * piE"

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
            I4 = partmodel.get_value(partrow, 34)
            _hrmodel['lambdab'] = partmodel.get_value(partrow, 46)
            VApplied = partmodel.get_value(partrow, 66)
            _hrmodel['piC'] = partmodel.get_value(partrow, 69)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Prated = partmodel.get_value(partrow, 93)
            VRated = partmodel.get_value(partrow, 94)

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
            Tj = Tcase + thetaJC * P

            # Temperature correction factor.  We store this in the pi_u
            # field in the Program Database.
            _hrmodel['piT'] = exp(-I4 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

            # Voltage stress correction factor.  We store this in the pi_sr
            # field in the Program Database.
            if partmodel.get_value(partrow, 5) < 7:
                Vs = VApplied / VRated
                if Vs > 0.3 and Vs < 1.0:
                    _hrmodel['piS'] = Vs**2.43
                else:
                    _hrmodel['piS'] = 0.54
            else:
                _hrmodel['piS'] = 1.0

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
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
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


class HighFrequency(Semiconductor):
    """
    High Frequency Diode Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.2
    """

    _application = ["", _(u"Varactor, Voltage Control"),
                    _(u"Varactor, Multiplier"), _(u"All Others")]

    _construction = ["", u"Si IMPATT", _(u"Gunn/Bulk Effect"),
                     _(u"Tunnel and Back"), u"PIN", _(u"Schottky Barrier"),
                     u"Varactor"]

    def __init__(self):
        """
        Initializes the High Frequency Diode Component Class.
        """

        Semiconductor.__init__(self)

        self.subcategory = 13               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._I4 = [5260, 2100, 2100, 2100, 2100, 2100]
        self._lambdab = [0.22, 0.18, 0.0023, 0.0081, 0.027, 0.0025]
        self._piA = [0.5, 2.5, 1.0]
        self._piE = [1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5,
                     9.0, 24.0, 250.0]
        self._piQ = [0.5, 1.0, 5.0, 25, 50]
        self._piQS = [0.5, 1.0, 1.8, 2.5, 1.0]
        self._lambdab_count = [[0.86, 2.80, 8.9, 5.6, 20.0, 11.0, 14.0, 36.0,
                                62.0, 44.0, 0.43, 16.0, 67.0, 350.0],
                               [0.31, 0.76, 2.1, 1.5, 4.60, 2.00, 2.50, 4.50,
                                7.60, 7.90, 0.16, 3.70, 12.0, 94.00],
                               [0.004, 0.0096, 0.0026, 0.0019, 0.058, 0.025,
                                0.032, 0.057, 0.097, 0.10, 0.002, 0.048, 0.15,
                                1.2],
                               [0.028, 0.068, 0.19, 0.14, 0.41, 0.18, 0.22,
                                0.40, 0.69, 0.71, 0.014, 0.34, 1.1, 8.5],
                               [0.047, 0.11, 0.31, 0.23, 0.68, 0.3, 0.37, 0.67,
                                1.1, 1.2, 0.023, 0.56, 1.8, 14.0],
                               [0.0043, 0.010, 0.029, 0.021, 0.063, 0.028,
                                0.034, 0.062, 0.11, 0.11, 0.0022, 0.052, 0.17,
                                1.3]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Application:"))
        self._in_labels.append(_(u"Diode Type:"))
        self._in_labels.append(_(u"Rated Power (P<sub>Rated</sub>):"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>A</sub>:")
        self._out_labels.append(u"\u03C0<sub>R</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for High Frequency Diode
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
        part.cmbConstruction = _widg.make_combo(simple=True)
        part.txtPwrRated = _widg.make_entry(width=100)

        # Load gtk.ComboBox().
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])
        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.cmbPackage, _x_pos, _y_pos[1])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[2])
        layout.put(part.cmbApplication, _x_pos, _y_pos[3])
        layout.put(part.cmbConstruction, _x_pos, _y_pos[4])
        layout.put(part.txtPwrRated, _x_pos, _y_pos[5])

        # Connect component specific widgets to callback methods.
        part.cmbApplication.connect("changed", self._callback_combo, part, 5)
        part.cmbConstruction.connect("changed", self._callback_combo, part, 16)
        part.txtPwrRated.connect("focus-out-event", self._callback_entry,
                                 part, "float", 93)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display High Frequency Diode calculation results.

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

        # Place the results widgets.
        layout.put(part.txtPiA, _x_pos, _y_pos[5])
        layout.put(part.txtPiR, _x_pos, _y_pos[6])

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
        part.txtPwrRated.set_text(str(fmt.format(_model.get_value(_row, 93))))

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
        part.txtPiR.set_text(str(fmt.format(_model.get_value(_row, 80))))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling High Frequency Diode Semicondutor
        Class ComboBox changes.

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

        Semiconductor._callback_combo(self, combo, part, idx)

        if idx == 5:                    # Application
            _model.set_value(_row, 68, self._piA[_index - 1])

        elif idx == 16:                 # Construction
            _model.set_value(_row, 34, self._I4[_index - 1])
            _model.set_value(_row, 46, self._lambdab[_index - 1])

        # Quality for Schottky diodes only.
        elif idx == 85 and _model.get_value(_row, 16) == 5:
            _model.set_value(_row, 79, self._piQS[_index - 1])

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
            High Frequency Diode Component Class.

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
            Aidx = partmodel.get_value(partrow, 5)          # Application index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Aidx - 1][Eidx - 1]

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
            the High Frequency Diode Component Class.

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
            _hrmodel['equation'] = "lambdab * piT * piA * piR * piQ * piE"

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
            I4 = partmodel.get_value(partrow, 34)
            _hrmodel['lambdab'] = partmodel.get_value(partrow, 46)
            _hrmodel['piA'] = partmodel.get_value(partrow, 68)
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

            Tj = Tcase + thetaJC * P

            # Temperature correction factor.  We store this in the pi_u
            # field in the Program Database.
            _hrmodel['piT'] = exp(-I4 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

            # Power rating correction factor.
            if partmodel.get_value(partrow, 16) == 4:
                _hrmodel['piR'] = 0.326 * log(Prated) - 0.25
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


            # Calculate the component predicted hazard rate.
            _lambdap = _lambdaa + _lambdad + _lambdas

            # Calculate overstresses.
            (_overstress,
             self.reason) = _calc.overstressed(partmodel, partrow,
                                               systemmodel, systemrow)

            partmodel.set_value(partrow, 39, Tj)
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piR'])
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
