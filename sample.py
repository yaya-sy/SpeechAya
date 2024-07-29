def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "Division by zero error"


def main():
    print("Addition of 5 and 3 is: ", add(5, 3))
    print("Subtraction of 5 and 3 is: ", subtract(5, 3))
    print("Multiplication of 5 and 3 is: ", multiply(5, 3))
    print("Division of 5 by 3 is: ", divide(5, 3))
    print("Division of 5 by 0 is: ", divide(5, 10))


if __name__ == "__main__":
    main()
