"""Message parsing utility functions."""
from typing import Dict, Optional


def message_parser(
    data: Dict,
    success_message: str = "Operation successful.",
    fail_message: str = "Operation failed.",
) -> str:
    """Parses a message from misty2py json Dict reply to a string.

    Args:
        data (Dict): json Dict to parse.
        message_if_success (str, optional): Brief success-indicating message / keyword. Defaults to "Operation successful.".
        message_if_fail (str, optional): Brief failure-indicating message / keyword. Defaults to "Operation failed.".

    Returns:
        str: Brief success-or-failure-indicating sentence / keyword and detailed information in the next sentence if available.
    """
    potential_message = data.get("message")
    if data.get("status") == "Success":
        return compose_str(success_message, potential_message)
    return compose_str(
        fail_message, potential_message, fallback="No further details provided."
    )


def compose_str(
    main_str: str, potential_str: Optional[str], fallback: Optional[str] = None
) -> str:
    """Composes a string from main_str, potential_str and fallback.

    Args:
        main_str (str): the main string.
        potential_str (Optional[str]): data that may be a string or None.
        fallback (Optional[str], optional): a string to attach to main_str if potential_str is not a string. None if nothing should be attached. Defaults to None.

    Returns:
        str: main_str if potential_str and fallback are None. main_str followed by a space and potential_str if potential_str is a string. main_str followed by a space and fallback if potential_str is None and fallback is a string.
    """
    if isinstance(potential_str, str):
        return "%s %s" % (main_str, potential_str)
    if isinstance(fallback, str):
        return "%s %s" % (main_str, fallback)
    return main_str
