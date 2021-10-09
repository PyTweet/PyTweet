class Unauthorized(Exception):
    """Raised when the api-key is invalid!"""
    pass

class NotFoundError(Exception):
    """Raised when it cant find the object in some functions."""
    pass

class MissingCredentials(Exception):
    """Raised upon using function that needed certain Credentials like consumer_key or consumer_key_secret"""
    pass

