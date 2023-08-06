################################################################################
#                                                                              #
#               This is the test module for testing configurator               #
#                                                                              #
#                    @author Jack <jack@thinkingcloud.info>                    #
#                                 @version 1.0                                 #
#                          @date 2021-05-31 14:35:49                           #
#                                                                              #
################################################################################

from configuratorpy import *
import logging

logger = logging.getLogger(__name__)


def test_init_fail():
    try:
        c = Configurator()
        assert False, 'We should have an exception'
    except ConfigNotExistsException:
        pass


def test_init_fail_with_directory():
    try:
        c = Configurator(directory=relative_path(__file__, 'data'),
                         name='nothing.toml')
        assert False, 'We should have an exception'
    except ConfigNotExistsException:
        pass


def test_init_success():
    try:
        c = Configurator(directory=relative_path(__file__, 'data'))
    except ConfigNotExistsException:
        assert False, 'File not found'


def test_load():
    try:
        c = Configurator(directory=relative_path(__file__, 'data'))
        c.load()
        assert c['test'] == 1, 'Load failed'
        assert c['section.sub.a'] == 1, 'Load failed'
        assert c['section/sub/*'] == [1, 2, 3], 'Search Failed'
        assert c['section/sub/a'] == 1, 'Load failed'
        assert c.sub('section')['a'] == 1, 'Sub failed'
        assert c['seq_*'] == list(i + 1
                                  for i in range(5)), 'Sequence is not working'
    except ConfigNotExistsException:
        assert False, 'File not found'
