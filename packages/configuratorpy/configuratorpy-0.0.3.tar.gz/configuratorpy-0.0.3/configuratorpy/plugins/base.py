################################################################################
#                                                                              #
#                           This is the base plugin                            #
#                                                                              #
#                    @author Jack <jack@thinkingcloud.info>                    #
#                                 @version 1.0                                 #
#                          @date 2021-05-31 15:45:04                           #
#                                                                              #
################################################################################

from abc import abstractproperty


class Plugin:
    @abstractproperty
    def provides(self):
        pass
