# -*- coding: utf-8 -*-
#
#       rtk.tests.modules.test_imports.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2018 Doyle "weibullguy" Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Imports class."""
#pylint: disable=protected-access

from collections import OrderedDict
import pandas as pd

import pytest

from rtk.dao import DAO
from rtk.modules.imports import dtmImports, dtcImports

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2018 Andrew "weibullguy" Rowland'


@pytest.mark.integration
def test_create_import_data_model(test_dao):
    """__init__() should return an instance of the Import data model."""
    DUT = dtmImports(test_dao)

    assert isinstance(DUT, dtmImports)
    assert isinstance(DUT.dao, DAO)
    assert isinstance(DUT._dic_field_map, dict)
    assert isinstance(DUT._lst_format_headers, list)
    assert DUT._input_data is None


@pytest.mark.integration
def test_do_read_input_csv(test_dao, test_csv_file_function):
    """do_read_input() should return None when reading a CSV file."""
    DUT = dtmImports(test_dao)

    DUT.do_read_input('csv', test_csv_file_function)

    assert isinstance(DUT._input_data, pd.core.frame.DataFrame)
    assert list(DUT._input_data) == [
        'Revision ID', 'Function ID', 'Level', 'Function Code',
        'Function Name', 'Parent', 'Remarks', 'Safety Critical', 'Type'
    ]
    assert list(DUT._input_data.values[0]) == [
        1, 4, 1, 'PRESS-001', 'Maintain system pressure.', 0,
        'This is a function that is about system pressure.  This remarks box also needs to be larger.',
        1, 0
    ]
    assert list(DUT._input_data.values[1]) == [
        1, 5, 1, 'FLOW-001', 'Maintain system flow.', 0,
        'These are remarks associated with the function FLOW-001.  The remarks box needs to be bigger.',
        0, 0
    ]


@pytest.mark.integration
def test_do_read_input_excel(test_dao, test_excel_file):
    """do_read_input() should return None when reading an Excel file."""
    DUT = dtmImports(test_dao)

    DUT.do_read_input('excel', test_excel_file)

    assert isinstance(DUT._input_data, pd.core.frame.DataFrame)
    assert list(DUT._input_data) == [
        'Revision ID', 'Function ID', 'Level', 'Function Code',
        'Function Name', 'Parent', 'Remarks', 'Safety Critical', 'Type'
    ]
    assert list(DUT._input_data.values[0]) == [
        1, 4, 1, 'PRESS-001', 'Maintain system pressure.', 0,
        'This is a function that is about system pressure.  This remarks box also needs to be larger.',
        1, 0
    ]
    assert list(DUT._input_data.values[1]) == [
        1, 5, 1, 'FLOW-001', 'Maintain system flow.', 0,
        'These are remarks associated with the function FLOW-001.  The remarks box needs to be bigger.',
        0, 0
    ]


@pytest.mark.integration
def test_do_map_field_function(test_dao, test_csv_file_function):
    """
    do_map_field() should return None and create a dictionary with
    RAMSTKFunction field mappings.
    """
    DUT = dtmImports(test_dao)

    DUT.do_read_input('csv', test_csv_file_function)

    for _idx, _key in enumerate(DUT._dic_field_map['Function']):
        DUT.do_map_to_field('Function', list(DUT._input_data)[_idx], _key)

    assert DUT._dic_field_map['Function'] == OrderedDict(
        [('Revision ID', 'Revision ID'), ('Function ID', 'Function ID'),
         ('Level', 'Level'), ('Function Code', 'Function Code'),
         ('Function Name', 'Function Name'), ('Parent', 'Parent'),
         ('Remarks', 'Remarks'), ('Safety Critical',
                                  'Safety Critical'), ('Type', 'Type')])


@pytest.mark.integration
def test_do_map_field_requirement(test_dao, test_csv_file_requirement):
    """
    do_map_field() should return None and create a dictionary with
    RAMSTKRequirement field mappings.
    """
    DUT = dtmImports(test_dao)

    DUT.do_read_input('csv', test_csv_file_requirement)

    for _idx, _key in enumerate(DUT._dic_field_map['Requirement']):
        DUT.do_map_to_field('Requirement', list(DUT._input_data)[_idx], _key)

    assert DUT._dic_field_map['Requirement'] == OrderedDict(
        [('Revision ID', 'Revision ID'), ('Requirement ID', 'Requirement ID'),
         ('Derived?',
          'Derived?'), ('Requirement',
                        'Requirement'), ('Figure Number',
                                         'Figure Number'), ('Owner', 'Owner'),
         ('Page Number',
          'Page Number'), ('Parent ID', 'Parent ID'), ('Priority', 'Priority'),
         ('Requirement Code',
          'Requirement Code'), ('Specification',
                                'Specification'), ('Requirement Type',
                                                   'Requirement Type'),
         ('Validated?', 'Validated?'), ('Validated Date', 'Validated Date')])


