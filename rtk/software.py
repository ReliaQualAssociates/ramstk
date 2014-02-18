#!/usr/bin/env python
""" This is the Class that is used to represent and hold information related
    to the software of the Program. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2009 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       software.py is part of the RTK Project
#
# All rights reserved.

import sys
import pango

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

# Import other RTK modules.
import calculations as _calc
import configuration as _conf
import utilities as _util
import widgets as _widg

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, "")

import gettext
_ = gettext.gettext

# Plotting package.
import matplotlib
matplotlib.use('GTK')
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure


def _test_selection_tree_edit(cell, path, position, model):
    """
    Called whenever a gtk.TreeView CellRenderer is edited for the
    test selection worksheet.

    Keyword Arguments:
    cell     -- the gtk.CellRenderer that was edited.
    path     -- the gtk.Treeview path of the gtk.CellRenderer that was
                edited.
    new_text -- the new text in the edited gtk.CellRenderer.
    position -- the column position of the edited gtk.CellRenderer.
    model    -- the gtk.TreeModel the gtk.CellRenderer belongs to.
    """

    model[path][position] = not cell.get_active()

    return False


class Software:

    # TODO: Write code to update notebook widgets when editing the
    # System treeview.

    """
    The Software class is simply the treeview that holds and displays the
    system tree in the RTK Treebook.
    """

    _gd_tab_labels = [[_("Module Description:"), _("Application Level:"),
                       _("Application Type:"), _("Development Phase:")]]

    _de_labels_ = [_(u"There are separate design and coding organizations."),
                       _(u"There is an independent software test organization."),
                       _(u"There is an independent software quality assurance organization."),
                       _(u"There is an independent software configuration management organization."),
                       _(u"There is an independent software verification and validation organization."),
                       _(u"A structured progamming team will develop the software."),
                       _(u"The educational level of the programming team members is above average."),
                       _(u"The experience level of teh programming team members is above average."),
                       _(u"Standards are defined and will be enforced."),
                       _(u"Software will be developed using a higher order language."),
                       _(u"The development process will include formal reviews (PDR, CDR, etc.)."),
                       _(u"The development process will include frequent walkthroughs."),
                       _(u"Development will take a top-down and structured approach."),
                       _(u"Unit development folders will be used."),
                       _(u"A software development library will be used."),
                       _(u"A formal change and error reporting process will be used."),
                       _(u"Progress and status will routinely be reported."),
                       _(u"System requirements specifications will be documented."),
                       _(u"Software requirements specifications will be documented."),
                       _(u"Interface design specifications will be documented."),
                       _(u"Software design specification will be documented."),
                       _(u"Test plans, procedures, and reports will be documented."),
                       _(u"The software development plan will be documented."),
                       _(u"The software quality assurance plan will be documented."),
                       _(u"The software configuration management plan will be documented."),
                       _(u"A requirements traceability matrix will be used."),
                       _(u"The software version description will be documented."),
                       _(u"All software discrepancies will be documented."),
                       _(u"The software language requirements will be specified."),
                       _(u"Formal program design language will be used."),
                       _(u"Program design graphical techniques (flowcharts, HIPO, etc.) will be used."),
                       _(u"Simulation/emulation tools will be used."),
                       _(u"Configuration management tools will be used."),
                       _(u"A code auditing tool will be used."),
                       _(u"A data flow analyzer will be used."),
                       _(u"A programmer's workbench will be used."),
                       _(u"Measurement tools will be used."),
                       _(u"Software code reviews will be used."),
                       _(u"Software branch testing will be used."),
                       _(u"Random testing will be used."),
                       _(u"Functional testing will be used."),
                       _(u"Error and anomaly detection testing will be used."),
                       _(u"Structure analysis will be used.")]

    _srr_labels_ = [[_(u"There is a standard for handling recognized errors such that all error conditions are passed to the calling function."),
                         _(u"Error tolerances are specified for all applicable external input data (i.e., range of numerical values, legal  combinations of alphanumerical values)."),
                         _(u"There are requirements for detection of and/or recovery from all computational failures."),
                         _(u"There are requirements to range test all critical loop and multiple transfer index parameters before used."),
                         _(u"There are requirements to range test all critical subscript values before use."),
                         _(u"There are requirements to range test all critical output data before final outputting."),
                         _(u"There are requirements for recovery from all detected hardware faults."),
                         _(u"There are requirements for recovery from all I/O divide errors."),
                         _(u"There are requirements for recovery from all communication transmission errors."),
                         _(u"There are requirements for recovery from all failures to communicate with other nodes or other systems."),
                         _(u"There are requirements to periodically check adjacent nodes or operating system for operational status."),
                         _(u"There are requirements to provide a strategy for alternating routing of messages."),
                         _(u"There are requirements to ensure communication paths to all remaining nodes/communication links in the event of a failure of one node/link."),
                         _(u"There are requirements for maintaining the integrity of all data values following the occurence of anomalous conditions."),
                         _(u"There are requirements to enable all disconnected nodes to rejoin the network after recovery, such that the processing functions of the system are not interrupted."),
                         _(u"There are requirements to replicate all cricital data at two or more distinct nodes.")],
                        [_(u"There is a table(s) tracing all of the allocated requirements to the parent system or the subsystem specification.")],
                        [_(u"There are quantitative accuracy requirements for all applicable inputs associated with each applicable function."),
                         _(u"There are quantitative accuracy requirements for all applicable outputs associated with each applicable function."),
                         _(u"There are quantitative accuracy requirements for all applicable constants associated with each applicable function."),
                         _(u"The existing math library routines which are planned for use provide enough precision to support accuracy objectives."),
                         _(u"All processes and functions are partitioned to be logically complete and self contained so as to minimize interface complexity."),
                         _(u"There are requirements for each operational CPU/System to have a separate power source."),
                         _(u"There are requirements for the executive software to perform testing of its own operation and of the communication links, memory devices, and peripheral devices."),
                         _(u"All inputs, processing, and outputs are clearly and precisely defined."),
                         _(u"All defined functions have been referenced."),
                         _(u"All system functions allocated to this module have been allocated to software functions within this module."),
                         _(u"All referenced functions have been defined (i.e., documented with precise inputs, processing, and output requirements)."),
                         _(u"The flow of processing (algorithms) and all decision points (conditions and alternate paths) in the flow  is described for all functions."),
                         _(u"Specific standards have been established for design representations (e.g., HIPO charts, program design language, flow charts, data flow diagrams)."),
                         _(u"Specific standards have been established for calling sequence protocol between software units."),
                         _(u"Specific standards have been established for external I/O protocol and format for all software units."),
                         _(u"Specific standards have been established for error handling for all software units."),
                         _(u"All references to the same function use a single, unique name."),
                         _(u"Specific standards have been established for all data representation in the design."),
                         _(u"Specific standards have been established for the naming of all data."),
                         _(u"Specific standards have been established for the definition and use of global variables."),
                         _(u"There are procedures for establishing consistency and concurrency of multiple copies (e.g., copies at different nodes) of the same software or database version."),
                         _(u"There are procedures for verifying consistency and concurrency of multiple copies (e.g., copies at different nodes) of the same software or database version."),
                         _(u"All references to the same data use a single, unique name.")],
                        [_(u"Number of instances of different processes (or functions, subfunctions) which are required to be executed at the same time (i.e., concurrent processing):"),
                         _(u"Number of instances of concurrent processing that are required to be centrally controlled:"),
                         _(u"Number of error conditions that are required to be recognized/identified:"),
                         _(u"Number of recognized error conditions that require recovery or repair:"),
                         _(u"Number of instances of the same process (or function, subfunction) being required to execute more than once for comparison purposes (i.e., polling of parallel or redundant processing results):"),
                         _(u"Number of instances of parallel/redundant processing that are required to be centrally controlled:")],
                        [_(u"Number of data references that are identified:"),
                         _(u"Number of identified data references that are documented with regard to source, meaning, and format:"),
                         _(u"Number of data items that are identified (e.g., documented with regard to source, meaning, and format):"),
                         _(u"Number of data items that are referenced:")]]

    _pdr_labels_ = [[_(u"There are provisions for recovery from all computational errors."),
                         _(u"There are provisions for recovery from all detected hardware faults (e.g., arithmetic faults, power failure, clock interrupt)."),
                         _(u"There are provisions for recovery from all I/O device errors."),
                         _(u"There are provisions for recovery from all communication transmission errors."),
                         _(u"Error checking information (e.g., checksum, parity bit) is computed and transmitted with all messages."),
                         _(u"Error checking information is computed and compared with all message receptions."),
                         _(u"Transmission retries are limited for all transmissions."),
                         _(u"There are provisions for recovery from all failures to communicate with other nodes or other systems."),
                         _(u"There are provisions to periodically check all adjacent nodes or operating systems for operational status."),
                         _(u"There are provisions for alternate routing of messages."),
                         _(u"Communication paths exist to all remaining nodes/links in the event of a failure of one node/link."),
                         _(u"The integrity of all data values is maintained following the occurence of anomalous conditions."),
                         _(u"All disconnected nodes can rejoin the network after recovery, such that the processing functions of the system are not interrupted."),
                         _(u"All critical data in the module is replicated at two or more distinct nodes")],
                        [_(u"There is a table tracing all the top-level CSC allocated requirements to the parent CSCI specification.")],
                        [_(u"The numerical techniques used in implementing applicable functions provide enough precision to support accuracy objectives."),
                         _(u"All processes and functions are partitioned to be logically complete and self-contained so as to minimize interface complexity."),
                         _(u"The executive software perform testing of its own operation and of the communication links, memory devices, and peripheral devices."),
                         _(u"All inputs, processing, and outputs are clearly and precisely defined."),
                         _(u"All functions of this module been allocated to top-level module."),
                         _(u"All conditions and alternative processing options are defined for each decision point."),
                         _(u"Design representations are in the formats of the established standard."),
                         _(u"All references to the same top-level module use a single, unique name."),
                         _(u"All data representation complies with the established standard."),
                         _(u"The naming of all data complies with the established standard."),
                         _(u"The definition and use of all global variables is in accordange with the established standard."),
                         _(u"There are procedures for establishing consistency and concurrency of multiple copies of the same software or data base version."),
                         _(u"There are procedures for verifying the consistency and concurrency of multiples copies of the same software or data base version."),
                         _(u"All references to the same data use a single, unique name.")],
                        [_(u"Estimated process time typically spent executing the entire module:"),
                         _(u"Estimated process time typically spent in execution of hardware and device interface protocol:"),
                         _(u"Number of data references that are defined:"),
                         _(u"Number of identified data references that are documented with regard to source, meaning, and format:"),
                         _(u"Number of data items that are defined (i.e., documented with regard to source, meaning, and format):"),
                         _(u"Number of data items that are referenced:"),
                         _(u"Number of data references that are identified:"),
                         _(u"Number of identified data references that are computed or obtained from an external source (e.g., referencing global data with preassigned values, input parameters with preassigned values):"),
                         _(u"Number of software discrepancy reports have been recorded, to date:"),
                         _(u"Number of software discrepancy reports have been closed, to date:")]]

    _cdr_labels_ = [[_(u"Values of all applicable external inputs with range specifications are checked with respect to specified range prior to use."),
                         _(u"All applicable external inputs are checked with respect to specified conflicting requests prior to use."),
                         _(u"All applicable external inputs are checked with respect to specified illegal combinations prior to use."),
                         _(u"All applicable external inputs are checked for reasonableness before processing begins."),
                         _(u"All detected errors, with respect to applicable external inputs, are reported before processing begins."),
                         _(u"Critical loop and multiple transfer index parameters (e.g., supporting a mission-critical system function) are checked for out-of-range values before use."),
                         _(u"All critical subscripts (e.g., supporting a mission-critical system function) are checked for out-of-range values before use."),
                         _(u"All critical output data (e.g., supporting a mission-critical system function) are checked for reasonable values prior to final outputting.")],
                        [_(u"The description of each software unit identifies all the requirements that the unit helps satisfy."),
                         _(u"The decomposition of top-level modules into lower-level modules and software units is graphically depicted.")],
                        [_(u"Estimated executable lines of source code in this module:"),
                         _(u"Estimated executable lines of source code necessary to handle hardware and device interface protocol in this module:"),
                         _(u"Number of units in this module:"),
                         _(u"Number of units in this module thsat perform processing of hardware and/or device interface protocol:"),
                         _(u"Estimated processing time typically spent executing this module:"),
                         _(u"Estimated processing time typically spent in execution of hardware and device interface protocol in this module:"),
                         _(u"Number of units that clearly and precisely define all inputs, processing, and outputs:"),
                         _(u"Data references identified in this module:"),
                         _(u"Identified data references that are documented with regard to source, meaning, and format in this module:"),
                         _(u"Data items that are defined (i.e., documented with regard to source, meaning, and format) in this module:"),
                         _(u"Data items are referenced in this module:"),
                         _(u"Data references identified in this module:"),
                         _(u"Identified data references that are computed or obtained from an external source (e.g., referencing global data with preassigned values, input parameters with preassigned values) in this module:"),
                         _(u"Number of units that define all conditions and alternative processing options for each decision point:"),
                         _(u"Number of units in which all parameters in the argument list are used:"),
                         _(u"Number of software discrepancy reports recorded, to date, for this module:"),
                         _(u"Number of software discrepancy reports recorded that have been closed, to date, for this module:"),
                         _(u"Number of units in which all design representations are in the formats of the established standard:"),
                         _(u"Number of units in which the calling sequence protocol (between units) complies with the established standard:"),
                         _(u"Number of units in which the I/O protocol and format complies with the established standard:"),
                         _(u"Number of units in which the handling of errors complies with the established standard:"),
                         _(u"Number of units in which all references to the unit use the same, unique name:"),
                         _(u"Number of units in which the naming of all data complies with the established standard:"),
                         _(u"Number of units in which is the definition and use of all global variables is in accordance with the established standard:"),
                         _(u"Number of units in which references to the same data use a single, unique name:")],
                        [_(u"This unit performs processing of hardware and/or device interface protocols."),
                         _(u"All inputs, processing, and outputs are clearly and precisely defined."),
                         _(u"All conditions and alternative processing options for each decision point are defined."),
                         _(u"All parameters in the argument list are used."),
                         _(u"All design representations are in the formats of the established standard."),
                         _(u"The calling sequence protocol (between units) complies with the established standard."),
                         _(u"The I/O protocol and format complies with the established standard."),
                         _(u"The handling of errors complies with the established standard."),
                         _(u"All references to the unit use the same, unique name."),
                         _(u"The naming of all data complies with the established standard."),
                         _(u"The definition and use of all global variables is in accordance with the established standard."),
                         _(u"References to the same data use a single, unique name.")],
                        [_(u"Estimated executable lines of source code in this unit:"),
                         _(u"Estimated executable lines of source code necessary to handle hardware and device interface protocol in this unit:"),
                         _(u"Estimated processing time typically spent executing this unit:"),
                         _(u"Estimated processing time typically spent in execution of hardware and device interface protocol in this unit:"),
                         _(u"Data references identified in this unit:"),
                         _(u"Identified data references that are documented with regard to source, meaning, and format in this unit:"),
                         _(u"Data items that are defined (i.e., documented with regard to source, meaning, and format) in this unit:"),
                         _(u"Data items are referenced in this unit:"),
                         _(u"Data references identified in this unit:"),
                         _(u"Identified data references that are computed or obtained from an external source (e.g., referencing global data with preassigned values, input parameters with preassigned values) in this unit:"),
                         _(u"Number of software discrepancy reports recorded, to date, for this unit:"),
                         _(u"Number of software discrepancy reports recorded that have been closed, to date, for this unit:")]]

    _trr_labels_ = [[_(u"Number of units in this module:"),
                         _(u"Total executable lines of source code in this module:"),
                         _(u"Total assembly language lines of code in this module:"),
                         _(u"Total higher order language lines of code in this module:")],
                        [_(u"When an error condition is detected resolution of the error is determined by the calling unit."),
                         _(u"A check is performed before processing begins to determine that all data is available.")],
                        [_(u"All inputs, processing, and outputs are clearly and precisely defined for this unit."),
                         _(u"All data references in this unit are defined."),
                         _(u"All data references in this unit are identified."),
                         _(u"All conditions and alternative processing options in this unit are defined for each decision point."),
                         _(u"All parameters in the argument list for this unit are used."),
                         _(u"All design representations in this unit are in the formats of the established standard."),
                         _(u"The between unit calling sequence protocol in this unit complies with the established standard."),
                         _(u"The I/O protocol and format in this unit complies with the established standard."),
                         _(u"The handling of errors in this unit complies with the established standard."),
                         _(u"All references to this unit use the same, unique name."),
                         _(u"All data representation in this unit complies with the established standard."),
                         _(u"The naming of all data in this unit complies with the established standard."),
                         _(u"The definition and use of all global variables in this unit is in accordance with the established standard."),
                         _(u"All references to the same data in this unit use a single, unique name.")],
                        [_(u"Total executable lines of source code in this unit:"),
                         _(u"Total assembly language lines of code in this unit:"),
                         _(u"Number of conditional branch statements (If, While, DO, FOR, Case) in this unit:"),
                         _(u"Number of unconditional branch statements (GOTO, CALL, RETURN) in this unit:")]]

    _ts_tab_labels = [_("Test Confidence Level:"), _("Test Path:"),
                      _("Test Effort:"), _("Test Approach:"),
                      _("Labor Hours for Testing:"),
                      _("Labor Hours for Development:"),
                      _("Budget for Testing:"),
                      _("Budget for Development:"),
                      _("Working Days for Testing:"),
                      _("Working Days for Development:"),
                      _("Number of Branches:"),
                      _("Number of Branches Tested:"),
                      _("Number of Inputs:"),
                      _("Number of Inputs Tested:"),
                      _("Number of Units:"),
                      _("Number of Units Tested:"),
                      _("Number of Interfaces:"),
                      _("Number of Interfaces Tested:"),
                      _("Number of Requirements:"),
                      _("Number of Requirements Tested:")]

# Create top level containers for the SOFTWARE object.
    notebook = gtk.Notebook()
    vbxSoftware = gtk.VBox()

# Create generic toolbar action buttons.  These will call different methods or
# functions depending on the ASSEMBLY Object notebook tab that is selected.
    btnAddItem = gtk.ToolButton(stock_id = gtk.STOCK_ADD)
    btnRemoveItem = gtk.ToolButton(stock_id = gtk.STOCK_REMOVE)
    btnAnalyze = gtk.ToolButton(stock_id = gtk.STOCK_NO)
    btnSaveResults = gtk.ToolButton(stock_id = gtk.STOCK_SAVE)

# Create the Risk Analysis tab widgets.
    hpnRiskAnalysis = gtk.HPaned()
    nbkRiskAnalysis = gtk.Notebook()
    tvwRiskMap = gtk.TreeView()

    # Create the Development Environment tab widgets.
    chkDevelopmentQ1 = _widg.make_check_button(_de_labels_[0])
    chkDevelopmentQ2 = _widg.make_check_button(_de_labels_[1])
    chkDevelopmentQ3 = _widg.make_check_button(_de_labels_[2])
    chkDevelopmentQ4 = _widg.make_check_button(_de_labels_[3])
    chkDevelopmentQ5 = _widg.make_check_button(_de_labels_[4])
    chkDevelopmentQ6 = _widg.make_check_button(_de_labels_[5])
    chkDevelopmentQ7 = _widg.make_check_button(_de_labels_[6])
    chkDevelopmentQ8 = _widg.make_check_button(_de_labels_[7])
    chkDevelopmentQ9 = _widg.make_check_button(_de_labels_[8])
    chkDevelopmentQ10 = _widg.make_check_button(_de_labels_[9])
    chkDevelopmentQ11 = _widg.make_check_button(_de_labels_[10])
    chkDevelopmentQ12 = _widg.make_check_button(_de_labels_[11])
    chkDevelopmentQ13 = _widg.make_check_button(_de_labels_[12])
    chkDevelopmentQ14 = _widg.make_check_button(_de_labels_[13])
    chkDevelopmentQ15 = _widg.make_check_button(_de_labels_[14])
    chkDevelopmentQ16 = _widg.make_check_button(_de_labels_[15])
    chkDevelopmentQ17 = _widg.make_check_button(_de_labels_[16])
    chkDevelopmentQ18 = _widg.make_check_button(_de_labels_[17])
    chkDevelopmentQ19 = _widg.make_check_button(_de_labels_[18])
    chkDevelopmentQ20 = _widg.make_check_button(_de_labels_[19])
    chkDevelopmentQ21 = _widg.make_check_button(_de_labels_[20])
    chkDevelopmentQ22 = _widg.make_check_button(_de_labels_[21])
    chkDevelopmentQ23 = _widg.make_check_button(_de_labels_[22])
    chkDevelopmentQ24 = _widg.make_check_button(_de_labels_[23])
    chkDevelopmentQ25 = _widg.make_check_button(_de_labels_[24])
    chkDevelopmentQ26 = _widg.make_check_button(_de_labels_[25])
    chkDevelopmentQ27 = _widg.make_check_button(_de_labels_[26])
    chkDevelopmentQ28 = _widg.make_check_button(_de_labels_[27])
    chkDevelopmentQ29 = _widg.make_check_button(_de_labels_[28])
    chkDevelopmentQ30 = _widg.make_check_button(_de_labels_[29])
    chkDevelopmentQ31 = _widg.make_check_button(_de_labels_[30])
    chkDevelopmentQ32 = _widg.make_check_button(_de_labels_[31])
    chkDevelopmentQ33 = _widg.make_check_button(_de_labels_[32])
    chkDevelopmentQ34 = _widg.make_check_button(_de_labels_[33])
    chkDevelopmentQ35 = _widg.make_check_button(_de_labels_[34])
    chkDevelopmentQ36 = _widg.make_check_button(_de_labels_[35])
    chkDevelopmentQ37 = _widg.make_check_button(_de_labels_[36])
    chkDevelopmentQ38 = _widg.make_check_button(_de_labels_[37])
    chkDevelopmentQ39 = _widg.make_check_button(_de_labels_[38])
    chkDevelopmentQ40 = _widg.make_check_button(_de_labels_[39])
    chkDevelopmentQ41 = _widg.make_check_button(_de_labels_[40])
    chkDevelopmentQ42 = _widg.make_check_button(_de_labels_[41])
    chkDevelopmentQ43 = _widg.make_check_button(_de_labels_[42])

    hbxDevelopmentEnvironment = gtk.HBox()

    # Create the Requirements Review widgets.
    # [0] = CSCI-level Yes/No from WS2A (16 questions --> Q1 - Q16)
    # [1] = CSCI-level Yes/No from WS3A (1 question --> Q17)
    # [2] = CSCI-level Yes/No from WS4A (23 questions --> Q18 - Q40)
    # [3] = CSCI-level quantity from WS2A (6 questions --> Q41 - Q46)
    # [4] = CSCI-level quantity from WS4A (4 questions --> Q47 - Q50)
    chkSRRQ1 = _widg.make_check_button(_srr_labels_[0][0])
    chkSRRQ2 = _widg.make_check_button(_srr_labels_[0][1])
    chkSRRQ3 = _widg.make_check_button(_srr_labels_[0][2])
    chkSRRQ4 = _widg.make_check_button(_srr_labels_[0][3])
    chkSRRQ5 = _widg.make_check_button(_srr_labels_[0][4])
    chkSRRQ6 = _widg.make_check_button(_srr_labels_[0][5])
    chkSRRQ7 = _widg.make_check_button(_srr_labels_[0][6])
    chkSRRQ8 = _widg.make_check_button(_srr_labels_[0][7])
    chkSRRQ9 = _widg.make_check_button(_srr_labels_[0][8])
    chkSRRQ10 = _widg.make_check_button(_srr_labels_[0][9])
    chkSRRQ11 = _widg.make_check_button(_srr_labels_[0][10])
    chkSRRQ12 = _widg.make_check_button(_srr_labels_[0][11])
    chkSRRQ13 = _widg.make_check_button(_srr_labels_[0][12])
    chkSRRQ14 = _widg.make_check_button(_srr_labels_[0][13])
    chkSRRQ15 = _widg.make_check_button(_srr_labels_[0][14])
    chkSRRQ16 = _widg.make_check_button(_srr_labels_[0][15])
    chkSRRQ17 = _widg.make_check_button(_srr_labels_[1][0])
    chkSRRQ18 = _widg.make_check_button(_srr_labels_[2][0])
    chkSRRQ19 = _widg.make_check_button(_srr_labels_[2][1])
    chkSRRQ20 = _widg.make_check_button(_srr_labels_[2][2])
    chkSRRQ21 = _widg.make_check_button(_srr_labels_[2][3])
    chkSRRQ22 = _widg.make_check_button(_srr_labels_[2][4])
    chkSRRQ23 = _widg.make_check_button(_srr_labels_[2][5])
    chkSRRQ24 = _widg.make_check_button(_srr_labels_[2][6])
    chkSRRQ25 = _widg.make_check_button(_srr_labels_[2][7])
    chkSRRQ26 = _widg.make_check_button(_srr_labels_[2][8])
    chkSRRQ27 = _widg.make_check_button(_srr_labels_[2][9])
    chkSRRQ28 = _widg.make_check_button(_srr_labels_[2][10])
    chkSRRQ29 = _widg.make_check_button(_srr_labels_[2][11])
    chkSRRQ30 = _widg.make_check_button(_srr_labels_[2][12])
    chkSRRQ31 = _widg.make_check_button(_srr_labels_[2][13])
    chkSRRQ32 = _widg.make_check_button(_srr_labels_[2][14])
    chkSRRQ33 = _widg.make_check_button(_srr_labels_[2][15])
    chkSRRQ34 = _widg.make_check_button(_srr_labels_[2][16])
    chkSRRQ35 = _widg.make_check_button(_srr_labels_[2][17])
    chkSRRQ36 = _widg.make_check_button(_srr_labels_[2][18])
    chkSRRQ37 = _widg.make_check_button(_srr_labels_[2][19])
    chkSRRQ38 = _widg.make_check_button(_srr_labels_[2][20])
    chkSRRQ39 = _widg.make_check_button(_srr_labels_[2][21])
    chkSRRQ40 = _widg.make_check_button(_srr_labels_[2][22])
    lblSRRQ41 = _widg.make_label(_srr_labels_[3][0], width=500, height=-1,
                                 bold=False)
    lblSRRQ42 = _widg.make_label(_srr_labels_[3][1], width=500, height=-1,
                                 bold=False)
    lblSRRQ43 = _widg.make_label(_srr_labels_[3][2], width=500, height=-1,
                                 bold=False)
    lblSRRQ44 = _widg.make_label(_srr_labels_[3][3], width=500, height=-1,
                                 bold=False)
    lblSRRQ45 = _widg.make_label(_srr_labels_[3][4], width=500, height=-1,
                                 bold=False)
    lblSRRQ46 = _widg.make_label(_srr_labels_[3][5], width=500, height=-1,
                                 bold=False)
    lblSRRQ47 = _widg.make_label(_srr_labels_[4][0], width=500, height=-1,
                                 bold=False)
    lblSRRQ48 = _widg.make_label(_srr_labels_[4][1], width=500, height=-1,
                                 bold=False)
    lblSRRQ49 = _widg.make_label(_srr_labels_[4][2], width=500, height=-1,
                                 bold=False)
    lblSRRQ50 = _widg.make_label(_srr_labels_[4][3], width=500, height=-1,
                                 bold=False)
    txtSRRQ41 = _widg.make_entry(_width_=50)
    txtSRRQ42 = _widg.make_entry(_width_=50)
    txtSRRQ43 = _widg.make_entry(_width_=50)
    txtSRRQ44 = _widg.make_entry(_width_=50)
    txtSRRQ45 = _widg.make_entry(_width_=50)
    txtSRRQ46 = _widg.make_entry(_width_=50)
    txtSRRQ47 = _widg.make_entry(_width_=50)
    txtSRRQ48 = _widg.make_entry(_width_=50)
    txtSRRQ49 = _widg.make_entry(_width_=50)
    txtSRRQ50 = _widg.make_entry(_width_=50)

    hpnSRR = gtk.HPaned()
    lblSRR = gtk.Label()

    # Create the Preliminary Design Review widgets.
    # [0] = CSCI-level Yes/No from WS2B (14 questions --> Q1 - Q14)
    # [1] = CSCI-level Yes/No from WS3B (1 question --> Q15)
    # [2] = CSCI-level Yes/No from WS4B (14 questions --> Q16 - Q29)
    # [3] = CSCI-level quantity from WS4B (10 questions --> Q30 - Q39)
    chkPDRQ1 = _widg.make_check_button(_pdr_labels_[0][0])
    chkPDRQ2 = _widg.make_check_button(_pdr_labels_[0][1])
    chkPDRQ3 = _widg.make_check_button(_pdr_labels_[0][2])
    chkPDRQ4 = _widg.make_check_button(_pdr_labels_[0][3])
    chkPDRQ5 = _widg.make_check_button(_pdr_labels_[0][4])
    chkPDRQ6 = _widg.make_check_button(_pdr_labels_[0][5])
    chkPDRQ7 = _widg.make_check_button(_pdr_labels_[0][6])
    chkPDRQ8 = _widg.make_check_button(_pdr_labels_[0][7])
    chkPDRQ9 = _widg.make_check_button(_pdr_labels_[0][8])
    chkPDRQ10 = _widg.make_check_button(_pdr_labels_[0][9])
    chkPDRQ11 = _widg.make_check_button(_pdr_labels_[0][10])
    chkPDRQ12 = _widg.make_check_button(_pdr_labels_[0][11])
    chkPDRQ13 = _widg.make_check_button(_pdr_labels_[0][12])
    chkPDRQ14 = _widg.make_check_button(_pdr_labels_[0][13])
    chkPDRQ15 = _widg.make_check_button(_pdr_labels_[1][0])
    chkPDRQ16 = _widg.make_check_button(_pdr_labels_[2][0])
    chkPDRQ17 = _widg.make_check_button(_pdr_labels_[2][1])
    chkPDRQ18 = _widg.make_check_button(_pdr_labels_[2][2])
    chkPDRQ19 = _widg.make_check_button(_pdr_labels_[2][3])
    chkPDRQ20 = _widg.make_check_button(_pdr_labels_[2][4])
    chkPDRQ21 = _widg.make_check_button(_pdr_labels_[2][5])
    chkPDRQ22 = _widg.make_check_button(_pdr_labels_[2][6])
    chkPDRQ23 = _widg.make_check_button(_pdr_labels_[2][7])
    chkPDRQ24 = _widg.make_check_button(_pdr_labels_[2][8])
    chkPDRQ25 = _widg.make_check_button(_pdr_labels_[2][9])
    chkPDRQ26 = _widg.make_check_button(_pdr_labels_[2][10])
    chkPDRQ27 = _widg.make_check_button(_pdr_labels_[2][11])
    chkPDRQ28 = _widg.make_check_button(_pdr_labels_[2][12])
    chkPDRQ29 = _widg.make_check_button(_pdr_labels_[2][13])
    lblPDRQ30 = _widg.make_label(_pdr_labels_[3][0], width=500, height=-1,
                                 bold=False)
    lblPDRQ31 = _widg.make_label(_pdr_labels_[3][1], width=500, height=-1,
                                 bold=False)
    lblPDRQ32 = _widg.make_label(_pdr_labels_[3][2], width=500, height=-1,
                                 bold=False)
    lblPDRQ33 = _widg.make_label(_pdr_labels_[3][3], width=500, height=-1,
                                 bold=False)
    lblPDRQ34 = _widg.make_label(_pdr_labels_[3][4], width=500, height=-1,
                                 bold=False)
    lblPDRQ35 = _widg.make_label(_pdr_labels_[3][5], width=500, height=-1,
                                 bold=False)
    lblPDRQ36 = _widg.make_label(_pdr_labels_[3][6], width=500, height=-1,
                                 bold=False)
    lblPDRQ37 = _widg.make_label(_pdr_labels_[3][7], width=500, height=-1,
                                 bold=False)
    lblPDRQ38 = _widg.make_label(_pdr_labels_[3][8], width=500, height=-1,
                                 bold=False)
    lblPDRQ39 = _widg.make_label(_pdr_labels_[3][9], width=500, height=-1,
                                 bold=False)
    txtPDRQ30 = _widg.make_entry(_width_=50)
    txtPDRQ31 = _widg.make_entry(_width_=50)
    txtPDRQ32 = _widg.make_entry(_width_=50)
    txtPDRQ33 = _widg.make_entry(_width_=50)
    txtPDRQ34 = _widg.make_entry(_width_=50)
    txtPDRQ35 = _widg.make_entry(_width_=50)
    txtPDRQ36 = _widg.make_entry(_width_=50)
    txtPDRQ37 = _widg.make_entry(_width_=50)
    txtPDRQ38 = _widg.make_entry(_width_=50)
    txtPDRQ39 = _widg.make_entry(_width_=50)

    hpnPDR = gtk.HPaned()
    lblPDR = gtk.Label()

    # Create the Critical Design Review widgets.
    chkCDRQ1 = _widg.make_check_button(_cdr_labels_[0][0], 700)
    chkCDRQ2 = _widg.make_check_button(_cdr_labels_[0][1], 700)
    chkCDRQ3 = _widg.make_check_button(_cdr_labels_[0][2], 700)
    chkCDRQ4 = _widg.make_check_button(_cdr_labels_[0][3], 700)
    chkCDRQ5 = _widg.make_check_button(_cdr_labels_[0][4], 700)
    chkCDRQ6 = _widg.make_check_button(_cdr_labels_[0][5], 700)
    chkCDRQ7 = _widg.make_check_button(_cdr_labels_[0][6], 700)
    chkCDRQ8 = _widg.make_check_button(_cdr_labels_[0][7], 700)
    chkCDRQ9 = _widg.make_check_button(_cdr_labels_[1][0], 700)
    chkCDRQ10 = _widg.make_check_button(_cdr_labels_[1][1], 700)
    lblCDRQ11 = _widg.make_label(_cdr_labels_[2][0], width=500, height=-1,
                                 bold=False)
    lblCDRQ12 = _widg.make_label(_cdr_labels_[2][1], width=500, height=-1,
                                 bold=False)
    lblCDRQ13 = _widg.make_label(_cdr_labels_[2][2], width=500, height=-1,
                                 bold=False)
    lblCDRQ14 = _widg.make_label(_cdr_labels_[2][3], width=500, height=-1,
                                 bold=False)
    lblCDRQ15 = _widg.make_label(_cdr_labels_[2][4], width=500, height=-1,
                                 bold=False)
    lblCDRQ16 = _widg.make_label(_cdr_labels_[2][5], width=500, height=-1,
                                 bold=False)
    lblCDRQ17 = _widg.make_label(_cdr_labels_[2][6], width=500, height=-1,
                                 bold=False)
    lblCDRQ18 = _widg.make_label(_cdr_labels_[2][7], width=500, height=-1,
                                 bold=False)
    lblCDRQ19 = _widg.make_label(_cdr_labels_[2][8], width=500, height=-1,
                                 bold=False)
    lblCDRQ20 = _widg.make_label(_cdr_labels_[2][9], width=500, height=-1,
                                 bold=False)
    lblCDRQ21 = _widg.make_label(_cdr_labels_[2][10], width=500, height=-1,
                                 bold=False)
    lblCDRQ22 = _widg.make_label(_cdr_labels_[2][11], width=500, height=-1,
                                 bold=False)
    lblCDRQ23 = _widg.make_label(_cdr_labels_[2][12], width=500, height=-1,
                                 bold=False)
    lblCDRQ24 = _widg.make_label(_cdr_labels_[2][13], width=500, height=-1,
                                 bold=False)
    lblCDRQ25 = _widg.make_label(_cdr_labels_[2][14], width=500, height=-1,
                                 bold=False)
    lblCDRQ26 = _widg.make_label(_cdr_labels_[2][15], width=500, height=-1,
                                 bold=False)
    lblCDRQ27 = _widg.make_label(_cdr_labels_[2][16], width=500, height=-1,
                                 bold=False)
    lblCDRQ28 = _widg.make_label(_cdr_labels_[2][17], width=500, height=-1,
                                 bold=False)
    lblCDRQ29 = _widg.make_label(_cdr_labels_[2][18], width=500, height=-1,
                                 bold=False)
    lblCDRQ30 = _widg.make_label(_cdr_labels_[2][19], width=500, height=-1,
                                 bold=False)
    lblCDRQ31 = _widg.make_label(_cdr_labels_[2][20], width=500, height=-1,
                                 bold=False)
    lblCDRQ32 = _widg.make_label(_cdr_labels_[2][21], width=500, height=-1,
                                 bold=False)
    lblCDRQ33 = _widg.make_label(_cdr_labels_[2][22], width=500, height=-1,
                                 bold=False)
    lblCDRQ34 = _widg.make_label(_cdr_labels_[2][23], width=500, height=-1,
                                 bold=False)
    txtCDRQ11 = _widg.make_entry(_width_=50)
    txtCDRQ12 = _widg.make_entry(_width_=50)
    txtCDRQ13 = _widg.make_entry(_width_=50)
    txtCDRQ14 = _widg.make_entry(_width_=50)
    txtCDRQ15 = _widg.make_entry(_width_=50)
    txtCDRQ16 = _widg.make_entry(_width_=50)
    txtCDRQ17 = _widg.make_entry(_width_=50)
    txtCDRQ18 = _widg.make_entry(_width_=50)
    txtCDRQ19 = _widg.make_entry(_width_=50)
    txtCDRQ20 = _widg.make_entry(_width_=50)
    txtCDRQ21 = _widg.make_entry(_width_=50)
    txtCDRQ22 = _widg.make_entry(_width_=50)
    txtCDRQ23 = _widg.make_entry(_width_=50)
    txtCDRQ24 = _widg.make_entry(_width_=50)
    txtCDRQ25 = _widg.make_entry(_width_=50)
    txtCDRQ26 = _widg.make_entry(_width_=50)
    txtCDRQ27 = _widg.make_entry(_width_=50)
    txtCDRQ28 = _widg.make_entry(_width_=50)
    txtCDRQ29 = _widg.make_entry(_width_=50)
    txtCDRQ30 = _widg.make_entry(_width_=50)
    txtCDRQ31 = _widg.make_entry(_width_=50)
    txtCDRQ32 = _widg.make_entry(_width_=50)
    txtCDRQ33 = _widg.make_entry(_width_=50)
    txtCDRQ34 = _widg.make_entry(_width_=50)
    chkCDRQ35 = _widg.make_check_button(_cdr_labels_[3][0], 700)
    chkCDRQ36 = _widg.make_check_button(_cdr_labels_[3][1], 700)
    chkCDRQ37 = _widg.make_check_button(_cdr_labels_[3][2], 700)
    chkCDRQ38 = _widg.make_check_button(_cdr_labels_[3][3], 700)
    chkCDRQ39 = _widg.make_check_button(_cdr_labels_[3][4], 700)
    chkCDRQ40 = _widg.make_check_button(_cdr_labels_[3][5], 700)
    chkCDRQ41 = _widg.make_check_button(_cdr_labels_[3][6], 700)
    chkCDRQ42 = _widg.make_check_button(_cdr_labels_[3][7], 700)
    chkCDRQ43 = _widg.make_check_button(_cdr_labels_[3][8], 700)
    chkCDRQ44 = _widg.make_check_button(_cdr_labels_[3][9], 700)
    chkCDRQ45 = _widg.make_check_button(_cdr_labels_[3][10], 700)
    chkCDRQ46 = _widg.make_check_button(_cdr_labels_[3][11], 700)
    lblCDRQ47 = _widg.make_label(_cdr_labels_[4][0], width=500, height=-1,
                                 bold=False)
    lblCDRQ48 = _widg.make_label(_cdr_labels_[4][1], width=500, height=-1,
                                 bold=False)
    lblCDRQ49 = _widg.make_label(_cdr_labels_[4][2], width=500, height=-1,
                                 bold=False)
    lblCDRQ50 = _widg.make_label(_cdr_labels_[4][3], width=500, height=-1,
                                 bold=False)
    lblCDRQ51 = _widg.make_label(_cdr_labels_[4][4], width=500, height=-1,
                                 bold=False)
    lblCDRQ52 = _widg.make_label(_cdr_labels_[4][5], width=500, height=-1,
                                 bold=False)
    lblCDRQ53 = _widg.make_label(_cdr_labels_[4][6], width=500, height=-1,
                                 bold=False)
    lblCDRQ54 = _widg.make_label(_cdr_labels_[4][7], width=500, height=-1,
                                 bold=False)
    lblCDRQ55 = _widg.make_label(_cdr_labels_[4][8], width=500, height=-1,
                                 bold=False)
    lblCDRQ56 = _widg.make_label(_cdr_labels_[4][9], width=500, height=-1,
                                 bold=False)
    lblCDRQ57 = _widg.make_label(_cdr_labels_[4][10], width=500, height=-1,
                                 bold=False)
    lblCDRQ58 = _widg.make_label(_cdr_labels_[4][11], width=500, height=-1,
                                 bold=False)
    txtCDRQ47 = _widg.make_entry(_width_=50)
    txtCDRQ48 = _widg.make_entry(_width_=50)
    txtCDRQ49 = _widg.make_entry(_width_=50)
    txtCDRQ50 = _widg.make_entry(_width_=50)
    txtCDRQ51 = _widg.make_entry(_width_=50)
    txtCDRQ52 = _widg.make_entry(_width_=50)
    txtCDRQ53 = _widg.make_entry(_width_=50)
    txtCDRQ54 = _widg.make_entry(_width_=50)
    txtCDRQ55 = _widg.make_entry(_width_=50)
    txtCDRQ56 = _widg.make_entry(_width_=50)
    txtCDRQ57 = _widg.make_entry(_width_=50)
    txtCDRQ58 = _widg.make_entry(_width_=50)

    fraCSCICDRAM = _widg.make_frame(_label_=_(u"Anomaly Management"))
    fraCSCICDRSQ = _widg.make_frame(_label_=_(u"Software Quality Control"))
    fraUnitCDRSQ = _widg.make_frame(_label_=_(u"Software Quality Control"))
    hpnCDR = gtk.HPaned()
    lblCDR = gtk.Label()

    # Create the Test Readiness Review widgets.
    # [0] = CSCI-level quantity from WS8D and WS9D (4 questions -> Q1 - Q4)
    # [2] = Unit-level Yes/No from WS2C (2 questions --> Q5 - Q8)
    # [3] = Unit-level Yes/No from WS4C (14 questions --> Q9 - Q22)
    # [4] = Unit-level Yes/No from WS8D (3 questions -> Q23 - Q25)
    chkTRRQ5 = _widg.make_check_button(_trr_labels_[1][0])
    chkTRRQ6 = _widg.make_check_button(_trr_labels_[1][1])
    chkTRRQ7 = _widg.make_check_button(_trr_labels_[2][0])
    chkTRRQ8 = _widg.make_check_button(_trr_labels_[2][1])
    chkTRRQ9 = _widg.make_check_button(_trr_labels_[2][2])
    chkTRRQ10 = _widg.make_check_button(_trr_labels_[2][3])
    chkTRRQ11 = _widg.make_check_button(_trr_labels_[2][4])
    chkTRRQ12 = _widg.make_check_button(_trr_labels_[2][5])
    chkTRRQ13 = _widg.make_check_button(_trr_labels_[2][6])
    chkTRRQ14 = _widg.make_check_button(_trr_labels_[2][7])
    chkTRRQ15 = _widg.make_check_button(_trr_labels_[2][8])
    chkTRRQ16 = _widg.make_check_button(_trr_labels_[2][9])
    chkTRRQ17 = _widg.make_check_button(_trr_labels_[2][10])
    chkTRRQ18 = _widg.make_check_button(_trr_labels_[2][11])
    chkTRRQ19 = _widg.make_check_button(_trr_labels_[2][12])
    chkTRRQ20 = _widg.make_check_button(_trr_labels_[2][13])
    lblTRRQ1 = _widg.make_label(_trr_labels_[0][0], width=500, height=-1,
                                bold=False)
    lblTRRQ2 = _widg.make_label(_trr_labels_[0][1], width=500, height=-1,
                                bold=False)
    lblTRRQ3 = _widg.make_label(_trr_labels_[0][2], width=500, height=-1,
                                bold=False)
    lblTRRQ4 = _widg.make_label(_trr_labels_[0][3], width=500, height=-1,
                                bold=False)
    lblTRRQ21 = _widg.make_label(_trr_labels_[3][0], width=500, height=-1,
                                 bold=False)
    lblTRRQ22 = _widg.make_label(_trr_labels_[3][1], width=500, height=-1,
                                 bold=False)
    lblTRRQ23 = _widg.make_label(_trr_labels_[3][2], width=500, height=-1,
                                 bold=False)
    lblTRRQ24 = _widg.make_label(_trr_labels_[3][3], width=500, height=-1,
                                 bold=False)
    txtTRRQ1 = _widg.make_entry(_width_=50)
    txtTRRQ2 = _widg.make_entry(_width_=50)
    txtTRRQ3 = _widg.make_entry(_width_=50)
    txtTRRQ4 = _widg.make_entry(_width_=50)
    txtTRRQ21 = _widg.make_entry(_width_=50)
    txtTRRQ22 = _widg.make_entry(_width_=50)
    txtTRRQ23 = _widg.make_entry(_width_=50)
    txtTRRQ24 = _widg.make_entry(_width_=50)

    fraCSCITRRSX = _widg.make_frame(_label_=_(u"Complexity &amp; Modularity"))
    fraUnitTRRAM = _widg.make_frame(_label_=_(u"Anomaly Management"))
    fraUnitTRRSQ = _widg.make_frame(_label_=_(u"Software Quality Control"))
    hpnTRR = gtk.HPaned()
    lblTRR = gtk.Label()

# Create the Reliability Estimation tab widgets.
    txtFT1 = _widg.make_entry()
    txtFT2 = _widg.make_entry()
    txtRENAVG = _widg.make_entry()
    txtRENEOT = _widg.make_entry()
    txtEC = _widg.make_entry()
    txtEV = _widg.make_entry()
    txtET = _widg.make_entry()
    txtOS = _widg.make_entry()
    txtEW = _widg.make_entry()
    txtE = _widg.make_entry()
    txtF = _widg.make_entry()

    def __init__(self, application):
        """
        Initializes the Software Object.

        Keyword Arguments:
        application -- the RTK application.
        """

        self._ready = False

        self._app = application

        gobject.idle_add(_util.long_call, self._app)

        self.treeview = None
        self.model = None
        self._selected_row = None

# Define global integer variables.
        self.software_id = 0

# Define local dictionary variables.
        self._dicSoftware = {}
        self._development_env_ = {}
        self._srr_ = {}
        self._pdr_ = {}
        self._cdr_ = {}
        self._trr_ = {}
        self._risk_ = {}

# Define local list variables.
        self._col_order = []

# Define local integer variables.
        self._app_level = 0
        self._dev_phase = 0

# Define local float variables.
        self._rpfom = 0.0

# General Data tab widgets.
        self.cmbApplication = _widg.make_combo(simple=True)
        self.cmbDevelopment = _widg.make_combo(simple=True)
        self.cmbLevel = _widg.make_combo(simple=True)
        self.cmbPhase = _widg.make_combo(simple=True)
        self.txtDescription = _widg.make_text_view(width=400)

# Test Technique Selection tab widgets.
        self.cmbTCL = _widg.make_combo(simple=True)
        self.cmbTestPath = _widg.make_combo(simple=True)
        self.cmbTestEffort = _widg.make_combo(simple=True)
        self.cmbTestApproach = _widg.make_combo(simple=True)

        self.txtLaborTest = _widg.make_entry(_width_=100)
        self.txtLaborDev = _widg.make_entry(_width_=100)
        self.txtBudgetTest = _widg.make_entry(_width_=100)
        self.txtBudgetDev = _widg.make_entry(_width_=100)
        self.txtScheduleTest = _widg.make_entry(_width_=100)
        self.txtScheduleDev = _widg.make_entry(_width_=100)
        self.txtBranches = _widg.make_entry(_width_=100)
        self.txtBranchesTest = _widg.make_entry(_width_=100)
        self.txtInputs = _widg.make_entry(_width_=100)
        self.txtInputsTest = _widg.make_entry(_width_=100)
        self.txtUnits = _widg.make_entry(_width_=100)
        self.txtUnitsTest = _widg.make_entry(_width_=100)
        self.txtInterfaces = _widg.make_entry(_width_=100)
        self.txtInterfacesTest = _widg.make_entry(_width_=100)

        self.scwTestSelectionMatrix = gtk.ScrolledWindow()

        self.tvwUnitTestSelectionMatrix = gtk.TreeView()
        self.tvwCSCITestSelectionMatrix = gtk.TreeView()

        if(_conf.TABPOS[2] == 'left'):
            self.notebook.set_tab_pos(gtk.POS_LEFT)
        elif(_conf.TABPOS[2] == 'right'):
            self.notebook.set_tab_pos(gtk.POS_RIGHT)
        elif(_conf.TABPOS[2] == 'top'):
            self.notebook.set_tab_pos(gtk.POS_TOP)
        else:
            self.notebook.set_tab_pos(gtk.POS_BOTTOM)

# Create the General Data tab
        if self._general_data_tab_create():
            self._app.debug_log.error("software.py: Failed to create General Data tab.")

# Create the Risk Analysis tab.
        if self._risk_analysis_widgets_create():
            self._app.debug_log.error("software.py: Failed to create Risk Analysis widgets.")
        if self._risk_analysis_tab_create():
            self._app.debug_log.error("software.py: Failed to create Risk Analysis tab.")

# Create the Test Technique Selection tab.
        if self._test_selection_tab_create():
            self._app.debug_log.error("software.py: Failed to create Test Technique Selection tab.")

# Create the Reliability Estimation tab.
        if self._reliability_estimation_tab_create():
            self._app.debug_log.error("software.py: Failed to create Reliability Estimation tab.")

        toolbar = self._toolbar_create()

        self.vbxSoftware.pack_start(toolbar, expand=False)
        self.vbxSoftware.pack_start(self.notebook)

        self.notebook.connect('switch-page', self._notebook_page_switched, 0)

        self._ready = True

    def _toolbar_create(self):
        """ Method to create the toolbar for the Assembly Object work book. """

        toolbar = gtk.Toolbar()

# Add sibling module button.
        button = gtk.ToolButton(stock_id = gtk.STOCK_NEW)
        button.set_tooltip_text(_("Adds a new software module at the same indenture level as the selected software module."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/insert_sibling.png')
        button.set_icon_widget(image)
        button.connect('clicked', self._module_add, 0)
        toolbar.insert(button, 0)

# Add child module button.
        button = gtk.ToolButton(stock_id = gtk.STOCK_NEW)
        button.set_tooltip_text(_("Adds a new software module one indenture level subordinate to the selected software module."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/insert_child.png')
        button.set_icon_widget(image)
        button.connect('clicked', self._module_add, 1)
        toolbar.insert(button, 1)

# Delete module button
        button = gtk.ToolButton(stock_id = gtk.STOCK_DELETE)
        button.set_tooltip_text(_("Removes the currently selected software module from the RTK Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/delete.png')
        button.set_icon_widget(image)
        button.connect('clicked', self._module_delete)
        toolbar.insert(button, 2)

        toolbar.insert(gtk.SeparatorToolItem(), 3)

# Perform analysis button.  Depending on the notebook page selected will
# determine which analysis is executed.
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        self.btnAnalyze.set_icon_widget(image)
        self.btnAnalyze.set_name('Calculate')
        self.btnAnalyze.set_tooltip_text(_("Calculates software reliability metrics."))
        self.btnAnalyze.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnAnalyze, 4)

# Save results button.  Depending on the notebook page selected will determine
# which results are saved.
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        self.btnSaveResults.set_icon_widget(image)
        self.btnSaveResults.set_name('Save')
        self.btnSaveResults.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnSaveResults, 5)

        toolbar.show()

        return(toolbar)

    def _general_data_tab_create(self):
        """
        Method to create the General Data gtk.Notebook tab and add it to the
        gtk.Notebook at the proper location.
        """

        def _general_data_widgets_create(self):
            """
            Function to create General Data widgets.
            """

    # Quadrant 1 (upper left) widgets.  These widgets are used to display
    # general information about the selected software module.
            self.txtDescription.set_tooltip_text(_("Enter a description of the selected software module."))
            self.txtDescription.get_child().get_child().connect('focus-out-event',
                                                                self._callback_entry,
                                                                'text', 3)

            self.cmbLevel.set_tooltip_text(_("Select the application level of the selected software module."))
            _query_ = "SELECT fld_level_desc \
                       FROM tbl_software_level"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)
            _widg.load_combo(self.cmbLevel, _results_, True)
            self.cmbLevel.connect('changed', self._callback_combo, 2)

            self.cmbApplication.set_tooltip_text(_("Select the application type of the selected software module."))
            self.cmbApplication.connect('changed', self._callback_combo, 4)
            _query_ = "SELECT fld_category_name \
                       FROM tbl_software_category"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)
            _widg.load_combo(self.cmbApplication, _results_, True)

            #self.cmbDevelopment.set_tooltip_text(_("Select the type of development environment for the selected software module."))
            #self.cmbDevelopment.connect('changed', self._callback_combo, 5)
            #_query_ = "SELECT fld_development_desc \
            #           FROM tbl_development_environment"
            #_results_ = self._app.COMDB.execute_query(_query_,
            #                                          None,
            #                                          self._app.ComCnx)
            #_widg.load_combo(self.cmbDevelopment, _results_, True)

            self.cmbPhase.set_tooltip_text(_("Select the development phase for the selected software module."))
            self.cmbPhase.connect('changed', self._callback_combo, 36)
            _query_ = "SELECT fld_phase_desc \
                       FROM tbl_development_phase"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)
            _widg.load_combo(self.cmbPhase, _results_, True)

            #self.chkDevAssessType.connect('toggled',
            #                              self._callback_check, 35)

            return False

        if _general_data_widgets_create(self):
            self._app.debug_log.error("software.py: Failed to create General Data tab widgets.")

# Populate quadrant 1 (upper left).
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_(u"General Information"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

# Create the labels for the upper-left and lower-left quadrants.
        y_pos = 5
        label = _widg.make_label(self._gd_tab_labels[0][0], -1, 25)
        fixed.put(label, 5, y_pos)
        y_pos += 110

        _max1_ = 0
        _max2_ = 0
        (_max1_, _heights_) = _widg.make_labels(self._gd_tab_labels[0][1:],
                                                fixed, 5, y_pos, y_inc=35)
        _x_pos_ = max(_max1_, _max2_) + 20

        # Place the widgets.
        y_pos = 5
        fixed.put(self.txtDescription, _x_pos_, y_pos)
        y_pos += 110

        fixed.put(self.cmbLevel, _x_pos_, y_pos)
        y_pos += 35

        fixed.put(self.cmbApplication, _x_pos_, y_pos)
        y_pos += 35

        #fixed.put(self.cmbDevelopment, _x_pos_, y_pos)
        #y_pos += 35

        fixed.put(self.cmbPhase, _x_pos_, y_pos)
        y_pos += 35

        fixed.show_all()

        # Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _(u"General\nData") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Displays general information about the selected software module."))
        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _general_data_tab_load(self):
        """
        Loads the widgets with general information about the SOFTWARE Object.
        """

        if(self._selected_row is not None):
            self.cmbLevel.set_active(int(self.model.get_value(self._selected_row, 2)))
            textbuffer = self.txtDescription.get_child().get_child().get_buffer()
            textbuffer.set_text(self.model.get_value(self._selected_row, 3))
            self.cmbApplication.set_active(int(self.model.get_value(self._selected_row, 4)))
            #self.cmbDevelopment.set_active(int(self.model.get_value(self._selected_row, 5)))
            self.cmbPhase.set_active(int(self.model.get_value(self._selected_row, 36)))

            self.cmbTCL.set_active(int(self.model.get_value(self._selected_row, 37)))
            self.cmbTestPath.set_active(int(self.model.get_value(self._selected_row, 38)))

        return False

    def _risk_analysis_widgets_create(self):
        """
        Method for creating Risk Analysis widgets for the Software Object.
        """

        def _development_env_widgets_create(self):
            """
            Method to create the Development Environment widgets.
            """

            self.chkDevelopmentQ1.connect('toggled', self._callback_check, 100)
            self.chkDevelopmentQ2.connect('toggled', self._callback_check, 101)
            self.chkDevelopmentQ3.connect('toggled', self._callback_check, 102)
            self.chkDevelopmentQ4.connect('toggled', self._callback_check, 103)
            self.chkDevelopmentQ5.connect('toggled', self._callback_check, 104)
            self.chkDevelopmentQ6.connect('toggled', self._callback_check, 105)
            self.chkDevelopmentQ7.connect('toggled', self._callback_check, 106)
            self.chkDevelopmentQ8.connect('toggled', self._callback_check, 107)
            self.chkDevelopmentQ9.connect('toggled', self._callback_check, 108)
            self.chkDevelopmentQ10.connect('toggled', self._callback_check, 109)
            self.chkDevelopmentQ11.connect('toggled', self._callback_check, 110)
            self.chkDevelopmentQ12.connect('toggled', self._callback_check, 111)
            self.chkDevelopmentQ13.connect('toggled', self._callback_check, 112)
            self.chkDevelopmentQ14.connect('toggled', self._callback_check, 113)
            self.chkDevelopmentQ15.connect('toggled', self._callback_check, 114)
            self.chkDevelopmentQ16.connect('toggled', self._callback_check, 115)
            self.chkDevelopmentQ17.connect('toggled', self._callback_check, 116)
            self.chkDevelopmentQ18.connect('toggled', self._callback_check, 117)
            self.chkDevelopmentQ19.connect('toggled', self._callback_check, 118)
            self.chkDevelopmentQ20.connect('toggled', self._callback_check, 119)
            self.chkDevelopmentQ21.connect('toggled', self._callback_check, 120)
            self.chkDevelopmentQ22.connect('toggled', self._callback_check, 121)
            self.chkDevelopmentQ23.connect('toggled', self._callback_check, 122)
            self.chkDevelopmentQ24.connect('toggled', self._callback_check, 123)
            self.chkDevelopmentQ25.connect('toggled', self._callback_check, 124)
            self.chkDevelopmentQ26.connect('toggled', self._callback_check, 125)
            self.chkDevelopmentQ27.connect('toggled', self._callback_check, 126)
            self.chkDevelopmentQ28.connect('toggled', self._callback_check, 127)
            self.chkDevelopmentQ29.connect('toggled', self._callback_check, 128)
            self.chkDevelopmentQ30.connect('toggled', self._callback_check, 129)
            self.chkDevelopmentQ31.connect('toggled', self._callback_check, 130)
            self.chkDevelopmentQ32.connect('toggled', self._callback_check, 131)
            self.chkDevelopmentQ33.connect('toggled', self._callback_check, 132)
            self.chkDevelopmentQ34.connect('toggled', self._callback_check, 133)
            self.chkDevelopmentQ35.connect('toggled', self._callback_check, 134)
            self.chkDevelopmentQ36.connect('toggled', self._callback_check, 135)
            self.chkDevelopmentQ37.connect('toggled', self._callback_check, 136)
            self.chkDevelopmentQ38.connect('toggled', self._callback_check, 137)
            self.chkDevelopmentQ39.connect('toggled', self._callback_check, 138)
            self.chkDevelopmentQ40.connect('toggled', self._callback_check, 139)
            self.chkDevelopmentQ41.connect('toggled', self._callback_check, 140)
            self.chkDevelopmentQ42.connect('toggled', self._callback_check, 141)
            self.chkDevelopmentQ43.connect('toggled', self._callback_check, 142)

            return False

        def _srr_widgets_create(self):
            """
            Method to create the requirements review widgets.
            """

            self.chkSRRQ1.get_child().props.width_request = 700
            self.chkSRRQ1.connect('toggled', self._callback_check, 200)
            self.chkSRRQ2.get_child().props.width_request = 700
            self.chkSRRQ2.connect('toggled', self._callback_check, 201)
            self.chkSRRQ3.get_child().props.width_request = 700
            self.chkSRRQ3.connect('toggled', self._callback_check, 202)
            self.chkSRRQ4.get_child().props.width_request = 700
            self.chkSRRQ4.connect('toggled', self._callback_check, 203)
            self.chkSRRQ5.get_child().props.width_request = 700
            self.chkSRRQ5.connect('toggled', self._callback_check, 204)
            self.chkSRRQ6.get_child().props.width_request = 700
            self.chkSRRQ6.connect('toggled', self._callback_check, 205)
            self.chkSRRQ7.get_child().props.width_request = 700
            self.chkSRRQ7.connect('toggled', self._callback_check, 206)
            self.chkSRRQ8.get_child().props.width_request = 700
            self.chkSRRQ8.connect('toggled', self._callback_check, 207)
            self.chkSRRQ9.get_child().props.width_request = 700
            self.chkSRRQ9.connect('toggled', self._callback_check, 208)
            self.chkSRRQ10.get_child().props.width_request = 700
            self.chkSRRQ10.connect('toggled', self._callback_check, 209)
            self.chkSRRQ11.get_child().props.width_request = 700
            self.chkSRRQ11.connect('toggled', self._callback_check, 210)
            self.chkSRRQ12.get_child().props.width_request = 700
            self.chkSRRQ12.connect('toggled', self._callback_check, 211)
            self.chkSRRQ13.get_child().props.width_request = 700
            self.chkSRRQ13.connect('toggled', self._callback_check, 212)
            self.chkSRRQ14.get_child().props.width_request = 700
            self.chkSRRQ14.connect('toggled', self._callback_check, 213)
            self.chkSRRQ15.get_child().props.width_request = 700
            self.chkSRRQ15.connect('toggled', self._callback_check, 214)
            self.chkSRRQ16.get_child().props.width_request = 700
            self.chkSRRQ16.connect('toggled', self._callback_check, 215)
            self.chkSRRQ17.get_child().props.width_request = 700
            self.chkSRRQ17.connect('toggled', self._callback_check, 216)
            self.chkSRRQ18.get_child().props.width_request = 700
            self.chkSRRQ18.connect('toggled', self._callback_check, 217)
            self.chkSRRQ19.get_child().props.width_request = 700
            self.chkSRRQ19.connect('toggled', self._callback_check, 218)
            self.chkSRRQ20.get_child().props.width_request = 700
            self.chkSRRQ20.connect('toggled', self._callback_check, 219)
            self.chkSRRQ21.get_child().props.width_request = 700
            self.chkSRRQ21.connect('toggled', self._callback_check, 220)
            self.chkSRRQ22.get_child().props.width_request = 700
            self.chkSRRQ22.connect('toggled', self._callback_check, 221)
            self.chkSRRQ23.get_child().props.width_request = 700
            self.chkSRRQ23.connect('toggled', self._callback_check, 222)
            self.chkSRRQ24.get_child().props.width_request = 700
            self.chkSRRQ24.connect('toggled', self._callback_check, 223)
            self.chkSRRQ25.get_child().props.width_request = 700
            self.chkSRRQ25.connect('toggled', self._callback_check, 224)
            self.chkSRRQ26.get_child().props.width_request = 700
            self.chkSRRQ26.connect('toggled', self._callback_check, 225)
            self.chkSRRQ27.get_child().props.width_request = 700
            self.chkSRRQ27.connect('toggled', self._callback_check, 226)
            self.chkSRRQ28.get_child().props.width_request = 700
            self.chkSRRQ28.connect('toggled', self._callback_check, 227)
            self.chkSRRQ29.get_child().props.width_request = 700
            self.chkSRRQ29.connect('toggled', self._callback_check, 228)
            self.chkSRRQ30.get_child().props.width_request = 700
            self.chkSRRQ30.connect('toggled', self._callback_check, 229)
            self.chkSRRQ31.get_child().props.width_request = 700
            self.chkSRRQ31.connect('toggled', self._callback_check, 230)
            self.chkSRRQ32.get_child().props.width_request = 700
            self.chkSRRQ32.connect('toggled', self._callback_check, 231)
            self.chkSRRQ33.get_child().props.width_request = 700
            self.chkSRRQ33.connect('toggled', self._callback_check, 232)
            self.chkSRRQ34.get_child().props.width_request = 700
            self.chkSRRQ34.connect('toggled', self._callback_check, 233)
            self.chkSRRQ35.get_child().props.width_request = 700
            self.chkSRRQ35.connect('toggled', self._callback_check, 234)
            self.chkSRRQ36.get_child().props.width_request = 700
            self.chkSRRQ36.connect('toggled', self._callback_check, 235)
            self.chkSRRQ37.get_child().props.width_request = 700
            self.chkSRRQ37.connect('toggled', self._callback_check, 236)
            self.chkSRRQ38.get_child().props.width_request = 700
            self.chkSRRQ38.connect('toggled', self._callback_check, 237)
            self.chkSRRQ39.get_child().props.width_request = 700
            self.chkSRRQ39.connect('toggled', self._callback_check, 238)
            self.chkSRRQ40.get_child().props.width_request = 700
            self.chkSRRQ40.connect('toggled', self._callback_check, 239)

            self.lblSRRQ41.set_alignment(xalign=0.05, yalign=0.05)
            self.lblSRRQ41.set_justify(gtk.JUSTIFY_LEFT)
            self.lblSRRQ42.set_alignment(xalign=0.05, yalign=0.05)
            self.lblSRRQ42.set_justify(gtk.JUSTIFY_LEFT)
            self.lblSRRQ43.set_alignment(xalign=0.05, yalign=0.05)
            self.lblSRRQ43.set_justify(gtk.JUSTIFY_LEFT)
            self.lblSRRQ44.set_alignment(xalign=0.05, yalign=0.05)
            self.lblSRRQ44.set_justify(gtk.JUSTIFY_LEFT)
            self.lblSRRQ45.set_alignment(xalign=0.05, yalign=0.05)
            self.lblSRRQ45.set_justify(gtk.JUSTIFY_LEFT)
            self.lblSRRQ46.set_alignment(xalign=0.05, yalign=0.05)
            self.lblSRRQ46.set_justify(gtk.JUSTIFY_LEFT)
            self.lblSRRQ47.set_alignment(xalign=0.05, yalign=0.05)
            self.lblSRRQ47.set_justify(gtk.JUSTIFY_LEFT)
            self.lblSRRQ48.set_alignment(xalign=0.05, yalign=0.05)
            self.lblSRRQ48.set_justify(gtk.JUSTIFY_LEFT)
            self.lblSRRQ49.set_alignment(xalign=0.05, yalign=0.05)
            self.lblSRRQ49.set_justify(gtk.JUSTIFY_LEFT)
            self.lblSRRQ50.set_alignment(xalign=0.05, yalign=0.05)
            self.lblSRRQ50.set_justify(gtk.JUSTIFY_LEFT)

            self.txtSRRQ41.connect('focus-out-event', self._callback_entry,
                                   'int', 240)
            self.txtSRRQ42.connect('focus-out-event', self._callback_entry,
                                   'int', 241)
            self.txtSRRQ43.connect('focus-out-event', self._callback_entry,
                                   'int', 242)
            self.txtSRRQ44.connect('focus-out-event', self._callback_entry,
                                   'int', 243)
            self.txtSRRQ45.connect('focus-out-event', self._callback_entry,
                                   'int', 244)
            self.txtSRRQ46.connect('focus-out-event', self._callback_entry,
                                   'int', 245)
            self.txtSRRQ47.connect('focus-out-event', self._callback_entry,
                                   'int', 246)
            self.txtSRRQ48.connect('focus-out-event', self._callback_entry,
                                   'int', 247)
            self.txtSRRQ49.connect('focus-out-event', self._callback_entry,
                                   'int', 248)
            self.txtSRRQ50.connect('focus-out-event', self._callback_entry,
                                   'int', 249)

            self.lblSRR.set_markup("<span weight='bold'>" +
                                   _("Requirements\nReview") +
                                   "</span>")
            self.lblSRR.set_alignment(xalign=0.5, yalign=0.5)
            self.lblSRR.set_justify(gtk.JUSTIFY_CENTER)
            self.lblSRR.set_angle(90)
            self.lblSRR.show_all()
            self.lblSRR.set_tooltip_text(_("Allows assessment of the reliability risk at requirements review."))

            return False

        def _pdr_widgets_create(self):
            """
            Method to create the preliminary design review widgets.
            """

            self.chkPDRQ1.get_child().props.width_request = 700
            self.chkPDRQ1.connect('toggled', self._callback_check, 300)
            self.chkPDRQ2.get_child().props.width_request = 700
            self.chkPDRQ2.connect('toggled', self._callback_check, 301)
            self.chkPDRQ3.get_child().props.width_request = 700
            self.chkPDRQ3.connect('toggled', self._callback_check, 302)
            self.chkPDRQ4.get_child().props.width_request = 700
            self.chkPDRQ4.connect('toggled', self._callback_check, 303)
            self.chkPDRQ5.get_child().props.width_request = 700
            self.chkPDRQ5.connect('toggled', self._callback_check, 304)
            self.chkPDRQ6.get_child().props.width_request = 700
            self.chkPDRQ6.connect('toggled', self._callback_check, 305)
            self.chkPDRQ7.get_child().props.width_request = 700
            self.chkPDRQ7.connect('toggled', self._callback_check, 306)
            self.chkPDRQ8.get_child().props.width_request = 700
            self.chkPDRQ8.connect('toggled', self._callback_check, 307)
            self.chkPDRQ9.get_child().props.width_request = 700
            self.chkPDRQ9.connect('toggled', self._callback_check, 308)
            self.chkPDRQ10.get_child().props.width_request = 700
            self.chkPDRQ10.connect('toggled', self._callback_check, 309)
            self.chkPDRQ11.get_child().props.width_request = 700
            self.chkPDRQ11.connect('toggled', self._callback_check, 310)
            self.chkPDRQ12.get_child().props.width_request = 700
            self.chkPDRQ12.connect('toggled', self._callback_check, 311)
            self.chkPDRQ13.get_child().props.width_request = 700
            self.chkPDRQ13.connect('toggled', self._callback_check, 312)
            self.chkPDRQ14.get_child().props.width_request = 700
            self.chkPDRQ14.connect('toggled', self._callback_check, 313)
            self.chkPDRQ15.get_child().props.width_request = 700
            self.chkPDRQ15.connect('toggled', self._callback_check, 314)
            self.chkPDRQ16.get_child().props.width_request = 700
            self.chkPDRQ16.connect('toggled', self._callback_check, 315)
            self.chkPDRQ17.get_child().props.width_request = 700
            self.chkPDRQ17.connect('toggled', self._callback_check, 316)
            self.chkPDRQ18.get_child().props.width_request = 700
            self.chkPDRQ18.connect('toggled', self._callback_check, 317)
            self.chkPDRQ19.get_child().props.width_request = 700
            self.chkPDRQ19.connect('toggled', self._callback_check, 318)
            self.chkPDRQ20.get_child().props.width_request = 700
            self.chkPDRQ20.connect('toggled', self._callback_check, 319)
            self.chkPDRQ21.get_child().props.width_request = 700
            self.chkPDRQ21.connect('toggled', self._callback_check, 320)
            self.chkPDRQ22.get_child().props.width_request = 700
            self.chkPDRQ22.connect('toggled', self._callback_check, 321)
            self.chkPDRQ23.get_child().props.width_request = 700
            self.chkPDRQ23.connect('toggled', self._callback_check, 322)
            self.chkPDRQ24.get_child().props.width_request = 700
            self.chkPDRQ24.connect('toggled', self._callback_check, 323)
            self.chkPDRQ25.get_child().props.width_request = 700
            self.chkPDRQ25.connect('toggled', self._callback_check, 324)
            self.chkPDRQ26.get_child().props.width_request = 700
            self.chkPDRQ26.connect('toggled', self._callback_check, 325)
            self.chkPDRQ27.get_child().props.width_request = 700
            self.chkPDRQ27.connect('toggled', self._callback_check, 326)
            self.chkPDRQ28.get_child().props.width_request = 700
            self.chkPDRQ28.connect('toggled', self._callback_check, 327)
            self.chkPDRQ29.get_child().props.width_request = 700
            self.chkPDRQ29.connect('toggled', self._callback_check, 328)

            self.lblPDRQ30.set_alignment(xalign=0.05, yalign=0.05)
            self.lblPDRQ30.set_justify(gtk.JUSTIFY_LEFT)
            self.lblPDRQ31.set_alignment(xalign=0.05, yalign=0.05)
            self.lblPDRQ31.set_justify(gtk.JUSTIFY_LEFT)
            self.lblPDRQ32.set_alignment(xalign=0.05, yalign=0.05)
            self.lblPDRQ32.set_justify(gtk.JUSTIFY_LEFT)
            self.lblPDRQ33.set_alignment(xalign=0.05, yalign=0.05)
            self.lblPDRQ33.set_justify(gtk.JUSTIFY_LEFT)
            self.lblPDRQ34.set_alignment(xalign=0.05, yalign=0.05)
            self.lblPDRQ34.set_justify(gtk.JUSTIFY_LEFT)
            self.lblPDRQ35.set_alignment(xalign=0.05, yalign=0.05)
            self.lblPDRQ35.set_justify(gtk.JUSTIFY_LEFT)
            self.lblPDRQ36.set_alignment(xalign=0.05, yalign=0.05)
            self.lblPDRQ36.set_justify(gtk.JUSTIFY_LEFT)
            self.lblPDRQ37.set_alignment(xalign=0.05, yalign=0.05)
            self.lblPDRQ37.set_justify(gtk.JUSTIFY_LEFT)
            self.lblPDRQ38.set_alignment(xalign=0.05, yalign=0.05)
            self.lblPDRQ38.set_justify(gtk.JUSTIFY_LEFT)
            self.lblPDRQ39.set_alignment(xalign=0.05, yalign=0.05)
            self.lblPDRQ39.set_justify(gtk.JUSTIFY_LEFT)

            self.txtPDRQ30.connect('focus-out-event', self._callback_entry,
                                   'int', 329)
            self.txtPDRQ31.connect('focus-out-event', self._callback_entry,
                                   'int', 330)
            self.txtPDRQ32.connect('focus-out-event', self._callback_entry,
                                   'int', 331)
            self.txtPDRQ33.connect('focus-out-event', self._callback_entry,
                                   'int', 332)
            self.txtPDRQ34.connect('focus-out-event', self._callback_entry,
                                   'int', 333)
            self.txtPDRQ35.connect('focus-out-event', self._callback_entry,
                                   'int', 334)
            self.txtPDRQ36.connect('focus-out-event', self._callback_entry,
                                   'int', 335)
            self.txtPDRQ37.connect('focus-out-event', self._callback_entry,
                                   'int', 336)
            self.txtPDRQ38.connect('focus-out-event', self._callback_entry,
                                   'int', 337)
            self.txtPDRQ39.connect('focus-out-event', self._callback_entry,
                                   'int', 338)

            self.lblPDR.set_markup("<span weight='bold'>" +
                                   _("Preliminary\nDesign\nReview") +
                                   "</span>")
            self.lblPDR.set_alignment(xalign=0.5, yalign=0.5)
            self.lblPDR.set_justify(gtk.JUSTIFY_CENTER)
            self.lblPDR.set_angle(90)
            self.lblPDR.show_all()
            self.lblPDR.set_tooltip_text(_("Allows assessment of the reliability risk at the preliminary design review."))

            return False

        def _cdr_widgets_create(self):
            """
            Method to create the critical design review widgets.
            """

            self.chkCDRQ1.connect('toggled', self._callback_check, 400)
            self.chkCDRQ2.connect('toggled', self._callback_check, 401)
            self.chkCDRQ3.connect('toggled', self._callback_check, 402)
            self.chkCDRQ4.connect('toggled', self._callback_check, 403)
            self.chkCDRQ5.connect('toggled', self._callback_check, 404)
            self.chkCDRQ6.connect('toggled', self._callback_check, 405)
            self.chkCDRQ7.connect('toggled', self._callback_check, 406)
            self.chkCDRQ8.connect('toggled', self._callback_check, 407)
            self.chkCDRQ9.connect('toggled', self._callback_check, 408)
            self.chkCDRQ10.connect('toggled', self._callback_check, 409)

            self.lblCDRQ11.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ11.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ12.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ12.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ13.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ13.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ14.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ14.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ15.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ15.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ16.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ16.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ17.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ17.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ18.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ18.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ19.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ19.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ20.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ20.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ21.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ21.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ22.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ22.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ23.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ23.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ24.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ24.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ25.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ25.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ26.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ26.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ27.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ27.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ28.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ28.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ29.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ29.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ30.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ30.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ31.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ31.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ32.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ32.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ33.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ33.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ34.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ34.set_justify(gtk.JUSTIFY_LEFT)

            self.txtCDRQ11.connect('focus-out-event', self._callback_entry,
                                   'int', 410)
            self.txtCDRQ12.connect('focus-out-event', self._callback_entry,
                                   'int', 411)
            self.txtCDRQ13.connect('focus-out-event', self._callback_entry,
                                   'int', 412)
            self.txtCDRQ14.connect('focus-out-event', self._callback_entry,
                                   'int', 413)
            self.txtCDRQ15.connect('focus-out-event', self._callback_entry,
                                   'int', 414)
            self.txtCDRQ16.connect('focus-out-event', self._callback_entry,
                                   'int', 415)
            self.txtCDRQ17.connect('focus-out-event', self._callback_entry,
                                   'int', 416)
            self.txtCDRQ18.connect('focus-out-event', self._callback_entry,
                                   'int', 417)
            self.txtCDRQ19.connect('focus-out-event', self._callback_entry,
                                   'int', 418)
            self.txtCDRQ20.connect('focus-out-event', self._callback_entry,
                                   'int', 419)
            self.txtCDRQ21.connect('focus-out-event', self._callback_entry,
                                   'int', 420)
            self.txtCDRQ22.connect('focus-out-event', self._callback_entry,
                                   'int', 421)
            self.txtCDRQ23.connect('focus-out-event', self._callback_entry,
                                   'int', 422)
            self.txtCDRQ24.connect('focus-out-event', self._callback_entry,
                                   'int', 423)
            self.txtCDRQ25.connect('focus-out-event', self._callback_entry,
                                   'int', 424)
            self.txtCDRQ26.connect('focus-out-event', self._callback_entry,
                                   'int', 425)
            self.txtCDRQ27.connect('focus-out-event', self._callback_entry,
                                   'int', 426)
            self.txtCDRQ28.connect('focus-out-event', self._callback_entry,
                                   'int', 427)
            self.txtCDRQ29.connect('focus-out-event', self._callback_entry,
                                   'int', 428)
            self.txtCDRQ30.connect('focus-out-event', self._callback_entry,
                                   'int', 429)
            self.txtCDRQ31.connect('focus-out-event', self._callback_entry,
                                   'int', 430)
            self.txtCDRQ32.connect('focus-out-event', self._callback_entry,
                                   'int', 431)
            self.txtCDRQ33.connect('focus-out-event', self._callback_entry,
                                   'int', 432)
            self.txtCDRQ34.connect('focus-out-event', self._callback_entry,
                                   'int', 433)

            self.chkCDRQ35.connect('toggled', self._callback_check, 434)
            self.chkCDRQ36.connect('toggled', self._callback_check, 435)
            self.chkCDRQ37.connect('toggled', self._callback_check, 436)
            self.chkCDRQ38.connect('toggled', self._callback_check, 437)
            self.chkCDRQ39.connect('toggled', self._callback_check, 438)
            self.chkCDRQ40.connect('toggled', self._callback_check, 439)
            self.chkCDRQ41.connect('toggled', self._callback_check, 440)
            self.chkCDRQ42.connect('toggled', self._callback_check, 441)
            self.chkCDRQ43.connect('toggled', self._callback_check, 442)
            self.chkCDRQ44.connect('toggled', self._callback_check, 443)
            self.chkCDRQ45.connect('toggled', self._callback_check, 444)
            self.chkCDRQ46.connect('toggled', self._callback_check, 445)

            self.lblCDRQ47.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ47.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ48.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ48.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ49.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ49.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ50.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ50.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ51.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ51.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ52.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ52.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ53.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ53.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ54.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ54.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ55.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ55.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ56.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ56.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ57.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ57.set_justify(gtk.JUSTIFY_LEFT)
            self.lblCDRQ58.set_alignment(xalign=0.05, yalign=0.05)
            self.lblCDRQ58.set_justify(gtk.JUSTIFY_LEFT)

            self.txtCDRQ47.connect('focus-out-event', self._callback_entry,
                                   'int', 446)
            self.txtCDRQ48.connect('focus-out-event', self._callback_entry,
                                   'int', 447)
            self.txtCDRQ49.connect('focus-out-event', self._callback_entry,
                                   'int', 448)
            self.txtCDRQ50.connect('focus-out-event', self._callback_entry,
                                   'int', 449)
            self.txtCDRQ51.connect('focus-out-event', self._callback_entry,
                                   'int', 450)
            self.txtCDRQ52.connect('focus-out-event', self._callback_entry,
                                   'int', 451)
            self.txtCDRQ53.connect('focus-out-event', self._callback_entry,
                                   'int', 452)
            self.txtCDRQ54.connect('focus-out-event', self._callback_entry,
                                   'int', 453)
            self.txtCDRQ55.connect('focus-out-event', self._callback_entry,
                                   'int', 454)
            self.txtCDRQ56.connect('focus-out-event', self._callback_entry,
                                   'int', 455)
            self.txtCDRQ57.connect('focus-out-event', self._callback_entry,
                                   'int', 456)
            self.txtCDRQ58.connect('focus-out-event', self._callback_entry,
                                   'int', 457)

            self.lblCDR.set_markup("<span weight='bold'>" +
                                   _(u"Critical\nDesign\nReview") +
                                   "</span>")
            self.lblCDR.set_alignment(xalign=0.5, yalign=0.5)
            self.lblCDR.set_justify(gtk.JUSTIFY_CENTER)
            self.lblCDR.set_angle(90)
            self.lblCDR.show_all()
            self.lblCDR.set_tooltip_text(_(u"Allows assessment of risk at the critical design review."))

            return False

        def _trr_widgets_create(self):
            """
            Method to create the test readiness review widgets.
            """

            self.chkTRRQ5.get_child().props.width_request = 700
            self.chkTRRQ5.connect('toggled', self._callback_check, 504)
            self.chkTRRQ6.get_child().props.width_request = 700
            self.chkTRRQ6.connect('toggled', self._callback_check, 505)
            self.chkTRRQ7.get_child().props.width_request = 700
            self.chkTRRQ7.connect('toggled', self._callback_check, 506)
            self.chkTRRQ8.get_child().props.width_request = 700
            self.chkTRRQ8.connect('toggled', self._callback_check, 507)
            self.chkTRRQ9.get_child().props.width_request = 700
            self.chkTRRQ9.connect('toggled', self._callback_check, 508)
            self.chkTRRQ10.get_child().props.width_request = 700
            self.chkTRRQ10.connect('toggled', self._callback_check, 509)
            self.chkTRRQ11.get_child().props.width_request = 700
            self.chkTRRQ11.connect('toggled', self._callback_check, 510)
            self.chkTRRQ12.get_child().props.width_request = 700
            self.chkTRRQ12.connect('toggled', self._callback_check, 511)
            self.chkTRRQ13.get_child().props.width_request = 700
            self.chkTRRQ13.connect('toggled', self._callback_check, 512)
            self.chkTRRQ14.get_child().props.width_request = 700
            self.chkTRRQ14.connect('toggled', self._callback_check, 513)
            self.chkTRRQ15.get_child().props.width_request = 700
            self.chkTRRQ15.connect('toggled', self._callback_check, 514)
            self.chkTRRQ16.get_child().props.width_request = 700
            self.chkTRRQ16.connect('toggled', self._callback_check, 515)
            self.chkTRRQ17.get_child().props.width_request = 700
            self.chkTRRQ17.connect('toggled', self._callback_check, 516)
            self.chkTRRQ18.get_child().props.width_request = 700
            self.chkTRRQ18.connect('toggled', self._callback_check, 517)
            self.chkTRRQ19.get_child().props.width_request = 700
            self.chkTRRQ19.connect('toggled', self._callback_check, 518)
            self.chkTRRQ20.get_child().props.width_request = 700
            self.chkTRRQ20.connect('toggled', self._callback_check, 519)

            self.lblTRRQ1.set_alignment(xalign=0.05, yalign=0.05)
            self.lblTRRQ1.set_justify(gtk.JUSTIFY_LEFT)
            self.lblTRRQ2.set_alignment(xalign=0.05, yalign=0.05)
            self.lblTRRQ2.set_justify(gtk.JUSTIFY_LEFT)
            self.lblTRRQ3.set_alignment(xalign=0.05, yalign=0.05)
            self.lblTRRQ3.set_justify(gtk.JUSTIFY_LEFT)
            self.lblTRRQ4.set_alignment(xalign=0.05, yalign=0.05)
            self.lblTRRQ4.set_justify(gtk.JUSTIFY_LEFT)
            self.lblTRRQ21.set_alignment(xalign=0.05, yalign=0.05)
            self.lblTRRQ21.set_justify(gtk.JUSTIFY_LEFT)
            self.lblTRRQ22.set_alignment(xalign=0.05, yalign=0.05)
            self.lblTRRQ22.set_justify(gtk.JUSTIFY_LEFT)
            self.lblTRRQ23.set_alignment(xalign=0.05, yalign=0.05)
            self.lblTRRQ23.set_justify(gtk.JUSTIFY_LEFT)
            self.lblTRRQ24.set_alignment(xalign=0.05, yalign=0.05)
            self.lblTRRQ24.set_justify(gtk.JUSTIFY_LEFT)

            self.txtTRRQ1.connect('focus-out-event', self._callback_entry,
                                   'int', 500)
            self.txtTRRQ2.connect('focus-out-event', self._callback_entry,
                                   'int', 501)
            self.txtTRRQ3.connect('focus-out-event', self._callback_entry,
                                   'int', 502)
            self.txtTRRQ4.connect('focus-out-event', self._callback_entry,
                                   'int', 503)
            self.txtTRRQ21.connect('focus-out-event', self._callback_entry,
                                   'int', 520)
            self.txtTRRQ22.connect('focus-out-event', self._callback_entry,
                                   'int', 521)
            self.txtTRRQ23.connect('focus-out-event', self._callback_entry,
                                   'int', 522)
            self.txtTRRQ24.connect('focus-out-event', self._callback_entry,
                                   'int', 523)

            self.lblTRR.set_markup("<span weight='bold'>" +
                                   _("Test\nReadiness\nReview") +
                                   "</span>")
            self.lblTRR.set_alignment(xalign=0.5, yalign=0.5)
            self.lblTRR.set_justify(gtk.JUSTIFY_CENTER)
            self.lblTRR.set_angle(90)
            self.lblTRR.show_all()
            self.lblTRR.set_tooltip_text(_("Allows assessment of risk at the test readiness review."))

            return False

        if _development_env_widgets_create(self):
            self._app.debug_log.error("software.py: Failed to create Development Environment widgets.")
        if _srr_widgets_create(self):
            self._app.debug_log.error("software.py: Failed to create Requirements Review widgets.")
        if _pdr_widgets_create(self):
            self._app.debug_log.error("software.py: Failed to create Preliminary Design Review widgets.")
        if _cdr_widgets_create(self):
            self._app.debug_log.error("software.py: Failed to create Critical Design Review widgets.")
        if _trr_widgets_create(self):
            self._app.debug_log.error("software.py: Failed to create Test Readiness Review widgets.")

        self.nbkRiskAnalysis.set_tab_pos(gtk.POS_RIGHT)
        self.nbkRiskAnalysis.connect('switch_page',
                                     self._notebook_page_switched, 1)

        model = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING)
        self.tvwRiskMap.set_model(model)
        self.tvwRiskMap.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        label = gtk.Label()
        label.set_line_wrap(True)
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.set_markup("<span weight='bold'>Software\nModule</span>")
        label.set_use_markup(True)
        label.show_all()
        column = gtk.TreeViewColumn()
        column.set_widget(label)
        column.set_visible(True)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        cell = gtk.CellRendererText()
        cell.set_property('visible', True)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0)
        self.tvwRiskMap.append_column(column)

        label = gtk.Label()
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.set_property('angle', 90)
        label.set_markup("<span weight='bold'>Application\nRisk</span>")
        label.set_use_markup(True)
        label.show_all()
        column = gtk.TreeViewColumn()
        column.set_widget(label)
        column.set_visible(True)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        cell = gtk.CellRendererText()       # Cell background color.
        cell.set_property('visible', True)
        column.pack_start(cell, True)
        column.set_attributes(cell, background=1)
        self.tvwRiskMap.append_column(column)

        label = gtk.Label()
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.set_property('angle', 90)
        label.set_markup("<span weight='bold'>Organization\nRisk</span>")
        label.set_use_markup(True)
        label.show_all()
        column = gtk.TreeViewColumn()
        column.set_widget(label)
        column.set_visible(True)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        cell = gtk.CellRendererText()       # Cell background color.
        cell.set_property('visible', True)
        column.pack_start(cell, True)
        column.set_attributes(cell, background=2)
        self.tvwRiskMap.append_column(column)

        label = gtk.Label()
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.set_property('angle', 90)
        label.set_markup("<span weight='bold'>Anomaly\nManagement\nRisk</span>")
        label.set_use_markup(True)
        label.show_all()
        column = gtk.TreeViewColumn()
        column.set_widget(label)
        column.set_visible(True)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        cell = gtk.CellRendererText()       # Cell background color.
        cell.set_property('visible', True)
        column.pack_start(cell, True)
        column.set_attributes(cell, background=3)
        self.tvwRiskMap.append_column(column)

        label = gtk.Label()
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.set_property('angle', 90)
        label.set_markup("<span weight='bold'>Quality\nAssurance\nRisk</span>")
        label.set_use_markup(True)
        label.show_all()
        column = gtk.TreeViewColumn()
        column.set_widget(label)
        column.set_visible(True)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        cell = gtk.CellRendererText()       # Cell background color.
        cell.set_property('visible', True)
        column.pack_start(cell, True)
        column.set_attributes(cell, background=4)
        self.tvwRiskMap.append_column(column)

        label = gtk.Label()
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.set_property('angle', 90)
        label.set_markup("<span weight='bold'>Code\nComplexity\nRisk</span>")
        label.set_use_markup(True)
        label.show_all()
        column = gtk.TreeViewColumn()
        column.set_widget(label)
        column.set_visible(True)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        cell = gtk.CellRendererText()       # Cell background color.
        cell.set_property('visible', True)
        column.pack_start(cell, True)
        column.set_attributes(cell, background=5)
        self.tvwRiskMap.append_column(column)

        label = gtk.Label()
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.set_property('angle', 90)
        label.set_markup("<span weight='bold'>Overall\nRisk</span>")
        label.set_use_markup(True)
        label.show_all()
        column = gtk.TreeViewColumn()
        column.set_widget(label)
        column.set_visible(True)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        cell = gtk.CellRendererText()       # Cell background color.
        cell.set_property('visible', True)
        column.pack_start(cell, True)
        column.set_attributes(cell, background=6)
        self.tvwRiskMap.append_column(column)

        return False

    def _risk_analysis_tab_create(self):
        """
        Method to create the Risk Analysis gtk.Notebook tab and add it to the
        gtk.Notebook in the proper location.
        """

# Create a notebook page for each phase in the program development cycle.

        def _development_env_tab_create(self):
            """
            Method to create and insert the Development Environment gtk.Notebook()
            tab for the Software Object risk analysis.
            """

            hbox = gtk.HBox()
            self.hbxDevelopmentEnvironment.pack_start(hbox)

    # Populate the first (left most) frame for assessing the development
    # organization.
            table = gtk.Table(rows=8)

            scrollwindow = gtk.ScrolledWindow()
            scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrollwindow.add_with_viewport(table)

            frame = _widg.make_frame(_label_=_(u"Organization"))
            frame.set_shadow_type(gtk.SHADOW_NONE)
            frame.add(scrollwindow)

            hbox.pack_start(frame)

            table.attach(self.chkDevelopmentQ1, 0, 1, 0, 1, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ2, 0, 1, 1, 2, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ3, 0, 1, 2, 3, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ4, 0, 1, 3, 4, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ5, 0, 1, 4, 5, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ6, 0, 1, 5, 6, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ7, 0, 1, 6, 7, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ8, 0, 1, 7, 8, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)

    # Populate the second frame for assessing planned anomaly management.
            table = gtk.Table(rows=9)

            scrollwindow = gtk.ScrolledWindow()
            scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrollwindow.add_with_viewport(table)

            frame = _widg.make_frame(_label_=_(u"Methods"))
            frame.set_shadow_type(gtk.SHADOW_NONE)
            frame.add(scrollwindow)

            hbox.pack_end(frame)

            table.attach(self.chkDevelopmentQ9, 0, 1, 0, 1, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ10, 0, 1, 1, 2, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ11, 0, 1, 2, 3, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ12, 0, 1, 3, 4, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ13, 0, 1, 4, 5, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ14, 0, 1, 5, 6, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ15, 0, 1, 6, 7, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ16, 0, 1, 7, 8, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ17, 0, 1, 8, 9, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)

    # Populate the third frame for assessing documentation requirements.
            hbox = gtk.HBox()
            self.hbxDevelopmentEnvironment.pack_end(hbox)

            table = gtk.Table(rows=11)

            scrollwindow = gtk.ScrolledWindow()
            scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrollwindow.add_with_viewport(table)

            frame = _widg.make_frame(_label_=_(u"Documentation"))
            frame.set_shadow_type(gtk.SHADOW_NONE)
            frame.add(scrollwindow)

            hbox.pack_start(frame)

            table.attach(self.chkDevelopmentQ18, 0, 1, 0, 1, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ19, 0, 1, 1, 2, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ20, 0, 1, 2, 3, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ21, 0, 1, 3, 4, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ22, 0, 1, 4, 5, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ23, 0, 1, 5, 6, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ24, 0, 1, 6, 7, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ25, 0, 1, 7, 8, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ26, 0, 1, 8, 9, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ27, 0, 1, 9, 10, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ28, 0, 1, 10, 11, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)

    # Populate the fourth (right most) frame for assessing development tools and
    # testing techniques planned.
            table = gtk.Table(rows=15)

            scrollwindow = gtk.ScrolledWindow()
            scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrollwindow.add_with_viewport(table)

            frame = _widg.make_frame(_label_=_(u"Tools &amp; Test Techniques"))
            frame.set_shadow_type(gtk.SHADOW_NONE)
            frame.add(scrollwindow)

            hbox.pack_end(frame)

            table.attach(self.chkDevelopmentQ29, 0, 1, 0, 1, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ30, 0, 1, 1, 2, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ31, 0, 1, 2, 3, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ32, 0, 1, 3, 4, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ33, 0, 1, 4, 5, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ34, 0, 1, 5, 6, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ35, 0, 1, 6, 7, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ36, 0, 1, 7, 8, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ37, 0, 1, 8, 9, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ38, 0, 1, 9, 10, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ39, 0, 1, 10, 11, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ40, 0, 1, 11, 12, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ41, 0, 1, 12, 13, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ42, 0, 1, 13, 14, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkDevelopmentQ43, 0, 1, 14, 15, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)

            label = gtk.Label()
            label.set_markup("<span weight='bold'>" +
                             _("Development\nEnvironment") +
                             "</span>")
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.set_angle(90)
            label.show_all()
            label.set_tooltip_text(_("Allows assessment of the development environment."))
            self.nbkRiskAnalysis.insert_page(self.hbxDevelopmentEnvironment,
                                             tab_label=label,
                                             position=0)

            return False

        def _srr_tab_create(self):
            """
            Method to create the Software Requirements Review gtk.Notebook tab and
            add it to the gtk.Notebook in the proper location.
            """

    # Create the Anomaly Management table.
            table = gtk.Table(rows=22, columns=4)

            scrollwindow = gtk.ScrolledWindow()
            scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrollwindow.add_with_viewport(table)

            frame = _widg.make_frame(_label_=_(u"Anomaly Management"))
            frame.set_shadow_type(gtk.SHADOW_NONE)
            frame.add(scrollwindow)

            table.attach(self.lblSRRQ41, 0, 1, 0, 1, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblSRRQ42, 0, 1, 1, 2, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblSRRQ43, 0, 1, 2, 3, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblSRRQ44, 0, 1, 3, 4, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtSRRQ41, 1, 2, 0, 1, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtSRRQ42, 1, 2, 1, 2, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtSRRQ43, 1, 2, 2, 3, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtSRRQ44, 1, 2, 3, 4, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ1, 0, 4, 4, 5, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblSRRQ45, 0, 1, 5, 6, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblSRRQ46, 0, 1, 6, 7, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtSRRQ45, 1, 2, 5, 6, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtSRRQ46, 1, 2, 6, 7, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ2, 0, 4, 7, 8, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ3, 0, 4, 8, 9, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ4, 0, 4, 9, 10, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ5, 0, 4, 10, 11, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ6, 0, 4, 11, 12, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ7, 0, 4, 12, 13, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ8, 0, 4, 13, 14, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ9, 0, 4, 14, 15, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ10, 0, 4, 15, 16, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ11, 0, 4, 16, 17, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ12, 0, 4, 17, 18, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ13, 0, 4, 18, 19, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ14, 0, 4, 19, 20, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ15, 0, 4, 20, 21, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ16, 0, 4, 21, 22, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)

            self.hpnSRR.pack1(frame, resize=False)

    # Create the Quality Control table.
            table = gtk.Table(rows=28, columns=4)

            scrollwindow = gtk.ScrolledWindow()
            scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrollwindow.add_with_viewport(table)

            frame = _widg.make_frame(_label_=_(u"Software Quality Control"))
            frame.set_shadow_type(gtk.SHADOW_NONE)
            frame.add(scrollwindow)

            table.attach(self.chkSRRQ17, 0, 4, 0, 1, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, ypadding=5)
            table.attach(self.chkSRRQ18, 0, 4, 1, 2, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ19, 0, 4, 2, 3, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ20, 0, 4, 3, 4, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ21, 0, 4, 4, 5, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ22, 0, 4, 5, 6, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ23, 0, 4, 6, 7, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ24, 0, 4, 7, 8, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)

            table.attach(self.lblSRRQ47, 0, 1, 8, 9, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblSRRQ48, 0, 1, 9, 10, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblSRRQ49, 0, 1, 10, 11, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblSRRQ50, 0, 1, 11, 12, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtSRRQ47, 1, 2, 8, 9, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtSRRQ48, 1, 2, 9, 10, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtSRRQ49, 1, 2, 10, 11, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtSRRQ50, 1, 2, 11, 12, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)

            table.attach(self.chkSRRQ25, 0, 4, 12, 13, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ26, 0, 4, 13, 14, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ27, 0, 4, 14, 15, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ28, 0, 4, 15, 16, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ29, 0, 4, 16, 17, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ30, 0, 4, 17, 18, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ31, 0, 4, 18, 19, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ32, 0, 4, 19, 20, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ33, 0, 4, 20, 21, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ34, 0, 4, 21, 22, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ35, 0, 4, 22, 23, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ36, 0, 4, 23, 24, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ37, 0, 4, 24, 25, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ38, 0, 4, 25, 26, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ39, 0, 4, 26, 27, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkSRRQ40, 0, 4, 27, 28, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)

            self.hpnSRR.pack2(frame, resize=False)

    # Insert the tab.
            self.nbkRiskAnalysis.insert_page(self.hpnSRR,
                                             tab_label=self.lblSRR,
                                             position=-1)

            return False

        def _pdr_tab_create(self):
            """
            Method to create the Preliminary Design Review gtk.Notebook tab and add
            it to the gtk.Notebook in the proper location.
            """

    # Create the table for Anomaly Management questions.
            table = gtk.Table(rows=14, columns=4)

            scrollwindow = gtk.ScrolledWindow()
            scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrollwindow.add_with_viewport(table)

            frame = _widg.make_frame(_label_=_(u"Anomaly Management"))
            frame.set_shadow_type(gtk.SHADOW_NONE)
            frame.add(scrollwindow)

            table.attach(self.chkPDRQ1, 0, 4, 0, 1, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ2, 0, 4, 1, 2, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ3, 0, 4, 2, 3, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ4, 0, 4, 3, 4, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ5, 0, 4, 4, 5, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ6, 0, 4, 5, 6, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ7, 0, 4, 6, 7, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ8, 0, 4, 7, 8, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ9, 0, 4, 8, 9, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ10, 0, 4, 9, 10, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ11, 0, 4, 10, 11, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ12, 0, 4, 11, 12, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ13, 0, 4, 12, 13, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ14, 0, 4, 13, 14, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)

            self.hpnPDR.pack1(frame, resize=False)

    # Create the table for Quaility Control questions.
            table = gtk.Table(rows=25, columns=4)

            scrollwindow = gtk.ScrolledWindow()
            scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrollwindow.add_with_viewport(table)

            frame = _widg.make_frame(_label_=_(u"Software Quality Control"))
            frame.set_shadow_type(gtk.SHADOW_NONE)
            frame.add(scrollwindow)

            table.attach(self.chkPDRQ15, 0, 4, 0, 1, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ16, 0, 4, 1, 2, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ17, 0, 4, 2, 3, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblPDRQ30, 0, 1, 3, 4, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblPDRQ31, 0, 1, 4, 5, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtPDRQ30, 1, 2, 3, 4, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtPDRQ31, 1, 2, 4, 5, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ18, 0, 4, 5, 6, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ19, 0, 4, 6, 7, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblPDRQ32, 0, 1, 7, 8, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblPDRQ33, 0, 1, 8, 9, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblPDRQ34, 0, 1, 9, 10, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblPDRQ35, 0, 1, 10, 11, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblPDRQ36, 0, 1, 11, 12, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblPDRQ37, 0, 1, 12, 13, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtPDRQ32, 1, 2, 7, 8, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtPDRQ33, 1, 2, 8, 9, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtPDRQ34, 1, 2, 9, 10, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtPDRQ35, 1, 2, 10, 11, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtPDRQ36, 1, 2, 11, 12, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtPDRQ37, 1, 2, 12, 13, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ20, 0, 4, 13, 14, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ21, 0, 4, 14, 15, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblPDRQ38, 0, 1, 15, 16, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblPDRQ39, 0, 1, 16, 17, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtPDRQ38, 1, 2, 15, 16, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtPDRQ39, 1, 2, 16, 17, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ22, 0, 4, 17, 18, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ23, 0, 4, 18, 19, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ24, 0, 4, 19, 20, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ25, 0, 4, 20, 21, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ26, 0, 4, 21, 22, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ27, 0, 4, 22, 23, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ28, 0, 4, 23, 24, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkPDRQ29, 0, 4, 24, 25, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)

            self.hpnPDR.pack2(frame, resize=False)

    # Insert the tab.
            self.nbkRiskAnalysis.insert_page(self.hpnPDR,
                                             tab_label=self.lblPDR,
                                             position=-1)

            return False

        def _cdr_tab_create(self):
            """
            Method to create the Critical Design Review gtk.Notebook tab and add
            it to the gtk.Notebook in the proper location.
            """

    # Create the table for CSCI Anomaly Management questions.
            table = gtk.Table(rows=8, columns=4)

            scrollwindow = gtk.ScrolledWindow()
            scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrollwindow.add_with_viewport(table)

            self.fraCSCICDRAM.set_shadow_type(gtk.SHADOW_NONE)
            self.fraCSCICDRAM.add(scrollwindow)

            table.attach(self.chkCDRQ1, 0, 4, 0, 1, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ2, 0, 4, 1, 2, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ3, 0, 4, 2, 3, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ4, 0, 4, 3, 4, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ5, 0, 4, 4, 5, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ6, 0, 4, 5, 6, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ7, 0, 4, 6, 7, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ8, 0, 4, 7, 8, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)

            self.hpnCDR.pack1(self.fraCSCICDRAM, resize=False)

    # Create the table for CSCI Quaility Control questions.
            table = gtk.Table(rows=26, columns=4)

            scrollwindow = gtk.ScrolledWindow()
            scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrollwindow.add_with_viewport(table)

            self.fraCSCICDRSQ.set_shadow_type(gtk.SHADOW_NONE)
            self.fraCSCICDRSQ.add(scrollwindow)

            table.attach(self.chkCDRQ9, 0, 4, 0, 1, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ10, 0, 4, 1, 2, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ11, 0, 1, 2, 3, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ11, 1, 2, 2, 3, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ12, 0, 1, 3, 4, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ12, 1, 2, 3, 4, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ13, 0, 1, 4, 5, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ13, 1, 2, 4, 5, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ14, 0, 1, 5, 6, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ14, 1, 2, 5, 6, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ15, 0, 1, 6, 7, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ15, 1, 2, 6, 7, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ16, 0, 1, 7, 8, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ16, 1, 2, 7, 8, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ17, 0, 1, 8, 9, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ17, 1, 2, 8, 9, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ18, 0, 1, 9, 10, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ18, 1, 2, 9, 10, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ19, 0, 1, 10, 11, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ19, 1, 2, 10, 11, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ20, 0, 1, 11, 12, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ20, 1, 2, 11, 12, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ21, 0, 1, 12, 13, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ21, 1, 2, 12, 13, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ22, 0, 1, 13, 14, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ22, 1, 2, 13, 14, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ23, 0, 1, 14, 15, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ23, 1, 2, 14, 15, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ24, 0, 1, 15, 16, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ24, 1, 2, 15, 16, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ25, 0, 1, 16, 17, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ25, 1, 2, 16, 17, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ26, 0, 1, 17, 18, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ26, 1, 2, 17, 18, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ27, 0, 1, 18, 19, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ27, 1, 2, 18, 19, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ28, 0, 1, 19, 20, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ28, 1, 2, 19, 20, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ29, 0, 1, 20, 21, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ29, 1, 2, 20, 21, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ30, 0, 1, 21, 22, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ30, 1, 2, 21, 22, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ31, 0, 1, 22, 23, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ31, 1, 2, 22, 23, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ32, 0, 1, 23, 24, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ32, 1, 2, 23, 24, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ33, 0, 1, 24, 25, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ33, 1, 2, 24, 25, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ34, 0, 1, 25, 26, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ34, 1, 2, 25, 26, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)

            self.hpnCDR.pack2(self.fraCSCICDRSQ, resize=False)

    # Create the table for Unit Software Quality Control questions.
            table = gtk.Table(rows=24, columns=4)

            scrollwindow = gtk.ScrolledWindow()
            scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrollwindow.add_with_viewport(table)

            self.fraUnitCDRSQ.set_shadow_type(gtk.SHADOW_NONE)
            self.fraUnitCDRSQ.add(scrollwindow)

            table.attach(self.lblCDRQ47, 0, 1, 0, 1, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ47, 1, 2, 0, 1, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ48, 0, 1, 1, 2, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ48, 1, 2, 1, 2, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ35, 0, 4, 2, 3, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ49, 0, 4, 3, 4, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ49, 1, 2, 3, 4, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ50, 0, 4, 4, 5, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ50, 1, 2, 4, 5, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ46, 0, 4, 5, 6, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ51, 0, 4, 6, 7, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ51, 1, 2, 6, 7, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ36, 0, 4, 7, 8, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ52, 0, 4, 8, 9, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ52, 1, 2, 8, 9, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ53, 0, 4, 9, 10, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ53, 1, 2, 9, 10, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ54, 0, 4, 10, 11, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ54, 1, 2, 10, 11, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ55, 0, 4, 11, 12, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ55, 1, 2, 11, 12, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ56, 0, 4, 12, 13, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ56, 1, 2, 12, 13, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ37, 0, 4, 13, 14, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ38, 0, 4, 14, 15, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ57, 0, 4, 15, 16, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ57, 1, 2, 15, 16, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblCDRQ58, 0, 4, 16, 17, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtCDRQ58, 1, 2, 16, 17, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ39, 0, 4, 17, 18, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ40, 0, 4, 18, 19, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ41, 0, 4, 19, 20, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ42, 0, 4, 20, 21, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ43, 0, 4, 21, 22, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ44, 0, 4, 22, 23, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkCDRQ45, 0, 4, 23, 24, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)

    # Insert the tab.
            self.nbkRiskAnalysis.insert_page(self.hpnCDR,
                                             tab_label=self.lblCDR,
                                             position=-1)

            return False

        def _trr_tab_create(self):
            """
            Method to create the Test Readiness Review gtk.Notebook tab and add
            it to the gtk.Notebook in the proper location.
            """

    # Place the CSCI level Complexity and Modularity questions.
            table = gtk.Table(rows=4, columns=4)

            scrollwindow = gtk.ScrolledWindow()
            scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrollwindow.add_with_viewport(table)

            self.fraCSCITRRSX.set_shadow_type(gtk.SHADOW_NONE)
            self.fraCSCITRRSX.add(scrollwindow)

            table.attach(self.lblTRRQ1, 0, 1, 0, 1, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtTRRQ1, 1, 2, 0, 1, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblTRRQ2, 0, 1, 1, 2, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtTRRQ2, 1, 2, 1, 2, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblTRRQ3, 0, 1, 2, 3, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtTRRQ3, 1, 2, 2, 3, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblTRRQ4, 0, 1, 3, 4, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtTRRQ4, 1, 2, 3, 4, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)

            self.hpnCDR.pack1(self.fraCSCITRRSX, resize=False)

    # Place the Unit level Anomaly Management questions.
            table = gtk.Table(rows=2, columns=4)

            scrollwindow = gtk.ScrolledWindow()
            scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrollwindow.add_with_viewport(table)

            self.fraUnitTRRAM.set_shadow_type(gtk.SHADOW_NONE)
            self.fraUnitTRRAM.add(scrollwindow)

            table.attach(self.chkTRRQ5, 0, 4, 0, 1, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkTRRQ6, 0, 4, 1, 2, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)

    # Place the Unit level Software Quality questions.
            table = gtk.Table(rows=18, columns=4)

            scrollwindow = gtk.ScrolledWindow()
            scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrollwindow.add_with_viewport(table)

            self.fraUnitTRRSQ.set_shadow_type(gtk.SHADOW_NONE)
            self.fraUnitTRRSQ.add(scrollwindow)

            table.attach(self.chkTRRQ7, 0, 4, 0, 1, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkTRRQ8, 0, 4, 1, 2, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkTRRQ9, 0, 4, 2, 3, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkTRRQ10, 0, 4, 3, 4, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkTRRQ11, 0, 4, 4, 5, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkTRRQ12, 0, 4, 5, 6, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkTRRQ13, 0, 4, 6, 7, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkTRRQ14, 0, 4, 7, 8, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkTRRQ15, 0, 4, 8, 9, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkTRRQ16, 0, 4, 9, 10, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkTRRQ17, 0, 4, 10, 11, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkTRRQ18, 0, 4, 11, 12, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkTRRQ19, 0, 4, 12, 13, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.chkTRRQ20, 0, 4, 13, 14, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblTRRQ21, 0, 1, 14, 15, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtTRRQ21, 1, 2, 14, 15, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblTRRQ22, 0, 1, 15, 16, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtTRRQ22, 1, 2, 15, 16, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblTRRQ23, 0, 1, 16, 17, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtTRRQ23, 1, 2, 16, 17, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.lblTRRQ24, 0, 1, 17, 18, xoptions=gtk.FILL,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
            table.attach(self.txtTRRQ24, 1, 2, 17, 18, xoptions=gtk.SHRINK,
                         yoptions=gtk.FILL, xpadding=5, ypadding=5)
    # Insert the tab.
            self.nbkRiskAnalysis.insert_page(self.hpnTRR,
                                             tab_label=self.lblTRR,
                                             position=-1)

            return False

        if _development_env_tab_create(self):
            self._app.debug_log.error("software.py: Failed to create Development Environment tab.")
        if _srr_tab_create(self):
            self._app.debug_log.error("software.py: Failed to create Requirements Review tab.")
        if _pdr_tab_create(self):
            self._app.debug_log.error("software.py: Failed to create Preliminary design Review tab.")
        if _cdr_tab_create(self):
            self._app.debug_log.error("software.py: Failed to create Critical Design Review tab.")
        if _trr_tab_create(self):
            self._app.debug_log.error("software.py: Failed to create Test Readiness Review tab.")

        hpaned = gtk.HPaned()

        hpaned.pack1(self.nbkRiskAnalysis, resize=False)

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add(self.tvwRiskMap)

        frame = _widg.make_frame(_label_=_(u"Software Risk Map"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        hpaned.pack2(frame, resize=False, shrink=True)

# Insert the tab in the main notebook.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("Risk\nAnalysis") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Allows assessment of the reliability risk."))
        self.notebook.insert_page(hpaned,
                                  tab_label=label,
                                  position=-1)

        return False

    def _risk_analysis_tab_load(self):
        """
        Method to load the widgets on the Risk Analysis gtk.Notebook page.
        """

        def _development_env_tab_load(self):
            """
            Loads the widgets with development environment assessment
            information for the Software Object.
            """

            _values_ = (self.model.get_value(self._selected_row, 1),)
            _query_ = "SELECT fld_question_id, fld_y \
                       FROM tbl_software_development \
                       WHERE fld_software_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx)

            if(_results_ == '' or not _results_):
                return True

    # Populate the dictionary used to hold the answers to the development
    # environment questions.
            for i in range(43):
                self._development_env_[_results_[i][0]] = _results_[i][1]

    # Set the development environment widgets.
            self.chkDevelopmentQ1.set_active(self._development_env_[0])
            self.chkDevelopmentQ2.set_active(self._development_env_[1])
            self.chkDevelopmentQ3.set_active(self._development_env_[2])
            self.chkDevelopmentQ4.set_active(self._development_env_[3])
            self.chkDevelopmentQ5.set_active(self._development_env_[4])
            self.chkDevelopmentQ6.set_active(self._development_env_[5])
            self.chkDevelopmentQ7.set_active(self._development_env_[6])
            self.chkDevelopmentQ8.set_active(self._development_env_[7])
            self.chkDevelopmentQ9.set_active(self._development_env_[8])
            self.chkDevelopmentQ10.set_active(self._development_env_[9])
            self.chkDevelopmentQ11.set_active(self._development_env_[10])
            self.chkDevelopmentQ12.set_active(self._development_env_[11])
            self.chkDevelopmentQ13.set_active(self._development_env_[12])
            self.chkDevelopmentQ14.set_active(self._development_env_[13])
            self.chkDevelopmentQ15.set_active(self._development_env_[14])
            self.chkDevelopmentQ16.set_active(self._development_env_[15])
            self.chkDevelopmentQ17.set_active(self._development_env_[16])
            self.chkDevelopmentQ18.set_active(self._development_env_[17])
            self.chkDevelopmentQ19.set_active(self._development_env_[18])
            self.chkDevelopmentQ20.set_active(self._development_env_[19])
            self.chkDevelopmentQ21.set_active(self._development_env_[20])
            self.chkDevelopmentQ22.set_active(self._development_env_[21])
            self.chkDevelopmentQ23.set_active(self._development_env_[22])
            self.chkDevelopmentQ24.set_active(self._development_env_[23])
            self.chkDevelopmentQ25.set_active(self._development_env_[24])
            self.chkDevelopmentQ26.set_active(self._development_env_[25])
            self.chkDevelopmentQ27.set_active(self._development_env_[26])
            self.chkDevelopmentQ28.set_active(self._development_env_[27])
            self.chkDevelopmentQ29.set_active(self._development_env_[28])
            self.chkDevelopmentQ30.set_active(self._development_env_[29])
            self.chkDevelopmentQ31.set_active(self._development_env_[30])
            self.chkDevelopmentQ32.set_active(self._development_env_[31])
            self.chkDevelopmentQ33.set_active(self._development_env_[32])
            self.chkDevelopmentQ34.set_active(self._development_env_[33])
            self.chkDevelopmentQ35.set_active(self._development_env_[34])
            self.chkDevelopmentQ36.set_active(self._development_env_[35])
            self.chkDevelopmentQ37.set_active(self._development_env_[36])
            self.chkDevelopmentQ38.set_active(self._development_env_[37])
            self.chkDevelopmentQ39.set_active(self._development_env_[38])
            self.chkDevelopmentQ40.set_active(self._development_env_[39])
            self.chkDevelopmentQ41.set_active(self._development_env_[40])
            self.chkDevelopmentQ42.set_active(self._development_env_[41])
            self.chkDevelopmentQ43.set_active(self._development_env_[42])

            return False

        def _srr_tab_load(self):
            """
            Loads the widgets with requirements review Risk Analysis assessment
            information for the Software Object.
            """

            _values_ = (self.model.get_value(self._selected_row, 1),)
            _query_ = "SELECT fld_question_id, fld_y, fld_value \
                       FROM tbl_srr_ssr \
                       WHERE fld_software_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx)

            if(_results_ == '' or not _results_):
                return True

    # Populate the dictionary used to hold the answers to the development
    # environment questions.
            for i in range(40):
                self._srr_[_results_[i][0]] = _results_[i][1]

            for i in range(40, 50):
                self._srr_[_results_[i][0]] = _results_[i][2]

            self.chkSRRQ1.set_active(self._srr_[0])
            self.chkSRRQ2.set_active(self._srr_[1])
            self.chkSRRQ3.set_active(self._srr_[2])
            self.chkSRRQ4.set_active(self._srr_[3])
            self.chkSRRQ5.set_active(self._srr_[4])
            self.chkSRRQ6.set_active(self._srr_[5])
            self.chkSRRQ7.set_active(self._srr_[6])
            self.chkSRRQ8.set_active(self._srr_[7])
            self.chkSRRQ9.set_active(self._srr_[8])
            self.chkSRRQ10.set_active(self._srr_[9])
            self.chkSRRQ11.set_active(self._srr_[10])
            self.chkSRRQ12.set_active(self._srr_[11])
            self.chkSRRQ13.set_active(self._srr_[12])
            self.chkSRRQ14.set_active(self._srr_[13])
            self.chkSRRQ15.set_active(self._srr_[14])
            self.chkSRRQ16.set_active(self._srr_[15])
            self.chkSRRQ17.set_active(self._srr_[16])
            self.chkSRRQ18.set_active(self._srr_[17])
            self.chkSRRQ19.set_active(self._srr_[18])
            self.chkSRRQ20.set_active(self._srr_[19])
            self.chkSRRQ21.set_active(self._srr_[20])
            self.chkSRRQ22.set_active(self._srr_[21])
            self.chkSRRQ23.set_active(self._srr_[22])
            self.chkSRRQ24.set_active(self._srr_[23])
            self.chkSRRQ25.set_active(self._srr_[24])
            self.chkSRRQ26.set_active(self._srr_[25])
            self.chkSRRQ27.set_active(self._srr_[26])
            self.chkSRRQ28.set_active(self._srr_[27])
            self.chkSRRQ29.set_active(self._srr_[28])
            self.chkSRRQ30.set_active(self._srr_[29])
            self.chkSRRQ31.set_active(self._srr_[30])
            self.chkSRRQ32.set_active(self._srr_[31])
            self.chkSRRQ33.set_active(self._srr_[32])
            self.chkSRRQ34.set_active(self._srr_[33])
            self.chkSRRQ35.set_active(self._srr_[34])
            self.chkSRRQ36.set_active(self._srr_[35])
            self.chkSRRQ37.set_active(self._srr_[36])
            self.chkSRRQ38.set_active(self._srr_[37])
            self.chkSRRQ39.set_active(self._srr_[38])
            self.chkSRRQ40.set_active(self._srr_[39])

            self.txtSRRQ41.set_text(str(self._srr_[40]))
            self.txtSRRQ42.set_text(str(self._srr_[41]))
            self.txtSRRQ43.set_text(str(self._srr_[42]))
            self.txtSRRQ44.set_text(str(self._srr_[43]))
            self.txtSRRQ45.set_text(str(self._srr_[44]))
            self.txtSRRQ46.set_text(str(self._srr_[45]))
            self.txtSRRQ47.set_text(str(self._srr_[46]))
            self.txtSRRQ48.set_text(str(self._srr_[47]))
            self.txtSRRQ49.set_text(str(self._srr_[48]))
            self.txtSRRQ50.set_text(str(self._srr_[49]))

            return False

        def _pdr_tab_load(self):
            """
            Loads the widgets with preliminary design review Risk Analysis
            assessment information for the Software Object.
            """

            _values_ = (self.model.get_value(self._selected_row, 1),)
            _query_ = "SELECT fld_question_id, fld_y, fld_value \
                       FROM tbl_pdr \
                       WHERE fld_software_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx)

            if(_results_ == '' or not _results_):
                return True

    # Populate the dictionary used to hold the answers to the development
    # environment questions.
            for i in range(29):
                self._pdr_[_results_[i][0]] = _results_[i][1]

            for i in range(10):
                self._pdr_[_results_[i + 29][0]] = _results_[i + 29][2]

            self.chkPDRQ1.set_active(self._pdr_[0])
            self.chkPDRQ2.set_active(self._pdr_[1])
            self.chkPDRQ3.set_active(self._pdr_[2])
            self.chkPDRQ4.set_active(self._pdr_[3])
            self.chkPDRQ5.set_active(self._pdr_[4])
            self.chkPDRQ6.set_active(self._pdr_[5])
            self.chkPDRQ7.set_active(self._pdr_[6])
            self.chkPDRQ8.set_active(self._pdr_[7])
            self.chkPDRQ9.set_active(self._pdr_[8])
            self.chkPDRQ10.set_active(self._pdr_[9])
            self.chkPDRQ11.set_active(self._pdr_[10])
            self.chkPDRQ12.set_active(self._pdr_[11])
            self.chkPDRQ13.set_active(self._pdr_[12])
            self.chkPDRQ14.set_active(self._pdr_[13])
            self.chkPDRQ15.set_active(self._pdr_[14])
            self.chkPDRQ16.set_active(self._pdr_[15])
            self.chkPDRQ17.set_active(self._pdr_[16])
            self.chkPDRQ18.set_active(self._pdr_[17])
            self.chkPDRQ19.set_active(self._pdr_[18])
            self.chkPDRQ20.set_active(self._pdr_[19])
            self.chkPDRQ21.set_active(self._pdr_[20])
            self.chkPDRQ22.set_active(self._pdr_[21])
            self.chkPDRQ23.set_active(self._pdr_[22])
            self.chkPDRQ24.set_active(self._pdr_[23])
            self.chkPDRQ25.set_active(self._pdr_[24])
            self.chkPDRQ26.set_active(self._pdr_[25])
            self.chkPDRQ27.set_active(self._pdr_[26])
            self.chkPDRQ28.set_active(self._pdr_[27])
            self.chkPDRQ29.set_active(self._pdr_[28])

            self.txtPDRQ30.set_text(str(self._pdr_[29]))
            self.txtPDRQ31.set_text(str(self._pdr_[30]))
            self.txtPDRQ32.set_text(str(self._pdr_[31]))
            self.txtPDRQ33.set_text(str(self._pdr_[32]))
            self.txtPDRQ34.set_text(str(self._pdr_[33]))
            self.txtPDRQ35.set_text(str(self._pdr_[34]))
            self.txtPDRQ36.set_text(str(self._pdr_[35]))
            self.txtPDRQ37.set_text(str(self._pdr_[36]))
            self.txtPDRQ38.set_text(str(self._pdr_[37]))
            self.txtPDRQ39.set_text(str(self._pdr_[38]))

            return False

        def _cdr_tab_load(self):
            """
            Loads the widgets with critical design review Risk Analysis
            assessment information for the Software Object.
            """

            _values_ = (self.model.get_value(self._selected_row, 1),)
            _query_ = "SELECT fld_question_id, fld_y, fld_value \
                       FROM tbl_cdr \
                       WHERE fld_software_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx)

            if(_results_ == '' or not _results_):
                return True

    # Populate the dictionary used to hold the answers to the development
    # environment questions.
            for i in range(10):
                # Eight CSCI-level Yes/No questions from WS2D and two
                # CSCI-level Yes/No questions from WS3C.
                self._cdr_[_results_[i][0]] = _results_[i][1]
            for i in range(25):
                # Twenty-five CSCI-level quantity questions from WS4D.
                self._cdr_[_results_[i + 10][0]] = _results_[i + 10][2]
            for i in range(12):
                # Twelve Unit-level Yes/No questions from WS4D.
                self._cdr_[_results_[i + 35][0]] = _results_[i + 35][1]
            for i in range(12):
                # Twelve Unit-level quantity questions from WS4D.
                self._cdr_[_results_[i + 47][0]] = _results_[i + 47][2]

    # Set the CSCI widgets.
            self.chkCDRQ1.set_active(self._cdr_[0])
            self.chkCDRQ2.set_active(self._cdr_[1])
            self.chkCDRQ3.set_active(self._cdr_[2])
            self.chkCDRQ4.set_active(self._cdr_[3])
            self.chkCDRQ5.set_active(self._cdr_[4])
            self.chkCDRQ6.set_active(self._cdr_[5])
            self.chkCDRQ7.set_active(self._cdr_[6])
            self.chkCDRQ8.set_active(self._cdr_[7])
            self.chkCDRQ9.set_active(self._cdr_[8])
            self.chkCDRQ10.set_active(self._cdr_[9])
            self.txtCDRQ11.set_text(str(self._cdr_[10]))
            self.txtCDRQ12.set_text(str(self._cdr_[11]))
            self.txtCDRQ13.set_text(str(self._cdr_[12]))
            self.txtCDRQ14.set_text(str(self._cdr_[13]))
            self.txtCDRQ15.set_text(str(self._cdr_[14]))
            self.txtCDRQ16.set_text(str(self._cdr_[15]))
            self.txtCDRQ17.set_text(str(self._cdr_[16]))
            self.txtCDRQ18.set_text(str(self._cdr_[17]))
            self.txtCDRQ19.set_text(str(self._cdr_[18]))
            self.txtCDRQ20.set_text(str(self._cdr_[19]))
            self.txtCDRQ21.set_text(str(self._cdr_[20]))
            self.txtCDRQ22.set_text(str(self._cdr_[21]))
            self.txtCDRQ23.set_text(str(self._cdr_[22]))
            self.txtCDRQ24.set_text(str(self._cdr_[23]))
            self.txtCDRQ25.set_text(str(self._cdr_[24]))
            self.txtCDRQ26.set_text(str(self._cdr_[25]))
            self.txtCDRQ27.set_text(str(self._cdr_[26]))
            self.txtCDRQ28.set_text(str(self._cdr_[27]))
            self.txtCDRQ29.set_text(str(self._cdr_[28]))
            self.txtCDRQ30.set_text(str(self._cdr_[29]))
            self.txtCDRQ31.set_text(str(self._cdr_[30]))
            self.txtCDRQ32.set_text(str(self._cdr_[31]))
            self.txtCDRQ33.set_text(str(self._cdr_[32]))
            self.txtCDRQ34.set_text(str(self._cdr_[33]))

    # Set the Unit widgets.
            self.chkCDRQ35.set_active(self._cdr_[34])
            self.chkCDRQ36.set_active(self._cdr_[35])
            self.chkCDRQ37.set_active(self._cdr_[36])
            self.chkCDRQ38.set_active(self._cdr_[37])
            self.chkCDRQ39.set_active(self._cdr_[38])
            self.chkCDRQ40.set_active(self._cdr_[39])
            self.chkCDRQ41.set_active(self._cdr_[40])
            self.chkCDRQ42.set_active(self._cdr_[41])
            self.chkCDRQ43.set_active(self._cdr_[42])
            self.chkCDRQ44.set_active(self._cdr_[43])
            self.chkCDRQ45.set_active(self._cdr_[44])
            self.chkCDRQ46.set_active(self._cdr_[45])
            self.txtCDRQ47.set_text(str(self._cdr_[46]))
            self.txtCDRQ48.set_text(str(self._cdr_[47]))
            self.txtCDRQ49.set_text(str(self._cdr_[48]))
            self.txtCDRQ50.set_text(str(self._cdr_[49]))
            self.txtCDRQ51.set_text(str(self._cdr_[50]))
            self.txtCDRQ52.set_text(str(self._cdr_[51]))
            self.txtCDRQ53.set_text(str(self._cdr_[52]))
            self.txtCDRQ54.set_text(str(self._cdr_[53]))
            self.txtCDRQ55.set_text(str(self._cdr_[54]))
            self.txtCDRQ56.set_text(str(self._cdr_[55]))
            self.txtCDRQ57.set_text(str(self._cdr_[56]))
            self.txtCDRQ58.set_text(str(self._cdr_[57]))

            return False

        def _trr_tab_load(self):
            """
            Loads the widgets with test readiness review Risk Analysis
            assessment information for the Software Object.
            """

            _values_ = (self.model.get_value(self._selected_row, 1),)
            _query_ = "SELECT fld_question_id, fld_y, fld_value \
                       FROM tbl_trr \
                       WHERE fld_software_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx)

            if(_results_ == '' or not _results_):
                return True

    # Populate the dictionary used to hold the answers to the development
    # environment questions.
            for i in range(4):
                self._trr_[_results_[i][0]] = _results_[i][2]
            for i in range(4, 20):
                self._trr_[_results_[i][0]] = _results_[i][1]
            for i in range(20, 24):
                self._trr_[_results_[i][0]] = _results_[i][2]

            self.txtTRRQ1.set_text(str(self._trr_[0]))
            self.txtTRRQ2.set_text(str(self._trr_[1]))
            self.txtTRRQ3.set_text(str(self._trr_[2]))
            self.txtTRRQ4.set_text(str(self._trr_[3]))
            self.chkTRRQ5.set_active(self._trr_[4])
            self.chkTRRQ6.set_active(self._trr_[5])
            self.chkTRRQ7.set_active(self._trr_[6])
            self.chkTRRQ8.set_active(self._trr_[7])
            self.chkTRRQ9.set_active(self._trr_[8])
            self.chkTRRQ10.set_active(self._trr_[9])
            self.chkTRRQ11.set_active(self._trr_[10])
            self.chkTRRQ12.set_active(self._trr_[11])
            self.chkTRRQ13.set_active(self._trr_[12])
            self.chkTRRQ14.set_active(self._trr_[13])
            self.chkTRRQ15.set_active(self._trr_[14])
            self.chkTRRQ16.set_active(self._trr_[15])
            self.chkTRRQ17.set_active(self._trr_[16])
            self.chkTRRQ18.set_active(self._trr_[17])
            self.chkTRRQ19.set_active(self._trr_[18])
            self.chkTRRQ20.set_active(self._trr_[19])
            self.txtTRRQ21.set_text(str(self._trr_[20]))
            self.txtTRRQ22.set_text(str(self._trr_[21]))
            self.txtTRRQ23.set_text(str(self._trr_[22]))
            self.txtTRRQ24.set_text(str(self._trr_[23]))

            return False

        if _development_env_tab_load(self):
            self._app.debug_log.error("software.py: Failed to load Development Environment tab.")
        if _srr_tab_load(self):
            self._app.debug_log.error("software.py: Failed to load Requirements Review tab.")
        if _pdr_tab_load(self):
            self._app.debug_log.error("software.py: Failed to load Preliminary Design Review tab.")
        if _cdr_tab_load(self):
            self._app.debug_log.error("software.py: Failed to load Critical Design Review tab.")
        if _trr_tab_load(self):
            self._app.debug_log.error("software.py: Failed to load Test Readiness Review tab.")
        if self._risk_map_load():
            self._app.debug_log.error("software.py: Failed to load the Risk Map.")

        self._risk_analysis_tab_show()

        return False

    def _risk_map_load(self):
        """
        Method to load the SOFTWARE Risk Map.
        """

# Load the risk matrix.
        _query_ = "SELECT fld_description, fld_a, fld_d, fld_sa, fld_sq, \
                          fld_sx, fld_parent_module \
                   FROM tbl_software \
                   WHERE fld_revision_id=%d" % \
                   (self._app.REVISION.revision_id)
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        if(_results_ == '' or not _results_):
            return True

        _n_modules_ = len(_results_)

        _model_ = self.tvwRiskMap.get_model()
        _model_.clear()
        for i in range(_n_modules_):
            _data_ = [_results_[i][0]]
            self._risk_['Name'] = [_results_[i][0]]
            self._risk_['A'] = _results_[i][1]
            self._risk_['D'] = _results_[i][2]
            self._risk_['SA'] = _results_[i][3]
            self._risk_['SQ'] = _results_[i][4]
            self._risk_['SX'] = _results_[i][5]
            self._risk_['Risk'] = _results_[i][1] * _results_[i][2] * \
                                  _results_[i][3] * _results_[i][4] * \
                                  _results_[i][5]

            if(_results_[i][6] == '-'):     # It's the top level element.
                _piter_ = None
            elif(_results_[i][6] != '-'):   # It's a child element.
                _piter_ = _model_.get_iter_from_string(_results_[i][6])

            _color_ = self._risk_color()
            _data_.append(_color_['A'])
            _data_.append(_color_['D'])
            _data_.append(_color_['SA'])
            _data_.append(_color_['SQ'])
            _data_.append(_color_['SX'])
            _data_.append(_color_['Risk'])

            _model_.append(_piter_, _data_)

        return False

    def _risk_map_update(self, _model_, _row_):
        """
        Method to update the SOFTWARE Risk Map when the risk is re-calculated.
        """

        _module_ = _model_.get_value(_row_, 0)
        while _module_ != self._risk_['Name']:
            if(_model_.iter_has_child(_row_)):
                _row_ = _model_.iter_children(_row_)
                self._risk_map_update(_model_, _row_)
            else:
                _row_ = _model_.iter_next(_row_)

            _module_ = _model_.get_value(_row_, 0)

        _color_ = self._risk_color()

        _model_.set_value(_row_, 1, _color_['A'])
        _model_.set_value(_row_, 2, _color_['D'])
        _model_.set_value(_row_, 3, _color_['SA'])
        _model_.set_value(_row_, 4, _color_['SQ'])
        _model_.set_value(_row_, 5, _color_['SX'])
        _model_.set_value(_row_, 6, _color_['Risk'])

        return False

    def _risk_color(self):
        """
        Method to find the hexadecimal code for the risk level colors.
        """

        _color_ = {}

        # Find the Application risk level.
        if(self._risk_['A'] == 1):
            _color_['A'] = '#90EE90'        # Green
        elif(self._risk_['A'] == 2):
            _color_['A'] = '#FFFF79'        # Yellow
        else:
            _color_['A'] = '#FFC0CB'        # Red

        # Find the Development risk level.
        if(self._risk_['D'] == 0.5):
            _color_['D'] = '#90EE90'        # Green
        elif(self._risk_['D'] == 1.0):
            _color_['D'] = '#FFFF79'        # Yellow
        else:
            _color_['D'] = '#FFC0CB'        # Red

        # Find the Anomaly Management risk level.
        if(self._risk_['SA'] == 0.9):
            _color_['SA'] = '#90EE90'       # Green
        elif(self._risk_['SA'] == 1.1):
            _color_['SA'] = '#FFC0CB'       # Red
        else:
            _color_['SA'] = '#FFFF79'       # Yellow

        # Find the Software Quality risk level.
        if(self._risk_['SQ'] == 1.1):
            _color_['SQ'] = '#FFC0CB'       # Red
        else:
            _color_['SQ'] = '#90EE90'       # Green

        # Find the Complexity risk level.
        if(self._risk_['SX'] > 1.1):
            _color_['SX'] = '#FFC0CB'       # Red
        elif(self._risk_['SX'] < 0.5):
            _color_['SX'] = '#90EE90'       # Green
        else:
            _color_['SX'] = '#FFFF79'       # Yellow

        # Find the overall risk level.
        if(self._risk_['Risk'] >= 3.5):
            _color_['Risk'] = '#FFC0CB'     # Red
        elif(self._risk_['Risk'] <= 1.5):
            _color_['Risk'] = '#90EE90'     # Green
        else:
            _color_['Risk'] = '#FFFF79'     # Yellow

        return(_color_)

    def _risk_analysis_tab_show(self):
        """
        Method to insert and remove pages from the Risk Analysis gtk.Notebook()
        depending on the application level and development phase.  This allows
        the user to only answer the pertinent risk analysis questions.
        """

        self.nbkRiskAnalysis.remove_page(4)
        self.nbkRiskAnalysis.remove_page(3)
        self.nbkRiskAnalysis.remove_page(2)
        self.nbkRiskAnalysis.remove_page(1)

        if((self._dev_phase == 1 or
            self._dev_phase == 2) and
            self._app_level == 2):          # SSR/SRR on CSCI
            self.nbkRiskAnalysis.insert_page(self.hpnSRR,
                                             tab_label=self.lblSRR,
                                             position=-1)
        elif(self._dev_phase == 3 and
             self._app_level == 2):         # PDR on CSCI
            self.nbkRiskAnalysis.insert_page(self.hpnSRR,
                                             tab_label=self.lblSRR,
                                             position=-1)
            self.nbkRiskAnalysis.insert_page(self.hpnPDR,
                                             tab_label=self.lblPDR,
                                             position=-1)
        elif(self._dev_phase == 4):         # CDR
            if(self.hpnCDR.get_child1() is not None):
                self.hpnCDR.remove(self.hpnCDR.get_child1())
            if(self.hpnCDR.get_child2() is not None):
                self.hpnCDR.remove(self.hpnCDR.get_child2())

            if(self._app_level == 2):       # CSCI
                self.nbkRiskAnalysis.insert_page(self.hpnSRR,
                                                 tab_label=self.lblSRR,
                                                 position=-1)
                self.nbkRiskAnalysis.insert_page(self.hpnPDR,
                                                 tab_label=self.lblPDR,
                                                 position=-1)
                self.hpnCDR.pack1(self.fraCSCICDRAM, resize=False)
                self.hpnCDR.pack2(self.fraCSCICDRSQ, resize=False)
            elif(self._app_level == 3):     # Unit
                self.hpnCDR.pack1(self.fraUnitCDRSQ, resize=False)

            self.hpnCDR.show_all()
            self.nbkRiskAnalysis.insert_page(self.hpnCDR,
                                             tab_label=self.lblCDR,
                                             position=-1)

        elif(self._dev_phase == 5):         # TRR
            if(self.hpnTRR.get_child1() is not None):
                self.hpnTRR.remove(self.hpnTRR.get_child1())
            if(self.hpnTRR.get_child2() is not None):
                self.hpnTRR.remove(self.hpnTRR.get_child2())

            if(self._app_level == 2):       # CSCI
                self.nbkRiskAnalysis.insert_page(self.hpnSRR,
                                                 tab_label=self.lblSRR,
                                                 position=-1)
                self.nbkRiskAnalysis.insert_page(self.hpnPDR,
                                                 tab_label=self.lblPDR,
                                                 position=-1)
                self.hpnTRR.pack1(self.fraCSCITRRSX, resize=False)
            elif(self._app_level == 3):       # Unit
                self.hpnTRR.pack1(self.fraUnitTRRAM, resize=False)
                self.hpnTRR.pack2(self.fraUnitTRRSQ, resize=False)

            self.nbkRiskAnalysis.insert_page(self.hpnCDR,
                                             tab_label=self.lblCDR,
                                             position=-1)
            self.nbkRiskAnalysis.insert_page(self.hpnTRR,
                                             tab_label=self.lblTRR,
                                             position=-1)
            self.hpnTRR.show_all()

        return False

    def _test_selection_tab_create(self):
        """
        Method to create the Test Technique selection gtk.Notebook tab and add
        it to the gtk.Notebook at the proper location.
        """

        def _test_selection_widgets_create(self):
            """
            Method to create the test planning tab widgets for the SOFTWARE Object.
            """

    # Software test technique selection widgets.  These widgets are used to
    # display test technique information about the selected software module.
            self.cmbTCL.connect('changed',
                                self._callback_combo, 37)
            self.cmbTCL.set_tooltip_text(_("Select the desired software test confidence level."))
            _list = [["Low"], ["Medium"], ["High"], ["Very High"]]
            _widg.load_combo(self.cmbTCL, _list, True)

            self.cmbTestPath.connect('changed',
                                     self._callback_combo, 38)
            self.cmbTestPath.set_tooltip_text(_("Select the path for determining software testing techniques."))
            _list = [[_("Choose techniques based on software category")],
                     [_("Choose techniques based on types of software errors")]]
            _widg.load_combo(self.cmbTestPath, _list, True)

            self.cmbTestEffort.connect('changed',
                                       self._callback_combo, 40)
            self.cmbTestEffort.set_tooltip_text(_("Select the software test effort alternative."))
            _list = [[_("Alternative 1, Labor Hours")],
                     [_("Alternative 2, Budget")],
                     [_("Alternative 3, Schedule")]]
            _widg.load_combo(self.cmbTestEffort, _list, True)

            self.cmbTestApproach.connect('changed',
                                         self._callback_combo, 41)
            self.cmbTestApproach.set_tooltip_text(_("Select the software test approach."))
            _list = [[_("Test Until Method is Exhausted")],
                     [_("Stopping Rules")]]
            _widg.load_combo(self.cmbTestApproach, _list, True)

            self.txtLaborTest.set_tooltip_text(_("Total number of labor hours for software testing."))
            self.txtLaborTest.connect('focus-out-event',
                                      self._callback_entry, 'float', 42)

            self.txtLaborDev.set_tooltip_text(_("Total number of labor hours entire software development effort."))
            self.txtLaborDev.connect('focus-out-event',
                                     self._callback_entry, 'float', 43)

            self.txtBudgetTest.set_tooltip_text(_("Total budget for software testing."))
            self.txtBudgetTest.connect('focus-out-event',
                                       self._callback_entry, 'float', 44)

            self.txtBudgetDev.set_tooltip_text(_("Total budget for entire software development effort."))
            self.txtBudgetDev.connect('focus-out-event',
                                      self._callback_entry, 'float', 45)

            self.txtScheduleTest.set_tooltip_text(_("Working days scheduled for software testing."))
            self.txtScheduleTest.connect('focus-out-event',
                                         self._callback_entry, 'float', 46)

            self.txtScheduleDev.set_tooltip_text(_("Working days scheduled for entire development effort."))
            self.txtScheduleDev.connect('focus-out-event',
                                        self._callback_entry, 'float', 47)

            self.txtBranches.set_tooltip_text(_("The total number of execution branches in the selected unit."))
            self.txtBranches.connect('focus-out-event',
                                     self._callback_entry, 'int', 48)

            self.txtBranchesTest.set_tooltip_text(_("The total number of execution branches actually tested in the selected unit."))
            self.txtBranchesTest.connect('focus-out-event',
                                         self._callback_entry, 'int', 49)

            self.txtInputs.set_tooltip_text(_("The total number of inputs to the selected unit."))
            self.txtInputs.connect('focus-out-event',
                                   self._callback_entry, 'int', 50)

            self.txtInputsTest.set_tooltip_text(_("The total number of inputs to the selected unit actually tested."))
            self.txtInputsTest.connect('focus-out-event',
                                       self._callback_entry, 'int', 51)

            self.txtUnits.set_tooltip_text(_("The total number of units in the selected CSCI."))

            self.txtUnitsTest.set_tooltip_text(_("The total number of units in the selected CSCI actually tested."))
            self.txtUnitsTest.connect('focus-out-event',
                                      self._callback_entry, 'int', 52)

            self.txtInterfaces.set_tooltip_text(_("The total number of interfaces to the selected CSCI."))
            self.txtInterfaces.connect('focus-out-event',
                                       self._callback_entry, 'int', 53)

            self.txtInterfacesTest.set_tooltip_text(_("The total number of interfaces in the selected CSCI actually tested."))
            self.txtInterfacesTest.connect('focus-out-event',
                                           self._callback_entry, 'int', 54)

            # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
    # Create and load the Test Matrix for CSCI-level testing.
            _model_ = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_INT,
                                    gobject.TYPE_INT, gobject.TYPE_INT,
                                    gobject.TYPE_INT, gobject.TYPE_INT,
                                    gobject.TYPE_STRING, gobject.TYPE_STRING,
                                    gobject.TYPE_STRING, gobject.TYPE_STRING,
                                    gobject.TYPE_STRING, gobject.TYPE_STRING,
                                    gobject.TYPE_INT, gobject.TYPE_INT,
                                    gobject.TYPE_STRING)
            self.tvwCSCITestSelectionMatrix.set_model(_model_)
            self.tvwCSCITestSelectionMatrix.set_tooltip_text(_("Software test technique selection matrix."))
            self.tvwCSCITestSelectionMatrix.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

            _test_rankings_ = [[1, 0, 0, 0, 0, 0, '12', '1', '4', '1', '-', '-', 0, 0, ''],
                               [0, 1, 0, 0, 0, 0, '18', '2', '6', '5', '-', '-', 0, 0, ''],
                               [0, 0, 1, 0, 0, 0, '16', '3', '2', '2', '-', '-', 0, 0, ''],
                               [0, 0, 0, 1, 0, 0, '32', '4', '3', '4', '2', '1', 0, 0, ''],
                               [0, 0, 0, 0, 1, 0, '58', '5', '1', '3', '1', '2', 0, 0, ''],
                               [0, 0, 0, 0, 0, 1, '44', '5', '5', '6', '3', '3', 0, 0, ''],
                               [1, 0, 1, 0, 0, 0, '-', '2', '7', '1', '-', '-', 0, 0, ''],
                               [0, 1, 1, 0, 0, 0, '-', '2', '7', '1', '-', '-', 0, 0, ''],
                               [1, 1, 0, 0, 0, 0, '-', '1', '1', '3', '-', '-', 0, 0, ''],
                               [0, 0, 1, 1, 0, 0, '-', '4', '6', '4', '7', '1', 0, 0, ''],
                               [0, 1, 0, 0, 1, 0, '-', '10', '14', '5', '3', '3', 0, 0, ''],
                               [1, 0, 0, 0, 1, 0, '-', '10', '14', '5', '3', '3', 0, 0, ''],
                               [0, 0, 1, 0, 0, 1, '-', '5', '3', '7', '10', '2', 0, 0, ''],
                               [1, 0, 0, 1, 0, 0, '-', '6', '10', '8', '7', '5', 0, 0, ''],
                               [0, 1, 0, 1, 0, 0, '-', '6', '9', '9', '7', '5', 0, 0, ''],
                               [0, 1, 1, 0, 1, 0, '-', '12', '12', '10', '3', '9', 0, 0, ''],
                               [0, 0, 0, 1, 1, 0, '-', '13', '12', '11', '1', '10', 0, 0, ''],
                               [1, 0, 0, 0, 0, 1, '-', '8', '3', '12', '10', '7', 0, 0, ''],
                               [0, 1, 0, 0, 0, 1, '-', '8', '3', '12', '10', '7', 0, 0, ''],
                               [0, 0, 0, 0, 1, 1, '-', '15', '11', '14', '1', '11', 0, 0, ''],
                               [0, 0, 0, 1, 0, 1, '-', '13', '2', '15', '6', '12', 0, 0, '']]

            _headings_ = [_(u"Error/Anomaly\nDetection"),
                          _(u"Structure\nAnalysis &amp;\nDocumentation"),
                          _(u"Code\nReviews"), _(u"Functional\nTesting"),
                          _(u"Branch\nTesting"), _(u"Random\nTesting"),
                          _(u"Stopping\nRule (Hours)"), _(u"Average\nEffort"),
                          _(u"Average %\nErrors Found"),
                          _(u"Detection\nEfficiency"), _(u"% Average\nCoverage"),
                          _(u"Coverage\nEfficiency")]

            for i in range(len(_headings_[:6])):
                cell = gtk.CellRendererToggle()
                cell.set_property('activatable', 0)
                cell.set_property('xalign', 0.5)
                cell.set_property('yalign', 0.5)
                label = gtk.Label()
                label.set_alignment(xalign=0.5, yalign=0.5)
                label.set_justify(gtk.JUSTIFY_CENTER)
                label.set_property('angle', 90)
                label.set_markup("<span weight='bold'>" + _headings_[i] + "</span>")
                label.set_use_markup(True)
                label.show_all()
                column = gtk.TreeViewColumn()
                column.pack_start(cell, True)
                column.set_attributes(cell, active=i)
                column.set_clickable(True)
                column.set_reorderable(True)
                column.set_max_width(75)
                column.set_sort_column_id(i)
                column.set_widget(label)
                self.tvwCSCITestSelectionMatrix.append_column(column)

            for i in range(len(_headings_[6:])):
                cell = gtk.CellRendererText()
                cell.set_property('editable', 0)
                cell.set_property('xalign', 0.5)
                cell.set_property('yalign', 0.5)
                label = gtk.Label()
                label.set_alignment(xalign=0.5, yalign=0.5)
                label.set_justify(gtk.JUSTIFY_CENTER)
                label.set_property('angle', 90)
                label.set_markup("<span weight='bold'>" + _headings_[i+6] + "</span>")
                label.set_use_markup(True)
                label.show_all()
                column = gtk.TreeViewColumn()
                column.pack_start(cell, True)
                column.set_attributes(cell, text=i+6)
                column.set_clickable(True)
                column.set_reorderable(True)
                column.set_max_width(75)
                column.set_sort_column_id(i+6)
                column.set_widget(label)
                self.tvwCSCITestSelectionMatrix.append_column(column)

            cell = gtk.CellRendererToggle()
            cell.set_property('activatable', 1)
            cell.set_property('xalign', 0.5)
            cell.set_property('yalign', 0.5)
            _header_ = _(u"Recommended")
            label = gtk.Label()
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.set_property('angle', 90)
            label.set_markup("<span weight='bold'>" + _header_ + "</span>")
            label.set_use_markup(True)
            label.show_all()
            column = gtk.TreeViewColumn()
            column.pack_start(cell, True)
            column.set_attributes(cell, active=12)
            column.set_clickable(True)
            column.set_max_width(75)
            column.set_sort_column_id(12)
            column.set_widget(label)
            self.tvwCSCITestSelectionMatrix.append_column(column)
            cell.connect('toggled', _test_selection_tree_edit, 12, _model_)

            cell = gtk.CellRendererToggle()
            cell.set_property('activatable', 1)
            cell.set_property('xalign', 0.5)
            cell.set_property('yalign', 0.5)
            _header_ = _(u"Selected")
            label = gtk.Label()
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.set_property('angle', 90)
            label.set_markup("<span weight='bold'>" + _header_ + "</span>")
            label.set_use_markup(True)
            label.show_all()
            column = gtk.TreeViewColumn()
            column.pack_start(cell, True)
            column.set_attributes(cell, active=13)
            column.set_clickable(True)
            column.set_max_width(75)
            column.set_sort_column_id(13)
            column.set_widget(label)
            self.tvwCSCITestSelectionMatrix.append_column(column)
            cell.connect('toggled', _test_selection_tree_edit, 13, _model_)

            for i in range(len(_test_rankings_)):
                _model_.append(_test_rankings_[i])

    # Create and load the Test Matrix for unit-level testing.
            _model_ = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_INT,
                                    gobject.TYPE_INT, gobject.TYPE_INT,
                                    gobject.TYPE_INT, gobject.TYPE_INT,
                                    gobject.TYPE_STRING, gobject.TYPE_STRING,
                                    gobject.TYPE_STRING, gobject.TYPE_STRING,
                                    gobject.TYPE_STRING, gobject.TYPE_STRING,
                                    gobject.TYPE_STRING, gobject.TYPE_STRING,
                                    gobject.TYPE_STRING, gobject.TYPE_STRING,
                                    gobject.TYPE_STRING, gobject.TYPE_STRING,
                                    gobject.TYPE_STRING, gobject.TYPE_STRING,
                                    gobject.TYPE_STRING, gobject.TYPE_STRING,
                                    gobject.TYPE_INT, gobject.TYPE_INT,
                                    gobject.TYPE_STRING)
            self.tvwUnitTestSelectionMatrix.set_model(_model_)
            self.tvwUnitTestSelectionMatrix.set_tooltip_text(_("Software test technique selection matrix."))
            self.tvwUnitTestSelectionMatrix.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

            _test_rankings_ = [[1, 0, 0, 0, 0, 0, '6', '2', '2', '1', '-', '-', 'L', 'M', '', '', '', '', 'H', '', '', '', 0, 0, ''],
                               [0, 1, 0, 0, 0, 0, '4', '1', '6', '2', '-', '-', '', 'L', '', '', '', '', '', '', '', '', 0, 0, ''],
                               [0, 0, 1, 0, 0, 0, '8', '4', '1', '3', '-', '-', 'L', 'H', '', 'L', 'H', '', 'L', 'M', '', 'L', 0, 0, ''],
                               [0, 0, 0, 1, 0, 0, '16', '3', '4', '4', '2', '1', 'L', 'L', '', 'L', 'H', '', '', 'H', '', 'L', 0, 0, ''],
                               [0, 0, 0, 0, 1, 0, '29', '6', '3', '5', '1', '3', 'L', 'M', '', '', 'H', 'L', '', 'H', '', 'L', 0, 0, ''],
                               [0, 0, 0, 0, 0, 1, '22', '5', '5', '6', '2', '2', 'L', '', 'L', '', 'M', 'L', '', 'M', '', 'L', 0, 0, ''],
                               [1, 1, 0, 0, 0, 0, '-', '1', '9', '1', '-', '-', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],
                               [1, 0, 1, 0, 0, 0, '-', '3', '1', '2', '-', '-', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],
                               [0, 1, 1, 0, 0, 0, '-', '2', '7', '3', '-', '-', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],
                               [1, 0, 0, 1, 0, 0, '-', '10', '2', '4', '7', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],
                               [0, 0, 1, 0, 0, 1, '-', '9', '4', '5', '7', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],
                               [1, 0, 0, 0, 0, 1, '-', '5', '5', '6', '7', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],
                               [1, 0, 0, 0, 1, 0, '-', '12', '3', '7', '3', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],
                               [0, 0, 1, 1, 0, 0, '-', '6', '6', '8', '7', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],
                               [0, 0, 0, 1, 0, 1, '-', '7', '10', '8', '6', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],
                               [0, 1, 0, 1, 0, 0, '-', '8', '12', '10', '7', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],
                               [0, 0, 0, 0, 1, 1, '-', '13', '11', '11', '1', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],
                               [0, 1, 0, 0, 1, 0, '-', '11', '14', '12', '3', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],
                               [0, 1, 0, 0, 0, 1, '-', '4', '15', '13', '7', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],
                               [0, 0, 1, 0, 1, 0, '-', '15', '8', '14', '37', '11', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],
                               [0, 0, 0, 1, 1, 0, '-', '14', '13', '15', '1', '11', '', '', '', '', '', '', '', '', '', '', 0, 0, '']]

            _headings_ = [_(u"Error/Anomaly\nDetection"),
                          _(u"Structure\nAnalysis &amp;\nDocumentation"),
                          _(u"Code\nReviews"), _(u"Functional\nTesting"),
                          _(u"Branch\nTesting"), _(u"Random\nTesting"),
                          _(u"Stopping\nRule (Hours)"), _(u"Average\nEffort"),
                          _(u"Average %\nErrors Found"),
                          _(u"Detection\nEfficiency"), _(u"% Average\nCoverage"),
                          _(u"Coverage\nEfficiency"), _(u"Computational\nErrors"),
                          _(u"Logic\nErrors"), _(u"Data\nInput\nErrors"),
                          _(u"Data\nVerification\nErrors"),
                          _(u"Data\nHandling\nErrors"), _(u"Data\nOutput\nErrors"),
                          _(u"Data\nDefinition\nErrors"), _(u"Interface\nErrors"),
                          _(u"Database\nErrors"), _(u"Other\nErrors")]

            for i in range(len(_headings_[:6])):
                cell = gtk.CellRendererToggle()
                cell.set_property('activatable', 0)
                label = gtk.Label()
                label.set_alignment(xalign=0.5, yalign=0.5)
                label.set_justify(gtk.JUSTIFY_CENTER)
                label.set_property('angle', 90)
                label.set_markup("<span weight='bold'>" + _headings_[i] + "</span>")
                label.set_use_markup(True)
                label.show_all()
                column = gtk.TreeViewColumn()
                column.pack_start(cell, True)
                column.set_attributes(cell, active=i)
                column.set_clickable(True)
                column.set_reorderable(True)
                column.set_max_width(75)
                column.set_sort_column_id(i)
                column.set_widget(label)
                self.tvwUnitTestSelectionMatrix.append_column(column)

            for i in range(len(_headings_[6:])):
                cell = gtk.CellRendererText()
                cell.set_property('editable', 0)
                label = gtk.Label()
                label.set_alignment(xalign=0.5, yalign=0.5)
                label.set_justify(gtk.JUSTIFY_CENTER)
                label.set_property('angle', 90)
                label.set_markup("<span weight='bold'>" + _headings_[i+6] + "</span>")
                label.set_use_markup(True)
                label.show_all()
                column = gtk.TreeViewColumn()
                column.pack_start(cell, True)
                column.set_attributes(cell, text=i+6)
                column.set_clickable(True)
                column.set_reorderable(True)
                column.set_max_width(75)
                column.set_sort_column_id(i+6)
                column.set_widget(label)
                self.tvwUnitTestSelectionMatrix.append_column(column)

            cell = gtk.CellRendererToggle()
            cell.set_property('activatable', 1)
            _header_ = _(u"Recommended")
            label = gtk.Label()
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.set_property('angle', 90)
            label.set_markup("<span weight='bold'>" + _header_ + "</span>")
            label.set_use_markup(True)
            label.show_all()
            column = gtk.TreeViewColumn()
            column.pack_start(cell, True)
            column.set_attributes(cell, active=22)
            column.set_clickable(True)
            column.set_max_width(75)
            column.set_sort_column_id(22)
            column.set_widget(label)
            self.tvwUnitTestSelectionMatrix.append_column(column)
            cell.connect('toggled', _test_selection_tree_edit, 22, _model_)

            cell = gtk.CellRendererToggle()
            cell.set_property('activatable', 1)
            _header_ = _(u"Selected")
            label = gtk.Label()
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.set_property('angle', 90)
            label.set_markup("<span weight='bold'>" + _header_ + "</span>")
            label.set_use_markup(True)
            label.show_all()
            column = gtk.TreeViewColumn()
            column.pack_start(cell, True)
            column.set_attributes(cell, active=23)
            column.set_clickable(True)
            column.set_max_width(75)
            column.set_sort_column_id(23)
            column.set_widget(label)
            self.tvwUnitTestSelectionMatrix.append_column(column)
            cell.connect('toggled', _test_selection_tree_edit, 23, _model_)

            for i in range(len(_test_rankings_)):
                _model_.append(_test_rankings_[i])

            return False

        if _test_selection_widgets_create(self):
            self._app.debug_log.error("software.py: Failed to create Test Technique Selection tab widgets.")

        hpaned = gtk.HPaned()

# Add the user input widgets to the left half.
        vpaned = gtk.VPaned()
        hpaned.pack1(vpaned, resize=False)

        # Create and place the labels.
        fixed = gtk.Fixed()
        y_pos = 5
        _max1_ = 0
        _max2_ = 0
        (_max1_, _heights_) = _widg.make_labels(self._ts_tab_labels[0:4],
                                                fixed, 5, y_pos, y_inc=35)
        _x_pos_ = max(_max1_, _max2_) + 25

        # Add the test planning widgets to the left half.
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Test Planning"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)
        frame.show_all()

        vpaned.pack1(frame, resize=False)

        y_pos = 5
        fixed.put(self.cmbTCL, _x_pos_, y_pos)
        y_pos += 35
        fixed.put(self.cmbTestPath, _x_pos_, y_pos)
        y_pos += 35
        fixed.put(self.cmbTestEffort, _x_pos_, y_pos)
        y_pos += 35
        fixed.put(self.cmbTestApproach, _x_pos_, y_pos)

        # Add the test effort widgets to the lower left half.
        hboxl = gtk.HBox()
        vpaned.pack2(hboxl, resize=False)

        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Test Effort"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)
        frame.show_all()

        hboxl.pack_start(frame)

        # Create and place the labels.
        _max1_ = 0
        _max2_ = 0
        (_max1_, _heights_) = _widg.make_labels(self._ts_tab_labels[4:10],
                                                fixed, 5, 5)
        _x_pos_ = max(_max1_, _max2_) + 25

        y_pos = 5
        fixed.put(self.txtLaborTest, _x_pos_, y_pos)
        y_pos += 30
        fixed.put(self.txtLaborDev, _x_pos_, y_pos)
        y_pos += 30
        fixed.put(self.txtBudgetTest, _x_pos_, y_pos)
        y_pos += 30
        fixed.put(self.txtBudgetDev, _x_pos_, y_pos)
        y_pos += 30
        fixed.put(self.txtScheduleTest, _x_pos_, y_pos)
        y_pos += 30
        fixed.put(self.txtScheduleDev, _x_pos_, y_pos)

        # Add the test coverage widgets to the lower right half.
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Test Coverage"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)
        frame.show_all()

        hboxl.pack_end(frame)

        # Create and place the labels.
        y_pos = 5
        _max1_ = 0
        _max2_ = 0
        (_max1_, _heights_) = _widg.make_labels(self._ts_tab_labels[10:18],
                                                fixed, 5, y_pos)
        _x_pos_ = max(_max1_, _max2_) + 25

        y_pos = 5
        fixed.put(self.txtBranches, _x_pos_, y_pos)
        y_pos += 30
        fixed.put(self.txtBranchesTest, _x_pos_, y_pos)
        y_pos += 30
        fixed.put(self.txtInputs, _x_pos_, y_pos)
        y_pos += 30
        fixed.put(self.txtInputsTest, _x_pos_, y_pos)
        y_pos += 30
        fixed.put(self.txtUnits, _x_pos_, y_pos)
        y_pos += 30
        fixed.put(self.txtUnitsTest, _x_pos_, y_pos)
        y_pos += 30
        fixed.put(self.txtInterfaces, _x_pos_, y_pos)
        y_pos += 30
        fixed.put(self.txtInterfacesTest, _x_pos_, y_pos)

        fixed.show_all()

# Add the test selection matrix gtk.Treeview to the right half.
        self.scwTestSelectionMatrix.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        frame = _widg.make_frame(_label_=_(u"Test Technique Selection"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(self.scwTestSelectionMatrix)
        frame.show_all()

        hpaned.pack2(frame, resize=False)

# Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("Test\nPlanning") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Assists in planning of software test program."))
        self.notebook.insert_page(hpaned,
                                  tab_label=label,
                                  position=-1)

        return False

    def _test_selection_tab_load(self):
        """
        Loads the test technique selection information for the selected
        software module.
        """

# Set the values of all the gtk.Combo() and gtk.Entry() widgets.
        self.cmbTCL.set_active(self.model.get_value(self._selected_row, 37))
        self.cmbTestPath.set_active(self.model.get_value(self._selected_row, 38))
        self.cmbTestEffort.set_active(self.model.get_value(self._selected_row, 40))
        self.cmbTestApproach.set_active(self.model.get_value(self._selected_row, 41))
        self.txtLaborTest.set_text(str(self.model.get_value(self._selected_row, 42)))
        self.txtLaborDev.set_text(str(self.model.get_value(self._selected_row, 43)))
        self.txtBudgetTest.set_text(str(self.model.get_value(self._selected_row, 44)))
        self.txtBudgetDev.set_text(str(self.model.get_value(self._selected_row, 45)))
        self.txtScheduleTest.set_text(str(self.model.get_value(self._selected_row, 46)))
        self.txtScheduleDev.set_text(str(self.model.get_value(self._selected_row, 47)))
        self.txtBranches.set_text(str(self.model.get_value(self._selected_row, 48)))
        self.txtBranchesTest.set_text(str(self.model.get_value(self._selected_row, 49)))
        self.txtInputs.set_text(str(self.model.get_value(self._selected_row, 50)))
        self.txtInputsTest.set_text(str(self.model.get_value(self._selected_row, 51)))
        self.txtUnits.set_text(str(self.model.get_value(self._selected_row, 24)))
        self.txtUnitsTest.set_text(str(self.model.get_value(self._selected_row, 52)))
        self.txtInterfaces.set_text(str(self.model.get_value(self._selected_row, 53)))
        self.txtInterfacesTest.set_text(str(self.model.get_value(self._selected_row, 54)))

# Set the correct test coverage gtk.Entry widgets editable depending on the
# application level of the selected software.
        _level_id = self.model.get_value(self._selected_row, 2)
        if(_level_id == 2):                 # CSCI
            self.txtBranches.props.editable = False
            self.txtBranches.set_sensitive(False)
            self.txtBranchesTest.props.editable = False
            self.txtBranchesTest.set_sensitive(False)
            self.txtInputs.props.editable = False
            self.txtInputs.set_sensitive(False)
            self.txtInputsTest.props.editable = False
            self.txtInputsTest.set_sensitive(False)
            self.txtUnits.props.editable = True
            self.txtUnits.set_sensitive(True)
            self.txtUnitsTest.props.editable = True
            self.txtUnitsTest.set_sensitive(True)
            self.txtInterfaces.props.editable = True
            self.txtInterfaces.set_sensitive(True)
            self.txtInterfacesTest.props.editable = True
            self.txtInterfacesTest.set_sensitive(True)
        elif(_level_id == 3):               # Unit
            self.txtBranches.props.editable = True
            self.txtBranches.set_sensitive(True)
            self.txtBranchesTest.props.editable = True
            self.txtBranchesTest.set_sensitive(True)
            self.txtInputs.props.editable = True
            self.txtInputs.set_sensitive(True)
            self.txtInputsTest.props.editable = True
            self.txtInputsTest.set_sensitive(True)
            self.txtUnits.props.editable = False
            self.txtUnits.set_sensitive(False)
            self.txtUnitsTest.props.editable = False
            self.txtUnitsTest.set_sensitive(False)
            self.txtInterfaces.props.editable = False
            self.txtInterfaces.set_sensitive(False)
            self.txtInterfacesTest.props.editable = False
            self.txtInterfacesTest.set_sensitive(False)
        else:
            self.txtBranches.props.editable = False
            self.txtBranches.set_sensitive(False)
            self.txtBranchesTest.props.editable = False
            self.txtBranchesTest.set_sensitive(False)
            self.txtInputs.props.editable = False
            self.txtInputs.set_sensitive(False)
            self.txtInputsTest.props.editable = False
            self.txtInputsTest.set_sensitive(False)
            self.txtUnits.props.editable = False
            self.txtUnits.set_sensitive(False)
            self.txtUnitsTest.props.editable = False
            self.txtUnitsTest.set_sensitive(False)
            self.txtInterfaces.props.editable = False
            self.txtInterfaces.set_sensitive(False)
            self.txtInterfacesTest.props.editable = False
            self.txtInterfacesTest.set_sensitive(False)

# Update the correct Test Matrix.
        if(self.scwTestSelectionMatrix.get_child() is not None):
            self.scwTestSelectionMatrix.remove(self.scwTestSelectionMatrix.get_child())
        if(self._app_level == 2):           # CSCI
            self.scwTestSelectionMatrix.add(self.tvwCSCITestSelectionMatrix)
        elif(self._app_level == 3):         # Unit
            self.scwTestSelectionMatrix.add(self.tvwUnitTestSelectionMatrix)
        self.scwTestSelectionMatrix.show_all()

        return False

    def _reliability_estimation_tab_create(self):
        """
        Method to create the reliability estimation gtk.Notebook tab and add it
        to the gtk.Notebook at the correct location.
        """

        _labels_ = [_(u"Average FR During Test:"), _(u"Failure Rate at EOT:"),
                    _(u"Average REN:"), _(u"EOT REN:"),
                    _(u"Number of Exception Conditions:"),
                    _(u"Input Variability:"), _(u"Total Execution Time:"),
                    _(u"OS Overhead Time:"), _(u"Workload:"),
                    _(u"Operating Environment Factor:"),
                    _(u"Estimated Failure Rate:")]

        def _reliability_estimation_widgets_create(self):
            """
            Method for creating reliability estimation widgets for the SOFTWARE
            Object.
            """

            self.txtFT1.set_tooltip_text(_("Displays the average failure rate during test for the selected software module."))
            self.txtFT2.set_tooltip_text(_("Displays the failure rate at the end of test for the selected software module."))
            self.txtRENAVG.set_tooltip_text(_("Displays the average Reliability Estimation Number (REN) for the selected software module."))
            self.txtRENEOT.set_tooltip_text(_("Displays the end of test Reliability Estimation Number (REN) for the selected software module."))
            self.txtEC.set_tooltip_text(_("Displays the number of exception conditions for the selected software module."))
            self.txtEC.connect('focus-out-event',
                               self._callback_entry, 'float', 63)
            self.txtEV.set_tooltip_text(_("Displays the variability of input for the selected software module."))
            self.txtET.set_tooltip_text(_("Displays the total execution time for the selected software module."))
            self.txtET.connect('focus-out-event',
                               self._callback_entry, 'float', 65)
            self.txtOS.set_tooltip_text(_("Displays the operating system overhead time for the selected software module."))
            self.txtOS.connect('focus-out-event',
                               self._callback_entry, 'float', 66)
            self.txtEW.set_tooltip_text(_("Displays the workload for the selected software module."))
            self.txtE.set_tooltip_text(_("Displays the operating environment factor for the selected software module."))
            self.txtF.set_tooltip_text(_("Displays the estimated failure rate for the selected software module."))

            return False

        if _reliability_estimation_widgets_create(self):
            self._app.debug_log.error("software.py: Failed to create Reliability Estimation tab widgets.")

        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_(u"Reliability Estimation Results"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)
        frame.show_all()

        y_pos = 5
        label = _widg.make_label(_labels_[0])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtFT1, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(_labels_[1])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtFT2, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(_labels_[2])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtRENAVG, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(_labels_[3])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtRENEOT, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(_labels_[4])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtEC, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(_labels_[5])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtEV, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(_labels_[6])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtET, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(_labels_[7])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtOS, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(_labels_[8])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtEW, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(_labels_[9])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtE, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(_labels_[10])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtF, 200, y_pos)

        # Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _(u"Reliability\nEstimation") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Displays software reliability estimation results."))
        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _reliability_estimation_tab_load(self):
        """
        Loads the gtk.Entry widgets with software reliability aestimation
        results information for the SOFTWARE Object.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        if(self._selected_row is not None):
            self.txtFT1.set_text(str(fmt.format(self.model.get_value(self._selected_row, 59))))
            self.txtFT2.set_text(str(fmt.format(self.model.get_value(self._selected_row, 60))))
            self.txtRENAVG.set_text(str(fmt.format(self.model.get_value(self._selected_row, 61))))
            self.txtRENEOT.set_text(str(fmt.format(self.model.get_value(self._selected_row, 62))))
            self.txtEC.set_text(str(fmt.format(self.model.get_value(self._selected_row, 63))))
            self.txtEV.set_text(str(fmt.format(self.model.get_value(self._selected_row, 64))))
            self.txtET.set_text(str(fmt.format(self.model.get_value(self._selected_row, 65))))
            self.txtOS.set_text(str(fmt.format(self.model.get_value(self._selected_row, 66))))
            self.txtEW.set_text(str(fmt.format(self.model.get_value(self._selected_row, 67))))
            self.txtE.set_text(str(fmt.format(self.model.get_value(self._selected_row, 68))))
            self.txtF.set_text(str(fmt.format(self.model.get_value(self._selected_row, 69))))

        return False

    def calculate(self, widget):
        """
        Method to calculate metrics for the selected Software Object.

        Keyword Arguments:
        widget -- the widget that called this method.
        """

        row = self.model.get_iter_root()
        RPFOM = _calc.calculate_software(self.model, row, self._app)
        self.model.set_value(row, 33, RPFOM)

        return False

    def _calculate_risk(self):
        """
        Method to calculate the SOFTWARE risk levels.
        """

        _model_ = self.treeview.get_model()
        self._risk_['Name'] = _model_.get_value(self._selected_row, 3)

        _util.set_cursor(self._app, gtk.gdk.WATCH)

        def _calculate_app_risk(self):

            if(self.cmbApplication.get_active() == 1 or
               self.cmbApplication.get_active() == 6):
                _A_ = 3.0
            elif(self.cmbApplication.get_active() == 2 or
                 self.cmbApplication.get_active() == 5):
                _A_ = 2.0
            else:
                _A_ = 1.0

            _model_.set_value(self._selected_row, self._col_order[6], _A_)
            self._risk_['A'] = _A_

            return(_A_)

        def _calculate_development_risk(self):

            _A_ = _calculate_app_risk(self)

            _D_ = (sum(self._development_env_.values()) / 43.0)
            if(_D_ < 0.5):                  # High risk
                _D_ = 2.0
            elif(_D_ > 0.9):                # Low risk
                _D_ = 0.5
            else:
                _D_ = 1.0

            _model_.set_value(self._selected_row, self._col_order[10], _D_)
            self._risk_['D'] = _D_

            return(_A_ * _D_)

        def _calculate_srr_risk(self):

    # Calculate the Development Environment factor.
            _D_ = _calculate_development_risk(self)

    # Calculate the Anomaly Management factor.
            _ratios_ = [0, 0, 0]
            if(self._srr_[41] / self._srr_[40] == 1):
                _ratios_[0] = 1
            if(self._srr_[43] / self._srr_[42] == 1):
                _ratios_[1] = 1
            if(self._srr_[45] / self._srr_[44] == 1):
                _ratios_[2] = 1

            y = sum(self._srr_[i] for i in range(16)) + sum(_ratios_)
            _AM_ = (19 - y) / 19.0
            if(_AM_ < 0.4):                 # Low risk
                _SA_ = 0.9
            elif(_AM_ > 0.6):               # High risk
                _SA_ = 1.1
            else:
                _SA_ = 1.0

    # Calculate the Requirements Traceability factor.
            if(self._srr_[16] == 1):        # Low risk
                _ST_ = 1.0
            else:
                _ST_ = 1.1

    # Calculate the Software Quality factor.
            _ratios_ = [0, 0]
            if(self._srr_[47] / self._srr_[46] == 1):
                _ratios_[0] = 1
            if(self._srr_[49] / self._srr_[48] == 1):
                _ratios_[1] = 1
            y = sum(self._srr_[i] for i in range(17, 40)) + sum(_ratios_)
            _DR_ = y / 25.0
            if(_DR_ < 0.5):                 # High risk
                _SQ_ = 1.1
            else:
                _SQ_ = 1.0

            self.model.set_value(self._selected_row, self._col_order[12], _SA_)
            self.model.set_value(self._selected_row, self._col_order[13], _ST_)
            self.model.set_value(self._selected_row, self._col_order[15], _SQ_)
            self._risk_['SA'] = _SA_
            self._risk_['ST'] = _ST_
            self._risk_['SQ'] = _SQ_

            return(_D_ * _SA_ * _ST_ * _SQ_)

        def _calculate_pdr_risk(self):

    # Calculate the Development Environment factor.
            _D_ = _calculate_development_risk(self)

    # Calculate the Anomaly Management factor.
            y = sum(self._pdr_[i] for i in range(14))
            _AM_ = (14 - y) / 14.0
            if(_AM_ < 0.4):                 # Low risk
                _SA_ = 0.9
            elif(_AM_ > 0.6):               # High risk
                _SA_ = 1.1
            else:
                _SA_ = 1.0

    # Calculate the Requirements Traceability factor.
            if(self._pdr_[14] == 1):        # Low risk
                _ST_ = 1.0
            else:
                _ST_ = 1.1

    # Calculate the Software Quality factor.
            _ratios_ = [0, 0, 0, 0, 0]
            if(self._pdr_[30] / (self._pdr_[29] + self._pdr_[30]) <= 0.3):
                _ratios_[0] = 1
            if(self._pdr_[32] / self._pdr_[31] > 0.5):
                _ratios_[1] = 1
            if(self._pdr_[34] / self._pdr_[33] > 0.5):
                _ratios_[2] = 1
            if(self._pdr_[36] / self._pdr_[35] > 0.5):
                _ratios_[3] = 1
            if(self._pdr_[38] / self._pdr_[37] > 0.75):
                _ratios_[4] = 1

            y = sum(self._pdr_[i] for i in range(15, 29)) + sum(_ratios_)
            _DR_ = y / 25.0
            if(_DR_ < 0.5):                 # High risk
                _SQ_ = 1.1
            else:
                _SQ_ = 1.0

            self.model.set_value(self._selected_row, self._col_order[12], _SA_)
            self.model.set_value(self._selected_row, self._col_order[13], _ST_)
            self.model.set_value(self._selected_row, self._col_order[15], _SQ_)
            self._risk_['SA'] = _SA_
            self._risk_['ST'] = _ST_
            self._risk_['SQ'] = _SQ_

            return(_D_ * _SA_ * _ST_ * _SQ_)

        def _calculate_cdr_risk(self):

    # Calculate the Development Environment factor.
            _D_ = _calculate_development_risk(self)

            _SA_ = 1.0
            _ST_ = 1.1
            if(self._app_level == 2):       # CSCI
    # Calculate the Anomaly Management factor.
                y = sum(self._cdr_[i] for i in range(8))
                _AM_ = (8 - y) / 8.0

                if(_AM_ < 0.4):             # Low risk
                    _SA_ = 0.9
                elif(_AM_ > 0.6):           # High risk
                    _SA_ = 1.1

    # Calculate the Requirements Traceability factor.
                if(self._cdr_[8] == 1 and
                    self._cdr_[9] == 1):    # Low risk
                    _ST_ = 1.0

    # Calculate the Software Quality factor.
                _ratios_ = [0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0]
                if(self._cdr_[12] / self._cdr_[11] <= 0.3):
                    _ratios_[0] = 1
                if(self._cdr_[13] / self._cdr_[10] <= 0.3):
                    _ratios_[1] = 1
                if(self._cdr_[15] / self._cdr_[14] <= 0.3):
                    _ratios_[2] = 1
                if(self._cdr_[16] / self._cdr_[10] > 0.5):
                    _ratios_[3] = 1
                if(self._cdr_[18] / self._cdr_[17] > 0.5):
                    _ratios_[4] = 1
                if(self._cdr_[20] / self._cdr_[19] > 0.5):
                    _ratios_[5] = 1
                if(self._cdr_[22] / self._cdr_[21] > 0.5):
                    _ratios_[6] = 1
                if(self._cdr_[23] / self._cdr_[10] > 0.5):
                    _ratios_[7] = 1
                if(self._cdr_[24] / self._cdr_[10] > 0.5):
                    _ratios_[8] = 1
                if(self._cdr_[26] / self._cdr_[25] > 0.75):
                    _ratios_[9] = 1
                if(self._cdr_[27] / self._cdr_[10] > 0.5):
                    _ratios_[10] = 1
                if(self._cdr_[28] / self._cdr_[10] > 0.5):
                    _ratios_[11] = 1
                if(self._cdr_[29] / self._cdr_[10] > 0.5):
                    _ratios_[12] = 1
                if(self._cdr_[30] / self._cdr_[10] > 0.5):
                    _ratios_[13] = 1
                if(self._cdr_[31] / self._cdr_[10] > 0.5):
                    _ratios_[14] = 1
                if(self._cdr_[32] / self._cdr_[10] > 0.5):
                    _ratios_[15] = 1
                if(self._cdr_[33] / self._cdr_[10] > 0.5):
                    _ratios_[16] = 1
                if(self._cdr_[34] / self._cdr_[10] > 0.5):
                    _ratios_[17] = 1

            elif(self._app_level == 3):    # Unit
    # Calculate the Software Quality factor.
                _ratios_ = [0, 0, 0, 0, 0, 0, 0]
                if(self._cdr_[47] / self._cdr_[46] <= 0.3):
                    _ratios_[0] = 1
                if(self._cdr_[34] / self._cdr_[12] <= 0.3):
                    _ratios_[1] = 1
                if(self._cdr_[49] / self._cdr_[48] <= 0.3):
                    _ratios_[2] = 1
                if(self._cdr_[50] / self._cdr_[51] > 0.5):
                    _ratios_[3] = 1
                if(self._cdr_[53] / self._cdr_[52] > 0.5):
                    _ratios_[4] = 1
                if(self._cdr_[55] / self._cdr_[54] > 0.5):
                    _ratios_[5] = 1
                if(self._cdr_[57] / self._cdr_[56] > 0.75):
                    _ratios_[6] = 1

            y = sum(self._cdr_[i] for i in range(34, 36)) + sum(_ratios_)
            _DR_ = y / 18.0
            if(_DR_  < 0.5):                 # High risk
                _SQ_ = 1.1
            else:
                _SQ_ = 1.0

            self.model.set_value(self._selected_row, self._col_order[12], _SA_)
            self.model.set_value(self._selected_row, self._col_order[13], _ST_)
            self.model.set_value(self._selected_row, self._col_order[15], _SQ_)
            self._risk_['SA'] = _SA_
            self._risk_['ST'] = _ST_
            self._risk_['SQ'] = _SQ_

            return(_D_ * _SA_ * _ST_ * _SQ_)

        def _calculate_trr_risk(self):

            _CDR_ = _calculate_cdr_risk(self)
            _SA_ = 1.0
            _SQ_ = 1.0
            if(self._app_level == 2):      # CSCI
    # Calculate the Complexity factor.
                self._trr_[3] = self._trr_[1] - self._trr_[2]
                _SX_ = (self._trr_[3] / self._trr_[1]) + (1.4 * self._trr_[2] / self._trr_[1])

            elif(self._app_level == 3):    # Unit
    # Calculate the Anomaly Management factor.
                y = self._trr_[4] + self._trr_[5]
                if(y / 2.0 > 0.4):          # Low risk
                    _SA_ = 0.9
                elif(y / 2.0 < 0.6):        # High risk
                    _SA_ = 1.1

    # Caclulate the Software Quality factor.
                y = sum(self._trr_[i] for i in range(7, 21))
                _DR_ = y / 14.0
                if(_DR_  < 0.5):            # High risk
                    _SQ_ = 1.1

    # Calculate the Complexity factor.
                _HLOC_ = self._trr_[20] - self._trr_[21]
                _SX_ = self._trr_[22] + self._trr_[23] + 1

            self.model.set_value(self._selected_row, self._col_order[12], _SA_)
            self.model.set_value(self._selected_row, self._col_order[15], _SQ_)
            self.model.set_value(self._selected_row, self._col_order[25], _SX_)
            self._dicSoftware[self._col_order[1]][self._col_order[12]] = _SA_
            self._dicSoftware[self._col_order[1]][self._col_order[15]] = _SQ_
            self._dicSoftware[self._col_order[1]][self._col_order[25]] = _SX_
            self._risk_['SA'] = _SA_
            self._risk_['SQ'] = _SQ_
            self._risk_['SX'] = _SX_

            return(_CDR_ * _SX_ * _SA_ * _SQ_)

        if(self._dev_phase == 1):
            _risk_ = _calculate_development_risk(self)
        elif(self._dev_phase == 2):
            _risk_ = _calculate_srr_risk(self)
        elif(self._dev_phase == 3):
            _risk_ = _calculate_pdr_risk(self)
        elif(self._dev_phase == 4):
            _risk_ = _calculate_cdr_risk(self)
        elif(self._dev_phase == 5):
            _risk_ = _calculate_trr_risk(self)

        self._risk_['Risk'] = _risk_

        _model_ = self.tvwRiskMap.get_model()
        _row_ = _model_.get_iter_root()
        self._risk_map_update(_model_, _row_)

        _util.set_cursor(self._app, gtk.gdk.LEFT_PTR)

        return False

    def _calculate_risk_reduction(self):
        """
        Method to calculate the risk reduction due to testing.
        """

