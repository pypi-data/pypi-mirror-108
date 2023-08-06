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
from liquid import tag_manager, Tag


def load_env(path=None):
    load_dotenv(verbose=True, dotenv_path=path)


def env(key, default=''):
    return os.getenv(key, default=default)


class TagLoadEnv(Tag):
    VOID = True
    RAW = False
    START = 'tag_loadenv'
    GRAMMAR = '''
    tag_loadenv: string
    '''

    def _render(self, local_vars, global_vars):
        p = self.parsed.children[0]
        load_env(p)
        return ''


class EnvironmentPlugin(Plugin):
    @property
    def tags(self):
        return {'loadenv': TagLoadEnv}

    @property
    def provides(self):
        return {'env': env}
