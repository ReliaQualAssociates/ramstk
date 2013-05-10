#!/usr/bin/env python
""" These are the memory integrated circuit classes. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       memory.py is part of The RelKit Project
#
# All rights reserved.

try:
    import relkit.calculations as _calc
    import relkit.widgets as _widg
except ImportError:
    import calculations as _calc
    import widgets as _widg

from ic import IntegratedCircuit


class MemoryDRAM(IntegratedCircuit):
    """
    DRAM memory class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 5.2
    """

    def __init__(self):
        """ Initializes the Memory, DRAM Integrated Circuit Component Class.
        """

        IntegratedCircuit.__init__(self)

        self.subcategory = 7                    # Subcategory ID in relkitcom database.

        self._B = [16384, 65536, 262144, 1024000]

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._C1 = [[0.0, 0.0, 0.0, 0.0],
                    [0.0013, 0.0025, 0.005, 0.01]]

        self._lambdab_count = [[0.0040, 0.014, 0.027, 0.027, 0.040, 0.029, 0.035, 0.040, 0.059, 0.055, 0.0040, 0.034, 0.080, 1.4],
                               [0.0055, 0.019, 0.039, 0.034, 0.051, 0.039, 0.047, 0.056, 0.079, 0.070, 0.0055, 0.043, 0.100, 1.7],
                               [0.0074, 0.023, 0.043, 0.040, 0.060, 0.049, 0.058, 0.076, 0.100, 0.084, 0.0074, 0.051, 0.120, 1.9],
                               [0.0110, 0.032, 0.057, 0.053, 0.077, 0.070, 0.080, 0.120, 0.150, 0.110, 0.0110, 0.067, 0.150, 2.3]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[2] = "# of Bits:"
        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Memory, DRAM Integrated
        Circuit prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = IntegratedCircuit.assessment_inputs_create(self, part, layout,
                                                           x_pos, y_pos)

        # Load the number of elements combo.
        part.cmbElements.append_text("")
        part.cmbElements.append_text("Up to 16K")
        part.cmbElements.append_text("16K to 64K")
        part.cmbElements.append_text("64K to 256K")
        part.cmbElements.append_text("256K to 1M")

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Memory, DRAM Integrated Circuit calculation
        results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = IntegratedCircuit.assessment_results_create(self, part, layout,
                                                            x_pos, y_pos)

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        IntegratedCircuit.assessment_inputs_load(self, part)

        part.cmbElements.set_active(int(part.model.get_value(part.selected_row, 24)))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Memory, DRAM Integrated Circuit Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ * piL"

        # Retrieve hazard rate inputs.
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
        Bidx = partmodel.get_value(partrow, 24)         # No of elements index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Y = partmodel.get_value(partrow, 112)

        _hrmodel['lambdab'] = self._lambdab_count[Bidx - 1][Eidx - 1]

        # Calculate the learning factor.  We store this in the pi_r
        # field in the Program Database.
        _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 80, _hrmodel['piL'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the Memory, DRAM Integrated Circuit Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "(C1 * piT + C2 * piE) * piQ * piL"

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

        # Calculate junction temperature.  If ambient temperature and
        # temperature rise are not set (i.e., equal to zero), use the
        # default case temperature values that are based on the active
        # environment.  Otherwise calculate case temperature.
        if(Tamb == 0 and Trise == 0):
            idx = int(systemmodel.get_value(systemrow, 22))
            Tcase = self._Tcase[idx - 1]
        else:
            Tcase = Tamb + Trise

        # Determine the junction-case thermal resistance.  If thetaJC is
        # not set (i.e., equal to zero), use the default value which is
        # based on the package type.
        idx = int(partmodel.get_value(partrow, 67))
        if(thetaJC == 0):
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

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 9, _hrmodel['C2'])
        partmodel.set_value(partrow, 35, K5)
        partmodel.set_value(partrow, 36, K6)
        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piL'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

class MemoryEEPROM(IntegratedCircuit):
    """
    EEPROM memory class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 5.2
    """

    # For programming cycles combobox item list.
    _cycles = ["", "Up to 100", "100 to 200", "200 to 500", "500 to 1K",
               "1k to 3K", "3K to 7K", "7K to 15K", "15K to 20K", "20K to 30K",
               "30K to 100K", "100K to 200K", "200K to 300K", "300K to 400K",
               "400K to 500K"]

    # For error correction code combobox item list.
    _ecc = ["", "No ECC", "Hamming Code", "Two Needs One Redundant Cell"]

    # For manufacturing type combobox item list.
    _man = ["", "FLOTOX", "Textured-Poly"]

    def __init__(self):
        """
        Initializes the Memory, EEPROM Integrated Circuit Component
        Class.
        """

        IntegratedCircuit.__init__(self)

        self.subcategory = 6                    # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._A1 = [[0.0007, 0.0014, 0.0034, 0.0068, 0.02, 0.049, 0.1, 0.14,
                     0.2, 0.68, 1.3, 2.7, 2.7, 3.4], [0.0097, 0.014, 0.023,
                     0.033, 0.061, 0.14, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,
                     0.3]]
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

        self._lambdab_count = [[[0.010, 0.028, 0.050, 0.046, 0.067, 0.082, 0.070, 0.10, 0.13, 0.096, 0.010, 0.058, 0.13, 1.9],
                                [0.017, 0.043, 0.071, 0.063, 0.091, 0.095, 0.110, 0.18, 0.21, 0.140, 0.017, 0.081, 0.18, 2.3],
                                [0.028, 0.065, 0.100, 0.085, 0.120, 0.150, 0.160, 0.30, 0.33, 0.190, 0.028, 0.110, 0.23, 2.3],
                                [0.053, 0.120, 0.180, 0.150, 0.210, 0.270, 0.290, 0.56, 0.61, 0.330, 0.053, 0.190, 0.39, 3.4]],
                               [[0.0049, 0.018, 0.036, 0.036, 0.053, 0.037, 0.046, 0.049, 0.075, 0.072, 0.0048, 0.045, 0.11, 1.9],
                                [0.0061, 0.022, 0.044, 0.043, 0.064, 0.046, 0.056, 0.062, 0.093, 0.087, 0.0062, 0.054, 0.13, 2.3],
                                [0.0072, 0.024, 0.048, 0.045, 0.067, 0.051, 0.061, 0.073, 0.100, 0.092, 0.0072, 0.057, 0.13, 2.3],
                                [0.0120, 0.038, 0.071, 0.068, 0.100, 0.080, 0.095, 0.120, 0.180, 0.140, 0.0120, 0.086, 0.20, 3.3]]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[2] = "# of Bits:"
        self._in_labels.append("# Prog Cycles:")
        self._in_labels.append("Error Correct Code:")
        self._in_labels.append("Man Method:")
        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub> + \u03BB<sub>CYC</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"
        self._out_labels.insert(9, u"\u03BB<sub>CYC</sub>:")
        self._out_labels.append(u"\u03C0<sub>ECC</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Memory, EEPROM Integrated
        Circuit prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = IntegratedCircuit.assessment_inputs_create(self, part, layout,
                                                           x_pos, y_pos)

        # Load the number of elements combo.
        part.cmbElements.append_text("")
        part.cmbElements.append_text("Up to 16K")
        part.cmbElements.append_text("16K to 64K")
        part.cmbElements.append_text("64K to 256K")
        part.cmbElements.append_text("256K to 1M")

        # Create the Number of Programming Cycles combobox.
        part.cmbCycles = _widg.make_combo(simple=True)
        for i in range(len(self._cycles)):
            part.cmbCycles.insert_text(i, self._cycles[i])
        part.cmbCycles.connect("changed",
                               self.combo_callback,
                               part, 18)
        layout.put(part.cmbCycles, x_pos, y_pos)
        y_pos += 30

        # Create the Error Correction Code combobox.
        part.cmbECC = _widg.make_combo(simple=True)
        for i in range(len(self._ecc)):
            part.cmbECC.insert_text(i, self._ecc[i])
        part.cmbECC.connect("changed",
                            self.combo_callback,
                            part, 23)
        layout.put(part.cmbECC, x_pos, y_pos)
        y_pos += 30

        # Create the Manufacturing Method combobox.
        part.cmbManufacturing = _widg.make_combo(simple=True)
        for i in range(len(self._man)):
            part.cmbManufacturing.insert_text(i, self._man[i])
        part.cmbManufacturing.connect("changed",
                                      self.combo_callback,
                                      part, 54)
        layout.put(part.cmbManufacturing, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Memory, EEPROM Integrated Circuit calculation
        results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = IntegratedCircuit.assessment_results_create(self, part, layout,
                                                            x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.txtPiECC = _widg.make_entry(_width_=entry_width,
                                         editable=False, bold=True)
        layout.put(part.txtPiECC, x_pos, y_pos)
        y_pos += 30

        part.txtlambdaCYC = _widg.make_entry(_width_=entry_width,
                                             editable=False, bold=True)
        layout.put(part.txtlambdaCYC, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        IntegratedCircuit.assessment_inputs_load(self, part)

        part.cmbCycles.set_active(int(part.model.get_value(part.selected_row, 18)))
        part.cmbECC.set_active(int(part.model.get_value(part.selected_row, 23)))
        part.cmbElements.set_active(int(part.model.get_value(part.selected_row, 24)))
        part.cmbManufacturing.set_active(int(part.model.get_value(part.selected_row, 54)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        IntegratedCircuit.assessment_results_load(self, part)

        part.txtlambdaCYC.set_text(str(fmt.format(part.model.get_value(part.selected_row, 52))))
        part.txtPiECC.set_text(str(fmt.format(part.model.get_value(part.selected_row, 73))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling ComboBox changes specific to the
        Memory, EEPROM Integrated Circuit Component Class.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        IntegratedCircuit.combo_callback(self, combo, part, _index_)

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        if(_index_ == 18):                      # Programming Cycles
            idx2 = part.cmbManufacturing.get_active()

            model.set_value(row, 3, self._A1[idx2 - 1][idx - 1])
            model.set_value(row, 4, self._A2[idx2 - 1][idx - 1])

        elif(_index_ == 23):                    # Error Correction Code
            model.set_value(row, 73, self._piECC[idx - 1])

        elif(_index_ == 24):                    # Number of elements
            model.set_value(row, 58, self._B[idx - 1])

        elif(_index_ == 54):                    # Manufacturing process
            model.set_value(row, 40, self._K1[idx - 1])
            model.set_value(row, 41, self._K2[idx - 1])
            model.set_value(row, 42, self._K3[idx - 1])
            model.set_value(row, 103, self._Tbase[idx - 1])

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Memory, EEPROM Integrated Circuit Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ * piL"

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

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 80, _hrmodel['piL'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the Memory, EEPROM Integrated Circuit Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "(C1 * piT + C2 * piE + lambdaCYC) * piQ * piL"

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

        # Calculate junction temperature.  If ambient temperature and
        # temperature rise are not set (i.e., equal to zero), use the
        # default case temperature values that are based on the active
        # environment.  Otherwise calculate case temperature.
        if(Tamb == 0 and Trise == 0):
            idx = int(systemmodel.get_value(systemrow, 22))
            Tcase = self._Tcase[idx - 1]
        else:
            Tcase = Tamb + Trise

        # Determine the junction-case thermal resistance.  If thetaJC is
        # not set (i.e., equal to zero), use the default value which is
        # based on the package type.
        if(thetaJC == 0):
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

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 9, _hrmodel['C2'])
        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 52, _hrmodel['lambdaCYC'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 73, _hrmodel['piECC'])
        partmodel.set_value(partrow, 80, _hrmodel['piL'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

class MemoryROM(IntegratedCircuit):
    """
    ROM Memory class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 5.2
    """

    def __init__(self):
        """ Initializes the Memory, ROM Integrated Circuit Component Class. """

        IntegratedCircuit.__init__(self)

        self.subcategory = 5        # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._B = [16384, 65536, 262144, 1024000]
        self._C1 = [[0.0094, 0.019, 0.038, 0.075],
                    [0.00085, 0.0017, 0.0034, 0.0068]]

        self._lambdab_count = [[[0.010, 0.028, 0.050, 0.046, 0.067, 0.062, 0.070, 0.10, 0.13, 0.096, 0.010, 0.058, 0.13, 1.9],
                                [0.017, 0.043, 0.071, 0.063, 0.091, 0.095, 0.110, 0.18, 0.21, 0.140, 0.017, 0.081, 0.18, 2.3],
                                [0.028, 0.065, 0.100, 0.085, 0.120, 0.150, 0.180, 0.30, 0.33, 0.190, 0.028, 0.110, 0.23, 2.3],
                                [0.053, 0.120, 0.180, 0.150, 0.210, 0.270, 0.290, 0.56, 0.61, 0.330, 0.053, 0.190, 0.39, 3.4]],
                               [[0.0047, 0.018, 0.036, 0.035, 0.053, 0.037, 0.045, 0.048, 0.074, 0.071, 0.0047, 0.044, 0.11, 1.9],
                                [0.0059, 0.022, 0.043, 0.042, 0.063, 0.045, 0.055, 0.060, 0.090, 0.086, 0.0059, 0.053, 0.13, 2.3],
                                [0.0067, 0.023, 0.045, 0.044, 0.066, 0.048, 0.059, 0.068, 0.099, 0.089, 0.0067, 0.055, 0.13, 2.3],
                                [0.0110, 0.036, 0.068, 0.066, 0.098, 0.075, 0.090, 0.110, 0.150, 0.140, 0.0110, 0.083, 0.20, 3.3]]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[2] = "# of Bits:"
        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Memory, ROM Integrated Circuit
        prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = IntegratedCircuit.assessment_inputs_create(self, part, layout,
                                                           x_pos, y_pos)

        # Load the number of elements combo.
        part.cmbElements.append_text("")
        part.cmbElements.append_text("Up to 16K")
        part.cmbElements.append_text("16K to 64K")
        part.cmbElements.append_text("64K to 256K")
        part.cmbElements.append_text("256K to 1M")

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Memory, ROM Integrated Circuit calculation
        results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = IntegratedCircuit.assessment_results_create(self, part, layout,
                                                            x_pos, y_pos)

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        IntegratedCircuit.assessment_inputs_load(self, part)

        part.cmbElements.set_active(int(part.model.get_value(part.selected_row, 24)))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Memory, ROM Integrated Circuit Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ * piL"

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

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 80, _hrmodel['piL'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the Memory, ROM Integrated Circuit Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "(C1 * piT + C2 * piE) * piQ * piL"

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

        # Calculate junction temperature.  If ambient temperature and
        # temperature rise are not set (i.e., equal to zero), use the
        # default case temperature values that are based on the active
        # environment.  Otherwise calculate case temperature.
        if(Tamb == 0 and Trise == 0):
            idx = int(systemmodel.get_value(systemrow, 22))
            Tcase = self._Tcase[idx - 1]
        else:
            Tcase = Tamb + Trise

        # Determine the junction-case thermal resistance.  If thetaJC is
        # not set (i.e., equal to zero), use the default value which is
        # based on the package type.
        if(thetaJC == 0):
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

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 9, _hrmodel['C2'])
        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piL'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

class MemorySRAM(IntegratedCircuit):
    """
    SRAM memory class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 5.2
    """

    def __init__(self):
        """
        Initializes the Memory, SRAM Integrated Circuit Component Class.
        """

        IntegratedCircuit.__init__(self)

        self.subcategory = 8                    # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._B = [16384, 65536, 262144, 1024000]
        self._C1 = [[0.0062, 0.011, 0.021, 0.042],
                    [0.0062, 0.011, 0.021, 0.042]]

        self._lambdab_count = [[[0.0075, 0.023, 0.043, 0.041, 0.060, 0.050, 0.058, 0.077, 0.10, 0.084, 0.0075, 0.052, 0.12, 1.9],
                                [0.0120, 0.033, 0.058, 0.054, 0.079, 0.072, 0.083, 0.120, 0.15, 0.110, 0.0120, 0.069, 0.15, 2.3],
                                [0.0180, 0.045, 0.074, 0.065, 0.095, 0.100, 0.110, 0.190, 0.22, 0.140, 0.0180, 0.084, 0.18, 2.3],
                                [0.0330, 0.079, 0.130, 0.110, 0.160, 0.180, 0.200, 0.350, 0.39, 0.240, 0.0330, 0.140, 0.30, 3.4]],
                               [[0.0079, 0.022, 0.038, 0.034, 0.050, 0.048, 0.054, 0.083, 0.10, 0.073, 0.0079, 0.044, 0.098, 1.4],
                                [0.0140, 0.034, 0.057, 0.050, 0.073, 0.077, 0.085, 0.140, 0.17, 0.110, 0.0140, 0.065, 0.140, 1.8],
                                [0.0230, 0.053, 0.084, 0.071, 0.100, 0.120, 0.130, 0.250, 0.27, 0.160, 0.0230, 0.092, 0.190, 1.9],
                                [0.0430, 0.092, 0.140, 0.110, 0.160, 0.220, 0.230, 0.460, 0.49, 0.260, 0.0430, 0.150, 0.300, 2.3]]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[2] = "# of Bits:"
        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Memory, SRAM Integrated
        Circuit prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = IntegratedCircuit.assessment_inputs_create(self, part, layout,
                                                           x_pos, y_pos)

        # Load the number of elements combo.
        part.cmbElements.append_text("")
        part.cmbElements.append_text("Up to 16K")
        part.cmbElements.append_text("16K to 64K")
        part.cmbElements.append_text("64K to 256K")
        part.cmbElements.append_text("256K to 1M")

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Memory, SRAM Integrated Circuit calculation
        results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = IntegratedCircuit.assessment_results_create(self, part, layout,
                                                            x_pos, y_pos)

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        IntegratedCircuit.assessment_inputs_load(self, part)

        part.cmbElements.set_active(int(part.model.get_value(part.selected_row, 24)))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Memory, SRAM Integrated Circuit Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ * piL"

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

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 80, _hrmodel['piL'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the Memory, SRAM Integrated Circuit Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "(C1 * piT + C2 * piE) * piQ * piL"

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

        # Calculate junction temperature.  If ambient temperature and
        # temperature rise are not set (i.e., equal to zero), use the
        # default case temperature values that are based on the active
        # environment.  Otherwise calculate case temperature.
        if(Tamb == 0 and Trise == 0):
            idx = int(systemmodel.get_value(systemrow, 22))
            Tcase = self._Tcase[idx - 1]
        else:
            Tcase = Tamb + Trise

        # Determine the junction-case thermal resistance.  If thetaJC is
        # not set (i.e., equal to zero), use the default value which is
        # based on the package type.
        idx = int(partmodel.get_value(partrow, 67))
        if(thetaJC == 0):
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

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 9, _hrmodel['C2'])
        partmodel.set_value(partrow, 35, K5)
        partmodel.set_value(partrow, 36, K6)
        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piL'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
