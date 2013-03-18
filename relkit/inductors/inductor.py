#!/usr/bin/env python
""" This is the Inductor meta-class. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       inductor.py is part of The RelKit Project
#
# All rights reserved.

import pango

try:
    import reliafree.widgets as _widg
except ImportError:
    import widgets as _widg


class Inductor:
    """
    Inductive Devices meta class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 11.
    """

    def __init__(self):
        """ Initializes the Inductive Devices Component Class. """

        self._ready = False

        self._in_labels = []
        self._out_labels = []

        self.category = 5                   # Category in reliafreecom database.

        # Label text for input data.
        self._in_labels.append(u"Quality:")
        self._in_labels.append(u"\u03C0<sub>Q</sub> Override:")
        self._in_labels.append(u"Insulation Class:")
        self._in_labels.append(u"Power Loss(W):")
        self._in_labels.append(u"Input Power (W):")
        self._in_labels.append(u"Radiating Surface Area (in\u00B2):")
        self._in_labels.append(u"Transformer Weight (lbs):")

        # Label text for output data.
        self._out_labels.append(u"Temp Rise (\u2070C):")
        self._out_labels.append(u"Hot Spot Temp. (\u00B0C):")
        self._out_labels.append("")
        self._out_labels.append(u"\u03BB<sub>b</sub>:")
        self._out_labels.append(u"\u03C0<sub>Q</sub>:")
        self._out_labels.append(u"\u03C0<sub>E</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Inductive Devices Component
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
            label.set_name("TRANSIENT")
            layout.put(label, 5, (i * 30 + y_pos))

        part.cmbQuality = _widg.make_combo(simple=True)
        part.cmbQuality.set_name("TRANSIENT")
        for i in range(len(self._quality)):
            part.cmbQuality.insert_text(i, self._quality[i])
        part.cmbQuality.connect("changed",
                                self.combo_callback,
                                part, 85)
        layout.put(part.cmbQuality, x_pos, y_pos)
        y_pos += 30

        part.txtCommercialPiQ = _widg.make_entry(_width_=entry_width)
        part.txtCommercialPiQ.set_name("TRANSIENT")
        part.txtCommercialPiQ.connect("focus-out-event",
                                      self.entry_callback,
                                      part, "float", 79)
        layout.put(part.txtCommercialPiQ, x_pos, y_pos)
        y_pos += 30

        part.cmbInsulation = _widg.make_combo(simple=True)
        part.cmbInsulation.set_name("TRANSIENT")
        for i in range(len(self._insulation)):
            part.cmbInsulation.insert_text(i, self._insulation[i])
        part.cmbInsulation.connect("changed",
                                   self.combo_callback,
                                   part, 38)
        layout.put(part.cmbInsulation, x_pos, y_pos)
        y_pos += 30

        part.txtOperPwr = _widg.make_entry(_width_=entry_width)
        part.txtOperPwr.set_name("TRANSIENT")
        part.txtOperPwr.connect("focus-out-event",
                                self.entry_callback,
                                part, "float", 64)
        layout.put(part.txtOperPwr, x_pos, y_pos)
        y_pos += 30

        # Create the input power entry.  We store this in the rated power
        # field in the program database.
        part.txtInputPwr = _widg.make_entry(_width_=entry_width)
        part.txtInputPwr.set_name("TRANSIENT")
        part.txtInputPwr.connect("focus-out-event",
                                 self.entry_callback,
                                 part, "float", 93)
        layout.put(part.txtInputPwr, x_pos, y_pos)
        y_pos += 30

        # Create the transformer surface area entry.  We store this in the
        # L1 field in the program database.
        part.txtArea = _widg.make_entry(_width_=entry_width)
        part.txtArea.set_name("TRANSIENT")
        part.txtArea.connect("focus-out-event",
                             self.entry_callback,
                             part, "float", 44)
        layout.put(part.txtArea, x_pos, y_pos)
        y_pos += 30

        # Create the transformer weight entry.  We store this in the L2 field
        # in the program database.
        part.txtWeight = _widg.make_entry(_width_=entry_width)
        part.txtWeight.set_name("TRANSIENT")
        part.txtWeight.connect("focus-out-event",
                               self.entry_callback,
                               part, "float", 45)
        layout.put(part.txtWeight, x_pos, y_pos)
        y_pos += 30

        layout.show_all()

        return(y_pos)

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Inductive Devices Component Class calculation
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
            label.set_name("TRANSIENT")
            layout.put(label, 5, (i * 30 + y_pos))

        part.txtTRise = _widg.make_entry(_width_=entry_width,
                                         editable=False, bold=True)
        part.txtTRise.set_name("TRANSIENT")
        layout.put(part.txtTRise, x_pos, y_pos)
        y_pos += 30

        part.txtTJunc = _widg.make_entry(_width_=entry_width,
                                         editable=False, bold=True)
        part.txtTJunc.set_name("TRANSIENT")
        layout.put(part.txtTJunc, x_pos, y_pos)
        y_pos += 60                         # Increment by 60 to make room to
                                            # display reliability formula.

        part.txtLambdaB = _widg.make_entry(_width_=entry_width,
                                           editable=False, bold=True)
        part.txtLambdaB.set_name("TRANSIENT")
        layout.put(part.txtLambdaB, x_pos, y_pos)
        y_pos += 30

        part.txtPiQ = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        part.txtPiQ.set_name("TRANSIENT")
        layout.put(part.txtPiQ, x_pos, y_pos)
        y_pos += 30

        part.txtPiE = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        part.txtPiE.set_name("TRANSIENT")
        layout.put(part.txtPiE, x_pos, y_pos)
        y_pos += 30

        layout.show_all()

        self._ready = True

        return(y_pos)

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
        part.txtOperPwr.set_text(str(fmt.format(part.model.get_value(part.selected_row, 64))))
        part.txtInputPwr.set_text(str(fmt.format(part.model.get_value(part.selected_row, 93))))
        part.txtArea.set_text(str(fmt.format(part.model.get_value(part.selected_row, 44))))
        part.txtWeight.set_text(str(fmt.format(part.model.get_value(part.selected_row, 45))))

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

        part.txtTRise.set_text(str(fmt.format(part.model.get_value(part.selected_row, 107))))
        part.txtTJunc.set_text(str(fmt.format(part.model.get_value(part.selected_row, 39))))
        part.txtLambdaB.set_text(str(fmt.format(part.model.get_value(part.selected_row, 46))))
        part.txtPiQ.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 79))))
        part.txtPiE.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 72))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Inductive Devices Component Class
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
        model.set_value(row, _index_, int(idx))

        if(_index_ == 85):                  # Quality
            if(part.txtCommercialPiQ.get_text() == ""):
                CpiQ = 0.0
            else:
                CpiQ = float(part.txtCommercialPiQ.get_text())

            # Use this value for piQ if not being over-ridden.
            if(CpiQ <= 0.0):
                model.set_value(row, 79, self._piQ[idx - 1])

        return False

    def entry_callback(self, entry, event, part, convert, _index_):
        """
        Callback function for handling Inductive Device Component Class
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

        # Commercial PiQ entry called the function.
        if(_index_ == 79):
            CpiQ = float(entry.get_text())

            # Use this value for piQ if it is greater than zero.
            if(CpiQ > 0):
                model.set_value(row, 79, CpiQ)

        return False
