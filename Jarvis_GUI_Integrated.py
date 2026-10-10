import datetime
import os
import subprocess
import threading
import webbrowser
import tkinter as tk
from tkinter import messagebox, simpledialog
from pathlib import Path

import requests


# These settings match the original Jarvis main.py.
MODEL_NAME = "gemma3:1b"
OLLAMA_URL = "http://localhost:11434/api/chat"

JARVIS_FOLDER = Path(__file__).parent
PRIVATE_DATA_FOLDER = JARVIS_FOLDER / "private_data"
PRIVATE_DATA_FOLDER.mkdir(exist_ok=True)
MEMORY_FILE = PRIVATE_DATA_FOLDER / "memory.txt"
MESSAGES_FILE = PRIVATE_DATA_FOLDER / "messages.txt"

commands = {
    "/open": "Opens a website or an application",
    "/weather": "Displays the current weather (not implemented yet)",
    "/help": "Displays a list of the current commands and their uses",
    "/files": "Opens your file explorer to a specific folder",
    "/chat": "Continues chatting with Jarvis in this window",
    "/memory": "Lets you view and change things you want the AI model to know",
    "/time": "Displays the current time and date",
    "/messages": "Opens the log of messages and responses",
    "/quit": "Closes Jarvis",
}

# Dark, ChatGPT-inspired palette.
BG = "#212121"
SIDEBAR = "#171717"
PANEL = "#2f2f2f"
HOVER = "#3b3b3b"
TEXT = "#f2f2f2"
MUTED = "#a8a8a8"
ACCENT = "#10a37f"
USER_BUBBLE = "#303030"


def ask_jarvis(message, memory=""):
    """Same Ollama API approach as the original Jarvis project."""
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": message},
                {"role": "system", "content": memory},
            ],
            "stream": False,
        },
        timeout=180,
    )
    response.raise_for_status()
    return response.json()["message"]["content"]


