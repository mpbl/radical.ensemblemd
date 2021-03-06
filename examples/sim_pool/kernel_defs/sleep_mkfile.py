#!/usr/bin/env python

"""A kernel that creates a new ASCII file with a given size and name.
"""

__author__    = "The ExTASY project <ardita.shkurti@nottingham.ac.uk>"
__copyright__ = "Copyright 2015, http://www.extasy-project.org/"
__license__   = "MIT"

from copy import deepcopy

from radical.ensemblemd.exceptions import ArgumentError
from radical.ensemblemd.exceptions import NoKernelConfigurationError
from radical.ensemblemd.engine import get_engine
from radical.ensemblemd.kernel_plugins.kernel_base import KernelBase

# ------------------------------------------------------------------------------
#
_KERNEL_INFO = {
    "name":         "custom.sleep_mkfile",
    "description":  "Performs the preprocessing necessary for the following MD simulation. ",
    "arguments":    {"--maxsleep=":
                        {
                            "mandatory": True,
                            "description": "Max sleep"
                        },

                        "--upperlimit=": 
                        {
                            "mandatory": True,
                            "description": "The upper limit of the random value."
                        },

                        "--filename=": 
                        {
                            "mandatory": True,
                            "description": "Output filename."
                        }
                    },
    "machine_configs":
    {
        "*": {
            "environment"   : {"FOO": "bar"},
            "pre_exec"      : [],
            "executable"    : "/bin/bash",
            "uses_mpi"      : False
        },
    }
}


# ------------------------------------------------------------------------------
#
class kernel_sleep_mkfile(KernelBase):

    # --------------------------------------------------------------------------
    #
    def __init__(self):
        """Le constructor.
        """
        super(kernel_sleep_mkfile, self).__init__(_KERNEL_INFO)

    # --------------------------------------------------------------------------
    #
    @staticmethod
    def get_name():
        return _KERNEL_INFO["name"]

    # --------------------------------------------------------------------------
    #
    def _bind_to_resource(self, resource_key):
        """(PRIVATE) Implements parent class method.
        """
        if resource_key not in _KERNEL_INFO["machine_configs"]:
            if "*" in _KERNEL_INFO["machine_configs"]:
                # Fall-back to generic resource key
                resource_key = "*"
            else:
                raise NoKernelConfigurationError(kernel_name=_KERNEL_INFO["name"], resource_key=resource_key)

        cfg = _KERNEL_INFO["machine_configs"][resource_key]

        arguments  = ["-c","'sleep $[ ( $RANDOM % {2} ) ] && echo $[ 1 + $[ RANDOM % {0} ]] > {1}'".format(
                self.get_arg("--upperlimit="),
                self.get_arg("--filename="),
                self.get_arg("--maxsleep="))
                ]

        self._executable  = cfg["executable"]
        self._arguments   = arguments
        self._environment = cfg["environment"]
        self._uses_mpi    = cfg["uses_mpi"]
        self._pre_exec    = None
