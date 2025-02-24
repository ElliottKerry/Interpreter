import tkinter as tk
from lexer import Tokenizer
from parser import Parser
from interpreter import Interpreter

def run_program():
    # Get the full text from the editor.
    source = text_editor.get("1.0", tk.END).strip()
    if not source:
        return
    try:
        # Tokenize, parse, and evaluate your custom language.
        tokenizer = Tokenizer(source)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse_program()
        result = interpreter.evaluate(ast)
        # Append the source code and result to the output history.
        output_text.insert(tk.END, f">>> {source}\n")
        output_text.insert(tk.END, f"{result}\n")
        output_text.insert(tk.END, "-" * 50 + "\n")
        # Scroll to the end to show the latest output.
        output_text.see(tk.END)
    except Exception as e:
        output_text.insert(tk.END, f"Error: {e}\n")
        output_text.insert(tk.END, "-" * 50 + "\n")
        output_text.see(tk.END)

# Set up the main window.
root = tk.Tk()
root.title("MyLang Editor with History")

# Create a single interpreter instance.
interpreter = Interpreter()

# Text widget for entering your language code.
text_editor = tk.Text(root, wrap="word", height=10, width=80)
text_editor.pack(pady=10)

# Button to run the entered code.
run_button = tk.Button(root, text="Run Code", command=run_program)
run_button.pack(pady=5)

# Text widget for displaying the output history.
output_text = tk.Text(root, wrap="word", height=15, width=80, bg="#f0f0f0")
output_text.pack(pady=10)

root.mainloop()
# The code above creates a simple Tkinter GUI application that allows you to write code in a custom language and see the output in a history window. The code uses the Tokenizer, Parser, and Interpreter classes from the previous snippets to tokenize, parse, and evaluate the code entered by the user.