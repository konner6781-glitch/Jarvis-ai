# Jarvis AI

*A locally hosted, AI-powered desktop assistant built with Python.*


The examples provided on this GitHub page demonstrate what the message log and memory file could look like. They are not real conversations or actual AI responses; they are provided solely to demonstrate the file formats.


## Overview

Jarvis AI is a Windows desktop assistant designed to make everyday tasks easier. It can chat with you using a locally hosted AI model, open supported applications and websites, navigate certain folders, and store conversation history locally.

This project started as a learning project and is gradually expanding into a more capable desktop assistant. The goal is to make interacting with your computer easier through a simple command system and AI-powered features.

Jarvis currently uses Ollama to run AI models locally. **Gemma 3 1B is the default model, but users can configure Jarvis to use other compatible Ollama models.**

## Features

* **AI Chat:** Chat with a locally hosted AI model, ask questions, and have conversations.
* **Command System:** Use commands such as `/open` and `/help` to interact with Jarvis. Enter `/` commands at the main prompt.
* **Website Launcher:** Open websites using the `/open` command and follow the prompts to enter the website information.
* **Application Launcher:** Open supported Windows applications, including Microsoft Paint, Microsoft Edge, Calculator, Notepad, Command Prompt, and Task Manager.
* **Memory System:** Use `/memory` to open `memory.txt` in Notepad. Add information you want Jarvis to consider when responding. Jarvis reads this file as context; it does not automatically train the AI model or give it unlimited permanent memory.
* **Conversation Logging:** Messages and Jarvis responses are recorded in `messages.txt` with timestamps. The file is stored locally on your computer by default.
* **File Navigation:** Open supported File Explorer locations, such as Downloads and Documents.
* **Configurable AI Models:** Use Gemma 3 1B or another compatible model available through Ollama by updating the model configuration in the source code.

## Available Commands

| Command    | Description                                                                                                  |
| ---------- | ------------------------------------------------------------------------------------------------------------ |
| `/open`    | Opens supported websites or applications by following the prompts.                                           |
| `/weather` | Reserved for weather functionality; not yet implemented if the current version still contains a placeholder. |
| `/help`    | Displays the available commands and their descriptions.                                                      |
| `/files`   | Opens supported File Explorer locations, such as Downloads and Documents.                                    |
| `/chat`    | Starts a conversation with the configured local AI model.                                                    |
| `/memory`  | Opens the memory file so you can view or edit stored information.                                            |
| `/time`    | Displays the current date and time.                                                                          |
| `/quit`    | Exits the program.                                                                                           |
| `/exit`    | Leaves AI chat and returns to the main command interface.                                                    |

## Requirements

* **Operating System:** Windows is the primary supported operating system. AI chat may work on other operating systems that support Python and Ollama, but Windows-specific features such as application launching may require changes.
* **Python:** Python 3.x. Compatibility with different Python versions has not been fully tested.
* **Ollama:** Required to run the AI model locally.
* **An Ollama-compatible AI model:** Gemma 3 1B is the default, but other compatible models can be used.
* **Python Dependencies:** The `requests` package.

## Installation

### 1. Download the Project

You can download Jarvis AI by cloning the repository using Git or downloading it as a ZIP file.

**Option A: Clone using Git**

Open a terminal and run:

