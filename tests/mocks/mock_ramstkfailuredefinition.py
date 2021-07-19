# RAMSTK Local Imports
from . import MockRAMSTKBaseTable


class MockRAMSTKFailureDefinition(MockRAMSTKBaseTable):
    __defaults__ = {"definition": "Mock Failure Definition"}

    def __init__(self):
        self.revision_id = 0
        self.definition_id = 0
        self.definition = self.__defaults__["definition"]

    def get_attributes(self):
        """Retrieve current values of the RAMSTKFailureDefinition attributes.

        :return: {revision_id, definition_id, definition} pairs.
        :rtype: (int, int, str)
        """
        _attributes = {
            "revision_id": self.revision_id,
            "definition_id": self.definition_id,
            "definition": self.definition,
        }

        return _attributes
