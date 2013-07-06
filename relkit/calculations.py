#!/usr/bin/env python2
""" This file contains various calculations used by the RTK Project. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       calculations.py is part of The RTK Project
#
# All rights reserved.

import sys
from os import name

# Modules required for the GUI.
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)

# Add NLS support.
import gettext
_ = gettext.gettext

# Import R library.
try:
    from rpy2 import robjects
    from rpy2.robjects import r as R
    from rpy2.robjects.packages import importr
    import rpy2.rlike.container as rlc
    import rpy2.rinterface as ri
    __USE_RPY__ = False
    __USE_RPY2__ = True
except ImportError:
    __USE_RPY__ = False
    __USE_RPY2__ = False

# Import mathematical functions.
import numpy as np
from math import ceil, exp, floor, log, sqrt

# Import other RTK modules.
import configuration as _conf
import utilities as _util


def calculate_project(button, application, index):
    """
    Calculates the hazard rate for the project.

    Keyword Arguments:
    button      -- the gtk.Toolbutton that called this function.
    application -- the RTK application object.
    index       -- an index indicating what to calculate:
                   0 - everything below.
                   1 - just the selected Revision.
                   2 - roll up all the Functions.
                   3 - roll up all the System hardware.
                   4 - roll up all the System software.
    """

    application.winTree.statusbar.push(2, "Calculating")

    if(index == 0):                         # Calculate everything.
        calculate_revision(None, application)

        _model_ = application.FUNCTION.model
        _row_ = _model_.get_iter_root()
        calculate_function(_model_, _row_, application)

        _model_ = application.HARDWARE.model
        _row_ = _model_.get_iter_root()
        (cost, lambdaa, lambdad, lambdas,
         lambdap, partcount, pwrdiss) = calculate_hardware(_model_, _row_,
                                                           application)
        application.HARDWARE.system_ht = lambdap

        _model_ = application.SOFTWARE.model
        _row_ = _model_.get_iter_root()
        application.SOFTWARE.rpfom = calculate_software(_model_, _row_,
                                                        application)
    elif(index == 1):                       # Calculate just the revision.
        calculate_revision(None, application)
    elif(index == 2):                       # Calculate just the functions.
        _model_ = application.FUNCTION.model
        _row_ = _model_.get_iter_root()
        calculate_function(_model_, _row_, application)
    elif(index == 3):                       # Calculate just the hardware.
        _model_ = application.HARDWARE.model
        _row_ = _model_.get_iter_root()
        (cost, lambdaa, lambdad, lambdas,
         lambdap, partcount, pwrdiss) = calculate_hardware(_model_, _row_,
                                                           application)
        application.HARDWARE.system_ht = lambdap
        application.ASSEMBLY.assessment_results_tab_load()
    elif(index == 4):                       # Calculate just the software.
        _model_ = application.SOFTWARE.model
        _row_ = _model_.get_iter_root()
        application.SOFTWARE.rpfom = calculate_software(_model_, _row_,
                                                        application)

    application.winTree.statusbar.pop(2)
    application.winTree.progressbar.set_fraction(0.0)

    return False


def calculate_revision(widget=None, application=None):
    """
    Calculates active hazard rate, dormant hazard rate, software hazard rate,
    predicted hazard rate, mission MTBF, limiting MTBF, mission reliability,
    limiting reliability, total cost, cost per failure, and cost per operating
    hour for the selected revision.

    Keyword Arguments:
    widget      -- the gtk.Widget that called this function.
    application -- the RTK application object.
    """

    _parent = application.HARDWARE.model.get_string_from_iter(application.HARDWARE.selected_row)
    if _parent is None:
        _parent = '0'

    values = (application.REVISION.revision_id,)
    if(_conf.BACKEND == 'mysql'):
        query = "SELECT SUM(fld_cost), \
                 SUM(fld_failure_rate_active), \
                 SUM(fld_failure_rate_dormant), \
                 SUM(fld_failure_rate_software), \
                 COUNT(fld_assembly_id) \
                 FROM tbl_system \
                 WHERE fld_revision_id=%d \
                 AND fld_part=1"
    elif(_conf.BACKEND == 'sqlite3'):
        query = "SELECT SUM(fld_cost), \
                 SUM(fld_failure_rate_active), \
                 SUM(fld_failure_rate_dormant), \
                 SUM(fld_failure_rate_software), \
                 COUNT(fld_assembly_id) \
                 FROM tbl_system \
                 WHERE fld_revision_id=? \
                 AND fld_part=1"

    results = application.DB.execute_query(query,
                                           values,
                                           application.ProgCnx,
                                           commit=False)

    if results[0][0] is None:
        return True
    else:
        cost = float(results[0][0])
        lambdaa = float(results[0][1])
        lambdad = float(results[0][2])
        lambdas = float(results[0][3])
        partcnt = int(results[0][4])

    lambdap = lambdaa + lambdad + lambdas   # Predicted h(t)

    # Calculate the MTBF
    mtbf = 1.0 / lambdap

    # Calculate reliabilities.
    rm = exp(-1.0 * lambdap * _conf.MTIME / _conf.FRMULT)

    _model_ = application.REVISION.model
    _row_ = application.REVISION.selected_row

    _model_.set_value(_row_, 3, cost)
    _model_.set_value(_row_, 6, lambdaa)
    _model_.set_value(_row_, 7, lambdad)
    _model_.set_value(_row_, 9, lambdap)
    _model_.set_value(_row_, 10, lambdas)
    _model_.set_value(_row_, 15, mtbf)
    _model_.set_value(_row_, 18, rm)
    _model_.set_value(_row_, 21, partcnt)

    application.REVISION.load_notebook()

    return False


def calculate_function(_model_, _row_, application):
    """
    Iterively calculates active hazard rate, dormant hazard rate,
    software hazard rate, predicted hazard rate, mission MTBF, limiting
    MTBF, mission reliability, limiting reliability, total cost, cost per
    failure, and cost per operating hour.

    Keyword Arguments:
    _model_     --
    _row_       --
    application -- the RTK application object.
    """

    #selection = application.FUNCTION.treeview.get_selection()
    #(_curmodel_, _currow_) = selection.get_selected()
    #_curpath_ = _model_.get_path(_currow_)

    if(_model_.iter_has_child(_row_)):
        print "A", _row_, _model_.get_value(_row_, 4)
        for j in range(_model_.iter_n_children(_row_)):
            calculate_function(_model_, _model_.iter_nth_child(_row_, j),
                               application)
    else:
        print "B", _row_, _model_.get_value(_row_, 4)

        values = (_model_.get_value(_row_, 1),)
        if(_conf.BACKEND == 'mysql'):
            query = "SELECT SUM(t2.fld_cost), \
                     SUM(t2.fld_failure_rate_predicted), \
                         COUNT(t2.fld_assembly_id), \
                         SUM(t2.fld_failure_rate_software) \
                         FROM tbl_system AS t2 \
                         INNER JOIN tbl_functional_matrix AS t1 \
                         ON t2.fld_assembly_id = t1.fld_assembly_id \
                         WHERE t1.fld_function_id=%d \
                         AND t2.fld_part=1"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT SUM(t2.fld_cost), \
                     SUM(t2.fld_failure_rate_predicted), \
                         COUNT(t2.fld_assembly_id), \
                         SUM(t2.fld_failure_rate_software) \
                         FROM tbl_system AS t2 \
                         INNER JOIN tbl_functional_matrix AS t1 \
                         ON t2.fld_assembly_id = t1.fld_assembly_id \
                         WHERE t1.fld_function_id=? \
                         AND t2.fld_part=1"

        results = application.DB.execute_query(query,
                                                   values,
                                                   application.ProgCnx)

        if(results[0][0] == None):
            return True
        else:
            cost = float(results[0][0])
            lambdap = float(results[0][1])
            partcnt = int(results[0][2])

        # Calculate the MTBF
        try:
            mtbf = 1.0 / lambdap
        except ZeroDivisionError:
            mtbf = 0.0
            application.user_log.error(_("Attempted to divide by zero when calculating function MTBF.\n \
                                           function id %s: lambdap = %f") % (application.FUNCTION.function_id, lambdap))

        _model_.set_value(_row_, 5, cost)
        _model_.set_value(_row_, 7, lambdap)
        _model_.set_value(_row_, 12, mtbf)
        _model_.set_value(_row_, 17, partcnt)

    #_column_ = application.FUNCTION.treeview.get_column(0)
   # application.FUNCTION.treeview.row_activated(_curpath_, _column_)

    application.FUNCTION.load_notebook()

    return False


def calculate_hardware(treemodel, row, application):
    """
    Iterively calculates active hazard rate, dormant hazard rate,
    software hazard rate, predicted hazard rate, mission MTBF, limiting
    MTBF, mission reliability, limiting reliability, total cost, cost per
    failure, cost per operating hour, and total power dissipation.

    Keyword Arguments:
    treemodel   -- the gtk.Treemodel containing the information to use in
                   calculations.
    row         -- the row in the gtk.Treemodel to read/write values.
    application -- the RTK application object.
    """

    application.winTree.progressbar.pulse()

    missiontime = treemodel.get_value(row, 45)
    num = treemodel.get_value(row, 67)
    refdes = treemodel.get_value(row, 68)
    hr_type = treemodel.get_value(row, 35)

    # Assemblies will first have their children calculated,
    # then sum the results.
    if(treemodel.iter_has_child(row)):
        cost = 0.0
        lambdaa = 0.0
        lambdad = 0.0
        lambdas = 0.0
        lambdap = 0.0
        partcount = 0
        pwrdiss = 0.0

        aaf = treemodel.get_value(row, 2)
        dutycycle = treemodel.get_value(row, 20)
        maf = treemodel.get_value(row, 57)

        if(hr_type == 1):                   # Assessed
            # Iterate through all the children and send each of them through
            # this function.
            for i in range(treemodel.iter_n_children(row)):
                (_cost, _lambdaa, _lambdad,
                _lambdas, _lambdap, _partcount,
                _pwrdiss) = calculate_hardware(treemodel,
                                               treemodel.iter_nth_child(row, i),
                                               application)

                cost += _cost
                lambdaa += _lambdaa
                lambdad += _lambdad
                lambdas += _lambdas
                lambdap += _lambdap
                partcount += _partcount
                pwrdiss += _pwrdiss

            lambdaa = lambdaa * num * maf + aaf
            lambdap = lambdaa + lambdad + lambdas

            pwrdiss = _pwrdiss * num

        else:                               # Specified.
            _cost = treemodel.get_value(row, 13)
            _partcount = treemodel.get_value(row, 67)
            _pwrdiss = treemodel.get_value(row, 83)

            if(hr_type == 2):               # Specified, hazard rate.
                lambdaa = treemodel.get_value(row, 34)
                try:
                    mtbf = 1.0 / lambdaa
                except ZeroDivisionError:
                    mtbf = 0.0

            elif(hr_type == 3):             # Specified, MTBF.
                mtbf = treemodel.get_value(row, 51)
                try:
                    lambdaa = 1.0 / mtbf
                except ZeroDivisionError:
                    lambdaa = 0.0

            lambdaa = (lambdaa + aaf) * num * maf * (dutycycle / 100.0)
            lambdad = 0.0
            lambdas = treemodel.get_value(row, 33)
            lambdap = lambdaa + lambdad + lambdas

    else:
        # Read the additive adjustment factor, cost, duty cycle,
        # multiplicative adjustment factor, and power dissipation.
        aaf = treemodel.get_value(row, 2)
        cost = treemodel.get_value(row, 13)
        dutycycle = treemodel.get_value(row, 20)
        maf = treemodel.get_value(row, 57)
        pwrdiss = treemodel.get_value(row, 83)

# Calculate component hazard rates.  Determine the type of hazard rate
# calculation that needs to be performed.
        if(hr_type == 1):               # Assessed.
            if(treemodel.get_value(row, 63) == 0):      # Assembly
                lambdaa = 0.0
                lambdad = 0.0
                # Assemblies should not show as overstressed.
                treemodel.set_value(row, 60, False)
                icon = _conf.ICON_DIR + '32x32/assembly.png'
                icon = gtk.gdk.pixbuf_new_from_file_at_size(icon, 16, 16)
                treemodel.set_value(row, 95, icon)

            elif(treemodel.get_value(row, 63) == 1):    # Component
                # Get the partlist full model and row associated with the selected
                # system tree item.
                partmodel = application.winParts.full_model
                path = application.winParts._treepaths[treemodel.get_value(row, 1)]
                partrow = partmodel.get_iter(path)

                # Determine the category and subcategory of part.
                category = treemodel.get_value(row, 11)
                subcategory = treemodel.get_value(row, 78)
                part = _util.set_part_model(category, subcategory)

                idx = treemodel.get_value(row, 10)
                try:
                    if(idx == 1):           # MIL-HDBK-217F Part Stress
                        part.calculate_mil_217_stress(partmodel, partrow,
                                                      treemodel, row)
                    elif(idx == 2):         # MIL-HDBK-217F Part Count
                        # TODO: Implement MIL-HDBK-217F part count model for all component types.
                        # TODO: Need to change lambda and pi output labels and gtk.Entry based on model selected (idx).
                        part.calculate_mil_217_count(partmodel, partrow,
                                                     treemodel, row)
                    elif(idx == 3):         # MIL-HDBK-217FN1 Part Stress
                        # TODO: Implement MIL-HDBK-217FN1 part stress model.
                        application.user_log.info(_("MIL-HDBK-217FN1 models not yet implemented.\n \
                                                  Contact weibullguy@gmail.com if you would like to help."))
                        _util.application_error(_("MIL-HDBK-217FN1 models not yet implemented.\n \
                                                Contact weibullguy@gmail.com if you would like to help."))
                    elif(idx == 4):         # MIL-HDBK-217FN1 Part Count
                        # TODO: Implement MIL-HDBK-217FN1 part count model.
                        application.user_log.info(_("MIL-HDBK-217FN1 models not yet implemented.\n \
                                                  Contact weibullguy@gmail.com if you would like to help."))
                        _util.application_error(_("MIL-HDBK-217FN1 models not yet implemented.\n \
                                               Contact weibullguy@gmail.com if you would like to help."))
                    elif(idx == 5):         # MIL-HDBK-217FN2 Part Stress
                        # TODO: Implement MIL-HDBK-217FN2 part stress model.
                        application.user_log.info(_("MIL-HDBK-217FN2 models not yet implemented.\n \
                                                  Contact weibullguy@gmail.com if you would like to help."))
                        _util.application_error(_("MIL-HDBK-217FN2 models not yet implemented.\n \
                                                Contact weibullguy@gmail.com if you would like to help."))
                    elif(idx == 6):         # MIL-HDBK-217FN2 Part Count
                        # TODO: Implement MIL-HDBK-217FN2 part count model.
                        application.user_log.info(_("MIL-HDBK-217FN2 models not yet implemented.\n \
                                                  Contact weibullguy@gmail.com if you would like to help."))
                        _util.application_error(_("MIL-HDBK-217FN2 models not yet implemented.\n \
                                                Contact weibullguy@gmail.com if you would like to help."))
                    elif(idx == 7):         # NSWC Mechanical
                        # TODO: Implement NSWC-07 model.
                        application.user_log.info(_("NSWC-07 Mechanical models not yet implemented.\n \
                                                  Contact weibullguy@gmail.com if you would like to help."))
                        _util.application_error(_("NSWC-07 Mechanical models not yet implemented.\n \
                                                Contact weibullguy@gmail.com if you would like to help."))

                    lambdaa = treemodel.get_value(row, 28)

                    # Calculate voltage ratio of component.
                    Voper = partmodel.get_value(partrow, 66)
                    Vrated = partmodel.get_value(partrow, 94)

                    try:
                        Vratio = Voper / Vrated
                    except ZeroDivisionError:
                        Vratio = 0.0

                    # Calculate current ratio of component.
                    Ioper = partmodel.get_value(partrow, 62)
                    Irated = partmodel.get_value(partrow, 92)

                    try:
                       Iratio = Ioper / Irated
                    except ZeroDivisionError:
                       Iratio = 0.0

                    # Calculate power ratio of component.
                    Poper = partmodel.get_value(partrow, 64)
                    Prated = partmodel.get_value(partrow, 93)

                    try:
                       Pratio = Poper / Prated
                    except ZeroDivisionError:
                       Pratio = 0.0

                    # Determine the total power dissipation.
                    num = treemodel.get_value(row, 67)
                    Ptotal = num * Poper

                    partmodel.set_value(partrow, 111, Vratio)
                    partmodel.set_value(partrow, 17, Iratio)
                    partmodel.set_value(partrow, 84, Pratio)

                    treemodel.set_value(row, 83, Ptotal)

                    # Check if component is overstressed.
                    (stressed, reason) = overstressed(partmodel, partrow,
                                                      treemodel, row)
                    treemodel.set_value(row, 60, stressed)
                    if(stressed):
                        icon = _conf.ICON_DIR + '32x32/overstress.png'
                    else:
                        icon = _conf.ICON_DIR + '32x32/part.png'

                    # TODO: Need to add field to database for holding the overstress reason.
                    #partmodel.set_value(partrow, , reason)
                    icon = gtk.gdk.pixbuf_new_from_file_at_size(icon, 16, 16)
                    treemodel.set_value(row, 91, icon)

                except SyntaxError:
                    lambdaa = 0.0

                active_env = treemodel.get_value(row, 22)
                dormant_env = treemodel.get_value(row, 23)
                lambdad = dormant_hazard_rate(category, subcategory, active_env,
                                              dormant_env, lambdaa)

        elif(hr_type == 2):                 # Specified, Hazard Rate.
            lambdaa = treemodel.get_value(row, 34)
            lambdad = 0.0

        elif(hr_type == 3):                 # Specified, MTBF.
            mtbf = treemodel.get_value(row, 51)
            lambdaa = 1.0 / mtbf
            lambdad = 0.0

        # Determine overall percentage of system hazard rate represented by
        # this particular component.
        try:
            hr_percent = lambdaa / application.HARDWARE.system_ht
            treemodel.set_value(row, 31, hr_percent)
        except ZeroDivisionError:
            refdes = treemodel.get_value(row, 68)
            _prompt_ = _("Attempted to divide by zero when calculating hazard rate percentage.\n \
                         refdes %s: Component lambda = %f and System lambda = %f") % (refdes, lambdaa, application.HARDWARE.system_ht)
            application.user_log.error(_prompt_)

        # Adjust the active hazard rate for additive adjustment factor,
        # quantity of items, multiplicative adjustment factor, and
        # duty cycle.
        lambdaa = (lambdaa + aaf) * num * maf * (dutycycle / 100.0)

        # Adjust the dormant hazard rate by the quantity of items.
        lambdad = lambdad * num

        # Calculate the software hazard rate.
        lambdas = treemodel.get_value(row, 33)
        lambdas = lambdas * num

        # Adjust the active, dormant, and software hazard rates by the hazard
        # rate multiplier.
        lambdaa = lambdaa / _conf.FRMULT
        lambdad = lambdad / _conf.FRMULT
        lambdas = lambdas / _conf.FRMULT

        # Calculate the predicted (total) hazard rate.
        lambdap = lambdaa + lambdad + lambdas

        # Set partcount.
        partcount = num

    # Calculate the mission MTBF and limiting MTBF
    try:
        MTBFM = 1.0 / (lambdaa + lambdas)
    except ZeroDivisionError:
        application.user_log.error(_("Attempted to divide by zero when calculating mission MTBF.\n \
                                      refdes %s: lambdaa = %f and lambdas = %f") % (refdes, lambdaa, lambdas))
        MTBFM = 0.0

    try:
        MTBF = 1.0 / lambdap
    except ZeroDivisionError:
        application.user_log.error(_("Attempted to divide by zero when calculating limiting MTBF.\n \
                                      refdes %s: lambdaa = %f") % (refdes, lambdap))
        MTBF = 0.0

    # Calculate the mission reliability and limiting reliability.
    Rmission = exp(-1.0 * (lambdaa + lambdas) * missiontime)
    Rlimit = exp(-1.0 * lambdap * missiontime)

    # Calculate cost per failure, cost per hour, and total cost.
    try:
        cpf = cost / (lambdap * missiontime)
    except ZeroDivisionError:
        application.user_log.error(_("Attempted to divide by zero when calculating cost per failure.\n \
                                      refdes %s: lambdap = %f and tm = %f") % (refdes, lambdap, missiontime))
        cpf = 0.0

    cph = cost * lambdap

    # TODO: Add database field for total cost results.
    #totalcost = cost * num

    treemodel.set_value(row, 13, cost)
    treemodel.set_value(row, 14, cpf)
    treemodel.set_value(row, 15, cph)
    treemodel.set_value(row, 28, lambdaa)
    treemodel.set_value(row, 29, lambdad)
    treemodel.set_value(row, 32, lambdap)
    treemodel.set_value(row, 49, MTBFM)
    treemodel.set_value(row, 50, MTBF)
    treemodel.set_value(row, 69, Rmission)
    treemodel.set_value(row, 70, Rlimit)
    treemodel.set_value(row, 82, partcount)
    treemodel.set_value(row, 83, pwrdiss)

    return(cost, lambdaa, lambdad, lambdas, lambdap, partcount, pwrdiss)


def calculate_part(dictionary):
    """
    Calculates the hazard rate for a component.

    Keyword Arguments:
    dictionary -- a dictionary containing the components h(t) prediction
                  model and the input variables.
    """

    keys = dictionary.keys()
    values = dictionary.values()

    for i in range(len(keys)):
        vars()[keys[i]] = values[i]

    lambdap = eval(dictionary['equation'])

    return(lambdap)


def calculate_software(treemodel, row, application):
    """
    Iterively calculates the software reliability prediction figure
    of merit (RPFOM).

    Keyword Arguments:
    treemodel   -- the gtk.Treemodel containing the information to edit.
    row         -- the row in the gtk.Treemodel to read/write values.
    application -- the RTK application object.
    """

    _level_id = treemodel.get_value(row, 2)
    _phase_id = treemodel.get_value(row, 36)

    # Systems will first have their children calculated, then sum the results.
    if(treemodel.iter_has_child(row)):

        RPFOM = 0

        for i in range(treemodel.iter_n_children(row)):

            _RPFOM = calculate_software(treemodel,
                                        treemodel.iter_nth_child(row, i),
                                        application)

            RPFOM += _RPFOM

        if(_level_id == 2):                 # This is a CSCI.
            RPFOM = calculate_csci(treemodel, row, application)

    else:

        if(_level_id == 2):                 # This is a CSCI.
            RPFOM = calculate_csci(treemodel, row, application)
        else:
            RPFOM = 0

    return(RPFOM)


def calculate_csci(treemodel, row, application):
    """
    This functions is used to calculate software reliability metrics for
    a CSCI.

    Keyword Arguments:
    treemodel   -- the gtk.Treemodel containing the information to edit.
    row         -- the row in the gtk.Treemodel to read/write values.
    application -- the RTK application object.
    """

    _fault_density = [0.0, 0.0128, 0.0092, 0.0078, 0.0018, 0.0085, 0.0123]
    _do = [0.0, 0.76, 1.0, 1.3]

    _phase_id = treemodel.get_value(row, 36)

    # Calculate the base fault density based on CSCI application.
    Ao = _fault_density[treemodel.get_value(row, 4)]

# ----- ----- --- Calculate the development environment factor -- ----- ----- #
    # If NOT using a detailed assessment, read the default value.  Otherwise,
    # calculate the development environment factor.
    _devel_id = treemodel.get_value(row, 5)
    _devel_type = treemodel.get_value(row, 35)

    if(_devel_type == 0):                   # Basic analysis.
        Do = _do[_devel_id]
    elif(_devel_type == 1):                 # Detailed analysis (default).
        values = (treemodel.get_value(row, 1),)
        (De, Dc, Do) = calculate_do_factor(_devel_id, values, application)

        treemodel.set_value(row, 7, De)
        treemodel.set_value(row, 9, Dc)
# - ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- - #

# ----- ----- ----- ----- - Calculate the S1 metric - ----- ----- ----- ----- #
    # We will pass these values to the next three functions for use in their
    # respective SQL queries.
    values = (treemodel.get_value(row, 1), _phase_id)

    # Calculate the anomaly management factor.
    (AM, SA) = calculate_am_factor(values, application)

    # Calculate the requirements traceability factor.  This is not influenced
    # by unit-level analyses, so we will always find the results at the
    # CSCI-level.
    ST = calculate_st_factor(_phase_id, values, application)

    # Calculate the software quality factor.
    (DR, SQ) = calculate_sq_factor(values, application)

    S1 = SA * ST * SQ
# - ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- - #

# ----- ----- ----- ----- - Calculate the S2 metric - ----- ----- ----- ----- #
    # We will pass these values to the next four functions for use in their
    # respective SQL queries.
    values = (treemodel.get_string_from_iter(row),)

    # Calculate the lines of code factor.
    (ALOC, HLOC, SLOC, SL) = calculate_sl_factor(values, application)

    # Calculate the complexity factor.
    (nm, ax, bx, cx, SX) = calculate_sx_factor(values, application)

    # Calculate the modularity factor.
    (um, xm, wm, SM) = calculate_sm_factor(nm, values, application)

    # Calculate the standards review factor.
    (DF, SR) = calculate_sr_factor(values, application)

    S2 = SL * SX * SM * SR
# - ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- - #

# ----- ----- ----- -- Calculate the test program metrics - ----- ----- ----- #
    # Calculate the test effort factor.
    _effort_id = treemodel.get_value(row, 40)
    if(_effort_id == 1):                    # Effort based on hours
        a = treemodel.get_value(row, 42)
        b = treemodel.get_value(row, 43)
    elif(_effort_id == 2):                  # Effort based on budget
        a = treemodel.get_value(row, 44)
        b = treemodel.get_value(row, 45)
    elif(_effort_id == 3):                  # Effort based on schedule
        a = treemodel.get_value(row, 46)
        b = treemodel.get_value(row, 47)
    else:
        a = 1.0
        b = 1.0

    AT = 0.4 * b / a
    if(AT < 1.0):
        TE = 0.9
    else:
        TE = 1.0

    # We will pass these values to the next two functions for use in their
    # respective SQL queries.
    values = (treemodel.get_value(row, 1),)

    # Calculate the test methodology factor (TM).
    (TT, TU, TM) = calculate_tm_factor(values, application)

    # Unit testing.
    #PT = treemodel.get_value(row, 48)
    #TP = treemodel.get_value(row, 49)
    #IT = treemodel.get_value(row, 50)
    #TI = treemodel.get_value(row, 51)

    MT = treemodel.get_value(row, 52)
    NM = treemodel.get_value(row, 24)
    NT = treemodel.get_value(row, 53)
    TN = treemodel.get_value(row, 54)

    # Calculate the test coverage factor.
    try:
        TC = 2 / (MT / NM + NT / TN)
    except ZeroDivisionError:
        TC = 1.0

    To = TE * TM * TC

    T1 = 0.02 * To
    T2 = 0.14 * To
# - ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- - #

# ----- ----- ----- - Calculate the RPFOM and failure rates ----- ----- ----- #
    if(_phase_id == 1):                     # Requirements development
        RPFOM = Ao * Do

    elif(_phase_id == 2 or
         _phase_id == 3 or
         _phase_id == 4):                   # Design
        RPFOM = Ao * Do * S1

    elif(_phase_id == 5):                   # Coding and testing
        RPFOM = Ao * Do * S1 * S2

        # Find the total number of incidents for the software module being
        # analyzed.
        if(_conf.BACKEND == 'mysql'):
            query = "SELECT COUNT(*) \
                     FROM tbl_incident \
                     WHERE fld_software_id=%d \
                     AND fld_incident_category=2 \
                     AND fld_life_cycle=2"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT COUNT(*) \
                     FROM tbl_incident \
                     WHERE fld_software_id=? \
                     AND fld_incident_category=2 \
                     AND fld_life_cycle=2"

        numIncidents = application.DB.execute_query(query,
                                                    values,
                                                    application.ProgCnx)

        # Find the maximum execution time of all the incidents for the software
        # module being analyzed.
        if(_conf.BACKEND == 'mysql'):
            query = "SELECT MAX(fld_execution_time) \
                     FROM tbl_incident \
                     WHERE fld_software_id=%d \
                     AND fld_incident_category=2 \
                     AND fld_life_cycle=2;"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT MAX(fld_execution_time) \
                     FROM tbl_incident \
                     WHERE fld_software_id=? \
                     AND fld_incident_category=2 \
                     AND fld_life_cycle=2;"

        maxTime = application.DB.execute_query(query,
                                               values,
                                               application.ProgCnx)

        # Calculate the failure rate during test (instaneous failure rate).
        try:
            FT1 = float(numIncidents[0][0]) / float(maxTime[0][0])
        except TypeError:
            FT1 = 1.0

        # Find the top three execution times for the software module being
        # analyzed.
        if(_conf.BACKEND == 'mysql'):
            query = "SELECT DISTINCT fld_execution_time \
                     FROM tbl_incident \
                     WHERE fld_software_id=%d \
                     AND fld_incident_category=2 \
                     AND fld_life_cycle=2 \
                     ORDER BY fld_execution_time DESC \
                     LIMIT 4"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT DISTINCT fld_execution_time \
                     FROM tbl_incident \
                     WHERE fld_software_id=? \
                     AND fld_incident_category=2 \
                     AND fld_life_cycle=2 \
                     ORDER BY fld_execution_time DESC \
                     LIMIT 4"

        times = application.DB.execute_query(query,
                                             values,
                                             application.ProgCnx)

        # Find the total number of incidents occurring during the last three
        # execution times for the software module being analyzed.
        values = (treemodel.get_value(row, 1),
                  times[3][0], times[0][0])

        if(_conf.BACKEND == 'mysql'):
            query = "SELECT COUNT(*) \
                     FROM tbl_incident \
                     WHERE fld_software_id=%d \
                     AND fld_incident_category=2 \
                     AND fld_life_cycle=2 \
                     AND fld_execution_time BETWEEN %f AND %f"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT COUNT(*) \
                     FROM tbl_incident \
                     WHERE fld_software_id=? \
                     AND fld_incident_category=2 \
                     AND fld_life_cycle=2 \
                     AND fld_execution_time BETWEEN ? AND ?"

        numIncidents = application.DB.execute_query(query,
                                                    values,
                                                    application.ProgCnx)

        # Calculate the failure rate at end of test (cumulative failure rate).
        try:
            delta_t = float(times[0][0]) - float(times[3][0])
            FT2 = float(numIncidents[0][0]) / float(delta_t)
        except TypeError:
            FT2 = 1.0

        REN_AVG = FT1 * T1
        REN_EOT = FT2 * T2

        ET = treemodel.get_value(row, 65)
        OS = treemodel.get_value(row, 66)
        EW = ET / (ET - OS)

        EC = treemodel.get_value(row, 63)
        EV = 0.1 + 4.5 * EC

        E = EW * EV

        F = FT2 * 0.14 * E

        treemodel.set_value(row, 59, FT1)
        treemodel.set_value(row, 60, FT2)
        treemodel.set_value(row, 61, REN_AVG)
        treemodel.set_value(row, 62, REN_EOT)
        treemodel.set_value(row, 64, EV)
        treemodel.set_value(row, 67, EW)
        treemodel.set_value(row, 68, E)
        treemodel.set_value(row, 69, F)
# - ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- - #

    treemodel.set_value(row, 6, Ao)
    treemodel.set_value(row, 10, Do)
    treemodel.set_value(row, 11, AM)
    treemodel.set_value(row, 12, SA)
    treemodel.set_value(row, 13, ST)
    treemodel.set_value(row, 14, DR)
    treemodel.set_value(row, 15, SQ)
    treemodel.set_value(row, 16, S1)
    treemodel.set_value(row, 17, HLOC)
    treemodel.set_value(row, 18, ALOC)
    treemodel.set_value(row, 19, SLOC)
    treemodel.set_value(row, 20, SL)
    treemodel.set_value(row, 21, ax)
    treemodel.set_value(row, 22, bx)
    treemodel.set_value(row, 23, cx)
    treemodel.set_value(row, 24, nm)
    treemodel.set_value(row, 25, SX)
    treemodel.set_value(row, 26, um)
    treemodel.set_value(row, 27, wm)
    treemodel.set_value(row, 28, xm)
    treemodel.set_value(row, 29, SM)
    treemodel.set_value(row, 30, DF)
    treemodel.set_value(row, 31, SR)
    treemodel.set_value(row, 32, S2)
    treemodel.set_value(row, 33, RPFOM)
    treemodel.set_value(row, 55, TE)
    treemodel.set_value(row, 56, TM)
    treemodel.set_value(row, 57, TC)
    treemodel.set_value(row, 58, To)

    return(RPFOM)


def calculate_do_factor(_devel_id, values, application):
    """
    This function calculate the software development environment factors
    (De, Dc, and Do).

    Keyword Arguments:
    _devel_id   -- the index of the type of development environment in which
                   the software module is being developed.
    values      -- a tuple containing the values to use in the SQL query.
    application -- the RTK application.
    """

    if(_conf.BACKEND == 'mysql'):
        query = "SELECT SUM(fld_y) \
                 FROM tbl_software_development \
                 WHERE fld_software_id=%d"
    elif(_conf.BACKEND == 'sqlite3'):
        query = "SELECT SUM(fld_y) \
                 FROM tbl_software_development \
                 WHERE fld_software_id=?"

    results = application.DB.execute_query(query,
                                           values,
                                           application.ProgCnx)

    if(results[0][0] is None):
        De = 0
    else:
        De = float(results[0][0])

    Dc = 1 - (De / 43.0)
    if(_devel_id == 1):                     # Embedded
        Do = (0.109 * Dc - 0.04) / 0.014
    elif(_devel_id == 2):                   # Semi-detached
        Do = (0.008 * Dc + 0.009) / 0.013
    elif(_devel_id == 3):                   # Organic
        Do = (0.018 * Dc - 0.003) / 0.008

    return(De, Dc, Do)


def calculate_am_factor(values, application):
    """
    This function calculate the software anomaly management factor (SA).

    Keyword Arguments:
    values      -- a tuple containing the values to use in the SQL query.
    application -- the RTK application.
    """

    # Get a count of the AM questions answered yes and no for the selected
    # software module.
    if(_conf.BACKEND == 'mysql'):
        query = "SELECT SUM(fld_y), SUM(fld_n) \
                 FROM tbl_anomaly_management \
                 WHERE fld_software_id=%d \
                 AND fld_phase_id=%d"
    elif(_conf.BACKEND == 'sqlite3'):
        query = "SELECT SUM(fld_y), SUM(fld_n) \
                 FROM tbl_anomaly_management \
                 WHERE fld_software_id=? \
                 AND fld_phase_id=?"

    results = application.DB.execute_query(query,
                                           values,
                                           application.ProgCnx)

    try:
        AM = float(results[0][1]) / (float(results[0][0]) + float(results[0][1]))
    except TypeError:
        AM = 1.0
    except ZeroDivisionError:
        AM = 1.0

    if(AM < 0.4):
        SA = 0.9
    elif(AM >= 0.4 and AM <= 0.6):
        SA = 1.0
    else:
        SA = 1.1

    return(AM, SA)


def calculate_st_factor(_phase_id, values, application):
    """
    This function calculate the software requirements traceability factor (ST).

    Keyword Arguments:
    _hase_id    -- the index of the development phase for the software module
                   being calculated.
    values      -- a tuple containing the values to use in the SQL query.
    application -- the RTK application.
    """

    if(_conf.BACKEND == 'mysql'):
        query = "SELECT fld_tc11, fld_tc12 \
                 FROM tbl_software_traceability \
                 WHERE fld_software_id=%d \
                 AND fld_phase_id=%d"
    elif(_conf.BACKEND == 'sqlite3'):
        query = "SELECT fld_tc11, fld_tc12 \
                 FROM tbl_software_traceability \
                 WHERE fld_software_id=? \
                 AND fld_phase_id=?"

    results = application.DB.execute_query(query,
                                           values,
                                           application.ProgCnx)

    if(_phase_id == 2 and results[0][0] == 1):
        ST = 1.0
    elif(_phase_id == 3 and results[0][0] == 1):
        ST = 1.0
    elif(_phase_id == 4 and results[0][0] == 1 and results[0][1] == 1):
        ST = 1.0
    else:
        ST = 1.1

    return(ST)


def calculate_sq_factor(values, application):
    """
    This function calculate the software quality factor (SQ).

    Keyword Arguments:
    values      -- a tuple containing the values to use in the SQL query.
    application -- the RTK application.
    """

    # Get a count of the SQ questions answered yes and no for the selected
    # software module.
    if(_conf.BACKEND == 'mysql'):
        query = "SELECT SUM(fld_y), SUM(fld_n) \
                 FROM tbl_software_quality \
                 WHERE fld_software_id=%d \
                 AND fld_phase_id=%d"
    elif(_conf.BACKEND == 'sqlite3'):
        query = "SELECT SUM(fld_y), SUM(fld_n) \
                 FROM tbl_software_quality \
                 WHERE fld_software_id=? \
                 AND fld_phase_id=?"

    results = application.DB.execute_query(query,
                                           values,
                                           application.ProgCnx)

    try:
        DR = float(results[0][1]) / (float(results[0][0]) + float(results[0][1]))
    except TypeError:
        DR = 0.0
    except ZeroDivisionError:
        DR = 0.0

    if(DR > 0.5):
        SQ = 1.0
    else:
        SQ = 1.1

    return(DR, SQ)


def calculate_sl_factor(values, application):
    """
    This function calculate the software lines of code factor (SL).

    Keyword Arguments:
    values      -- a tuple containing the values to use in the SQL query.
    application -- the RTK application.
    """

    # Get a count of the number of lines of assembly code, higher order
    # language code, and total lines of code for the selected software module.
    if(_conf.BACKEND == 'mysql'):
        query = "SELECT SUM(fld_aloc), SUM(fld_hloc), SUM(fld_loc) \
                 FROM tbl_software \
                 WHERE fld_parent_module='%s'"
    elif(_conf.BACKEND == 'sqlite3'):
        query = "SELECT SUM(fld_aloc), SUM(fld_hloc), SUM(fld_loc) \
                 FROM tbl_software \
                 WHERE fld_parent_module=?"

    results = application.DB.execute_query(query,
                                           values,
                                           application.ProgCnx)

    if(results == '' or not results or results[0][0] is None):
        ALOC = 0.0
        HLOC = 0.0
        SLOC = 0.0
    else:
        ALOC = results[0][0]
        HLOC = results[0][1]
        SLOC = results[0][2]

    try:
        SL = (float(HLOC) / float(SLOC)) + (1.4 * float(ALOC) / float(SLOC))
    except ZeroDivisionError:
        SL = 1.0

    return(ALOC, HLOC, SLOC, SL)


def calculate_sx_factor(values, application):
    """
    This function calculates the software complexity factor (SX).

    Keyword Arguments:
    values      -- a tuple containing the values to use in the SQL query.
    application -- the RTK application.
    """

    # Get a count of the number of units comprising the selected software
    # module.
    if(_conf.BACKEND == 'mysql'):
        query = "SELECT COUNT(fld_sx) \
                 FROM tbl_software \
                 WHERE fld_parent_module='%s'"
    elif(_conf.BACKEND == 'sqlite3'):
        query = "SELECT COUNT(fld_sx) \
                 FROM tbl_software \
                 WHERE fld_parent_module=?"

    results = application.DB.execute_query(query,
                                           values,
                                           application.ProgCnx)

    if(results == '' or not results):
        nm = 0
    else:
        nm = results[0][0]


    # Find the count of all the units with a complexity levels greater than 20
    # in the selected software module.
    if(_conf.BACKEND == 'mysql'):
        query = "SELECT COUNT(fld_sx) \
                 FROM tbl_software \
                 WHERE fld_parent_module='%s' \
                 AND fld_sx>20"
    elif(_conf.BACKEND == 'sqlite3'):
        query = "SELECT COUNT(fld_sx>20) \
                 FROM tbl_software \
                 WHERE fld_parent_module=? \
                 AND fld_sx>20"

    results = application.DB.execute_query(query,
                                           values,
                                           application.ProgCnx)

    if(results == '' or not results):
        ax = 0
    else:
        ax = results[0][0]

    # Find the count of all the units with a complexity levels less than 7 in
    # the selected software module.
    if(_conf.BACKEND == 'mysql'):
        query = "SELECT COUNT(fld_sx<7) \
                 FROM tbl_software \
                 WHERE fld_parent_module='%s' \
                 AND fld_sx<7"
    elif(_conf.BACKEND == 'sqlite3'):
        query = "SELECT COUNT(fld_sx<7) \
                 FROM tbl_software \
                 WHERE fld_parent_module=? \
                 AND fld_sx<7"

    results = application.DB.execute_query(query,
                                           values,
                                           application.ProgCnx)

    if(results == '' or not results):
        cx = 0
    else:
        cx = results[0][0]

    bx = nm - ax - cx

    try:
        SX = (1.5 * float(ax) + float(bx) + 0.8 * float(cx)) / float(nm)
    except ZeroDivisionError:
        SX = 1.0

    return(nm, ax, bx, cx, SX)


def calculate_sm_factor(nm, values, application):
    """
    This function calculates the software modularity factor (SM).

    Keyword Arguments:
    nm          -- the total number of units comprising the selected software
                   module.
    values      -- a tuple containing the values to use in the SQL query.
    application -- the RTK application.
    """

    # Find the counts of all the units in the CSCI with less than 200 lines
    # of executable code.
    if(_conf.BACKEND == 'mysql'):
        query = "SELECT COUNT(fld_loc) \
                 FROM tbl_software \
                 WHERE fld_parent_module='%s' \
                 AND fld_loc<200"
    elif(_conf.BACKEND == 'sqlite3'):
        query = "SELECT COUNT(fld_loc) \
                 FROM tbl_software \
                 WHERE fld_parent_module=? \
                 AND fld_loc<200"

    results = application.DB.execute_query(query,
                                           values,
                                           application.ProgCnx)

    if(results is None):
        um = 0
    else:
        um = results[0][0]

    # Find the counts of all the units in the CSCI with greater than 3000
    # lines of executable code.
    if(_conf.BACKEND == 'mysql'):
        query = "SELECT COUNT(fld_loc) \
                 FROM tbl_software \
                 WHERE fld_parent_module='%s' \
                 AND fld_loc>3000"
    elif(_conf.BACKEND == 'sqlite3'):
        query = "SELECT COUNT(fld_loc) \
                 FROM tbl_software \
                 WHERE fld_parent_module=? \
                 AND fld_loc>3000"

    results = application.DB.execute_query(query,
                                           values,
                                           application.ProgCnx)

    if(results is None):
        xm = 0
    else:
        xm = results[0][0]

    wm = nm - um - xm

    try:
        SM = (0.9 * float(um) + float(wm) + 2 * float(xm)) / float(nm)
    except ZeroDivisionError:
        SM = 1.0

    return(um, xm, wm, SM)


def calculate_sr_factor(values, application):
    """
    This function calculates the software standards review factor (SR).

    Keyword Arguments:
    values      -- a tuple containing the values to use in the SQL query.
    application -- the RTK application.
    """

    if(_conf.BACKEND == 'mysql'):
        query = "SELECT SUM(fld_y), SUM(fld_n) \
                 FROM tbl_software_standards \
                 WHERE fld_software_id=%d \
                 AND fld_phase_id=%d"
    elif(_conf.BACKEND == 'sqlite3'):
        query = "SELECT SUM(fld_y), SUM(fld_n) \
                 FROM tbl_software_standards \
                 WHERE fld_software_id=? \
                 AND fld_phase_id=?"

    results = application.DB.execute_query(query,
                                           values,
                                           application.ProgCnx)

    try:
        DF = float(results[0][1]) / (float(results[0][0]) + float(results[0][1]))
    except TypeError:
        DF = 0.0
    except ZeroDivisionError:
        DF = 0.0

    if(DF >= 0.5):
        SR = 1.5
    elif(DF < 0.5 and DF >= 0.25):
        SR = 1.0
    else:
        SR = 0.75

    return(DF, SR)


def calculate_tm_factor(values, application):
    """
    This function calculates the software test methodology factor (TM).

    Keyword Arguments:
    values      -- a tuple containing the values to use in the SQL query.
    application -- the RTK application.
    """

    # Find the sum of all the test methods recommended for the software module
    # being analyzed.
    if(_conf.BACKEND == 'mysql'):
        query = "SELECT SUM(fld_effectiveness_single | \
                            fld_effectiveness_paired | \
                            fld_coverage_single | \
                            fld_coverage_paired | \
                            fld_error_cat) \
                 FROM tbl_software_tests \
                 WHERE fld_software_id=%d"
    elif(_conf.BACKEND == 'sqlite3'):
        query = "SELECT SUM(fld_effectiveness_single | \
                            fld_effectiveness_paired | \
                            fld_coverage_single | \
                            fld_coverage_paired | \
                            fld_error_cat) \
                 FROM tbl_software_tests \
                 WHERE fld_software_id=?"

    TT = application.DB.execute_query(query,
                                      values,
                                      application.ProgCnx)

    if(not TT[0][0] or TT[0][0] == '' or TT[0][0] is None):
        TT = 1.0
    else:
        TT = float(TT[0][0])

    # Find the sum of test methods actually being used for the software module
    # being analyzed.
    if(_conf.BACKEND == 'mysql'):
        query = "SELECT SUM(fld_used) \
                 FROM tbl_software_tests \
                 WHERE fld_software_id=%d"
    elif(_conf.BACKEND == 'sqlite3'):
        query = "SELECT SUM(fld_used) \
                 FROM tbl_software_tests \
                 WHERE fld_software_id=?"

    TU = application.DB.execute_query(query,
                                      values,
                                      application.ProgCnx)

    if(not TU[0][0] or TU[0][0] == '' or TU[0][0] is None):
        TU = 0.0
    else:
        TU = float(TU[0][0])

    # Calculate the test methodology factor.
    if(TU/TT > 0.75):
        TM = 0.9
    elif(TU/TT < 0.75 and TU/TT > 0.5):
        TM = 1.0
    else:
        TM = 1.1

    return(TT, TU, TM)


def overstressed(partmodel, partrow, systemmodel, systemrow):
    """
    Determines whether the component is overstressed based on derating
    rules.

    Keyword arguments:
    application -- the RTK application.
    partmodel   -- the RTK winParts full gtk.TreeModel.
    partrow     -- the currently selected row in the winParts full
                   gtk.TreeModel.
    systemmodel -- the RTK HARDWARE object gtk.TreeModel.
    systemrow   -- the currently selected row in the RTK HARWARE
                   object gtk.TreeModel.

    Currently only default derating rules from Reliability Toolkit:
    Commercial Practices Edition, Section 6.3.3 are used.

      Component  |                            |    Environment    |
        Type     |     Derating Parameter     | Severe  | Benign  |
    -------------+----------------------------+---------+---------+
     Capacitor   | DC Voltage                 |   60%   |   90%   |
                 | Temp from Max Limit        |   10C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Circuit Bkr | Current                    |   80%   |   80%   |
    -------------+----------------------------+---------+---------+
     Connectors  | Voltage                    |   70%   |   90%   |
                 | Current                    |   70%   |   90%   |
                 | Insert Temp from Max Limit |   25C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Diodes      | Power Dissipation          |   70%   |   90%   |
                 | Max Junction Temperature   |  125C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Fiber Optics| Bend Radius                |  200%   |  200%   |
                 | Cable Tension              |   50%   |   50%   |
    -------------+----------------------------+---------+---------+
     Fuses       | Current (Maximum           |   50%   |   70%   |
                 | Capability)                |         |         |
    -------------+----------------------------+---------+---------+
     Inductors   | Operating Current          |   60%   |   90%   |
                 | Dielectric Voltage         |   50%   |   90%   |
                 | Temp from Hot Spot         |   15C   |         |
    -------------+----------------------------+---------+---------+
     Lamps       | Voltage                    |   94%   |   94%   |
    -------------+----------------------------+---------+---------+
     Memories    | Supply Voltage             |  +/-5%  |  +/-5%  |
                 | Output Current             |   80%   |   90%   |
                 | Max Junction Temp          |  125C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Micro-      | Supply Voltage             |  +/-5%  |  +/-5%  |
     circuits    | Fan Out                    |   80%   |   80%   |
                 | Max Junction Temp          |  125C   |   N/A   |
    -------------+----------------------------+---------+---------+
     GaAs Micro- | Max Junction Temp          |  135C   |   N/A   |
     circuits    |                            |         |         |
    -------------+----------------------------+---------+---------+
     Micro-      | Supply Voltage             |  +/-5%  |  +/-5%  |
     processors  | Fan Out                    |   80%   |   80%   |
                 | Max Junction Temp          |  125C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Photo-      | Reverse Voltage            |   70%   |    70%  |
     diode       | Max Junction Temp          |  125C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Photo-      | Max Junction Temp          |  125C   |   N/A   |
     transistor  |                            |         |         |
    -------------+----------------------------+---------+---------+
     Relays      | Resistive Load Current     |   75%   |   90%   |
                 | Capacitive Load Current    |   75%   |   90%   |
                 | Inductive Load Current     |   40%   |   50%   |
                 | Contact Power              |   50%   |   60%   |
    -------------+----------------------------+---------+---------+
     Resistors   | Power Dissipation          |   50%   |   80%   |
                 | Temp from Max Limit        |   30C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Transistor, | Power Dissipation          |   70%   |   90%   |
     Silicon     | Breakdown Voltage          |   75%   |   90%   |
                 | Max Junction Temp          |  125C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Transistor, | Power Dissipation          |   70%   |   90%   |
     GaAs        | Breakdown Voltage          |   70%   |   90%   |
                 | Max Junction Temp          |  135C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Thyristors  | On-State Current           |   70%   |   90%   |
                 | Off-State Voltage          |   70%   |   90%   |
                 | Max Junction Temp          |  125C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Switches    | Resistive Load Current     |   75%   |   90%   |
                 | Capacitive Load Current    |   75%   |   90%   |
                 | Inductive Load Current     |   40%   |   50%   |
                 | Contact Power              |   50%   |   60%   |
    -------------+----------------------------+---------+---------+
    """

    # |------------------  <---- Knee Temperature
    # |                  \
    # |                   \
    # |                    \
    # |                     \  <---- Maximum Temperature
    # +------------------------
    overstress = False
    reason = ""
    r_index = 1
    harsh = True

    Eidx = systemmodel.get_value(systemrow, 22)
    Tknee = partmodel.get_value(partrow, 43)
    Tmax = partmodel.get_value(partrow, 55)
    Tmin = partmodel.get_value(partrow, 56)

    category = systemmodel.get_value(systemrow, 11)
    subcategory = systemmodel.get_value(systemrow, 78)

    # If the active environment is Benign Ground, Fixed Ground,
    # Sheltered Naval, or Space Flight it is NOT harsh.
    if(Eidx == 1 or Eidx == 2 or Eidx == 4 or Eidx == 11):
        harsh = False

    if(category == 1):                      # Capacitor
        Voper = partmodel.get_value(partrow, 66)
        Vrate = partmodel.get_value(partrow, 94)
        Toper = systemmodel.get_value(systemrow, 80)

        if(harsh):
            if(Voper > 0.60 * Vrate):
                overstress = True
                reason = reason + str(r_index) + ". Operating voltage > 60% rated voltage.\n"
                r_index += 1
            if(Tmax - Toper <= 10.0):
                overstress = True
                reason = reason + str(r_index) + ". Operating temperature within 10.0C of maximum rated temperature.\n"
                r_index += 1
        else:
            if(Voper > 0.90 * Vrate):
                overstress = True
                reason = reason + str(r_index) + ". Operating voltage > 90% rated voltage.\n"
                r_index += 1

    elif(category == 2):                    # Connection
        Tmax = partmodel.get_value(partrow, 55)
        Ioper = partmodel.get_value(partrow, 62)
        Voper = partmodel.get_value(partrow, 66)
        Irate = partmodel.get_value(partrow, 92)
        Vrate = partmodel.get_value(partrow, 94)
        Trise = partmodel.get_value(partrow, 107)
        Toper = partmodel.get_value(partrow, 80)

        if(harsh):
            if(Voper > 0.7 * Vrate):
                overstress = True
                reason = reason + str(r_index) + ". Operating voltage > 70% rated voltage.\n"
                r_index += 1
            if(Ioper > 0.7 * Irate):
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 70% rated current.\n"
                r_index += 1
            if((Trise + Toper - Tmax) < 25):
                overstress = True
                reason = reason + str(r_index) + ". Operating temperature within 25.0C of maximum rated temperature.\n"
                r_index += 1
        else:
            if(Voper > 0.9 * Vrate):
                overstress = True
                reason = reason + str(r_index) + ". Operating voltage > 90% rated voltage.\n"
                r_index += 1
            if(Ioper > 0.9 * Irate):
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 90% rated current.\n"
                r_index += 1

    elif(category == 3):                    # Inductive Device
        Ths = partmodel.get_value(partrow, 39)
        Ioper = partmodel.get_value(partrow, 62)
        Voper = partmodel.get_value(partrow, 66)
        Irate = partmodel.get_value(partrow, 92)
        Vrate = partmodel.get_value(partrow, 94)
        Toper = partmodel.get_value(partrow, 105)

        if(harsh):
            if(Ioper > 0.60 * Irate):
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 60% rated current.\n"
                r_index += 1
            if(Voper > 0.50 * Vrate):
                overstress = True
                reason = reason + str(r_index) + ". Operating voltage > 50% rated voltage.\n"
                r_index += 1
            if(Ths - Toper < 15.0):
                overstress = True
                reason = reason + str(r_index) + ". Operating temperature within 15.0C of maximum rated temperature.\n"
                r_index += 1
        else:
            if(Ioper > 0.90 * Irate):
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 90% rated current.\n"
                r_index += 1
            if(Voper > 0.90 * Vrate):
                overstress = True
                reason = reason + str(r_index) + ". Operating voltage > 90% rated voltage.\n"
                r_index += 1

    elif(category == 4):                    # Integrated Circuit
        Tjunc = partmodel.get_value(partrow, 39)
        Ioper = partmodel.get_value(partrow, 62)
        Voper = partmodel.get_value(partrow, 66)
        Irate = partmodel.get_value(partrow, 92)
        Vrate = partmodel.get_value(partrow, 94)

        if(subcategory < 3):                # GaAs
            if(harsh):
                if(Tjunc > 135.0):
                    overstress = True
                    reason = reason + str(r_index) + ". Junction temperature > 135.0C.\n"
                    r_index += 1
        else:
            if(harsh):
                if(Voper > 1.05 * Vrate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage > 105% rated voltage.\n"
                    r_index += 1
                if(Voper < 0.95 * Vrate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage < 95% rated voltage.\n"
                    r_index += 1
                if(Ioper > 0.80 * Irate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current > 80% rated current.\n"
                    r_index += 1
                if(Tjunc > 125.0):
                    overstress = True
                    reason = reason + str(r_index) + ". Junction temperature > 125.0C.\n"
                    r_index += 1
            else:
                if(Voper > 1.05 * Vrate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage > 105% rated voltage.\n"
                    r_index += 1
                if(Voper < 0.95 * Vrate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage < 95% rated voltage.\n"
                    r_index += 1
                if(Ioper > 0.90 * Irate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current > 90% rated current.\n"
                    r_index += 1

    elif(category == 6):                    # Miscellaneous
        if(subcategory == 80):              # Crystal
            # TODO: Overstress calculations for crystals.
            print "TODO: Overstress calculations for crystals."
        elif(subcategory == 81):            # Lamps
            Voper = partmodel.get_value(partrow, 66)
            Vrated = partmodel.get_value(partrow, 94)
            if(Voper >= 0.94 * Vrated):
                overstress = True
                reason = reason + str(r_index) + ". Operating voltage > 94% rated voltage.\n"
                r_index += 1
        elif(subcategory == 82):            # Fuse
            # TODO: Overstress calculations for fuses.
            print "TODO: Overstress calculations for fuses."
        elif(subcategory == 83):            # Filter
            # TODO: Overstress calculations for filters.
            print "TODO: Overstress calculations for filters."

    elif(category == 7):                    # Relay
        # TODO: Add contact power overstress calculations for relays
        Aidx = partmodel.get_value(partrow, 30)
        Ioper = partmodel.get_value(partrow, 62)
        Irated = partmodel.get_value(partrow, 92)

        if(harsh):
            if(Aidx == 1 and Ioper > 0.75 * Irated):
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 75% rated current.\n"
                r_index += 1
            elif(Aidx == 2 and Ioper > 0.75 * Irated):
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 75% rated current.\n"
                r_index += 1
            elif(Aidx == 3 and Ioper > 0.40 * Irated):
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 40% rated current.\n"
                r_index += 1
        else:
            if(Aidx == 1 and Ioper > 0.90 * Irated):
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 90% rated current.\n"
                r_index += 1
            elif(Aidx == 2 and Ioper > 0.90 * Irated):
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 90% rated current.\n"
                r_index += 1
            elif(Aidx == 3 and Ioper > 0.50 * Irated):
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 50% rated current.\n"
                r_index += 1

    elif(category == 8):                    # Resistor
        # TODO: Add temperature limit overstress calculations for resistors
        # TODO: Add voltage ratio overstress calculations for variable resistors.
        Poper = partmodel.get_value(partrow, 64)
        Prated = partmodel.get_value(partrow, 93)

        if(harsh):
            if(Poper > 0.5 * Prated):
                overstress = True
                reason = reason + str(r_index) + ". Operating power > 50% rated power.\n"
                r_index += 1
        else:
            if(Poper > 0.8 * Prated):
                overstress = True
                reason = reason + str(r_index) + ". Operating power > 80% rated power.\n"
                r_index += 1

    elif(category == 9):                    # Semiconductor
        Tjunc = partmodel.get_value(partrow, 39)
        Ioper = partmodel.get_value(partrow, 62)
        Poper = partmodel.get_value(partrow, 64)
        Voper = partmodel.get_value(partrow, 66)
        Irate = partmodel.get_value(partrow, 92)
        Prate = partmodel.get_value(partrow, 93)
        Vrate = partmodel.get_value(partrow, 94)

        if(subcategory == 1 or \
           subcategory == 2):               # Diodes
            if(harsh):
                if(Poper > 0.7 * Prate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating power > 70% rated power.\n"
                    r_index += 1
                if(Tjunc > 125.0):
                    overstress = True
                    reason = reason + str(r_index) + ". Junction temperature > 125.0C.\n"
                    r_index += 1
            else:
                if(Poper > 0.9 * Prate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating power > 90% rated power.\n"
                    r_index += 1

        elif(subcategory > 2 and \
             subcategory < 6):              # Optoelectronics
            if(Voper > 0.70 * Vrate):
                overstress = True
                reason = reason + str(r_index) + ". Operating voltage > 70% rated voltage.\n"
                r_index += 1
            if(Tjunc > 125.0):
                overstress = True
                reason = reason + str(r_index) + ". Junction temperature > 125.0C.\n"
                r_index += 1

        elif(subcategory == 6):             # Thyristor
            if(harsh):
                if(Ioper > 0.70 * Irate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current > 70% rated current.\n"
                    r_index += 1
                if(Voper > 0.70 * Vrate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage > 70% rated voltage.\n"
                    r_index += 1
                if(Tjunc > 125.0):
                    overstress = True
                    reason = reason + str(r_index) + ". Junction temperature > 125.0C.\n"
                    r_index += 1
            else:
                if(Ioper > 0.90 * Irate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current > 90% rated current.\n"
                    r_index += 1
                if(Voper > 0.90 * Vrate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage > 90% rated voltage.\n"
                    r_index += 1

        elif(subcategory == 7):             # GaAs transistor
            if(harsh):
                if(Poper > 0.70 * Prate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating power > 70% rated power.\n"
                    r_index += 1
                if(Voper > 0.70 * Vrate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage > 70% rated voltage.\n"
                    r_index += 1
                if(Tjunc > 135.0):
                    overstress = True
                    reason = reason + str(r_index) + ". Junction temperature > 125.0C.\n"
                    r_index += 1
            else:
                if(Poper > 0.90 * Prate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating power > 90% rated power.\n"
                    r_index += 1
                if(Voper > 0.90 * Vrate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage > 90% rated voltage.\n"
                    r_index += 1

        elif(subcategory > 7):              # Silicon transistor
            if(harsh):
                if(Poper > 0.70 * Prate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating power > 70% rated power.\n"
                    r_index += 1
                if(Voper > 0.75 * Vrate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage > 70% rated voltage.\n"
                    r_index += 1
                if(Tjunc > 125.0):
                    overstress = True
                    reason = reason + str(r_index) + ". Junction temperature > 125.0C.\n"
                    r_index += 1
            else:
                if(Poper > 0.90 * Prate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating power > 90% rated power.\n"
                    r_index += 1
                if(Voper > 0.90 * Vrate):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage > 90% rated voltage.\n"
                    r_index += 1

    elif(category == 10):                   # Switching Device
        # TODO: Add contact power overstress calculations for switches
        Aidx = partmodel.get_value(partrow, 5)
        Ioper = partmodel.get_value(partrow, 62)
        Irated = partmodel.get_value(partrow, 92)

        if(subcategory == 71):              # Circuit Breaker
            if(Ioper > 0.8 * Irated):
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 80% rated current.\n"
                r_index += 1

        else:
            if(harsh):
                if(Aidx == 1 and Ioper > 0.75 * Irated):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current > 75% rated current.\n"
                    r_index += 1
                elif(Aidx == 2 and Ioper > 0.75 * Irated):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current > 75% rated current.\n"
                    r_index += 1
                elif(Aidx == 3 and Ioper > 0.40 * Irated):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current > 40% rated current.\n"
                    r_index += 1
            else:
                if(Aidx == 1 and Ioper > 0.90 * Irated):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current > 90% rated current.\n"
                    r_index += 1
                elif(Aidx == 2 and Ioper > 0.90 * Irated):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current > 90% rated current.\n"
                    r_index += 1
                elif(Aidx == 3 and Ioper > 0.50 * Irated):
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current > 50% rated current.\n"
                    r_index += 1

    return(overstress, reason)


def similar_hazard_rate(component, new_qual, new_environ, new_temp):

    """
    Calculates the estimated hazard rate of a similar item based on
    differences in quality level, environment, and operating temperature.

    All conversion factors come from Reliability Toolkit: Commercial Practices
    Edition, Section 6.3.3.

    Keyword Arguments:
    component   -- the Component Object to perform calculations on.
    new_qual    -- the quality level of the new item.
    new_environ -- the environment of the new item.
    new_temp    -- the operating temperature of the new item.

    Returns:
    hr_similar -- the estimated hazard rate for the new item.

    To convert from quality A to quality B use conversion factors from
    Table 6.3.3-1 (reproduced below).

                  |           |    Full   |           |           |
                  |   Space   |  Military | Ruggedized| Commercial|
    --------------+-----------+-----------+-----------+-----------+
    Space         |    1.0    |    0.8    |    0.5    |    0.2    |
    --------------+-----------+-----------+-----------+-----------+
    Full Military |    1.3    |    1.0    |    0.6    |    0.3    |
    --------------+-----------+-----------+-----------+-----------+
    Ruggedized    |    2.0    |    1.7    |    1.0    |    0.4    |
    --------------+-----------+-----------+-----------+-----------+
    Commercial    |    5.0    |    3.3    |    2.5    |    1.0    |
    --------------+-----------+-----------+-----------+-----------+

    To convert from environment A to environment B use the conversion
    factors from Table 6.3.3-2 (reproduced below).

                  |  GB   |  GM   |  NS   |  AIC  |  ARW  |  SF   |
    --------------+-------+-------+-------+-------+-------+-------+
    GB            |  1.0  |  0.2  |  0.3  |  0.3  |  0.1  |  1.1  |
    --------------+-------+-------+-------+-------+-------+-------+
    GM            |  5.0  |  1.0  |  1.4  |  1.4  |  0.5  |  5.0  |
    --------------+-------+-------+-------+-------+-------+-------+
    NS            |  3.3  |  0.7  |  1.0  |  1.0  |  0.3  |  3.3  |
    --------------+-------+-------+-------+-------+-------+-------+
    AIC           |  3.3  |  0.7  |  1.0  |  1.0  |  0.3  |  3.3  |
    --------------+-------+-------+-------+-------+-------+-------+
    ARW           | 10.0  |  2.0  |  3.3  |  3.3  |  1.0  | 10.0  |
    --------------+-------+-------+-------+-------+-------+-------+
    SF            |  0.9  |  0.2  |  0.3  |  0.3  |  0.1  |  1.0  |
    --------------+-------+-------+-------+-------+-------+-------+

    To convert from temperature A to temperature B (both in Celcius) use
    conversion factors from Table 6.3.3-3 (reproduced below).

                 |  10  |  20  |  30  |  40  |  50  |  60  |  70  |
    -------------+------+------+------+------+------+------+------+
    10           |  1.0 |  0.9 |  0.8 |  0.8 |  0.7 |  0.5 |  0.4 |
    -------------+------+------+------+------+------+------+------+
    20           |  1.1 |  1.0 |  0.9 |  0.8 |  0.7 |  0.6 |  0.5 |
    -------------+------+------+------+------+------+------+------+
    30           |  1.2 |  1.1 |  1.0 |  0.9 |  0.8 |  0.6 |  0.5 |
    -------------+------+------+------+------+------+------+------+
    40           |  1.3 |  1.2 |  1.1 |  1.0 |  0.9 |  0.7 |  0.6 |
    -------------+------+------+------+------+------+------+------+
    50           |  1.5 |  1.4 |  1.2 |  1.1 |  1.0 |  0.8 |  0.7 |
    -------------+------+------+------+------+------+------+------+
    60           |  1.9 |  1.7 |  1.6 |  1.5 |  1.2 |  1.0 |  0.8 |
    -------------+------+------+------+------+------+------+------+
    70           |  2.4 |  2.2 |  1.9 |  1.8 |  1.5 |  1.2 |  1.0 |
    -------------+------+------+------+------+------+------+------+
    """

    qual_factor = [[1.0, 0.8, 0.5, 0.2],
                   [1.3, 1.0, 0.6, 0.3],
                   [2.0, 1.7, 1.0, 0.4],
                   [5.0, 3.3, 2.5, 1.0],
                   [1.0, 1.0, 1.0, 1.0]]

    if(component.model.get_value(component.selected_row, 85) == 1):
        base_qual = 0
    elif(component.model.get_value(component.selected_row, 85) == 2):
        base_qual = 1
    elif(component.model.get_value(component.selected_row, 85) == 3):
        base_qual = 2
    elif(component.model.get_value(component.selected_row, 85) == 4):
        base_qual = 3
    else:
        base_qual = 4

    quality = qual_factor[base_qual][new_qual]

    environ_factor = [[1.0, 0.2, 0.3, 0.3, 0.1, 1.1],
                      [5.0, 1.0, 1.4, 1.4, 0.5, 5.0],
                      [3.3, 0.7, 1.0, 1.0, 0.3, 3.3],
                      [3.3, 0.7, 1.0, 1.0, 0.3, 3.3],
                      [10.0, 2.0, 3.3, 3.3, 1.0, 10.0],
                      [0.9, 0.2, 0.3, 0.3, 0.1, 1.0],
                      [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]

    if(component.system_model.get_value(component.system_selected_row, 22) == 1):
        base_environ = 0
    elif(component.system_model.get_value(component.system_selected_row, 22) == 3):
        base_environ = 1
    elif(component.system_model.get_value(component.system_selected_row, 22) == 4):
        base_environ = 2
    elif(component.system_model.get_value(component.system_selected_row, 22) == 6):
        base_environ = 3
    elif(component.system_model.get_value(component.system_selected_row, 22) == 10):
        base_environ = 4
    elif(component.system_model.get_value(component.system_selected_row, 22) == 11):
        base_environ = 5
    else:
        base_environ = 6

    environ = environ_factor[base_environ][new_environ]

    temp_factor = [[1.0, 0.9, 0.8, 0.8, 0.7, 0.5, 0.4],
                   [1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5],
                   [1.2, 1.1, 1.0, 0.9, 0.8, 0.6, 0.5],
                   [1.3, 1.2, 1.1, 1.0, 0.9, 0.7, 0.6],
                   [1.5, 1.4, 1.2, 1.1, 1.0, 0.8, 0.7],
                   [1.9, 1.7, 1.6, 1.5, 1.2, 1.0, 0.8],
                   [2.4, 2.2, 1.9, 1.8, 1.5, 1.2, 1.0]]

    base_temp = component.system_model.get_value(component.system_selected_row, 80)
    temp = temp_factor[base_temp][new_temp]

    hr_similar = 1 / ((1 / component.system_model.get_value(component.system_selected_row, 28)) * quality * environ * temp)

    return(hr_similar)


def dormant_hazard_rate(category, subcategory, active_env, dormant_env, lambdaa):

    """
    Calculates the dormant hazard rate based on active environment, dormant
    environment, and component category.

    Keyword Arguments:
    category    -- the component category index.
    subcategory -- the component subcategory index.
    active_env  -- the active environment index.
    dormant_env -- the dormant environment index.
    lambdaa     -- the active hazard rate of the component.

    All conversion factors come from Reliability Toolkit: Commercial
    Practices Edition, Section 6.3.4, Table 6.3.4-1 (reproduced below).

                  |Ground |Airborne|Airborne|Naval  |Naval  |Space  |Space  |
                  |Active |Active  |Active  |Active |Active |Active |Active |
                  |to     |to      |to      |to     |to     |to     |to     |
                  |Ground |Airborne|Ground  |Naval  |Ground |Space  |Ground |
                  |Passive|Passive |Passive |Passive|Passive|Passive|Passive|
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Integrated    | 0.08  |  0.06  |  0.04  | 0.06  | 0.05  | 0.10  | 0.30  |
    Circuits      |       |        |        |       |       |       |       |
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Diodes        | 0.04  |  0.05  |  0.01  | 0.04  | 0.03  | 0.20  | 0.80  |
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Transistors   | 0.05  |  0.06  |  0.02  | 0.05  | 0.03  | 0.20  | 1.00  |
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Capacitors    | 0.10  |  0.10  |  0.03  | 0.10  | 0.04  | 0.20  | 0.40  |
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Resistors     | 0.20  |  0.06  |  0.03  | 0.10  | 0.06  | 0.50  | 1.00  |
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Switches      | 0.40  |  0.20  |  0.10  | 0.40  | 0.20  | 0.80  | 1.00  |
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Relays        | 0.20  |  0.20  |  0.04  | 0.30  | 0.08  | 0.40  | 0.90  |
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Connectors    | 0.005 |  0.005 |  0.003 | 0.008 | 0.003 | 0.02  | 0.03  |
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Circuit       | 0.04  |  0.02  |  0.01  | 0.03  | 0.01  | 0.08  | 0.20  |
    Boards        |       |        |        |       |       |       |       |
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Transformers  | 0.20  |  0.20  |  0.20  | 0.30  | 0.30  | 0.50  | 1.00  |
    --------------+-------+--------+--------+-------+-------+-------+-------+
    """

    factor = [[0.08, 0.06, 0.04, 0.06, 0.05, 0.10, 0.30, 0.00],
              [0.04, 0.05, 0.01, 0.04, 0.03, 0.20, 0.80, 0.00],
              [0.05, 0.06, 0.02, 0.05, 0.03, 0.20, 1.00, 0.00],
              [0.10, 0.10, 0.03, 0.10, 0.04, 0.20, 0.40, 0.00],
              [0.20, 0.06, 0.03, 0.10, 0.06, 0.50, 1.00, 0.00],
              [0.40, 0.20, 0.10, 0.40, 0.20, 0.80, 1.00, 0.00],
              [0.20, 0.20, 0.04, 0.30, 0.08, 0.40, 0.90, 0.00],
              [0.005, 0.005, 0.003, 0.008, 0.003, 0.02, 0.03, 0.00],
              [0.04, 0.02, 0.01, 0.03, 0.01, 0.08, 0.20, 0.00],
              [0.20, 0.20, 0.20, 0.30, 0.30, 0.50, 1.00, 0.00]]

# First find the component category/subcategory index.
    if(category == 1):                      # Capacitor
        c_index = 3
    elif(category == 2):                    # Connection
        c_index = 7
    elif(category == 3):                    # Inductive Device.
        if(subcategory > 1):                # Transformer
            c_index = 9
    elif(category == 4):                    # Integrated Circuit
        c_index = 0
    elif(category == 7):                    # Relay
        c_index = 6
    elif(category == 8):                    # Resistor
        c_index = 4
    elif(category == 9):                    # Semiconductor
        if(subcategory > 0 and
           subcategory < 7):                # Diode
            c_index = 1
        elif(subcategory > 6 and
             subcategory < 14):             # Transistor
            c_index = 2
    elif(category == 10):                   # Switching Device
        c_index = 5

# Now find the appropriate active to passive environment index.
    if(active_env > 0 and
       active_env < 4):                     # Ground
        if(dormant_env == 1):               # Ground
            e_index = 0
        else:
            e_index = 7
    elif(active_env > 3 and
         active_env < 6):                   # Naval
        if(dormant_env == 1):               # Ground
            e_index = 4
        elif(dormant_env == 2):             # Naval
            e_index = 3
        else:
            e_index = 7
    elif(active_env > 5 and
         active_env < 11):                  # Airborne
        if(dormant_env == 1):               # Ground
            e_index = 2
        elif(dormant_env == 3):             # Airborne
            e_index = 1
        else:
            e_index = 7
    elif(active_env == 11):                 # Space
        if(dormant_env == 1):               # Ground
            e_index = 6
        elif(dormant_env == 4):             # Space
            e_index = 5
        else:
            e_index = 7

    try:
        lambdad = lambdaa * factor[c_index - 1][e_index]
    except:
        lambdad = 0.0

    return(lambdad)


def criticality_analysis(_CA_, _ItemCA_, _RPN_):
    """
    Function to perform criticality calculations for FMECA.

    Keyword Arguments:
    _CA_     -- list containing inputs for the MIL-STD-1629A mode criticality
                calculation.
    _ItemCA_ -- list containing inputs for the MIL-STD-1629A item criticality
                calculation.
    _RPN_    -- list containing inputs for the automotive criticality
                calculation.
    """

    fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

    _item_crit = u''

# First, calculate the mode criticality and assign result to position 4.
# Second, calculate the mode failure rate and assign result to position 5.
# Third, calculate the item criticality and assign result to position 6.
    _keys = _CA_.keys()
    for i in range(len(_keys)):
        _CA_[_keys[i]][4] = _CA_[_keys[i]][0] * _CA_[_keys[i]][1] * _CA_[_keys[i]][2] * _CA_[_keys[i]][3]
        _CA_[_keys[i]][5] = _CA_[_keys[i]][1] * _CA_[_keys[i]][2]

# Now calculate the item criticality in accordance with MIL-STD-1629A.
    _keys = _ItemCA_.keys()
    for i in range(len(_keys)):
        _cats = sorted(list(set([j[1] for j in _ItemCA_[_keys[i]]])))
        for k in range(len(_cats)):
            _crit = 0.0
            _modes = [j[0] for j in _ItemCA_[_keys[i]] if j[1] == _cats[k]]
            for l in range(len(_modes)):
                _crit += _CA_[_modes[l]][4]

            _item_crit = _item_crit + _cats[k] + ": " + str(fmt.format(_crit)) + "\n"

        _ItemCA_[_keys[i]].append(_item_crit)

# Now calculate the RPN criticality.
    _keys = _RPN_.keys()
    for i in range(len(_keys)):
        _RPN_[_keys[i]][3] = _RPN_[_keys[i]][0] * _RPN_[_keys[i]][1] * _RPN_[_keys[i]][2]
        _RPN_[_keys[i]][7] = _RPN_[_keys[i]][4] * _RPN_[_keys[i]][5] * _RPN_[_keys[i]][6]

    return(_CA_, _ItemCA_, _RPN_)


def moving_average(_data_, n=3):
    """
    Function to calculate the moving average of a dataset.

    Keyword Arguments:
    _data_ -- the dataset for which to find the moving average.
    n      -- the desired period.
    """

    import numpy as np

    _cumsum_ = np.cumsum(_data_, dtype=float)

    return (_cumsum_[n - 1:] - _cumsum_[:1 - n]) / n


def calculate_field_ttf(_dates_):
    """
    Function to calculate the time to failure (TTF) of field incidents.

    Keyword Arguments:
    _dates_ -- tuple containing start and end date for calculating
               time to failure.
    """

    from datetime import datetime

    _start = datetime(*time.strptime(_dates_[0], "%Y-%m-%d")[0:5]).date()
    _fail = datetime(*time.strptime(_dates_[1], "%Y-%m-%d")[0:5]).date()
    ttf = _fail - _start

    return(ttf.days)


def kaplan_meier(_dataset_, _reltime_, _conf_=0.75, _type_=3):
    """
    Function to calculate the Kaplan-Meier survival function estimates.

    Keyword Arguments:
    _dataset_  -- list of tuples where each tuple is in the form of:
                  (Left of Interval, Right of Interval, Event Status) and
                  event status are:
                  0 = right censored
                  1 = event at time
                  2 = left censored
                  3 = interval censored
    _reltime_  -- time at which to stop analysis (helps eliminate stretched
                  plots due to small number of events at high hours).
    _conf_     -- the confidence level of the KM estimates (default is 75%).
    _type_     -- the confidence interval type for the KM estimates.
    """

    from scipy.stats import norm

    # Eliminate zero time failures and failures occurring after any
    # user-supplied upper limit.
    _dataset_ = [i for i in _dataset_ if i[0] >= 0.0]
    if(_reltime_ != 0.0):
        _dataset_ = [i for i in _dataset_ if i[0] <= _reltime_]
        times = [i[0] for i in _dataset_ if i[0] <= _reltime_]
        times2 = [i[1] for i in _dataset_ if i[0] <= _reltime_]
        status = [i[2] for i in _dataset_ if i[0] <= _reltime_]

    for i in range(len(status)):
        if(status[i] == "Right Censored"):
            status[i] = 0
        elif(status[i] == "Left Censored"):
            status[i] = 2
        elif(status[i] == "Interval Censored"):
            status[i] = 3
        else:
            status[i] = 1

    # If Rpy2 is available, we will use that to perform the KM estimations.
    # Returns an object with the following fields:
    #    0 = total number of subjects in each curve.
    #    1 = the time points at which the curve has a step.
    #    2 = the number of subjects at risk at t.
    #    3 = the number of events that occur at time t.
    # 4 = the boolean inverse of three.
    #    5 = the estimate of survival at time t+0. This may be a vector or a
    #        matrix.
    #    6 = type of survival censoring.
    #    7 = the standard error of the cumulative hazard or -log(survival).
    #    8 = upper confidence limit for the survival curve.
    #    9 = lower confidence limit for the survival curve.
    #   10 = the approximation used to compute the confidence limits.
    #   11 = the level of the confidence limits, e.g. 90 or 95%.
    #   12 = the returned value from the na.action function, if any.
    #        It will be used in the printout of the curve, e.g., the number of
    #        observations deleted due to missing values.
    if(__USE_RPY__):
        print "Probably using Windoze."

    elif(__USE_RPY2__):
        survival = importr('survival')

        times = robjects.FloatVector(times)
        times2 = robjects.FloatVector(times2)
        status = robjects.IntVector(status)

        surv = survival.Surv(times, times2, status, type='interval')
        robjects.globalenv['surv'] = surv
        fmla = robjects.Formula('surv ~ 1')
        _KM_ = survival.survfit(fmla)

        # Every subject must have a censored time to use survrec.
        #survrec = importr('survrec')
        #units = robjects.StrVector(units)
        #survr = survrec.Survr(units, times2, status2)
        #fit = survrec.wc_fit(survr)

        return(_KM_)

    else:

        # Determine the confidence bound z-value.
        _z_norm_ = norm.ppf(_conf_)

        # Get the total number of events.
        _n_ = len(_dataset_)
        N = _n_

        _KM_ = []
        _Sh_ = 1.0
        muhat = 0.0
        var = 0.0
        z = 0.0
        ti = float(_dataset_[0][0])
        tj = 0.0
        i = 0

        while (_n_ > 0):
            # Find the total number of failures and
            # suspensions in interval [i - 1, i].
            _d_ = len([t for t in _dataset_ if (t[0] == _dataset_[i][0] and t[1] == 1)])
            _s_ = len([t for t in _dataset_ if (t[0] == _dataset_[i][0] and t[1] == 0)])

            # Estimate the probability of failing in interval [i - 1, i].
            _Si_ = 1.0 - (float(_d_) / float(_n_))

            # Estimate the probability of survival up to time i [S(ti)].
            _Sh_ = _Si_ * _Sh_

            # Calculate the standard error for S(ti).
            z = z + 1.0 / ((_n_ - _d_ + 1) * _n_)
            _se_ = sqrt(_Si_ * _Si_ * z)

            # Calculate confidence bounds for S(ti).
            _ll_ = _Sh_ - _z_norm_ * _se_
            _ul_ = _Sh_ + _z_norm_ * _se_
            if(_type_ == 1 or _ul_ > 1.0):
                _ul_ = _Sh_
            if(_type_ == 2 or _ll_ < 0.0):
                _ll_ = _Sh_

            # Calculate the cumulative hazard rate.
            try:
                _H_ = -log(_Sh_)
            except ValueError:
                _H_ = _H_

            # Calculate the mean.
            muhat = muhat + _Sh_ * (ti - tj)
            tj = ti
            ti = _dataset_[i][0]

            _KM_.append([ti, _n_, _d_, _Si_, _Sh_, _se_, _ll_, _ul_, _H_, muhat, var])
            #if(_s_ > 0):
            #    _KM_.append([str(_dataset_[i][0]) + '+', _n_, _s_, '-', _Sh_,
            #                 _se_, _ll_, _ul_, _H_])

            _n_ = _n_ - _d_ - _s_
            i = i + _d_ + _s_

        return(_KM_)


def mean_cumulative_function(units, times, data, _conf_=0.75):
    """ This function estimates the mean cumulative function for a population
        of items.

        Keyword Argumesnts:
        units  -- list of unique unit ID's in the dataset.
        times  -- list of unique failure times in the dataset.
        data   -- a data.frame or matrix where:
                  Column 0 is the failed unit id.
                  Column 1 is the left of the interval.
                  Column 2 is the right of the interval.
                  Column 3 is the interarrival time.
        _conf_ -- the confidence level of the KM estimates (default is 75%).
    """

    from scipy.stats import norm

    # Determine the confidence bound z-value.
    _z_norm_ = norm.ppf(_conf_)

    _m_ = len(units)
    _n_ = len(times)

    datad = []

    for i in range(len(data)):
        datad.append(data[i])
    data = np.asarray(data)
    datad = np.asarray(datad)

    _d_ = np.zeros(shape=(_m_, _n_))
    _delta_ = np.zeros(shape=(_m_, _n_))

    for i in range(_n_):
        k = np.where(data[:, 2] == str(times[i]))    # Array of indices with failure times equal to the current unique failure time.
        _u_ = np.array(data[k, 0])[0].tolist()       # List of units whose failure time is equal to the current unique failure time.
        for j in range(len(_u_)):
            k = [a for a, x in enumerate(units) if x == _u_[j]]     #
            _delta_[k, 0:i+1] = 1

    for i in range(_n_):
        k = np.where(datad[:, 2] == str(times[i]))   # Array of indices with failure times equal to the current unique failure time.
        _u_ = np.array(datad[k, 0])[0].tolist()      # List of units whose failure time is equal to the current unique failure time.
        for j in range(len(_u_)):
            k = [a for a, x in enumerate(units) if x == _u_[j]]     #
            _d_[k, i] += 1

    _delta_ = _delta_.transpose()
    _d_ = _d_.transpose()

    _delta_dot = _delta_.sum(axis=1)
    _d_dot = (_d_ * _delta_).sum(axis=1)
    _d_bar = _d_dot / _delta_dot

    _MCF_ = []
    _x_ = (_delta_.transpose() / _delta_dot).transpose()
    _y_ = (_d_.transpose() - _d_bar).transpose()
    for i in range(len(times)):
        muhat = _d_bar[0:i+1].sum(axis=0)

        # Estimate the variance.
        _z_ = (_x_[0:i+1] * _y_[0:i+1])
        _var_ = ((_z_.sum(axis=0))**2).sum(axis=0)

        _ll_ = muhat - _z_norm_ * sqrt(_var_)
        _ul_ = muhat + _z_norm_ * sqrt(_var_)

        _MCF_.append([times[i], _delta_[i], _d_[i], _delta_dot[i], _d_dot[i], _d_bar[i], _var_, _ll_, _ul_, muhat])

    return(_MCF_)


def parametric_fit(_dataset_, _starttime_, _reltime_,
                   _fitmeth_, _dist_='exponential'):
    """ Function to fit data to a parametric distribution and estimate the
        parameters.

        Keyword Arguments:
        _dataset_ -- the dataset to fit.  This is a
        _reltime_ -- the maximum time to include in the fit.  Used to exclude
                     outliers.
        _fitmeth_ -- method used to fit data to the selected distribution.
                     1 = rank regression
                     2 = maximum likelihood estimation (MLE)
        _dist_    -- the noun name of the distribution to fit.  Defaults to
                     the exponential distribution.
    """

    # Eliminate zero time failures and failures occurring after any
    # user-supplied upper limit.
    _dataset_ = [i for i in _dataset_ if i[2] > _starttime_]
    _dataset_ = [i for i in _dataset_ if i[2] <= _reltime_]

    if(__USE_RPY__):
        print "Probably using Windoze."

    elif(__USE_RPY2__):

        Rbase = importr('base')

        if(_fitmeth_ == 1):                 # MLE
            if(_dist_ == 'exponential'):
                _dist_ = 'exp'
            elif(_dist_ == 'lognormal'):
                _dist_ = 'lnorm'
            elif(_dist_ == 'normal'):
                _dist_ = 'norm'

            left = [i[1] for i in _dataset_]
            right = [i[2] for i in _dataset_]
            for i in range(len(_dataset_)):
                if(_dataset_[i][4] == 0):
                    right[i] = 'NA'
                elif(_dataset_[i][4] == 1):
                    left[i] = right[i]
                elif(_dataset_[i][4] == 2):
                    left[i] = 'NA'

            od = rlc.OrdDict([('left', robjects.FloatVector(left)),
                              ('right', robjects.FloatVector(right))])

            censdata = robjects.DataFrame(od)
            n_row = Rbase.nrow(censdata)
            if(n_row[0] > 1):
                fitdistrplus = importr('fitdistrplus')
                try:
                    fit = fitdistrplus.fitdistcens(censdata, _dist_)
                except ri.RRuntimeError:
                    return(True)
                    return(True)
                #para=R.list(scale=fit[0][1], shape=fit[0][0])
                #fitdistrplus.plotdistcens(censdata, _dist_, para)
            else:
                return(True)

        elif(_fitmeth_ == 2):               # Regression
            if(_dist_ == 'normal'):
                _dist_ = 'gaussian'

            if(_reltime_ != 0.0):
                time = [i[1] + 0.01 for i in _dataset_ if i[2] <= _reltime_]
                time2 = [i[2] + 0.01 for i in _dataset_ if i[2] <= _reltime_]
                status = [i[4] for i in _dataset_ if i[2] <= _reltime_]

            survival = importr('survival')

            for i in range(len(status)):
                if(status[i] == 'Right Censored'):
                    status[i] = 0
                elif(status[i] == 'Event'):
                    status[i] = 1
                elif(status[i] == 'Left Censored'):
                    status[i] = 2
                else:
                    status[i] = 3

            time = robjects.FloatVector(time)
            time2 = robjects.FloatVector(time2)
            status = robjects.IntVector(status)

            surv = survival.Surv(time, time2, status, type='interval')
            robjects.globalenv['surv'] = surv
            formula = robjects.Formula('surv ~ 1')

            fit = survival.survreg(formula, dist=_dist_)

    else:
        print "No R"

    return(fit)


def bathtub_filter(_dataset_, _starttime_, _reltime_, _step_):
    """
    Function to explore early life to useful life and useful life to wearout
    transition times.

    Keyword aAguments:
    _dataset_    -- the dataset to perform the search on.
    _starttime_ -- the time to start the search.
    _endtime_   -- the time to end the search.
    _step_      -- how large the time increment should be.
    """

    # Initialize scalar variables.
    start = int(_starttime_)
    end = int(_reltime_)

    # Initialize list variables.
    times = []
    scale = [0]
    shape = [0]
    deltascale = []
    deltashape = []

    for i in range(start, end, _step_):
        fit = parametric_fit(_dataset_, i, end, 1, _dist_='weibull')

        if(fit is True):
            continue

        j = int(((i - _starttime_) / _step_)) + 1
        try:
            shape.append(fit[0][0])
            scale.append(fit[0][1])
            _deltascale = (scale[j] - scale[j - 1]) / scale[j - 1]
            _deltashape = (shape[j] - shape[j - 1]) / shape[j - 1]
        except ZeroDivisionError:
            try:
                _deltascale = deltascale[j - 1]
                _deltashape = deltashape[j - 1]
            except IndexError:
                _deltascale = 0.0
                _deltashape = 0.0
        except IndexError:
            print i, j
            _deltascale = 0.0
            _deltashape = 0.0
        deltascale.append(_deltascale * 100.0)
        deltashape.append(_deltashape * 100.0)

        times.append(i)

    return(scale, deltascale, shape, deltashape, times)


def theoretical_distribution(_data_, _distr_, _para_):

    Rbase = importr('base')

# Create the R density and probabilty distribution names.
    ddistname = R.paste('d', _distr_, sep='')
    pdistname = R.paste('p', _distr_, sep='')

# Calculate the minimum and maximum values for x.
    xminleft = min([i[0] for i in _data_ if i[0] != 'NA'])
    xminright = min([i[1] for i in _data_ if i[1] != 'NA'])
    xmin = min(xminleft, xminright)

    xmaxleft = max([i[0] for i in _data_ if i[0] != 'NA'])
    xmaxright = max([i[1] for i in _data_ if i[1] != 'NA'])
    xmax = max(xmaxleft, xmaxright)

    xrange = xmax - xmin
    xmin = xmin - 0.3 * xrange
    xmax = xmax + 0.3 * xrange

# Creat a list of probabilities for the theoretical distribution with the
# estimated parameters.
    den = float(len(_data_))
    densfun = R.get(ddistname, mode='function')
    nm = R.names(_para_)
    f = R.formals(densfun)
    args = R.names(f)
    m = R.match(nm, args)
    s = R.seq(xmin, xmax, by=(xmax - xmin) / den)
    theop = Rbase.do_call(pdistname, R.c(R.list(s), _para_))

    return(theop)


def calculate_rg_phase(model, row, GR, MS, FEF, Prob, ti):
    """
    Function to calculate the values for an individual reliability growth
    phase.

    Keyword Arguments:
    model -- the gtk.TreeModel containing the RG phase information.
    row   -- the selected gtk.Iter containning the specific RG phase
             information.
    MS    -- the management strategy for this program.
    FEF   -- the average FEF for this program.
    Prob  -- the probability of seeing one failure.
    ti    -- the growth start time; time to first fix for this program.
    """

# Read the RG phase-specific values.
    TTTi = model.get_value(row, 4)
    MTBFi = model.get_value(row, 6)
    MTBFf = model.get_value(row, 7)
    MTBFa = model.get_value(row, 8)

# Calculate the average growth rate for the phase.
    if(GR == 0.0 or GR == '' or GR is None):
        try:
            GRi = -log(TTTi / ti) - 1.0 + sqrt((1.0 + log(TTTi / ti))**2.0 + 2.0 * log(MTBFf / MTBFi))
        except(ValueError, ZeroDivisionError):
            GRi = 0.0
    else:
        GRi = GR

    model.set_value(row, 5, GRi)

# Calculate initial MTBF for the phase.
    if(MTBFi == 0.0 or MTBFi == '' or MTBFi is None):
        try:
            MTBFi = (-1.0 * ti * MS) / log(1.0 - Prob)
        except(ValueError, ZeroDivisionError):
            try:
                MTBFi = MTBFf / exp(GRi * (0.5 * GRi + log(TTTi / ti) + 1.0))
            except(ValueError, ZeroDivisionError):
                try:
                    MTBFi = (ti * (TTTi / ti)**(1.0 - GRi)) / Ni
                except(ValueError, ZeroDivisionError):
                    MTBFi = 0.0
        model.set_value(row, 6, MTBFi)

# Calculate final MTBF for the phase.
    if(MTBFf == 0.0 or MTBFf == '' or MTBFf is None):
        try:
            MTBFf = MTBFi * exp(GRi * (0.5 * GRi + log(TTTi / ti) + 1.0))
        except (ValueError, ZeroDivisionError):
            MTBFf = 0.0
        model.set_value(row, 7, MTBFf)

# Calculate total test time for the phase.
    if(TTTi == 0.0 or TTTi == '' or TTTi is None):
        try:
            TTTi = exp(log(ti) + 1.0 / GRi * (log(MTBFf /MTBFi) + log(1.0 - GRi)))
        except(ValueError, ZeroDivisionError):
            TTTi = 0.0
        model.set_value(row, 4, TTTi)

    return(GRi, TTTi)


def calculate_rgtmc(F, X, I, _grouped=False):
    """
    Function to estimate the parameters (beta and lambda) of the AMSAA-Crow
    continous model using either the Option for Individual Failure Data
    (default) or the Option for Grouped Failure Data.

    Keyword Arguments:
    F -- list of failure counts.
    X -- list of individual failures times.
    I -- the grouping interval width.
    _grouped -- whether or not to use grouped data.
    """

    from scipy.optimize import fsolve

# Define the function that will be set equal to zero and solved for beta.
    def _beta(b, f, t, logt):
        """ Function for estimating the beta value from grouped data. """

        return(sum(f[1:] * ((t[1:]**b * logt[1:] - t[:-1]**b * logt[:-1]) / (t[1:]**b - t[:-1]**b) - log(max(t)))))

# Find the total time on test.
    TTT = X[len(X) - 1:][0]
    FFF = sum(F)

    _rho = []
    _mu = []

    if(not _grouped):
        for i in range(len(X)):
            try:
                _iters = int(X[i] - X[i - 1])
            except IndexError:
                _iters = int(X[i])

# Estimate the failure rate of this interval.
            for j in range(_iters - 1):
                _rho.append(np.nan)

            try:
                _rho_ = F[i] / (X[i] - X[i - 1])
            except IndexError:
                _rho_ = F[i] / X[i]
            except ZeroDivisionError:
                _rho_ = _rho[i - 1]

            if(_rho_ < 0):
                _rho_ = 0.0
            _rho.append(_rho_)

# Estimate the MTBF of this interval.
            for j in range(_iters - 1):
                _mu.append(np.nan)

            try:
                _mu_ = (X[i] - X[i - 1]) / F[i]
            except IndexError:
                _mu_ = X[i] / F[i]
            except ZeroDivisionError:
                _mu_ = _mu[i - 1]

            if(_mu_ < 0):
                _mu_ = 0.0

            _mu.append(_mu_)

        logX = [log(x) for x in X]

        _beta_hat = (FFF / (FFF * log(TTT) - sum(logX)))
        _lambda_hat = FFF / TTT**_beta_hat

    elif(_grouped):
# Calculate the number of intervals we need, then create a list of zeros the
# same length as the number of intervals.
        _num_intervals = int(ceil(TTT / I))
        _cum_fails = [0] * _num_intervals

# Iterate through the data and count the nuber of failures in each interval.
        for i in range(len(X)):
            for j in range(_num_intervals):
                if(X[i] > j * I and X[i] <= (j + 1) * I):
                    _cum_fails[j] += F[i]

        for j in range(_num_intervals):
# Estimate the failure rate of this interval.
            try:
                _rho.extend([_cum_fails[j] / I] * (int(I) - 1))
            except ZeroDivisionError:
                try:
                    _rho.extend([_rho[j - 1]] * (int(I) - 1))
                except IndexError:
                    _rho.extend([0.0] * (int(I) - 1))
            _rho.append(np.nan)

# Estimate the MTBF of this interval.
            try:
                _mu.extend([I / _cum_fails[j]] * (int(I) - 1))
            except ZeroDivisionError:
                try:
                    _mu.extend([_mu[j - 1]] * (int(I) - 1))
                except IndexError:
                    _mu.extend([0.0] * (int(I) - 1))
            _mu.append(np.nan)

        f = [0]
        t = [1]
        logt = [0]
        for i in range(len(X)):
            f.append(F[i])
            t.append(X[i])
            logt.append(log(X[i]))

        f = np.array(f)
        t = np.array(t)
        logt = np.array(logt)

        _beta_hat = fsolve(_beta, 1.0, args=(f, t, logt))[0]
        _lambda_hat = FFF / TTT**_beta_hat

# Append non-plotting values to pad the failure rate and MTBF lists so they
# have the same length as everything else being plotted.
    if(len(_rho) < int(TTT)):
        for j in range(int(TTT) - len(_rho)):
            _rho.append(np.nan)
            _mu.append(np.nan)

    return(_beta_hat, _lambda_hat, _rho, _mu)
