import re

ACCEPTABLE_PATTERN = r"¥?\d{1,3}((,{1}\d{3})*|\d*)"
acceptable_pattern = re.compile(ACCEPTABLE_PATTERN, re.ASCII)

REPLACE_PATTERN = r"¥|,"
replace_pattern = re.compile(REPLACE_PATTERN)


def parse_yen(s: str):
    """
    Parse yen string to number.

    Parameters
    ----------
    s: str
        Only accept following formats.::

            "1234" # only number
            "1,234" # with comma
            "¥1234" # with yen mark
            "¥1,234" # with comma and yen mark

    Returns
    -------
    int

    Raises
    ------
    TypeError
        Non string value specified.
    ValueError
        A string in not acceptable format specified.
    """
    if not acceptable_pattern.fullmatch(s):
        raise ValueError()

    s = replace_pattern.sub('', s)
    return int(s)
