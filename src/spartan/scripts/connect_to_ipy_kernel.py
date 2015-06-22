# connect_to_ipy_kernel.py is part of the 'spartan' package.
# It was written by Gus Dunn and was created on 9/4/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
connect_to_ipy_kernel.py
=================================================
Purpose:
Manage exchanging security kernel info and connecting to remote ipython notebook.
"""
__author__ = 'Gus Dunn'
import sh
import json

# NOTE: this turned out not to require such a complicated solution.  But this may be useful at some point so I am not
# Killing it completely

class RemoteMachine(object):
    """
    Manages doing stuff on the remote machine through ssh.
    """
    def __init__(self, user, server, kernel_info_path, pub_key_path=None):
        """

        :param user:
        :param server:
        :param pub_key_path:
        :return:
        """
        self.user = user
        self.server = server
        self.pub_key = pub_key_path
        self.kernel_id = kernel_info_path
        self.kernel_data = None
        self.kernel_name = None

        try:
            # TODO: figure out how to test this HERE not later and find out if `ssh-copy-id yourservername` would help
            self.connection = sh.ssh.bake("%s@%s" % (self.user, self.server))
        except:
            raise

    def get_kernel_info(self):
        """
        Retrieves remote kernel info.
        :return:
        """

        self.kernel_data = json.loads(str(self.connection("cat %s" % self.kernel_id)))

        self.kernel_name = self.kernel_id.split('/')[-1]
        with open("~/.ipython/profile_default/security/%s" % self.kernel_name, 'w') as self.local_kernel_info:
            self.local_kernel_info.write(json.dumps(self.kernel_data, indent=2))

    def open_port_forwarding(self):
        """
        Opens correct ports in remote for forwarding.
        :return:
        """

        base_command = "ssh %(user)s@%(server)s -f -N -L %(port)s:%(ip)s:%(port)s"

        # open stdin_port
        sh.ssh(base_command
               % {"user": self.user,
                  "server": self.server,
                  "port": self.kernel_data.get("stdin_port"),
                  "ip": self.kernel_data.get("ip")})

        # open control_port
        sh.ssh(base_command
               % {"user": self.user,
                  "server": self.server,
                  "port": self.kernel_data.get("control_port"),
                  "ip": self.kernel_data.get("ip")})

        # open hb_port
        sh.ssh(base_command
               % {"user": self.user,
                  "server": self.server,
                  "port": self.kernel_data.get("hb_port"),
                  "ip": self.kernel_data.get("ip")})

        # open shell_port
        sh.ssh(base_command
               % {"user": self.user,
                  "server": self.server,
                  "port": self.kernel_data.get("shell_port"),
                  "ip": self.kernel_data.get("ip")})

        # open iopub_port
        sh.ssh(base_command
               % {"user": self.user,
                  "server": self.server,
                  "port": self.kernel_data.get("iopub_port"),
                  "ip": self.kernel_data.get("ip")})

    def start_notebook(self):
        """
        Start a notebook on the local machine.
        :return:
        """

        base_command = "notebook --existing %(kernel_name)s"
        fill_ins = {"kernel_name": self.kernel_name}

        sh.ipython(base_command % fill_ins)

