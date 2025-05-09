import socket
import threading
import tkinter as tk
from tkinter import ttk, simpledialog, scrolledtext, messagebox

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat")

        self.username = simpledialog.askstring("Nome de Usuário", "Escolha um nome:")
        if not self.username:
            master.quit()
            return

        self.master.title(f"Chat - Usuário: {self.username}")

        # Conectar ao servidor
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(("localhost", 12345))
            self.socket.send(self.username.encode())
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível conectar: {e}")
            master.quit()
            return

        # Abas
        self.tabs = ttk.Notebook(master)
        self.tabs.pack(expand=True, fill='both')

        # Aba pública
        self.public_tab = self.create_chat_tab("Geral")

        # Dicionário de abas privadas
        self.private_tabs = {}

        self.running = True
        threading.Thread(target=self.receive_messages, daemon=True).start()
    def insert_emoji(self, entry_widget):
        # Emojis populares - você pode personalizar ou expandir
        emojis = ["😀", "😂", "😍", "😎", "😭", "😡", "👍", "🎉", "❤️", "🔥"]
    
        # Nova janela flutuante
        emoji_win = tk.Toplevel(self.master)
        emoji_win.title("Escolha um emoji")
        emoji_win.geometry("200x150")

        for emoji in emojis:
            btn = tk.Button(emoji_win, text=emoji, font=("Arial", 14),
                command=lambda e=emoji: (entry_widget.insert(tk.END, e), emoji_win.destroy()))
            btn.pack(side=tk.LEFT, padx=5, pady=5)

    def create_chat_tab(self, title):
        frame = ttk.Frame(self.tabs)
        self.tabs.add(frame, text=title)

        text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state='disabled')
        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        entry = tk.Entry(frame)
        entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10), fill=tk.X, expand=True)
        entry.bind("<Return>", lambda event: self.send_message(entry, text_area, title))

        button = tk.Button(frame, text="Enviar", command=lambda: self.send_message(entry, text_area, title))
        button.pack(side=tk.RIGHT, padx=(0, 10), pady=(0, 10))
        emoji_button = tk.Button(frame, text="😊", command=lambda: self.insert_emoji(entry))
        emoji_button.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))

        return {"frame": frame, "text_area": text_area, "entry": entry}

    def send_message(self, entry, text_area, tab_name):
        msg = entry.get()
        if msg:
            if tab_name == "Geral":
                full_msg = msg
            else:
                full_msg = f"/msg {tab_name} {msg}"
            try:
                self.socket.send(full_msg.encode())
                if tab_name != "Geral":
                    self.display_message(f"Você (para {tab_name}): {msg}", tab_name)
                entry.delete(0, tk.END)
            except:
                self.display_message("Erro ao enviar mensagem.", tab_name)

    def receive_messages(self):
        while self.running:
            try:
                msg = self.socket.recv(1024).decode()
                if msg:
                    if msg.startswith("[PM de "):
                        user = msg.split(" ")[2].strip("]:")
                        self.display_message(msg, user)
                    else:
                        self.display_message(msg, "Geral")
            except:
                self.display_message("Desconectado do servidor.", "Geral")
                break

    def display_message(self, msg, tab_name):
        if tab_name not in self.private_tabs and tab_name != "Geral":
            self.private_tabs[tab_name] = self.create_chat_tab(tab_name)
        tab = self.public_tab if tab_name == "Geral" else self.private_tabs[tab_name]
        tab["text_area"].config(state='normal')
        tab["text_area"].insert(tk.END, msg + "\n")
        tab["text_area"].config(state='disabled')
        tab["text_area"].yview(tk.END)

    def on_close(self):
        self.running = False
        try:
            self.socket.close()
        except:
            pass
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.protocol("WM_DELETE_WINDOW", client.on_close)
    root.mainloop()
