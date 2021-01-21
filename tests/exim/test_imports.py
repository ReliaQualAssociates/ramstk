# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.exim.test_imports.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle "weibullguy" Rowland doyle.rowland <AT>
# reliaqual <DOT> com
"""Test class for testing the Imports class."""

# Standard Library Imports
import math
from collections import OrderedDict

# Third Party Imports
import numpy as np
import pandas as pd
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase
from ramstk.exim import Import, _do_replace_nan, _get_input_value


@pytest.mark.usefixtures('test_csv_file_function', 'test_program_dao')
class TestImport():
    """Test class for import methods."""
    def on_succeed_read_db_fields(self, db_fields):
        assert isinstance(db_fields, list)
        assert db_fields == [
            'Revision ID', 'Function ID', 'Level', 'Function Code',
            'Function Name', 'Parent', 'Remarks', 'Safety Critical', 'Type'
        ]
        print("\033[36m\nsucceed_read_db_fields topic was broadcast.")

    def on_succeed_import_function(self, module):
        assert module == 'Function'
        print("\033[36m\nsucceed_import_module topic was broadcast.")

    def on_fail_import_function(self, error_message):
        assert error_message == ('_do_import: There was a problem importing '
                                 'Function records.  This is usually caused '
                                 'by key violations; check the ID and/or '
                                 'parent ID fields in the import file.')
        print("\033[35m\nfail_import_module topic was broadcast.")

    def on_succeed_import_requirement(self, module):
        assert module == 'Requirement'
        print("\033[36m\nsucceed_import_module topic was broadcast.")

    def on_succeed_import_hardware(self, module):
        assert module == 'Hardware'
        print("\033[36m\nsucceed_import_module topic was broadcast.")

    def on_succeed_import_validation(self, module):
        assert module == 'Validation'
        print("\033[36m\nsucceed_import_module topic was broadcast.")

    @pytest.mark.unit
    def test_create_import(self):
        """__init__() should return an instance of the Import data model."""
        DUT = Import()

        assert isinstance(DUT, Import)
        assert isinstance(DUT._dic_field_map, dict)
        assert isinstance(DUT._dao, BaseDatabase)
        assert isinstance(DUT._df_input_data, pd.DataFrame)
        assert pub.isSubscribed(DUT._do_connect,
                                'succeed_connect_program_database')
        assert pub.isSubscribed(DUT._do_map_to_field, 'request_map_to_field')
        assert pub.isSubscribed(DUT._do_read_db_fields, 'request_db_fields')
        assert pub.isSubscribed(DUT._do_read_file, 'request_read_import_file')

    @pytest.mark.unit
    def test_do_read_file_csv(self, test_csv_file_function):
        """_do_read_file() should return None when reading a CSV file."""
        DUT = Import()

        DUT._do_read_file('csv', test_csv_file_function)

        assert isinstance(DUT._df_input_data, pd.core.frame.DataFrame)
        assert list(DUT._df_input_data) == [
            'Revision ID', 'Function ID', 'Level', 'Function Code',
            'Function Name', 'Parent', 'Remarks', 'Safety Critical', 'Type'
        ]
        assert list(DUT._df_input_data.values[0]) == [
            1, 5, 1, 'PRESS-001', 'Maintain system pressure.', 0,
            'This is a function that is about system pressure.  This remarks box also needs to be larger.',
            1, 0
        ]
        assert list(DUT._df_input_data.values[1]) == [
            1, 6, 1, 'FLOW-001', 'Maintain system flow.', 0,
            'These are remarks associated with the function FLOW-001.  The remarks box needs to be bigger.',
            0, 0
        ]

    @pytest.mark.unit
    def test_do_read_file_txt(self, test_text_file_function):
        """_do_read_file() should return None when reading a TXT file."""
        DUT = Import()

        DUT._do_read_file('text', test_text_file_function)

        assert isinstance(DUT._df_input_data, pd.core.frame.DataFrame)
        assert list(DUT._df_input_data) == [
            'Revision ID', 'Function ID', 'Level', 'Function Code',
            'Function Name', 'Parent', 'Remarks', 'Safety Critical', 'Type'
        ]
        assert list(DUT._df_input_data.values[0]) == [
            1, 5, 1, 'PRESS-001', 'Maintain system pressure.', 0,
            'This is a function that is about system pressure.  This remarks box also needs to be larger.',
            1, 0
        ]
        assert list(DUT._df_input_data.values[1]) == [
            1, 6, 1, 'FLOW-001', 'Maintain system flow.', 0,
            'These are remarks associated with the function FLOW-001.  The remarks box needs to be bigger.',
            0, 0
        ]

    @pytest.mark.unit
    def test_do_read_file_excel(self, test_excel_file):
        """do_read_read_file() should return None when reading an Excel file."""
        DUT = Import()

        DUT._do_read_file('excel', test_excel_file)

        assert isinstance(DUT._df_input_data, pd.core.frame.DataFrame)
        assert list(DUT._df_input_data)[1:] == [
            'Revision ID', 'Function ID', 'Level', 'Function Code',
            'Function Name', 'Parent', 'Remarks', 'Safety Critical', 'Type'
        ]
        assert list(DUT._df_input_data.values[0])[1:] == [
            1, 5, 1, 'PRESS-001', 'Maintain system pressure.', 0,
            'This is a function that is about system pressure.  This remarks box also needs to be larger.',
            1, 0
        ]
        assert list(DUT._df_input_data.values[1])[1:] == [
            1, 6, 1, 'FLOW-001', 'Maintain system flow.', 0,
            'These are remarks associated with the function FLOW-001.  The remarks box needs to be bigger.',
            0, 0
        ]

    @pytest.mark.unit
    def test_do_read_file_unsupported_type(self, test_excel_file):
        """do_read_read_file() should return None when reading an Excel file."""
        DUT = Import()

        DUT._do_read_file('pdf', test_excel_file)

        assert isinstance(DUT._df_input_data, pd.core.frame.DataFrame)

    @pytest.mark.unit
    def test_do_read_db_fields(self):
        """_do_read_db_fields() should return a list of database fields for the work stream module name passed."""
        pub.subscribe(self.on_succeed_read_db_fields, 'succeed_read_db_fields')

        DUT = Import()

        pub.sendMessage('request_db_fields', module='Function')

        pub.unsubscribe(self.on_succeed_read_db_fields,
                        'succeed_read_db_fields')

    @pytest.mark.unit
    def test_do_map_field_function(self, test_csv_file_function):
        """do_map_field() should return None and create a dictionary with RAMSTKFunction field mappings."""
        DUT = Import()

        DUT._do_read_file('csv', test_csv_file_function)

        for _idx, _key in enumerate(DUT._dic_field_map['Function']):
            DUT._do_map_to_field('Function',
                                 list(DUT._df_input_data)[_idx], _key)

        assert DUT._dic_field_map['Function'] == OrderedDict([
            ('Revision ID', 'Revision ID'), ('Function ID', 'Function ID'),
            ('Level', 'Level'), ('Function Code', 'Function Code'),
            ('Function Name', 'Function Name'), ('Parent', 'Parent'),
            ('Remarks', 'Remarks'), ('Safety Critical', 'Safety Critical'),
            ('Type', 'Type')
        ])

    @pytest.mark.unit
    def test_do_map_field_requirement(self, test_csv_file_requirement):
        """do_map_field() should return None and create a dictionary with RAMSTKRequirement field mappings."""
        DUT = Import()

        DUT._do_read_file('csv', test_csv_file_requirement)

        for _idx, _key in enumerate(DUT._dic_field_map['Requirement']):
            DUT._do_map_to_field('Requirement',
                                 list(DUT._df_input_data)[_idx], _key)

        assert DUT._dic_field_map['Requirement'] == OrderedDict([
            ('Revision ID', 'Revision ID'),
            ('Requirement ID', 'Requirement ID'), ('Derived?', 'Derived?'),
            ('Requirement', 'Requirement'), ('Figure Number', 'Figure Number'),
            ('Owner', 'Owner'), ('Page Number', 'Page Number'),
            ('Parent ID', 'Parent ID'), ('Priority', 'Priority'),
            ('Requirement Code', 'Requirement Code'),
            ('Specification', 'Specification'),
            ('Requirement Type', 'Requirement Type'),
            ('Validated?', 'Validated?'), ('Validated Date', 'Validated Date')
        ])

    @pytest.mark.unit
    def test_do_map_field_hardware(self, test_csv_file_hardware):
        """do_map_field() should return None and create a dictionary with RAMSTKHardware field mappings."""
        DUT = Import()

        DUT._do_read_file('csv', test_csv_file_hardware)

        for _idx, _key in enumerate(DUT._dic_field_map['Hardware']):
            DUT._do_map_to_field('Hardware',
                                 list(DUT._df_input_data)[_idx], _key)

        assert DUT._dic_field_map['Hardware'] == OrderedDict([
            ('Revision ID', 'Revision ID'), ('Hardware ID', 'Hardware ID'),
            ('Alternate Part Number', 'Alt. Part Num.'),
            ('CAGE Code', 'CAGE Code'), ('Category ID', 'Category'),
            ('Composite Ref. Des.', 'Comp. Ref. Des.'), ('Cost', 'Unit Cost'),
            ('Cost Type', 'Cost Type'), ('Description', 'Description'),
            ('Duty Cycle', 'Duty Cycle'), ('Figure Number', 'Fig. Num.'),
            ('LCN', 'LCN'), ('Level', 'Level'), ('Manufacturer', 'Supplier'),
            ('Mission Time', 'Mission Time'), ('Name', 'Name'), ('NSN', 'NSN'),
            ('Page Number', 'Page Num.'), ('Parent Assembly', 'Parent ID'),
            ('Part', 'Part?'), ('Part Number', 'PN'), ('Quantity', 'Quantity'),
            ('Reference Designator', 'Ref. Des.'), ('Remarks', 'Remarks'),
            ('Repairable', 'Repairable?'), ('Specification', 'Specification'),
            ('Subcategory ID', 'SubCat'), ('Tagged Part', 'Tagged'),
            ('Year of Manufacture', 'Year of Manufacture')
        ])

    @pytest.mark.unit
    def test_do_map_field_design_electric(self, test_csv_file_hardware):
        """do_map_field() should return None and create a dictionary with RAMSTKDesignElectric field mappings."""
        DUT = Import()

        DUT._do_read_file('csv', test_csv_file_hardware)

        for _idx, _key in enumerate(DUT._dic_field_map['Design Electric']):
            if _idx == 0:
                DUT._do_map_to_field('Design Electric',
                                     list(DUT._df_input_data)[1],
                                     'Hardware ID')
            else:
                DUT._do_map_to_field('Design Electric',
                                     list(DUT._df_input_data)[_idx + 28], _key)

        assert DUT._dic_field_map['Design Electric'] == OrderedDict([
            ('Hardware ID', 'Hardware ID'), ('Application ID', 'App. ID'),
            ('Area', 'Area'), ('Capacitance', 'Capacitance'),
            ('Configuration ID', 'Configuration'),
            ('Construction ID', 'Construction ID'),
            ('Contact Form ID', 'Contact Form'),
            ('Contact Gauge', 'Constact Gauge'),
            ('Contact Rating ID', 'Contact Rating ID'),
            ('Current Operating', 'Operating Current'),
            ('Current Rated', 'Rated Current'),
            ('Current Ratio', 'Current Ratio'),
            ('Environment Active ID', 'Active Environment'),
            ('Environment Dormant ID', 'Dormant Environment'),
            ('Family ID', 'Family'), ('Feature Size', 'Feature Size'),
            ('Frequency Operating', 'Operating Freq.'),
            ('Insert ID', 'Insert ID'), ('Insulation ID', 'Insulation ID'),
            ('Manufacturing ID', 'Manufacturing ID'),
            ('Matching ID', 'Matching'), ('N Active Pins', 'Num. Active Pins'),
            ('N Circuit Planes', 'Num. Ckt. Planes'),
            ('N Cycles', 'Num. Cycles'), ('N Elements', 'Num. Elements'),
            ('N Hand Soldered', 'Hand Soldered'),
            ('N Wave Soldered', 'Wave Soldered'),
            ('Operating Life', 'Operating Life'),
            ('Overstress', 'Overstressed?'), ('Package ID', 'Package ID'),
            ('Power Operating', 'Operating Power'),
            ('Power Rated', 'Rated Power'), ('Power Ratio', 'Power Ratio'),
            ('Reason', 'Overstress Reason'), ('Resistance', 'Resistance'),
            ('Specification ID', 'Specification ID'),
            ('Technology ID', 'Tech. ID'),
            ('Temperature, Active', 'Active Temp.'),
            ('Temperature, Case', 'Case Temp.'),
            ('Temperature, Dormant', 'Dormant Temp.'),
            ('Temperature, Hot Spot', 'Hot Spot Temp.'),
            ('Temperature, Junction', 'Junction Temp.'),
            ('Temperature, Knee', 'Knee Temp.'),
            ('Temperature, Rated Max', 'Max. Rated Temp.'),
            ('Temperature, Rated Min', 'Min. Rated Temp.'),
            ('Temperature Rise', 'Temperature Rise'), ('Theta JC', 'Theta JC'),
            ('Type ID', 'Type'),
            ('Voltage, AC Operating', 'AC Operating Voltage'),
            ('Voltage, DC Operating', 'DC Operating Voltage'),
            ('Voltage ESD', 'ESD Withstand Volts'),
            ('Voltage, Rated', 'Rated Voltage'),
            ('Voltage Ratio', 'Voltage Ratio'), ('Weight', 'Weight'),
            ('Years in Production', 'Years in Prod.')
        ])

    @pytest.mark.unit
    def test_do_map_field_reliability(self, test_csv_file_hardware):
        """do_map_field() should return None and create a dictionary with RAMSTKReliability field mappings."""
        DUT = Import()

        DUT._do_read_file('csv', test_csv_file_hardware)

        for _idx, _key in enumerate(DUT._dic_field_map['Reliability']):
            if _idx == 0:
                DUT._do_map_to_field('Reliability',
                                     list(DUT._df_input_data)[1],
                                     'Hardware ID')
            else:
                DUT._do_map_to_field('Reliability',
                                     list(DUT._df_input_data)[_idx + 82], _key)

        assert DUT._dic_field_map['Reliability'] == OrderedDict([
            ('Hardware ID', 'Hardware ID'),
            ('Additive Adjustment Factor', 'Add. Adj. Factor'),
            ('Failure Distribution ID', 'Fail. Dist. ID'),
            ('Failure Rate Method ID', 'h(t) Method'),
            ('Failure Rate Model', 'h(t) Model'),
            ('Specified Failure Rate', 'Specified h(t)'),
            ('Failure Rate Type ID', 'h(t) Type'),
            ('Location Parameter', 'Location'),
            ('Specified MTBF', 'Specified MTBF'),
            ('Multiplicative Adjustment Factor', 'Mult. Adj. Factor'),
            ('Quality ID', 'Quality'), ('Reliability Goal', 'R(t) Goal'),
            ('Reliability Goal Measure ID', 'R(t) Goal Measure'),
            ('Scale Parameter', 'Scale Parameter'),
            ('Shape Parameter', 'Shape Parameter'),
            ('Survival Analysis ID', 'Surv. Analysis')
        ])

    @pytest.mark.unit
    def test_do_map_field_validation(self, test_csv_file_validation):
        """do_map_field() should return None and create a dictionary with RAMSTKValidation field mappings."""
        DUT = Import()

        DUT._do_read_file('csv', test_csv_file_validation)

        for _idx, _key in enumerate(DUT._dic_field_map['Validation']):
            DUT._do_map_to_field('Validation',
                                 list(DUT._df_input_data)[_idx], _key)

        assert DUT._dic_field_map['Validation'] == OrderedDict([
            ('Revision ID', 'Revision ID'), ('Validation ID', 'Validation ID'),
            ('Acceptable Maximum', 'Maximum Acceptable'),
            ('Acceptable Mean', 'Mean Acceptable'),
            ('Acceptable Minimum', 'Minimum Acceptable'),
            ('Acceptable Variance', 'Acceptable Variance'),
            ('s-Confidence', 's-Confidence'),
            ('Average Task Cost', 'Avg. Task Cost'),
            ('Maximum Task Cost', 'Max. Task Cost'),
            ('Minimum Task Cost', 'Min. Task Cost'),
            ('Start Date', 'Start Date'), ('End Date', 'Finish Date'),
            ('Task Description', 'Description'),
            ('Unit of Measure', 'Unit of Measure'), ('Name', 'Task Name'),
            ('Task Status', 'Status'), ('Task Type', 'Type'),
            ('Task Specification', 'Task Spec.'),
            ('Average Task Time', 'Average Task Time'),
            ('Maximum Task Time', 'Maximum Task Time'),
            ('Minimum Task Time', 'Minimum Task Time')
        ])

    @pytest.mark.unit
    def test__do_replace_nan_good_value(self):
        """_do_replace_nan() should return the same value passed if not NaN."""
        assert _do_replace_nan('Suck It', 'Real Good') == 'Suck It'

    @pytest.mark.unit
    def test__do_replace_nan_python_nan(self):
        """_do_replace_nan() should return the default value if passed NaN."""
        assert _do_replace_nan(math.nan, 'Real Good') == 'Real Good'

    @pytest.mark.unit
    def test__do_replace_nan_numpy_nan(self):
        """_do_replace_nan() should return the default value if passed NaN."""
        assert _do_replace_nan(np.nan,
                               'Suck It, Real Good') == 'Suck It, Real Good'

    @pytest.mark.unit
    def test__get_input_value(self, test_csv_file_hardware):
        """_get_input_value() should return the value in the input file."""
        DUT = Import()
        DUT._do_read_file('csv', test_csv_file_hardware)

        assert _get_input_value(DUT._dic_field_map['Hardware'],
                                DUT._df_input_data.iloc[0], 'Revision '
                                'ID', 10) == 1
        assert _get_input_value(DUT._dic_field_map['Hardware'],
                                DUT._df_input_data.iloc[0], 'Hardware '
                                'ID', 1) == 10
        assert _get_input_value(DUT._dic_field_map['Hardware'],
                                DUT._df_input_data.iloc[0], 'Category ID',
                                1) == 0
        assert _get_input_value(DUT._dic_field_map['Hardware'],
                                DUT._df_input_data.iloc[0],
                                'Composite Ref. Des.', '') == 'S1'

    @pytest.mark.unit
    def test__get_input_value_nan(self, test_csv_file_hardware):
        """_get_input_value() should return the default value when the input file contains a NaN."""
        DUT = Import()
        DUT._do_read_file('csv', test_csv_file_hardware)

        assert _get_input_value(DUT._dic_field_map['Hardware'],
                                DUT._df_input_data.iloc[0],
                                'Alternate Part Number', 'C2') == 'C2'
        assert _get_input_value(DUT._dic_field_map['Hardware'],
                                DUT._df_input_data.iloc[0], 'CAGE Code',
                                '') == ''
        assert _get_input_value(DUT._dic_field_map['Hardware'],
                                DUT._df_input_data.iloc[0], 'Manufacturer',
                                54) == 54

    @pytest.mark.unit
    def test__get_input_value_key_error(self, test_csv_file_hardware):
        """_get_input_value() should return the default value when the key passed does not exist."""
        DUT = Import()
        DUT._do_read_file('csv', test_csv_file_hardware)

        assert _get_input_value(DUT._dic_field_map['Hardware'],
                                DUT._df_input_data.iloc[0], 'Alt. Part Num.',
                                'C2') == 'C2'

    @pytest.mark.unit
    def test_do_insert_function(self, test_program_dao,
                                test_csv_file_function):
        """do_insert() should return a zero error code on success and create a new RAMSTKFunction object with it's attributes set from the external file data."""
        pub.subscribe(self.on_succeed_import_function, 'succeed_import_module')

        DUT = Import()
        pub.sendMessage('succeed_connect_program_database',
                        dao=test_program_dao)

        DUT._do_read_file('csv', test_csv_file_function)

        for _idx, _key in enumerate(DUT._dic_field_map['Function']):
            DUT._do_map_to_field('Function',
                                 list(DUT._df_input_data)[_idx], _key)

        pub.sendMessage('request_import', module='Function')

        pub.unsubscribe(self.on_succeed_import_function,
                        'succeed_import_module')

    @pytest.mark.unit
    def test_fail_insert_function(self, test_csv_file_function):
        """do_insert() should return a zero error code on success and create a new RAMSTKFunction object with it's attributes set from the external file data."""
        pub.subscribe(self.on_fail_import_function, 'fail_import_module')

        DUT = Import()

        DUT._do_read_file('csv', test_csv_file_function)

        for _idx, _key in enumerate(DUT._dic_field_map['Function']):
            DUT._do_map_to_field('Function',
                                 list(DUT._df_input_data)[_idx], _key)

        pub.sendMessage('request_import', module='Function')

        pub.unsubscribe(self.on_fail_import_function, 'fail_import_module')

    @pytest.mark.unit
    def test_do_insert_requirement(self, test_program_dao,
                                   test_csv_file_requirement):
        """do_insert() should return a zero error code on success and create a new RAMSTKRequirement object with it's attributes set from the external file data."""
        pub.subscribe(self.on_succeed_import_requirement,
                      'succeed_import_module')

        DUT = Import()
        pub.sendMessage('succeed_connect_program_database',
                        dao=test_program_dao)

        DUT._do_read_file('csv', test_csv_file_requirement)

        for _idx, _key in enumerate(DUT._dic_field_map['Requirement']):
            DUT._do_map_to_field('Requirement',
                                 list(DUT._df_input_data)[_idx], _key)

        pub.sendMessage('request_import', module='Requirement')

        pub.unsubscribe(self.on_succeed_import_requirement,
                        'succeed_import_module')

    @pytest.mark.unit
    def test_do_insert_hardware(self, test_program_dao,
                                test_csv_file_hardware):
        """do_insert() should return a zero error code on success and create a new RAMSTKHardware, RAMSTKDesignElectric, and RAMSTKReliability object with it's attributes set from the external file data."""
        pub.subscribe(self.on_succeed_import_hardware, 'succeed_import_module')

        DUT = Import()
        pub.sendMessage('succeed_connect_program_database',
                        dao=test_program_dao)

        DUT._do_read_file('csv', test_csv_file_hardware)

        for _idx, _key in enumerate(DUT._dic_field_map['Hardware']):
            DUT._do_map_to_field('Hardware',
                                 list(DUT._df_input_data)[_idx], _key)
        for _idx, _key in enumerate(DUT._dic_field_map['Design Electric']):
            if _idx == 0:
                DUT._do_map_to_field('Design Electric',
                                     list(DUT._df_input_data)[1],
                                     'Hardware ID')
            else:
                DUT._do_map_to_field('Design Mechanic',
                                     list(DUT._df_input_data)[_idx + 28], _key)
        for _idx, _key in enumerate(DUT._dic_field_map['Reliability']):
            if _idx == 0:
                DUT._do_map_to_field('Reliability',
                                     list(DUT._df_input_data)[1],
                                     'Hardware ID')
            else:
                DUT._do_map_to_field('Reliability',
                                     list(DUT._df_input_data)[_idx + 82], _key)

        pub.sendMessage('request_import', module='Hardware')

        pub.unsubscribe(self.on_succeed_import_hardware,
                        'succeed_import_module')

    @pytest.mark.unit
    def test_do_insert_validation(self, test_program_dao,
                                  test_csv_file_validation):
        """do_insert() should return None on success and create a new RAMSTKValidation object with it's attributes set from the external file data."""
        pub.subscribe(self.on_succeed_import_validation,
                      'succeed_import_module')

        DUT = Import()
        pub.sendMessage('succeed_connect_program_database',
                        dao=test_program_dao)

        DUT._do_read_file('csv', test_csv_file_validation)

        for _idx, _key in enumerate(DUT._dic_field_map['Validation']):
            DUT._do_map_to_field('Validation',
                                 list(DUT._df_input_data)[_idx], _key)

        pub.sendMessage('request_import', module='Validation')

        pub.unsubscribe(self.on_succeed_import_validation,
                        'succeed_import_module')

    @pytest.mark.unit
    def test_do_insert_unsupported(self, test_program_dao,
                                   test_csv_file_validation):
        """do_insert() should return None when passed a module name that doesn't exist."""
        DUT = Import()
        pub.sendMessage('succeed_connect_program_database',
                        dao=test_program_dao)

        DUT._do_read_file('csv', test_csv_file_validation)

        for _idx, _key in enumerate(DUT._dic_field_map['Validation']):
            DUT._do_map_to_field('Validation',
                                 list(DUT._df_input_data)[_idx], _key)

        assert DUT._do_import('Shibboly') is None
