# -*- coding: utf-8 -*-
#
#       rtk.hardware.Model.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Hardware Package Data Model."""  # pragma: no cover

# Import other RTK modules.
# pylint: disable=E0401
from datamodels import RTKDataModel  # pragma: no cover
# pylint: disable=E0401
from dao import RTKHardware, RTKDesignElectric, RTKDesignMechanic, \
    RTKMilHdbkF, RTKNSWC, RTKReliability  # pragma: no cover


class HardwareBoMDataModel(RTKDataModel):
    """
    Contain the attributes and methods of a Hardware Bill of Materials (BoM).

    Class for Hardware BoM data model.  This model builds a Hardware BoM from
    the Hardware, DesignElectric, DesignMechanic, MilHdbkF, NSWC, and
    Reliability data models.  This is a non-hierarchical relationship, such as:

        * Hardware Assembly 1
            - General Data
            - Electrical Design Parameters
            - Mechanical Design Parameters
            - MIL-HDBK-217FN2 Model Parameters
            - NSWC-11 Model Parameters
            - Reliability Parameters
    """

    _tag = 'HardwareBoM'

    def __init__(self, dao):
        """
        Initialize a Hardware BoM data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dtm_hardware = HardwareDataModel(dao)
        self.dtm_design_electric = DesignElectricDataModel(dao)
        self.dtm_design_mechanic = DesignMechanicDataModel(dao)
        self.dtm_mil_hdbk_f = MilHdbkFDataModel(dao)
        self.dtm_nswc = NSWCDataModel(dao)
        self.dtm_reliability = ReliabilityDataModel(dao)

    def select_all(self, revision_id):
        """
        Retrieve all the Hardware BoM data from the RTK Program database.

        :param int revision_id: the Revision ID to select the Hardware BoM for.
        :return: tree; the Tree() of data models.
        :rtype: :class:`treelib.Tree`
        """
        for _node in self.dtm_hardware.select_all(revision_id).all_nodes()[1:]:
            _data = {}
            _hardware_id = _node.data.hardware_id
            _data = _node.data.get_attributes()
            try:
                _electrical = self.dtm_design_electric.select_all(_hardware_id)
                _data.update(
                    _electrical.nodes[_hardware_id].data.get_attributes())
            except KeyError:
                pass

            try:
                _mechanical = self.dtm_design_mechanic.select_all(_hardware_id)
                _data.update(
                    _mechanical.nodes[_hardware_id].data.get_attributes())
            except KeyError:
                pass

            try:
                _mil_hdbk_f = self.dtm_mil_hdbk_f.select_all(_hardware_id)
                _data.update(
                    _mil_hdbk_f.nodes[_hardware_id].data.get_attributes())
            except KeyError:
                pass

            try:
                _nswc = self.dtm_nswc.select_all(_hardware_id)
                _data.update(_nswc.nodes[_hardware_id].data.get_attributes())
            except KeyError:
                pass

            try:
                _reliability = self.dtm_reliability.select_all(_hardware_id)
                _data.update(
                    _reliability.nodes[_hardware_id].data.get_attributes())
            except KeyError:
                pass

            self.tree.create_node(
                _node.data.comp_ref_des,
                _hardware_id,
                parent=_node.data.parent_id,
                data=_data)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _hardware_id)

        return self.tree

    def insert(self, **kwargs):
        """
        Add a new hardware item.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _revision_id = kwargs['revision_id']
        _parent_id = kwargs['parent_id']
        _part = kwargs['part']

        _parent = self.dtm_hardware.select(_parent_id)
        try:
            _parent_is_part = _parent.part
        except AttributeError:
            _parent_is_part = 0

        if _parent_is_part == 1 and _part == 0:
            _error_code = 3006
            _msg = 'RTK ERROR: You can not have a hardware assembly as a ' \
                   'child of a component/piece part.'
        elif _parent_is_part == 1 and _part == 1:
            _error_code = 3006
            _msg = 'RTK ERROR: You can not have a component/piece part as a ' \
                   'child of another component/piece part.'
        else:
            _error_code, _msg = self.dtm_hardware.insert(
                revision_id=_revision_id, parent_id=_parent_id, part=_part)

        if _error_code == 0:
            _hardware_id = self.dtm_hardware.last_id
            _hardware = self.dtm_hardware.select(_hardware_id)
            _data = {'general': self.dtm_hardware.select(_hardware_id)}
            # FIXME: Handle error codes in HardwareBoMDataModel.insert().
            _error_code, _msg = self.dtm_design_electric.insert(
                hardware_id=_hardware_id)
            _data['electrical_design'] = self.dtm_design_electric.select(
                _hardware_id)
            _error_code, _msg = self.dtm_design_mechanic.insert(
                hardware_id=_hardware_id)
            _data['mechanical_design'] = self.dtm_design_mechanic.select(
                _hardware_id)
            _error_code, _msg = self.dtm_mil_hdbk_f.insert(
                hardware_id=_hardware_id)
            _data['mil_hdbk_f'] = self.dtm_mil_hdbk_f.select(_hardware_id)
            _error_code, _msg = self.dtm_nswc.insert(hardware_id=_hardware_id)
            _data['nswc'] = self.dtm_nswc.select(_hardware_id)
            _error_code, _msg = self.dtm_reliability.insert(
                hardware_id=_hardware_id)
            _data['reliability'] = self.dtm_reliability.select(_hardware_id)
            # FIXME: Add code to insert record to analyses tables in HardwareBoMDataModel.insert().

            self.tree.create_node(
                _hardware.comp_ref_des,
                _hardware_id,
                parent=_hardware.parent_id,
                data=_data)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _hardware_id)

        return _error_code, _msg

    def delete(self, node_id):
        """
        Remove a Hardware item.

        :param int node_id: the ID of the Hardware item to be removed from the
                            RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        _session = self.dao.RTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)

        # Delete the RTKHardware entry.  Other RTK Program database tables will
        # delete their entries based on CASCADE behavior.
        try:
            _hardware = self.dtm_hardware.tree.get_node(node_id).data
            if _hardware is not None:
                _error_code, _msg = self.dao.db_delete(_hardware, _session)

        except AttributeError:
            _error_code = 2005
            _msg = 'RTK ERROR: Attempted to delete non-existent Hardware ' \
                   'BoM record ID {0:s}.'.format(str(node_id))

        _session.close()

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code == 0:
            self.tree.remove_node(node_id)
            # CASCADE DELETE removes the records from the database.  Now they
            # need to be reomved from the data model trees.
            self.dtm_hardware.tree.remove_node(node_id)
            self.dtm_design_electric.tree.remove_node(node_id)
            self.dtm_design_mechanic.tree.remove_node(node_id)
            self.dtm_mil_hdbk_f.tree.remove_node(node_id)
            self.dtm_nswc.tree.remove_node(node_id)
            self.dtm_reliability.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def update(self, node_id):
        """
        Update the record associated with Node ID to the RTK Program database.

        :param int node_id: the Hardware ID of the Hardware to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg0 = ''

        _session = self.dao.RTK_SESSION(
            bind=self.dao.engine,
            autoflush=True,
            autocommit=False,
            expire_on_commit=False)

        try:
            _entity = self.dtm_hardware.tree.get_node(node_id).data
            if _entity is not None:
                _session.add(_entity)
        except AttributeError:
            _error_code = 2006
            _msg0 = 'RTKHardware record'

        try:
            _entity = self.dtm_design_electric.tree.get_node(node_id).data
            if _entity is not None:
                _session.add(_entity)
        except AttributeError:
            _error_code = 2006
            _msg0 = _msg0 + ', RTKDesignElectric record'

        try:
            _entity = self.dtm_design_mechanic.tree.get_node(node_id).data
            if _entity is not None:
                _session.add(_entity)
        except AttributeError:
            _error_code = 2006
            _msg0 = _msg0 + ', RTKDesignMechanic record'

        try:
            _entity = self.dtm_mil_hdbk_f.tree.get_node(node_id).data
            if _entity is not None:
                _session.add(_entity)
        except AttributeError:
            _error_code = 2006
            _msg0 = _msg0 + ', RTKMilHdbkF record'

        try:
            _entity = self.dtm_nswc.tree.get_node(node_id).data
            if _entity is not None:
                _session.add(_entity)
        except AttributeError:
            _error_code = 2006
            _msg0 = _msg0 + ', RTKNSWC record'

        try:
            _entity = self.dtm_reliability.tree.get_node(node_id).data
            if _entity is not None:
                _session.add(_entity)
        except AttributeError:
            _error_code = 2006
            _msg0 = _msg0 + ', RTKReliability record'

        if _error_code == 0:
            _error_code, _msg = self.dao.db_update(_session)
        else:
            _error_code = 2006
            _msg = 'RTK ERROR: Problem saving Hardware BoM ID {0:d}.  Error ' \
                   'when saving: {1:s}.'.format(node_id, _msg0)

        _session.close()

        return _error_code, _msg

    def update_all(self):
        """
        Update all RTKHardware table records in the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes()[1:]:
            try:
                _error_code, _msg = self.update(_node.identifier)

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.hardware.Model.HardwareDataModel.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.hardware.Model.HardwareDataModel.update_all().'

        return _error_code, _msg


class HardwareDataModel(RTKDataModel):
    """
    Contain the attributes and methods of a Hardware item.

    An RTK Project will consist of one or more Hardware items.  The attributes
    of a Hardware item are:
    """

    _tag = 'Hardware'  # pragma: no cover

    def __init__(self, dao):
        """
        Initialize a Hardware data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select_all(self, revision_id):
        """
        Retrieve all the Hardware from the RTK Program database.

        This method retrieves all the records from the RTKHardware table in the
        connected RTK Program database.  It then add each to the Hardware data
        model treelib.Tree().

        :param int revision_id: the Revision ID to select the hardware for.
        :return: tree; the Tree() of RTKHardware data models.
        :rtype: :class:`treelib.Tree`
        """
        _session = RTKDataModel.select_all(self)

        for _hardware in _session.query(RTKHardware).filter(
                RTKHardware.revision_id == revision_id).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _hardware.get_attributes()
            _hardware.set_attributes(_attributes)
            self.tree.create_node(
                _hardware.comp_ref_des,
                _hardware.hardware_id,
                parent=_hardware.parent_id,
                data=_hardware)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _hardware.hardware_id)

        _session.close()

        return self.tree

    def insert(self, **kwargs):
        """
        Add a record to the RTKHardware table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _hardware = RTKHardware()
        _hardware.revision_id = kwargs['revision_id']
        _hardware.parent_id = kwargs['parent_id']
        _hardware.part = kwargs['part']
        _error_code, _msg = RTKDataModel.insert(
            self, entities=[
                _hardware,
            ])

        if _error_code == 0:
            self.tree.create_node(
                _hardware.name,
                _hardware.hardware_id,
                parent=_hardware.parent_id,
                data=_hardware)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = _hardware.hardware_id

        return _error_code, _msg

    def delete(self, node_id):
        """
        Remove a record from the RTKHardware table.

        :param int node_id: the ID of the RTKHardware record to be removed from
                            the RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'Hardware ID {0:s}.'.format(str(node_id))
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def update(self, node_id):
        """
        Update the record associated with Node ID to the RTK Program database.

        :param int node_id: the Hardware ID of the Hardware to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent Hardware ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def update_all(self):
        """
        Update all RTKHardware table records in the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.hardware_id)

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.hardware.Model.HardwareDataModel.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.hardware.Model.HardwareDataModel.update_all().'

        return _error_code, _msg

    def make_composite_ref_des(self, node_id=1):
        """
        Make the composite reference designator.

        :keyword int node_id: the ID of the node to make the composite
                              reference designator.
        :return: False if successful or True if an error is encountered
        :rtype: bool
        """
        _return = False
        _pref_des = ''

        # Retrieve the parent hardware item's composite reference designator.
        _node = self.tree.get_node(node_id)
        if self.tree.get_node(_node.bpointer).data is not None:
            _pref_des = self.tree.get_node(_node.bpointer).data.comp_ref_des

        if _pref_des != '':
            _node.data.comp_ref_des = _pref_des + ':' + _node.data.ref_des
        else:
            _node.data.comp_ref_des = _node.data.ref_des

        # Now make the composite reference designator for all the chil nodes.
        for _child_node in self.tree.children(node_id):
            self.make_composite_ref_des(node_id=_child_node.identifier)

        return _return


