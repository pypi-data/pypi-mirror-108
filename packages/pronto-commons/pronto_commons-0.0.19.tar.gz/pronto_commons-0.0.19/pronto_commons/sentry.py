from sentry_sdk import capture_exception

from pronto_commons.exceptions import BusinessException


def log_exception(
    *, exception: Exception, force_capture_business_exception: bool = False
) -> None:

    if isinstance(exception, BusinessException):
        if force_capture_business_exception:
            capture_exception(exception)
        return
    capture_exception(exception)
