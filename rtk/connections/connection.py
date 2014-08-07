#!/usr/bin/env python
""" This is the electrical connection meta-class. """

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       connection.py is part of The RTK Project
#
# All rights reserved.

import locale
import gettext
import pango

try:
    import rtk.configuration as _conf
    import rtk.widgets as _widg
except ImportError:
    import configuration as _conf
    import widgets as _widg

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except ImportError:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Connection(object):
    """
    Connections meta class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, sections 15, 16, and 17.
    """

    def __init__(self):
        """
        Initializes the Connection Class.
        """

        self._ready = False

        self.category = 8                   # Category in the rtkcom database.

        # Label text for input data.
        self._in_labels = [_("Quality:"), (u"\u03C0<sub>Q</sub> Override:")]

        # Label text for output data.
        self._out_labels = [(""), (u"\u03BB<sub>b</sub>:"),
                            (u"\u03C0<sub>E</sub>:")]

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Connections Component Class
        prediction calculations.

        :param rtk.Component part: the current instance of the Component class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._in_labels, layout,
                                             x_pos, y_pos)

        part.cmbQuality = _widg.make_combo(simple=True)
        for i in range(len(self._quality)):
            part.cmbQuality.insert_text(i, self._quality[i])
        part.txtCommercialPiQ = _widg.make_entry()

        layout.put(part.cmbQuality, _x_pos, _y_pos[0])
        layout.put(part.txtCommercialPiQ, _x_pos, _y_pos[1])

        part.txtCommercialPiQ.connect('focus-out-event',
                                      self._callback_entry,
                                      part, 'float', 79)
        part.cmbQuality.connect('changed',
                                self._callback_combo,
                                part, 85)

        layout.show_all()

        return(y_pos)

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with
        calculation input information.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        part.cmbQuality.set_active(int(_model.get_value(_row, 85)))
        if int(_model.get_value(_row, 85)) <= 0:
            _commercial_piq = _model.get_value(_row, 79)
            part.txtCommercialPiQ.set_text(str(fmt.format(_commercial_piq)))
        else:
            part.txtCommercialPiQ.set_text("0.0")

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Connections Component Class calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Create and place all the labels.
        (_x_pos, _y_pos) = _widg.make_labels(self._out_labels[1:],
                                             layout, x_pos, y_pos)
        _x_pos += x_pos
        _x_pos -= 30

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

        part.txtLambdaB = _widg.make_entry(editable=False, bold=True)
        part.txtPiE = _widg.make_entry(editable=False, bold=True)

        layout.put(part.txtLambdaB, x_pos, y_pos[0])
        y_pos += 30

        layout.put(part.txtPiE, x_pos, y_pos[1])
        y_pos += 30

        layout.show_all()

        self._ready = True

        return(y_pos)

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RTK COMPONENT object.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        lambdab = part.model.get_value(part.selected_row, 46)
        pie = part.model.get_value(part.selected_row, 72)
        part.txtLambdaB.set_text(str(fmt.format(lambdab)))
        part.txtPiE.set_text(str('{0:0.2g}'.format(pie)))

        return False

    def _callback_combo(self, combo, part, _index_):
        """
        Callback function for handling Connections Component Class ComboBox
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

        # Update the Parts List.
        model.set_value(row, _index_, int(idx))

        return False

    def _callback_entry(self, entry, event, part, convert, _index_):
        """
        Callback function for handling Connections Component Class
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
            # Get the Parts List treeview full model and full model iter.
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        # Update the Component object property.
        if(convert == 'text'):
            model.set_value(row, _index_, entry.get_text())

        elif(convert == 'int'):
            model.set_value(row, _index_, int(entry.get_text()))

        elif(convert == 'float'):
            model.set_value(row, _index_, float(entry.get_text()))

        # Commercial PiQ entry called the function.
        if(_index_ == 79):
            CpiQ = float(entry.get_text())

            # Use this value for piQ if it is greater than zero.
            if(CpiQ > 0):
                model.set_value(row, 79, CpiQ)

        return False
