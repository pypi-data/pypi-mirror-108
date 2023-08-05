################################################################################
#                                                                              #
#    This is the module which provides the basic helpers for this project.     #
#                                                                              #
#                    @author Jack <jack@thinkingcloud.info>                    #
#                                 @version 1.0                                 #
#                          @date 2021-05-31 13:53:26                           #
#                                                                              #
################################################################################

from os import path
from benedict import benedict
import importlib


def relative_path(p, file_name=None):
    """
    Get the absolute path of the file that relative to the first file
    """
    pp = path.abspath(path.dirname(p))
    if file_name:
        return path.join(pp, file_name)
    return pp


def load_class(name, package=None):
    names = name.split('.')
    n = '.'.join(names[:-1])
    if not package:
        package = __package__
    if n[0] == '.':
        mod = importlib.import_module(n, package=package)
    else:
        mod = importlib.import_module(n)

    clz = names[-1]
    m = mod
    if hasattr(m, clz):
        m = getattr(m, clz)
    else:
        m = None
    return m
