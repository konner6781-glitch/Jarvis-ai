# Jarvis AI

A locally hosted, AI-powered desktop assistant built with Python.

Jarvis AI is a personal desktop assistant that combines Python automation with a locally hosted AI model through Ollama. It can open applications and websites, interact with you through a terminal chat, maintain a text-based memory file, and record conversations for later review.

## Features

* **Local AI chat:** Chat with the Gemma 3 1B model through Ollama without requiring a paid AI API key.
* **Application launcher:** Open supported Windows applications directly from the terminal.
* **Website launcher:** Open websites by entering a website name and domain.
* **Memory system:** Store information in a text file for Jarvis to reference in memory-enabled chat modes.
* **Memory read mode:** Let Jarvis use saved memory when generating responses.
* **Memory write mode:** Add new information to the memory file and then chat with Jarvis using the updated memory.
* **Conversation logging:** Save user messages, Jarvis's responses, timestamps, and chat modes to a log file.
* **File explorer shortcuts:** Open supported folders such as Downloads, Documents, and Gallery.
* **Command menu:** Use `/help` to view available commands and descriptions.
* **Example files:** View example memory and message-log formats without exposing your actual private data.

## Requirements

* Windows
* Python
* [Ollama](https://ollama.com/)
* The `gemma3:1b` model, or another compatible model configured in the code
* Python `requests` library

## Setup

1. Install Python if it is not already installed.

2. Install Ollama from [ollama.com](https://ollama.com/).

3. Download the default AI model by running this command in your terminal:

   ```bash
   ollama pull gemma3:1b
   ```

4. Install the required Python package:

   ```bash
   pip install requests
   ```

5. Make sure Ollama is running locally.

6. Run `Jarvis main.py` using Python.

Jarvis connects to Ollama through its local API at `http://localhost:11434/api/chat`.

No external AI API key is required for the default local setup.

## Commands

| Command     | Description                                                                                                |
| ----------- | ---------------------------------------------------------------------------------------------------------- |
| `/open`     | Opens a supported application or website.                                                                  |
| `/weather`  | Reserved for weather functionality; implementation is not yet complete.                                    |
| `/help`     | Displays the available commands and their descriptions.                                                    |
| `/files`    | Opens a supported folder in File Explorer.                                                                 |
| `/chat`     | Starts a conversation with the AI model.                                                                   |
| `/memory`   | Opens the memory file in Notepad when used from the main menu. Inside chat, it opens the memory-mode menu. |
| `/messages` | Opens the conversation log in Notepad.                                                                     |
| `/time`     | Displays the current date and time.                                                                        |
| `/quit`     | Stops the program.                                                                                         |

### Chat commands

While inside `/chat`:

| Command   | Description                                       |
| --------- | ------------------------------------------------- |
| `/memory` | Opens the memory-mode menu.                       |
| `/exit`   | Leaves chat and returns to the main command menu. |

### Memory modes

After entering `/memory` inside chat, choose a mode:

* **Read (`read`)** — Jarvis reads `memory.txt` and uses its contents when answering your prompt.
* **Write (`write`)** — Enter a memory note to append to `memory.txt`. Jarvis then loads the updated memory and answers your next prompt using it.
* **Return (`return`)** — Leaves the memory menu and returns to normal chat.

Normal chat does not load the saved memory file into the AI request. This allows you to chat without supplying your saved memory.

## Data and file storage

Jarvis stores its memory and message log in a `private_data` folder alongside the main Python file.

```text
jarvis/
├── Jarvis main.py
├── ollama test.py
├── README.md
├── .gitignore
├── memory example.txt
├── messages example.txt
└── private_data/
    ├── memory.txt
    └── messages.txt
```

The example files demonstrate the intended formatting. They are not intended to contain real private memories or actual conversation logs.

### Memory file

`memory.txt` stores information you choose to save. In memory-read and memory-write modes, Jarvis loads the saved contents to provide context for its responses.

Example:

```text
My favorite car is a Lamborghini.
My favorite color is blue.
I like coding.
```

### Message log

`messages.txt` records chat interactions with timestamps and mode labels.

The modes currently recorded are:

* `default` — Normal chat without saved memory supplied to the AI.
* `read` — Chat using saved memory.
* `write` — Chat following a memory update.

Example:

```text
You: Hello
Time: 2026-10-10 17:30:00
Mode: default
Jarvis: Hello! How can I help?
Time: 2026-10-10 17:30:00
Mode: default
```

Memory and message logs are excluded from version control using `.gitignore` so personal data is not intentionally uploaded to the public repository.

## Supported applications

The `/open` command currently supports applications such as:

* Calculator
* Notepad
* Microsoft Paint
* Command Prompt
* File Explorer
* Task Manager
* Microsoft Edge
* Windows Settings

Application availability and paths may vary between Windows installations.

## Privacy

Jarvis uses a locally hosted Ollama model for AI responses. Its memory and conversation logs are stored as local text files.

The `private_data/` directory is excluded from Git tracking. Keep personal information out of public example files, and check your repository before pushing changes to ensure private data is not included.

## Project status

Jarvis AI is an ongoing personal Python project. Features are developed and improved over time as I learn more about Python, functions, file handling, loops, APIs, and debugging.

The goal is to build a useful desktop assistant while understanding and maintaining the code behind it.

## License

No license has been specified yet.
