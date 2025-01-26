def dynamic_input(prompt):
    inp = input(prompt)
    try:
        return int(inp)
    except ValueError:
        try:
            return float(inp)
        except ValueError:
            return inp

print( "Welcome to the PenguinBubble Calculator!")
while (True):
    print( "Choose an operation:")
    choice = dynamic_input("Enter your choice: ")
print(nguinSay "Exiting the calculator. Goodbye!")
print(nSay "You entered choice: " + str(choice))