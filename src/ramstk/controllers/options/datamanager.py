# -*- coding: utf-8 -*-
#
#       ramstk.controllers.options.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Options Package Data Model."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.models.commondb import RAMSTKSiteInfo
from ramstk.models.programdb import RAMSTKProgramInfo


class DataManager(RAMSTKDataManager):
    """
    Contain the attributes and methods of the Options data manager.

    This class manages the user-configurable Preferences and Options data from
    the Site and Program databases.
    """

    _tag = 'options'
    _root = 0

    def __init__(self, **kwargs) -> None:
        """Initialize a Options data manager instance."""
        RAMSTKDataManager.__init__(self, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._parent_id = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.common_dao = kwargs['common_dao']
        self.site_configuration = kwargs['site_configuration']
        self.user_configuration = kwargs['user_configuration']

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_select_all, 'selected_revision')
        pub.subscribe(self.do_update, 'request_update_option')
        pub.subscribe(self.do_get_attributes, 'request_get_option_attributes')
        pub.subscribe(self.do_get_tree, 'request_get_options_tree')
        pub.subscribe(self.do_set_attributes, 'request_set_option_attributes')

    def do_get_tree(self) -> None:
        """
        Retrieve the Options treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_options_tree', tree=self.tree)

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """
        Retrieve all the Options data from the RAMSTK Program database.

        :param dict attributes: the RAMSTK option attributes for the
            selected Revision.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        # noinspection PyUnresolvedReferences
        for _option in self.common_dao.session.query(RAMSTKSiteInfo).all():

            self.tree.create_node(tag='Site Info',
                                  identifier='siteinfo',
                                  parent=self._root,
                                  data={'siteinfo': _option})

        # noinspection PyUnresolvedReferences
        for _option in self.dao.session.query(RAMSTKProgramInfo).filter(
                RAMSTKProgramInfo.revision_id == self._revision_id).all():

            self.tree.create_node(tag='Program Info',
                                  identifier='programinfo',
                                  parent=self._root,
                                  data={'programinfo': _option})

        pub.sendMessage('succeed_retrieve_options', tree=self.tree)

    def do_set_attributes(self, node_id: List[str],
                          package: Dict[str, Any]) -> None:
        """
        Set the attributes of the record associated with the Module ID.

        :param int node_id: the ID of the record in the RAMSTK Program
            database table whose attributes are to be set.
        :param dict package: the key:value for the attribute being updated.
        :return: None
        :rtype: None
        """
        [[_key, _value]] = package.items()

        _pkey = {'siteinfo': 'site_id', 'programinfo': 'revision_id'}

        for _table in node_id:
            # noinspection PyTypeChecker
            _attributes = self.do_select(_table,
                                         table=_table).get_attributes()

            if _key in _attributes:
                _attributes[_key] = _value

                _attributes.pop(_pkey[_table])

                # noinspection PyTypeChecker
                self.do_select(_table,
                               table=_table).set_attributes(_attributes)

    def do_update(self, node_id: str) -> None:
        """
        Update the record associated with node ID in RAMSTK databases.

        :param str node_id: the node ID of the Options item to save.
        :return: None
        :rtype: None
        """
        if node_id == 'siteinfo':
            # noinspection PyUnresolvedReferences
            self.common_dao.session.add(
                self.tree.get_node(node_id).data[node_id])
            self.dao.do_update()
            pub.sendMessage('succeed_update_options', node_id=node_id)
        elif node_id == 'programinfo':
            # noinspection PyUnresolvedReferences
            self.dao.session.add(self.tree.get_node(node_id).data[node_id])
            self.dao.do_update()
            pub.sendMessage('succeed_update_options', node_id=node_id)
        else:
            pub.sendMessage('fail_update_options',
                            error_message=('Error saving {0:s} Options to the '
                                           'database.').format(node_id))
