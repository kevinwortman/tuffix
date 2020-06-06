"""
Exceptions defined for the Tuffix API
AUTHOR: Kevin Wortman
INSTITUTION: California State University Fullerton
"""

# base types for exceptions that include a string message
class MessageException(Exception):
    def __init__(self, message):
        if not (isinstance(message, str)):
            raise ValueError
        self.message = message

# commandline usage error
class UsageError(MessageException):
    def __init__(self, message):
        super().__init__(message)

# problem with the environment (wrong OS, essential shell command missing, etc.)
class EnvironmentError(MessageException):
    def __init__(self, message):
        super().__init__(message)

# issue reported by the `status` command, that's at the level of a fatal error
class StatusError(MessageException):
    def __init__(self, message):
        super().__init__(message)

# issue reported by the `status` command, that's at the level of a nonfatal
# warning
class StatusWarning(MessageException):
    def __init__(self, message):
        super().__init__(message)