# Calculate the risk reduction due to the test effort.
        if(self.cmbTestEffort.get_active() == 1):   # Labor hours
            _a_ = float(self.txtLaborTest.get_text())
            _b_ = float(self.txtLaborDev.get_text())
        elif(self.cmbTestEffort.get_active() == 2): # Budget
            _a_ = float(self.txtBudgetTest.get_text())
            _b_ = float(self.txtBudgetDev.get_text())
        elif(self.cmbTestEffort.get_active() == 3): # Schedule
            _a_ = float(self.txtScheduleTest.get_text())
            _b_ = float(self.txtScheduleDev.get_text())

        _TE_ = 1.0
        if(_a_ / _b_ > 0.4):
            _TE_ = 0.9

# Calculate the risk reduction due to test methods used.
        _TU_ = 1.0
        _TT_ = 1.0
        _TM_ = 1.0
        if(_TU_ / _TT_ > 0.75):
            _TM_ = 0.9
        elif(_TU_ / _TT_ < 0.5):
            _TM_ = 1.1

# Calculate the risk reduction due to test coverage.
        _TP_ = int(self.txtBranches.get_text())
        _PT_ = int(self.txtBranchesTest.get_text())
        _TI_ = int(self.txtInputs.get_text())
        _IT_ = int(self.txtInputsTest.get_text())
        _NM_ = int(self.txtUnits.get_text())
        _MT_ = int(self.txtUnitsTest.get_text())
        _TC_ = int(self.txtInterfaces.get_text())
        _CT_ = int(self.txtInterfacesTest.get_text())

        if(self._app_level == 2):           # CSCI
            _VS_ = ((_MT_ / _NM_) +(_CT_ / _TC_)) / 2.0
        elif(self._app_level == 3):         # Unit
            _VS_ = ((_PT_ / _TP_) + (_IT_ / _TI_)) / 2.0
        _TC_ = 1.0 / _VS_

        self._risk_['TE'] = _TE_
        self._risk_['TM'] = _TM_
        self._risk_['TC'] = _TC_

        return(_TE_ * _TM_ * _TC_)

    def _module_add(self, widget, type_):
        """
        Adds a new Software module to the Program's database.

        Keyword Arguments:
        widget -- the widget that called this function.
        type_  -- the type of Software module to add;
                  0 = sibling,
                  1 = child.
        """

        if(type_ == 0):
            _iter = self.model.iter_parent(self._selected_row)
            _parent = self.model.get_string_from_iter(_iter)
            n_new_module = _util.add_items(title=_(u"RTK - Add Sibling Modules"),
                                           prompt=_(u"How many sibling modules to add?"))
        if(type_ == 1):
            _parent = self.model.get_string_from_iter(self._selected_row)
            n_new_module = _util.add_items(title = _(u"RTK - Child Modules"),
                                           prompt=_(u"How many child modules to add?"))

        _util.set_cursor(self._app, gtk.gdk.WATCH)

        for i in range(n_new_module):
