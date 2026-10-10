# Jarvis AI

*A locally hosted AI-powered desktop assistant built with Python.*

## Overview

Jarvis ai is a windows assistant helper tool that can chat with you, open stuff for you and make life easier, I created this tool as a learning project but now I plan to make it something bigger.  This AI tool is used to make your life easier with opening commands and weather etc. without having to go and search stuff up.

## Features

* **AI Chat:** You can interact with the local AI model by asking it questions, telling it to perform a simple task, or having a simple chat.
* 
* **Command System:** The way Jarvis listens to instructions is by using commands, common commands include, /open and /help which help lists all of the current commands and their uses, use a / to enter a command.
* 
* **Website Launcher:** You can open a website by using the command /open then typing in website which then asks you for the domain, which is a .com .gg etc. then enter the url (the website you want to enter) for youtube it would be like this /open, website, .com, youtube.

* **Application Launcher:** Jarvis can currently open several common windows applications including, microsoft paint, microsoft edge, calculator, notepad, cmd, and task manager.
* use /open to open an application then choose app and enter the app name.
* 
* **Memory System:** Jarvis has a built in command to remember things */memory* which opens your notepad to the file memory.txt and you can add things about yourself or things you want the ai model to know. NOTICE: This feature DOES NOT give the ai model itself ability to remember everything about you it reads the memory file every time before it responds so it can answer relative to what it knows.
* 
* **Conversation Logging:** The conversations you have with the ai model gets logged on a local file called "messages.txt" which records your message and Jarvis response with timestamps NOTICE: This DOES NOT let other people view your chats its stored locally on your device only.
  
* **File Navigation:** Jarvis can also open some file explorer areas like downloads and documents.

## Available Commands

| Command    | Description                                                                           |
| ---------- | ------------------------------------------------------------------------------------- |
| `/open`    | [Explain how this command opens websites and applications.]                           |
| `/weather` | [Describe what this command currently does, or state that it is not implemented yet.] |
| `/help`    | Displays the available commands and their descriptions.                               |
| `/files`   | [Explain how users navigate to supported folders.]                                    |
| `/chat`    | Starts a conversation with the locally hosted AI model.                               |
| `/memory`  | Opens the memory file so users can view or edit stored information.                   |
| `/time`    | Displays the current date and time.                                                   |
| `/quit`    | Exits the program.                                                                    |
| `/exit`    | Exits AI chat and returns to the main command interface.                              |

## Requirements

* **Operating System:** Windows is currently the supported operating system for this AI tool, however any operating system capable of using python libraries and ollama can  use the ai chat still with memory but app opening is native to windows.

* **Python:** Python 3.10 or newer (recommended; compatibility with other versions has not been fully tested).
* 
* **Ollama:** Ollama is a platform that you can use to locally host ai models, you need to download it on windows the command is irm https://ollama.com/install.ps1 | iex you can use this to download ollama on your computer https://ollama.com/download/windows here is the page you can view.
* 
* **AI Model:** Currently Gemma3:1b is the currently coded ai model but if you have a preference to other ai models you can go into the section where the ai logic is by the top of the code and change your ai to the "model": "(your model here)" where gemma is right now.
* 
* **Python Dependencies:** You need the package 'requests' downloaded on python.

## Installation

### 1. Download the Project

You can download Jarvis AI by cloning the repository with Git or downloading it as a ZIP file.

**Option A: Clone using Git**

Open a terminal and run:

```bash
git clone https://github.com/konner6781-glitch/Jarvis-ai
cd Jarvis-ai
```

**Option B: Download as a ZIP**

1. Open this repository on GitHub.
2. Click the **Code** button.
3. Select **Download ZIP**.
4. Extract the downloaded ZIP file.
5. Open a terminal in the extracted project folder.

### 2. Install Dependencies

Jarvis uses Python's `requests` package to communicate with Ollama. The other Python modules currently used by the project are included with Python.

Run the following command in your terminal:

```bash
python -m pip install requests
```

If `python` doesn't work on Windows, try:

```bash
py -m pip install requests
```

### 3. Set Up Ollama

Jarvis uses Ollama to run its AI model locally.

1. Download and install Ollama from https://ollama.com/.
2. Open a terminal.
3. Download the required model by running:

```bash
ollama pull gemma3:1b
```
you can use another ai model but make sure to replace it in your code 
Wait for the download to finish before continuing.

### 4. Start the AI Service

Ollama provides a local service that Jarvis uses to communicate with the AI model.

Ollama normally starts its service automatically after installation. If it isn't running, open the Ollama application or start the service using the appropriate command for your operating system.

To check whether the local service is available, open this address in your browser:

http://localhost:11434

If the service is running, Ollama should respond with a message indicating that it is running.

You can also check whether the model is installed by running:

```bash
ollama list
```

Look for `gemma3:1b` OR your ai model in the list.

### 5. Launch Jarvis

Open a terminal in the project directory and run the Python file that contains the main program.

For example, if the main file is named `main.py`, run:

```bash
python main.py
```

On Windows, you can also use:

```bash
py main.py
```

Replace `main.py` with the actual name of your main Python file if it is different.

Once Jarvis starts, follow the instructions displayed in the terminal to interact with it.

## Usage Guide

### Opening Websites
To open websites using Jarvis you can use the /open command and then follow the prompt into website and enter your domain and url to the website.

### Opening Applications
You can also open applications using /open to open apps follow the prompt into what app you want to enter. You will need to enter one of the supported apps.

### Using AI Chat
Use the command /chat to have a chat with the ai model that you chose you can use /exit while in the chat to go back to the prompt to ask about what command.

### Managing Memory
to change things you want the ai model to know use the command /memory and it will open a file in notepad to change jarvis memory.


## Configuration
You can change the ai model in the code where the ai logic is listed make sure if you change the ai model you also make sure you have that same one installed and running.

## Current Limitations
As of right now apps dont open if they are not on the list of supported apps 

## Planned Features
Later Jarvis will be able to open any app for you and have more control over files on your computer
NOTICE: Jarvis WILL NOT create read or manage files on your computer without permission. OR under specific instruction.

## Technology Stack

* **Python:** Python is the code of this project, it does everything that is in the code as instructed and it is the do of the project.
* 
* **Ollama:** Ollama hosts the ai model you choose locally on your computer for free.

* **Gemma 3 1B:** Gemma3:1b is the currently defualt ai model for this project although the model can be changed at any point in the project.

* **Requests:** Requests has the job of communicating with the local ai model 

* **Pathlib / OS:** These libraries help to access files and operating system functions and operations on your computer.


## Contributing and Feedback

[Explain whether users can report bugs, suggest improvements, or contribute code. Include instructions for reporting issues if you want to accept them.]

## License
This project has no currently specified open source license.


## Project Status
This project is currently under development and are working on new features Stay on track for updates.

[Describe the current development stage, what works today, and what you are actively working on next.]

