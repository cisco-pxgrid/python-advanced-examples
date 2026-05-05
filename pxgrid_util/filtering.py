import argparse
import jmespath
from jmespath.exceptions import JMESPathError


def validate_filter_syntax(filter_value):
    if filter_value is None:
        return None
    try:
        jmespath.compile(filter_value)
    except JMESPathError as exc:
        raise ValueError(f"invalid JMESPath filter syntax: {exc}") from exc
    return filter_value


def argparse_filter(filter_value):
    try:
        return validate_filter_syntax(filter_value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc))


def build_query_payload(start_timestamp=None, filter_value=None):
    payload = {}
    if start_timestamp:
        payload["startTimestamp"] = start_timestamp
    if filter_value:
        payload["filter"] = filter_value
    return payload
