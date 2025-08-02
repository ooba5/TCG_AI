import requests

payload = {
    "query": "I am a total Noob, looking to just get started what do I need to know"
}

response = requests.post("http://localhost:8000/ask", json=payload)
print(response.text)

payload = {
    "query": "What Question did I just ask?",
}

response = requests.post("http://localhost:8000/ask", json=payload)
print(response.text)