class DesignElectricDataModel(RTKDataModel):
    """Contain the attributes and methods of an Electrical Design model."""

    _tag = 'DesignElectric'

    def __init__(self, dao):
        """
        Initialize an Electrical Design parameter data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select_all(self, hardware_id):
        """
        Retrieve all RTKDesignElectric records from the RTK Program database.

        This method retrieves all the records from the RTKDesignElectric table
        in the connected RTK Program database.  It then add each to the
        Design Electric data model treelib.Tree().

        :param int hardware_id: the ID of the Hardware item to retrieve the
                                Electrical Design parameters for.
        :return: tree; the treelib Tree() of RTKDesignElectric data models that
                 comprise the DesignElectric tree.
        :rtype: :class:`treelib.Tree`
        """
        # Don't use the RTKDataModel.select_all() method because we don't want
        # to clear the tree or we'll only be left with the last hardware ID
        # passed.
        _session = self.dao.RTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)

        for _design in _session.query(RTKDesignElectric).\
                filter(RTKDesignElectric.hardware_id == hardware_id).all():
            self.tree.create_node(
                _design.hardware_id,
                _design.hardware_id,
                parent=0,
                data=_design)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _design.hardware_id)

        _session.close()

        return self.tree

    def insert(self, **kwargs):
        """
        Add a record to the RTKDesignElectric table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _design = RTKDesignElectric()
        _design.hardware_id = kwargs['hardware_id']
        _error_code, _msg = RTKDataModel.insert(
            self, entities=[
                _design,
            ])

        if _error_code == 0:
            self.tree.create_node(
                _design.hardware_id,
                _design.hardware_id,
                parent=0,
                data=_design)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _design.hardware_id)

        return _error_code, _msg

    def delete(self, node_id):
        """
        Remove a record from the RTKDesignElectric table.

        :param int node_id: the ID of the RTKDesignElectric record to be
                            removed from the RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'DesignElectric record ID ' \
                          '{0:s}.'.format(str(node_id))
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def update(self, node_id):
        """
        Update the record associated with Node ID to the RTK Program database.

        :param int node_id: the DesignElectric ID of the DesignElectric record
                            to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent ' \
                   'DesignElectric record ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def update_all(self):
        """
        Update all RTKDesignElectric table records in the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.hardware_id)

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.hardware.Model.DesignElectricDataModel.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.hardware.Model.DesignElectricDataModel.update_all().'

        return _error_code, _msg


class DesignMechanicDataModel(RTKDataModel):
    """Contain the attributes and methods of a Mechanical Design model."""

    _tag = 'DesignMechanic'

    def __init__(self, dao):
        """
        Initialize a Mechanical Design parameter data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select_all(self, hardware_id):
        """
        Retrieve all RTKDesignMechanic records from the RTK Program database.

        This method retrieves all the records from the RTKDesignMechanic table
        in the connected RTK Program database.  It then add each to the
        Mechanical Design parameter data model treelib.Tree().

        :param int hardware_id: the ID of the Hardware item to retrieve the
                                Mechanical Design parameters for.
        :return: tree; the treelib Tree() of RTKDesignMechanic data models that
                 comprise the DesignMechanic tree.
        :rtype: :class:`treelib.Tree`
        """
        # Don't use the RTKDataModel.select_all() method because we don't want
        # to clear the tree or we'll only be left with the last hardware ID
        # passed.
        _session = self.dao.RTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)

        for _design in _session.query(RTKDesignMechanic).\
                filter(RTKDesignMechanic.hardware_id == hardware_id).all():
            self.tree.create_node(
                _design.hardware_id,
                _design.hardware_id,
                parent=0,
                data=_design)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _design.hardware_id)

        _session.close()

        return self.tree

    def insert(self, **kwargs):
        """
        Add a record to the RTKDesignMechanic table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _design = RTKDesignMechanic()
        _design.hardware_id = kwargs['hardware_id']
        _error_code, _msg = RTKDataModel.insert(
            self, entities=[
                _design,
            ])

        if _error_code == 0:
            self.tree.create_node(
                _design.hardware_id,
                _design.hardware_id,
                parent=0,
                data=_design)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _design.hardware_id)

        return _error_code, _msg

    def delete(self, node_id):
        """
        Remove a record from the RTKDesignMechanic table.

        :param int node_id: the ID of the RTKDesignMechanic record to be
                            removed from the RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'DesignMechanic record ID ' \
                          '{0:s}.'.format(str(node_id))
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def update(self, node_id):
        """
        Update the record associated with Node ID to the RTK Program database.

        :param int node_id: the DesignMechanic ID of the DesignMechanic record
                            to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent ' \
                   'DesignMechanic record ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def update_all(self):
        """
        Update all RTKDesignMechanic table records in the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.hardware_id)

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.hardware.Model.DesignMechanicDataModel.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.hardware.Model.DesignMechanicDataModel.update_all().'

        return _error_code, _msg


