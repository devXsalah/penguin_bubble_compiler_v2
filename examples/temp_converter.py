def dynamic_input(prompt):
    inp = input(prompt)
    try:
        return int(inp)
    except ValueError:
        try:
            return float(inp)
        except ValueError:
            return inp

print("Welcome to the PenguinTemp Converter!")
def celsiusToFahrenheit(celsius):
    return celsius * 1.8 + 32
def fahrenheitToCelsius(fahrenheit):
    return fahrenheit - 32 / 1.8
while (True):
    print("Choose conversion:")
    print("1 -> Celsius to Fahrenheit")
    print("2 -> Fahrenheit to Celsius")
    print("3 -> Exit")
    choice = dynamic_input("Enter your choice: ")
    if (choice == 3):
        print("Stay warm, goodbye!")
        break
    if (choice == 1):
        temp = dynamic_input("Enter temperature in Celsius: ")
        result = celsiusToFahrenheit(temp)
        print(str(temp) + "°C is " + str(result) + "°F")
    elif (choice == 2):
        temp = dynamic_input("Enter temperature in Fahrenheit: ")
        result = fahrenheitToCelsius(temp)
        print(str(temp) + "°F is " + str(result) + "°C")
    else : 
        print("Invalid choice! Try again.")