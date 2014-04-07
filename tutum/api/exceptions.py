class TutumApiError(Exception):
    """An error status code was returned when querying the HTTP API"""
    pass


class TutumAuthError(TutumApiError):
    """An 401 Unauthorized status code was returned when querying the API"""
    pass