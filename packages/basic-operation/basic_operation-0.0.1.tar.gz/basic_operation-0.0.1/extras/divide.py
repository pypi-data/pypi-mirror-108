def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("La variable denominateur est egale a 0.")
    else:
        return result
