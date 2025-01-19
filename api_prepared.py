from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ollama import chat

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342"],  # Replace with your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define the request model
class RequestModel(BaseModel):
    instruction: str
    content: str

# Define the response model
class ResponseModel(BaseModel):
    translated_content: str

@app.post("/translate/", response_model=ResponseModel)
async def translate(request: RequestModel):
    """
    Endpoint to translate content based on user instruction.
    """
    system_message = f"You are an intelligent assistant. {request.instruction}"
    print(request.instruction)
    print(request.content)
    try:
        response = chat(
            model='phi4',  # Adjust the model name as needed
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": request.content}
            ]
        )

        if 'message' in response and 'content' in response['message']:
            translated_content = response['message']['content']
            return {"translated_content": translated_content}
        else:
            raise HTTPException(
                status_code=500,
                detail="Unexpected response format from the model."
            )

    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during translation: {str(ex)}"
        )
