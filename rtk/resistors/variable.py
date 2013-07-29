#!/usr/bin/env python
""" These are the variable resistor component classes. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       variable.py is part of The RelKit Project
#
# All rights reserved.

try:
    import relkit.calculations as _calc
    import relkit.widgets as _widg
except ImportError:
    import calculations as _calc
    import widgets as _widg

from resistor import Resistor


class VarWirewound(Resistor):
    """
    Variable Value Wirewound Resistor Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 9.9
    """

    _quality = ["", "S", "R", "P", "M", "MIL-R-27208", "Lower"]
    _range = ["", "10 to 2.0K", "2.0K to 5.0K", "5.0K to 20.0K"]
    _specification = ["", "MIL-R-39015 (RTR)", "MIL-R-27208 (RE)"]
    _specsheet = [["", "RTR12", "RTR22", "RTR24"], ["", "RT12", "RT22", "RT26",
                   "RT27"]]

    def __init__(self):
        """
        Initializes the Variable Value Wirewound Resistor Component Class.
        """

        Resistor.__init__(self)

        self.subcategory = 33               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piR = [1.0, 1.4, 2.0]
        self._piE = [1.0, 2.0, 12.0, 6.0, 20.0, 5.0, 8.0, 9.0, 15.0, 33.0, 0.5,
                     18.0, 48.0, 870.0]
        self._piQ = [0.02, 0.06, 0.2, 0.6, 3.0, 10.0]
        self._lambdab_count = [0.025, 0.055, 0.35, 0.15, 0.58, 0.16, 0.26, 0.35, 0.58, 1.1, 0.013, 0.52, 1.6, 24.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Nominal Resistance (\u03A9):")
        self._in_labels.append(u"Specification:")
        self._in_labels.append(u"Spec Sheet:")
        self._in_labels.append(u"Number of Taps:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>TAPS</sub>")
        self._out_labels.append(u"\u03C0<sub>V</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Variable Value Wirewound
        Resistor Component Class prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Resistor.assessment_inputs_create(self, part, layout,
                                                  x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.txtResistance = _widg.make_entry(_width_=entry_width)
        part.txtResistance.connect("focus-out-event",
                                   self.entry_callback,
                                   part, "float", 95)
        layout.put(part.txtResistance, x_pos, y_pos)
        y_pos += 30

        part.cmbSpecification = _widg.make_combo(simple=True)
        for i in range(len(self._specification)):
            part.cmbSpecification.insert_text(i, self._specification[i])
        part.cmbSpecification.connect("changed",
                                     self.combo_callback,
                                     part, 101)
        layout.put(part.cmbSpecification, x_pos, y_pos)
        y_pos += 30

        part.cmbSpecSheet = _widg.make_combo(simple=True)
        part.cmbSpecSheet.connect("changed",
                                  self.combo_callback,
                                  part, 102)
        layout.put(part.cmbSpecSheet, x_pos, y_pos)
        y_pos += 30

        part.txtNTaps = _widg.make_entry(_width_=entry_width)
        part.txtNTaps.connect("focus-out-event",
                              self.entry_callback,
                              part, "float", 57)
        layout.put(part.txtNTaps, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Variable Value Resistor Component Class
        calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Resistor.assessment_results_create(self, part, layout,
                                                   x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        # Create the Pi TAPS results entry.  We use the pi_u field
        # in the program database to the results.
        part.txtPiTAPS = _widg.make_entry(_width_=entry_width,
                                          editable=False, bold=True)
        layout.put(part.txtPiTAPS, x_pos, y_pos)
        y_pos += 30

        part.txtPiV = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiV, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        Resistor.assessment_inputs_load(self, part)

        part.txtResistance.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 95))))
        part.cmbSpecification.set_active(int(part.model.get_value(part.selected_row, 101)))
        part.cmbSpecSheet.set_active(int(part.model.get_value(part.selected_row, 102)))
        part.txtNTaps.set_text(str("{0:0.0g}".format(part.model.get_value(part.selected_row, 57))))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Resistor.assessment_results_load(self, part)

        part.txtPiTAPS.set_text(str(fmt.format(part.model.get_value(part.selected_row, 82))))
        part.txtPiV.set_text(str(fmt.format(part.model.get_value(part.selected_row, 83))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Variable Value Resistor Component
        Class ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        Resistor.combo_callback(self, combo, part, _index_)

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        if(_index_ == 101):                     # Specification
            for i in range(len(self._specsheet[idx - 1])):
                part.cmbSpecSheet.insert_text(i, self._specsheet[idx - 1][i])

        elif(_index_== 102):                    # Specification sheet
            idx2 = model.get_value(row, 101)

            if(idx2 == 1):                      # RTR
                model.set_value(row, 94, 90.0)
            elif(idx2 == 2):                    # RT
                if(idx == 1 or idx == 2):
                    model.set_value(row, 94, 90.0)
                elif(idx == 3 or idx == 4):
                    model.set_value(row, 94, 40.0)
                else:
                    model.set_value(row, 94, 1.0)
            else:
                model.set_value(row, 94, 1.0)

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Variable Value Wirewound Resistor Component Class.

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
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

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
        the Variable Value Wirewound Resistor Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp
        from math import sqrt

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piTAPS * piR * piV * piQ * piE"

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
        R = partmodel.get_value(row, 95)

        # Base hazard rate
        S = P / Prated
        _hrmodel['lambdab'] = 0.0062 * exp(((Tamb + 273) / 298)**5.0) * exp(S * ((Tamb + 273) / 273))

        # Potentiometer taps correction factor.
        _hrmodel['piTAPS'] = ((Ntaps ** 1.5) / 25.0) + 0.792

        # Voltage correction factor.
        Vratio = Vapplied / Vrated
        if(Vratio > 0.0 and Vratio <= 0.1):
            _hrmodel['piV'] = 1.00
        elif(Vratio > 0.1 and Vratio <= 0.2):
            _hrmodel['piV'] = 1.05
        elif(Vratio > 0.2 and Vratio <= 0.6):
            _hrmodel['piV'] = 1.00
        elif(Vratio > 0.6 and Vratio <= 0.7):
            _hrmodel['piV'] = 1.10
        elif(Vratio > 0.7 and Vratio <= 0.8):
            _hrmodel['piV'] = 1.22
        elif(Vratio > 0.8 and Vratio <= 0.9):
            _hrmodel['piV'] = 1.40
        elif(Vratio > 0.9 and Vratio <= 1.0):
            _hrmodel['piV'] = 2.00

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 66, Vapplied)
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piR'])
        partmodel.set_value(partrow, 82, _hrmodel['piTAPS'])
        partmodel.set_value(partrow, 83, _hrmodel['piV'])
        partmodel.set_value(partrow, 111, Vratio)

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class VarWirewoundPower(Resistor):
    """
    Variable Value Wirewound Power Resistor Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 9.12
    """

    _construction = ["", "Enclosed", "Unenclosed"]
    _quality = ["", "MIL-SPEC", "Lower"]
    _range = ["", "1 to 2.0K", ">2.0K to 5.0K", ">5.0K to 10.0K"]
    _specsheet = ["", "RR0900", "RR1000", "RR1100", "RR1300", "RR1400",
                  "RR2000", "RR2100", "RR3000", "RR3100", "RR3200", "RR3300",
                  "RR3400", "RR3500", "RR3600", "RR3700", "RR3800", "RR3900"]

    def __init__(self):
        """
        Initializes the Variable Value Wirewound Power Resistor Component
        Class.
        """

        Resistor.__init__(self)

        self.subcategory = 33               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piC = [2.0, 1.0]
        self._piR = [1.0, 1.4, 2.0]
        self._piE = [1.0, 3.0, 16.0, 7.0, 28.0, 8.0, 12.0, 0.0, 0.0, 38.0,
                     0.5, 0.0, 0.0, 0.0]
        self._piQ = [2.0, 4.0]
        self._lambdab_count =[0.15, 0.34, 2.9, 1.2, 5.0, 1.6, 2.4, 0.0, 0.0, 7.6, 0.076, 0.0, 0.0, 0.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Nominal Resistance (\u03A9):")
        self._in_labels.append(u"Construction:")
        self._in_labels.append(u"Number of Taps:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>C</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>TAPS</sub>")
        self._out_labels.append(u"\u03C0<sub>C</sub>")
        self._out_labels.append(u"\u03C0<sub>V</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Variable Value Wirewound Power
        Resistor Component Class prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Resistor.assessment_inputs_create(self, part, layout,
                                                  x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.txtResistance = _widg.make_entry(_width_=entry_width)
        part.txtResistance.connect("focus-out-event",
                                   self.entry_callback,
                                   part, "float", 95)
        layout.put(part.txtResistance, x_pos, y_pos)
        y_pos += 30

        part.cmbConstruction = _widg.make_combo(simple=True)
        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])
        part.cmbConstruction.connect("changed",
                                  self.combo_callback,
                                  part, 16)
        layout.put(part.cmbConstruction, x_pos, y_pos)
        y_pos += 30

        part.txtNTaps = _widg.make_entry(_width_=entry_width)
        part.txtNTaps.connect("focus-out-event",
                              self.entry_callback,
                              part, "float", 57)
        layout.put(part.txtNTaps, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Variable Value Wirewound Power Resistor
        Component Class calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Resistor.assessment_results_create(self, part, layout,
                                                   x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        # Create the Pi TAPS results entry.  We use the pi_u field
        # in the program database to the results.
        part.txtPiTAPS = _widg.make_entry(_width_=entry_width,
                                          editable=False, bold=True)
        layout.put(part.txtPiTAPS, x_pos, y_pos)
        y_pos += 30

        part.txtPiC = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiC, x_pos, y_pos)
        y_pos += 30

        part.txtPiV = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiV, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        Resistor.assessment_inputs_load(self, part)

        part.txtResistance.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 95))))
        part.cmbConstruction.set_active(int(part.model.get_value(part.selected_row, 16)))
        part.txtNTaps.set_text(str("{0:0.0g}".format(part.model.get_value(part.selected_row, 57))))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Resistor.assessment_results_load(self, part)

        part.txtPiC.set_text(str("{0:0.2e}".format(part.model.get_value(part.selected_row, 69))))
        part.txtPiTAPS.set_text(str(fmt.format(part.model.get_value(part.selected_row, 82))))
        part.txtPiV.set_text(str(fmt.format(part.model.get_value(part.selected_row, 83))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Variable Value Wirewound Power
        Resistor Component Class ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        Resistor.combo_callback(self, combo, part, _index_)
        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        if(_index_ == 16):                      # Construction
            model.set_value(row, 69, self._piC[idx - 1])

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Variable Value Wirewound Power Resistor Component Class.

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
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

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
        the Variable Value Wirewound Power Resistor Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp
        from math import sqrt

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piTAPS * piR * piV * piQ * piE"

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
        if(Vratio > 0.0 and Vratio <= 0.1):
            _hrmodel['piV'] = 1.10
        elif(Vratio > 0.1 and Vratio <= 0.2):
            _hrmodel['piV'] = 1.05
        elif(Vratio > 0.2 and Vratio <= 0.6):
            _hrmodel['piV'] = 1.00
        elif(Vratio > 0.6 and Vratio <= 0.7):
            _hrmodel['piV'] = 1.10
        elif(Vratio > 0.7 and Vratio <= 0.8):
            _hrmodel['piV'] = 1.22
        elif(Vratio > 0.8 and Vratio <= 0.9):
            _hrmodel['piV'] = 1.40
        elif(Vratio > 0.9 and Vratio <= 1.0):
            _hrmodel['piV'] = 2.00

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 66, Vapplied)
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piR'])
        partmodel.set_value(partrow, 82, _hrmodel['piTAPS'])
        partmodel.set_value(partrow, 83, _hrmodel['piV'])
        partmodel.set_value(partrow, 111, Vratio)

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class WirewoundPrecision(Resistor):
    """
    Variable Value Precision Wirewound Resistor Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 9.10
    """

    _construction = ["", "Class 2", "Class 3", "Class 4", "Class 5"]
    _quality = ["", "MIL-SPEC", "Lower"]
    _range = ["", "100 to 10.0K", "10.0K to 20.0K", "20.0K to 50.0K",
              "50.0K to 100.0K", "100.0K to 200.0K", "200.0K to 500.0K"]
    _specsheet = ["", "RR0900", "RR1000", "RR1100", "RR1300", "RR1400",
                  "RR2000", "RR2100", "RR3000", "RR3100", "RR3200", "RR3300",
                  "RR3400", "RR3500", "RR3600", "RR3700", "RR3800", "RR3900"]

    def __init__(self):
        """
        Initializes the Variable Value Precision Wirewound Resistor Component
        Class.
        """

        Resistor.__init__(self)

        self.subcategory = 33               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piC = [2.0, 1.0, 3.0, 1.5]
        self._piR = [1.0, 1.1, 1.4, 2.0, 2.5, 3.5]
        self._piE = [1.0, 2.0, 18.0, 8.0, 30.0, 8.0, 12.0, 13.0, 18.0, 53.0,
                     0.5, 29.0, 76.0, 1400.0]
        self._piQ = [2.5, 5.0]
        self._lambdab_count = [0.33, 0.73, 7.0, 2.9, 12.0, 3.5, 5.3, 7.1, 9.8, 23.0, 0.16, 11.0, 33.0, 510.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Nominal Resistance (\u03A9):")
        self._in_labels.append(u"Spec Sheet:")
        self._in_labels.append(u"Construction:")
        self._in_labels.append(u"Number of Taps:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>C</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>TAPS</sub>")
        self._out_labels.append(u"\u03C0<sub>C</sub>")
        self._out_labels.append(u"\u03C0<sub>V</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Variable Value Precision
        Wirewound Resistor Component Class prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Resistor.assessment_inputs_create(self, part, layout,
                                                  x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.txtResistance = _widg.make_entry(_width_=entry_width)
        part.txtResistance.connect("focus-out-event",
                                   self.entry_callback,
                                   part, "float", 95)
        layout.put(part.txtResistance, x_pos, y_pos)
        y_pos += 30

        part.cmbSpecSheet = _widg.make_combo(simple=True)
        for i in range(len(self._specsheet)):
            part.cmbSpecification.insert_text(i, self._specsheet[i])
        part.cmbSpecSheet.connect("changed",
                                  self.combo_callback,
                                  part, 102)
        layout.put(part.cmbSpecSheet, x_pos, y_pos)
        y_pos += 30

        part.cmbConstruction = _widg.make_combo(simple=True)
        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])
        part.cmbConstruction.connect("changed",
                                  self.combo_callback,
                                  part, 16)
        layout.put(part.cmbConstruction, x_pos, y_pos)
        y_pos += 30

        part.txtNTaps = _widg.make_entry(_width_=entry_width)
        part.txtNTaps.connect("focus-out-event",
                              self.entry_callback,
                              part, "float", 57)
        layout.put(part.txtNTaps, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Variable Value Precision Wirewound Resistor
        Component Class calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Resistor.assessment_results_create(self, part, layout,
                                                   x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        # Create the Pi TAPS results entry.  We use the pi_u field
        # in the program database to the results.
        part.txtPiTAPS = _widg.make_entry(_width_=entry_width,
                                          editable=False, bold=True)
        layout.put(part.txtPiTAPS, x_pos, y_pos)
        y_pos += 30

        part.txtPiC = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiC, x_pos, y_pos)
        y_pos += 30

        part.txtPiV = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiV, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        Resistor.assessment_inputs_load(self, part)

        part.cmbConstruction.set_active(int(part.model.get_value(part.selected_row, 16)))
        part.txtNTaps.set_text(str("{0:0.0g}".format(part.model.get_value(part.selected_row, 57))))
        part.txtResistance.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 95))))
        part.cmbSpecSheet.set_active(int(part.model.get_value(part.selected_row, 102)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Resistor.assessment_results_load(self, part)

        part.txtPiC.set_text(str("{0:0.2e}".format(part.model.get_value(part.selected_row, 69))))
        part.txtPiTAPS.set_text(str(fmt.format(part.model.get_value(part.selected_row, 82))))
        part.txtPiV.set_text(str(fmt.format(part.model.get_value(part.selected_row, 83))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Variable Value Precision Wirewound
        Resistor Component Class ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        Resistor.combo_callback(self, combo, part, _index_)
        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        if(_index_ == 16):                      # Construction
            model.set_value(row, 69, self._piC[idx - 1])

        elif(_index_== 102):                    # Specification sheet
            if(idx == 1 or idx == 3 or idx == 4 or idx == 6 or idx == 8 or
               idx == 9 or idx == 10 or idx == 11 or idx == 12 or idx == 13):
                model.set_value(row, 94, 250.0)
            elif(idx == 14 or idx == 15):
                model.set_value(row, 94, 423.0)
            elif(idx == 2 or idx == 5 or idx == 7 or idx == 16 or idx == 17):
                model.set_value(row, 94, 500.0)
            else:
                model.set_value(row, 94, 1.0)

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Variable Value Precision Wirewound Resistor Component Class.

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
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

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
        the Variable Value Precision Wirewound Resistor Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp, sqrt

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ * piC * piR * piTAPS * piE * piV"

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

        if(Vratio > 0.0 and Vratio <= 0.1):
            _hrmodel['piV'] = 1.10
        elif(Vratio > 0.1 and Vratio <= 0.2):
            _hrmodel['piV'] = 1.05
        elif(Vratio > 0.2 and Vratio <= 0.6):
            _hrmodel['piV'] = 1.00
        elif(Vratio > 0.6 and Vratio <= 0.7):
            _hrmodel['piV'] = 1.10
        elif(Vratio > 0.7 and Vratio <= 0.8):
            _hrmodel['piV'] = 1.22
        elif(Vratio > 0.8 and Vratio <= 0.9):
            _hrmodel['piV'] = 1.40
        elif(Vratio > 0.9 and Vratio <= 1.0):
            _hrmodel['piV'] = 2.00

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 66, Vapplied)
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piR'])
        partmodel.set_value(partrow, 82, _hrmodel['piTAPS'])
        partmodel.set_value(partrow, 83, _hrmodel['piV'])
        partmodel.set_value(partrow, 111, Vratio)

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class WirewoundSemiPrecision(Resistor):
    """
    Variable Value Semiprecision Wirewound Resistor Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 9.11
    """

    _quality = ["", "MIL-SPEC", "Lower"]
    _range = ["", "10 to 2.0K", ">2.0K to 5.0K", ">5.0K to 10.0K"]
    _specsheet = ["", "RA10", "RA20X-XA", "RA20X-XC, F", "RA30X-XA",
                  "RA30X-XC, F", "RK09"]

    def __init__(self):

        Resistor.__init__(self)

        self.subcategory = 35               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piR = [1.0, 1.4, 2.0]
        self._piE = [1.0, 2.0, 16.0, 7.0, 28.0, 8.0, 12.0, 0.0, 0.0, 38.0,
                     0.5, 0.0, 0.0, 0.0]
        self._piQ = [2.0, 4.0]
        self._lambdab_count = [0.15, 0.35, 3.1, 1.2, 5.4, 1.9, 2.8, 0.0, 0.0, 9.0, 0.075, 0.0, 0.0, 0.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Nominal Resistance (\u03A9):")
        self._in_labels.append(u"Spec Sheet:")
        self._in_labels.append(u"Number of Taps:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>TAPS</sub>")
        self._out_labels.append(u"\u03C0<sub>V</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Variable Value Semiprecision
        Wirewound Resistor Component Class prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Resistor.assessment_inputs_create(self, part, layout,
                                                  x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.txtResistance = _widg.make_entry(_width_=entry_width)
        part.txtResistance.connect("focus-out-event",
                                   self.entry_callback,
                                   part, "float", 95)
        layout.put(part.txtResistance, x_pos, y_pos)
        y_pos += 30

        part.cmbSpecSheet = _widg.make_combo(simple=True)
        for i in range(len(self._specsheet)):
            part.cmbSpecification.insert_text(i, self._specsheet[i])
        part.cmbSpecSheet.connect("changed",
                                  self.combo_callback,
                                  part, 102)
        layout.put(part.cmbSpecSheet, x_pos, y_pos)
        y_pos += 30

        part.txtNTaps = _widg.make_entry(_width_=entry_width)
        part.txtNTaps.connect("focus-out-event",
                              self.entry_callback,
                              part, "float", 57)
        layout.put(part.txtNTaps, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Variable Value Semiprecision Wirewound Resistor
        Component Class calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Resistor.assessment_results_create(self, part, layout,
                                                   x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        # Create the Pi TAPS results entry.  We use the pi_u field
        # in the program database to the results.
        part.txtPiTAPS = _widg.make_entry(_width_=entry_width,
                                          editable=False, bold=True)
        layout.put(part.txtPiTAPS, x_pos, y_pos)
        y_pos += 30

        part.txtPiV = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiV, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        Resistor.assessment_inputs_load(self, part)

        part.cmbConstruction.set_active(int(part.model.get_value(part.selected_row, 16)))
        part.txtNTaps.set_text(str("{0:0.0g}".format(part.model.get_value(part.selected_row, 57))))
        part.txtResistance.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 95))))
        part.cmbSpecSheet.set_active(int(part.model.get_value(part.selected_row, 102)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Resistor.assessment_results_load(self, part)

        part.txtPiTAPS.set_text(str(fmt.format(part.model.get_value(part.selected_row, 82))))
        part.txtPiV.set_text(str(fmt.format(part.model.get_value(part.selected_row, 83))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Variable Value Semiprecision
        Wirewound Resistor Component Class ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        Resistor.combo_callback(self, combo, part, _index_)

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        if(_index_== 102):                  # Specification sheet
            if(idx == 1):
                model.set_value(row, 94, 50.0)
            elif(idx == 2):
                model.set_value(row, 94, 175.0)
            elif(idx == 3):
                model.set_value(row, 94, 75.0)
            elif(idx == 4):
                model.set_value(row, 94, 320.0)
            elif(idx == 5):
                model.set_value(row, 94, 130.0)
            elif(idx == 6):
                model.set_value(row, 94, 275.0)
            else:
                model.set_value(row, 94, 1.0)

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Variable Value Semiprecision Wirewound Resistor Component Class.

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
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

        _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(Part._hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the Variable Value Semiprecision Wirewound Resistor Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp, sqrt

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piTAPS * piR * piV * piQ * piE"

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
        if(Vratio > 0.0 and Vratio <= 0.1):
            _hrmodel['piV'] = 1.10
        elif(Vratio > 0.1 and Vratio <= 0.2):
            _hrmodel['piV'] = 1.05
        elif(Vratio > 0.2 and Vratio <= 0.6):
            _hrmodel['piV'] = 1.00
        elif(Vratio > 0.6 and Vratio <= 0.7):
            _hrmodel['piV'] = 1.10
        elif(Vratio > 0.7 and Vratio <= 0.8):
            _hrmodel['piV'] = 1.22
        elif(Vratio > 0.8 and Vratio <= 0.9):
            _hrmodel['piV'] = 1.40
        elif(Vratio > 0.9 and Vratio <= 1.0):
            _hrmodel['piV'] = 2.00

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 66, Vapplied)
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piR'])
        partmodel.set_value(partrow, 82, _hrmodel['piTAPS'])
        partmodel.set_value(partrow, 83, _hrmodel['piV'])
        partmodel.set_value(partrow, 111, Vratio)

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class NonWirewound(Resistor):
    """
    Variable Value Nonwirewound Resistor Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 9.15
    """

    _quality = ["", "S", "R", "P", "M", "MIL-R-22097", "Lower"]
    _range = ["", "10 to 50.0K", ">50.0K to 100.0K", ">100.0K to 200.0K",
              ">200.0K to 500.0K", ">500.0K to 1.0M"]
    _specsheet = ["", "RJ28", "RJ50", "RJR28", "RJR50", "Other"]

    def __init__(self):
        """
        Initializes the Variable Value NonWirewound Resistor Component Class.
        """

        Resistor.__init__(self)

        self.subcategory = 37               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piR = [1.0, 1.1, 1.2, 1.4, 1.8]
        self._piE = [1.0, 3.0, 14.0, 6.0, 24.0, 5.0, 7.0, 12.0, 18.0, 39.0,
                     0.5, 22.0, 57.0, 1000.0]
        self._piQ = [0.02, 0.06, 0.2, 0.6, 3.0, 10.0]
        self._lambdab_count = [0.043, 0.15, 0.75, 0.35, 1.3, 0.39, 0.78, 1.8, 2.8, 2.5, 0.21, 1.2, 3.7, 49.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Nominal Resistance (\u03A9):")
        self._in_labels.append(u"Spec Sheet:")
        self._in_labels.append(u"Number of Taps:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>TAPS</sub>")
        self._out_labels.append(u"\u03C0<sub>V</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Variable Value Nonwirewound
        Resistor Component Class prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Resistor.assessment_inputs_create(self, part, layout,
                                                  x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.txtResistance = _widg.make_entry(_width_=entry_width)
        part.txtResistance.connect("focus-out-event",
                                   self.entry_callback,
                                   part, 'float', 95)
        layout.put(part.txtResistance, x_pos, y_pos)
        y_pos += 30

        part.cmbSpecSheet = _widg.make_combo(simple=True)
        for i in range(len(self._specsheet)):
            part.cmbSpecSheet.insert_text(i, self._specsheet[i])
        part.cmbSpecSheet.connect("changed",
                                  self.combo_callback,
                                  part, 102)
        layout.put(part.cmbSpecSheet, x_pos, y_pos)
        y_pos += 30

        part.txtNTaps = _widg.make_entry(_width_=entry_width)
        part.txtNTaps.connect("focus-out-event",
                              self.entry_callback,
                              part, "float", 57)
        layout.put(part.txtNTaps, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Variable Value Nonwirewound Resistor Component
        Class calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Resistor.assessment_results_create(self, part, layout,
                                                   x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        # Create the Pi TAPS results entry.  We use the pi_u field
        # in the program database to the results.
        part.txtPiTAPS = _widg.make_entry(_width_=entry_width,
                                          editable=False, bold=True)
        layout.put(part.txtPiTAPS, x_pos, y_pos)
        y_pos += 30

        part.txtPiV = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiV, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        Resistor.assessment_inputs_load(self, part)

        part.txtResistance.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 95))))
        part.cmbSpecSheet.set_active(int(part.model.get_value(part.selected_row, 102)))
        part.txtNTaps.set_text(str("{0:0.0g}".format(part.model.get_value(part.selected_row, 57))))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Resistor.assessment_results_load(self, part)

        part.txtPiTAPS.set_text(str(fmt.format(part.model.get_value(part.selected_row, 82))))
        part.txtPiV.set_text(str(fmt.format(part.model.get_value(part.selected_row, 83))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Variable Value Nonwirewound Resistor
        Component Class ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        Resistor.combo_callback(self, combo, part, _index_)

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        if(_index_== 102):                  # Specification sheet
            if(idx == 1 or idx == 2 or idx == 3 or idx == 4):
                model.set_value(row, 94, 200.0)
            else:
                model.set_value(row, 94, 300.0)

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Variable Value Nonwirewound Resistor Component Class.

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
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

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
        the Variable Value Nonwirewound Resistor Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp, sqrt

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piTAPS * piR * piV * piQ * piE"

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

        if(Vratio > 0.0 and Vratio <= 0.8):
            _hrmodel['piV'] = 1.00
        elif(Vratio > 0.8 and Vratio <= 0.9):
            _hrmodel['piV'] = 1.05
        elif(Vratio > 0.9 and Vratio <= 1.0):
            _hrmodel['piV'] = 1.20
        else:
            _hrmodel['piV'] = 0.0

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 66, Vapplied)
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piR'])
        partmodel.set_value(partrow, 82, _hrmodel['piTAPS'])
        partmodel.set_value(partrow, 83, _hrmodel['piV'])
        partmodel.set_value(partrow, 111, Vratio)

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class Composition(Resistor):
    """
    Variable Value Carbon Composition Resistor Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 9.14
    """

    _quality = ["", "MIL-SPEC", "Lower"]
    _range = ["", "50 to 50.0K", ">50.0K to 100.0K", ">100.0K to 200.0K",
              ">200.0K to 500.0K", ">500.0K to 1.0M"]
    _specsheet = ["", "RV1X-XA, XB", "RV2X-XA, XB", "RV3X-XA, XB",
                  "RV4X-XA, XB", "RV5X-XA, XB", "RV6X-XA, XB", "RV7X-XA, XB",
                  "Other"]

    def __init__(self):
        """
        Initializes the Variable Value Carbon Composition Resistor Component
        Class.
        """

        Resistor.__init__(self)

        self.subcategory = 37               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piR = [1.0, 1.1, 1.2, 1.4, 1.8]
        self._piE = [1.0, 2.0, 19.0, 8.0, 29.0, 40.0, 65.0, 48.0, 78.0,
                     46.0, 0.5, 25.0, 66.0, 1200.0]
        self._piQ = [2.5, 5.0]
        self._lambdab_count =[0.05, 0.11, 1.1, 0.45, 1.7, 2.8, 4.6, 4.6, 7.5, 3.3, 0.025, 1.5, 4.7, 67.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Nominal Resistance (\u03A9):")
        self._in_labels.append(u"Spec Sheet:")
        self._in_labels.append(u"Number of Taps:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>TAPS</sub>")
        self._out_labels.append(u"\u03C0<sub>V</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Variable Value Carbon
        Composition Resistor Component Class prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Resistor.assessment_inputs_create(self, part, layout,
                                                  x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.txtResistance = _widg.make_entry()
        part.txtResistance.connect("focus-out-event",
                                   self.entry_callback,
                                   part, "float", 95)
        layout.put(part.txtResistance, x_pos, y_pos)
        y_pos += 30

        part.cmbSpecSheet = _widg.make_combo(simple=True)
        for i in range(len(self._specsheet)):
            part.cmbSpecSheet.insert_text(i, self._specsheet[i])
        part.cmbSpecSheet.connect("changed",
                                  self.combo_callback,
                                  part, 102)
        layout.put(part.cmbSpecSheet, x_pos, y_pos)
        y_pos += 30

        part.txtNTaps = _widg.make_entry(_width_=entry_width)
        part.txtNTaps.connect("focus-out-event",
                              self.entry_callback,
                              part, "float", 57)
        layout.put(part.txtNTaps, x_pos, y_pos)
        y_pos += 30

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Variable Value Carbon Composition Resistor
        Component Class calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Resistor.assessment_results_create(self, part, layout,
                                                   x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        # Create the Pi TAPS results entry.  We use the pi_u field
        # in the program database to the results.
        part.txtPiTAPS = _widg.make_entry(_width_=entry_width,
                                          editable=False, bold=True)
        layout.put(part.txtPiTAPS, x_pos, y_pos)
        y_pos += 30

        part.txtPiV = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiV, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        Resistor.assessment_inputs_load(self, part)

        part.txtNTaps.set_text(str("{0:0.0g}".format(part.model.get_value(part.selected_row, 57))))
        part.txtResistance.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 95))))
        part.cmbSpecSheet.set_active(int(part.model.get_value(part.selected_row, 102)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Resistor.assessment_results_load(self, part)

        part.txtPiTAPS.set_text(str(fmt.format(part.model.get_value(part.selected_row, 82))))
        part.txtPiV.set_text(str(fmt.format(part.model.get_value(part.selected_row, 83))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Variable Value Carbon Composition
        Resistor Component Class ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        Resistor.combo_callback(self, combo, part, _index_)

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        if(_index_== 102):                  # Specification sheet
            if(idx == 1):
                model.set_value(row, 94, 250.0)
            elif(idx == 2 or idx == 4 or idx == 5 or idx == 6):
                model.set_value(row, 94, 350.0)
            elif(idx == 3 or idx == 7):
                model.set_value(row, 94, 500.0)
            else:
                model.set_value(row, 94, 200.0)

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Variable Value Carbon Composition Resistor Component Class.

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
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

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
        the Variable Value Carbon Composition Resistor Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp, sqrt

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piTAPS * piR * piV * piQ * piE"

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
        idx = part._app.HARDWARE.model.get_value(part._app.HARDWARE.selected_row, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 66, Vapplied)
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piR'])
        partmodel.set_value(partrow, 82, _hrmodel['piTAPS'])
        partmodel.set_value(partrow, 83, _hrmodel['piV'])
        partmodel.set_value(partrow, 111, Vratio)

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class VarFilm(Resistor):
    """
    Variable Value Film Resistor Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 9.15
    """

    _quality = ["", "MIL-SPEC", "Lower"]
    _range = ["", "Up to 10.0K", ">10.0K to 50.0K", ">50.0K to 200.0K",
              ">200.0K to 1.0M"]
    _specification = ["", "MIL-R-39023 (RQ)", "MIL-R-23285 (RVC)"]
    _specsheet = [["", "RQ090", "RQ100", "RQ110", "RQ150", "RQ160",
                   "RQ200", "RQ210", "RQ300"], ["", "RVC5", "RVC6"]]

    def __init__(self):
        """ Initializes the Variable Value Film Resistor Component Class. """

        Resistor.__init__(self)

        self.subcategory = 37               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piR = [1.0, 1.1, 1.2, 1.4, 1.8]
        self._piE = [1.0, 3.0, 14.0, 7.0, 24.0, 6.0, 12.0, 20.0, 30.0,
                     39.0, 0.5, 22.0, 57.0, 1000.0]
        self._piQ = [2.0, 4.0]
        self._lambdab_count = [0.048, 0.16, 0.76, 0.36, 1.3, 0.36, 0.72, 1.4, 2.2, 2.3, 0.024, 1.2, 3.4, 52.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Nominal Resistance (\u03A9):")
        self._in_labels.append(u"Specification:")
        self._in_labels.append(u"Spec Sheet:")
        self._in_labels.append(u"Number of Taps:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>TAPS</sub>")
        self._out_labels.append(u"\u03C0<sub>V</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Variable Value Film Resistor
        Component Class prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Resistor.assessment_inputs_create(self, part, layout,
                                                  x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.txtResistance = _widg.make_entry()
        part.txtResistance.connect("focus-out-event",
                                   self.entry_callback,
                                   part, "float", 95)
        layout.put(part.txtResistance, x_pos, y_pos)
        y_pos += 30

        part.cmbSpecification = _widg.make_combo(simple=True)
        for i in range(len(self._specification)):
            part.cmbSpecification.insert_text(i, self._specification[i])
        part.cmbSpecification.connect("changed",
                                      self.combo_callback,
                                      part, 101)
        layout.put(part.cmbSpecification, x_pos, y_pos)
        y_pos += 30

        part.cmbSpecSheet = _widg.make_combo(simple=True)
        part.cmbSpecSheet.connect("changed",
                                  self.combo_callback,
                                  part, 102)
        layout.put(part.cmbSpecSheet, x_pos, y_pos)
        y_pos += 30

        part.txtNTaps = _widg.make_entry(_width_=entry_width)
        part.txtNTaps.connect("focus-out-event",
                              self.entry_callback,
                              part, "float", 57)
        layout.put(part.txtNTaps, x_pos, y_pos)
        y_pos += 30

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Variable Value Film Resistor Component Class
        calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Resistor.assessment_results_create(self, part, layout,
                                                   x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        # Create the Pi TAPS results entry.  We use the pi_u field
        # in the program database to the results.
        part.txtPiTAPS = _widg.make_entry(_width_=entry_width,
                                          editable=False, bold=True)
        layout.put(part.txtPiTAPS, x_pos, y_pos)
        y_pos += 30

        part.txtPiV = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiV, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        Resistor.assessment_inputs_load(self, part)

        part.txtResistance.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 95))))
        part.cmbSpecification.set_active(int(part.model.get_value(part.selected_row, 101)))
        part.cmbSpecSheet.set_active(int(part.model.get_value(part.selected_row, 102)))
        part.txtNTaps.set_text(str("{0:0.0g}".format(part.model.get_value(part.selected_row, 57))))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Resistor.assessment_results_load(self, part)

        part.txtPiTAPS.set_text(str(fmt.format(part.model.get_value(part.selected_row, 82))))
        part.txtPiV.set_text(str(fmt.format(part.model.get_value(part.selected_row, 83))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Variable Value Film Resistor
        Component Class ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        Resistor.combo_callback(self, combo, part, _index_)

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        if(_index_ == 101):                 # Specification
            for i in range(len(self._specsheet[idx - 1])):
                part.cmbSpecSheet.insert_text(i, self._specsheet[idx - 1][i])

        elif(_index_== 102):                # Specification sheet
            if(idx == 1):
                model.set_value(row, 94, 250.0)
            elif(idx == 2 or idx == 4 or idx == 5 or idx == 6):
                model.set_value(row, 94, 350.0)
            elif(idx == 3 or idx == 7):
                model.set_value(row, 94, 500.0)
            else:
                model.set_value(row, 94, 200.0)

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Variable Value Film Resistor Component Class.

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
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Sidx = partmodel.get_value(partrow, 101)        # Specification index
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

        _hrmodel['lambdab'] = self._lambdab_count[Sidx - 1][Eidx - 1]

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
        the Variable Value Film Resistor Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp, sqrt

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piTAPS * piR * piV * piQ * piE"

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
        if(Vratio >= 0.0 and Vratio <= 0.8):
            _hrmodel['piV'] = 1.00
        elif(Vratio > 0.8 and Vratio <= 0.9):
            _hrmodel['piV'] = 1.05
        elif(Vratio > 0.9 and Vratio <= 1.0):
            _hrmodel['piV'] = 1.20
        else:
            _hrmodel['piV'] = 0.0

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 66, Vapplied)
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piR'])
        partmodel.set_value(partrow, 82, _hrmodel['piTAPS'])
        partmodel.set_value(partrow, 83, _hrmodel['piV'])
        partmodel.set_value(partrow, 111, Vratio)

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
