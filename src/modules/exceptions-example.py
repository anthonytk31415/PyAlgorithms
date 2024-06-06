def exceptionFn(x):
    try:
        # Check if x is zero to avoid ZeroDivisionError
        if x == 0:
            raise ZeroDivisionError("x cannot be zero")
        # Perform the division
        result = 1 / x

    except ZeroDivisionError:
        print("x cannot be zero (division by zero)")

    except TypeError:
        print("you have a type error")

    except Exception as e:
        print(f"Error: {e}")

    else:
        print(result)
        return result

    return 0

exceptionFn(0)
exceptionFn("a string is fed")