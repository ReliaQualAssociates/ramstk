# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.__mocks__.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""File for organizing mock structures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
from treelib import Tree

MOCK_ENVIRONMENTS = {
    1: {
        'name': 'Condition Name',
        'units': 'Units',
        'minimum': 0.0,
        'maximum': 0.0,
        'mean': 0.0,
        'variance': 0.0,
        'ramp_rate': 0.0,
        'low_dwell_time': 0.0,
        'high_dwell_time': 0.0
    },
    2: {
        'name': 'Condition Name',
        'units': 'Units',
        'minimum': 0.0,
        'maximum': 0.0,
        'mean': 0.0,
        'variance': 0.0,
        'ramp_rate': 0.0,
        'low_dwell_time': 0.0,
        'high_dwell_time': 0.0
    },
    3: {
        'name': 'Condition Name',
        'units': 'Units',
        'minimum': 0.0,
        'maximum': 0.0,
        'mean': 0.0,
        'variance': 0.0,
        'ramp_rate': 0.0,
        'low_dwell_time': 0.0,
        'high_dwell_time': 0.0
    }
}

MOCK_FAILURE_DEFINITIONS = {1: {'definition': 'Failure Definition'}}

MOCK_FUNCTIONS = {
    1: {
        'availability_logistics': 1.0,
        'availability_mission': 1.0,
        'cost': 0.0,
        'function_code': 'PRESS-001',
        'hazard_rate_logistics': 0.0,
        'hazard_rate_mission': 0.0,
        'level': 0,
        'mcmt': 0.0,
        'mmt': 0.0,
        'mpmt': 0.0,
        'mtbf_logistics': 0.0,
        'mtbf_mission': 0.0,
        'mttr': 0.0,
        'name': 'Function Name',
        'parent_id': 0,
        'remarks': '',
        'safety_critical': 0,
        'total_mode_count': 0,
        'total_part_count': 0,
        'type_id': 0
    },
    2: {
        'availability_logistics': 1.0,
        'availability_mission': 1.0,
        'cost': 0.0,
        'function_code': 'PRESS-001',
        'hazard_rate_logistics': 0.0,
        'hazard_rate_mission': 0.0,
        'level': 0,
        'mcmt': 0.0,
        'mmt': 0.0,
        'mpmt': 0.0,
        'mtbf_logistics': 0.0,
        'mtbf_mission': 0.0,
        'mttr': 0.0,
        'name': 'Function Name',
        'parent_id': 0,
        'remarks': '',
        'safety_critical': 0,
        'total_mode_count': 0,
        'total_part_count': 0,
        'type_id': 0
    }
}

MOCK_HAZARDS = {
    1: {
        'assembly_effect': '',
        'assembly_hri': 20,
        'assembly_hri_f': 4,
        'assembly_mitigation': '',
        'assembly_probability': 'Level A - Frequent',
        'assembly_probability_f': 'Level A - Frequent',
        'assembly_severity': 'Medium',
        'assembly_severity_f': 'Medium',
        'function_1': '',
        'function_2': '',
        'function_3': '',
        'function_4': '',
        'function_5': '',
        'potential_cause': '',
        'potential_hazard': '',
        'remarks': '',
        'result_1': 0.0,
        'result_2': 0.0,
        'result_3': 0.0,
        'result_4': 0.0,
        'result_5': 0.0,
        'system_effect': '',
        'system_hri': 20,
        'system_hri_f': 20,
        'system_mitigation': '',
        'system_probability': 'Level A - Frequent',
        'system_probability_f': 'Level A - Frequent',
        'system_severity': 'Medium',
        'system_severity_f': 'Medium',
        'user_blob_1': '',
        'user_blob_2': '',
        'user_blob_3': '',
        'user_float_1': 0.0,
        'user_float_2': 0.0,
        'user_float_3': 0.0,
        'user_int_1': 0,
        'user_int_2': 0,
        'user_int_3': 0
    }
}