def message_log(message, answer, mode):
    """Keep the existing log format and private_data location."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(MESSAGES_FILE, "a", encoding="utf-8") as file:
        file.write(f"You: {message}\n Time: {current_time}\n")
        file.write(f"Jarvis: {answer}\n Time: {current_time}\n Mode: {mode}\n")


class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis AI")
        self.root.geometry("1100x760")
        self.root.minsize(760, 560)
        self.root.configure(bg=BG)
        self.busy = False
        self.memory_enabled = False
        self.conversation = []
        self.thinking_widget = None

        self.build_ui()
        self.show_welcome()
        self.entry.focus_set()
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def build_ui(self):
        sidebar = tk.Frame(self.root, bg=SIDEBAR, width=235)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="◈  Jarvis AI", bg=SIDEBAR, fg=TEXT,
                 font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=18, pady=(22, 24))
        self.side_button(sidebar, "＋  New chat", self.new_chat)
        self.side_button(sidebar, "▤  Memory", self.open_memory)
        self.side_button(sidebar, "⚙  Settings", self.open_settings)
        self.side_button(sidebar, "◷  Previous messages", self.show_messages)

        tk.Frame(sidebar, bg="#343434", height=1).pack(fill="x", padx=14, pady=18)
        tk.Label(sidebar, text="COMMANDS", bg=SIDEBAR, fg=MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(0, 8))
        self.side_button(sidebar, "/help  Command list", self.show_help)
        self.side_button(sidebar, "/open  App or website", self.open_target)
        self.side_button(sidebar, "/files  File explorer", self.open_folder)
        self.side_button(sidebar, "/messages  View logs", self.open_messages)

        self.status = tk.Label(sidebar, text="●  Ready", bg=SIDEBAR, fg="#75c99a",
                               font=("Segoe UI", 10))
        self.status.pack(side="bottom", anchor="w", padx=20, pady=20)

        main = tk.Frame(self.root, bg=BG)
        main.pack(side="left", fill="both", expand=True)
        topbar = tk.Frame(main, bg=BG, height=58)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        tk.Label(topbar, text="Jarvis", bg=BG, fg=TEXT,
                 font=("Segoe UI", 13, "bold")).pack(side="left", padx=25, pady=15)
        self.memory_label = tk.Label(topbar, text="Memory: off", bg=BG, fg=MUTED,
                                     font=("Segoe UI", 9))
        self.memory_label.pack(side="right", padx=22)

        area = tk.Frame(main, bg=BG)
        area.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(area, bg=BG, highlightthickness=0, borderwidth=0)
        scroll = tk.Scrollbar(area, orient="vertical", command=self.canvas.yview)
        self.messages_frame = tk.Frame(self.canvas, bg=BG)
        self.window_id = self.canvas.create_window((0, 0), window=self.messages_frame, anchor="nw")
        self.messages_frame.bind("<Configure>", lambda _e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(
            self.window_id, width=e.width))
        self.canvas.configure(yscrollcommand=scroll.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        bottom = tk.Frame(main, bg=BG)
        bottom.pack(fill="x", padx=24, pady=(12, 10))
        composer = tk.Frame(bottom, bg=PANEL, highlightbackground="#444444", highlightthickness=1)
        composer.pack(fill="x")
        self.entry = tk.Text(composer, height=3, wrap="word", bg=PANEL, fg=TEXT,
                             insertbackground=TEXT, relief="flat", borderwidth=0,
                             font=("Segoe UI", 11), padx=14, pady=13, undo=True)
        self.entry.pack(side="left", fill="both", expand=True)
        self.entry.bind("<Return>", self.enter_to_send)
        self.send_button = tk.Button(
            composer, text="↑", command=self.send_message, bg=ACCENT, fg="white",
            activebackground="#0e8c6d", activeforeground="white", relief="flat",
            borderwidth=0, font=("Segoe UI", 17, "bold"), width=3, cursor="hand2")
        self.send_button.pack(side="right", padx=9, pady=9, anchor="s")
        tk.Label(bottom, text="Local AI powered by Ollama • Enter to send • Shift+Enter for a new line",
                 bg=BG, fg=MUTED, font=("Segoe UI", 9)).pack(pady=(8, 0))

    def side_button(self, parent, label, command):
        tk.Button(parent, text=label, command=command, anchor="w", padx=14, pady=9,
                  bg=SIDEBAR, fg=TEXT, activebackground=HOVER, activeforeground=TEXT,
                  relief="flat", borderwidth=0, font=("Segoe UI", 10),
                  cursor="hand2").pack(fill="x", padx=10, pady=2)

    def show_welcome(self):
        self.welcome = tk.Frame(self.messages_frame, bg=BG)
        self.welcome.pack(fill="x", pady=(100, 30))
        tk.Label(self.welcome, text="What can I help with?", bg=BG, fg=TEXT,
                 font=("Segoe UI", 25, "bold")).pack()
        tk.Label(self.welcome, text="Ask Jarvis something, or type /help to see commands.",
                 bg=BG, fg=MUTED, font=("Segoe UI", 11)).pack(pady=(10, 0))

    def new_chat(self):
        if self.busy:
            return
        self.conversation = []
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
        self.show_welcome()
        self.entry.focus_set()

    def add_message(self, who, text, is_user=False):
        if hasattr(self, "welcome") and self.welcome.winfo_exists():
            self.welcome.destroy()
        outer = tk.Frame(self.messages_frame, bg=BG)
        outer.pack(fill="x", padx=28, pady=(14, 7))
        if is_user:
            tk.Label(outer, text="You", bg=BG, fg=TEXT,
                     font=("Segoe UI", 10, "bold")).pack(anchor="e", pady=(0, 5))
            bubble = tk.Frame(outer, bg=USER_BUBBLE)
            bubble.pack(anchor="e", padx=(45, 0))
            tk.Label(bubble, text=text, bg=USER_BUBBLE, fg=TEXT, justify="left",
                     anchor="w", wraplength=max(280, self.canvas.winfo_width() - 180), font=("Segoe UI", 11),
                     padx=15, pady=11).pack()
        else:
            head = tk.Frame(outer, bg=BG)
            head.pack(fill="x", pady=(0, 5))
            tk.Label(head, text="◈", bg=BG, fg=ACCENT,
                     font=("Segoe UI", 14, "bold")).pack(side="left", padx=(0, 9))
            tk.Label(head, text=who, bg=BG, fg=TEXT,
                     font=("Segoe UI", 10, "bold")).pack(side="left")
            label = tk.Label(outer, text=text, bg=BG, fg=TEXT, justify="left",
                             anchor="w", wraplength=max(300, self.canvas.winfo_width() - 120), font=("Segoe UI", 11))
            label.pack(fill="x", padx=(28, 8), pady=(0, 8))
            return label
        self.root.after(50, lambda: self.canvas.yview_moveto(1.0))
        return None

    def enter_to_send(self, event):
        if event.state & 0x0001:  # Shift+Enter
            return None
        self.send_message()
        return "break"

    def send_message(self):
        if self.busy:
            return
        text = self.entry.get("1.0", "end-1c").strip()
        if not text:
            return
        self.entry.delete("1.0", "end")
        self.add_message("You", text, True)

        # Crucially: commands are routed here and are NEVER sent to Ollama as chat text.
        if text.startswith("/"):
            self.handle_command(text.strip())
            return

        self.ask_async(text, mode="default")

    def handle_command(self, command):
        parts = command.lower().split()
        if not parts:
            return
        base = parts[0]

        if base == "/chat":
            self.add_message("Jarvis", "You're already in chat. Type a message normally to talk to the AI.")
        elif base == "/help":
            self.show_help()
        elif base == "/time":
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.add_message("Jarvis", f"The current time and date is: {current_time}")
        elif base == "/memory":
            parts = command.split(maxsplit=1)
            self.memory_menu(parts[1] if len(parts) > 1 else "")
        elif base == "/messages":
            self.show_messages()
        elif base == "/files":
            self.open_folder()
        elif base == "/open":
            self.open_target()
        elif base == "/weather":
            self.add_message("Jarvis", "The /weather command is still a placeholder in your original code, so it isn't implemented yet.")
        elif base == "/quit":
            self.root.destroy()
        elif base == "/exit":
            self.add_message("Jarvis", "You're in the desktop app, so use /quit to close Jarvis or keep chatting here.")
        else:
            self.add_message("Jarvis", f"'{base}' isn't a supported command. Type /help to see the command list.")

    def show_help(self):
        lines = [f"{name} — {description}" for name, description in commands.items()]
        self.add_message("Jarvis", "Here are Jarvis's commands:\n\n" + "\n".join(lines))

    def ask_async(self, message, mode="default"):
        if self.busy:
            return
        self.busy = True
        self.send_button.configure(state="disabled", text="…")
        self.status.configure(text="●  Thinking…", fg="#e6bd67")
        self.thinking_widget = self.add_message("Jarvis", "Thinking…")
        memory = ""
        use_memory = mode in ("read", "write") or self.memory_enabled
        if use_memory and MEMORY_FILE.exists():
            try:
                memory = MEMORY_FILE.read_text(encoding="utf-8")
            except OSError as error:
                self.finish_answer(None, f"Could not read saved memory: {error}")
                return
        threading.Thread(target=self._worker, args=(message, memory, mode), daemon=True).start()

    def _worker(self, message, memory, mode):
        try:
            answer = ask_jarvis(message, memory)
            try:
                message_log(message, answer, mode)
            except OSError as error:
                self.root.after(0, self.finish_answer, answer, f"Response received, but message log could not be saved: {error}")
                return
            self.root.after(0, self.finish_answer, answer, None)
        except requests.exceptions.ConnectionError:
            self.root.after(0, self.finish_answer, None,
                            "Couldn't connect to Ollama. Make sure Ollama is running.")
        except requests.exceptions.Timeout:
            self.root.after(0, self.finish_answer, None,
                            "Jarvis took too long to respond. Try again.")
        except requests.exceptions.HTTPError as error:
            self.root.after(0, self.finish_answer, None, f"Ollama request failed: {error}")
        except (ValueError, KeyError, TypeError) as error:
            self.root.after(0, self.finish_answer, None, f"Ollama returned an unexpected response: {error}")
        except Exception as error:
            self.root.after(0, self.finish_answer, None, str(error))

    def finish_answer(self, answer, error):
        if self.thinking_widget is not None and self.thinking_widget.winfo_exists():
            self.thinking_widget.destroy()
        if error and answer is None:
            self.add_message("Jarvis", "Error: " + error)
            self.status.configure(text="●  Needs attention", fg="#e6bd67")
        elif error:
            self.add_message("Jarvis", answer)
            self.add_message("Jarvis", error)
            self.status.configure(text="●  Needs attention", fg="#e6bd67")
        else:
            self.add_message("Jarvis", answer)
            self.status.configure(text="●  Ready", fg="#75c99a")
        self.busy = False
        self.send_button.configure(state="normal", text="↑")
        self.entry.focus_set()

    def memory_menu(self, requested_mode=""):
        """Choose the existing memory read/write workflow in a GUI panel."""
        window = tk.Toplevel(self.root)
        window.title("Memory mode")
        window.geometry("360x245")
        window.configure(bg=BG)
        window.transient(self.root)
        tk.Label(window, text="Choose a memory mode", bg=BG, fg=TEXT,
                 font=("Segoe UI", 15, "bold")).pack(anchor="w", padx=20, pady=(20, 14))
        tk.Label(window, text="Read uses saved notes. Write saves a note, then asks your question.",
                 bg=BG, fg=MUTED, wraplength=315, justify="left").pack(anchor="w", padx=20, pady=(0, 12))
        row = tk.Frame(window, bg=BG)
        row.pack(fill="x", padx=20, pady=8)
        tk.Button(row, text="Read", command=lambda: (window.destroy(), self.memory_prompt("read")),
                  bg=ACCENT, fg="white", relief="flat", padx=18, pady=8).pack(side="left", padx=(0, 8))
        tk.Button(row, text="Write", command=lambda: (window.destroy(), self.memory_prompt("write")),
                  bg=PANEL, fg=TEXT, relief="flat", padx=18, pady=8).pack(side="left", padx=8)
        tk.Button(row, text="Return", command=window.destroy, bg=PANEL, fg=TEXT,
                  relief="flat", padx=18, pady=8).pack(side="left", padx=8)
        if requested_mode.lower() in ("read", "write"):
            window.after(0, lambda: (window.destroy(), self.memory_prompt(requested_mode.lower())))
        elif requested_mode:
            messagebox.showerror("Invalid mode", "Use /memory, /memory read, or /memory write.", parent=window)

    def memory_prompt(self, mode):
        if mode == "read":
            prompt = simpledialog.askstring("Memory read mode", "What should Jarvis answer using memory?", parent=self.root)
            if prompt and prompt.strip():
                self.add_message("You", f"[Memory read] {prompt.strip()}", True)
                self.ask_async(prompt.strip(), mode="read")
            return
        note = simpledialog.askstring("Memory write mode", "What would you like to add to memory?", parent=self.root)
        if not note or not note.strip():
            return
        try:
            with MEMORY_FILE.open("a", encoding="utf-8") as file:
                file.write("\n" + note.strip() + "\n")
        except OSError as error:
            messagebox.showerror("Could not save memory", str(error), parent=self.root)
            return
        self.add_message("Jarvis", "Saved that note to memory.")
        prompt = simpledialog.askstring("Memory write mode", "What would you like to ask Jarvis next?", parent=self.root)
        if prompt and prompt.strip():
            self.add_message("You", prompt.strip(), True)
            self.ask_async(prompt.strip(), mode="write")

    def open_memory(self):
        MEMORY_FILE.touch(exist_ok=True)
        editor = tk.Toplevel(self.root)
        editor.title("Jarvis Memory")
        editor.geometry("620x500")
        editor.configure(bg=BG)
        tk.Label(editor, text="Saved memory", bg=BG, fg=TEXT,
                 font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=18, pady=(16, 8))
        box = tk.Text(editor, bg=PANEL, fg=TEXT, insertbackground=TEXT,
                      font=("Consolas", 10), wrap="word", relief="flat", padx=12, pady=12)
        box.pack(fill="both", expand=True, padx=18, pady=(0, 12))
        try:
            box.insert("1.0", MEMORY_FILE.read_text(encoding="utf-8"))
        except OSError as error:
            messagebox.showerror("Could not read memory", str(error), parent=editor)

        def save():
            try:
                MEMORY_FILE.write_text(box.get("1.0", "end-1c"), encoding="utf-8")
            except OSError as error:
                messagebox.showerror("Could not save memory", str(error), parent=editor)
                return
            messagebox.showinfo("Memory saved", "Your memory notes were saved.", parent=editor)
        tk.Button(editor, text="Save memory", command=save, bg=ACCENT, fg="white",
                  relief="flat", padx=16, pady=8).pack(anchor="e", padx=18, pady=(0, 16))

    def open_settings(self):
        window = tk.Toplevel(self.root)
        window.title("Jarvis Settings")
        window.geometry("390x230")
        window.configure(bg=BG)
        tk.Label(window, text="Settings", bg=BG, fg=TEXT,
                 font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=20, pady=(20, 14))
        var = tk.BooleanVar(value=self.memory_enabled)
        tk.Checkbutton(window, text="Use saved memory in conversations", variable=var,
                       command=lambda: self.set_memory(var.get()), bg=BG, fg=TEXT,
                       selectcolor=PANEL, activebackground=BG, activeforeground=TEXT).pack(anchor="w", padx=20)
        tk.Label(window, text=f"Model: {MODEL_NAME}\nOllama: {OLLAMA_URL}",
                 bg=BG, fg=MUTED, justify="left").pack(anchor="w", padx=20, pady=14)

    def set_memory(self, enabled):
        self.memory_enabled = enabled
        self.memory_label.configure(text="Memory: on" if enabled else "Memory: off")

    def show_messages(self):
        MESSAGES_FILE.touch(exist_ok=True)
        viewer = tk.Toplevel(self.root)
        viewer.title("Jarvis conversation history")
        viewer.geometry("760x560")
        viewer.configure(bg=BG)
        tk.Label(viewer, text="Previous messages", bg=BG, fg=TEXT,
                 font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=18, pady=14)
        body = tk.Frame(viewer, bg=BG)
        body.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        box = tk.Text(body, bg=PANEL, fg=TEXT, insertbackground=TEXT, wrap="word",
                      font=("Consolas", 10), relief="flat", padx=12, pady=12)
        scroll = tk.Scrollbar(body, command=box.yview)
        box.configure(yscrollcommand=scroll.set)
        box.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        try:
            box.insert("1.0", MESSAGES_FILE.read_text(encoding="utf-8") or "No messages have been logged yet.")
        except OSError as error:
            box.insert("1.0", f"Could not read the message log: {error}")
        box.configure(state="disabled")

    def open_messages(self):
        self.show_messages()

    def open_folder(self):
        choice = simpledialog.askstring("Open folder", "Which folder? (downloads, documents, gallery)",
                                        parent=self.root)
        if not choice:
            return
        one_drive = os.environ.get("OneDrive")
        documents = Path(one_drive) / "Documents" if one_drive else Path.home() / "Documents"
        gallery = Path(one_drive) / "Gallery" if one_drive else Path.home() / "Pictures"
        folders = {"downloads": Path.home() / "Downloads", "documents": documents, "gallery": gallery}
        folder = folders.get(choice.strip().lower())
        if folder and folder.exists():
            if hasattr(os, "startfile"):
                os.startfile(str(folder))
            else:
                subprocess.Popen(["xdg-open", str(folder)])
        elif choice.strip().lower() in folders:
            messagebox.showerror("Folder not found", f"Could not find:\n{folder}", parent=self.root)
        else:
            messagebox.showerror("Unsupported folder", "Choose downloads, documents, or gallery.", parent=self.root)

    def open_target(self):
        target = simpledialog.askstring("Open", "Open an application or a website? (app / website)",
                                        parent=self.root)
        if not target:
            return
        target = target.strip().lower()
        if target in ("website", "open website", "open a website"):
            url = simpledialog.askstring("Open website", "Website name (e.g. youtube):", parent=self.root)
            if not url:
                return
            domain = simpledialog.askstring("Open website", "Domain ending (e.g. .com, .gg, .vercel):",
                                            initialvalue=".com", parent=self.root)
            if not domain:
                return
            if domain.strip().lower() == ".vercel":
                webbrowser.open(f"https://{url.strip()}.vercel.app")
            else:
                webbrowser.open(f"https://www.{url.strip()}{domain.strip()}")
            self.add_message("Jarvis", f"Opened website: {url.strip()}{domain.strip()}")
        elif target in ("app", "application", "open an app", "open an application"):
            app = simpledialog.askstring("Open application", "Application name:", parent=self.root)
            if not app:
                return
            app = app.strip().lower()
            apps = {
                "calculator": "calc", "notepad": "notepad", "paint": "mspaint",
                "microsoft paint": "mspaint", "command prompt": "cmd", "cmd": "cmd",
                "file explorer": "explorer", "explorer": "explorer", "task manager": "taskmgr",
                "settings": "ms-settings:",
            }
            if app in ("microsoft edge", "edge"):
                edge = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
                if edge.exists():
                    subprocess.Popen([str(edge)])
                else:
                    subprocess.Popen(["cmd", "/c", "start", "", "msedge"])
            elif app in apps:
                subprocess.Popen(apps[app], shell=True)
            else:
                messagebox.showerror("Unsupported app", "That app isn't in Jarvis's supported list.", parent=self.root)
                return
            self.add_message("Jarvis", f"Opened application: {app}")
        else:
            messagebox.showerror("Choose app or website", "Enter 'app' or 'website'.", parent=self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisGUI(root)
    root.mainloop()
