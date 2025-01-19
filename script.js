// Function to automatically populate the input field with clipboard content
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const clipboardText = await navigator.clipboard.readText();
        document.getElementById('inputText').value = clipboardText;
    } catch (error) {
        console.error("Failed to read clipboard content:", error);
    }
});

// Function to retrieve the value from the input textarea
function getInputTextValue() {
    return document.getElementById('inputText').value.trim();
}

// Function to make API calls
async function processText(text_content, instruction) {
    const outputTextArea = document.getElementById('outputText');

    if (!text_content) {
        outputTextArea.value = "Input text is empty!";
        return;
    }

    const prompt = instruction.replace("{input}", text_content);

    try {
        // Make the API call
        const translatedContent = await apiCall(prompt, instruction);

        // Update the output field
        outputTextArea.value = translatedContent;

        // Copy the output to the clipboard if the document is focused
        if (document.hasFocus()) {
            await navigator.clipboard.writeText(translatedContent);
        } else {
            console.warn("Document is not focused; clipboard write skipped.");
        }

        console.log(`Instruction: ${instruction}`);
        console.log(`Input: ${text_content}`);
        console.log(`Output: ${translatedContent}`);
    } catch (error) {
        outputTextArea.value = `Error: ${error.message}`;
    }
}

// API call function
async function apiCall(prompt, instruction) {
    const apiUrl = "http://127.0.0.1:8000/translate/";
    try {
        const response = await fetch(apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                instruction: instruction,
                content: prompt
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        const data = await response.json();
        return data.translated_content || "No content received from the server.";
    } catch (error) {
        console.error("Error during API call:", error);
        throw error;
    }
}