@pytest.mark.integration
def test_do_map_field_hardware(test_dao, test_csv_file_hardware):
    """
    do_map_field() should return None and create a dictionary with
    RAMSTKHardware field mappings.
    """
    DUT = dtmImports(test_dao)

    DUT.do_read_input('csv', test_csv_file_hardware)

    for _idx, _key in enumerate(DUT._dic_field_map['Hardware']):
        DUT.do_map_to_field('Hardware', list(DUT._input_data)[_idx], _key)

    assert DUT._dic_field_map['Hardware'] == OrderedDict(
        [('Revision ID', 'Revision ID'), ('Hardware ID', 'Hardware ID'),
         ('Alternate Part Number',
          'Alt. Part Num.'), ('CAGE Code', 'CAGE Code'), ('Category ID',
                                                          'Category'),
         ('Composite Ref. Des.', 'Comp. Ref. Des.'), ('Cost', 'Unit Cost'),
         ('Cost Type',
          'Cost Type'), ('Description',
                         'Description'), ('Duty Cycle',
                                          'Duty Cycle'), ('Figure Number',
                                                          'Fig. Num.'),
         ('LCN', 'LCN'), ('Level', 'Level'), ('Manufacturer',
                                              'Supplier'), ('Mission Time',
                                                            'Mission Time'),
         ('Name',
          'Name'), ('NSN', 'NSN'), ('Page Number',
                                    'Page Num.'), ('Parent Assembly',
                                                   'Parent ID'), ('Part',
                                                                  'Part?'),
         ('Part Number',
          'PN'), ('Quantity',
                  'Quantity'), ('Reference Designator',
                                'Ref. Des.'), ('Remarks',
                                               'Remarks'), ('Repairable',
                                                            'Repairable?'),
         ('Specification',
          'Specification'), ('Subcategory ID',
                             'SubCat'), ('Tagged Part',
                                         'Tagged'), ('Year of Manufacture',
                                                     'Year of Manufacture')])


@pytest.mark.integration
def test_do_map_field_design_electric(test_dao, test_csv_file_hardware):
    """
    do_map_field() should return None and create a dictionary with
    RAMSTKDesignElectric field mappings.
    """
    DUT = dtmImports(test_dao)

    DUT.do_read_input('csv', test_csv_file_hardware)

    for _idx, _key in enumerate(DUT._dic_field_map['Design Electric']):
        if _idx == 0:
            DUT.do_map_to_field('Design Electric',
                                list(DUT._input_data)[1], 'Hardware ID')
        else:
            DUT.do_map_to_field('Design Electric',
                                list(DUT._input_data)[_idx + 28], _key)

    assert DUT._dic_field_map['Design Electric'] == OrderedDict(
        [('Hardware ID',
          'Hardware ID'), ('Application ID',
                           'App. ID'), ('Area', 'Area'), ('Capacitance',
                                                          'Capacitance'),
         ('Configuration ID',
          'Configuration'), ('Construction ID',
                             'Construction ID'), ('Contact Form ID',
                                                  'Contact Form'),
         ('Contact Gauge',
          'Constact Gauge'), ('Contact Rating ID',
                              'Contact Rating ID'), ('Current Operating',
                                                     'Operating Current'),
         ('Current Rated',
          'Rated Current'), ('Current Ratio',
                             'Current Ratio'), ('Environment Active ID',
                                                'Active Environment'),
         ('Environment Dormant ID',
          'Dormant Environment'), ('Family ID', 'Family'), ('Feature Size',
                                                            'Feature Size'),
         ('Frequency Operating',
          'Operating Freq.'), ('Insert ID', 'Insert ID'), ('Insulation ID',
                                                           'Insulation ID'),
         ('Manufacturing ID',
          'Manufacturing ID'), ('Matching ID',
                                'Matching'), ('N Active Pins',
                                              'Num. Active Pins'),
         ('N Circuit Planes',
          'Num. Ckt. Planes'), ('N Cycles', 'Num. Cycles'), ('N Elements',
                                                             'Num. Elements'),
         ('N Hand Soldered',
          'Hand Soldered'), ('N Wave Soldered',
                             'Wave Soldered'), ('Operating Life',
                                                'Operating Life'),
         ('Overstress', 'Overstressed?'), ('Package ID',
                                           'Package ID'), ('Power Operating',
                                                           'Operating Power'),
         ('Power Rated',
          'Rated Power'), ('Power Ratio',
                           'Power Ratio'), ('Reason', 'Overstress Reason'),
         ('Resistance', 'Resistance'), ('Specification ID',
                                        'Specification ID'), ('Technology ID',
                                                              'Tech. ID'),
         ('Temperature, Active',
          'Active Temp.'), ('Temperature, Case',
                            'Case Temp.'), ('Temperature, Dormant',
                                            'Dormant Temp.'),
         ('Temperature, Hot Spot',
          'Hot Spot Temp.'), ('Temperature, Junction',
                              'Junction Temp.'), ('Temperature, Knee',
                                                  'Knee Temp.'),
         ('Temperature, Rated Max',
          'Max. Rated Temp.'), ('Temperature, Rated Min',
                                'Min. Rated Temp.'), ('Temperature Rise',
                                                      'Temperature Rise'),
         ('Theta JC', 'Theta JC'), ('Type ID',
                                    'Type'), ('Voltage, AC Operating',
                                              'AC Operating Voltage'),
         ('Voltage, DC Operating',
          'DC Operating Voltage'), ('Voltage ESD',
                                    'ESD Withstand Volts'), ('Voltage, Rated',
                                                             'Rated Voltage'),
         ('Voltage Ratio',
          'Voltage Ratio'), ('Weight', 'Weight'), ('Years in Production',
                                                   'Years in Prod.')])


