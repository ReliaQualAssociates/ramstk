# -*- coding: utf-8 -*-
#
#       rtk.modules.similar_item.Model.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Similar Item Analysis Data Model."""

from treelib.exceptions import NodeIDAbsentError

# Import other RTK modules.
from rtk.modules import RTKDataModel
from rtk.dao import RTKSimilarItem


class SimilarItemDataModel(RTKDataModel):
    """
    Contain the attributes and methods of a reliability similar_item.

    An RTK Project will consist of one or more Modes.  The attributes of a
    Mode are:
    """

    _tag = 'SimilarItems'

    def __init__(self, dao):
        """
        Initialize a SimilarItem data model instance.

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

    def do_select_all(self, **kwargs):
        """
        Retrieve all the SimilarItems from the RTK Program database.

        This method retrieves all the records from the RTKSimilarItem table in
        the connected RTK Program database.  It then adds each to the
        SimilarItem data model treelib.Tree().

        :param int revision_id: the Revision ID the SimilarItems are associated
                                with.
        :return: tree; the Tree() of RTKSimilarItem data models.
        :rtype: :class:`treelib.Tree`
        """
        _revision_id = kwargs['revision_id']
        _session = RTKDataModel.do_select_all(self)

        for _similar_item in _session.query(RTKSimilarItem).filter(
                RTKSimilarItem.revision_id == _revision_id).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _similar_item.get_attributes()
            _similar_item.set_attributes(_attributes)
            self.tree.create_node(
                'SimilarItem ID: {0:d}'.format(_similar_item.hardware_id),
                _similar_item.hardware_id,
                parent=_similar_item.parent_id,
                data=_similar_item)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _similar_item.hardware_id)

        _session.close()

        return self.tree

    def do_select_children(self, node_id):
        """
        Select a list containing the immediate child nodes.

        :param int node_id: the Node (Hardware) ID to select the subtree for.
        :return: a list of the immediate child nodes of the passed Node
                 (Hardware) ID.
        :rtype: list
        """
        try:
            _children = self.tree.children(node_id)
        except NodeIDAbsentError:
            _children = []

        return _children

    def do_insert(self, **kwargs):
        """
        Add a record to the RTKSimilarItem table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _similar_item = RTKSimilarItem()
        _similar_item.revision_id = kwargs['revision_id']
        _similar_item.hardware_id = kwargs['hardware_id']
        _similar_item.parent_id = kwargs['parent_id']
        _error_code, _msg = RTKDataModel.do_insert(
            self, entities=[
                _similar_item,
            ])

        self.tree.create_node(
            'SimilarItem ID: {0:d}'.format(_similar_item.hardware_id),
            _similar_item.hardware_id,
            parent=_similar_item.parent_id,
            data=_similar_item)

        self.last_id = max(self.last_id, _similar_item.hardware_id)

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RTKFailureDefinition table.

        :param int node_id: the PyPubSub Tree() ID of the Similar Item to be
                            removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'SimilarItem ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record in the RTKSimilarItem table.

        :param int node_id: the SimilarItem ID to save to the RTK Program
                            database.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = RTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2207
            _msg = 'RTK ERROR: Attempted to save non-existent SimilarItem ' \
                   'ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self):
        """
        Update all RTKSimilarItem records.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.do_update(_node.data.hardware_id)

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.analyses.similar_item.Model.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.analyses.ssimilar_item.Model.update_all().'

        return _error_code, _msg

    def do_calculate(self, node_id, **kwargs):
        """
        Calculate and allocate the goals for the selected hardware item.

        :param int node_id: the Node (Hardware) ID of the hardware item whose
                            goal is to be allocated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _hazard_rate = kwargs['hazard_rate']
        _return = False

        _sia = self.select(node_id)

        if _sia.method_id == 1:
            _return = (_return or _sia.topic_633(_hazard_rate))
        elif _sia.method_id == 2:
            _return = (_return or _sia.user_defined(_hazard_rate))
        else:
            _return = True

        return _return

    def do_calculate_all(self, **kwargs):
        """
        Calculate metrics for all Similar Item analysis.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Calculate all Similar Items, skipping the top node in the tree.
        for _node in self.tree.all_nodes():
            if _node.identifier != 0:
                self.do_calculate(_node.identifier, **kwargs)

        return _return