# Create the default description of the assembly.
            _descrip = str(_conf.RTK_PREFIX[16]) + ' ' + \
                       str(_conf.RTK_PREFIX[17])

# Increment the assembly index.
            _conf.RTK_PREFIX[17] = _conf.RTK_PREFIX[17] + 1

# First we add the module to the software table.
            _values_ = (self._app.REVISION.revision_id,
                        _parent, _descrip)

            _query_ = "INSERT INTO tbl_software \
                       (fld_revision_id, fld_parent_module, \
                        fld_description) \
                       VALUES (%d, '%s', '%s')" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if not _results_:
                self._app.debug_log.error("software.py: Failed to add new module to software table.")
                return True

# Retrienve the ID of the newly created module.
            if(_conf.BACKEND == 'mysql'):
                _query_ = "SELECT LAST_INSERT_ID()"
            elif(_conf.BACKEND == 'sqlite3'):
                _query_ = "SELECT seq \
                           FROM sqlite_sequence \
                           WHERE name='tbl_software'"

            _new_id_ = self._app.DB.execute_query(_query_,
                                                  None,
                                                  self._app.ProgCnx)
            _new_id_ = _new_id_[0][0]

            if(_new_id_ == ''):
                self._app.debug_log.error("software.py: Failed to retrieve new software module ID.")
                return True

