# -*- coding: utf-8 -*-
#
#       ramstk.modules.similar_item.Model.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Similar Item Analysis Data Model."""

from treelib.exceptions import NodeIDAbsentError

# Import other RAMSTK modules.
from ramstk.modules import RAMSTKDataModel
from ramstk.dao import RAMSTKSimilarItem


class SimilarItemDataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of a reliability similar_item.

    An RAMSTK Project will consist of one or more Modes.  The attributes of a
    Mode are:
    """

    _tag = 'SimilarItems'

    def __init__(self, dao):
        """
        Initialize a SimilarItem data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all the SimilarItems from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKSimilarItem table in
        the connected RAMSTK Program database.  It then adds each to the
        SimilarItem data model treelib.Tree().

        :param int revision_id: the Revision ID the SimilarItems are associated
                                with.
        :return: tree; the Tree() of RAMSTKSimilarItem data models.
        :rtype: :class:`treelib.Tree`
        """
        _revision_id = kwargs['revision_id']
        _session = RAMSTKDataModel.do_select_all(self)

        for _similar_item in _session.query(RAMSTKSimilarItem).filter(
                RAMSTKSimilarItem.revision_id == _revision_id).all():
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
            # It is defined in RAMSTKDataModel.__init__
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
            _children = None

        return _children

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKSimilarItem table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _similar_item = RAMSTKSimilarItem()
        _similar_item.revision_id = kwargs['revision_id']
        _similar_item.hardware_id = kwargs['hardware_id']
        _similar_item.parent_id = kwargs['parent_id']
        _error_code, _msg = RAMSTKDataModel.do_insert(
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
        Remove a record from the RAMSTKFailureDefinition table.

        :param int node_id: the PyPubSub Tree() ID of the Similar Item to be
                            removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'SimilarItem ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record in the RAMSTKSimilarItem table.

        :param int node_id: the SimilarItem ID to save to the RAMSTK Program
                            database.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0 and node_id is not None:
            _error_code = 2207
            _msg = 'RAMSTK ERROR: Attempted to save non-existent SimilarItem ' \
                   'ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Update all RAMSTKSimilarItem records.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _debug_msg = self.do_update(_node.identifier)

                _msg = _msg + _debug_msg + '\n'

            except AttributeError:
                _error_code = 1
                _msg = ("RAMSTK ERROR: One or more line items in the similar "
                        "item analysis worksheet did not update.")

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all line items in the similar item "
                "analysis worksheet.")

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

        _sia = self.do_select(node_id)

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

    def do_roll_up(self, node_id):
        """
        Concatenate the descriptions for lower indenture level items.

        :param int node_id: the Node ID to roll the child descriptions up to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False
        _description = ['', '', '', '', '', '', '', '', '', '']

        # Retrieve the change descriptions from all the child elements and
        # concatenate them together to form the parent descriptions.
        for _child in self.do_select_children(node_id):
            _attributes = _child.data.get_attributes()

            _description[0] = _description[0] + \
                              _attributes['change_description_1'] + '\n\n'
            _description[1] = _description[1] + \
                              _attributes['change_description_2'] + '\n\n'
            _description[2] = _description[2] + \
                              _attributes['change_description_3'] + '\n\n'
            _description[3] = _description[3] + \
                              _attributes['change_description_4'] + '\n\n'
            _description[4] = _description[4] + \
                              _attributes['change_description_5'] + '\n\n'
            _description[5] = _description[5] + \
                              _attributes['change_description_6'] + '\n\n'
            _description[6] = _description[6] + \
                              _attributes['change_description_7'] + '\n\n'
            _description[7] = _description[7] + \
                              _attributes['change_description_8'] + '\n\n'
            _description[8] = _description[8] + \
                              _attributes['change_description_9'] + '\n\n'
            _description[9] = _description[9] + \
                              _attributes['change_description_10'] + '\n\n'

        # Now set the parent change descriptions to the concatenated versions
        # created above.
        _entity = self.do_select(node_id)
        _attributes = _entity.get_attributes()
        _attributes['change_description_1'] = _description[0]
        _attributes['change_description_2'] = _description[1]
        _attributes['change_description_3'] = _description[2]
        _attributes['change_description_4'] = _description[3]
        _attributes['change_description_5'] = _description[4]
        _attributes['change_description_6'] = _description[5]
        _attributes['change_description_7'] = _description[6]
        _attributes['change_description_8'] = _description[7]
        _attributes['change_description_9'] = _description[8]
        _attributes['change_description_10'] = _description[9]
        _entity.set_attributes(_attributes)
        self.do_update(node_id)

        return _return
