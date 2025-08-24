from google import genai
from google.genai import types

from html import escape
import markdown

def generate(query, system_instructions,
            history = None, selected_datastore = None, 
            selected_model = "gemini-2.5-flash-lite"):
   """Generates content using Google Generative AI with specified datastore and model."""
   client = genai.Client(
   vertexai=True,
   project="kinetic-calling-463721-a8",
   location="global",
   )
   if selected_datastore:
      tools = [
         types.Tool(
         retrieval=types.Retrieval(
         vertex_rag_store=types.VertexRagStore(
            rag_resources=[
            types.VertexRagStoreRagResource(
                  rag_corpus=selected_datastore
            )
            ],
         )
         )
         )
      ]
   else: 
      tools = []

   generate_content_config = types.GenerateContentConfig(
   temperature = 1,
   top_p = 0.95,
   max_output_tokens = 19629,
   safety_settings = [types.SafetySetting(
      category="HARM_CATEGORY_HATE_SPEECH",
      threshold="OFF"
   ),types.SafetySetting(
      category="HARM_CATEGORY_DANGEROUS_CONTENT",
      threshold="OFF"
   ),types.SafetySetting(
      category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
      threshold="OFF"
   ),types.SafetySetting(
      category="HARM_CATEGORY_HARASSMENT",
      threshold="OFF"
   )],
   tools = tools,
   system_instruction=[types.Part.from_text(text=system_instructions)],
   thinking_config=types.ThinkingConfig(
      thinking_budget=0,
   ),
   )
  
   contents_list = []
   if history:
      for msg in history:
         contents_list.append(
         types.Content(
            role=msg['role'],
            parts=[types.Part.from_text(text=msg['content'])]
         )
      )


   contents_list.append(
      types.Content(
      role="user",
      parts=[types.Part.from_text(text=query)]
      )
   )
   
   response = client.models.generate_content(
      model=selected_model,
      contents=contents_list,
      config=generate_content_config)
   print(response.text)
   
   return response

def clean_for_html(text):

    # Convert markdown to HTML
    html = markdown.markdown(text)
    return html

system_instructions_choose_game = """
You are an AI agent that analyzes user queries and conversation history to determine which of the following three games the user is referring to: Pokemon, Riftbound, or YuGiOh.
Or choose "fallback" if you are not 100% sure, it should be clear as the user is will provide the game name in their query.
Instructions:
- Consider both the current user input and the historical conversation context.
- Choose only one game from the list: Pokemon, Riftbound, YuGiOh. 
- If one of those games has not been explicity written by the user, choose "fallback".
- If you are unsure, do not guess; instead, respond with "fallback".
- Output your answer strictly in the following machine-readable JSON format: {"game":"<game_name>"}
- Replace <game_name> with either "pokemon", "riftbound", "yugioh", or "fallback (all UPPERCASE).
- Do not include any explanation, extra text, or formatting—only output the JSON object.
"""

system_instructions_teach_rules = """Role: You are an AI assistant dedicated to helping users learn and play a card games Core 
Objective: To guide users through the game's rules, mechanics, and strategies in a clear, concise, and helpful manner, fostering a positive learning experience."""