class MilHdbkFDataModel(RTKDataModel):
    """Contain the attributes and methods of a MIL-HDBK-217F model."""

    _tag = 'MilHdbkF'

    def __init__(self, dao):
        """
        Initialize a MIL-HDBK-217F data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select_all(self, hardware_id):
        """
        Retrieve all RTKMilHdbkF records from the RTK Program database.

        This method retrieves all the records from the RTKMilHdbkF table
        in the connected RTK Program database.  It then add each to the
        MIL-HDBK-217F data model treelib.Tree().

        :param int hardware_id: the ID of the Hardware item to retrieve the
                                MIL-HDBK-217F parameters for.
        :return: tree; the treelib Tree() of RTKMilHdbkF data models that
                 comprise the MilHdbkF tree.
        :rtype: :class:`treelib.Tree`
        """
        # Don't use the RTKDataModel.select_all() method because we don't want
        # to clear the tree or we'll only be left with the last hardware ID
        # passed.
        _session = self.dao.RTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)

        for _milhdbkf in _session.query(RTKMilHdbkF).\
                filter(RTKMilHdbkF.hardware_id == hardware_id).all():
            self.tree.create_node(
                _milhdbkf.hardware_id,
                _milhdbkf.hardware_id,
                parent=0,
                data=_milhdbkf)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _milhdbkf.hardware_id)

        _session.close()

        return self.tree

    def insert(self, **kwargs):
        """
        Add a record to the RTKMilHdbkF table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _milhdbkf = RTKMilHdbkF()
        _milhdbkf.hardware_id = kwargs['hardware_id']
        _error_code, _msg = RTKDataModel.insert(
            self, entities=[
                _milhdbkf,
            ])

        if _error_code == 0:
            self.tree.create_node(
                _milhdbkf.hardware_id,
                _milhdbkf.hardware_id,
                parent=0,
                data=_milhdbkf)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _milhdbkf.hardware_id)

        return _error_code, _msg

    def delete(self, node_id):
        """
        Remove a record from the RTKMilHdbkF table.

        :param int node_id: the ID of the RTKMilHdbkF record to be
                            removed from the RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'MilHdbkF record ID ' \
                          '{0:s}.'.format(str(node_id))
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def update(self, node_id):
        """
        Update the record associated with Node ID to the RTK Program database.

        :param int node_id: the MilHdbkF ID of the MilHdbkF record
                            to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent ' \
                   'MilHdbkF record ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def update_all(self):
        """
        Update all RTKMilHdbkF table records in the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.hardware_id)

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.hardware.Model.MilHdbkFDataModel.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.hardware.Model.MilHdbkFDataModel.update_all().'

        return _error_code, _msg


class NSWCDataModel(RTKDataModel):
    """Contain the attributes and methods of a NSWC model."""

    _tag = 'NSWC'

    def __init__(self, dao):
        """
        Initialize a NSWC data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select_all(self, hardware_id):
        """
        Retrieve all RTKNSWC records from the RTK Program database.

        This method retrieves all the records from the RTKNSWC table
        in the connected RTK Program database.  It then add each to the
        NSWC data model treelib.Tree().

        :param int hardware_id: the ID of the Hardware item to retrieve the
                                NSWC parameters for.
        :return: tree; the treelib Tree() of RTKNSWC data models that
                 comprise the NSWC tree.
        :rtype: :class:`treelib.Tree`
        """
        # Don't use the RTKDataModel.select_all() method because we don't want
        # to clear the tree or we'll only be left with the last hardware ID
        # passed.
        _session = self.dao.RTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)

        for _nswc in _session.query(RTKNSWC).\
                filter(RTKNSWC.hardware_id == hardware_id).all():
            self.tree.create_node(
                _nswc.hardware_id, _nswc.hardware_id, parent=0, data=_nswc)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _nswc.hardware_id)

        _session.close()

        return self.tree

    def insert(self, **kwargs):
        """
        Add a record to the RTKNSWC table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _nswc = RTKNSWC()
        _nswc.hardware_id = kwargs['hardware_id']
        _error_code, _msg = RTKDataModel.insert(
            self, entities=[
                _nswc,
            ])

        if _error_code == 0:
            self.tree.create_node(
                _nswc.hardware_id, _nswc.hardware_id, parent=0, data=_nswc)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _nswc.hardware_id)

        return _error_code, _msg

    def delete(self, node_id):
        """
        Remove a record from the RTKNSWC table.

        :param int node_id: the ID of the RTKNSWC record to be
                            removed from the RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'NSWC record ID ' \
                          '{0:s}.'.format(str(node_id))
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def update(self, node_id):
        """
        Update the record associated with Node ID to the RTK Program database.

        :param int node_id: the NSWC ID of the NSWC record
                            to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent ' \
                   'NSWC record ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def update_all(self):
        """
        Update all RTKNSWC table records in the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.hardware_id)

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.hardware.Model.NSWCDataModel.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.hardware.Model.NSWCDataModel.update_all().'

        return _error_code, _msg


