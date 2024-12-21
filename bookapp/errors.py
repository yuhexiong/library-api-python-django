from enum import Enum

# error code
class LibraryCode(Enum):
    SUCCESSFUL = 0
    INVALID_API = 1001
    INVALID_PARAMETER = 1002
    INSUFFICIENT_PARAMETER = 1003
    OVER_BORROW_TIMES_LIMIT = 1004