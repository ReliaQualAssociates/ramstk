#!/usr/bin/env python
""" These are the optoelectronic component classes. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       optoelectronics.py is part of The RelKit Project
#
# All rights reserved.

import pango

try:
    import relkit.calculations as _calc
    import relkit.configuration as _conf
    import relkit.widgets as _widg
except ImportError:
    import calculations as _calc
    import configuration as _conf
    import widgets as _widg

from semiconductor import Semiconductor


class Detector(Semiconductor):
    """
    Photodetector Component Class.  Includes photodetectors, optoisolators,
    and photoemitters.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 6.11
    """

    _application = ["", "Photodetector", "Optoisolator", "Emitter"]
    _detector = ["", "Phototransistor", "Photodiode"]
    _isolator = ["", "Photodiode Output, Single Device",
                 "Phototransistor Output, Single Device",
                 "Photodarlington Output, Single Device",
                 "Light Sensitive Resistor, Single Device",
                 "Photodiode Output, Dual Device",
                 "Phototransistor Output, Dual Device",
                 "Photodarlington Output, Dual Device",
                 "Light Sensitive Resistor, Dual Device"]
    _emitter = ["", "Infrared Light Emitting Diode (IRLED)",
                "Light Emitting Diode (LED)"]
    _construction = ["", "With Logic Chip", "Without Logic Chip"]

    def __init__(self):
        """ Initializes the Photodetector Component Class. """

        Semiconductor.__init__(self)

        self.subcategory = 22               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._lambdab = [[0.0055, 0.0040], [0.0025, 0.013, 0.013, 0.0064,
                          0.0033, 0.017, 0.017, 0.0086], [0.0013, 0.00023]]
        self._piE = [1.0, 2.0, 8.0, 5.0, 12.0, 4.0, 6.0, 6.0, 8.0, 17.0, 0.5,
                     9.0, 24.0, 450.0]
        self._piQ = [0.7, 1.0, 2.4, 5.5, 8.0]
        self._lambdab_count = [[0.01100, 0.0290, 0.0830, 0.0590, 0.1800, 0.0840, 0.1100, 0.2100, 0.3500, 0.3400, 0.00570, 0.1500, 0.510, 3.70],
                               [0.02700, 0.0700, 0.2000, 0.1400, 0.4300, 0.2000, 0.2500, 0.4900, 0.8300, 0.8000, 0.01300, 0.3500, 1.200, 8.70],
                               [0.00047, 0.0012, 0.0035, 0.0025, 0.0077, 0.0035, 0.0044, 0.0086, 0.0150, 0.0140, 0.00024, 0.0053, 0.021, 0.15]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Type:")
        self._in_labels.append(u"Construction:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Photodetector Component Class
        prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_inputs_create(self, part, layout,
                                                       x_pos, y_pos)

        part.cmbApplication = _widg.make_combo(simple=True)
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])
        part.cmbApplication.connect("changed",
                                    self.combo_callback,
                                    part, 5)
        layout.put(part.cmbApplication, x_pos, y_pos)
        y_pos += 30

        part.cmbConstruction = _widg.make_combo(simple=True)
        part.cmbConstruction.connect("changed",
                                     self.combo_callback,
                                     part, 16)
        layout.put(part.cmbConstruction, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Photodetector Component Class calculation
        results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_results_create(self, part, layout,
                                                        x_pos, y_pos)

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

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Photodetector Component Class
        ComboBox changes.

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

        if(_index_ == 5):                   # Application
            if(idx == 1):
                for i in range(len(self._detector)):
                    part.cmbConstruction.insert_text(i, self._detector[i])

            elif(idx == 2):
                for i in range(len(self._isolator)):
                    part.cmbConstruction.insert_text(i, self._isolator[i])

            elif(idx == 3):
                for i in range(len(self._emitter)):
                    part.cmbConstruction.insert_text(i, self._emitter[i])

            part.cmbConstruction.set_active(int(part._calc_data[16]))

        elif(_index_ == 16):                # Construction
            idx2 = part._calc_data[5]
            part._calc_data[46] = self._lambdab[idx2 - 1][idx - 1]
            model.set_value(row, 46, part._calc_data[46])

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Photodetector Component Class.

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
        Aidx = partmodel.get_value(partrow, 5)          # Application
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

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
        the Photodetector Component Class.

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
        _hrmodel['equation'] = "lambdab * piT * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        P = partmodel.get_value(partrow, 64)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        _hrmodel['lambdab'] = partmodel.get_value(partrow, 46)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

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
        _hrmodel['piT'] = exp(-2790.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class Display(Semiconductor):
    """
    Alphanumeric Display Component Class.

    Hazard Rate Models:
    1. MIL-HDBK-217F, section 6.12
    """

    _application = ["", "Segment", "Diode Array"]
    _construction = ["", "With Logic Chip", "Without Logic Chip"]

    def __init__(self):
        """ Initializes the Alphanumeric Display Component Class. """

        Semiconductor.__init__(self)

        self.subcategory = 23               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._lambdaIC = [0.000043, 0.0]
        self._piE = [1.0, 2.0, 8.0, 5.0, 12.0, 4.0, 6.0, 6.0, 8.0, 17.0, 0.5,
                     9.0, 24.0, 450.0]
        self._piQ = [0.7, 1.0, 2.4, 5.5, 8.0]
        self._lambdab_count = [[0.0062, 0.016, 0.045, 0.032, 0.10, 0.046, 0.058, 0.11, 0.19, 0.18, 0.0031, 0.082, 0.28, 2.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Display Type:")
        self._in_labels.append(u"Construction:")
        self._in_labels.append(u"# of Segments:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Alphanumeric Display Component
        Class prediction calculations.

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

        part.txtNumSegments = _widg.make_entry(width=entry_width)
        part.txtNumSegments.connect("focus-out-event",
                                    self.entry_callback,
                                    part, "float", 58)
        layout.put(part.txtNumSegments, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Alphanumeric Display Component Class calculation
        results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_results_create(self, part, layout,
                                                        x_pos, y_pos)

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        Semiconductor.assessment_inputs_load(self, part)

        part.cmbApplication.set_active(int(part.model.get_value(part.selected_row, 5)))
        part.cmbConstruction.set_active(int(part.model.get_value(part.selected_row, 16)))
        part.txtNumSegments.set_text(str("{0:0.0g}".format(part.model.get_value(part.selected_row, 58))))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Alphanumeric Display Component Class.

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
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

        _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

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
        the Alphanumeric Display Component Class.

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
        _hrmodel['equation'] = "lambdab * piT * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        P = partmodel.get_value(partrow, 64)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        C = partmodel.get_value(partrow, 58)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

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

        # Base hazard rate.
        idx = partmodel.get_value(partrow, 16)
        lambdaIC = self._lambdaIC[idx -1]

        idx = model.get_value(row, 5)
        if(idx == 1):
            _hrmodel['lambdab'] = 0.00043 * float(C) + lambdaIC
        else:
            _hrmodel['lambdab'] = 0.00009 + 0.00017 * float(C) + lambdaIC

        # Temperature correction factor.  We store this in the pi_u
        # field in the Program Database.
        _hrmodel['piT'] = exp(-2790.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class LaserDiode(Semiconductor):
    """
    Laser Diode Component Class.

    Hazard Rate Models:
    1. MIL-HDBK-217F, section 6.13
    """

    _application = ["", "Continuous", "Pulsed"]
    _construction = ["", "GaAs/Al GaAs", "In GaAs/In GaAsP"]
    _quality = ["", "Hermetic Packaging", "Nonhermetic with Facet Coating",
                "Nonhermetic without Facet Coating"]

    def __init__(self):
        """ Initializes the Laser Diode Component Class. """

        Semiconductor.__init__(self)

        self.subcategory = 24               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._lambdab = [3.23, 5.65]
        self._piE = [1.0, 2.0, 8.0, 5.0, 12.0, 4.0, 6.0, 6.0, 8.0, 17.0, 0.5,
                     9.0, 24.0, 450.0]
        self._piQ = [1.0, 1.0, 3.3]
        self._lambdab_count = [[5.1, 16.0, 49.0, 32.0, 110.0, 58.0, 72.0, 100.0, 170.0, 230.0, 2.6, 87.0, 350.0, 2000.0],
                               [8.9, 28.0, 85.0, 55.0, 190.0, 100.0, 130.0, 180.0, 300.0, 400.0, 4.5, 150.0, 600.0, 3500.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Application:")
        self._in_labels.append(u"Duty Cycle:")
        self._in_labels.append(u"Technology:")
        self._in_labels.append(u"Peak Fwd Current(I<sub>Fpk</sub>):")
        self._in_labels.append(u"Rated Optical Pwr(P<sub>Rated</sub>):")
        self._in_labels.append(u"Required Optical Pwr(P<sub>Rqd</sub>):")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>C</sub>\u03C0<sub>I</sub>\u03C0<sub>A</sub>\u03C0<sub>P</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>I</sub>:")
        self._out_labels.append(u"\u03C0<sub>A</sub>:")
        self._out_labels.append(u"\u03C0<sub>P</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Laser Diode Component Class
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

        part.txtDutyCycle = _widg.make_entry(width=entry_width)
        layout.put(part.txtDutyCycle, x_pos, y_pos)
        y_pos += 30
        part.txtDutyCycle.connect("focus-out-event",
                                  self.entry_callback,
                                  part, "float", 19)

        part.cmbConstruction = _widg.make_combo(simple=True)
        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])
        part.cmbConstruction.connect("changed",
                                     self.combo_callback,
                                     part, 16)
        layout.put(part.cmbConstruction, x_pos, y_pos)
        y_pos += 30

        part.txtFwdCurrent = _widg.make_entry(width=entry_width)
        part.txtFwdCurrent.connect("focus-out-event",
                                   self.entry_callback,
                                   part, "float", 62)
        layout.put(part.txtFwdCurrent, x_pos, y_pos)
        y_pos += 30

        # Create the rated optical power entry.  We store these results
        # in the operating_freq field in the program database.
        part.txtRatedOptPwr = _widg.make_entry(width=entry_width)
        part.txtRatedOptPwr.connect("focus-out-event",
                                    self.entry_callback,
                                    part, "float", 63)
        layout.put(part.txtRatedOptPwr, x_pos, y_pos)
        y_pos += 30

        # Create the required optical power entry.
        part.txtRqdOptPwr = _widg.make_entry(width=entry_width)
        part.txtRqdOptPwr.connect("focus-out-event",
                                  self.entry_callback,
                                  part, "float", 93)
        layout.put(part.txtRqdOptPwr, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Laser Diode Component Class calculation
        results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_results_create(self, part, layout,
                                                        x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.txtPiI = _widg.make_entry(width=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiI, x_pos, y_pos)
        y_pos += 30

        part.txtPiA = _widg.make_entry(width=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiA, x_pos, y_pos)
        y_pos += 30

        part.txtPiP = _widg.make_entry(width=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiP, x_pos, y_pos)

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
        part.txtDutyCycle.set_text(str(fmt.format(part.model.get_value(part.selected_row, 19))))
        part.txtFwdCurrent.set_text(str(fmt.format(part.model.get_value(part.selected_row, 62))))
        part.txtRatedOptPwr.set_text(str(fmt.format(part.model.get_value(part.selected_row, 63))))
        part.txtRqdOptPwr.set_text(str(fmt.format(part.model.get_value(part.selected_row, 93))))

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
        part.txtPiI.set_text(str(fmt.format(part.model.get_value(part.selected_row, 75))))
        part.txtPiP.set_text(str(fmt.format(part.model.get_value(part.selected_row, 78))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Laser Diode Component Class
        ComboBox changes.

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

        if(_index_ == 5):                       # Duty cycle
            if(idx == 2):
                part.txtDutyCycle.show()
            else:
                part.txtDutyCycle.hide()

        elif(_index_ == 16):                    # Construction
            part._calc_data[46] = self._lambdab[idx - 1]
            model.set_value(row, 46, part._calc_data[46])

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Laser Diode Component Class.

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
        Cidx = partmodel.get_value(partrow, 16)         # Construction index
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

        _hrmodel['lambdab'] = self._lambdab_count[Cidx - 1][Eidx - 1]

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
        the Laser Diode Component Class.

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
        _hrmodel['equation'] = "lambdab * piT * piI * piA * piP * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        P = partmodel.get_value(partrow, 64)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        DC = partmodel.get_value(partrow, 19)
        _hrmodel['lambdab'] = partmodel.get_value(partrow, 46)
        IF = partmodel.get_value(partrow, 62)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Prated = partmodel.get_value(partrow, 63)
        Prqd = partmodel.get_value(partrow, 93)

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
        _hrmodel['piT'] = exp(-4635.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

        # Forward current correction factor.
        _hrmodel['piI'] = IF**0.68

        # Application correction factor.
        if(partmodel.get_value(partrow, 5) == 1):
            _hrmodel['piA'] = 4.4
        else:
            _hrmodel['piA'] = DC**0.5

        # Power degradation correction factor.
        _hrmodel['piP'] = 1.0 / (2.0 * (1 - (Prqd / Prated)))

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 68, _hrmodel['piA'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 75, _hrmodel['piI'])
        partmodel.set_value(partrow, 78, _hrmodel['piP'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
