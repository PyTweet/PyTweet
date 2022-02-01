from typing import Any


class Comparable:
    """Represents a class that can compare other classes.

    The sole purpose of this class is to enables other classes to be compare to one or another through an object.

    .. versionadded:: 1.5.0
    """

    def __init__(self, o: object):
        self.o = o

    def __eq__(self, other: Any):
        print("CALLING EQ")
        return self.o == other

    def __ne__(self, other: Any):
        return self.o != other
