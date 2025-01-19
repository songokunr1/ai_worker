from ollama import chat
from ollama import ChatResponse
# gemma2
# llama3.1:8b-instruct-q8_0
# phi4
instructions = 'You are translator. translate into Polish.}'
content = 'im running fast'

response: ChatResponse = chat(model='phi4', messages=[
    {"role": "system", "content": f"You are an intelligent assistant. {instructions}"},
    {
        'role': 'user',
        'content': content,

    },
])
print(response['message']['content'])
