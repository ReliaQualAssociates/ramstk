# -*- coding: utf-8 -*-
#
#       ramstk.controllers.options.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Options Package Data Model."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.commondb import RAMSTKSiteInfo
from ramstk.models.programdb import RAMSTKProgramInfo


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Options data manager.

    This class manages the user-configurable Preferences and Options
    data from the Site and Program databases.
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag = 'options'
    _root = 0

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs) -> None:
        """Initialize a Options data manager instance."""
        RAMSTKDataManager.__init__(self, **kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {'siteinfo': ['site_id'], 'programinfo': ['revision_id']}

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
        pub.subscribe(super().do_get_attributes,
                      'request_get_option_attributes')
        pub.subscribe(super().do_set_attributes,
                      'request_set_option_attributes')

        pub.subscribe(self.do_get_tree, 'request_get_options_tree')
        pub.subscribe(self.do_select_all, 'selected_revision')
        pub.subscribe(self.do_update, 'request_update_option')

    def do_get_tree(self) -> None:
        """Retrieve the Options treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_options_tree', tree=self.tree)

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Options data from the RAMSTK Program database.

        :param attributes: the RAMSTK option attributes for the
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

        pub.sendMessage(
            'succeed_retrieve_options',
            tree=self.tree,
        )

    def do_update(self, node_id: str) -> None:
        """Update the record associated with node ID in RAMSTK databases.

        :param node_id: the node ID of the Options item to save.
        :return: None
        :rtype: None
        """
        try:
            if node_id == 'siteinfo':
                # noinspection PyUnresolvedReferences
                self.common_dao.session.add(
                    self.tree.get_node(node_id).data[node_id])
                self.common_dao.do_update()
                pub.sendMessage(
                    'succeed_update_options',
                    node_id=node_id,
                )
            elif node_id == 'programinfo':
                # noinspection PyUnresolvedReferences
                self.dao.session.add(self.tree.get_node(node_id).data[node_id])
                self.dao.do_update()
                pub.sendMessage(
                    'succeed_update_options',
                    node_id=node_id,
                )
            else:
                _method_name: str = inspect.currentframe(  # type: ignore
                ).f_code.co_name
                _error_msg = ('{1}: Attempted to save non-existent Option '
                              'type {0}.').format(str(node_id), _method_name)
                pub.sendMessage(
                    'do_log_debug',
                    logger_name='DEBUG',
                    message=_error_msg,
                )
                pub.sendMessage(
                    'fail_update_options',
                    error_message=_error_msg,
                )
        except KeyError:
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg = ('{1}: No data package found for Option {0}.').format(
                str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_update_options',
                error_message=_error_msg,
            )
        except (TypeError, DataAccessError):
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg = ('{1}: The value for one or more attributes for '
                          'Options {0} was the wrong type.').format(
                              str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_update_options',
                error_message=_error_msg,
            )
