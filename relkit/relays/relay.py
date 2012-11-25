#!/usr/bin/env python
""" These are the relay component classes. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2012 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       relay.py is part of The RelKit Project
#
# All rights reserved.

import pango

try:
    import reliafree.calculations as _calc
    import reliafree.widgets as _widg
except ImportError:
    import calculations as _calc
    import widgets as _widg


class Mechanical:
    """
    Mechanical Relay Component Class.
    Covers specifications MIL-R-5757, MIL-R-6106, MIL-R-19523, and
    MIL-R-39016.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 13.1
    """

    _application = [["", "Dry Circuit"],
                    ["", "General Purpose", "Sensitive (0-100 mW)",
                     "Polarized", "Vibrating Reed", "High Speed",
                     "Thermal Time Delay", "Electronic Time Delay",
                     "Magnetic Latching"],
                    ["",  "High Voltage", "Medium Power"],
                    ["", "Contactor"]]
    _construction = [[["", "Long Armature", "Dry Reed", "Mercury Wetted",
                       "Magnetic Latching", "Balanced Armature", "Solenoid"]],
                     [["", "Long Armature", "Balanaced Armature", "Solenoid"],
                      ["", "Long Armature", "Short Armature", "Mercury Wetted",
                       "Magnetic Latching", "Meter Movement",
                       "Balanced Armature"],
                      ["", "Short Armature", "Meter Movement"],
                      ["", "Dry Reed", "Mecury Wetted"],
                      ["", "Balanced Armature", "Short Armature", "Dry Reed"],
                      ["", "Bimetal"],
                      [""],
                      ["", "Dry Reed", "Mercury Wetted", "Balanced Armature"]],
                     [["", "Vacuum, Glass", "Vacuum, Ceramic"],
                      ["", "Long Armature", "Short Armature", "Mercury Wetted",
                       "Magnetic Latching", "Mechanical Latching",
                       "Balanced Armature", "Solenoid"]],
                     [["", "Short Armature", "Mechanical Latching",
                       "Balanced Armature", "Solenoid"]]]
    _form = ["", "SPST", "DPST", "SPDT", "3PST", "4PST", "DPDT", "3PDT",
                "4PDT", "6PDT"]
    _insulation = ["", u"85\u00B0C", u"125\u00B0C"]
    _load = ["", "Resistive", "Inductive", "Lamp"]
    _quality = ["", "R", "P", "X", "U", "M", "L", "Non-Est. Reliability", "Lower"]
    _rating = ["", "Signal Current (Low mV and mA)", "0-5 Amp", "5-20 Amp", "20-600 Amp"]

    def __init__(self):
        """ Initializes the Mechanical Relay Component Class. """

        self._ready = False

        self._in_labels = []
        self._out_labels = []

        self.category = 6                   # Category in reliafreecom database.
        self.subcategory = 64               # Subcategory in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piC = [1.0, 1.5, 1.75, 2.0, 2.5, 3.0, 4.25, 5.5, 8.0]
        self._piE = [[1.0, 2.0, 15.0, 8.0, 27.0, 7.0, 9.0, 11.0, 12.0, 46.0,
                      0.50, 25.0, 66.0, 0.0], [2.0, 5.0, 44.0, 24.0, 78.0,
                      15.0, 20.0, 28.0, 38.0, 140.0, 1.0, 72.0, 200.0, 0.0]]
        self._piQ = [0.10, 0.30, 0.45, 0.60, 1.0, 1.5, 3.0, 3.0]
        self._lambdab_count =[[0.13, 0.28, 2.1, 1.1, 3.8, 1.1, 1.4, 1.9, 2.0, 7.0, 0.66, 3.5, 10.0, 0.0],
                              [0.43, 0.89, 6.9, 3.6, 12.0, 3.4, 4.4, 6.2, 6.7, 22.0, 0.21, 11.0, 32.0, 0.0],
                              [0.13, 0.26, 2.1, 1.1, 3.8, 1.1, 1.4, 1.9, 2.0, 7.0, 0.66, 3.5, 10.0, 0.0],
                              [0.11, 0.23, 1.8, 0.92, 3.3, 0.96, 1.2, 2.1, 2.3, 6.5, 0.54, 3.0, 9.0, 0.0],
                              [0.29, 0.60, 4.8, 2.4, 8.2, 2.3, 2.9, 4.1, 4.5, 15.0, 0.14, 7.6, 22.0, 0.0],
                              [0.88, 1.8, 14.0, 7.4, 26.0, 7.1, 9.1, 13.0, 14.0, 46.0, 0.44, 24.0, 67.0, 0.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        # Label text for input data.
        self._in_labels.append(u"Quality:")
        self._in_labels.append(u"\u03C0<sub>Q</sub> Override:")
        self._in_labels.append(u"Rated Temperature (\u00B0C):")
        self._in_labels.append(u"Load Type:")
        self._in_labels.append(u"Rated Current (A):")
        self._in_labels.append(u"Operating Current (A):")
        self._in_labels.append(u"Cycling Rate:")
        self._in_labels.append(u"Contact Form:")
        self._in_labels.append(u"Contact Rating:")
        self._in_labels.append(u"Application:")
        self._in_labels.append(u"Construction:")

        # Label text for output data.
        self._out_labels.append(u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>L</sub>\u03C0<sub>C</sub>\u03C0<sub>CYC</sub>\u03C0<sub>F</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>")
        self._out_labels.append(u"\u03BB<sub>b</sub>:")
        self._out_labels.append(u"\u03C0<sub>L</sub>:")
        self._out_labels.append(u"\u03C0<sub>C</sub>:")
        self._out_labels.append(u"\u03C0<sub>CYC</sub>:")
        self._out_labels.append(u"\u03C0<sub>F</sub>:")
        self._out_labels.append(u"\u03C0<sub>Q</sub>:")
        self._out_labels.append(u"\u03C0<sub>E</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Mechanical Relay Component
        Class prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        entry_width = int((int(part.fmt) + 5) * 8)

        # Get the list of widgets already on the layout.
        # Check each child widget's name.  If it is IC,
        # then it needs to be removed before placing new
        # widgets.
        chwidgets = layout.get_children()
        for i in range(len(chwidgets)):
            if(chwidgets[i].get_name() == "TRANSIENT"):
                layout.remove(chwidgets[i])

        # Create and place all the labels for the inputs.
        numlabels = len(self._in_labels)
        for i in range(numlabels):
            label = _widg.make_label(self._in_labels[i])
            layout.put(label, 5, (i * 30 + y_pos))

        part.cmbQuality = _widg.make_combo(simple=True)
        for i in range(len(self._quality)):
            part.cmbQuality.insert_text(i, self._quality[i])
        part.cmbQuality.connect("changed",
                                self.combo_callback,
                                part, 85)
        layout.put(part.cmbQuality, x_pos, y_pos)
        y_pos += 35

        part.txtCommercialPiQ = _widg.make_entry(_width_=entry_width)
        part.txtCommercialPiQ.connect("focus-out-event",
                                      self.entry_callback,
                                      part, "float", 79)
        layout.put(part.txtCommercialPiQ, x_pos, y_pos)
        y_pos += 30

        part.cmbInsulation = _widg.make_combo(simple=True)
        for i in range(len(self._insulation)):
            part.cmbInsulation.insert_text(i, self._insulation[i])
        part.cmbInsulation.connect("changed",
                                   self.combo_callback,
                                   part, 38)
        layout.put(part.cmbInsulation, x_pos, y_pos)
        y_pos += 35

        # Create the load type combobox.  We store this in the func_id field
        # in the program database.
        part.cmbLoad = _widg.make_combo(simple=True)
        for i in range(len(self._load)):
            part.cmbLoad.insert_text(i, self._load[i])
        part.cmbLoad.connect("changed",
                             self.combo_callback,
                             part, 30)
        layout.put(part.cmbLoad, x_pos, y_pos)
        y_pos += 35

        part.txtRatedCurrent = _widg.make_entry(_width_=entry_width)
        part.txtRatedCurrent.connect("focus-out-event",
                                     self.entry_callback,
                                     part, "float", 92)
        layout.put(part.txtRatedCurrent, x_pos, y_pos)
        y_pos += 30

        part.txtOperCurrent = _widg.make_entry(_width_=entry_width)
        part.txtOperCurrent.connect("focus-out-event",
                                    self.entry_callback,
                                    part, "float", 62)
        layout.put(part.txtOperCurrent, x_pos, y_pos)
        y_pos += 30

        part.txtCycleRate = _widg.make_entry(_width_=entry_width)
        part.txtCycleRate.connect("focus-out-event",
                                  self.entry_callback,
                                  part, "float", 19)
        layout.put(part.txtCycleRate, x_pos, y_pos)
        y_pos += 30

        # Create the contact form combobox.  We store this in the family_id
        # field in the program database.
        part.cmbForm = _widg.make_combo(simple=True)
        for i in range(len(self._form)):
            part.cmbForm.insert_text(i, self._form[i])
        part.cmbForm.connect("changed",
                             self.combo_callback,
                             part, 28)
        layout.put(part.cmbForm, x_pos, y_pos)
        y_pos += 35

        # Create the contact rating combobox.  We store this in the
        # resistance_id field in the program database.
        part.cmbRating = _widg.make_combo(simple=True)
        for i in range(len(self._rating)):
            part.cmbRating.insert_text(i, self._rating[i])
        part.cmbRating.connect("changed",
                               self.combo_callback,
                               part, 96)
        layout.put(part.cmbRating, x_pos, y_pos)
        y_pos += 35

        part.cmbApplication = _widg.make_combo(simple=True)
        part.cmbApplication.connect("changed",
                                    self.combo_callback,
                                    part, 5)
        layout.put(part.cmbApplication, x_pos, y_pos)
        y_pos += 35

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
        widgets to display Mechanical Relay Component Class calculation
        results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        entry_width = int((int(part.fmt) + 5) * 8)

        # Get the list of widgets already on the layout.
        # Check each child widget's name.  If it is IC,
        # then it needs to be removed before placing new
        # widgets.
        chwidgets = layout.get_children()
        for i in range(len(chwidgets)):
            if(chwidgets[i].get_name() == "TRANSIENT"):
                layout.remove(chwidgets[i])

        # Create and place all the labels.
        numlabels = len(self._out_labels)
        for i in range(numlabels):
            if(i == 2):
                label = _widg.make_label(self._out_labels[i], width=400)
                llayout = label.get_layout()
                llayout.set_alignment(pango.ALIGN_CENTER)
                label.show_all()
            else:
                label = _widg.make_label(self._out_labels[i])
            layout.put(label, 5, (i * 30 + y_pos))

        y_pos += 30

        # Create the Temperature Rise results entry.
        #part.txtTRise = _widg.make_entry(editable=False, bold=True)
        #layout.put(part.txtTRise, 155, 305)
        #part.txtTRise.set_text(str(part._calc_data[107]))

        # Create the Junction Temperature results entry.
        #part.txtTJunc = _widg.make_entry(editable=False, bold=True)
        #layout.put(part.txtTJunc, 155, 335)
        #part.txtTJunc.set_text(str(part._calc_data[39]))

        part.txtLambdaB = _widg.make_entry(_width_=entry_width,
                                           editable=False, bold=True)
        layout.put(part.txtLambdaB, x_pos, y_pos)
        y_pos += 30

        # Create the Pi L results entry.  We store this in the pi_m field
        # in the program database.
        part.txtPiL = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiL, x_pos, y_pos)
        y_pos += 30

        part.txtPiC = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiC, x_pos, y_pos)
        y_pos += 30

        part.txtPiCYC = _widg.make_entry(_width_=entry_width,
                                         editable=False, bold=True)
        layout.put(part.txtPiCYC, x_pos, y_pos)
        y_pos += 30

        part.txtPiF = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiF, x_pos, y_pos)
        y_pos += 30

        part.txtPiQ = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiQ, x_pos, y_pos)
        y_pos += 30

        part.txtPiE = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiE, x_pos, y_pos)

        layout.show_all()

        self._ready = True

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        part.cmbQuality.set_active(int(part.model.get_value(part.selected_row, 85)))
        part.cmbInsulation.set_active(int(part.model.get_value(part.selected_row, 38)))
        part.cmbLoad.set_active(int(part.model.get_value(part.selected_row, 30)))
        part.txtRatedCurrent.set_text(str(fmt.format(part.model.get_value(part.selected_row, 92))))
        part.txtOperCurrent.set_text(str(fmt.format(part.model.get_value(part.selected_row, 62))))
        part.txtCycleRate.set_text(str(fmt.format(part.model.get_value(part.selected_row, 19))))
        part.cmbForm.set_active(int(part.model.get_value(part.selected_row, 28)))
        part.cmbRating.set_active(int(part.model.get_value(part.selected_row, 96)))
        part.cmbApplication.set_active(int(part.model.get_value(part.selected_row, 5)))
        part.cmbConstruction.set_active(int(part.model.get_value(part.selected_row, 16)))
        if (int(part.model.get_value(part.selected_row, 85)) <= 0):
            part.txtCommercialPiQ.set_text(str(part.model.get_value(part.selected_row, 79)))
        else:
            part.txtCommercialPiQ.set_text("0.0")

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        part.txtLambdaB.set_text(str(fmt.format(part.model.get_value(part.selected_row, 46))))
        part.txtPiL.set_text(str(fmt.format(part.model.get_value(part.selected_row, 76))))
        part.txtPiC.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 69))))
        part.txtPiCYC.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 71))))
        part.txtPiF.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 74))))
        part.txtPiQ.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 79))))
        part.txtPiE.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 72))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Mechanical Relay Component Class
        ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        # Update the Component object property and the Parts List treeview.
        part._calc_data[_index_] = int(idx)
        model.set_value(row, _index_, int(idx))

        if(_index_ == 5):                       # Application
            idx2 = part.cmbRating.get_active()
            part.cmbConstruction.get_model().clear()
            for i in range(len(self._construction[idx2 - 1][idx - 1])):
                part.cmbConstruction.insert_text(i, self._construction[idx2 - 1][idx - 1][i])

        elif(_index_ == 85):                    # Quality
            if(part.txtCommercialPiQ.get_text() == ""):
                CpiQ = 0.0
            else:
                CpiQ = float(part.txtCommercialPiQ.get_text())

            # Use this value for piQ if not being over-ridden.
            if(CpiQ <= 0.0):
                part._calc_data[79] = self._piQ[idx - 1]
                model.set_value(row, 79, part._calc_data[79])

        elif(_index_ == 96):                    # Contact rating
            part.cmbApplication.get_model().clear()
            for i in range(len(self._application[idx - 1])):
                part.cmbApplication.insert_text(i, self._application[idx - 1][i])

        return False

    def entry_callback(self, entry, event, part, convert, _index_):
        """
        Callback function for handling Mechanical Relay Component Class
        Entry changes.

        Keyword Arguments:
        entry   -- the entry widget calling this function.
        event   -- the event that triggered calling this function.
        part    -- the RelKit COMPONENT object.
        convert -- the data type to convert the entry contents to.
        _index_ -- the position in the Component property array
                   associated with the data from the entry that called
                   this function.
        """

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        # Update the Component object property.
        if(convert == "text"):
            part._calc_data[_index_] = entry.get_text()
            model.set_value(row, _index_, entry.get_text())

        elif(convert == "int"):
            part._calc_data[_index_] = int(entry.get_text())
            model.set_value(row, _index_, int(entry.get_text()))

        elif(convert == "float"):
            part._calc_data[_index_] = float(entry.get_text())
            model.set_value(row, _index_, float(entry.get_text()))

        # Commercial PiQ entry called the function.
        if(_index_ == 79):
            CpiQ = float(entry.get_text())

            # Use this value for piQ if it is greater than zero.
            if(CpiQ > 0):
                part._calc_data[79] = CpiQ
                model.set_value(row, 79, CpiQ)

        if(self._ready):
            part.calculate()

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Mechanical Relay Component Class.

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
        Aidx = partmodel.get_value(partrow, 5)      # Application index
        Cidx = partmodel.get_value(partrow, 16)     # Construction index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Ridx = partmodel.get_value(partrow, 96)     # Rating index
        Eidx = systemmodel.get_value(systemrow, 22) # Environment index

        if(Ridx == 1):
            if(Cidx == 2):
                Sidx = 3
            else:
                Sidx = 0
        elif(Ridx == 2):
            if(Aidx == 2):
                if(Cidx == 4):
                    Sidx = 2
                elif(Cidx == 5):
                    Sidx = 5
                else:
                    Sidx = 0
            elif(Aidx == 3):
                if(Cidx == 2):
                    Sidx = 5
                else:
                    Sidx = 0
            elif(Aidx == 4):
                Sidx = 3
            elif(Aidx == 5):
                if(Cidx == 3):
                    Sidx = 3
                else:
                    Sidx = 0
            elif(Aidx == 6):
                Sidx = 4
            elif(Aidx == 8):
                if(Cidx == 2 or Cidx == 3):
                    Sidx = 2
                else:
                    Sidx = 0
            else:
                Sidx = 0
        elif(Ridx == 3):
            if(Aidx == 2):
                if(Cidx == 4 or Cidx == 5):
                    Sidx = 2
                else:
                    Sidx = 0
            else:
                Sidx = 0
        elif(Ridx == 4):
            if(Cidx == 2):
                Sidx = 2
            else:
                Sidx = 0
        else:
            Sidx = 0

        _hrmodel['lambdab'] = self._lambdab_count[Sidx][Eidx - 1]

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
        the Mechanical Relay Component Class.

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
        _hrmodel['equation'] = "lambdab * piL * piC * piCYC * piF * piQ * piE"

        # Retrieve hazard rate inputs.
        Cyc = partmodel.get_value(partrow, 19)
        Tamb = partmodel.get_value(partrow, 37)
        Ioper = partmodel.get_value(partrow, 62)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Irated = partmodel.get_value(partrow, 92)

        # Base hazard rate.
        idx = partmodel.get_value(partrow, 38)
        if(idx == 1):                           # 85C
            Tref = 352.0
            K1 = 0.00555
            K2 = 15.7
        elif(idx == 2):                         # 125C
            Tref = 377.0
            K1 = 0.0054
            K2 = 10.4
        else:                                   # Default
            Tref = 352.0
            K1 = 0.00555
            K2 = 15.7

        _hrmodel['lambdab'] = K1 * exp(((Tamb + 273) / Tref)**K2)

        # Load stress correction factor.
        idx = partmodel.get_value(partrow, 30)
        S = Ioper / Irated
        if(idx == 1):                           # Resistive
            K = 0.8
        elif(idx == 2):                         # Inductive
            K = 0.4
        elif(idx == 3):                         # Lamp
            K = 0.2
        else:                                   # Default
            K = 0.2

        _hrmodel['piL'] = exp(S / K)**2

        # Contact form correction factor.
        idx = partmodel.get_value(partrow, 28)
        _hrmodel['piC'] = self._piC[idx - 1]

        # Cycling rate correction factor.
        idx = partmodel.get_value(partrow, 85)
        if(idx == 8):                           # Non MIL-SPEC
            if(Cyc >= 1000):
                _hrmodel['piCYC'] = (Cyc / 100.0)**2.0
            elif(Cyc >= 10 and Cyc < 1000.0):
                _hrmodel['piCYC'] = Cyc / 10.0
            else:
                _hrmodel['piCYC'] = 1.0
        else:
            if(Cyc >= 1.0):
                _hrmodel['piCYC'] = Cyc / 10.0
            else:
                _hrmodel['piCYC'] = 1.0

        # Application and construction correction factor.
        _hrmodel['piF'] = 1.0
        idx2 = partmodel.get_value(partrow, 96) # Contact rating
        idx3 = partmodel.get_value(partrow, 5)  # Application
        idx4 = partmodel.get_value(partrow, 16) # Construction
        if(idx2 == 1):                          # Signal Current
            if(idx3 == 1):                      # Dry Contact
                if(idx4 == 1):                  # Long Armature
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 8.0
                    else:
                        _hrmodel['piF'] = 4.0
                elif(idx4 == 2):                # Dry Reed
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 18.0
                    else:
                        _hrmodel['piF'] = 6.0
                elif(idx4 == 3):                # Mercury Wetted
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 3.0
                    else:
                        _hrmodel['piF'] = 1.0
                elif(idx4 == 4):                # Magnetic Latching
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 8.0
                    else:
                        _hrmodel['piF'] = 4.0
                elif(idx4 == 5):                # Balanced Armature
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 14.0
                    else:
                        _hrmodel['piF'] = 7.0
                elif(idx4 == 6):                # Solenoid
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 4.0
                    else:
                        _hrmodel['piF'] = 7.0
        elif(idx2 == 2):                        # 0-5 Amp
            if(idx3 == 1):                      # General Purpose
                if(idx4 == 1):                  # Long Armature
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 6.0
                    else:
                        _hrmodel['piF'] = 3.0
                elif(idx4 == 2):                # Balanced Armature
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 10.0
                    else:
                        _hrmodel['piF'] = 5.0
                elif(idx4 == 3):                # Solenoid
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 12.0
                    else:
                        _hrmodel['piF'] = 6.0
            elif(idx3 == 2):                    # Sensitive
                if(idx4 == 1):                  # Long Armature
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 10.0
                    else:
                        _hrmodel['piF'] = 5.0
                elif(idx4 == 2):                # Short Armature
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 10.0
                    else:
                        _hrmodel['piF'] = 5.0
                elif(idx4 == 3):                # Mercury Wetted
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 6.0
                    else:
                        _hrmodel['piF'] = 2.0
                elif(idx4 == 4):                # Magnetic Latching
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 12.0
                    else:
                        _hrmodel['piF'] = 6.0
                elif(idx4 == 5):                # Meter Movement
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 100.0
                    else:
                        _hrmodel['piF'] = 100.0
                elif(idx4 == 6):                # Balanced Armature
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 20.0
                    else:
                        _hrmodel['piF'] = 10.0
            elif(idx3 == 3):                    # Polarized
                if(idx4 == 1):                  # Short Armature
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 20.0
                    else:
                        _hrmodel['piF'] = 10.0
                elif(idx4 == 2):                # Meter Movement
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 100.0
                    else:
                        _hrmodel['piF'] = 100.0
            elif(idx3 == 4):                    # Vibrating Reed
                if(idx4 == 1):                  # Dry Reed
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 12.0
                    else:
                        _hrmodel['piF'] = 6.0
                elif(idx4 == 2):                # Mecury Wetted
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 3.0
                    else:
                        _hrmodel['piF'] = 1.0
            elif(idx3 == 5):                    # High Speed
                if(idx4 == 1):                  # Balanced Armature
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 0.0
                    else:
                        _hrmodel['piF'] = 25.0
                elif(idx4 == 2):                # Short Armature
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 0.0
                    else:
                        _hrmodel['piF'] = 25.0
                elif(idx4 == 3):                # Dry Reed
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 0.0
                    else:
                        _hrmodel['piF'] = 6.0
            elif(idx3 == 6):                    # Thermal Time Delay
                if(idx4 == 1):                  # Bimetal
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 20.0
                    else:
                        _hrmodel['piF'] = 10.0
            elif(idx3 == 7):                    # Electronic Time Delay
                if(idx == 8):                   # Non MIL-SPEC
                    _hrmodel['piF'] = 12.0
                else:
                    _hrmodel['piF'] = 9.0
            elif(idx3 == 8):                    # Magnetic Latching
                if(idx4 == 1):                  # Dry Reed
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 20.0
                    else:
                        _hrmodel['piF'] = 10.0
                elif(idx4 == 2):                # Mercury Wetted
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 10.0
                    else:
                        _hrmodel['piF'] = 5.0
                elif(idx4 == 3):                # Balanced Armature
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 10.0
                    else:
                        _hrmodel['piF'] = 5.0
        elif(idx2 == 3):                        # 5-20 Amp
            if(idx3 == 1):                      # High Voltage
                if(idx4 == 1):                  # Vacuum, Glass
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 40.0
                    else:
                        _hrmodel['piF'] = 20.0
                elif(idx4 == 2):                # Vacuum, Ceramic
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 10.0
                    else:
                        _hrmodel['piF'] = 5.0
            elif(idx3 == 2):                    # Medium Power
                if(idx4 == 1):                  # Long Armature
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 6.0
                    else:
                        _hrmodel['piF'] = 3.0
                elif(idx4 == 2):                # Short Armature
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 6.0
                    else:
                        _hrmodel['piF'] = 3.0
                elif(idx4 == 3):                # Mercury Wetted
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 3.0
                    else:
                        _hrmodel['piF'] = 1.0
                elif(idx4 == 4):                # Magnetic Latching
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 6.0
                    else:
                        _hrmodel['piF'] = 2.0
                elif(idx4 == 5):                # Mechanical Latching
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 6.0
                    else:
                        _hrmodel['piF'] = 3.0
                elif(idx4 == 6):                # Balanced Armature
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 6.0
                    else:
                        _hrmodel['piF'] = 2.0
                elif(idx4 == 7):                # Solenoid
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 6.0
                    else:
                        _hrmodel['piF'] = 2.0
        elif(idx2 == 4):                        # 20-600 Amp
            if(idx3 == 1):                      # Contactor
                if(idx4 == 1):                  # Short Armature
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 14.0
                    else:
                        _hrmodel['piF'] = 7.0
                elif(idx4 == 2):                # Mechanical Latching
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 24.0
                    else:
                        _hrmodel['piF'] = 12.0
                elif(idx4 == 3):                # Balanced Armature
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 20.0
                    else:
                        _hrmodel['piF'] = 10.0
                elif(idx4 == 4):                # Solenoid
                    if(idx == 8):               # Non MIL-SPEC
                        _hrmodel['piF'] = 10.0
                    else:
                        _hrmodel['piF'] = 5.0
        else:
            _hrmodel['piF'] = 1.0

        # Environmental correction factor.
        idx2 = systemmodel.get_value(systemrow, 22)
        if(idx == 8):                           # Non MIL-SPEC
            _hrmodel['piE'] = self._piE[1][idx2 - 1]
        else:
            _hrmodel['piE'] = self._piE[0][idx2 - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 69, _hrmodel['piC'])
        partmodel.set_value(partrow, 71, _hrmodel['piCYC'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 74, _hrmodel['piF'])
        partmodel.set_value(partrow, 76, _hrmodel['piL'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

class SolidState:
    """
    Solid State Relay Component Class.
    Covers specifications MIL-R-28750 and MIL-R-83726.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 13.2
    """

    _quality = ["", "MIL-SPEC", "Lower"]
    _type = ["", "Solid State", "Solid State Time Delay", "Hybrid"]

    def __init__(self):
        """ Initializes the Solid State Relay Component Class. """

        self._ready = False

        self._in_labels = []
        self._out_labels = []

        self.category = 6                       # Category in reliafreecom database.
        self.subcategory = 65                   # Subcategory in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 3.0, 12.0, 6.0, 17.0, 12.0, 19.0, 21.0, 32.0, 23.0,
                     0.4, 12.0, 33.0, 590.0]
        self._piQ = [1.0, 4.0]
        self._lambdab_count = [[0.40, 1.2, 4.8, 2.4, 6.8, 4.8, 7.6, 8.4, 13.0, 9.2, 0.16, 4.8, 13.0, 240.0],
                               [0.40, 1.2, 4.8, 2.4, 6.8, 4.8, 7.6, 8.4, 13.0, 9.2, 0.16, 4.8, 13.0, 240.0],
                               [0.50, 1.5, 6.0, 3.0, 8.5, 5.0, 9.5, 11.0, 16.0, 12.0, 0.20, 5.0, 17.0, 300.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        # Label text for input data.
        self._in_labels.append(u"Quality:")
        self._in_labels.append(u"\u03C0<sub>Q</sub> Override:")
        self._in_labels.append(u"Relay Type:")

        # Label text for output data.
        self._out_labels.append(u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>")
        self._out_labels.append(u"\u03BB<sub>b</sub>:")
        self._out_labels.append(u"\u03C0<sub>Q</sub>:")
        self._out_labels.append(u"\u03C0<sub>E</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Solid State Relay Component
        Class prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        entry_width = int((int(part.fmt) + 5) * 8)

        # Get the list of widgets already on the layout.
        # Check each child widget's name.  If it is IC,
        # then it needs to be removed before placing new
        # widgets.
        chwidgets = layout.get_children()
        for i in range(len(chwidgets)):
            if(chwidgets[i].get_name() == "TRANSIENT"):
                layout.remove(chwidgets[i])

        # Create and place all the labels for the inputs.
        y_pos = 365
        numlabels = len(self._in_labels)
        for i in range(numlabels):
            label = _widg.make_label(self._in_labels[i])
            layout.put(label, 5, (i * 30 + y_pos))

        part.cmbQuality = _widg.make_combo(simple=True)
        for i in range(len(self._quality)):
            part.cmbQuality.insert_text(i, self._quality[i])
        part.cmbQuality.connect("changed",
                                self.combo_callback,
                                part, 85)
        layout.put(part.cmbQuality, x_pos, y_pos)
        y_pos += 30

        part.txtCommercialPiQ = _widg.make_entry(_width_=entry_width)
        part.txtCommercialPiQ.connect("focus-out-event",
                                      self.entry_callback,
                                      part, "float", 79)
        layout.put(part.txtCommercialPiQ, x_pos, y_pos)
        y_pos += 30

        # Create and populate the relay type combobox.  We store this in the
        # construction id field in the program database.
        part.cmbType = _widg.make_combo(simple=True)
        for i in range(len(self._type)):
            part.cmbType.insert_text(i, self._type[i])
        part.cmbType.connect("changed",
                             self.combo_callback,
                             part, 16)
        layout.put(part.cmbType, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Solid State Relay Component Class calculation
        results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        entry_width = int((int(part.fmt) + 5) * 8)

        # Get the list of widgets already on the layout.
        # Check each child widget's name.  If it is IC,
        # then it needs to be removed before placing new
        # widgets.
        chwidgets = layout.get_children()
        for i in range(len(chwidgets)):
            if(chwidgets[i].get_name() == "TRANSIENT"):
                layout.remove(chwidgets[i])

        # Create and place all the labels.
        numlabels = len(self._out_labels)
        for i in range(numlabels):
            if(i == 2):
                label = _widg.make_label(self._out_labels[i], width=400)
                llayout = label.get_layout()
                llayout.set_alignment(pango.ALIGN_CENTER)
                label.show_all()
            else:
                label = _widg.make_label(self._out_labels[i])
            layout.put(label, 5, (i * 30 + y_pos))

        y_pos += 30

        # Create the Temperature Rise results entry.
        #part.txtTRise = _widg.make_entry(editable=False, bold=True)
        #part.txtTRise.set_name("TRANSIENT")
        #layout.put(part.txtTRise, 155, y_pos)
        #y_pos += 30

        # Create the Junction Temperature results entry.
        #part.txtTJunc = _widg.make_entry(editable=False, bold=True)
        #part.txtTJunc.set_name("TRANSIENT")
        #layout.put(part.txtTJunc, 155, y_pos)
        #y_pos += 30

        part.txtLambdaB = _widg.make_entry(_width_=entry_width,
                                           editable=False, bold=True)
        layout.put(part.txtLambdaB, x_pos, y_pos)
        y_pos += 30

        part.txtPiQ = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiQ, x_pos, y_pos)
        y_pos += 30

        part.txtPiE = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiE, x_pos, y_pos)

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

        part.cmbQuality.set_active(int(part.model.get_value(part.selected_row, 85)))
        part.cmbType.set_active(int(part.model.get_value(part.selected_row, 16)))
        if (int(part.model.get_value(part.selected_row, 85)) <= 0):
            part.txtCommercialPiQ.set_text(str(fmt.format(part.model.get_value(part.selected_row, 79))))
        else:
            part.txtCommercialPiQ.set_text("0.0")

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        part.txtLambdaB.set_text(str(fmt.format(part.model.get_value(part.selected_row, 46))))
        part.txtPiQ.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 79))))
        part.txtPiE.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 72))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Solid State Relay Component Class
        ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        # Update the Component object property and the Parts List treeview.
        part._calc_data[_index_] = int(idx)
        model.set_value(row, _index_, int(idx))

        if(_index_ == 85):                      # Quality
            if(part.txtCommercialPiQ.get_text() == ""):
                CpiQ = 0.0
            else:
                CpiQ = float(part.txtCommercialPiQ.get_text())

            # Use this value for piQ if not being over-ridden.
            if(CpiQ <= 0.0):
                part._calc_data[79] = self._piQ[idx - 1]
                model.set_value(row, 79, part._calc_data[79])

        return False

    def entry_callback(self, entry, event, part, convert, _index_):
        """
        Callback function for handling Solid State Relay Component Class
        Entry changes.

        Keyword Arguments:
        entry   -- the entry widget calling this function.
        event   -- the event that triggered calling this function.
        part    -- the RelKit COMPONENT object.
        convert -- the data type to convert the entry contents to.
        _index_ -- the position in the Component property array
                   associated with the data from the entry that called
                   this function.
        """

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        # Update the Component object property.
        if(convert == "text"):
            part._calc_data[_index_] = entry.get_text()
            model.set_value(row, _index_, entry.get_text())

        elif(convert == "int"):
            part._calc_data[_index_] = int(entry.get_text())
            model.set_value(row, _index_, int(entry.get_text()))

        elif(convert == "float"):
            part._calc_data[_index_] = float(entry.get_text())
            model.set_value(row, _index_, float(entry.get_text()))

        # Commercial PiQ entry called the function.
        if(_index_ == 79):
            CpiQ = float(entry.get_text())

            # Use this value for piQ if it is greater than zero.
            if(CpiQ > 0):
                part._calc_data[79] = CpiQ
                model.set_value(row, 79, CpiQ)

        if(self._ready):
            part.calculate()

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Solid State Component Class.

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
        Cidx = partmodel.get_value(partrow, 16)         # Construction (type) index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

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
        the Solid State Relay Component Class.

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
        _hrmodel['equation'] = "lambdab * piQ * piE"

        # Retrieve hazard rate inputs.
        Cyc = partmodel.get_value(partrow, 19)
        Tamb = partmodel.get_value(partrow, 37)
        Ioper = partmodel.get_value(partrow, 62)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Irated = partmodel.get_value(partrow, 92)

        # Base hazard rate.
        idx = partmodel.get_value(partrow, 16)
        if(idx == 1):                           # Solid State
            _hrmodel['lambdab'] = 0.40
        elif(idx == 2):                         # Solid State Time Delay
            _hrmodel['lambdab'] = 0.50
        elif(idx == 3):                         # Hybrid
            _hrmodel['lambdab'] = 0.50

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
