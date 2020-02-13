"""Utils methods"""
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
    