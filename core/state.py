import logging


class RoverState:
    """
    A state class abstraction which serves as part of the state machine
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Starting state: {str(self)}")

    async def run(self):
        pass

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__class__.__name__

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return str(self) != str(other)
