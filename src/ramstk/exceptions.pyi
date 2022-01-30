class RAMSTKError(Exception):
    def __init__(self, msg: str = ...) -> None: ...

class DataAccessError(RAMSTKError):
    msg: str
    def __init__(self, msg: str) -> None: ...

class OutOfRangeError(RAMSTKError):
    msg: str
    def __init__(self, msg: str) -> None: ...
