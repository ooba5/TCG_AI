from google import genai
from google.genai import types

from html import escape
import markdown

def generate(query, history = None, selected_datastore = "projects/812596078800/locations/us-central1/ragCorpora/7454583283205013504", 
             selected_model = "gemini-2.5-flash-lite"):
    """Generates content using Google Generative AI with specified datastore and model."""
    client = genai.Client(
      vertexai=True,
      project="kinetic-calling-463721-a8",
      location="global",
   )

    si_text1 = """Role: You are an AI assistant dedicated to helping users learn and play a card games
   Core Objective: To guide users through the game's rules, mechanics, and strategies in a clear, concise, and helpful manner, fostering a positive learning experience."""


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
      system_instruction=[types.Part.from_text(text=si_text1)],
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