@pytest.mark.integration
def test_do_map_field_reliability(test_dao, test_csv_file_hardware):
    """
    do_map_field() should return None and create a dictionary with
    RAMSTKReliability field mappings.
    """
    DUT = dtmImports(test_dao)

    DUT.do_read_input('csv', test_csv_file_hardware)

    for _idx, _key in enumerate(DUT._dic_field_map['Reliability']):
        if _idx == 0:
            DUT.do_map_to_field('Reliability',
                                list(DUT._input_data)[1], 'Hardware ID')
        else:
            DUT.do_map_to_field('Reliability',
                                list(DUT._input_data)[_idx + 82], _key)

    assert DUT._dic_field_map['Reliability'] == OrderedDict(
        [('Hardware ID', 'Hardware ID'), ('Additive Adjustment Factor',
                                          'Add. Adj. Factor'),
         ('Failure Distribution ID',
          'Fail. Dist. ID'), ('Failure Rate Method ID',
                              'h(t) Method'), ('Failure Rate Model',
                                               'h(t) Model'),
         ('Specified Failure Rate',
          'Specified h(t)'), ('Failure Rate Type ID',
                              'h(t) Type'), ('Location Parameter', 'Location'),
         ('Specified MTBF',
          'Specified MTBF'), ('Multiplicative Adjustment Factor',
                              'Mult. Adj. Factor'), ('Quality ID', 'Quality'),
         ('Reliability Goal', 'R(t) Goal'), ('Reliability Goal Measure ID',
                                             'R(t) Goal Measure'),
         ('Scale Parameter',
          'Scale Parameter'), ('Shape Parameter',
                               'Shape Parameter'), ('Survival Analysis ID',
                                                    'Surv. Analysis')])


