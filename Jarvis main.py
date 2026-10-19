
#imports
import subprocess
import webbrowser
import os
import datetime
import requests
import json
from pathlib import Path  


#the commands for jarvis and their uses
commands = {
    "/open": "Opens a website or an application",

    "/weather": "Displays the current weather",

    "/help": "Displays a list of the current commands and their uses",
 
    "/files": "Opens your file explorer to a specific folder",

    "/chat": "Let's you chat with the ai model",

    "/memory": "Lets you view and change things you want the ai model to know",

    "/time": "Displays the current time and date",

    "/messages": "Displays a list of all the messages you have sent to the ai model and the responses it has given",

    "/quit": "Stops the program"

}

#stores the user directory and the onedrive directory in variables
user_directory = os.path.expanduser("~")
onedrive_directory = os.environ.get("OneDrive")
user_path = Path(user_directory)
onedrive_path = Path(onedrive_directory)



#ai reusable logic for the rest of the program

def ask_jarvis(message, memory):
    ollama_options = {
        "temperature": settings["temperature"]
    }

    response = requests.post(
        settings["ollama_url"] + "/api/chat",
        json={
            "model": settings["model"],
            "messages": [
    {
        "role": "system",
        "content": f'{settings["memory_prompt"]}\n\nSaved memory:\n{memory}'
    },
    {"role": "user", "content": message}
],
            "stream": False,
            "options": ollama_options
        },
        timeout=settings["request_timeout"]
    )
    data = response.json()
    return data["message"]["content"]

JARVIS_FOLDER = Path(__file__).parent

PRIVATE_DATA_FOLDER = JARVIS_FOLDER / "private_data"
PRIVATE_DATA_FOLDER.mkdir(exist_ok=True)

MEMORY_FILE = PRIVATE_DATA_FOLDER / "memory.txt"
MESSAGES_FILE = PRIVATE_DATA_FOLDER / "messages.txt"

settings_config = JARVIS_FOLDER / "settings.json"
if settings_config.exists():
    with open(settings_config, "r", encoding="utf-8") as file:
        settings = json.load(file)

else:
    settings = {
    "model": "gemma3:1b",
    "ollama_url": "http://localhost:11434",
    "temperature": 0.7,
    "request_timeout": 60,
    "memory_enabled": True,
    "logging_enabled": True,
     "memory_prompt": "You are Jarvis, a helpful AI assistant. You have access to saved information about the user.\n\nUse these rules:\n\n1. Read the user's current message and understand its context before deciding whether any saved information is relevant.\n2. Use saved information when it directly helps answer the current message, understand the user's preferences, or continue a previous project or conversation.\n3. If the user explicitly asks about their interests, preferences, past conversations, or saved information, answer using the relevant facts from memory.\n4. If saved information is unrelated to the current message, ignore it completely.\n5. Do not list saved facts just because they are available. Do not bring up personal details during ordinary greetings or unrelated conversations.\n6. When memory is relevant, use it naturally. You do not need to announce that you are using memory.\n7. If the user asks about something that is not present in the saved information, be honest that you cannot find it. Never invent memories.\n8. Always prioritize answering the user's actual message over discussing their saved information."
}
    with open(settings_config, "w", encoding="utf-8") as file:
      json.dump(settings, file)



shortcuts_folder = f"{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs"
shortcuts_path = Path(shortcuts_folder)

for item in shortcuts_path.iterdir():
   if item.is_file() and item.suffix == ".lnk":
     pass 

def message_log(message, answer, mode):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(MESSAGES_FILE, "a", encoding="utf-8") as file:
        file.write(f"You: {message}\n Time: {current_time}\n")
        file.write(f"Jarvis: {answer}\n Time: {current_time}\n Mode: {mode}\n")




#creats the main loop for the program
while True:
    choice = input("Enter a command (use /help for a list of all commands) ").lower().strip()

    parts = choice.split()

    print(parts)

    if parts[0] == "/open":
        target = input("Would you like to open an application or a website? ").lower().strip()

        if target in ["open website", "website", "open a website"]:  
          
            domain = input("Enter the website domain (.com, .gg etc.): ").lower().strip()

            url = input("What would you like to open? ").lower().strip()

            if domain == ".vercel":
                project = input("What is your project name? ").lower()
                webbrowser.open(f"https://{project}.vercel.app")

            else:
                webbrowser.open(f"https://www.{url}{domain}")

        elif target in ["open an app", "open an application", "app", "application"]:

            app = input("What app would you like to open? ").lower().strip()

            if app == "calculator":
                subprocess.run("calc")

            elif app == "notepad":
                subprocess.run("notepad")

            elif app in ["paint", "microsoft paint"]:
                subprocess.run("mspaint")

            elif app in ["command prompt", "cmd"]:
                subprocess.run("cmd")

            elif app in ["file explorer", "explorer"]:
                subprocess.run("explorer")

            elif app == "task manager":
                subprocess.run("taskmgr")

            elif app in ["microsoft edge", "edge"]:
                subprocess.run(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

            elif app == "settings":
                subprocess.run("ms-settings:")

            else:
                print("This app is not currently supported or has been entered incorrectly.")

        else:
            print("This is not supported")

    elif choice == "/weather":
     pass

    elif choice == "/help":
     print("Here's a list of all supported commands!")

     print(commands)

    elif choice == "/files":
     folder = input("What folder would you like to open? (downloads, documents)")

     if folder == "downloads":
        subprocess.run(["explorer.exe", r"C:\Users\k9734\Downloads"])

     elif folder == "documents":
        subprocess.run(["explorer.exe", r"C:\Users\k9734\OneDrive\Documents"])

     elif folder == "gallery":
        subprocess.run(["explorer.exe", r"C:\Users\k9734\OneDrive\Gallery"])

    elif choice == "/chat":
     memory_active = True
     while True:
            
            message = input("You: ").strip()

            with open(MEMORY_FILE, "r", encoding="utf-8") as file:
                                memory = file.read()

            if message.lower() == "/exit":
             break

            elif message.lower() == "/memory write":
                 memory_note = input("What would you like to add to memory?").strip()
                 with open(MEMORY_FILE, "a", encoding="utf-8") as file:
                  file.write("\n" + memory_note + "\n")
                  prompt = input("You: ").strip()
                 with open(MEMORY_FILE, "r", encoding="utf-8") as file:
                    memory = file.read()
                    answer = ask_jarvis(prompt, memory)
                    print("Jarvis:", answer)
                    message_log(prompt, answer, "write")
                    continue 

            elif message.lower() == "/memory disable":
                         memory_active = False
                         message = input("You: ")
            
                         answer = ask_jarvis(message, "")
                         print("Jarvis: ", answer)
                         message_log(message, answer, "memory disabled")
                         continue 
            

            if memory_active: 
              answer = ask_jarvis(message, memory)

            elif not memory_active:
               answer = ask_jarvis(message, "")
           
            print("Jarvis: ", answer)
            message_log(message, answer, "memory mode")


    elif choice == "/memory":
     subprocess.Popen(["notepad", str(MEMORY_FILE)])

    elif choice == "/messages":
        subprocess.Popen(["notepad", str(MESSAGES_FILE)])

    elif choice == "/time":
     current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     print(f"The current time and date is: {current_time}")
       
    elif choice == "/quit":
        break

    else:
        print("This is not valid.")