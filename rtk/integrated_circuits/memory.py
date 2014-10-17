#!/usr/bin/env python

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       memory.py is part of The RTK Project
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
from ic import IntegratedCircuit

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except ImportError:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class MemoryDRAM(IntegratedCircuit):
    """
    DRAM memory class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.2
    """

    def __init__(self):
        """
        Initializes the Memory, DRAM Integrated Circuit Component Class.
        """

        IntegratedCircuit.__init__(self)

        self.subcategory = 7                # Subcategory ID in the rtkcom DB.

        self._B = [16384, 65536, 262144, 1024000]

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        # There is no C1 for the bipolar DRAM model.
        self._C1 = [[0.0, 0.0, 0.0, 0.0],
                    [0.0013, 0.0025, 0.005, 0.01]]

        self._lambdab_count = [[0.0040, 0.014, 0.027, 0.027, 0.040, 0.029,
                                0.035, 0.040, 0.059, 0.055, 0.0040, 0.034,
                                0.080, 1.4],
                               [0.0055, 0.019, 0.039, 0.034, 0.051, 0.039,
                                0.047, 0.056, 0.079, 0.070, 0.0055, 0.043,
                                0.100, 1.7],
                               [0.0074, 0.023, 0.043, 0.040, 0.060, 0.049,
                                0.058, 0.076, 0.100, 0.084, 0.0074, 0.051,
                                0.120, 1.9],
                               [0.0110, 0.032, 0.057, 0.053, 0.077, 0.070,
                                0.080, 0.120, 0.150, 0.110, 0.0110, 0.067,
                                0.150, 2.3]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[2] = _(u"# of Bits:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Memory, DRAM Integrated
        Circuit prediction calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = IntegratedCircuit.assessment_inputs_create(self, part,
                                                              layout,
                                                              x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 35

        # Update the number of elements gtk.ComboBox().
        part.cmbElements.append_text("")
        part.cmbElements.append_text(_(u"Up to 16K"))
        part.cmbElements.append_text(_(u"16K to 64K"))
        part.cmbElements.append_text(_(u"64K to 256K"))
        part.cmbElements.append_text(_(u"256K to 1M"))

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.move(part.cmbTechnology, _x_pos, _y_pos[2])
        layout.move(part.cmbElements, _x_pos, _y_pos[3])
        layout.move(part.cmbPackage, _x_pos, _y_pos[4])
        layout.move(part.txtNumPins, _x_pos, _y_pos[5])
        layout.move(part.txtYears, _x_pos, _y_pos[6])

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

        (_model, _row) = IntegratedCircuit.assessment_inputs_load(self, part)

        part.cmbElements.set_active(int(_model.get_value(_row, 24)))

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
            Memory, DRAM Integrated Circuit Class.

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
            _hrmodel['equation'] = "lambdab * piQ * piL"

            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hazard rate inputs.
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
            Bidx = partmodel.get_value(partrow, 24)         # No of elements index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Y = partmodel.get_value(partrow, 112)

            _hrmodel['lambdab'] = self._lambdab_count[Bidx - 1][Eidx - 1]

            # Calculate the learning factor.  We store this in the pi_r
            # field in the Program Database.
            _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

            # Calculate component active hazard rate.
            _lambdaa = _calc.calculate_part(_hrmodel)
            _lambdaa = _lambdaa * _quantity / 1000000.0

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 80, _hrmodel['piL'])

            systemmodel.set_value(systemrow, 28, _lambdaa)
            systemmodel.set_value(systemrow, 32, _lambdaa)
            systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

            return False

        def _calculate_mil_217_stress(partmodel, partrow,
                                      systemmodel, systemrow):
            """
            Performs MIL-HDBK-217F part stress hazard rate calculations for
            the Memory, DRAM Integrated Circuit Class.

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
            _hrmodel['equation'] = "(C1 * piT + C2 * piE) * piQ * piL"

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
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)
            P = partmodel.get_value(partrow, 64)

            # Retrieve hazard rate inputs.
            _hrmodel['C1'] = partmodel.get_value(partrow, 8)
            K1 = partmodel.get_value(partrow, 40)
            K2 = partmodel.get_value(partrow, 41)
            K3 = partmodel.get_value(partrow, 42)
            B = partmodel.get_value(partrow, 58)
            Np = partmodel.get_value(partrow, 60)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Tbase = partmodel.get_value(partrow, 103)
            Y = partmodel.get_value(partrow, 112)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Vapplied = partmodel.get_value(partrow, 66)
            Irated = partmodel.get_value(partrow, 92)
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
            idx = int(partmodel.get_value(partrow, 67))
            if thetaJC == 0:
                thetaJC = self._thetaJC[idx - 1]
                partmodel.set_value(partrow, 109, thetaJC)
            else:
                thetaJC = partmodel.get_value(partrow, 109)

            Tj = Tcase + thetaJC * P

            # Calculate the temperature factor.  We store this in the pi_u
            # field in the Program Database.
            _hrmodel['piT'] = 0.1 * exp((-1.0 * 0.65 / 0.00008617) * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

            K5 = self._K5[idx - 1]
            K6 = self._K6[idx - 1]
            _hrmodel['C2'] = K5 * (Np ** K6)

            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

            # Calculate the learning factor.  We store this in the pi_r
            # field in the Program Database.
            _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

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
            _v_ratio = Vapplied / Vrated

            partmodel.set_value(partrow, 9, _hrmodel['C2'])
            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 35, K5)
            partmodel.set_value(partrow, 36, K6)
            partmodel.set_value(partrow, 39, Tj)
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piL'])
            partmodel.set_value(partrow, 82, _hrmodel['piT'])
            partmodel.set_value(partrow, 111, _v_ratio)

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


class MemoryEEPROM(IntegratedCircuit):
    """
    EEPROM memory class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.2
    """

    # For programming cycles combobox item list.
    _cycles = ["", _(u"Up to 100"), _(u"100 to 200"), _(u"200 to 500"),
               _(u"500 to 1K"), _(u"1K to 3K"), _(u"3K to 7K"),
               _(u"7K to 15K"), _(u"15K to 20K"), _(u"20K to 30K"),
               _(u"30K to 100K"), _(u"100K to 200K"), _(u"200K to 300K"),
               _(u"300K to 400K"), _(u"400K to 500K")]

    # For error correction code combobox item list.
    _ecc = ["", _(u"No ECC"), _(u"Hamming Code"),
            _(u"Two Needs One Redundant Cell")]

    # For manufacturing type combobox item list.
    _man = ["", "FLOTOX", _(u"Textured-Poly")]

    def __init__(self):
        """
        Initializes the Memory, EEPROM Integrated Circuit Component
        Class.
        """

        IntegratedCircuit.__init__(self)

        self.subcategory = 6                # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._A1 = [[0.0007, 0.0014, 0.0034, 0.0068, 0.02, 0.049, 0.1, 0.14,
                     0.2, 0.68, 1.3, 2.7, 2.7, 3.4],
                    [0.0097, 0.014, 0.023, 0.033, 0.061, 0.14, 0.3, 0.3, 0.3,
                     0.3, 0.3, 0.3, 0.3, 0.3]]
        self._A2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.1, 2.3]]
        self._B = [16384, 65536, 262144, 1024000]
        self._C1 = [[0.0094, 0.019, 0.038, 0.075],
                    [0.00085, 0.0017, 0.0034, 0.0068]]
        self._K1 = [16000, 64000]
        self._K2 = [0.5, 0.25]
        self._K3 = [0.15, 0.12]
        self._piECC = [1.0, 0.72, 0.68]
        self._Tbase = [303, 333]

        self._lambdab_count = [[[0.010, 0.028, 0.050, 0.046, 0.067, 0.082,
                                 0.070, 0.10, 0.13, 0.096, 0.010, 0.058, 0.13,
                                 1.9],
                                [0.017, 0.043, 0.071, 0.063, 0.091, 0.095,
                                 0.110, 0.18, 0.21, 0.140, 0.017, 0.081, 0.18,
                                 2.3],
                                [0.028, 0.065, 0.100, 0.085, 0.120, 0.150,
                                 0.160, 0.30, 0.33, 0.190, 0.028, 0.110, 0.23,
                                 2.3],
                                [0.053, 0.120, 0.180, 0.150, 0.210, 0.270,
                                 0.290, 0.56, 0.61, 0.330, 0.053, 0.190, 0.39,
                                 3.4]],
                               [[0.0049, 0.018, 0.036, 0.036, 0.053, 0.037,
                                 0.046, 0.049, 0.075, 0.072, 0.0048, 0.045,
                                 0.11, 1.9],
                                [0.0061, 0.022, 0.044, 0.043, 0.064, 0.046,
                                 0.056, 0.062, 0.093, 0.087, 0.0062, 0.054,
                                 0.13, 2.3],
                                [0.0072, 0.024, 0.048, 0.045, 0.067, 0.051,
                                 0.061, 0.073, 0.100, 0.092, 0.0072, 0.057,
                                 0.13, 2.3],
                                [0.0120, 0.038, 0.071, 0.068, 0.100, 0.080,
                                 0.095, 0.120, 0.180, 0.140, 0.0120, 0.086,
                                 0.20, 3.3]]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[2] = _(u"# of Bits:")
        self._in_labels.append(_(u"# Prog Cycles:"))
        self._in_labels.append(_(u"Error Correction Code:"))
        self._in_labels.append(_(u"Manufacture Method:"))
        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub> + \u03BB<sub>CYC</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"

        self._out_labels.insert(9, u"\u03BB<sub>CYC</sub>:")
        self._out_labels.append(u"\u03C0<sub>ECC</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Memory, EEPROM Integrated
        Circuit prediction calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = IntegratedCircuit.assessment_inputs_create(self, part,
                                                              layout,
                                                              x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 35

        part.cmbCycles = _widg.make_combo(simple=True)
        part.cmbECC = _widg.make_combo(simple=True)
        part.cmbManufacturing = _widg.make_combo(simple=True)

        # Load all the gtk.ComboBox().
        part.cmbElements.append_text("")
        part.cmbElements.append_text(_(u"Up to 16K"))
        part.cmbElements.append_text(_(u"16K to 64K"))
        part.cmbElements.append_text(_(u"64K to 256K"))
        part.cmbElements.append_text(_(u"256K to 1M"))

        for i in range(len(self._cycles)):
            part.cmbCycles.insert_text(i, self._cycles[i])
        for i in range(len(self._ecc)):
            part.cmbECC.insert_text(i, self._ecc[i])
        for i in range(len(self._man)):
            part.cmbManufacturing.insert_text(i, self._man[i])

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.move(part.cmbTechnology, _x_pos, _y_pos[2])
        layout.move(part.cmbElements, _x_pos, _y_pos[3])
        layout.move(part.cmbPackage, _x_pos, _y_pos[4])
        layout.move(part.txtNumPins, _x_pos, _y_pos[5])
        layout.move(part.txtYears, _x_pos, _y_pos[6])
        layout.put(part.cmbCycles, _x_pos, _y_pos[7])
        layout.put(part.cmbECC, _x_pos, _y_pos[8])
        layout.put(part.cmbManufacturing, _x_pos, _y_pos[9])

        # Connect to callback methods.
        part.cmbCycles.connect("changed", self._callback_combo, part, 18)
        part.cmbECC.connect("changed", self._callback_combo, part, 23)
        part.cmbManufacturing.connect("changed",
                                      self._callback_combo, part, 54)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Memory, EEPROM Integrated Circuit calculation
        results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = IntegratedCircuit.reliability_results_create(self, part,
                                                                layout,
                                                                x_pos, y_pos)

        # Create the EEPROM specific reliability results widgets.
        part.txtPiECC = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtlambdaCYC = _widg.make_entry(width=100, editable=False,
                                             bold=True)

        # Place the reliability results widgets.
        layout.move(part.txtC1, _x_pos, _y_pos[1])
        layout.move(part.txtPiT, _x_pos, _y_pos[2])
        layout.move(part.txtC2, _x_pos, _y_pos[3])
        layout.move(part.txtPiE, _x_pos, _y_pos[4])
        layout.move(part.txtPiQ, _x_pos, _y_pos[5])
        layout.move(part.txtPiL, _x_pos, _y_pos[6])
        layout.put(part.txtPiECC, _x_pos, _y_pos[7])
        layout.put(part.txtlambdaCYC, _x_pos, _y_pos[8])

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

        (_model, _row) = IntegratedCircuit.assessment_inputs_load(self, part)

        part.cmbCycles.set_active(int(_model.get_value(_row, 18)))
        part.cmbECC.set_active(int(_model.get_value(_row, 23)))
        part.cmbElements.set_active(int(_model.get_value(_row, 24)))
        part.cmbManufacturing.set_active(int(_model.get_value(_row, 54)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = "{0:0." + str(_conf.PLACES) + "g}"

        (_model, _row) = IntegratedCircuit.assessment_results_load(self, part)

        part.txtlambdaCYC.set_text(str(fmt.format(_model.get_value(_row, 52))))
        part.txtPiECC.set_text(str(fmt.format(_model.get_value(_row, 73))))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling ComboBox changes specific to the
        Memory, EEPROM Integrated Circuit Component Class.

        :param gtk.ComboBox combo: the gtk.ComboBox() calling this method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param int idx: the user-defined index for the calling combobx.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        IntegratedCircuit._callback_combo(self, combo, part, idx)

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        _index = combo.get_active()

        if idx == 18:                       # Programming Cycles
            _index2 = part.cmbManufacturing.get_active()

            _model.set_value(_row, 3, self._A1[_index2 - 1][_index - 1])
            _model.set_value(_row, 4, self._A2[_index2 - 1][_index - 1])

        elif idx == 23:                     # Error Correction Code
            _model.set_value(_row, 73, self._piECC[_index - 1])

        elif idx == 24:                     # Number of elements
            _model.set_value(_row, 58, self._B[_index - 1])

        elif idx == 54:                     # Manufacturing process
            _model.set_value(_row, 40, self._K1[_index - 1])
            _model.set_value(_row, 41, self._K2[_index - 1])
            _model.set_value(_row, 42, self._K3[_index - 1])
            _model.set_value(_row, 103, self._Tbase[_index - 1])

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
            _hrmodel['equation'] = "lambdab * piQ * piL"

            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hazard rate inputs.
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
            Bidx = partmodel.get_value(partrow, 24)         # No of elements index
            Tidx = partmodel.get_value(partrow, 104)        # Technology index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Y = partmodel.get_value(partrow, 112)

            _hrmodel['lambdab'] = self._lambdab_count[Tidx - 1][Bidx - 1][Eidx - 1]

            # Calculate the learning factor.  We store this in the pi_r
            # field in the Program Database.
            _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

            # Calculate component active hazard rate.
            _lambdaa = _calc.calculate_part(_hrmodel)
            _lambdaa = _lambdaa * _quantity / 1000000.0

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 80, _hrmodel['piL'])

            systemmodel.set_value(systemrow, 28, _lambdaa)
            systemmodel.set_value(systemrow, 32, _lambdaa)
            systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

            return False

        def _calculate_mil_217_stress(partmodel, partrow,
                                      systemmodel, systemrow):
            """
            Performs MIL-HDBK-217F part stress hazard rate calculations for
            the Linear Integrated Circuit Class.

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
            _hrmodel['equation'] = "(C1 * piT + C2 * piE + lambdaCYC) * piQ * piL"

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
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)
            P = partmodel.get_value(partrow, 64)

            # Retrieve hazard rate inputs.
            A1 = partmodel.get_value(partrow, 3)
            A2 = partmodel.get_value(partrow, 4)
            _hrmodel['C1'] = partmodel.get_value(partrow, 8)
            K1 = partmodel.get_value(partrow, 40)
            K2 = partmodel.get_value(partrow, 41)
            K3 = partmodel.get_value(partrow, 42)
            K5 = partmodel.get_value(partrow, 35)
            K6 = partmodel.get_value(partrow, 36)
            B = partmodel.get_value(partrow, 58)
            Np = partmodel.get_value(partrow, 60)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Tbase = partmodel.get_value(partrow, 103)
            Y = partmodel.get_value(partrow, 112)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Vapplied = partmodel.get_value(partrow, 66)
            Irated = partmodel.get_value(partrow, 92)
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
            else:
                thetaJC = partmodel.get_value(partrow, 109)

            Tj = Tcase + thetaJC * P

            # Calculate the temperature factor.  We store this in the pi_u
            # field in the Program Database.
            _hrmodel['piT'] = 0.1 * exp((-0.6 / 0.00008617) * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

            _hrmodel['C2'] = K5 * (Np ** K6)

            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

            idx = partmodel.get_value(partrow, 23)
            _hrmodel['piECC'] = self._piECC[idx - 1]

            # Calculate failure rate due to programming cycles.  We store
            # this in the lambda_g field in the Program Database.
            B1 = ((B / K1)**K2) * exp((-1.0 * K3 / 0.0000863) * ((1 / (Tj + 273)) - (1 / Tbase)))
            B2 = ((B / K1)**K2) * exp((-0.1 / 8.63E-5) * ((1 / (Tj + 273)) - (1 / Tbase)))
            _hrmodel['lambdaCYC'] = (A1 * B1 + ((A2 * B2) / float(_hrmodel['piQ']))) * float(_hrmodel['piECC'])

            # Calculate the learning factor.  We store this in the pi_r
            # field in the Program Database.
            _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

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
            _v_ratio = Vapplied / Vrated

            partmodel.set_value(partrow, 9, _hrmodel['C2'])
            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 39, Tj)
            partmodel.set_value(partrow, 52, _hrmodel['lambdaCYC'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 73, _hrmodel['piECC'])
            partmodel.set_value(partrow, 80, _hrmodel['piL'])
            partmodel.set_value(partrow, 82, _hrmodel['piT'])
            partmodel.set_value(partrow, 111, _v_ratio)

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


class MemoryROM(IntegratedCircuit):
    """
    ROM Memory class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.2
    """

    def __init__(self):
        """
        Initializes the Memory, ROM Integrated Circuit Component Class.
        """

        IntegratedCircuit.__init__(self)

        self.subcategory = 5                # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._B = [16384, 65536, 262144, 1024000]
        self._C1 = [[0.0094, 0.019, 0.038, 0.075],
                    [0.00085, 0.0017, 0.0034, 0.0068]]

        self._lambdab_count = [[[0.010, 0.028, 0.050, 0.046, 0.067, 0.062,
                                 0.070, 0.10, 0.13, 0.096, 0.010, 0.058, 0.13,
                                 1.9],
                                [0.017, 0.043, 0.071, 0.063, 0.091, 0.095,
                                 0.110, 0.18, 0.21, 0.140, 0.017, 0.081, 0.18,
                                 2.3],
                                [0.028, 0.065, 0.100, 0.085, 0.120, 0.150,
                                 0.180, 0.30, 0.33, 0.190, 0.028, 0.110, 0.23,
                                 2.3],
                                [0.053, 0.120, 0.180, 0.150, 0.210, 0.270,
                                 0.290, 0.56, 0.61, 0.330, 0.053, 0.190, 0.39,
                                 3.4]],
                               [[0.0047, 0.018, 0.036, 0.035, 0.053, 0.037,
                                 0.045, 0.048, 0.074, 0.071, 0.0047, 0.044,
                                 0.11, 1.9],
                                [0.0059, 0.022, 0.043, 0.042, 0.063, 0.045,
                                 0.055, 0.060, 0.090, 0.086, 0.0059, 0.053,
                                 0.13, 2.3],
                                [0.0067, 0.023, 0.045, 0.044, 0.066, 0.048,
                                 0.059, 0.068, 0.099, 0.089, 0.0067, 0.055,
                                 0.13, 2.3],
                                [0.0110, 0.036, 0.068, 0.066, 0.098, 0.075,
                                 0.090, 0.110, 0.150, 0.140, 0.0110, 0.083,
                                 0.20, 3.3]]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[2] = _(u"# of Bits:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Memory, ROM Integrated Circuit
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
         _y_pos) = IntegratedCircuit.assessment_inputs_create(self, part,
                                                              layout,
                                                              x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 35

        # Load the number of elements gtk.ComboBox().
        part.cmbElements.append_text("")
        part.cmbElements.append_text(_(u"Up to 16K"))
        part.cmbElements.append_text(_(u"16K to 64K"))
        part.cmbElements.append_text(_(u"64K to 256K"))
        part.cmbElements.append_text(_(u"256K to 1M"))

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.move(part.cmbTechnology, _x_pos, _y_pos[2])
        layout.move(part.cmbElements, _x_pos, _y_pos[3])
        layout.move(part.cmbPackage, _x_pos, _y_pos[4])
        layout.move(part.txtNumPins, _x_pos, _y_pos[5])
        layout.move(part.txtYears, _x_pos, _y_pos[6])

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with
        calculation input information.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = IntegratedCircuit.assessment_inputs_load(self, part)

        part.cmbElements.set_active(int(_model.get_value(_row, 24)))

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
            _hrmodel['equation'] = "lambdab * piQ * piL"

            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hazard rate inputs.
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
            Bidx = partmodel.get_value(partrow, 24)         # No of elements index
            Tidx = partmodel.get_value(partrow, 104)        # Technology index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Y = partmodel.get_value(partrow, 112)

            _hrmodel['lambdab'] = self._lambdab_count[Tidx - 1][Bidx - 1][Eidx - 1]

            # Calculate the learning factor.  We store this in the pi_r
            # field in the Program Database.
            _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

            # Calculate component active hazard rate.
            _lambdaa = _calc.calculate_part(_hrmodel)
            _lambdaa = _lambdaa * _quantity / 1000000.0

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 80, _hrmodel['piL'])

            systemmodel.set_value(systemrow, 28, _lambdaa)
            systemmodel.set_value(systemrow, 32, _lambdaa)
            systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

            return False

        def _calculate_mil_217_stress(partmodel, partrow,
                                      systemmodel, systemrow):
            """
            Performs MIL-HDBK-217F part stress hazard rate calculations for
            the Linear Integrated Circuit Class.

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
            _hrmodel['equation'] = "(C1 * piT + C2 * piE) * piQ * piL"

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
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)
            P = partmodel.get_value(partrow, 64)

            # Retrieve hazard rate inputs.
            _hrmodel['C1'] = partmodel.get_value(partrow, 8)
            K1 = partmodel.get_value(partrow, 40)
            K2 = partmodel.get_value(partrow, 41)
            K3 = partmodel.get_value(partrow, 42)
            K5 = partmodel.get_value(partrow, 35)
            K6 = partmodel.get_value(partrow, 36)
            B = partmodel.get_value(partrow, 58)
            Np = partmodel.get_value(partrow, 60)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Tbase = partmodel.get_value(partrow, 103)
            Y = partmodel.get_value(partrow, 112)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Vapplied = partmodel.get_value(partrow, 66)
            Irated = partmodel.get_value(partrow, 92)
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
            else:
                thetaJC = partmodel.get_value(partrow, 109)

            Tj = Tcase + thetaJC * P

            # Calculate the temperature factor.  We store this in the pi_u
            # field in the Program Database.
            _hrmodel['piT'] = 0.1 * exp((-1.0 * 0.65 / 0.00008617) * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

            _hrmodel['C2'] = K5 * (Np ** K6)

            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

            # Calculate the learning factor.  We store this in the pi_r
            # field in the Program Database.
            _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

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
            _v_ratio = Vapplied / Vrated

            partmodel.set_value(partrow, 9, _hrmodel['C2'])
            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 39, Tj)
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piL'])
            partmodel.set_value(partrow, 82, _hrmodel['piT'])
            partmodel.set_value(partrow, 111, _v_ratio)

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


class MemorySRAM(IntegratedCircuit):
    """
    SRAM memory class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.2
    """

    def __init__(self):
        """
        Initializes the Memory, SRAM Integrated Circuit Component Class.
        """

        IntegratedCircuit.__init__(self)

        self.subcategory = 8                # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._B = [16384, 65536, 262144, 1024000]
        self._C1 = [[0.0062, 0.011, 0.021, 0.042],
                    [0.0062, 0.011, 0.021, 0.042]]

        self._lambdab_count = [[[0.0075, 0.023, 0.043, 0.041, 0.060, 0.050,
                                 0.058, 0.077, 0.10, 0.084, 0.0075, 0.052,
                                 0.12, 1.9],
                                [0.0120, 0.033, 0.058, 0.054, 0.079, 0.072,
                                 0.083, 0.120, 0.15, 0.110, 0.0120, 0.069,
                                 0.15, 2.3],
                                [0.0180, 0.045, 0.074, 0.065, 0.095, 0.100,
                                 0.110, 0.190, 0.22, 0.140, 0.0180, 0.084,
                                 0.18, 2.3],
                                [0.0330, 0.079, 0.130, 0.110, 0.160, 0.180,
                                 0.200, 0.350, 0.39, 0.240, 0.0330, 0.140,
                                 0.30, 3.4]],
                               [[0.0079, 0.022, 0.038, 0.034, 0.050, 0.048,
                                 0.054, 0.083, 0.10, 0.073, 0.0079, 0.044,
                                 0.098, 1.4],
                                [0.0140, 0.034, 0.057, 0.050, 0.073, 0.077,
                                 0.085, 0.140, 0.17, 0.110, 0.0140, 0.065,
                                 0.140, 1.8],
                                [0.0230, 0.053, 0.084, 0.071, 0.100, 0.120,
                                 0.130, 0.250, 0.27, 0.160, 0.0230, 0.092,
                                 0.190, 1.9],
                                [0.0430, 0.092, 0.140, 0.110, 0.160, 0.220,
                                 0.230, 0.460, 0.49, 0.260, 0.0430, 0.150,
                                 0.300, 2.3]]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[2] = _(u"# of Bits:")
        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Memory, SRAM Integrated
        Circuit prediction calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = IntegratedCircuit.assessment_inputs_create(self, part,
                                                              layout,
                                                              x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 35

        # Load the number of elements combo.
        part.cmbElements.append_text("")
        part.cmbElements.append_text(_(u"Up to 16K"))
        part.cmbElements.append_text(_(u"16K to 64K"))
        part.cmbElements.append_text(_(u"64K to 256K"))
        part.cmbElements.append_text(_(u"256K to 1M"))

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.move(part.cmbTechnology, _x_pos, _y_pos[2])
        layout.move(part.cmbElements, _x_pos, _y_pos[3])
        layout.move(part.cmbPackage, _x_pos, _y_pos[4])
        layout.move(part.txtNumPins, _x_pos, _y_pos[5])
        layout.move(part.txtYears, _x_pos, _y_pos[6])

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with
        calculation input information.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = IntegratedCircuit.assessment_inputs_load(self, part)

        part.cmbElements.set_active(int(_model.get_value(_row, 24)))

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
            _hrmodel['equation'] = "lambdab * piQ * piL"

            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hazard rate inputs.
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
            Bidx = partmodel.get_value(partrow, 24)         # No of elements index
            Tidx = partmodel.get_value(partrow, 104)        # Technology index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Y = partmodel.get_value(partrow, 112)

            _hrmodel['lambdab'] = self._lambdab_count[Tidx - 1][Bidx - 1][Eidx - 1]

            # Calculate the learning factor.  We store this in the pi_r
            # field in the Program Database.
            _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

            # Calculate component active hazard rate.
            _lambdaa = _calc.calculate_part(_hrmodel)
            _lambdaa = _lambdaa * _quantity / 1000000.0

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 80, _hrmodel['piL'])

            systemmodel.set_value(systemrow, 28, _lambdaa)
            systemmodel.set_value(systemrow, 32, _lambdaa)
            systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

            return False

        def _calculate_mil_217_stress(partmodel, partrow,
                                      systemmodel, systemrow):
            """
            Performs MIL-HDBK-217F part stress hazard rate calculations for
            the Linear Integrated Circuit Class.

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
            _hrmodel['equation'] = "(C1 * piT + C2 * piE) * piQ * piL"

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
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)
            P = partmodel.get_value(partrow, 64)

            # Retrieve hazard rate inputs.
            _hrmodel['C1'] = partmodel.get_value(partrow, 8)
            K1 = partmodel.get_value(partrow, 40)
            K2 = partmodel.get_value(partrow, 41)
            K3 = partmodel.get_value(partrow, 42)
            B = partmodel.get_value(partrow, 58)
            Np = partmodel.get_value(partrow, 60)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Tbase = partmodel.get_value(partrow, 103)
            Y = partmodel.get_value(partrow, 112)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Vapplied = partmodel.get_value(partrow, 66)
            Irated = partmodel.get_value(partrow, 92)
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
            idx = int(partmodel.get_value(partrow, 67))
            if thetaJC == 0:
                thetaJC = self._thetaJC[idx - 1]
                partmodel.set_value(partrow, 109, thetaJC)
            else:
                thetaJC = partmodel.get_value(partrow, 109)

            Tj = Tcase + thetaJC * P

            # Calculate the temperature factor.  We store this in the pi_u
            # field in the Program Database.
            _hrmodel['piT'] = 0.1 * exp((-1.0 * 0.65 / 0.00008617) * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

            K5 = self._K5[idx - 1]
            K6 = self._K6[idx - 1]
            _hrmodel['C2'] = K5 * (Np ** K6)

            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

            # Calculate the learning factor.  We store this in the pi_r
            # field in the Program Database.
            _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

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
            _v_ratio = Vapplied / Vrated

            partmodel.set_value(partrow, 9, _hrmodel['C2'])
            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 35, K5)
            partmodel.set_value(partrow, 36, K6)
            partmodel.set_value(partrow, 39, Tj)
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piL'])
            partmodel.set_value(partrow, 82, _hrmodel['piT'])
            partmodel.set_value(partrow, 111, _v_ratio)

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