@pytest.mark.integration
def test_do_map_field_validation(test_dao, test_csv_file_validation):
    """
    do_map_field() should return None and create a dictionary with
    RAMSTKValidation field mappings.
    """
    DUT = dtmImports(test_dao)

    DUT.do_read_input('csv', test_csv_file_validation)

    for _idx, _key in enumerate(DUT._dic_field_map['Validation']):
        DUT.do_map_to_field('Validation', list(DUT._input_data)[_idx], _key)

    assert DUT._dic_field_map['Validation'] == OrderedDict(
        [('Revision ID', 'Revision ID'), ('Validation ID', 'Validation ID'),
         ('Acceptable Maximum',
          'Maximum Acceptable'), ('Acceptable Mean',
                                  'Mean Acceptable'), ('Acceptable Minimum',
                                                       'Minimum Acceptable'),
         ('Acceptable Variance',
          'Acceptable Variance'), ('s-Confidence',
                                   's-Confidence'), ('Average Task Cost',
                                                     'Avg. Task Cost'),
         ('Maximum Task Cost',
          'Max. Task Cost'), ('Minimum Task Cost',
                              'Min. Task Cost'), ('Start Date', 'Start Date'),
         ('End Date', 'Finish Date'), ('Task Description',
                                       'Description'), ('Unit of Measure',
                                                        'Unit of Measure'),
         ('Name', 'Task Name'), ('Task Status',
                                 'Status'), ('Task Type',
                                             'Type'), ('Task Specification',
                                                       'Task Spec.'),
         ('Average Task Time',
          'Average Task Time'), ('Maximum Task Time',
                                 'Maximum Task Time'), ('Minimum Task Time',
                                                        'Minimum Task Time')])


@pytest.mark.integration
def test_do_insert_function(test_dao, test_csv_file_function):
    """
    do_insert() should return a zero error code on success and create a new
    RAMSTKFunction object with it's attributes set from the external file data.
    """
    DUT = dtmImports(test_dao)

    DUT.do_read_input('csv', test_csv_file_function)

    for _idx, _key in enumerate(DUT._dic_field_map['Function']):
        DUT.do_map_to_field('Function', list(DUT._input_data)[_idx], _key)

    _revision_id, _count, _error_code, _msg = DUT.do_insert(module='Function')

    assert _revision_id == 1
    assert _count == 2
    assert _error_code == 0
    assert _msg == 'RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program database.'


@pytest.mark.integration
def test_do_insert_requirement(test_dao, test_csv_file_requirement):
    """
    do_insert() should return a zero error code on success and create a new
    RAMSTKRequirement object with it's attributes set from the external file
    data.
    """
    DUT = dtmImports(test_dao)

    DUT.do_read_input('csv', test_csv_file_requirement)

    for _idx, _key in enumerate(DUT._dic_field_map['Requirement']):
        DUT.do_map_to_field('Requirement', list(DUT._input_data)[_idx], _key)

    _revision_id, _count, _error_code, _msg = DUT.do_insert(module='Requirement')

    assert _revision_id == 1
    assert _count == 0
    assert _error_code == 0
    assert _msg == 'RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program database.'


@pytest.mark.integration
def test_do_insert_hardware(test_dao, test_csv_file_hardware):
    """
    do_insert() should return a zero error code on success and create a new
    RAMSTKHardware, RAMSTKDesignElectric, and RAMSTKReliability object with it's
    attributes set from the external file data.
    """
    DUT = dtmImports(test_dao)

    DUT.do_read_input('csv', test_csv_file_hardware)

    for _idx, _key in enumerate(DUT._dic_field_map['Hardware']):
        DUT.do_map_to_field('Hardware', list(DUT._input_data)[_idx], _key)
    for _idx, _key in enumerate(DUT._dic_field_map['Design Electric']):
        if _idx == 0:
            DUT.do_map_to_field('Design Electric',
                                list(DUT._input_data)[1], 'Hardware ID')
        else:
            DUT.do_map_to_field('Design Electric',
                                list(DUT._input_data)[_idx + 28], _key)
    for _idx, _key in enumerate(DUT._dic_field_map['Reliability']):
        if _idx == 0:
            DUT.do_map_to_field('Reliability',
                                list(DUT._input_data)[1], 'Hardware ID')
        else:
            DUT.do_map_to_field('Reliability',
                                list(DUT._input_data)[_idx + 82], _key)

    _revision_id, _count, _error_code, _msg = DUT.do_insert(module='Hardware')

    assert _revision_id == 1
    assert _count == 0
    assert _error_code == 0
    assert _msg == 'RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program database.'


@pytest.mark.integration
def test_do_insert_validation(test_dao, test_csv_file_validation):
    """
    do_insert() should return a zero error code on success and create a new
    RAMSTKValidation object with it's attributes set from the external  file
    data.
    """
    DUT = dtmImports(test_dao)

    DUT.do_read_input('csv', test_csv_file_validation)

    for _idx, _key in enumerate(DUT._dic_field_map['Validation']):
        DUT.do_map_to_field('Validation', list(DUT._input_data)[_idx], _key)

    _revision_id, _count, _error_code, _msg = DUT.do_insert(module='Validation')

    assert _revision_id == 1
    assert _count == 0
    assert _error_code == 0
    assert _msg == 'RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program database.'


