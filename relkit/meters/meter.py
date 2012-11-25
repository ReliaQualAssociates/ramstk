#!/usr/bin/env python
""" These are the meter classes. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2012 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       meter.py is part of The RelKit Project
#
# All rights reserved.

import pango

try:
    import reliafree.calculations as _calc
    import reliafree.widgets as _widg
except ImportError:
    import calculations as _calc
    import widgets as _widg


class ElapsedTime:
    """
    Elapsed Time Meter Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, sections 12.3.
    """

    _type = [u"", u"A.C.", u"Inverter Driven", u"Cummutator D.C."]

    def __init__(self):
        """ Initializes the Elapsed Time Meter Component Class. """

        self._ready = False

        self._in_labels = []
        self._out_labels = []

        self.category = 9                   # Category in reliafreecom database.
        self.subcategory = 77               # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._lambdab = [20.0, 30.0, 80.0]
        self._piE = [1.0, 2.0, 12.0, 7.0, 18.0, 5.0, 8.0, 16.0, 25.0, 26.0,
                     0.5, 14.0, 38.0, 0.0]
        self._lambdab_count = [[10.0, 20.0, 120.0, 70.0, 180.0, 50.0, 80.0,
                                160.0, 250.0, 260.0, 5.0, 140.0, 380.0, 0.0],
                               [15.0, 30.0, 180.0, 105.0, 270.0, 75.0, 120.0,
                                240.0, 375.0, 390.0, 7.5, 210.0, 570.0, 0.0],
                               [40.0, 80.0, 480.0, 280.0, 720.0, 200.0, 320.0,
                                640.0, 1000.0, 1040.0, 20.0, 560.0, 1520.0,
                                0.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        # Label text for input data.
        self._in_labels.append(u"Type:")
        self._in_labels.append(u"Operating Temperature (\u00B0C):")
        self._in_labels.append(u"Rated Temperature (\u00B0C):")

        # Label text for output data.
        self._out_labels.append(u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>E</sub></span>")
        self._out_labels.append(u"\u03BB<sub>b</sub>:")
        self._out_labels.append(u"\u03C0<sub>T</sub>:")
        self._out_labels.append(u"\u03C0<sub>E</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the ReliaFree Workbook calculation input tab with the
        widgets needed to select inputs for Elapsed Time Meter Component
        Class prediction calculations.

        Keyword Arguments:
        part   -- the ReliaFree COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        entry_width = int((int(part.fmt) + 5) * 8)

        # Get the list of widgets already on the layout.
        # Check each child widget's name.  If it is SWITCH,
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

        # Create the Meter Type ComboBox.  We store the index in the
        # technology_id filed in the program database.
        part.cmbType = _widg.make_combo(simple=True)
        for i in range(len(self._type)):
            part.cmbType.insert_text(i, self._type[i])
        part.cmbType.connect("changed",
                             self.combo_callback,
                             part, 104)
        layout.put(part.cmbType, x_pos, y_pos)
        y_pos += 30

        part.txtOperatingTemp = _widg.make_entry(_width_=entry_width)
        part.txtOperatingTemp.connect("focus-out-event",
                                      self.entry_callback,
                                      part, "float", 105)
        layout.put(part.txtOperatingTemp, x_pos, y_pos)
        y_pos += 30

        part.txtRatedTemp = _widg.make_entry(_width_=entry_width)
        part.txtRatedTemp.connect("focus-out-event",
                                  self.entry_callback,
                                  part, "float", 55)
        layout.put(part.txtRatedTemp, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the ReliaFree Workbook calculation results tab with the
        widgets to display Elapsed Time Meter Component Class calculation
        results.

        Keyword Arguments:
        part   -- the ReliaFree COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        entry_width = int((int(part.fmt) + 5) * 8)

        # Get the list of widgets already on the layout.
        # Check each child widget's name.  If it is SWITCH,
        # then it needs to be removed before placing new
        # widgets.
        chwidgets = layout.get_children()
        for i in range(len(chwidgets)):
            if(chwidgets[i].get_name() == "TRANSIENT"):
                layout.remove(chwidgets[i])

        # Create and place all the labels.
        y_pos = 305
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

        part.txtLambdaB = _widg.make_entry(_width_=entry_width,
                                           editable=False, bold=True)
        layout.put(part.txtLambdaB, x_pos, y_pos)
        y_pos += 30

        # Create the piT Entry.  We store this value in the pi_sr field in the
        # program database.
        part.txtPiT = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiT, x_pos, y_pos)
        y_pos += 30

        part.txtPiE = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiE, x_pos, y_pos)
        y_pos += 30

        layout.show_all()

        self._ready = True

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the ReliaFree Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the ReliaFree COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        part.txtRatedTemp.set_text(str(fmt.format(part.model.get_value(part.selected_row, 55))))
        part.cmbType.set_active(int(part.model.get_value(part.selected_row, 104)))
        part.txtOperatingTemp.set_text(str(fmt.format(part.model.get_value(part.selected_row, 105))))

        return False

    def assessment_results_load(self, part):
        """
        Loads the ReliaFree Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the ReliaFree COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        part.txtLambdaB.set_text(str(fmt.format(part.model.get_value(part.selected_row, 46))))
        part.txtPiE.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 72))))
        part.txtPiT.set_text(str(fmt.format(part.model.get_value(part.selected_row, 81))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Elapsed Time Meter Component Class
        ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the ReliaFree COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        # Update the Component object property and the Parts List treeview.
        model.set_value(row, _index_, int(idx))

        return False

    def entry_callback(self, entry, event, part, convert, _index_):
        """
        Callback function for handling Elapsed Time Meter Component Class
        Entry changes.

        Keyword Arguments:
        entry   -- the entry widget calling this function.
        event   -- the event that triggered calling this function.
        part    -- the ReliaFree COMPONENT object.
        convert -- the data type to convert the entry contents to.
        _index_ -- the position in the Component property array
                   associated with the data from the entry that called
                   this function.
        """

        try:
            # Get the Parts List treeview full model and full model iter.
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        # Update the Component object property.
        if(convert == "text"):
            model.set_value(row, _index_, entry.get_text())

        elif(convert == "int"):
            model.set_value(row, _index_, int(entry.get_text()))

        elif(convert == "float"):
            model.set_value(row, _index_, float(entry.get_text()))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Elapsed Time Meter Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab"

        # Retrieve hazard rate inputs.
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
        Tidx = partmodel.get_value(partrow, 104)        # Type index

        _hrmodel['lambdab'] = self._lambdab_count[Tidx - 1][Eidx - 1]

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
        the Elapsed Time Meter Component Class.

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
        _hrmodel['equation'] = "lambdab * piT * piE"

        # Retrieve hazard rate inputs.
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
        Trate = partmodel.get_value(partrow, 55)
        Tidx = partmodel.get_value(partrow, 104)        # Type index
        Toper = partmodel.get_value(partrow, 105)

        # Base hazard rate.
        _hrmodel['lambdab'] = self._lambdab[Tidx - 1]

        # Temperature stress correction factor.
        try:
            S = Toper / Trate
        except:
            S = 1.0

        if(S <= 0.5):
            _hrmodel['piT'] = 0.5
        elif(S > 0.5 and S <= 0.6):
            _hrmodel['piT'] = 0.6
        elif(S > 0.6 and S <= 0.8):
            _hrmodel['piT'] = 0.8
        else:
            _hrmodel['piT'] = 1.0

        # Environmental correction factor.
        _hrmodel['piE'] = self._piE[Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 81, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))
        print lambdap
        return False

class Panel:
    """
    Panel Meter Component Class.
    Covers specifications MIL-M-10304.

    Hazard Rate Models:
        1. MIL-HDBK-217F, sections 18.1.
    """

    _application = [u"", u"Direct Current", u"Alternating Current"]
    _quality = [u"", u"MIL-M-10304", u"Lower"]
    _type = [u"", u"Ammeter", u"Voltmeter", u"Other"]

    def __init__(self):
        """ Initializes the Panel Meter Component Class. """

        self._ready = False

        self._in_labels = []
        self._out_labels = []

        self.category = 9                       # Category in reliafreecom database.
        self.subcategory = 78                   # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piA = [1.0, 1.7]
        self._piE = [1.0, 4.0, 25.0, 12.0, 35.0, 28.0, 42.0, 58.0, 73.0, 60.0,
                     1.1, 60.0, 0.0, 0.0]
        self._piF = [1.0, 1.0, 2.8]
        self._piQ = [1.0, 3.4]
        self._lambdab_count = [[0.09, 0.36, 2.3, 1.1, 3.2, 2.5, 3.8, 5.2, 6.6,
                                5.4, 0.099, 5.4, 0.0, 0.0],
                               [0.15, 0.81, 2.8, 1.8, 5.4, 4.3, 6.4, 8.9, 11.0,
                                9.2, 0.17, 9.2, 0.0, 0.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        # Label text for input data.
        self._in_labels.append(u"Quality:")
        self._in_labels.append(u"\u03C0<sub>Q</sub> Override:")
        self._in_labels.append(u"Application:")
        self._in_labels.append(u"Function:")

        # Label text for output data.
        self._out_labels.append(u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>A</sub>\u03C0<sub>F</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>")
        self._out_labels.append(u"\u03BB<sub>b</sub>:")
        self._out_labels.append(u"\u03C0<sub>A</sub>:")
        self._out_labels.append(u"\u03C0<sub>F</sub>:")
        self._out_labels.append(u"\u03C0<sub>Q</sub>:")
        self._out_labels.append(u"\u03C0<sub>E</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the ReliaFree Workbook calculation input tab with the
        widgets needed to select inputs for Panel Meter Component
        Class prediction calculations.

        Keyword Arguments:
        part   -- the ReliaFree COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        entry_width = int((int(part.fmt) + 5) * 8)

        # Get the list of widgets already on the layout.
        # Check each child widget's name.  If it is SWITCH,
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
        y_pos += 30

        part.txtCommercialPiQ = _widg.make_entry(_width_=entry_width)
        part.txtCommercialPiQ.connect("focus-out-event",
                                      self.entry_callback,
                                      part, "float", 79)
        layout.put(part.txtCommercialPiQ, x_pos, y_pos)
        y_pos += 30

        part.cmbApplication = _widg.make_combo(simple=True)
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])
        part.cmbApplication.connect("changed",
                                    self.combo_callback,
                                    part, 5)
        layout.put(part.cmbApplication, x_pos, y_pos)
        y_pos += 30

        # Create the Meter Type ComboBox.  We store the index in the
        # technology_id filed in the program database.
        part.cmbType = _widg.make_combo(simple=True)
        for i in range(len(self._type)):
            part.cmbType.insert_text(i, self._type[i])
        part.cmbType.connect("changed",
                                self.combo_callback,
                                part, 104)
        layout.put(part.cmbType, x_pos, y_pos)
        y_pos += 30

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the ReliaFree Workbook calculation results tab with the
        widgets to display Panel Meter Component Class calculation
        results.

        Keyword Arguments:
        part   -- the ReliaFree COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        entry_width = int((int(part.fmt) + 5) * 8)

        # Get the list of widgets already on the layout.
        # Check each child widget's name.  If it is SWITCH,
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
        part.txtLambdaB = _widg.make_entry(_width_=entry_width,
                                           editable=False, bold=True)
        layout.put(part.txtLambdaB, x_pos, y_pos)
        y_pos += 30

        part.txtPiA = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiA, x_pos, y_pos)
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
        Loads the ReliaFree Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the ReliaFree COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        part.cmbApplication.set_active(int(part.model.get_value(part.selected_row, 5)))
        part.cmbQuality.set_active(int(part.model.get_value(part.selected_row, 85)))
        part.cmbType.set_active(int(part.model.get_value(part.selected_row, 104)))
        if (int(part.model.get_value(part.selected_row, 85)) <= 0):
            part.txtCommercialPiQ.set_text(str(fmt.format(part.model.get_value(part.selected_row, 79))))
        else:
            part.txtCommercialPiQ.set_text("0.0")

        return False

    def assessment_results_load(self, part):
        """
        Loads the ReliaFree Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the ReliaFree COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        part.txtLambdaB.set_text(str(fmt.format(part.model.get_value(part.selected_row, 46))))
        part.txtPiA.set_text(str(fmt.format(part.model.get_value(part.selected_row, 68))))
        part.txtPiE.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 72))))
        part.txtPiF.set_text(str(fmt.format(part.model.get_value(part.selected_row, 74))))
        part.txtPiQ.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 79))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Panel Meter Component Class ComboBox
        changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the ReliaFree COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        # Update the Component object property and the Parts List treeview.
        model.set_value(row, _index_, int(idx))

        return False

    def entry_callback(self, entry, event, part, convert, _index_):
        """
        Callback function for handling Panel Meter Component Class
        Entry changes.

        Keyword Arguments:
        entry   -- the entry widget calling this function.
        event   -- the event that triggered calling this function.
        part    -- the ReliaFree COMPONENT object.
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
            model.set_value(row, _index_, entry.get_text())
        elif(convert == "int"):
            model.set_value(row, _index_, int(entry.get_text()))

        elif(convert == "float"):
            model.set_value(row, _index_, float(entry.get_text()))

        # Commercial PiQ entry called the function.
        if(_index_ == 79):
            CpiQ = float(entry.get_text())

            # Use this value for piQ if it is greater than zero.
            if(CpiQ > 0):
                model.set_value(row, 79, CpiQ)

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Panel Meter Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

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
        the Panel Meter Component Class.

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
        _hrmodel['equation'] = "lambdab * piA * piF * piQ * piE"

        # Retrieve hazard rate inputs.
        Aidx = partmodel.get_value(partrow, 5)          # Application index
        Qidx = partmodel.get_value(partrow, 85)         # Quality index
        Tidx = partmodel.get_value(partrow, 104)        # Type index
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

        # Base hazard rate.
        _hrmodel['lambdab'] = 0.090

        # Application correction factor.
        _hrmodel['piA'] = self._piA[Aidx - 1]

        # Function correction factor.
        _hrmodel['piF'] = self._piF[Tidx - 1]

        # Quality correction factor.
        _hrmodel['piQ'] = self._piQ[Qidx - 1]

        # Environmental correction factor.
        _hrmodel['piE'] = self._piE[Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 68, _hrmodel['piA'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 74, _hrmodel['piF'])
        partmodel.set_value(partrow, 79, _hrmodel['piQ'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