# Add the new software module to the Development Environment risk analysis table.
            _base_query_ = "INSERT INTO tbl_software_development \
                            (fld_software_id, fld_question_id) \
                            VALUES (%d, %d)"
            for i in range(43):
                _values_ = (_new_id_, i)
                _query_ = _base_query_ % _values_
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

# Add the new software module to the Requirements Review risk analysis table.
            _base_query_ = "INSERT INTO tbl_srr_ssr \
                            (fld_software_id, fld_question_id) \
                            VALUES (%d, %d)"
            for i in range(50):
                _values_ = (_new_id_, i)
                _query_ = _base_query_ % _values_
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

# Add the new software module to the Preliminary Design Review risk analysis table.
            _base_query_ = "INSERT INTO tbl_pdr \
                            (fld_software_id, fld_question_id) \
                            VALUES (%d, %d)"
            for i in range(39):
                _values_ = (_new_id_, i)
                _query_ = _base_query_ % _values_
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

# Add the new software module to the Critical Design Review risk analysis table.
            _base_query_ = "INSERT INTO tbl_cdr \
                            (fld_software_id, fld_question_id) \
                            VALUES (%d, %d)"
            for i in range(59):
                _values_ = (_new_id_, i)
                _query_ = _base_query_ % _values_
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

# Add the new software module to the Test Readiness Review risk analysis table.
            _base_query_ = "INSERT INTO tbl_trr \
                            (fld_software_id, fld_question_id) \
                            VALUES (%d, %d)"
            for i in range(25):
                _values_ = (_new_id_, i)
                _query_ = _base_query_ % _values_
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

