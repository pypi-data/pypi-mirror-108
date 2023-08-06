# __init__.py
from tgcf.plugins import TgcfPlugin


class TgcfHello(TgcfPlugin):
    id = "hello"
    # the plugin class must have this `id` attribute

    def __init__(self, data):
        # the plugin class must have a constructor and should validate data here
        self.data = data

    def modify(self, message):
        # the modify method, receives the message collected by tgcf
        # the output of this method will be forwarded
        message = "hello " + message
        # manipulate the message here
        return message