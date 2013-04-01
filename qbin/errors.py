"""
Common error classes used throughout the application.
"""


class ExecutionError(BaseException):
    """
    Raised when an error occurrs executing an external process.
    """

    def __init__(self, args, exitcode, output=None):
        """
        Construct a new object with the called process args, exit code, and
        error output.
        """
        self.args = args
        self.exitcode = exitcode
        self.output = output

    def __str__(self):
        """
        Convert the object into a printable string.
        """
        value = "bad exit code %s for %s" % (
            self.exitcode, self.args)
        if self.output:
            value = '%s: %s' % (value, self.output)
        return value

    def __repr__(self):
        """
        Return a string representation of the object.
        """
        return "<ExecuteError(%s, %s, %s)>" % (
            repr(self.args), repr(self.exitcode), repr(self.output))