# Add the new software module to the test table.
            _base_query_ = "INSERT INTO tbl_software_tests \
                            (fld_software_id, fld_technique_id) \
                            VALUES (%d, %d)"

            for i in range(6):
                _values_ = (_new_id_, i)
                _query_ = _base_query_ % _values_
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

        self.load_tree()

        _util.set_cursor(self._app, gtk.gdk.LEFT_PTR)

        return False

    def _module_delete(self, widget):
        """
        Deletes the currently selected software modules from the Program's
        database.

        Keyword Arguments:
        widget -- the widget that called this function.
        """

# First delete all of the children from the software table.
        _query_ = "DELETE FROM tbl_software \
                   WHERE fld_parent_module=%d" % \
                   (self.model.get_string_from_iter(self._selected_row),)
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not results:
            self._app.debug_log.error("software.py: Failed to delete module from software table.")
            return True

# Second delete the parent from the software table.
        _query_ = "DELETE FROM tbl_software \
                   WHERE fld_revision_id=%d \
                   AND fld_software_id=%d" % \
                   (self.model.get_string_from_iter(self._selected_row),)
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error("software.py: Failed to delete module from software table.")
            return True

        self.load_tree()

        return False

    def create_tree(self):
        """
        Creates the Software gtk.Treeview and connects it to callback functions
        to handle editting.  Background and foreground colors can be set using
        the user-defined values in the RTK configuration file.
        """

        scrollwindow = gtk.ScrolledWindow()
        bg_color = _conf.RTK_COLORS[6]
        fg_color = _conf.RTK_COLORS[7]
        (self.treeview, self._col_order) = _widg.make_treeview('Software', 15,
                                                               self._app,
                                                               None,
                                                               bg_color,
                                                               fg_color)

        self.treeview.set_tooltip_text(_("Displays an indentured list (tree) of software."))
        self.treeview.set_enable_tree_lines(True)
        scrollwindow.add(self.treeview)
        self.model = self.treeview.get_model()

        self.treeview.set_search_column(0)
        self.treeview.set_reorderable(True)

        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None, 0)
        self.treeview.connect('row_activated', self._treeview_row_changed, 0)

        return(scrollwindow)

    def load_tree(self):
        """
        Loads the Software treeview model with system information.  This
        information can be stored either in a MySQL or SQLite3 database.
        """

        if(_conf.RTK_MODULES[0] == 1):
            values = (self._app.REVISION.revision_id,)
        else:
            values = (0,)

        if(_conf.BACKEND == 'mysql'):
            query = "SELECT * FROM tbl_software WHERE fld_revision_id=%d"
        if(_conf.BACKEND == 'sqlite3'):
            query = "SELECT * FROM tbl_software WHERE fld_revision_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        if(results == '' or not results):
            return True

        n_assemblies = len(results)

        self.model.clear()
        self._selected_row = None
        for i in range(n_assemblies):
            _values_ = [results[i][0]]
            self._dicSoftware[results[i][1]] = _util.tuple_to_list(results[i][2:], _values_)
            if(results[i][34] == '-'):      # It's the top level element.
                piter = None
            elif(results[i][34] != '-'):    # It's a child element.
                piter = self.model.get_iter_from_string(results[i][34])

            self.model.append(piter, results[i])

        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)

        root = self.model.get_iter_root()
        if root is not None:
            path = self.model.get_path(root)
            col = self.treeview.get_column(0)
            self.treeview.row_activated(path, col)

        return False

    def _treeview_clicked(self, treeview, event):
        """
        Callback function for handling mouse clicks on the Software Object
        treeview.

        Keyword Arguments:
        treeview -- the Software Object treeview.
        event    -- a gtk.gdk.Event that called this function (the
                    important attribute is which mouse button was clicked).
                    1 = left
                    2 = scrollwheel
                    3 = right
                    4 = forward
                    5 = backward
                    8 =
                    9 =
        """

        if(event.button == 1):
            self._treeview_row_changed(treeview, None, 0, 0)
        elif(event.button == 3):
            print "Pop-up a menu!"

        return False

    def _treeview_row_changed(self, treeview, path, column, _index_):
        """
        Callback function to handle events for the SOFTWARE Object
        gtk.Treeview.  It is called whenever the Software Object treeview is
        clicked or a row is activated.  It will save the previously selected
        row in the Software Object treeview.  Then it loads the SOFTWARE Object.

        Keyword Arguments:
        treeview -- the Software Object treeview.
        path     -- the actived row gtk.TreeView path.
        column   -- the actived gtk.TreeViewColumn.
        _index_  -- determined which treeview had the change (0 = main
                    treeview, 1 = incident list treeview, 2 = incident
                    action list treeview)
        """

        # Save the previously selected row in the Software tree.
        if(_index_ == 0):                   # The main software treeview.
            if self._selected_row is not None:
                path_ = self.model.get_path(self._selected_row)
                self._save_line_item(self.model, path_, self._selected_row)

            selection = self.treeview.get_selection()
            (self.model, self._selected_row) = selection.get_selected()
            self.software_id = self.model.get_value(self._selected_row, 1)

            # Build the queries to select the reliability tests and program
            # incidents associated with the selected HARDWARE.
            values = (self.software_id, )
            if(_conf.BACKEND == 'mysql'):
                qryIncidents = "SELECT * FROM tbl_incident \
                                WHERE fld_software_id=%d"
            elif(_conf.BACKEND == 'sqlite3'):
                qryIncidents = "SELECT * FROM tbl_incident \
                                WHERE fld_software_id=?"

            if self._selected_row is not None:
                self.load_notebook()
                self._app.winParts.load_incident_tree(qryIncidents, values)
                return False
            else:
                return True

    def load_notebook(self):
        """ Method to load the SOFTWARE Object gtk.Notebook. """

