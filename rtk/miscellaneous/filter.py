#!/usr/bin/env python
""" This is the electronic filter class. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       filter.py is part of The RTK Project
#
# All rights reserved.

import pango

try:
    import relkit.calculations as _calc
    import relkit.widgets as _widg
except ImportError:
    import calculations as _calc
    import widgets as _widg


class Filter:
    """
    Filter Component Class.
    Covers specifications MIL-F-15733 and MIL-F-18327.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 21.1
    """

    _construction = [[u"", u"Ceramic-Ferrite Construction",
                      u"Discrete LC Components"],
                     [u"", u"Discrete LC Components",
                      u"Discrete LC and Crystal Components"]]
    _quality = [u"", u"MIL-SPEC", u"Lower"]
    _specification = [u"", u"MIL-F-15733", u"MIL-F-18327"]

    def __init__(self):
        """ Initializes the Filter Component Class. """

        self._ready = False

        self._in_labels = []
        self._out_labels = []

        self.category = 10                      # Category in relkitcom database.
        self.subcategory = 83                   # Subcategory in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 6.0, 4.0, 9.0, 7.0, 9.0, 11.0, 13.0, 11.0, 0.8,
                     7.0, 15.0, 120.0]
        self._lambdab = [0.022, 0.12, 0.12, 0.27]
        self._lambdab_count = [[3.9, 7.8, 12.0, 12.0, 16.0, 16.0, 16.0, 19.0,
                                23.0, 19.0, 2.7, 16.0, 23.0, 100.0],
                               [13.0, 26.0, 38.0, 38.0, 51.0, 51.0, 51.0, 64.0,
                                77.0, 64.0, 9.0, 51.0, 77.0, 350.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Quality:")
        self._in_labels.append(u"Specification:")
        self._in_labels.append(u"Construction:")

        self._out_labels.append(u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>")
        self._out_labels.append(u"\u03BB<sub>b</sub>:")
        self._out_labels.append(u"\u03C0<sub>Q</sub>:")
        self._out_labels.append(u"\u03C0<sub>E</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Lamp Component
        Class prediction calculations.

        Keyword Arguments:
        part   -- the RTK COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        entry_width = int((int(part.fmt) + 5) * 8)

        # Get the list of widgets already on the layout.
        # Check each child widget's name.  If it is LAMP,
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

        # Create hte Utilization ComboBox.  We store the index value in the
        # cycles_id field in the program database.
        part.cmbUtilization = _widg.make_combo(simple=True)
        for i in range(len(self._utilization)):
            part.cmbUtilization.insert_text(i, self._utilization[i])
        part.cmbUtilization.connect("changed",
                                    self.combo_callback,
                                    part, 18)
        layout.put(part.cmbUtilization, x_pos, y_pos)
        y_pos += 30

        part.cmbApplication = _widg.make_combo(simple=True)
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])
        part.cmbApplication.connect("changed",
                                    self.combo_callback,
                                    part, 5)
        layout.put(part.cmbApplication, x_pos, y_pos)
        y_pos += 30

        part.txtVoltage = _widg.make_entry(width=entry_width)
        part.txtVoltage.connect("focus-out-event",
                                self.entry_callback,
                                part, "float", 94)
        layout.put(part.txtVoltage, x_pos, y_pos)

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Lamp Component Class calculation
        results.

        Keyword Arguments:
        part   -- the RTK COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        entry_width = int((int(part.fmt) + 5) * 8)

        # Get the list of widgets already on the layout.
        # Check each child widget's name.  If it is LAMP,
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
        part.txtLambdaB = _widg.make_entry(width=entry_width,
                                           editable=False, bold=True)
        layout.put(part.txtLambdaB, x_pos, y_pos)
        y_pos += 30

        part.txtPiU = _widg.make_entry(width=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiU, x_pos, y_pos)
        y_pos += 30

        part.txtPiA = _widg.make_entry(width=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiA, x_pos, y_pos)
        y_pos += 30

        part.txtPiE = _widg.make_entry(width=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiE, x_pos, y_pos)

        layout.show_all()

        self._ready = True

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RTK COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        part.cmbUtilization.set_active(int(part.model.get_value(part.selected_row, 18)))
        part.cmbApplication.set_active(int(part.model.get_value(part.selected_row, 5)))
        part.txtVoltage.set_text(str(fmt.format(part.model.get_value(part.selected_row, 94))))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RTK COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        part.txtLambdaB.set_text(str(fmt.format(part.model.get_value(part.selected_row, 46))))
        part.txtPiA.set_text(str(fmt.format(part.model.get_value(part.selected_row, 68))))
        part.txtPiE.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 72))))
        part.txtPiU.set_text(str(fmt.format(part.model.get_value(part.selected_row, 82))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Lamp Component Class ComboBox
        changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RTK COMPONENT object.
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
        Callback function for handling Crystal Component Class
        Entry changes.

        Keyword Arguments:
        entry   -- the entry widget calling this function.
        event   -- the event that triggered calling this function.
        part    -- the RTK COMPONENT object.
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
        Filter Component Class.

        Keyword Arguments:
        partmodel   -- the RTK winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RTK HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RTK HARWARE
                       object gtk.TreeModel.
        """

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab"

        # Retrieve hazard rate inputs.
        Aidx = partmodel.get_value(partrow, 5)          # Configuration index
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
        the Filter Component Class.

        Keyword Arguments:
        partmodel   -- the RTK winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RTK HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RTK HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piU * piA * piE"

        # Retrieve hazard rate inputs.
        Aidx = partmodel.get_value(partrow, 5)  # Application index
        Uidx = partmodel.get_value(partrow, 18) # Utilization index
        Vr = partmodel.get_value(partrow, 94)   # Rated voltage
        Qidx = partmodel.get_value(partrow, 85)

        # Base hazard rate.
        _hrmodel['lambdab'] = 0.074 * Vr**1.29

        # Utilization correction factor.
        _hrmodel['piU']= self._piU[Uidx - 1]

        # Application correction factor.
        _hrmodel['piA'] = self._piA[Aidx - 1]

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 68, _hrmodel['piA'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 82, _hrmodel['piU'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
