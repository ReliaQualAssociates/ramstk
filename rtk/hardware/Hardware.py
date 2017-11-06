# -*- coding: utf-8 -*-
#
#       rtk.hardware.Hardware.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
Hardware Package Hardware Module
===============================================================================
"""

from pubsub import pub                          # pylint: disable=E0401

# Import other RTK modules.
from datamodels import RTKDataModel             # pylint: disable=E0401
from datamodels import RTKDataMatrix            # pylint: disable=E0401
from datamodels import RTKDataController        # pylint: disable=E0401
from dao import RTKHardware, RTKHardware        # pylint: disable=E0401


def _get_component_index(category, subcategory):
    """
    Helper method to find the correct component index.

    """

    if category == 1:  # Capacitor
        _c_index = 3
    elif category == 2:  # Connection
        _c_index = 7
    elif category == 3:  # Inductive Device.
        if subcategory > 1:  # Transformer
            _c_index = 9
    elif category == 4:  # IC
        _c_index = 0
    elif category == 7:  # Relay
        _c_index = 6
    elif category == 8:  # Resistor
        _c_index = 4
    elif category == 9:  # Semiconductor
        if subcategory in [1, 2, 3, 4, 5, 6]:
            _c_index = 1
        elif subcategory in [7, 8, 9, 10, 11, 12, 13]:
            _c_index = 2
    elif category == 10:  # Switching Device
        _c_index = 5

    return _c_index


def _get_environment_index(active, dormant):
    """
    Helper method to find the correct environment index.

    """

    if active in [1, 2, 3]:  # Ground
        if dormant == 1:  # Ground
            _e_index = 0
        else:
            _e_index = 7
    elif active in [4, 5]:  # Naval
        if dormant == 1:  # Ground
            _e_index = 4
        elif dormant == 2:  # Naval
            _e_index = 3
        else:
            _e_index = 7
    elif active in [6, 7, 8, 9, 10]:  # Airborne
        if dormant == 1:  # Ground
            _e_index = 2
        elif dormant == 3:  # Airborne
            _e_index = 1
        else:
            _e_index = 7
    elif active == 11:  # Space
        if dormant == 1:  # Ground
            _e_index = 6
        elif dormant == 4:  # Space
            _e_index = 5
        else:
            _e_index = 7

    return _e_index


class Model(RTKDataModel):
    """
    The Hardware data model contains the attributes and methods of a hardware.
    A :py:class:`rtk.hardware.Hardware` will consist of one or more Hardwares.
    The attributes of a Hardware data model are:
    """

    _tag = 'Hardwares'

    def __init__(self, dao):
        """
        Method to initialize a Hardware data model instance.
        """

        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select(self, hardware_id):
        """
        Method to retrieve the instance of the RTKHardware data model for the
        Hardware ID passed.

        :param int hardware_id: the ID Of the Hardware to retrieve.
        :return: the instance of the RTKHardware class that was requested or
                 None if the requested Hardware ID does not exist.
        :rtype: :py:class:`rtk.dao.RTKHardware.RTKHardware`
        """

        return RTKDataModel.select(self, hardware_id)

    def select_all(self, revision_id):
        """
        Method to retrieve all the Hardwares from the RTK Program database.
        Then add each to

        :param int revision_id: the Revision ID to select the Hardwares for.
        :return: tree; the Tree() of RTKHardware data models.
        :rtype: :py:class:`treelib.Tree`
        """

        _session = RTKDataModel.select_all(self)

        for _hardware in _session.query(RTKHardware).filter(
                RTKHardware.revision_id == revision_id).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _hardware.get_attributes()
            _hardware.set_attributes(_attributes[2:])
            self.tree.create_node(_hardware.name, _hardware.hardware_id,
                                  parent=_hardware.parent_id, data=_hardware)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _hardware.hardware_id)

        _session.close()

        return self.tree

    def insert(self, **kwargs):
        """
        Method to add a Hardware to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _hardware = RTKHardware()
        _hardware.revision_id = kwargs['revision_id']
        _hardware.parent_id = kwargs['parent_id']
        _error_code, _msg = RTKDataModel.insert(self, [_hardware, ])

        if _error_code == 0:
            self.tree.create_node(_hardware.name, _hardware.hardware_id,
                                  parent=_hardware.parent_id, data=_hardware)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = _hardware.hardware_id

        return _error_code, _msg

    def delete(self, hardware_id):
        """
        Method to remove the hardware associated with Hardware ID.

        :param int hardware_id: the ID of the Hardware to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _hardware = self.tree.get_node(hardware_id).data
            _error_code, _msg = RTKDataModel.delete(self, _hardware)

            if _error_code == 0:
                self.tree.remove_node(hardware_id)

        except AttributeError:
            _error_code = 2005
            _msg = 'RTK ERROR: Attempted to delete non-existent Hardware ' \
                   'ID {0:d}.'.format(hardware_id)

        return _error_code, _msg

    def update(self, hardware_id):
        """
        Method to update the hardware associated with Hardware ID to the RTK
        Program database.

        :param int hardware_id: the Hardware ID of the Hardware to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code, _msg = RTKDataModel.update(self, hardware_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent Hardware ID ' \
                   '{0:d}.'.format(hardware_id)

        return _error_code, _msg

    def update_all(self):
        """
        Method to save all Hardwares to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = 'RTK SUCCESS: Saving all Hardwares.'

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.hardware_id)

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.hardware.Hardware.Model.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.hardware.Hardware.Model.update_all().'

        return _error_code, _msg

    def calculate_reliability(self, hardware_id):
        """
        Method to calculate the logistics MTBF and mission MTBF.

        :param int hardware_id: the Hardware ID to calculate.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _hardware = self.tree.get_node(hardware_id).data

        _error_code = 0
        _msg = 'RTK SUCCESS: Calculating reliability metrics for Hardware ' \
               'ID {0:d}.'.format(_hardware.hardware_id)

        # Calculate the logistics MTBF.
        try:
            _hardware.mtbf_logistics = 1.0 / _hardware.hazard_rate_logistics
        except(ZeroDivisionError, OverflowError):
            _hardware.mtbf_logistics = 0.0
            _error_code = 3008
            _msg = "RTK ERROR: Zero Division or Overflow Error '" \
                   "when calculating the logistics MTBF for Hardware ID " \
                   "{1:d}.  Logistics hazard rate: {0:f}.".\
                   format(_hardware.hazard_rate_logistics,
                          _hardware.hardware_id)

        # Calculate the mission MTBF.
        try:
            _hardware.mtbf_mission = 1.0 / _hardware.hazard_rate_mission
        except(ZeroDivisionError, OverflowError):
            _hardware.mtbf_mission = 0.0
            _error_code = 3008
            _msg = "RTK ERROR: Zero Division or Overflow Error " \
                   "when calculating the mission MTBF for Hardware ID " \
                   "{1:d}.  Mission hazard rate: {0:f}.".\
                format(_hardware.hazard_rate_logistics, _hardware.hardware_id)

        return _error_code, _msg

    def calculate_availability(self, hardware_id):
        """
        Method to calculate the logistics availability and mission
        availability.

        :param int hardware_id: the Hardware ID to calculate.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _hardware = self.tree.get_node(hardware_id).data

        _error_code = 0
        _msg = 'RTK SUCCESS: Calculating availability metrics for Hardware ' \
               'ID {0:d}.'.format(_hardware.hardware_id)

        # Calculate logistics availability.
        try:
            _hardware.availability_logistics = _hardware.mtbf_logistics \
                                               / (_hardware.mtbf_logistics +
                                                  _hardware.mttr)
        except(ZeroDivisionError, OverflowError):
            _hardware.availability_logistics = 1.0
            _error_code = 3009
            _msg = "RTK ERROR: Zero Division or Overflow Error " \
                   "when calculating the logistics availability for " \
                   "Hardware ID {2:d}.  Logistics MTBF: {0:f} and MTTR: " \
                   "{1:f}.".\
                   format(_hardware.mtbf_logistics, _hardware.mttr,
                          _hardware.hardware_id)

        # Calculate mission availability.
        try:
            _hardware.availability_mission = _hardware.mtbf_mission \
                                             / (_hardware.mtbf_mission +
                                                _hardware.mttr)
        except(ZeroDivisionError, OverflowError):
            _hardware.availability_mission = 1.0
            _error_code = 3009
            _msg = "RTK ERROR: Zero Division or Overflow Error " \
                   "when calculating the mission availability for " \
                   "Hardware ID {2:d}.  Mission MTBF: {0:f} and MTTR: " \
                   "{1:f}.".\
                   format(_hardware.mtbf_mission, _hardware.mttr,
                          _hardware.hardware_id)

        return _error_code, _msg

    def _dormant_hazard_rate(self, component):
        """
        Method to calculate the dormant hazard rate based on active
        environment, dormant environment, and component category.

        All conversion factors come from Reliability Toolkit: Commercial
        Practices Edition, Section 6.3.4, Table 6.3.4-1 (reproduced below).

        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Component |Ground |Airborne|Airborne|Naval  |Naval  |Space  |Space  |
        | Category  |Active |Active  |Active  |Active |Active |Active |Active |
        |           |to     |to      |to      |to     |to     |to     |to     |
        |           |Ground |Airborne|Ground  |Naval  |Ground |Space  |Ground |
        |           |Passive|Passive |Passive |Passive|Passive|Passive|Passive|
        +===========+=======+========+========+=======+=======+=======+=======+
        | Integrated| 0.08  |  0.06  |  0.04  | 0.06  | 0.05  | 0.10  | 0.30  |
        | Circuits  |       |        |        |       |       |       |       |
        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Diodes    | 0.04  |  0.05  |  0.01  | 0.04  | 0.03  | 0.20  | 0.80  |
        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Transistor| 0.05  |  0.06  |  0.02  | 0.05  | 0.03  | 0.20  | 1.00  |
        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Capacitors| 0.10  |  0.10  |  0.03  | 0.10  | 0.04  | 0.20  | 0.40  |
        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Resistors | 0.20  |  0.06  |  0.03  | 0.10  | 0.06  | 0.50  | 1.00  |
        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Switches  | 0.40  |  0.20  |  0.10  | 0.40  | 0.20  | 0.80  | 1.00  |
        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Relays    | 0.20  |  0.20  |  0.04  | 0.30  | 0.08  | 0.40  | 0.90  |
        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Connectors| 0.005 |  0.005 |  0.003 | 0.008 | 0.003 | 0.02  | 0.03  |
        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Circuit   | 0.04  |  0.02  |  0.01  | 0.03  | 0.01  | 0.08  | 0.20  |
        | Boards    |       |        |        |       |       |       |       |
        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Xformers  | 0.20  |  0.20  |  0.20  | 0.30  | 0.30  | 0.50  | 1.00  |
        +-----------+-------+--------+--------+-------+-------+-------+-------+

        :param :class: `rtk.hardware.Component` component: the rtk.Component()
                                                           data model to
                                                           calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # TODO: Move to each component type model.
        _status = False

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
        c_index = _get_component_index(component.category_id,
                                       component.subcategory_id)

        # Now find the appropriate active to passive environment index.
        e_index = _get_environment_index(component.environment_active,
                                         component.environment_dormant)

        try:
            component.hazard_rate_dormant = component.hazard_rate_active * \
                                            factor[c_index - 1][e_index]
        except IndexError:
            component.hazard_rate_dormant = 0.0
            _status = True
        except UnboundLocalError:
            component.hazard_rate_dormant = 0.0
            _status = True

        return _status


class Hardware(object):
    """
    The Hardware data controller provides an interface between the Hardware
    data model and an RTK view model.  A single Hardware controller can manage
    one or more Hardware data models.  The Hardware data controller is
    currently unused.
    """

    def __init__(self):
        """
        Method to initialize a Hardware data controller instance.
        """

        pass