MOCK_MISSIONS = {
    1: {
        'description': '',
        'mission_time': 0.0,
        'time_units': 'hours'
    },
    2: {
        'description': 'Mission #2',
        'mission_time': 0.0,
        'time_units': 'hours'
    }
}

MOCK_MISSION_PHASES = {
    1: {
        'description': '',
        'name': '',
        'phase_start': 0.0,
        'phase_end': 0.0
    },
    2: {
        'description': 'Phase #1 for mission #2',
        'name': '',
        'phase_start': 0.0,
        'phase_end': 0.0
    },
    3: {
        'description': 'Phase #2 for mission #2',
        'name': '',
        'phase_start': 0.0,
        'phase_end': 0.0
    }
}

MOCK_REVISIONS = {
    1: {
        'availability_logistics': 0.9986,
        'availability_mission': 0.99934,
        'cost': 12532.15,
        'cost_failure': 0.0000352,
        'cost_hour': 1.2532,
        'hazard_rate_active': 0.0,
        'hazard_rate_dormant': 0.0,
        'hazard_rate_logistics': 0.0,
        'hazard_rate_mission': 0.0,
        'hazard_rate_software': 0.0,
        'mmt': 0.0,
        'mcmt': 0.0,
        'mpmt': 0.0,
        'mtbf_logistics': 0.0,
        'mtbf_mission': 0.0,
        'mttr': 0.0,
        'name': 'Original Revision',
        'reliability_logistics': 0.99986,
        'reliability_mission': 0.99992,
        'remarks': 'This is the original revision.',
        'revision_code': 'Rev. -',
        'program_time': 2562,
        'program_time_sd': 26.83,
        'program_cost': 26492.83,
        'program_cost_sd': 15.62
    },
    2: {
        'availability_logistics': 1.0,
        'availability_mission': 1.0,
        'cost': 0.0,
        'cost_failure': 0.0,
        'cost_hour': 0.0,
        'hazard_rate_active': 0.0,
        'hazard_rate_dormant': 0.0,
        'hazard_rate_logistics': 0.0,
        'hazard_rate_mission': 0.0,
        'hazard_rate_software': 0.0,
        'mmt': 0.0,
        'mcmt': 0.0,
        'mpmt': 0.0,
        'mtbf_logistics': 0.0,
        'mtbf_mission': 0.0,
        'mttr': 0.0,
        'name': 'Revision A',
        'reliability_logistics': 1.0,
        'reliability_mission': 1.0,
        'remarks': 'This is the second revision.',
        'revision_code': 'Rev. A',
        'program_time': 0,
        'program_time_sd': 0.0,
        'program_cost': 0.0,
        'program_cost_sd': 0.0
    }
}

MOCK_STATUS = {
    1: {
        'cost_remaining': 284.98,
        'date_status': date.today() - timedelta(days=1),
        'time_remaining': 125.0
    },
    2: {
        'cost_remaining': 212.32,
        'date_status': date.today(),
        'time_remaining': 112.5
    }
}

