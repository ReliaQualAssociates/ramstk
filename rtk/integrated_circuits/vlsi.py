#!/usr/bin/env python
""" This is the VLSI integrated circuit class. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       vlsi.py is part of The RelKit Project
#
# All rights reserved.

try:
    import relkit.calculations as _calc
    import relkit.widgets as _widg
except ImportError:
    import calculations as _calc
    import widgets as _widg

from ic import IntegratedCircuit


class VLSI(IntegratedCircuit):
    """
    VHSIC/VHSIC-like and VLSI CMOS integrated circuit class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 5.3
    """

    _man = ["", "QML or QPL", "Non QML or Non QPL"]

    _app = ["", "Logic or Custom", "Gate Array"]

    _package = ["", "Hermetic DIP", "Hermetic PGA",
                "Hermetic Chip Carrier", "Nonhermetic DIP",
                "Nonhermetic PGA", "Nonhermetic Chip Carrier"]

    def __init__(self):
        """ Initializes the VLSI integrated circuit class. """

        IntegratedCircuit.__init__(self)

        self.subcategory = 11       # Subcategory ID in relkitcom database.

        self._in_labels[2] = "# of Transistors:"
        self._in_labels.append("Man Process:")
        self._in_labels.append("Application:")
        self._in_labels.append("Feature Size:")
        self._in_labels.append("Die Area:")
        self._in_labels.append("ESD Susceptibility:")
        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>BD</sub>\u03C0<sub>T</sub>\u03C0<sub>MFG</sub>\u03C0<sub>CD</sub> + \u03BB<sub>BP</sub>\u03C0<sub>E</sub>\u03C0<sub>Q</sub>\u03C0<sub>PT</sub> + \u03BB<sub>EOS</sub></span>"
        self._out_labels[3] = u"\u03BB<sub>BD</sub>:"   # Use txtC1 to display results.
        self._out_labels[5] = u"\u03C0<sub>MFG</sub>:"  # Use txtC2 to display results.
        self._out_labels[8] = u"\u03C0<sub>PT</sub>:"   # Use txtPiL to dsiplay results.
        self._out_labels.append(u"\u03C0<sub>CD</sub>:")
        self._out_labels.append(u"\u03BB<sub>BP</sub>:")
        self._out_labels.append(u"\u03BB<sub>EOS</sub>:")

        self._Ea = [[0.35], [0.35]]
        self._lambdaBD = [0.16, 0.24]
        self._piMFG = [0.55, 2.0]
        self._piPT = [1.0, 2.2, 4.7, 1.3, 2.9, 6.1]

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for VLSI Integrated Circuit
        prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = IntegratedCircuit.assessment_inputs_create(self, part, layout,
                                                           x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.cmbElements.append_text("")
        part.cmbElements.append_text("> 60000")

        for i in range(len(self._package)):
            part.cmbPackage.insert_text(i, self._package[i])

        # Create the Manufacturing Method combobox.
        part.cmbManufacturing = _widg.make_combo(simple=True)
        for i in range(len(self._man)):
            part.cmbManufacturing.insert_text(i, self._man[i])
        part.cmbManufacturing.connect("changed",
                                      self.combo_callback,
                                      part, 54)
        layout.put(part.cmbManufacturing, x_pos, y_pos)
        y_pos += 30

        # Create the Application combobox.
        part.cmbApplication = _widg.make_combo(simple=True)
        for i in range(len(self._app)):
            part.cmbApplication.insert_text(i, self._app[i])
        part.cmbApplication.connect("changed",
                                    self.combo_callback,
                                    part, 5)
        layout.put(part.cmbApplication, x_pos, y_pos)
        y_pos += 30

        # Create the Die Area text entry.
        part.txtArea = _widg.make_entry(width=entry_width)
        part.txtArea.connect("focus-out-event",
                             self.entry_callback,
                             part, "float", 21)
        layout.put(part.txtArea, x_pos, y_pos)
        y_pos += 30

        # Create the ESD Susceptibility text entry.
        part.txtESD = _widg.make_entry(width=entry_width)
        part.txtESD.connect("focus-out-event",
                            self.entry_callback,
                            part, "float", 25)
        layout.put(part.txtESD, x_pos, y_pos)
        y_pos += 30

        # Create the Die Feature Size text entry.
        part.txtFeature = _widg.make_entry(width=entry_width)
        part.txtFeature.connect("focus-out-event",
                                self.entry_callback,
                                part, "float", 29)
        layout.put(part.txtFeature, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display VLSI Integrated Circuit calculation
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

        part.txtPiCD = _widg.make_entry(width=entry_width,
                                        editable=False, bold=True)
        layout.put(part.txtPiCD, x_pos, y_pos)
        y_pos += 30

        part.txtPiMFG = _widg.make_entry(width=entry_width,
                                        editable=False, bold=True)
        layout.put(part.txtPiMFG, x_pos, y_pos)
        y_pos += 30

        part.txtPiPT = _widg.make_entry(width=entry_width,
                                        editable=False, bold=True)
        layout.put(part.txtPiPT, x_pos, y_pos)
        y_pos += 30

        part.txtLambdaBP = _widg.make_entry(width=entry_width,
                                            editable=False, bold=True)
        layout.put(part.txtLambdaBP, x_pos, y_pos)
        y_pos += 30

        part.txtLambdaEOS = _widg.make_entry(width=entry_width,
                                             editable=False, bold=True)
        layout.put(part.txtLambdaEOS, x_pos, y_pos)

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

        IntegratedCircuit.assessment_inputs_load(self, part)

        part.cmbApplication.set_active(int(part.model.get_value(part.selected_row, 5)))
        part.txtArea.set_text(str(fmt.format(part.model.get_value(part.selected_row, 21))))
        part.cmbElements.set_active(int(part.model.get_value(part.selected_row, 24)))
        part.txtESD.set_text(str(fmt.format(part.model.get_value(part.selected_row, 25))))
        part.txtFeature.set_text(str(fmt.format(part.model.get_value(part.selected_row, 29))))
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

        part.txtPiCD.set_text(str(fmt.format(part.model.get_value(part.selected_row, 70))))
        part.txtPiMFG.set_text(str("{0:0.3g}".format(part.model.get_value(part.selected_row, 77))))
        part.txtPiPT.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 78))))
        part.txtLambdaBP.set_text(str(fmt.format(part.model.get_value(part.selected_row, 52))))
        part.txtLambdaEOS.set_text(str(fmt.format(part.model.get_value(part.selected_row, 51))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Integrated Circuit Class
        ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        idx = combo.get_active()

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        if(_index_ == 24 or _index_ == 104):
            model.set_value(row, _index_, int(idx))
        else:
            IntegratedCircuit.combo_callback(self, combo, part, _index_)

        if(_index_ == 5):           # Application
            model.set_value(row, 50, self._lambdaBD[idx - 1])

        elif(_index_ == 54):        # Manufacturing process
            model.set_value(row, 77, self._piMFG[idx - 1])

        elif(_index_ == 67):        # Package type
            model.set_value(row, 78, self._piPT[idx - 1])

    def entry_callback(self, entry, event, part, convert, _index_):
        """
        Callback function for handling Integrated Circuit Class Entry
        changes.

        Keyword Arguments:
        entry   -- the entry widget calling this function.
        event   -- the event that triggered calling this function.
        part    -- the RelKit COMPONENT object.
        convert -- the data type to convert the entry contents to.
        _index_ -- the position in the Component property array
                   associated with the data from the entry that called
                   this function.
        """

        IntegratedCircuit.entry_callback(self, entry, event,
                                         part, convert, _index_)

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        if(_index_ == 21):          # Die area
            model.set_value(row, 21, float(entry.get_text()))

        elif(_index_ == 25):        # ESD susceptibility
            model.set_value(row, 25, float(entry.get_text()))

        elif(_index_ == 29):        # Feature size
            model.set_value(row, 29, float(entry.get_text()))

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        VLSI Integrated Circuit Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        print "MIL-HDBK-217 parts count methodology not yet implemented."
        # TODO: Implement MIL-HDBK-217F parts count methodology for VLSI IC.

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the VLSI Integrated Circuit Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp
        from math import log

        _hrmodel = {}
        _hrmodel['equation'] = "lambdaBD * piMFG * piT * piCD + lambdaBP * piE * piQ *piPT + lambdaEOS"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)
        P = partmodel.get_value(partrow, 64)

        # Retrieve hazard rate inputs.
        A = partmodel.get_value(partrow, 21)
        Ea = partmodel.get_value(partrow, 22)
        Vth = partmodel.get_value(partrow, 25)
        Xs = partmodel.get_value(partrow, 29)
        _hrmodel['lambdaBD'] = partmodel.get_value(partrow, 50)
        B = partmodel.get_value(partrow, 58)
        Np = partmodel.get_value(partrow, 60)
        _hrmodel['piMFG'] = partmodel.get_value(partrow, 77)
        _hrmodel['piPT'] = partmodel.get_value(partrow, 78)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
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

        # Junction temperature
        Tj = Tcase + thetaJC * P

        # Calculate the temperature factor.  We store this in the pi_u
        # field in the Program Database.
        _hrmodel['piT'] = 0.1 * exp((-1.0 * Ea / 0.00008617) * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

        # Environmental factor
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Die complexity correction factor.  We store this in the pi_cf
        # field in the Program Database.
        _hrmodel['piCD'] = ((A / 0.21) * ((2.0 / Xs) ** 2.0) * 0.64) + 0.36

        # Package base failure rate.  We store this in the lambda_g
        # field in the program database.
        _hrmodel['lambdaBP'] = 0.0022 + (0.0000172 * Np)

        # Electrical overstress failure rate.
        _hrmodel['lambdaEOS'] = (-1.0 * log(1.0 - 0.00057 * exp(-1.0 * 0.0002 * Vth))) / 0.00876

        # Part failure rate
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 50, _hrmodel['lambdaBD'])
        partmodel.set_value(partrow, 51, _hrmodel['lambdaEOS'])
        partmodel.set_value(partrow, 52, _hrmodel['lambdaBP'])
        partmodel.set_value(partrow, 70, _hrmodel['piCD'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
