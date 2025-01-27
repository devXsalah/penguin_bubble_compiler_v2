def dynamic_input(prompt):
    inp = input(prompt)
    try:
        return int(inp)
    except ValueError:
        try:
            return float(inp)
        except ValueError:
            return inp

print("Welcome to the PenguinBubble Calculator!")
def addOperation(x, y):
    return x + y
def subOperation(x, y):
    return x - y
def mulOperation(x, y):
    return x * y
def divOperation(x, y):
    return x / y
def powOperation(x, y):
    return x ** y
while (True):
    print("Choose an operation:")
    print("1 -> Addition")
    print("2 -> Subtraction")
    print("3 -> Multiplication")
    print("4 -> Division")
    print("5 -> Exponentiation")
    print("6 -> Exit")
    choice = dynamic_input("Enter your choice: ")
    if (choice == 6):
        print("Exiting the calculator. Goodbye!")
        break 
    num1 = dynamic_input("Enter the first number: ")
    num2 = dynamic_input("Enter the second number: ")
    if (choice == 1):
        result = addOperation(num1, num2)
        print("Result: " + str(result))
    elif (choice == 2):
        result = subOperation(num1, num2)
        print("Result: " + str(result))
    elif (choice == 3):
        result = mulOperation(num1, num2)
        print("Result: " + str(result))
    elif (choice == 4):
        result = divOperation(num1, num2)
        print("Result: " + str(result))
    elif (choice == 5):
        result = powOperation(num1, num2)
        print("Result: " + str(result))
    else :
        print("Invalid choice. Please try again.")