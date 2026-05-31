def is_int(value):
    try:
        int(value)
    except ValueError:
        return False
    return True
    

def is_digit(amt):
    try:
        float(amt)
    except ValueError:
        return False
    return True


def is_positive_int(value, zero_inclusive=False):
    return is_int(value) and is_positive(value, zero_inclusive)
    

def is_positive(amt, zero_inclusive=False):
    try:
        amt = float(amt)
    except ValueError:
        return False
    else:
        return amt >= 0 if zero_inclusive else amt > 0