# Get the application level ID and development phase ID.
        self._app_level = self.model.get_value(self._selected_row, 2)
        self._dev_phase = self.model.get_value(self._selected_row, 36)

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxSoftware)
        self._app.winWorkBook.show_all()

# Always display the General Data page and Development Environment page.
        self._general_data_tab_load()
        self._risk_analysis_tab_load()
        self._test_selection_tab_load()

        self.notebook.set_current_page(0)

        _title_ = _("RTK Work Book: Analyzing %s") % \
                  self.model.get_value(self._selected_row, 3)
        self._app.winWorkBook.set_title(_title_)

        return False

    def _callback_check(self, check, _index_):
        """
        Callback function to retrieve and save checkbutton changes.

        Keyword Arguments:
        check   -- the checkbutton that called the function.
        _index_ -- the position in the Software Object _attribute list
                   associated with the data from the calling checkbutton.
        """

        if(_index_ < 100):                  # Main Software Tree.
            self.model.set_value(self._selected_row,
                                 _index_,
                                 check.get_active())

# Risk analysis checkbutton handling.
        elif(_index_ >= 100 and _index_ < 200): # Development Environment check buttons.
            self._development_env_[_index_ - 100] = _util.string_to_boolean(check.get_active())
        elif(_index_ >= 200 and _index_ < 300): # Requirements Review check buttons.
            self._srr_[_index_ - 200] = _util.string_to_boolean(check.get_active())
        elif(_index_ >= 300 and _index_ < 400): # Preliminary Design Review check buttons.
            self._pdr_[_index_ - 300] = _util.string_to_boolean(check.get_active())
        elif(_index_ >= 400 and _index_ < 500): # Critical Design Review check buttons.
            self._cdr_[_index_ - 400] = _util.string_to_boolean(check.get_active())
        elif(_index_ >= 500 and _index_ < 600): # Test Readiness Review check buttons.
            self._trr_[_index_ - 500] = _util.string_to_boolean(check.get_active())

        return False

    def _callback_combo(self, combo, _index_):
        """
        Callback function to retrieve and save combobox changes.

        Keyword Arguments:
        combo   -- the combobox that called the function.
        _index_ -- the position in the Software Object gtk.TreeView
                   associated with the data from the calling combobox.
        """

        i = combo.get_active()

        if(_index_ < 100):
            if(_index_ == 2):               # Software level
                _phase_id = self.model.get_value(self._selected_row, 36)
                self._app_level = i
                self._risk_analysis_tab_show()
