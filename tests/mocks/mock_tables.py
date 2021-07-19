# RAMSTK Package Imports
from ramstk.utilities import none_to_default


class MockRAMSTKBaseTable:
    def set_attributes(self, attributes):
        for _key in attributes:
            getattr(self, _key)
            setattr(
                self, _key, none_to_default(attributes[_key], self.__defaults__[_key])
            )
