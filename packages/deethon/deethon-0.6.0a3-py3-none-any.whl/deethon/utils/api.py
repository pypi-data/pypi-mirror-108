from ..errors import DeezerApiError


def raise_if_error(body: dict):
    if "error" in body:
        error = body["error"]
        raise DeezerApiError(
            error["type"],
            error["message"],
            error["code"]
        )
