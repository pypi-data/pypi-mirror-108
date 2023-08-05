# miscset.dt


"""Date and time methods."""


import datetime


def format(dt, fmt = "dt", simplified = True):
    """Format a datetime object.
    
    Args:
        dt (datetime.datetime): A datetime object to format to a string.
        fmt (string): A date/time format to apply, one of:
            "dt" aka date and time -> YYYY-MM-DD HH:MM:SS
            "d"  aka date          -> YYYY-MM-DD
            "t"  aka time          -> HH:MM:SS
            "f"  aka file name     -> YYYY-MM-DD_HH-MM-SS
            "n"  aka numbers       -> YYYYMMDDHHMMSS
        simplified (boolean): True to expand the `fmt` from a simplified encoding;
            otherwise use the formats supported by datetime's `strftime` method.
        tz (None): Ignored.
    
    Returns:
        (string): The datetime object converted to a string, as done by datetime's `strftime` method.
    """
    if simplified:
        fmt = fmt.lower()
        if fmt == "dt":
            fmt = "%Y-%m-%d %H:%M:%S"
        elif fmt == "d":
            fmt = "%Y-%m-%d"
        elif fmt == "t":
            fmt = "%H:%M:%S"
        elif fmt == "f":
            fmt = "%Y-%m-%d_%H-%M-%S"
        elif fmt == "n":
            fmt = "%Y%m%d%H%M%S"
        else:
            fmt = ""
    return dt.strftime(fmt)
    

def now(fmt = "dt", simplified = True):
    """Obtain the current time as string.

    Args:
        fmt (string): A date/time format defined in `format`.
        simplified (boolean): See `format`.
    
    Returns:
        (string): The current time formatted as string.
    """
    dt = datetime.datetime.now()
    return format(dt, fmt, simplified)

