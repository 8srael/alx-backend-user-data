#!/usr/bin/env python3

"""Task 0. Regex-ing"""


import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        obf_message = re.sub(field + "=.*?" + separator,
                         field + "=" + redaction + separator, message)
    return obf_message
