from abc import ABC, abstractmethod

class BasePlugin(ABC):
    """
    Abstract base class for all workflow plugins.
    """
    @property
    @abstractmethod
    def command_name(self):
        """The command name this plugin registers."""
        pass