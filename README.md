# Jarvis AI

A personal AI assistant built with Python and Ollama. Jarvis runs locally using a language model and includes chat, memory, message logging, and helpful commands.

## Features

* **Local AI chat** powered by Ollama.
* **Persistent memory** to store notes and information for future conversations.
* **Message logging** to keep a record of conversations.
* **Built-in commands** to access features such as time, files, applications, and memory.
* **Terminal interface** for the main Jarvis experience.
* **Optional GUI interface** for users who prefer a graphical, ChatGPT-style layout.

## Interfaces

Jarvis offers two ways to interact with the assistant.

### Terminal Version — Main Version

The terminal version is the primary version of Jarvis AI. It is the main development focus and is expected to receive **more frequent updates, improvements, bug fixes, and support**.

The terminal version is recommended for users who want the latest features and the most actively maintained experience.

### GUI Version — Optional

An optional graphical user interface (GUI) is available for users who prefer a more visual experience instead of interacting through the terminal.

The GUI is intended to make Jarvis easier to navigate through a chat-style interface. Availability of features may depend on the current state of GUI development.

**Please note:** The GUI is an alternative interface, not the primary development focus. Updates and support for the GUI may be less frequent than for the terminal version.

## Requirements

* Python 3
* [Ollama](https://ollama.com/)
* The `gemma3:1b` model, unless the model configuration has been changed
* Python packages used by the project, including `requests`

## Setup

### 1. Install Python

Download Python from [python.org](https://www.python.org/downloads/) if it is not already installed.

### 2. Install Ollama

Download and install Ollama from [ollama.com](https://ollama.com/).

### 3. Download the model

Open a terminal and run:

```bash
ollama pull gemma3:1b
```

Make sure Ollama is running before starting Jarvis.

### 4. Install dependencies

From the project directory, run:

```bash
pip install requests
```

Install any additional dependencies required by the interface you choose.

### 5. Start Jarvis

**Terminal version:**

Run the main Python file:

```bash
python "Jarvis main.py"
```

**GUI version:**

Run the GUI Python file included in the project, if available:

```bash
python "Jarvis GUI.py"
```

The GUI filename may differ depending on the version of the project. Use the actual filename provided in your copy of the repository.

## Commands

Jarvis includes commands for accessing different features. Available commands may change as development continues.

| Command     | Description                                             |
| ----------- | ------------------------------------------------------- |
| `/help`     | Display available commands                              |
| `/chat`     | Enter the chat interface                                |
| `/memory`   | View or manage Jarvis memory                            |
| `/messages` | Open the conversation log                               |
| `/files`    | Access supported file locations                         |
| `/open`     | Open supported applications or websites                 |
| `/weather`  | Weather command; availability depends on implementation |
| `/time`     | Display the current date and time                       |
| `/quit`     | Exit Jarvis                                             |
| `/exit`     | Exit the current chat session                           |

Some commands may behave differently depending on whether you are using the terminal or GUI interface.

## Memory and Privacy

Jarvis uses local files to store memory and conversation history. These files may contain personal information, so they should not be shared publicly.

Private data files should remain excluded from version control. Review `.gitignore` before committing or uploading changes to ensure private memory and message logs are not included.

The AI model runs through your local Ollama installation. However, the privacy of other features depends on how they are implemented and configured.

## Development and Updates

Jarvis AI is an ongoing project. Features, commands, and interfaces may change as development continues.

The **terminal version is the main development priority** and should receive more frequent updates and support. The GUI is provided as an optional alternative and may receive updates less frequently.

Bug reports, suggestions, and contributions are welcome, but compatibility and feature availability may vary between versions.

## License

Check the repository for the project's current license before redistributing or modifying it.

---

**Jarvis AI — A personal assistant built with Python and Ollama.**

