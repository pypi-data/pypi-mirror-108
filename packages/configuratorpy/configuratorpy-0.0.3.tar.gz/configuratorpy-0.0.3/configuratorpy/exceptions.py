################################################################################
#                                                                              #
#                      This is the module for exceptions                       #
#                                                                              #
#                    @author Jack <jack@thinkingcloud.info>                    #
#                                 @version 1.0                                 #
#                          @date 2021-05-31 14:32:15                           #
#                                                                              #
################################################################################


class BaseException(Exception):
    pass


class ConfigException(BaseException):
    pass


class ConfigNotExistsException(ConfigException):
    pass

class ConfigNotLoadException(ConfigException):
    pass