# Remove the existing Test Selection Matrix and add the correct one.
                if(self.scwTestSelectionMatrix.get_child() is not None):
                    self.scwTestSelectionMatrix.remove(self.scwTestSelectionMatrix.get_child())
                if(self._app_level == 2):   # CSCI
                    self.scwTestSelectionMatrix.add(self.tvwCSCITestSelectionMatrix)
                elif(self._app_level == 3): # Unit
                    self.scwTestSelectionMatrix.add(self.tvwUnitTestSelectionMatrix)
                self.scwTestSelectionMatrix.show_all()
            #elif(_index_ == 4):             # Application type
                #self.model.set_value(self._selected_row, 6, self._fault_density[i])
            #elif(_index_ == 5):             # Development environment
            #    self.model.set_value(self._selected_row, 7, self._do[i])
            elif(_index_ == 36):            # Development phase
                _level_id = self.model.get_value(self._selected_row, 2)
                self._dev_phase = i
                self._risk_analysis_tab_show()
            elif(_index_ == 40):            # Test effort
                if(i == 1):
                    self.txtLaborTest.props.editable = True
                    self.txtLaborTest.set_sensitive(True)
                    self.txtLaborDev.props.editable = True
                    self.txtLaborDev.set_sensitive(True)
                    self.txtBudgetTest.props.editable = False
                    self.txtBudgetTest.set_sensitive(False)
                    self.txtBudgetDev.props.editable = False
                    self.txtBudgetDev.set_sensitive(False)
                    self.txtScheduleTest.props.editable = False
                    self.txtScheduleTest.set_sensitive(False)
                    self.txtScheduleDev.props.editable = False
                    self.txtScheduleDev.set_sensitive(False)
                elif(i == 2):
                    self.txtLaborTest.props.editable = False
                    self.txtLaborTest.set_sensitive(False)
                    self.txtLaborDev.props.editable = False
                    self.txtLaborDev.set_sensitive(False)
                    self.txtBudgetTest.props.editable = True
                    self.txtBudgetTest.set_sensitive(True)
                    self.txtBudgetDev.props.editable = True
                    self.txtBudgetDev.set_sensitive(True)
                    self.txtScheduleTest.props.editable = False
                    self.txtScheduleTest.set_sensitive(False)
                    self.txtScheduleDev.props.editable = False
                    self.txtScheduleDev.set_sensitive(False)
                elif(i == 3):
                    self.txtLaborTest.props.editable = False
                    self.txtLaborTest.set_sensitive(False)
                    self.txtLaborDev.props.editable = False
                    self.txtLaborDev.set_sensitive(False)
                    self.txtBudgetTest.props.editable = False
                    self.txtBudgetTest.set_sensitive(False)
                    self.txtBudgetDev.props.editable = False
                    self.txtBudgetDev.set_sensitive(False)
                    self.txtScheduleTest.props.editable = True
                    self.txtScheduleTest.set_sensitive(True)
                    self.txtScheduleDev.props.editable = True
                    self.txtScheduleDev.set_sensitive(True)

            self.model.set_value(self._selected_row, _index_, i)

        return False

    def _callback_entry(self, entry, event, convert, _index_):
        """
        Callback function to retrieve and save entry changes.

        Keyword Arguments:
        entry    -- the entry that called the function.
        event    -- the gtk.gdk.Event that called the function.
        convert  -- the data type to convert the entry contents to.
        _index_  -- the position in the Software Object gtk.TreeView
                    associated with the data from the calling entry.
        """

        from datetime import datetime

        if(convert == 'text'):
            if(_index_ == 3):
                textbuffer = self.txtDescription.get_child().get_child().get_buffer()
                _text_ = textbuffer.get_text(*textbuffer.get_bounds())
            else:
                _text_ = entry.get_text()

        elif(convert == 'int'):
            try:
                _text_ = int(entry.get_text())
            except ValueError:
                _text_ = 0

        elif(convert == 'float'):
            _text_ = float(entry.get_text().replace('$', ''))

        elif(convert == 'date'):
            _text_ = datetime.strptime(entry.get_text(), '%Y-%m-%d').toordinal()

        if(_index_ < 100):                  # Software information.
            # Calculate the number of higher order language lines of code.
            if(_index_ == 18):
                ALOC = self.model.get_value(self._selected_row, 18)
                SLOC = self.model.get_value(self._selected_row, 19)
                HLOC = SLOC - _text_
                try:
                    SL = (float(HLOC)/float(_text_)) + 1.4 * (float(ALOC)/float(_text_))
                except ZeroDivisionError:
                    SL = 0.0
                self.txt83.set_text(str(HLOC))
                self.model.set_value(self._selected_row, 17, HLOC)
                self.model.set_value(self._selected_row, 20, SL)
            elif(_index_ == 19):
                ALOC = self.model.get_value(self._selected_row, 18)
                SLOC = self.model.get_value(self._selected_row, 19)
                HLOC = _text_ - ALOC
                try:
                    SL = (float(HLOC)/float(_text_)) + 1.4 * (float(ALOC)/float(_text_))
                except ZeroDivisionError:
                    SL = 0.0
                self.txt83.set_text(str(HLOC))
                self.model.set_value(self._selected_row, 17, HLOC)
                self.model.set_value(self._selected_row, 20, SL)