```bash
git clone https://github.com/konner6781-glitch/Jarvis-ai.git
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

Run:

```bash
python -m pip install requests
```

If `python` doesn't work on Windows, try:

```bash
py -m pip install requests
```

### 3. Install Ollama

Download and install Ollama from the official website:

https://ollama.com/download

Ollama runs the AI model locally and provides the API that Jarvis uses to communicate with it.

### 4. Download an AI Model

**Gemma 3 1B is the default model, but you are not limited to it.**

To download the default model, run:

```bash
ollama pull gemma3:1b
```

To use a different model, find a compatible model in the [Ollama model library](https://ollama.com/library) and download it using its documented model name.

For example, another model might be downloaded with a command like:

```bash
ollama pull MODEL_NAME
```

Replace `MODEL_NAME` with the actual name of the model you want to use.

**Important:** Jarvis does not automatically switch models when you download a new one. You must also update the model name in the source code wherever the current model is configured. The model must be available through your local Ollama installation.

Different models have different hardware requirements, response speeds, and capabilities. Choose a model that works well on your computer.

### 5. Start the Ollama Service

Ollama normally starts its service automatically after installation. If it isn't running, open the Ollama application or start the service using the appropriate method for your operating system.

To check whether the local service is available, visit:

http://localhost:11434

If the service is running, it should return a message indicating that Ollama is running.

To check which models are installed, run:

```bash
ollama list
```

Make sure your selected model appears in the list.

### 6. Launch Jarvis

Open a terminal in the project directory and run the Python file containing the main program.

For example, if the main file is named `main.py`:

```bash
python main.py
```

On Windows, you can also use:

```bash
py main.py
```

Replace `main.py` with the actual filename if your main Python file has a different name.

Once Jarvis starts, follow the prompts in the terminal to interact with it.

## Usage Guide

### Opening Websites

Use `/open` and select the website option. Follow the prompts to enter the website information.

### Opening Applications

Use `/open` and select the application option. Enter the name of a supported application when prompted.

Applications not currently supported by the launcher may not open.

### Using AI Chat

Enter `/chat` to start a conversation with your configured AI model. Enter `/exit` to return to the main command interface.

### Managing Memory

Use `/memory` to open `memory.txt` in Notepad. Add or edit information you want Jarvis to consider in future responses.

### Viewing Conversation History

Jarvis records conversations in `messages.txt`, including timestamps. You can open the file using a text editor to review the saved messages.

## Configuration

### Changing the AI Model

Jarvis is currently configured to use `gemma3:1b` by default. You can change this to another model supported by your Ollama installation.

1. Download your chosen model through Ollama.
2. Locate the model configuration in the Jarvis source code.
3. Replace `gemma3:1b` with the model's exact Ollama name.
4. Save the changes and restart Jarvis.

For example, if the code contains:

```python
"model": "gemma3:1b"
```

You can change the model name to match another model you have downloaded.

The exact configuration may vary depending on how the model is referenced in the code. Make sure every relevant model reference is updated if necessary.

## Current Limitations

* The application launcher currently supports a predefined list of applications.
* Website launching follows the prompts implemented in the current command system.
* The weather command may not be implemented yet.
* AI responses depend on the selected model's capabilities and available computer resources.
* Changing the configured model requires editing the source code.
* Some features rely on Windows-specific paths or applications.

## Planned Features

Future development may include:

* Discovering and launching more applications automatically.
* Improved natural-language command handling.
* Expanded file navigation and management, with appropriate user permission and confirmation.
* Voice input and spoken responses.
* Screenshot analysis and other AI-assisted desktop features.

Jarvis should validate AI-suggested actions before executing them, especially for operations that could modify files or affect the computer.

## Technology Stack

* **Python:** Powers the command system, application launching, file navigation, and AI integration.
* **Ollama:** Runs compatible AI models locally and provides a local API.
* **Gemma 3 1B:** The default AI model currently configured for Jarvis. It can be replaced with another compatible Ollama model.
* **Requests:** Sends requests to Ollama's local API and receives responses.
* **Pathlib / OS:** Help manage file paths, directories, and operating-system information.
* **Subprocess:** Launches supported applications and system processes.
* **Webbrowser:** Opens websites in the default browser.
* **Datetime:** Provides timestamps and current date and time information.

## Contributing and Feedback

Jarvis AI is an ongoing learning project. Suggestions, bug reports, and feature requests are welcome.

If you encounter a bug or have an idea for an improvement, open an issue in this GitHub repository and describe the problem or suggestion. Include relevant error messages and steps to reproduce a bug when possible.

## License

This project does not currently specify an open-source license. Until a license is added, others should not assume they have permission to redistribute or modify the project under open-source terms.

## Project Status

Jarvis AI is currently under development. The existing version supports a command-based interface, local AI chat, configurable Ollama model selection, application and website launching, basic file navigation, editable memory, and local conversation logging.

Development will continue as new features are added and existing functionality is improved.
