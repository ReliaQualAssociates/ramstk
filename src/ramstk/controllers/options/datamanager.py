# -*- coding: utf-8 -*-
#
#       ramstk.controllers.options.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Options Package Data Model."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.models.commondb import RAMSTKSiteInfo
from ramstk.models.programdb import RAMSTKProgramInfo


class DataManager(RAMSTKDataManager):
    """
    Contain the attributes and methods of the Options data manager.

    This class manages the Options data from the RAMSTKMode, RAMSTKMechains,
    RAMSTKOpLoad, RAMSTKOpStress, and RAMSTKTestMethod data models.
    """

    _tag = 'options'
    _root = 0

    def __init__(self, dao, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize a Options data manager instance.

        :param dao: the data access object for communicating with the RAMSTK
            Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataManager.__init__(self, dao, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._parent_id = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.common_dao = kwargs['common_dao']

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_select_all, 'request_select_options')
        pub.subscribe(self.do_update, 'request_update_option')
        pub.subscribe(self.do_get_attributes, 'request_get_option_attributes')
        pub.subscribe(self.do_get_tree, 'request_get_options_tree')
        pub.subscribe(self.do_set_attributes, 'request_set_option_attributes')

    def do_get_tree(self):
        """
        Retrieve the Options treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_options_tree', dmtree=self.tree)

    def do_select_all(self, parent_id):  # pylint: disable=arguments-differ
        """
        Retrieve all the Options data from the RAMSTK Program database.

        :param int parent_id: the parent (function or hardware) ID to select
            the Options for.
        :return: None
        :rtype: None
        """
        self._revision_id = parent_id

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _option in self.common_dao.session.query(RAMSTKSiteInfo).all():

            self.tree.create_node(tag='Site Info',
                                  identifier='siteinfo',
                                  parent=self._root,
                                  data={'siteinfo': _option})

        for _option in self.dao.session.query(RAMSTKProgramInfo).filter(
                RAMSTKProgramInfo.revision_id == self._revision_id).all():

            self.tree.create_node(tag='Program Info',
                                  identifier='programinfo',
                                  parent=self._root,
                                  data={'programinfo': _option})

        pub.sendMessage('succeed_retrieve_options', tree=self.tree)

    def do_set_attributes(self, node_id, key, value, table):
        """
        Set the attributes of the record associated with the Module ID.

        :param int node_id: the ID of the record in the RAMSTK Program
            database table whose attributes are to be set.
        :param str key: the key in the attributes dict.
        :param value: the new value of the attribute to set.
        :param str table: the name of the table whose attributes are being set.
        :return: None
        :rtype: None
        """
        _poppers = {'siteinfo': ['site_id'], 'programinfo': ['revision_id']}

        _attributes = self.do_select(node_id, table=table).get_attributes()

        for _field in _poppers[table]:
            _attributes.pop(_field)

        if key in _attributes:
            _attributes[key] = value

            self.do_select(node_id, table=table).set_attributes(_attributes)

    def do_update(self, node_id):
        """
        Update the record associated with node ID in RAMSTK databases.

        :param int node_id: the node ID of the Options item to save.
        :return: None
        :rtype: None
        """
        try:
            _table = list(self.tree.get_node(node_id).data.keys())[0]
            if node_id in ['siteinfo']:
                self.common_dao.session.add(
                    self.tree.get_node(node_id).data[_table])
            elif node_id in ['programinfo']:
                self.dao.session.add(self.tree.get_node(node_id).data[_table])

            _error_code, _error_msg = self.dao.db_update()

            if _error_code == 0:
                pub.sendMessage('succeed_update_options', node_id=node_id)
            else:
                pub.sendMessage('fail_update_options', error_msg=_error_msg)
        except AttributeError:
            pub.sendMessage('fail_update_options',
                            error_msg=('Attempted to save non-existent '
                                       'Option with Options ID '
                                       '{0:s}.').format(str(node_id)))