# Update the Software Tree.
            self.model.set_value(self._selected_row, _index_, _text_)

# Risk analysis entry handling.
        elif(_index_ >= 200 and _index_ < 300): # Requirements review
            self._srr_[_index_ - 200] = _text_
        elif(_index_ >= 300 and _index_ < 400): # Preliminary design review
            self._pdr_[_index_ - 300] = _text_
        elif(_index_ >= 400 and _index_ < 500): # Critical design review
            self._cdr_[_index_ - 400] = _text_
        elif(_index_ >= 500 and _index_ < 600): # Test readiness review
            self._trr_[_index_ - 500] = _text_

        return False

    def software_save(self):
        """
        Saves the SOFTWARE Object treeview information to the RTK Program's
        MySQL or SQLit3 database.
        """

        self.model.foreach(self._save_line_item)

        return False

    def _save_line_item(self, model, path_, row):
        """
        Saves each row in the SOFTWARE Object treeview model to the MySQL or
        SQLite3 database.

        Keyword Arguments:
        model -- the Software Object treemodel.
        path_ -- the path of the active row in the Software Object
                 treemodel.
        row   -- the selected row in the Software Object treeview.
        """

        values = (model.get_value(row, self._col_order[2]),
                  model.get_value(row, self._col_order[3]),
                  model.get_value(row, self._col_order[4]),
                  model.get_value(row, self._col_order[5]),
                  model.get_value(row, self._col_order[6]),
                  model.get_value(row, self._col_order[7]),
                  model.get_value(row, self._col_order[8]),
                  model.get_value(row, self._col_order[9]),
                  model.get_value(row, self._col_order[10]),
                  model.get_value(row, self._col_order[11]),
                  model.get_value(row, self._col_order[12]),
                  model.get_value(row, self._col_order[13]),
                  model.get_value(row, self._col_order[14]),
                  model.get_value(row, self._col_order[15]),
                  model.get_value(row, self._col_order[16]),
                  model.get_value(row, self._col_order[17]),
                  model.get_value(row, self._col_order[18]),
                  model.get_value(row, self._col_order[19]),
                  model.get_value(row, self._col_order[20]),
                  model.get_value(row, self._col_order[21]),
                  model.get_value(row, self._col_order[22]),
                  model.get_value(row, self._col_order[23]),
                  model.get_value(row, self._col_order[24]),
                  model.get_value(row, self._col_order[25]),
                  model.get_value(row, self._col_order[26]),
                  model.get_value(row, self._col_order[27]),
                  model.get_value(row, self._col_order[28]),
                  model.get_value(row, self._col_order[29]),
                  model.get_value(row, self._col_order[30]),
                  model.get_value(row, self._col_order[31]),
                  model.get_value(row, self._col_order[32]),
                  model.get_value(row, self._col_order[33]),
                  model.get_value(row, self._col_order[34]),
                  model.get_value(row, self._col_order[35]),
                  model.get_value(row, self._col_order[36]),
                  model.get_value(row, self._col_order[37]),
                  model.get_value(row, self._col_order[38]),
                  model.get_value(row, self._col_order[39]),
                  model.get_value(row, self._col_order[40]),
                  model.get_value(row, self._col_order[41]),
                  model.get_value(row, self._col_order[42]),
                  model.get_value(row, self._col_order[43]),
                  model.get_value(row, self._col_order[44]),
                  model.get_value(row, self._col_order[45]),
                  model.get_value(row, self._col_order[46]),
                  model.get_value(row, self._col_order[47]),
                  model.get_value(row, self._col_order[48]),
                  model.get_value(row, self._col_order[49]),
                  model.get_value(row, self._col_order[50]),
                  model.get_value(row, self._col_order[51]),
                  model.get_value(row, self._col_order[52]),
                  model.get_value(row, self._col_order[53]),
                  model.get_value(row, self._col_order[54]),
                  model.get_value(row, self._col_order[55]),
                  model.get_value(row, self._col_order[56]),
                  model.get_value(row, self._col_order[57]),
                  model.get_value(row, self._col_order[58]),
                  model.get_value(row, self._col_order[59]),
                  model.get_value(row, self._col_order[60]),
                  model.get_value(row, self._col_order[61]),
                  model.get_value(row, self._col_order[62]),
                  model.get_value(row, self._col_order[63]),
                  model.get_value(row, self._col_order[64]),
                  model.get_value(row, self._col_order[65]),
                  model.get_value(row, self._col_order[66]),
                  model.get_value(row, self._col_order[67]),
                  model.get_value(row, self._col_order[68]),
                  model.get_value(row, self._col_order[69]),
                  model.get_value(row, self._col_order[0]),
                  model.get_value(row, self._col_order[1]))

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_software \
                     SET fld_level_id=%d, fld_description='%s', \
                         fld_application_id=%d, fld_development_id=%d, \
                         fld_a=%f, fld_do=%f, fld_dd=%d, fld_dc=%f, \
                         fld_d=%f, fld_am=%f, fld_sa=%f, fld_st=%f, \
                         fld_dr=%f, fld_sq=%f, fld_s1=%f, fld_hloc=%d, \
                         fld_aloc=%d, fld_loc=%d, fld_sl=%f, fld_ax=%d, \
                         fld_bx=%d, fld_cx=%d, fld_nm=%d, fld_sx=%f, \
                         fld_um=%d, fld_wm=%d, fld_xm=%d, fld_sm=%f, \
                         fld_df=%f, fld_sr=%f, fld_s2=%f, fld_rpfom=%f, \
                         fld_parent_module='%s', fld_dev_assess_type=%d, \
                         fld_phase_id=%d, fld_tcl=%d, fld_test_path=%d, \
                         fld_category=%d, fld_test_effort=%d, \
                         fld_test_approach=%d, fld_labor_hours_test=%f, \
                         fld_labor_hours_dev=%f, fld_budget_test=%f, \
                         fld_budget_dev=%f, fld_schedule_test=%f, \
                         fld_schedule_dev=%f, fld_branches=%d, \
                         fld_branches_test=%d, fld_inputs=%d, \
                         fld_inputs_test=%d, fld_nm_test=%d, \
                         fld_interfaces=%d, fld_interfaces_test=%d, \
                         fld_te=%f, fld_tc=%f, fld_tm=%f, fld_t=%f, \
                         fld_ft1=%f, fld_ft2=%f, fld_ren_avg=%f, \
                         fld_ren_eot=%f, fld_ec=%f, fld_ev=%f, fld_et=%f, \
                         fld_os=%f, fld_ew=%f, fld_e=%f, fld_f=%f \
                 WHERE fld_revision_id=%d AND fld_software_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_software \
                     SET fld_level_id=?, fld_description=?, \
                         fld_application_id=?, fld_development_id=?, \
                         fld_a=?, fld_do=?, fld_dd=?, fld_dc=?, \
                         fld_d=?, fld_am=?, fld_sa=?, fld_st=?, \
                         fld_dr=?, fld_sq=?, fld_s1=?, fld_hloc=?, \
                         fld_aloc=?, fld_loc=?, fld_sl=?, fld_ax=?, \
                         fld_bx=?, fld_cx=?, fld_nm=?, fld_sx=?, \
                         fld_um=?, fld_wm=?, fld_xm=?, fld_sm=?, \
                         fld_df=?, fld_sr=?, fld_s2=?, fld_rpfom=?, \
                         fld_parent_module=?, fld_dev_assess_type=?, \
                         fld_phase_id=?, fld_tcl=?, fld_test_path=?, \
                         fld_category=?, fld_test_effort=?, \
                         fld_test_approach=?, fld_labor_hours_test=?, \
                         fld_labor_hours_dev=?, fld_budget_test=?, \
                         fld_budget_dev=?, fld_schedule_test=?, \
                         fld_schedule_dev=?, fld_branches=?, \
                         fld_branches_test=?, fld_inputs=?, \
                         fld_inputs_test=?, fld_nm_test=?, \
                         fld_interfaces=?, fld_interfaces_test=?, \
                         fld_te=?, fld_tc=?, fld_tm=?, fld_t=?, \
                         fld_ft1=?, fld_ft2=?, fld_ren_avg=?, \
                         fld_ren_eot=?, fld_ec=?, fld_ev=?, fld_et=?, \
                         fld_os=?, fld_ew=?, fld_e=?, fld_f=? \
                    WHERE fld_revision_id=? AND fld_software_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("software.py: Failed to save software to software table.")
            return True

        return False

    def _save_risk_analysis(self):
        """
        Method to save the answers to the Risk Analysis questions on the
        currently selected tab in the risk analysis gtk.NoteBook.
        """

        def _save_development_env(self):
            _base_query_ = "UPDATE tbl_software_development \
                            SET fld_y=%d \
                            WHERE fld_software_id=%d \
                            AND fld_question_id=%d"
            for i in range(43):
                _values_ = (self._development_env_[i], self.software_id, i)
                _query_ = _base_query_ % _values_
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            return False

        def _save_srr(self):
            _base_query_ = "UPDATE tbl_srr_ssr \
                            SET fld_y=%d \
                            WHERE fld_software_id=%d \
                            AND fld_question_id=%d"
            for i in range(40):
                _values_ = (self._srr_[i], self.software_id, i)
                _query_ = _base_query_ % _values_
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            _base_query_ = "UPDATE tbl_srr_ssr \
                            SET fld_value=%d \
                            WHERE fld_software_id=%d \
                            AND fld_question_id=%d"
            for i in range(40, 50):
                _values_ = (self._srr_[i], self.software_id, i)
                _query_ = _base_query_ % _values_
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            return False

        def _save_pdr(self):
            _base_query_ = "UPDATE tbl_pdr \
                            SET fld_y=%d \
                            WHERE fld_software_id=%d \
                            AND fld_question_id=%d"
            for i in range(29):
                _values_ = (self._pdr_[i], self.software_id, i)
                _query_ = _base_query_ % _values_
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            _base_query_ = "UPDATE tbl_pdr \
                            SET fld_value=%d \
                            WHERE fld_software_id=%d \
                            AND fld_question_id=%d"
            for i in range(20, 39):
                _values_ = (self._pdr_[i], self.software_id, i)
                _query_ = _base_query_ % _values_
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            return False

        def _save_cdr(self):
            _base_query_ = "UPDATE tbl_cdr \
                            SET fld_y=%d \
                            WHERE fld_software_id=%d \
                            AND fld_question_id=%d"
            for i in range(10):
                _values_ = (self._cdr_[i], self.software_id, i)
                _query_ = _base_query_ % _values_
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)
            for i in range(35, 47):
                _values_ = (self._cdr_[i], self.software_id, i)
                _query_ = _base_query_ % _values_
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            _base_query_ = "UPDATE tbl_cdr \
                            SET fld_value=%d \
                            WHERE fld_software_id=%d \
                            AND fld_question_id=%d"
            for i in range(10, 59):
                _values_ = (self._cdr_[i], self.software_id, i)
                _query_ = _base_query_ % _values_
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            return False

        def _save_trr(self):
            _base_query_ = "UPDATE tbl_trr \
                            SET fld_value=%d \
                            WHERE fld_software_id=%d \
                            AND fld_question_id=%d"
            for i in range(4):
                _values_ = (self._trr_[i], self.software_id, i)
                _query_ = _base_query_ % _values_
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)
            for i in range(20, 24):
                _values_ = (self._trr_[i], self.software_id, i)
                _query_ = _base_query_ % _values_
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            _base_query_ = "UPDATE tbl_trr \
                            SET fld_y=%d \
                            WHERE fld_software_id=%d \
                            AND fld_question_id=%d"
            for i in range(4, 20):
                _values_ = (self._trr_[i], self.software_id, i)
                _query_ = _base_query_ % _values_
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            return False

# Find the currently selected tab in the Risk Analysis gtk.NoteBook().  If the
# software item being analyzed is unit-level and the selected tab is not the
# Development Environment tab, then add two to account for the lack of SRR and
# PDR tabs for software units.
        _page_ = self.nbkRiskAnalysis.get_current_page()
        if(self._app_level == 3 and _page_ > 0):
            _page_ += 2

        _util.set_cursor(self._app, gtk.gdk.WATCH)

# Save the correct results.
        if(_page_ == 0):
            if _save_development_env(self):
                self._app.debug_log.error("software.py: Failed to save Development Environment answers.")
        elif(_page_ == 1):
            if _save_srr(self):
                self._app.debug_log.error("software.py: Failed to save Requirements Review answers.")
        elif(_page_ == 2):
            if _save_pdr(self):
                self._app.debug_log.error("software.py: Failed to save Preliminary Design Review answers.")
        elif(_page_ == 3):
            if _save_cdr(self):
                self._app.debug_log.error("software.py: Failed to save Critical Design Review answers.")
        elif(_page_ == 4):
            if _save_trr(self):
                self._app.debug_log.error("software.py: Failed to save Test Readiness Review answers.")

        _util.set_cursor(self._app, gtk.gdk.LEFT_PTR)

        return False

    def _save_test_techniques(self):
        """
        Method to save the test techniques for the currently selected
        software module.
        """

        _selection_ = self.treeview.get_selection()
        (_model_, _row_) = _selection_.get_selected()

        _model_.set_value(_row_, 37, self.cmbTCL.get_active())
        _model_.set_value(_row_, 38, self.cmbTestPath.get_active())

        _values_ = (_model_.get_value(_row_, self._col_order[37]),
                    _model_.get_value(_row_, self._col_order[39]),
                    _model_.get_value(_row_, self._col_order[40]),
                    _model_.get_value(_row_, self._col_order[41]),
                    _model_.get_value(_row_, self._col_order[42]),
                    _model_.get_value(_row_, self._col_order[43]),
                    _model_.get_value(_row_, self._col_order[44]),
                    _model_.get_value(_row_, self._col_order[45]),
                    _model_.get_value(_row_, self._col_order[46]),
                    _model_.get_value(_row_, self._col_order[47]),
                    _model_.get_value(_row_, self._col_order[48]),
                    _model_.get_value(_row_, self._col_order[49]),
                    _model_.get_value(_row_, self._col_order[50]),
                    _model_.get_value(_row_, self._col_order[51]),
                    _model_.get_value(_row_, self._col_order[52]),
                    _model_.get_value(_row_, self._col_order[53]),
                    _model_.get_value(_row_, self._col_order[54]),
                    _model_.get_value(_row_, self._col_order[1]))
        _query_ = "UPDATE tbl_software \
                   SET fld_tcl=%d, fld_test_path=%d, fld_test_effort=%d, \
                       fld_test_approach=%d, fld_labor_hours_test=%f, \
                       fld_labor_hours_dev=%f, fld_budget_test=%f, \
                       fld_budget_dev=%f, fld_schedule_test=%f, \
                       fld_schedule_dev=%f, fld_branches=%d, \
                       fld_branches_test=%d, fld_inputs=%d, \
                       fld_inputs_test=%d, fld_nm_test=%d, fld_interfaces=%d, \
                       fld_interfaces_test=%d \
                   WHERE fld_software_id=%d" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

        #for i in range(5):
        #    _values_ = (model.get_value(row, 37), model.get_value(row, 2),
        #                model.get_value(row, 3), model.get_value(row, 4),
        #                model.get_value(row, 5), model.get_value(row, 6),
        #                model.get_value(row, 7), self.software_id, i)
        #    _query_ = _base_query_ % _values_
        #    _results_ = self._app.DB.execute_query(_query_,
        #                                           None,
        #                                           self._app.ProgCnx,
        #                                           commit=True)

        #    if not _results_:
        #        self._app.debug_log.error("software.py: Failed to save test techniques to software test table.")
        #        return True

        #    row = model.iter_next(row)

        return False

    def _notebook_page_switched(self, notebook, page, page_num, index):
        """
        Called whenever the Tree Book notebook page is changed.

        Keyword Arguments:
        notebook -- the Tree Book notebook widget.
        page     -- the newly selected page widget.
        page_num -- the newly selected page number.
                    0 = General Data
                    1 = Risk Analysis
                    2 =
                    3 =
                    4 =
                    5 =
                    6 =
                    7 =
                    8 =
        index    -- which gtk.Notebook() called this function
        """

        if(index == 0):                     # Main gtk.Notebook
            if(page_num == 1):              # Risk Analysis
                self.btnSaveResults.set_tooltip_text(_("Saves risk analysis information for the selected software unit or module."))
            elif(page_num == 2):            # Test planning
                self.btnSaveResults.set_tooltip_text(_("Saves test planning information for the selected software unit or module."))
            elif(page_num == 3):            # Reliability estimation
                self.btnSaveResults.set_tooltip_text(_("Saves reliability estimates for the selected software unit or module."))
            else:                           # Everything else
                self.btnSaveResults.set_tooltip_text(_("Saves the selected software module."))

        return False

    def _toolbutton_pressed(self, widget):
        """
        Method to reacte to the SOFTWARE Object toolbar button clicked events.

        Keyword Arguments:
        widget -- the toolbar button that was pressed.
        """

        _button_ = widget.get_name()
        _page_ = self.notebook.get_current_page()

        if(_page_ == 1):                    # Risk Analysis
            if(_button_ == 'Save'):
                self._save_risk_analysis()
            if(_button_ == 'Calculate'):
                self._calculate_risk()
        elif(_page_ == 2):                  # Test planning
            if(_button_ == 'Save'):
                self._save_test_techniques()
            if(_button_ == 'Calculate'):
                self._calculate_risk_reduction()
        elif(_page_ == 3):                  #
            if(_button_ == 'Save'):
                print "Save that shit"
        elif(_page_ == 4):                  #
            if(_button_ == 'Save'):
                print "Save that shit"
        elif(_page_ == 5):                  #
            if(_button_ == 'Save'):
                print "Save that shit"
        elif(_page_ == 7):                  #
            if(_button_ == 'Save'):
                print "Save that shit"
        else:                               # Everything else.
            if(_button_ == 'Save'):
                self.software_save()

        return False
