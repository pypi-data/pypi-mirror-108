class DiscListException(Exception):
    """
    The base class to all DiscList Error Exceptions.
    """

class Unauthorized(DiscListException):
    def __init__(self, message: str):
        """
        The Exception when you did not enter a specific data.
        """
        super().__init__(message)

class BotTokenRequired(Unauthorized):
    def __init__(self, message: str):
        """
        The Exception when you did not enter a bot token.
        """
        super().__init__("You must enter a bot token.")

class NotFound(DiscListException):
    def __init__(self, message: str):
        """
        The Exception when you did enter an invalid data.
        """
        super().__init__(message)

class InvalidToken(NotFound):
    def __init__(self):
        """
        The Exception when you did enter an invalid bot token.
        """
        super().__init__("You entered an invalid bot token.")