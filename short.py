import time

import pyperclip
import json
import pyautogui
# from textblob import TextBlob

def clipboard_to_json():
    try:
        text = pyperclip.paste()
        json_data = json.dumps({"text": text}, indent=4)
        pyperclip.copy(json_data)
        pyautogui.alert("Data transformed into JSON and copied to clipboard.", "Success")
    except Exception as e:
        pyautogui.alert(f"Error: {e}", "Error")

def convert_text_int_json_part(clipboard_content):
    parsed_content = clipboard_content.replace(' ', '').replace('\r', '')
    elements = clipboard_content.split('\n')

    parsed_content = {"data": elements}
    print(parsed_content)
    formatted_json = json.dumps(parsed_content, indent=4)

    # Print the formatted JSON
    print(formatted_json)
    return formatted_json

def clipboard_to_json_and_paste():
    try:
        # Get the current clipboard content
        clipboard_content = pyperclip.paste()
        # Attempt to parse it as JSON if it's already JSON-like
        formatted_json = convert_text_int_json_part("""a
b
c
d
f""")
        # Convert to a pretty-printed JSON string
        # json_content = json.dumps(parsed_content, indent=4)
        # Simulate pasting the JSON content
        # time.sleep(5)  # Small delay to give time to focus the cursor
        formatted_json_with_placeholder = formatted_json.replace("\n", "<SHIFT_ENTER>")

        # Type the entire string at once
        for char in formatted_json:
            if char == '\n':
                pyautogui.hotkey('shift', 'enter')  # Simulate Shift+Enter for new lines
                time.sleep(0.1)  # Optional: Add small delay to make it more natural
            else:
                pyautogui.write(char)

    except Exception as e:
        # Display an alert if something goes wrong
        pyautogui.alert(f"An error occurred: {e}", title="Error")
def correct_english():
    try:
        text = pyperclip.paste()
        # corrected_text = str(TextBlob(text).correct())
        # pyperclip.copy(corrected_text)
        # pyautogui.alert("Text corrected and copied to clipboard.", "Success")
    except Exception as e:
        pyautogui.alert(f"Error: {e}", "Error")

def main():
    option = pyautogui.confirm("Choose an action:", "Clipboard Transformer",
                               buttons=["Convert to JSON", "Correct English", "Exit"])
    if option == "Convert to JSON":
        clipboard_to_json_and_paste()
    elif option == "Correct English":
        correct_english()
    elif option == "Exit":
        return

if __name__ == "__main__":
    main()
