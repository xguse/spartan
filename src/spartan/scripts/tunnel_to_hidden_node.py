# tunnel_to_hidden_node.py is part of the 'spartan' package.
# It was written by Gus Dunn and was created on 9/7/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
tunnel_to_hidden_node.py
=================================================
Purpose:
Provide automated way to tunnel one or more ports between local machine and a node hidden on a remote cluster.

"""
__author__ = 'Gus Dunn'

from spartan.utils.externals import run_external_app


class Tunnel(object):
    """
    Manages connection and breakdown of ssh port tunnel.
    Assumes passwordless login.
    """

    def __init__(self, user, visible_server, hidden_server, local_port, remote_port):
        """
        Initializes Tunnel object with needed info.

        :param user: Your user name on `visible_server`.
        :param visible_server: fully qualified address of the login server.
        :param hidden_server: machine name of the hidden node.
        :param local_port: port you will point your LOCAL browser etc to when communicating with the hidden node.
        :param remote_port: port that the hidden node will be communicating on.
        :return: initialized Tunnel Obj
        """

        self.user = user
        self.visible_server = visible_server
        self.hidden_server = hidden_server
        self.local_port = local_port
        self.remote_port = remote_port
        self.connection_result = None
        self.process = None

    # def __enter__(self):
    #     return self
    #
    # def __exit__(self, exc_type, exc_val, exc_tb):


    def _build_command(self):
        """
        Returns constructed `ssh` argument string.
        :return:
        """

        cmd_str = "-f -N -L %(local_port)s:%(hidden_server)s:%(remote_port)s %(user)s@%(visible_server)s"
        cmd_vals = {"local_port": self.local_port,
                    "hidden_server": self.hidden_server,
                    "remote_port": self.remote_port,
                    "user": self.user,
                    "visible_server": self.visible_server}

        return cmd_str % cmd_vals

    def open_tunnel(self):
        """
        Opens ssh tunnel and stores subprocess Popen instance in `self.process`.
        :return:
        """

        ssh_cmd = self._build_command()
        self.process = run_external_app("ssh", ssh_cmd)
