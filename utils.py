"""Utils methods"""
from datetime import datetime
from decimal import Decimal


def float_to_decimal(float_value):
    """Convert float value to decimal 2 places"""
    TWOPLACES = Decimal(10) ** -2
    return Decimal(float_value).quantize(TWOPLACES)

def post_params_is_valid(params, required_params):
    """Check all required params is present in params"""
    for param in required_params:
        if not param in params.keys():
            return False
    return True

def set_value_if_exist(params, param, object):
    """If param, set value in object"""
    if param in params:
        setattr(object, param, params[param])

def str_date_to_date(str_date):
    """Convert date string to date"""
    try:
        return datetime.strptime(str_date, "%Y-%m-%d")
    except:
        return None

def date_to_str_date(date):
    """Convert date to date string"""
    try:
        return date.strftime("%Y-%m-%d")
    except:
        return None
    