class ReliabilityDataModel(RTKDataModel):
    """Contain the attributes and methods of a Reliability model."""

    _tag = 'Reliability'

    def __init__(self, dao):
        """
        Initialize a Reliability data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select_all(self, hardware_id):
        """
        Retrieve all RTKReliability records from the RTK Program database.

        This method retrieves all the records from the RTKReliability table
        in the connected RTK Program database.  It then add each to the
        Reliability data model treelib.Tree().

        :param int hardware_id: the ID of the Hardware item to retrieve the
                                Reliability parameters for.
        :return: tree; the treelib Tree() of RTKReliability data models that
                 comprise the Reliability tree.
        :rtype: :class:`treelib.Tree`
        """
        # Don't use the RTKDataModel.select_all() method because we don't want
        # to clear the tree or we'll only be left with the last hardware ID
        # passed.
        _session = self.dao.RTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)

        for _reliability in _session.query(RTKReliability).\
                filter(RTKReliability.hardware_id == hardware_id).all():
            self.tree.create_node(
                _reliability.hardware_id,
                _reliability.hardware_id,
                parent=0,
                data=_reliability)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _reliability.hardware_id)

        _session.close()

        return self.tree

    def insert(self, **kwargs):
        """
        Add a record to the RTKReliability table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _reliability = RTKReliability()
        _reliability.hardware_id = kwargs['hardware_id']
        _error_code, _msg = RTKDataModel.insert(
            self, entities=[
                _reliability,
            ])

        if _error_code == 0:
            self.tree.create_node(
                _reliability.hardware_id,
                _reliability.hardware_id,
                parent=0,
                data=_reliability)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _reliability.hardware_id)

        return _error_code, _msg

    def delete(self, node_id):
        """
        Remove a record from the RTKReliability table.

        :param int node_id: the ID of the RTKReliability record to be
                            removed from the RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'Reliability record ID ' \
                          '{0:s}.'.format(str(node_id))
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def update(self, node_id):
        """
        Update the record associated with Node ID to the RTK Program database.

        :param int node_id: the Reliability ID of the Reliability record
                            to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent ' \
                   'Reliability record ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def update_all(self):
        """
        Update all RTKReliability table records in the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.hardware_id)

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.hardware.Model.ReliabilityDataModel.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.hardware.Model.ReliabilityDataModel.update_all().'

        return _error_code, _msg
