import tkinter as tk
from tkinter import ttk
import pyperclip
import openai
import logging

# Configure OpenAI API Key
openai.api_key = "your_openai_api_key"  # Replace with your OpenAI API key

# Configure logger
logging.basicConfig(
    filename="log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_action(action_name, input_text, output_text):
    """Log actions to a file using Python's logging library."""
    logging.info(f"Action: {action_name}\nInput: {input_text}\nOutput: {output_text}\n{'-'*80}")


import requests


def translate_content(instruction, content):
    """
    Sends a translation request to the FastAPI server.

    Parameters:
        instruction (str): The instructions for the translation.
        content (str): The text content to be translated.

    Returns:
        str: The translated content with additional instructions appended,
             or an error message if something goes wrong.
    """

    # Define the URL of your running FastAPI application
    url = "http://127.0.0.1:8000/translate/"

    # Prepare the data payload with instruction and content
    data = {
        "instruction": instruction,
        "content": content
    }

    try:
        # Send a POST request to the FastAPI server
        response = requests.post(url, json=data)

        # Check if the request was successful
        response.raise_for_status()

        # Extract and return the translated content from the response
        translated_content = response.json().get("translated_content")
        return f"Translated Content: {translated_content}"

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

def send_to_gpt(action_name, prompt_template):
    """Send the input text (from Box A) to GPT with the given prompt template."""
    try:
        text = input_text_box.get("1.0", tk.END).strip()
        result = translate_content(prompt_template, text)
        # Copy result to clipboard and update UI
        pyperclip.copy(result)
        update_ui(text, result)
        log_action(action_name, text, result)

    except Exception as e:
        error_message = f"Error: {str(e)}"
        log_action(action_name, error_message, 'Error')
        update_ui(text, error_message)

def update_ui(input_text, output_text):
    """Update the input and output text boxes."""
    for box, text in [(input_text_box, input_text), (output_text_box, output_text)]:
        box.delete("1.0", tk.END)
        box.insert(tk.END, text or "Clipboard is empty!")

def add_action(button_name, prompt_template):
    """Add a new action button dynamically."""
    action_buttons.append({"name": button_name, "prompt": prompt_template})

def render_buttons():
    """Render buttons dynamically."""
    for button_info in action_buttons:
        ttk.Button(
            button_frame,
            text=button_info["name"],
            command=lambda n=button_info["name"], p=button_info["prompt"]: send_to_gpt(n, p)
        ).pack(pady=5, padx=10)

def fill_input_from_clipboard():
    """Automatically fill the input text box with clipboard content."""
    clipboard_content = pyperclip.paste().strip()
    update_ui(clipboard_content or "Clipboard is empty!", "")

# Initialize the Tkinter root
root = tk.Tk()
root.title("Clipboard Magic Tool")
root.geometry("1200x600")

main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=50, pady=25)

button_frame = ttk.Frame(main_frame)
button_frame.pack(side="left", fill="y", padx=10, pady=10)

text_frame = ttk.Frame(main_frame)
text_frame.pack(side="right", fill="both", expand=True, padx=50, pady=10)

# Input Text Display (Box A)
input_label = ttk.Label(text_frame, text="Input (Clipboard Content):")
input_label.grid(row=0, column=0, sticky="w")

input_text_box = tk.Text(text_frame, height=15, width=40, wrap="word")
input_text_box.grid(row=1, column=0, padx=5, pady=5)

# Output Text Display (Box B)
output_label = ttk.Label(text_frame, text="Output (GPT Response):")
output_label.grid(row=0, column=1, sticky="w")

output_text_box = tk.Text(text_frame, height=15, width=40, wrap="word")
output_text_box.grid(row=1, column=1, padx=10, pady=10)

# Action Buttons
action_buttons = []

# Predefined actions
actions = [
    ("A - Translate to Polish", "Translate the following English text to Polish:\n\n{input}"),
    ("B - Correct English", "Correct the following English text:\n\n{input}"),
    ("C - Correct & Explain", "Correct the following English text and provide detailed feedback:\n\n{input}"),
    ("D - create list", "create list of strings")
]

for name, template in actions:
    add_action(name, template)

# Render buttons
render_buttons()

# Fill input from clipboard on startup
fill_input_from_clipboard()

# Run the Tkinter main loop
root.mainloop()