import uuid
from dateutil.parser import ParserError
from time import sleep
from .general_runtime_vars import env_vars
from pytz import timezone
from dateutil import parser


def generate_guid():
    return str(uuid.uuid1())


def parse_headers(msg_header):
    """
    Converts headers to a dict
    :param msg_header: A message .headers() (confluent) or .headers (faust) instance
    :return: a decoded dict version of the headers
    """
    if msg_header:
        msg_header = dict(msg_header)
        return {key: value.decode() for key, value in msg_header.items()}
    return {}


def log_and_raise_error(metrics_manager, error):
    """
    Since the metric manager pushing is a separate thread, ensure an exception gets sent to prometheus
    """
    metrics_manager.inc_message_errors(error)
    sleep(int(env_vars()['METRICS_PUSH_RATE']) * 2 + 1)
    raise


def universal_datetime_converter(incoming_datetime, incoming_timezone=timezone("Etc/UTC")):
    """
    Converts datetime values of all kinds into a normalized format
    If provided, timezone must be passed in as a pytz.timezone type
    Accepts string and datetime types
    Assumes UTC if no timezone is provided
    Assumes midnight if datetime does not include time
    Returns empty string if datetime cannot be parsed
    """
    try:
        datetime_to_convert = parser.parse(str(incoming_datetime))
    except ParserError:
        return ""

    if datetime_to_convert.tzinfo is None or datetime_to_convert.tzinfo.utcoffset(datetime_to_convert) is None:
        datetime_to_convert = incoming_timezone.localize(datetime_to_convert)

    with_offset_for_given_timezone = incoming_timezone.normalize(datetime_to_convert)
    datetime_to_convert = with_offset_for_given_timezone.astimezone(timezone("Etc/UTC"))

    converted_datetime = datetime_to_convert.strftime('%Y-%m-%dT%H:%M:%SZ')
    return converted_datetime
