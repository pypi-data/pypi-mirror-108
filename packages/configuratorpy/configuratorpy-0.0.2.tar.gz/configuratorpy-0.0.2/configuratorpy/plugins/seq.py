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
from liquid import tag_manager, Tag
import uuid

seqs = {}


class TagUUID(Tag):
    VOID = True

    def _render(self, local_vars, global_vars):
        return str(uuid.uuid4())


def seq(name):
    global seqs
    if name not in seqs:
        seqs[name] = 0
    seqs[name] += 1
    return seqs[name]


class SequencePlugin(Plugin):
    @property
    def tags(self):
        return {'uuid': TagUUID}

    @property
    def provides(self):
        return {'seq': seq}
