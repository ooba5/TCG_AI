from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict
from chat_functions import generate, clean_for_html, system_instructions_teach_rules, system_instructions_choose_game
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.output_parsers import JsonOutputParser
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#Object for parsing JSON output from the agent
parser = JsonOutputParser()

# Global state for conversation history (NOT USER SPECIFIC)
past_conversation: List[Dict[str, str]] = []

class QuestionRequest(BaseModel):
    query: str
    game: str = "Default"  # Default game if not specified

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    # Each data store should represent the rulebook of one game trained into a RAG engine.
    # The data store needs to be selected by an Agent based on the user's context.
    agents_chosen_datastore = generate(request.query, system_instructions_choose_game, past_conversation, selected_datastore = None )
    selected_datastore = parser.parse(agents_chosen_datastore.text).get('game', 'fallback')
    # Retrieve the Correct Datastore
    print(f"Selected Datastore: {selected_datastore}")
    if selected_datastore.upper() == "RIFTBOUND":
        selected_datastore = "projects/kinetic-calling-463721-a8/locations/us-central1/ragCorpora/3379951520341557248"
    elif selected_datastore.upper() == "YUGIOH":
        selected_datastore = "projects/kinetic-calling-463721-a8/locations/us-central1/ragCorpora/7454583283205013504"
    elif selected_datastore.upper() == "POKEMON":
        selected_datastore = "projects/kinetic-calling-463721-a8/locations/us-central1/ragCorpora/4749045807062188032"
    else:
        selected_datastore = "fallback"
    # Simple fallback if the agent fails to choose a game (could use another agent here or a use a retry mechanism)
    if selected_datastore == "fallback":  
        return {"answer": "I'm sorry, I couldn't determine which game you're referring to. Please specify either Pokemon, Riftbound, or YuGiOh."}
    else:  
        response = generate(request.query, system_instructions_teach_rules, past_conversation, selected_datastore=selected_datastore)
        past_conversation.append({"role": "user", "content": request.query})
        past_conversation.append({"role": "assistant", "content": response.text})
        cleaned_text = clean_for_html(response.text)
    return {"answer": cleaned_text}