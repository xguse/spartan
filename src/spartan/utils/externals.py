#*****************************************************************************
#  externals.py (part of the spartan package)
#
#  (c) 2013 - Augustine Dunn
#  James Laboratory
#  Department of Biochemistry and Molecular Biology
#  University of California Irvine
#  wadunn83@gmail.com
#
#  Licensed under the GNU General Public License 3.0 license.
#******************************************************************************

"""
####################
externals.py
####################
Code facilitating the execution of external system calls.
"""


import subprocess
import shlex
import os
import sys

from spartan.utils.errors import *

# ++++++++ Verifying/preparing external environment ++++++++
def whereis(program):
    """
    returns path of program if it exists in your ``$PATH`` variable or ``None`` otherwise
    """
    for path in os.environ.get('PATH', '').split(':'):
        if os.path.exists(os.path.join(path, program)) and not os.path.isdir(os.path.join(path, program)):
            return os.path.join(path, program)
    return None

def mkdirp(path):
    """
    Create new dir while creating any parent dirs in the path as needed.
    """

    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except OSError as errTxt:
            if "File exists" in errTxt:
                sys.stderr.write("FYI: %s" % (errTxt))
            else:
                raise
            
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def run_external_app(prog_name, arg_str, ret_val='result'):
    """
    Convenience func to handle calling and monitoring output of external programs.
    

    :param prog_name: name of system program command
    :param arg_str: string containing command line options for ``prog_name``
    :param ret_val: `['result', 'process']`
            `'result'`: `tuple (stdout, stderr)`
            `'process'`: `Popen` instance after it has communicated.
    
    :returns:
    """

    ret_val_options = ["result", "process"]
    if ret_val not in ret_val_options:
        msg = "Invalid `ret_val` value: %s. Valid options are: %s" % (ret_val, str(ret_val_options))
        raise ValueError(msg)
    
    # Ensure program is callable.
    prog_path = whereis(prog_name)
    if not prog_path:
        raise SystemCallError(None, '"%s" command not found in your PATH environmental variable.' % (prog_name))
    
    # Construct shell command
    cmd_str = "%s %s" % (prog_path, arg_str)
    
    # Set up process obj
    process = subprocess.Popen(cmd_str,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    # Get results
    result = process.communicate()
    
    # Check returncode for success/failure
    if process.returncode != 0:
        raise SystemCallError(process.returncode, result[1], prog_name)

    if ret_val == "result":
        # Return result
        return result
    elif ret_val == "process":
        return process

