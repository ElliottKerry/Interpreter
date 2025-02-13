def repl():
    while True:
        try:
            user_input = input("PyLox> ")  # Read user input
            if user_input.strip().lower() == "exit":
                break  # Exit when user types "exit"
            print("You typed:", user_input)  # Echo the input
        except EOFError:
            break  # Exit on Ctrl+D (EOF)

# Run the REPL
if __name__ == "__main__":
    repl()
H