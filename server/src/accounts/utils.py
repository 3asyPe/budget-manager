from app.utils import get_upload_image_path
import enum


def get_user_upload_image_path(*args, **kwargs):
    return get_upload_image_path(*args, **kwargs, prefix="users")


class AccountErrorMessages(enum.Enum):
    TOO_LONG_EMAIL_ERROR = "TOO_LONG_EMAIL_ERROR"
    NON_UNIQUE_EMAIL_ERROR = "NON_UNIQUE_EMAIL_ERROR"
    INCORRECT_PASSWORD_SCHEME_ERROR = "INCORRECT_PASSWORD_SCHEME_ERROR"

    DISABLED_ACCOUNT_ERROR = "DISABLED_ACCOUNT_ERROR"
    CREDENTIALS_ERROR = "CREDENTIALS_ERROR"
    REQUEST_FIELDS_ERROR = "REQUEST_FIELDS_ERROR"

    USER_IS_NOT_AUTHENTICATED_ERROR = "USER_IS_NOT_AUTHENTICATED_ERROR"