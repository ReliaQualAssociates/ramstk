#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       switch.py is part of The ReliaFree Project
#
#       Copyright (C) 2007-2012 Andrew "Weibullguy" Rowland <darowland@ieee.org>
#
# All rights reserved.

import pango

try:
    import reliafree.widgets as _widg
except:
    import widgets as _widg

class Switch:

    """ Switches meta class.

        Hazard Rate Models:
            1. MIL-HDBK-217F, section 14.

    """

    def __init__(self):

        """ Initializes the Switches Component Class. """

        self._ready = False

        self._in_labels = []
        self._out_labels = []

        self.category = 7                       # Category in reliafreecom database.

        # Label text for input data.
        self._in_labels.append(u"Quality:")
        self._in_labels.append(u"\u03C0<sub>Q</sub> Override:")
        self._in_labels.append(u"Application:")
        self._in_labels.append(u"Cycling Rate (cycles/hour):")
        self._in_labels.append(u"Rated Current (A):")
        self._in_labels.append(u"Operating Current (A):")

        # Label text for output data.
        self._out_labels.append("")
        self._out_labels.append(u"\u03BB<sub>b</sub>:")
        self._out_labels.append(u"\u03C0<sub>E</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):

        """ Populates the ReliaFree Workbook calculation input tab with the
            widgets needed to select inputs for Switches Component Class
            prediction calculations.

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

        part.txtCycleRate = _widg.make_entry(_width_=entry_width)
        part.txtCycleRate.connect("focus-out-event",
                                  self.entry_callback,
                                  part, "float", 19)
        layout.put(part.txtCycleRate, x_pos, y_pos)
        y_pos += 30

        part.txtCurrentRated = _widg.make_entry(_width_=entry_width)
        part.txtCurrentRated.connect("focus-out-event",
                                     self.entry_callback,
                                     part, "float", 92)
        layout.put(part.txtCurrentRated, x_pos, y_pos)
        y_pos += 30

        part.txtCurrentOper = _widg.make_entry(_width_=entry_width)
        part.txtCurrentOper.connect("focus-out-event",
                                    self.entry_callback,
                                    part, "float", 62)
        layout.put(part.txtCurrentOper, x_pos, y_pos)
        y_pos += 30

        layout.show_all()

        return(y_pos)

    def assessment_results_create(self, part, layout, x_pos, y_pos):

        """ Populates the ReliaFree Workbook calculation results tab with the
            widgets to display Switches Component Class calculation results.

            Keyword Arguments:
            part   -- the ReliaFree COMPONENT object.
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

        part.txtLambdaB = _widg.make_entry(_width_=entry_width,
                                           editable=False, bold=True)
        layout.put(part.txtLambdaB, x_pos, y_pos)
        y_pos += 30

        part.txtPiE = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiE, x_pos, y_pos)
        y_pos += 30

        layout.show_all()

        self._ready = True

        return(y_pos)

    def assessment_inputs_load(self, part):

        """ Loads the ReliaFree Workbook calculation input widgets with
            calculation input information.

            Keyword Arguments:
            part -- the ReliaFree COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        part.cmbQuality.set_active(int(part.model.get_value(part.selected_row, 85)))
        part.cmbApplication.set_active(int(part.model.get_value(part.selected_row, 5)))
        part.txtCycleRate.set_text(str(fmt.format(part.model.get_value(part.selected_row, 19))))
        part.txtCurrentRated.set_text(str(fmt.format(part.model.get_value(part.selected_row, 92))))
        part.txtCurrentOper.set_text(str(fmt.format(part.model.get_value(part.selected_row, 62))))
        if (int(part.model.get_value(part.selected_row, 85)) <= 0):
            part.txtCommercialPiQ.set_text(str(fmt.format(part.model.get_value(part.selected_row, 79))))
        else:
            part.txtCommercialPiQ.set_text("0.0")

        return False

    def assessment_results_load(self, part):

        """ Loads the ReliaFree Workbook calculation results widgets with
            calculation results.

            Keyword Arguments:
            part -- the ReliaFree COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        part.txtLambdaB.set_text(str(fmt.format(part.model.get_value(part.selected_row, 46))))
        part.txtPiE.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 72))))

        return False

    def combo_callback(self, combo, part, _index_):

        """ Callback function for handling Switches Component Class ComboBox
            changes.

            Keyword Arguments:
              combo -- the combobox widget calling this function.
               part -- the ReliaFree COMPONENT object.
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

        if(self._ready):
            part.calculate()

        return False

    def entry_callback(self, entry, event, part, convert, _index_):

        """ Callback function for handling Switches Component Class Entry
            changes.

            Keyword Arguments:
              entry -- the entry widget calling this function.
              event -- the event that triggered calling this function.
               part -- the ReliaFree COMPONENT object.
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

        if(self._ready):
            part.calculate()

        return False
