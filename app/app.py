from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict
from chat_functions import generate, clean_for_html
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Global state for conversation history (NOT USER SPECIFIC)
past_conversation: List[Dict[str, str]] = []

class QuestionRequest(BaseModel):
    query: str
    game: str = "Default"  # Default game if not specified

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    # Each data store should represent the rulebook of one game trained into a RAG engine.
    if request.game == "Default":
        selected_datastore = "projects/kinetic-calling-463721-a8/locations/us-central1/ragCorpora/4749045807062188032"
    elif request.game == "Alt":
        selected_datastore = "projects/812596078800/locations/us-central1/ragCorpora/7454583283205013504"
    response = generate(request.query, past_conversation, selected_datastore=selected_datastore)
    past_conversation.append({"role": "user", "content": request.query})
    past_conversation.append({"role": "assistant", "content": response.text})
    cleaned_text = clean_for_html(response.text)
    return {"answer": cleaned_text}