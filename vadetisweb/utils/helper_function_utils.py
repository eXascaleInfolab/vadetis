def convertStrToBoolean(s):
    if s == 'True' or s == 'true':
        return True
    elif s == 'False' or s == 'false':
        return False
    else:
        raise ValueError


def replaceEmptyStrWithNone(str):
    if not str:
        return None
    else:
        try:
            val = int(str)
            return val
        except:
            pass
        return None


def isValidSelection(selected_val, possibleSelectionTuple):
    if (selected_val, selected_val) in possibleSelectionTuple:
        return True

    return False


def isBoolean(val):
    return isinstance(val, bool)


def isNone(val):
    if val == None:
        return True
    return False


def convertToFloat(str):
    try:
        val = float(str)
        return val
    except:
        pass
        return None


def convertToInt(str):
    try:
        val = int(str)
        return val
    except:
        pass
        return None


def isFloatInRange(low, high, value):
    if low < value < high:
        return True
    return False


def isFloatInNuRange(value):
    if 0 < value <= 1:
        return True
    return False


def isPositiveInteger(number):
    try:
        val = int(number)
        if val < 1:
            print("Input must be a positive integer")
            return False
        else:
            return True
    except:
        pass
        return False
