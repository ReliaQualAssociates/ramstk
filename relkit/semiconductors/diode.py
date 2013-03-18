#!/usr/bin/env python
""" These are the diode component classes. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       diode.py is part of The RelKit Project
#
# All rights reserved.

import pango

try:
    import reliafree.calculations as _calc
    import reliafree.widgets as _widg
except ImportError:
    import calculations as _calc
    import widgets as _widg

from semiconductor import Semiconductor


class LowFrequency(Semiconductor):
    """
    Low Frequency Diode Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 6.1
    """

    _application = ["", "General Purpose Analog", "Switching", "Power Rectifier, Fast Recovery",
                    "Power Rectifier, Schottky", "Power Rectifier, Stacked", "Transient Suppressor",
                    "Current Regulator", "Voltage Regulator/Reference"]

    _construction = ["", "Metallurgically Bonded", "Spring Loaded"]

    def __init__(self):
        """ Initializes the Low Frequency Diode Component Class. """

        Semiconductor.__init__(self)

        self.subcategory = 12               # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._I4 = [3091, 3091, 3091, 3091, 3091, 3091, 1925, 1925]
        self._lambdab = [0.0038, 0.0010, 0.069, 0.003, 0.005, 0.0013, 0.0034, 0.002]
        self._piC = [1.0, 2.0]
        self._piE = [1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0, 0.5, 14.0, 32.0, 320.0]
        self._piQ = [0.7, 1.0, 2.4, 5.5, 8.0]
        self._lambdab_count = [[0.00360, 0.0280, 0.049, 0.043, 0.100, 0.092, 0.210, 0.200, 0.44, 0.170, 0.00180, 0.076, 0.23, 1.50],
                               [0.00094, 0.0075, 0.013, 0.011, 0.027, 0.024, 0.054, 0.054, 0.12, 0.045, 0.00047, 0.020, 0.06, 0.40],
                               [0.06500, 0.5200, 0.890, 0.780, 1.900, 1.700, 3.700, 3.700, 8.00, 3.100, 0.03200, 1.400, 4.10, 28.0],
                               [0.00280, 0.0220, 0.039, 0.034, 0.062, 0.073, 0.160, 0.160, 0.35, 0.130, 0.00140, 0.060, 0.18, 1.20],
                               [0.00290, 0.0230, 0.040, 0.035, 0.084, 0.075, 0.170, 0.170, 0.36, 0.140, 0.00150, 0.062, 0.18, 1.20],
                               [0.00330, 0.0240, 0.039, 0.035, 0.082, 0.066, 0.150, 0.130, 0.27, 0.120, 0.00160, 0.060, 0.16, 1.30],
                               [0.00560, 0.0400, 0.066, 0.060, 0.140, 0.110, 0.250, 0.220, 0.460, 0.21, 0.00280, 0.100, 0.28, 2.10]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Application:")
        self._in_labels.append(u"Contact Construction:")
        self._in_labels.append(u"Applied Voltage (V<sub>Applied</sub>):")
        self._in_labels.append(u"Rated Voltage (V<sub>Rated</sub>):")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>S</sub>\u03C0<sub>C</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>S</sub>:")
        self._out_labels.append(u"\u03C0<sub>C</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Low Frequency Diode
        prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_inputs_create(self, part, layout,
                                                       x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        # Create and populate the application combobox.
        part.cmbApplication = _widg.make_combo(simple=True)
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])
        part.cmbApplication.connect("changed",
                                    self.combo_callback,
                                    part, 5)
        layout.put(part.cmbApplication, x_pos, y_pos)
        y_pos += 30

        # Create and populate the construction combobox.
        part.cmbConstruction = _widg.make_combo(simple=True)
        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])
        part.cmbConstruction.connect("changed",
                                     self.combo_callback,
                                     part, 16)
        layout.put(part.cmbConstruction, x_pos, y_pos)
        y_pos += 30

        # Create the applied voltage entry.
        part.txtVApplied = _widg.make_entry(_width_=entry_width)
        part.txtVApplied.connect("focus-out-event",
                                 self.entry_callback,
                                 part, "float", 66)
        layout.put(part.txtVApplied, x_pos, y_pos)
        y_pos += 30

        # Create the rated voltage entry.
        part.txtVRated = _widg.make_entry(_width_=entry_width)
        part.txtVRated.connect("focus-out-event",
                               self.entry_callback,
                               part, "float", 94)
        layout.put(part.txtVRated, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Low Frequency Diode calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_results_create(self, part, layout,
                                                        x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.txtPiS = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiS, x_pos, y_pos)
        y_pos += 30

        part.txtPiC = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiC, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Semiconductor.assessment_inputs_load(self, part)

        part.cmbApplication.set_active(int(part.model.get_value(part.selected_row, 5)))
        part.cmbConstruction.set_active(int(part.model.get_value(part.selected_row, 16)))
        part.txtVApplied.set_text(str(fmt.format(part.model.get_value(part.selected_row, 66))))
        part.txtVRated.set_text(str(fmt.format(part.model.get_value(part.selected_row, 94))))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Semiconductor.assessment_results_load(self, part)

        part.txtPiC.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 69))))
        part.txtPiS.set_text(str(fmt.format(part.model.get_value(part.selected_row, 81))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Low Frequency Diode Semicondutor
        Class ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        Semiconductor.combo_callback(self, combo, part, _index_)

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        if(_index_ == 5):                       # Application
            part._calc_data[34] = self._I4[idx - 1]
            part._calc_data[46] = self._lambdab[idx - 1]
            model.set_value(row, 34, part._calc_data[34])
            model.set_value(row, 46, part._calc_data[46])

        elif(_index_ == 16):                    # Construction
            part._calc_data[69] = self._piC[idx - 1]
            model.set_value(row, 69, part._calc_data[69])

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Low Frequency Diode Class.

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
        _hrmodel['equation'] = "lambdab * piQ"

        # Retrieve hazard rate inputs.
        Aidx = partmodel.get_value(partrow, 5)          # Application index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

        _hrmodel['lambdab'] = self._lambdab_count[Aidx - 1][Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the Low Frequency Diode Component Class.

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
        _hrmodel['equation'] = "lambdab * piT * piS * piC * piQ * piE"

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

        # Junction temperature.
        Tj = Tcase + thetaJC * P

        # Temperature correction factor.  We store this in the pi_u
        # field in the Program Database.
        _hrmodel['piT'] = exp(-I4 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

        # Voltage stress correction factor.  We store this in the pi_sr
        # field in the Program Database.
        if(model.get_value(row, 5) < 7):
            Vs = VApplied / VRated
            if(Vs > 0.3 and Vs < 1.0):
                _hrmodel['piS'] = Vs**2.43
            else:
                _hrmodel['piS'] = 0.54
        else:
            _hrmodel['piS'] = 1.0

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 81, _hrmodel['piS'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

class HighFrequency(Semiconductor):
    """
    High Frequency Diode Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 6.2
    """

    _application = ["", "Varactor, Voltage Control", "Varactor, Multiplier", "All Others"]

    _construction = ["", "Si IMPATT", "Gunn/Bulk Effect", "Tunnel and Back",
                     "PIN", "Schottky Barrier", "Varactor"]

    def __init__(self):
        """ Initializes the High Frequency Diode Component Class. """

        Semiconductor.__init__(self)

        self.subcategory = 13               # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._I4 = [5260, 2100, 2100, 2100, 2100, 2100]
        self._lambdab = [0.22, 0.18, 0.0023, 0.0081, 0.027, 0.0025]
        self._piA = [0.5, 2.5, 1.0]
        self._piE = [1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5, 9.0, 24.0, 250.0]
        self._piQ = [0.5, 1.0, 5.0, 25, 50]
        self._piQS = [0.5, 1.0, 1.8, 2.5, 1.0]
        self._lambdab_count = [[0.86, 2.80, 8.9, 5.6, 20.0, 11.0, 14.0, 36.0, 62.0, 44.0, 0.43, 16.0, 67.0, 350.0],
                               [0.31, 0.76, 2.1, 1.5, 4.60, 2.00, 2.50, 4.50, 7.60, 7.90, 0.16, 3.70, 12.0, 94.00],
                               [0.004, 0.0096, 0.0026, 0.0019, 0.058, 0.025, 0.032, 0.057, 0.097, 0.10, 0.002, 0.048, 0.15, 1.2],
                               [0.028, 0.068, 0.19, 0.14, 0.41, 0.18, 0.22, 0.40, 0.69, 0.71, 0.014, 0.34, 1.1, 8.5],
                               [0.047, 0.11, 0.31, 0.23, 0.68, 0.3, 0.37, 0.67, 1.1, 1.2, 0.023, 0.56, 1.8, 14.0],
                               [0.0043, 0.010, 0.029, 0.021, 0.063, 0.028, 0.034, 0.062, 0.11, 0.11, 0.0022, 0.052, 0.17, 1.3]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Application:")
        self._in_labels.append(u"Diode Type:")
        self._in_labels.append(u"Rated Power (P<sub>Rated</sub>):")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>A</sub>:")
        self._out_labels.append(u"\u03C0<sub>R</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for High Frequency Diode
        prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_inputs_create(self, part, layout,
                                                       x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.cmbApplication = _widg.make_combo(simple=True)
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])
        part.cmbApplication.connect("changed",
                                    self.combo_callback,
                                    part, 5)
        layout.put(part.cmbApplication, x_pos, y_pos)
        y_pos += 30

        part.cmbConstruction = _widg.make_combo(simple=True)
        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])
        part.cmbConstruction.connect("changed",
                                     self.combo_callback,
                                     part, 16)
        layout.put(part.cmbConstruction, x_pos, y_pos)
        y_pos += 30

        part.txtPwrRated = _widg.make_entry(_width_=entry_width)
        part.txtPwrRated.connect("focus-out-event",
                                 self.entry_callback,
                                 part, "float", 93)
        layout.put(part.txtPwrRated, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display High Frequency Diode calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_results_create(self, part, layout,
                                                        x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.txtPiA = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiA, x_pos, y_pos)
        y_pos += 30

        part.txtPiR = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiR, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Semiconductor.assessment_inputs_load(self, part)

        part.cmbApplication.set_active(int(part.model.get_value(part.selected_row, 5)))
        part.cmbConstruction.set_active(int(part.model.get_value(part.selected_row, 16)))
        part.txtPwrRated.set_text(str(fmt.format(part.model.get_value(part.selected_row, 93))))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Semiconductor.assessment_results_load(self, part)

        part.txtPiA.set_text(str(fmt.format(part.model.get_value(part.selected_row, 68))))
        part.txtPiR.set_text(str(fmt.format(part.model.get_value(part.selected_row, 80))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling High Frequency Diode Semicondutor
        Class ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        Semiconductor.combo_callback(self, combo, part, _index_)

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        if(_index_ == 5):               # Application
            part._calc_data[68] = self._piA[idx - 1]
            model.set_value(row, 68, part._calc_data[68])

        elif(_index_ == 16):            # Construction
            part._calc_data[34] = self._I4[idx - 1]
            part._calc_data[46] = self._lambdab[idx - 1]
            model.set_value(row, 34, part._calc_data[34])
            model.set_value(row, 46, part._calc_data[46])

        elif(_index_ == 85 and part._calc_data[16] == 5):   # Quality for Schottky diode.
            part._calc_data[79] = self._piQS[idx - 1]
            model.set_value(row, 79, part._calc_data[79])

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        High Frequency Diode Component Class.

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
        _hrmodel['equation'] = "lambdab * piQ"

        # Retrieve hazard rate inputs.
        Aidx = partmodel.get_value(partrow, 5)          # Application index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

        _hrmodel['lambdab'] = self._lambdab_count[Aidx - 1][Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the High Frequency Diode Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp, log

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piT * piA * piR * piQ * piE"

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

        Tj = Tcase + thetaJC * P

        # Temperature correction factor.  We store this in the pi_u
        # field in the Program Database.
        _hrmodel['piT'] = exp(-I4 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

        # Power rating correction factor.
        if(model.get_value(row, 16) == 4):
            _hrmodel['piR'] = 0.326 * log(Prated) - 0.25
        else:
            _hrmodel['piR'] = 1.0

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piR'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
