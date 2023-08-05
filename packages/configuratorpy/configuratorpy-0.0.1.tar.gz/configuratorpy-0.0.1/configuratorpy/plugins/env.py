################################################################################
#                                                                              #
#                 This is the plugin for environment variables                 #
#                                                                              #
#                    @author Jack <jack@thinkingcloud.info>                    #
#                                 @version 1.0                                 #
#                          @date 2021-05-31 15:33:20                           #
#                                                                              #
################################################################################

import os
from .base import Plugin
from dotenv import load_dotenv
from contextlib import suppress
from liquid.nodes import NodeVoid, register_node
from liquid.defaults import LIQUID_RENDERED_APPEND
from liquid.exceptions import LiquidSyntaxError, LiquidCodeTagExists


def load_env(path=None):
    load_dotenv(verbose=True, dotenv_path=path)


def env(key, default=''):
    return os.getenv(key, default=default)


class NodeLoadEnv(NodeVoid):
    def start(self):
        if not self.attrs:
            raise LiquidSyntaxError("No configuration file!", self.context)

    def parse_node(self):
        # log the parsing process
        super().parse_node()
        p = self.attrs.replace("'", '')
        load_env(p)


class EnvironmentPlugin(Plugin):
    def __init__(self):
        register_node("load_env", NodeLoadEnv)

    @property
    def provides(self):
        return {'env': env}
