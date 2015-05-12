# *****************************************************************************
#  errors.py (part of the  package)
#
#  (c) 2013 - Augustine Dunn
#  James Laboratory
#  Department of Biochemistry and Molecular Biology
#  University of California Irvine
#  wadunn83@gmail.com
#
#  Licensed under the GNU General Public License 3.0 license.
# ******************************************************************************

"""
####################
errors.py
####################
Code defining custom base error classes to provide a foundation for graceful error handling.
"""
import warnings


class SpartanError(Exception):
    """Base class for exceptions in the blacktie package."""

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return """%s""" % self.msg


class SystemCallError(SpartanError):
    """Error raised when a problem occurs while attempting to run an external system call.

    Attributes:
        | ``errno`` -- return code from system call
        | ``filename`` -- file involved if any
        | ``strerror`` -- error msg """

    def __init__(self, errno, strerror, filename=None):
        self.errno = errno
        self.strerror = strerror
        self.filename = filename

    def __str__(self):
        if not self.filename:
            return """ERROR:\n %s.\nRETURN_STATE: %s.""" % (self.strerror.strip('\n'),
                                                            self.errno)
        else:
            return """ERROR in %s:\n %s.\nRETURN_STATE: %s.""" % (self.filename,
                                                                  self.strerror.strip('\n'),
                                                                  self.errno)


class SanityCheckError(SpartanError):
    """When a 'state check' comes back as conflicting or nonsensical."""


class UnexpectedValueError(SpartanError):
    """When values that "should" not be possible happen; like if a variable was changed unexpectedly."""


class InvalidFileFormatError(SpartanError):
    """When errors occur due to malformed file formats."""


class MissingArgumentError(SpartanError):
    """When a required argument is missing from the parsed command line options."""


class InvalidOptionError(SpartanError):
    """
    Raised when a constrained settable option fails its validity test.
    """
    def __init__(self, wrong_value, option_name, valid_values=None):
        """
        Provides standard format for error messages of this type.
        :param wrong_value: Value encountered
        :param option_name: Name of option
        :param valid_values: iterable of valid values
        """
        self.wrong_value = wrong_value
        self.option_name = option_name
        self.valid_values = valid_values

    def __str__(self):
        if self.valid_values:
            return """%s is not a valid value for arg:%s.\n\tValid values are: %s""" % (
                self.wrong_value, self.option_name, self.valid_values)
        else:
            return """%s is not a valid value for arg:%s.""" % (self.wrong_value, self.option_name)


class IgnoreThisError(SpartanError):
    """
    Raised when a function sees a value that does not match what is expected but should not cause the code to die.
    Useful for parsers that may need to ignore 'commented' lines or malformed but 'harmless' text.
    When caught, `spartan` functions should handle by gracefully ignoring that run of the function.
    """

    # def __init__(self, msg):
    #     self.msg = msg


class FixMeError(SpartanError):
    """
    Raised when a function is called that has been identified as functionally bankrupt and running of said function
    deemed too risky to allow without someone's attention used to fix it.
    """