MOCK_REQUIREMENTS = {
    1: {
        'derived': 0,
        'description': '',
        'figure_number': '',
        'owner': '',
        'page_number': '',
        'parent_id': 0,
        'priority': 0,
        'requirement_code': 'REL.1',
        'specification': '',
        'requirement_type': '',
        'validated': 0,
        'validated_date': date.today(),
        'q_clarity_0': 0,
        'q_clarity_1': 0,
        'q_clarity_2': 0,
        'q_clarity_3': 0,
        'q_clarity_4': 0,
        'q_clarity_5': 0,
        'q_clarity_6': 0,
        'q_clarity_7': 0,
        'q_clarity_8': 0,
        'q_complete_0': 0,
        'q_complete_1': 0,
        'q_complete_2': 0,
        'q_complete_3': 0,
        'q_complete_4': 0,
        'q_complete_5': 0,
        'q_complete_6': 0,
        'q_complete_7': 0,
        'q_complete_8': 0,
        'q_complete_9': 0,
        'q_consistent_0': 0,
        'q_consistent_1': 0,
        'q_consistent_2': 0,
        'q_consistent_3': 0,
        'q_consistent_4': 0,
        'q_consistent_5': 0,
        'q_consistent_6': 0,
        'q_consistent_7': 0,
        'q_consistent_8': 0,
        'q_verifiable_0': 0,
        'q_verifiable_1': 0,
        'q_verifiable_2': 0,
        'q_verifiable_3': 0,
        'q_verifiable_4': 0,
        'q_verifiable_5': 0
    },
    2: {
        'derived': 1,
        'description': 'Derived requirement #1 for base requirement #1.',
        'figure_number': '',
        'owner': '',
        'page_number': '',
        'parent_id': 1,
        'priority': 0,
        'requirement_code': 'REL.1.1',
        'specification': '',
        'requirement_type': '',
        'validated': 0,
        'validated_date': date.today(),
        'q_clarity_0': 0,
        'q_clarity_1': 0,
        'q_clarity_2': 0,
        'q_clarity_3': 0,
        'q_clarity_4': 0,
        'q_clarity_5': 0,
        'q_clarity_6': 0,
        'q_clarity_7': 0,
        'q_clarity_8': 0,
        'q_complete_0': 0,
        'q_complete_1': 0,
        'q_complete_2': 0,
        'q_complete_3': 0,
        'q_complete_4': 0,
        'q_complete_5': 0,
        'q_complete_6': 0,
        'q_complete_7': 0,
        'q_complete_8': 0,
        'q_complete_9': 0,
        'q_consistent_0': 0,
        'q_consistent_1': 0,
        'q_consistent_2': 0,
        'q_consistent_3': 0,
        'q_consistent_4': 0,
        'q_consistent_5': 0,
        'q_consistent_6': 0,
        'q_consistent_7': 0,
        'q_consistent_8': 0,
        'q_verifiable_0': 0,
        'q_verifiable_1': 0,
        'q_verifiable_2': 0,
        'q_verifiable_3': 0,
        'q_verifiable_4': 0,
        'q_verifiable_5': 0
    }
}

MOCK_STAKEHOLDERS = {
    1: {
        'customer_rank': 1,
        'description': 'Stakeholder Input',
        'group': '',
        'improvement': 0.0,
        'overall_weight': 0.0,
        'planned_rank': 1,
        'priority': 1,
        'requirement_id': 0,
        'stakeholder': '',
        'user_float_1': 1.0,
        'user_float_2': 1.0,
        'user_float_3': 1.0,
        'user_float_4': 1.0,
        'user_float_5': 1.0
    },
    2: {
        'customer_rank': 1,
        'description': 'Stakeholder Input',
        'group': '',
        'improvement': 0.0,
        'overall_weight': 0.0,
        'planned_rank': 1,
        'priority': 1,
        'requirement_id': 0,
        'stakeholder': '',
        'user_float_1': 1.0,
        'user_float_2': 1.0,
        'user_float_3': 1.0,
        'user_float_4': 1.0,
        'user_float_5': 1.0
    }
}

