class UserError(Exception):
    """The user has done something wrong and we should return a 4xx error"""

    pass


class CSRFError(Exception):
    """The CSRF Token didn't match"""

    pass