@pytest.mark.integration
def test_create_data_controller(test_dao, test_configuration):
    """__init__() should create and instance of the Import data controller."""
    DUT = dtcImports(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcImports)
    assert isinstance(DUT._dtm_data_model, dtmImports)


@pytest.mark.integration
def test_request_do_read_input_csv(test_dao, test_configuration,
                                   test_csv_file_function):
    """
    request_do_read_input() should return None when reading a CSV file."""
    DUT = dtcImports(test_dao, test_configuration, test=True)

    assert DUT.request_do_read_input('csv', test_csv_file_function) is None
    assert isinstance(DUT._dtm_data_model._input_data, pd.core.frame.DataFrame)
    assert list(DUT._dtm_data_model._input_data) == [
        'Revision ID', 'Function ID', 'Level', 'Function Code',
        'Function Name', 'Parent', 'Remarks', 'Safety Critical', 'Type'
    ]
    assert list(DUT._dtm_data_model._input_data.values[0]) == [
        1, 4, 1, 'PRESS-001', 'Maintain system pressure.', 0,
        'This is a function that is about system pressure.  This remarks box also needs to be larger.',
        1, 0
    ]
    assert list(DUT._dtm_data_model._input_data.values[1]) == [
        1, 5, 1, 'FLOW-001', 'Maintain system flow.', 0,
        'These are remarks associated with the function FLOW-001.  The remarks box needs to be bigger.',
        0, 0
    ]


@pytest.mark.integration
def test_request_do_read_input_excel(test_dao, test_configuration,
                                     test_excel_file):
    """
    request_do_read_input() should return None when reading an Excel file.
    """
    DUT = dtcImports(test_dao, test_configuration, test=True)

    assert DUT.request_do_read_input('excel', test_excel_file) is None

    assert isinstance(DUT._dtm_data_model._input_data, pd.core.frame.DataFrame)
    assert list(DUT._dtm_data_model._input_data) == [
        'Revision ID', 'Function ID', 'Level', 'Function Code',
        'Function Name', 'Parent', 'Remarks', 'Safety Critical', 'Type'
    ]
    assert list(DUT._dtm_data_model._input_data.values[0]) == [
        1, 4, 1, 'PRESS-001', 'Maintain system pressure.', 0,
        'This is a function that is about system pressure.  This remarks box also needs to be larger.',
        1, 0
    ]
    assert list(DUT._dtm_data_model._input_data.values[1]) == [
        1, 5, 1, 'FLOW-001', 'Maintain system flow.', 0,
        'These are remarks associated with the function FLOW-001.  The remarks box needs to be bigger.',
        0, 0
    ]


@pytest.mark.integration
def test_request_do_map_field_function(test_dao, test_configuration,
                                       test_csv_file_function):
    """request_do_map_field() should return None."""
    DUT = dtcImports(test_dao, test_configuration, test=True)

    DUT.request_do_read_input('csv', test_csv_file_function)

    for _idx, _key in enumerate(
            DUT._dtm_data_model._dic_field_map['Function']):
        DUT.request_do_map_to_field(
            'Function',
            list(DUT._dtm_data_model._input_data)[_idx], _key)

    assert DUT._dtm_data_model._dic_field_map['Function'] == OrderedDict(
        [('Revision ID', 'Revision ID'), ('Function ID', 'Function ID'),
         ('Level', 'Level'), ('Function Code', 'Function Code'),
         ('Function Name', 'Function Name'), ('Parent', 'Parent'),
         ('Remarks', 'Remarks'), ('Safety Critical',
                                  'Safety Critical'), ('Type', 'Type')])


@pytest.mark.integration
def test_request_do_insert_function_primary_key_violation(
        test_dao, test_configuration, test_csv_file_function):
    """
    request_do_insert() should return a three error code and count of zero
    inserted entities when there is a primary key violation.
    """
    DUT = dtcImports(test_dao, test_configuration, test=True)

    DUT.request_do_read_input('csv', test_csv_file_function)

    for _idx, _key in enumerate(
            DUT._dtm_data_model._dic_field_map['Function']):
        DUT.request_do_map_to_field(
            'Function',
            list(DUT._dtm_data_model._input_data)[_idx], _key)

    _count, _error_code, _msg = DUT.request_do_insert('Function')

    assert _count == 0
    assert _error_code == 3
