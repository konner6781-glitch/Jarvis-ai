

import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "gemma4:latest",
        "prompt": """
You are the command interpreter for Jarvis.

If the user wants to open a website, reply: open_website
If the user wants to open an application, reply: open_app
If the user wants to quit Jarvis, reply: quit

Reply with exactly one label.
User command: Open YouTube
""",
        "stream": False
    }
)

data = response.json()
print(data["response"])