import datetime
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog
from pathlib import Path

import requests


# Keep this file in the same folder as "Jarvis main.py".
JARVIS_FOLDER = Path(__file__).parent
PRIVATE_DATA_FOLDER = JARVIS_FOLDER / "private_data"
PRIVATE_DATA_FOLDER.mkdir(exist_ok=True)

MEMORY_FILE = PRIVATE_DATA_FOLDER / "memory.txt"
MESSAGES_FILE = PRIVATE_DATA_FOLDER / "messages.txt"

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "gemma3:1b"

# Dark ChatGPT-inspired colors
BG = "#212121"
SIDEBAR = "#171717"
PANEL = "#2f2f2f"
PANEL_HOVER = "#3b3b3b"
TEXT = "#f2f2f2"
MUTED = "#a8a8a8"
ACCENT = "#10a37f"
USER_BUBBLE = "#303030"


def ask_jarvis(message, memory=""):
    """Send a message to the local Ollama model."""
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": memory},
                {"role": "user", "content": message},
            ],
            "stream": False,
        },
        timeout=180,
    )
    response.raise_for_status()
    return response.json()["message"]["content"]


def log_message(message, answer, mode="default"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(MESSAGES_FILE, "a", encoding="utf-8") as file:
        file.write(f"You: {message}\nTime: {timestamp}\n")
        file.write(f"Jarvis: {answer}\nTime: {timestamp}\nMode: {mode}\n\n")


class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis AI")
        self.root.geometry("1100x760")
        self.root.minsize(760, 560)
        self.root.configure(bg=BG)

        self.busy = False
        self.chat_number = 0
        self.memory_enabled = True
        self.current_chat = []

        self._build_layout()
        self.new_chat()
        self._show_welcome()
        self.entry.focus_set()

    def _build_layout(self):
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR, width=245)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=SIDEBAR)
        brand.pack(fill="x", padx=18, pady=(22, 18))
        tk.Label(
            brand, text="◈  Jarvis AI", bg=SIDEBAR, fg=TEXT,
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w")

        self._sidebar_button("＋  New chat", self.new_chat, top=8)
        self._sidebar_button("▤  Memory", self.open_memory)
        self._sidebar_button("⚙  Settings", self.open_settings)

        tk.Frame(self.sidebar, bg="#343434", height=1).pack(fill="x", padx=14, pady=18)
        tk.Label(
            self.sidebar, text="LOCAL ASSISTANT", bg=SIDEBAR, fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=20)

        tk.Label(
            self.sidebar,
            text="Powered by Ollama\nModel: gemma3:1b",
            bg=SIDEBAR, fg=MUTED, justify="left",
            font=("Segoe UI", 10), pady=12
        ).pack(anchor="w", padx=20)

        self.status_label = tk.Label(
            self.sidebar, text="●  Ready", bg=SIDEBAR, fg="#75c99a",
            font=("Segoe UI", 10)
        )
        self.status_label.pack(side="bottom", anchor="w", padx=20, pady=20)

        main = tk.Frame(self.root, bg=BG)
        main.pack(side="left", fill="both", expand=True)

        topbar = tk.Frame(main, bg=BG, height=60)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        tk.Label(
            topbar, text="Jarvis", bg=BG, fg=TEXT,
            font=("Segoe UI", 13, "bold")
        ).pack(side="left", padx=26, pady=16)
        self.memory_status = tk.Label(
            topbar, text="Memory: on", bg=BG, fg=MUTED,
            font=("Segoe UI", 9)
        )
        self.memory_status.pack(side="right", padx=24)

        conversation_area = tk.Frame(main, bg=BG)
        conversation_area.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            conversation_area, bg=BG, highlightthickness=0, borderwidth=0
        )
        self.scrollbar = tk.Scrollbar(
            conversation_area, orient="vertical", command=self.canvas.yview
        )
        self.messages_frame = tk.Frame(self.canvas, bg=BG)
        self.messages_window = self.canvas.create_window(
            (0, 0), window=self.messages_frame, anchor="nw"
        )
        self.messages_frame.bind("<Configure>", self._on_messages_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        bottom = tk.Frame(main, bg=BG)
        bottom.pack(fill="x", padx=24, pady=(12, 10))

        composer = tk.Frame(
            bottom, bg=PANEL, highlightbackground="#444444",
            highlightthickness=1
        )
        composer.pack(fill="x")

        self.entry = tk.Text(
            composer, height=3, wrap="word", bg=PANEL, fg=TEXT,
            insertbackground=TEXT, relief="flat", borderwidth=0,
            font=("Segoe UI", 11), padx=14, pady=13,
            undo=True
        )
        self.entry.pack(side="left", fill="both", expand=True)
        self.entry.bind("<Return>", self._enter_to_send)
        self.entry.bind("<Shift-Return>", lambda event: None)

        self.send_button = tk.Button(
            composer, text="↑", command=self.send_message,
            bg=ACCENT, fg="white", activebackground="#0e8c6d",
            activeforeground="white", relief="flat", borderwidth=0,
            font=("Segoe UI", 17, "bold"), width=3, cursor="hand2"
        )
        self.send_button.pack(side="right", padx=9, pady=9, anchor="s")

        tk.Label(
            bottom,
            text="Jarvis runs locally through Ollama. Responses can take a little time.",
            bg=BG, fg=MUTED, font=("Segoe UI", 9)
        ).pack(pady=(8, 0))

    def _sidebar_button(self, label, command, top=2):
        button = tk.Button(
            self.sidebar, text=label, command=command,
            anchor="w", padx=14, pady=10,
            bg=SIDEBAR, fg=TEXT, activebackground=PANEL_HOVER,
            activeforeground=TEXT, relief="flat", borderwidth=0,
            font=("Segoe UI", 10), cursor="hand2"
        )
        button.pack(fill="x", padx=10, pady=(top, 2))

    def _on_messages_configure(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfigure(self.messages_window, width=event.width)

    def _scroll_to_bottom(self):
        self.root.after(50, lambda: self.canvas.yview_moveto(1.0))

    def _show_welcome(self):
        welcome = tk.Frame(self.messages_frame, bg=BG)
        welcome.pack(fill="x", expand=True, pady=(100, 30))
        tk.Label(
            welcome, text="What can I help with?",
            bg=BG, fg=TEXT, font=("Segoe UI", 25, "bold")
        ).pack()
        tk.Label(
            welcome, text="Ask Jarvis something to get started.",
            bg=BG, fg=MUTED, font=("Segoe UI", 11)
        ).pack(pady=(10, 0))
        self.welcome_frame = welcome

    def new_chat(self):
        self.chat_number += 1
        self.current_chat = []
        if hasattr(self, "messages_frame"):
            for child in self.messages_frame.winfo_children():
                child.destroy()
            self._show_welcome()
        if hasattr(self, "entry"):
            self.entry.focus_set()

    def _add_message(self, who, text, is_user=False):
        if hasattr(self, "welcome_frame") and self.welcome_frame.winfo_exists():
            self.welcome_frame.destroy()

        outer = tk.Frame(self.messages_frame, bg=BG)
        outer.pack(fill="x", padx=28, pady=(14, 6))

        row = tk.Frame(outer, bg=BG)
        row.pack(fill="x")

        if is_user:
            tk.Label(
                row, text="You", bg=BG, fg=TEXT,
                font=("Segoe UI", 10, "bold")
            ).pack(anchor="e", pady=(0, 5))
            bubble = tk.Frame(row, bg=USER_BUBBLE)
            bubble.pack(anchor="e", padx=(50, 0))
            tk.Label(
                bubble, text=text, bg=USER_BUBBLE, fg=TEXT,
                justify="left", anchor="w", wraplength=650,
                font=("Segoe UI", 11), padx=15, pady=11
            ).pack()
        else:
            header = tk.Frame(row, bg=BG)
            header.pack(fill="x", pady=(0, 5))
            tk.Label(
                header, text="◈", bg=BG, fg=ACCENT,
                font=("Segoe UI", 14, "bold")
            ).pack(side="left", padx=(0, 9))
            tk.Label(
                header, text=who, bg=BG, fg=TEXT,
                font=("Segoe UI", 10, "bold")
            ).pack(side="left")
            tk.Label(
                row, text=text, bg=BG, fg=TEXT, justify="left",
                anchor="w", wraplength=740, font=("Segoe UI", 11),
            ).pack(fill="x", padx=(28, 8), pady=(0, 8))

        self._scroll_to_bottom()

    def _enter_to_send(self, event):
        if event.state & 0x0001:  # Shift+Enter adds a newline
            return None
        self.send_message()
        return "break"

    def send_message(self):
        if self.busy:
            return
        message = self.entry.get("1.0", "end-1c").strip()
        if not message:
            return
        self.entry.delete("1.0", "end")
        self._add_message("You", message, is_user=True)
        self.current_chat.append({"role": "user", "content": message})
        self.busy = True
        self.send_button.configure(state="disabled", text="…")
        self.status_label.configure(text="●  Thinking…", fg="#e6bd67")
        self._add_message("Jarvis", "Thinking…")
        self.root.update_idletasks()

        threading.Thread(
            target=self._get_answer, args=(message,), daemon=True
        ).start()

    def _get_answer(self, message):
        try:
            memory = ""
            if self.memory_enabled and MEMORY_FILE.exists():
                memory = MEMORY_FILE.read_text(encoding="utf-8").strip()

            # Send recent conversation turns along with saved memory.
            messages = [{"role": "system", "content": (
                "You are Jarvis, a helpful local desktop assistant. "
                "Use the saved memory when relevant.\n\nSaved memory:\n" + memory
            )}]
            messages.extend(self.current_chat[-12:])

            response = requests.post(
                OLLAMA_URL,
                json={"model": MODEL_NAME, "messages": messages, "stream": False},
                timeout=180,
            )
            response.raise_for_status()
            answer = response.json()["message"]["content"]
            log_message(message, answer, "gui")
            self.current_chat.append({"role": "assistant", "content": answer})
            self.root.after(0, self._finish_answer, answer, None)
        except requests.exceptions.ConnectionError:
            self.root.after(
                0, self._finish_answer, None,
                "Couldn't connect to Ollama. Make sure Ollama is running."
            )
        except requests.exceptions.Timeout:
            self.root.after(
                0, self._finish_answer, None,
                "Jarvis took too long to respond. Try again."
            )
        except Exception as error:
            self.root.after(0, self._finish_answer, None, str(error))

    def _finish_answer(self, answer, error):
        # Remove the temporary "Thinking…" bubble.
        children = self.messages_frame.winfo_children()
        if children:
            children[-1].destroy()

        if error:
            self._add_message("Jarvis", "Error: " + error)
            self.status_label.configure(text="●  Needs attention", fg="#e6bd67")
        else:
            self._add_message("Jarvis", answer)
            self.status_label.configure(text="●  Ready", fg="#75c99a")

        self.busy = False
        self.send_button.configure(state="normal", text="↑")
        self.entry.focus_set()

    def open_memory(self):
        if not MEMORY_FILE.exists():
            MEMORY_FILE.write_text("", encoding="utf-8")
        editor = tk.Toplevel(self.root)
        editor.title("Jarvis Memory")
        editor.geometry("620x500")
        editor.configure(bg=BG)

        tk.Label(
            editor, text="Saved memory", bg=BG, fg=TEXT,
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=18, pady=(16, 5))
        tk.Label(
            editor, text="Jarvis can use these notes when memory is enabled.",
            bg=BG, fg=MUTED, font=("Segoe UI", 10)
        ).pack(anchor="w", padx=18, pady=(0, 12))

        text_box = tk.Text(
            editor, bg=PANEL, fg=TEXT, insertbackground=TEXT,
            font=("Consolas", 10), wrap="word", relief="flat",
            padx=12, pady=12
        )
        text_box.pack(fill="both", expand=True, padx=18, pady=(0, 12))
        text_box.insert("1.0", MEMORY_FILE.read_text(encoding="utf-8"))

        def save_memory():
            MEMORY_FILE.write_text(text_box.get("1.0", "end-1c"), encoding="utf-8")
            messagebox.showinfo("Memory saved", "Your memory notes were saved.", parent=editor)

        tk.Button(
            editor, text="Save memory", command=save_memory,
            bg=ACCENT, fg="white", activebackground="#0e8c6d",
            relief="flat", padx=16, pady=8, cursor="hand2"
        ).pack(anchor="e", padx=18, pady=(0, 16))

    def open_settings(self):
        settings = tk.Toplevel(self.root)
        settings.title("Jarvis Settings")
        settings.geometry("380x250")
        settings.configure(bg=BG)

        tk.Label(
            settings, text="Settings", bg=BG, fg=TEXT,
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 14))

        memory_var = tk.BooleanVar(value=self.memory_enabled)
        tk.Checkbutton(
            settings, text="Use saved memory in conversations",
            variable=memory_var, command=lambda: self._set_memory(memory_var.get()),
            bg=BG, fg=TEXT, selectcolor=PANEL, activebackground=BG,
            activeforeground=TEXT, font=("Segoe UI", 10)
        ).pack(anchor="w", padx=20, pady=8)

        tk.Label(
            settings, text=f"Model: {MODEL_NAME}\nOllama: {OLLAMA_URL}",
            bg=BG, fg=MUTED, justify="left", font=("Segoe UI", 9)
        ).pack(anchor="w", padx=20, pady=12)

    def _set_memory(self, enabled):
        self.memory_enabled = enabled
        self.memory_status.configure(text="Memory: on" if enabled else "Memory: off")


if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisGUI(root)
    root.mainloop()
