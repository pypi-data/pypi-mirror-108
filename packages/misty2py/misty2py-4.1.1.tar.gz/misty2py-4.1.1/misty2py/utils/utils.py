"""Utility functions that do not fit anywhere else."""
from typing import Any, Dict, Type


def query_dict_with_fallback(
    data: Dict, query: str, fallback: Any, required_type: Type = None
) -> Any:
    """Safely queries a dictionary, returns the queried value if it passes type check and the fallback otherwise.

    Args:
        data (Dict): the dictionary to query.
        query (str): the query.
        fallback (Any): the fallback value to return if the key does not exist or the queried value does not pass the type check.
        required_type (Type, optional): The required type of the queried value. None if there is no required type. Defaults to None.

    Returns:
        Any: the query result.
    """
    result = data.get(query)

    if result is None:
        return fallback

    if not required_type is None:
        if not isinstance(result, required_type):
            return fallback

    return result
