class Unauthorized(Exception):
    "Raised when the api-key is invalid!"
    pass

class UserNotFound(Exception):
    "Raised when it cant find the right user in get_user functions"
    pass