################################################################################
#                                                                              #
#      This is the plugin which will provide the functions for sequences       #
#                                                                              #
#                    @author Jack <jack@thinkingcloud.info>                    #
#                                 @version 1.0                                 #
#                          @date 2021-06-02 11:41:53                           #
#                                                                              #
################################################################################

import os
from .base import Plugin
from dotenv import load_dotenv
from contextlib import suppress
from liquid.nodes import NodeVoid, register_node
from liquid.defaults import LIQUID_RENDERED_APPEND
from liquid.exceptions import LiquidSyntaxError, LiquidCodeTagExists

seqs = {}


class NodeUUID(NodeVoid):
    def parse_node(self):
        # log the parsing process
        super().parse_node()

        # let us just do a simple version, using subprocess.check_output
        # import the module, since this module will be import just once,
        # so we put it in the shared_code
        with suppress(LiquidCodeTagExists), \
                self.shared_code.tag('import_uuid') as tagged:
            tagged.add_line("import uuid")

        # use it to parse the command
        # save the result to a variable first
        # add id here to avoid conflicts
        self.code.add_line(f"command_{id(self)} = uuid.uuid4()")
        # put the results in rendered content
        self.code.add_line(f"{LIQUID_RENDERED_APPEND}(command_{id(self)})")


def seq(name):
    global seqs
    if name not in seqs:
        seqs[name] = 0
    seqs[name] += 1
    return seqs[name]


class SequencePlugin(Plugin):
    def __init__(self):
        register_node("uuid", NodeUUID)

    @property
    def provides(self):
        return {'seq': seq}