MOCK_VALIDATIONS = {
    1: {
        'acceptable_maximum': 30.0,
        'acceptable_mean': 20.0,
        'acceptable_minimum': 10.0,
        'acceptable_variance': 0.0,
        'confidence': 95.0,
        'cost_average': 0.0,
        'cost_ll': 0.0,
        'cost_maximum': 0.0,
        'cost_mean': 0.0,
        'cost_minimum': 0.0,
        'cost_ul': 0.0,
        'cost_variance': 0.0,
        'date_end': date.today() + timedelta(days=30),
        'date_start': date.today(),
        'description': '',
        'measurement_unit': '',
        'name': 'PRF-0001',
        'status': 0.0,
        'task_type': '',
        'task_specification': '',
        'time_average': 0.0,
        'time_ll': 0.0,
        'time_maximum': 0.0,
        'time_mean': 0.0,
        'time_minimum': 0.0,
        'time_ul': 0.0,
        'time_variance': 0.0
    },
    2: {
        'acceptable_maximum': 30.0,
        'acceptable_mean': 20.0,
        'acceptable_minimum': 10.0,
        'acceptable_variance': 0.0,
        'confidence': 95.0,
        'cost_average': 0.0,
        'cost_ll': 0.0,
        'cost_maximum': 0.0,
        'cost_mean': 0.0,
        'cost_minimum': 0.0,
        'cost_ul': 0.0,
        'cost_variance': 0.0,
        'date_end': date.today() + timedelta(days=20),
        'date_start': date.today() - timedelta(days=10),
        'description': '',
        'measurement_unit': '',
        'name': '',
        'status': 0.0,
        'task_type': 'Reliability, Assessment',
        'task_specification': '',
        'time_average': 0.0,
        'time_ll': 0.0,
        'time_maximum': 0.0,
        'time_mean': 0.0,
        'time_minimum': 0.0,
        'time_ul': 0.0,
        'time_variance': 0.0
    },
    3: {
        'acceptable_maximum': 30.0,
        'acceptable_mean': 20.0,
        'acceptable_minimum': 10.0,
        'acceptable_variance': 0.0,
        'confidence': 95.0,
        'cost_average': 0.0,
        'cost_ll': 0.0,
        'cost_maximum': 0.0,
        'cost_mean': 0.0,
        'cost_minimum': 0.0,
        'cost_ul': 0.0,
        'cost_variance': 0.0,
        'date_end': date.today() + timedelta(days=30),
        'date_start': date.today(),
        'description': '',
        'measurement_unit': '',
        'name': '',
        'status': 0.0,
        'task_type': 'Reliability, Assessment',
        'task_specification': '',
        'time_average': 20.0,
        'time_ll': 19.0,
        'time_maximum': 40.0,
        'time_mean': 34.0,
        'time_minimum': 12.0,
        'time_ul': 49.0,
        'time_variance': 0.0
    }
}

# Mock treelib Tree()'s.
MOCK_FNCTN_TREE = Tree()
MOCK_FNCTN_TREE.create_node(tag='function',
                            identifier=0,
                            parent=None,
                            data=None)

MOCK_HRDWR_TREE = Tree()
MOCK_HRDWR_TREE.create_node(tag='hardware',
                            identifier=0,
                            parent=None,
                            data=None)
MOCK_HRDWR_TREE.create_node(tag='S1', identifier=1, parent=0, data=None)
MOCK_HRDWR_TREE.create_node(tag='S1:SS1', identifier=2, parent=1, data=None)
MOCK_HRDWR_TREE.create_node(tag='S1:SS2', identifier=3, parent=1, data=None)
MOCK_HRDWR_TREE.create_node(tag='S1:SS3', identifier=4, parent=1, data=None)
MOCK_HRDWR_TREE.create_node(tag='S1:SS4', identifier=5, parent=1, data=None)
MOCK_HRDWR_TREE.create_node(tag='S1:SS1:A1', identifier=6, parent=5, data=None)
MOCK_HRDWR_TREE.create_node(tag='S1:SS1:A2', identifier=7, parent=5, data=None)
MOCK_HRDWR_TREE.create_node(tag='S1:SS1:A2:C1',
                            identifier=8,
                            parent=7,
                            data=None)

MOCK_RQRMNT_TREE = Tree()
MOCK_RQRMNT_TREE.create_node(tag='requirement',
                             identifier=0,
                             parent=None,
                             data=None)
MOCK_RQRMNT_TREE.create_node(tag='REL-0001', identifier=1, parent=0, data=None)
MOCK_RQRMNT_TREE.create_node(tag='PRF-0002', identifier=2, parent=0, data=None)
MOCK_RQRMNT_TREE.create_node(tag='FUN-0003', identifier=3, parent=0, data=None)
