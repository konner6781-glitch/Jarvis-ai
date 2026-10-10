# making a simple open command in my laptop to open youtube (later a ai model will determine the command and open it)

#imports
import subprocess
import webbrowser
import os
import datetime
import requests
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

    "/quit": "Stops the program"

}

#stores the user directory and the onedrive directory in variables
user_directory = os.path.expanduser("~")
onedrive_directory = os.environ.get("OneDrive")
user_path = Path(user_directory)




#ai reusable logic for the rest of the program

def ask_jarvis(message, memory):
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "gemma3:1b",
            "messages": [
                {"role": "user", "content": message},
                {"role": "system", "content": memory}
            ],
            "stream": False
        }
    )

    return response.json()["message"]["content"]


JARVIS_FOLDER = Path(__file__).parent
MEMORY_FILE = JARVIS_FOLDER / "memory.txt"
MESSAGES_FILE = JARVIS_FOLDER / "messages.txt"


shortcuts_folder = f"{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs"
shortcuts_path = Path(shortcuts_folder)

for item in shortcuts_path.iterdir():
   if item.is_file() and item.suffix == ".lnk":
      print(f"Shortcut: {item.name}, path: {item.resolve()}")




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
     while True:  
      message = input("You: ")

      if message.lower().strip() == "/exit":
        break

      with open(MEMORY_FILE, "r" , encoding="utf-8") as file:
         memory = file.read()
  
      answer = ask_jarvis(message, memory)
      print("Jarvis:", answer)

      current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

      #logs messages to a text file for later use
      with open(MESSAGES_FILE, "a", encoding="utf-8") as file:
        file.write(f"You: {message}, Time: {current_time}\n")
        file.write(f"Jarvis: {answer}, Time: {current_time}\n")


    elif choice == "/memory":
     subprocess.Popen(["notepad", str(MEMORY_FILE)])

    elif choice == "/time":
     current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     print(f"The current time and date is: {current_time}")
       
    elif choice == "/quit":
        break

    else:
        print("This is not valid.")