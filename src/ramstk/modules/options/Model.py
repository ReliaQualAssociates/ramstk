# -*- coding: utf-8 -*-
#
#       ramstk.modules.options.Model.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Options Data Model."""

# RAMSTK Package Imports
from ramstk.dao import RAMSTKProgramInfo, RAMSTKSiteInfo
from ramstk.modules import RAMSTKDataModel


class OptionsDataModel(RAMSTKDataModel):
    """Contains the attributes and methods of an Options data model."""

    _tag = 'Options'
    _root = 0

    def __init__(self, dao, site_dao):
        """
        Initialize an Options data model instance.

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
        self.dtm_site_options = SiteOptionsDataModel(site_dao)
        self.dtm_program_options = ProgramOptionsDataModel(dao)
        self.site_options = None
        self.program_options = None

    def do_select_all(self, **kwargs):
        """
        Retrieve Options from the RAMSTK Site and RAMSTK Program database.

        This method retrieves all the records from the RAMSTKSiteInfo table and
        the RAMSTKProgramInfo table in the connected RAMSTK Program database.  It
        then adds each to the Options data model treelib.Tree().

        :return: None
        :rtype: None
        """
        _site = kwargs['site']
        _program = kwargs['program']

        if _site:
            self.site_options = self.dtm_site_options.do_select_all()[0]
        if _program:
            self.program_options = self.dtm_program_options.do_select_all()[0]

    def do_update(self):  # pylint: disable=arguments-differ
        """
        Update the selected Options in the RAMSTKProgramInfo table.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = self.dtm_site_options.do_update()
        _return = _return or self.dtm_program_options.do_update()

        return _return


class SiteOptionsDataModel(RAMSTKDataModel):
    """Contain the attributes and methods for Site-wide options."""

    _tag = 'SiteOpts'
    _root = 0

    def __init__(self, dao):
        """
        Initialize a Site Options data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._site_info = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all the Site configuration options from the RAMSTK Site database.

        This method retrieves all the records from the RAMSTKSiteInfo table in the
        connected RAMSTK Site database.  There should only be one record in the
        RAMSTKSiteInfo database.

        :return: None
        :rtype: None
        """
        _session = self.dao.RAMSTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False,
        )

        self._site_info = _session.query(RAMSTKSiteInfo).all()

        _session.close()

        return self._site_info

    def do_update(self):  # pylint: disable=arguments-differ
        """
        Update the record associated with Site ID to the RAMSTK Site database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _return = False

        _session = self.dao.RAMSTK_SESSION(
            bind=self.dao.engine,
            autoflush=True,
            autocommit=False,
            expire_on_commit=False,
        )

        for _entity in self._site_info:
            _session.add(_entity)
        _error_code, _msg = self.dao.db_update(_session)

        _session.close()

        if _error_code != 0:
            _return = True

        return _return


class ProgramOptionsDataModel(RAMSTKDataModel):
    """Contains the attributes and methods for Program (user) options."""

    _tag = 'ProgramOpts'
    _root = 0

    def __init__(self, dao):
        """
        Initialize a Program Options data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._program_info = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all the Program options from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKProgramInfo table in
        the connected RAMSTK Program database.

        :return: None
        :rtype: None
        """
        _session = self.dao.RAMSTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False,
        )

        self._program_info = _session.query(RAMSTKProgramInfo).all()

        _session.close()

        return self._program_info

    def do_update(self):  # pylint: disable=arguments-differ
        """
        Update the record associated with Site ID to the RAMSTK Site database.

        :param int node_id: the Mode ID of the Mode to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _return = False

        _session = self.dao.RAMSTK_SESSION(
            bind=self.dao.engine,
            autoflush=True,
            autocommit=False,
            expire_on_commit=False,
        )

        for _entity in self._program_info:
            _session.add(_entity)
        _error_code, _msg = self.dao.db_update(_session)

        _session.close()

        if _error_code != 0:
            _return = True

        return _return
