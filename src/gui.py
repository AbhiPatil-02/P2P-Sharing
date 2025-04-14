import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
import threading
import os
import peer
import chat
import file_transfer
from animation import animator
from config import config
from utils import format_bytes
from PIL import Image, ImageTk
import sv_ttk

class P2PGUI:
    def __init__(self, root):
        self.root = root
        self.colors = {
            'primary': '#6a1b9a',
            'secondary': '#0288d1',
            'background': '#f5f5f5',
            'text': '#212121',
            'accent': '#ffab00',
            'success': '#388e3c',
            'error': '#d32f2f',
            'chat_bg': '#ffffff',
            'chat_fg': '#000000',
            'status_bar': '#e0e0e0'
        }
        animator.init_root(root)
        self._setup_window()
        self._create_variables()
        self._build_connect_screen()

    def _setup_window(self):
        self.root.title("✨ P2P Share - Secure File Transfer & Chat")
        self.root.geometry("800x700")
        self.root.minsize(700, 600)
        sv_ttk.set_theme("dark")

        try:
            if os.path.exists("assets/icon.png"):
                img = Image.open("assets/icon.png")
                icon = ImageTk.PhotoImage(img)
                self.root.tk.call('wm', 'iconphoto', self.root._w, icon)
        except:
            pass

    def _create_variables(self):
        self.peer_ip = tk.StringVar()
        self.mode = tk.StringVar()
        self.chat_input = tk.StringVar()
        self.conn = None
        self.chat_handler = None
        self.progress = tk.DoubleVar()
        self.style = ttk.Style()
        self.style.configure('Accent.TButton', foreground='white', background=self.colors['secondary'])

    def _build_connect_screen(self):
        self._clear_window()
        self.root.configure(bg=self.colors['background'])

        header = tk.Label(self.root, 
                         text="🌐 P2P Share", 
                         font=('Helvetica', 24, 'bold'),
                         bg=self.colors['primary'],
                         fg='white')
        header.pack(fill=tk.X, pady=(0, 20))

        conn_frame = tk.LabelFrame(self.root, 
                                  text=" ⚡ Connection Settings ",
                                  font=('Helvetica', 11, 'bold'),
                                  bg=self.colors['background'],
                                  fg=self.colors['primary'],
                                  relief=tk.GROOVE,
                                  borderwidth=3)
        conn_frame.pack(padx=20, pady=10, fill=tk.X)

        tk.Label(conn_frame, text="Enter Peer IP:", 
                 font=('Helvetica', 11),
                 bg=self.colors['background'],
                 fg=self.colors['text']).pack(pady=5)

        ip_entry = tk.Entry(conn_frame, textvariable=self.peer_ip, width=30,
                            bg='white', fg='black', insertbackground='black')
        ip_entry.pack()
        ip_entry.focus()

        ttk.Label(conn_frame, text="Select Mode:", font=('Helvetica', 11)).pack(pady=10)

        btn_frame = ttk.Frame(conn_frame)
        btn_frame.pack()

        for text, mode in [("📤 Send Mode", "send"), ("📥 Receive Mode", "receive")]:
            button = tk.Button(btn_frame, text=text, bg=self.colors['secondary'], fg='white',
                               command=lambda m=mode: self._setup_mode(m))
            button.pack(side=tk.LEFT, padx=5)
            button.bind("<Enter>", lambda e, b=button: b.config(bg=self.colors['accent']))
            button.bind("<Leave>", lambda e, b=button: b.config(bg=self.colors['secondary']))

        ttk.Label(self.root, text="🔒 Secure P2P File Sharing • Drag & Drop Supported",
                 font=('Helvetica', 9)).pack(side=tk.BOTTOM, pady=(20, 0))

    def _setup_mode(self, mode):
        self.mode.set(mode)
        ip = self.peer_ip.get().strip()

        if mode == "receive":
            try:
                self.conn = peer.start_server()
                self.chat_handler = chat.ChatHandler(
                    is_server=True, 
                    peer_ip=None, 
                    on_message_callback=self._append_chat
                )
                self.peer_ip.set(self.conn.getpeername()[0])
                self._build_main_window()
                threading.Thread(target=self._receive_loop_logic, daemon=True).start()
            except peer.PeerConnectionError as e:
                messagebox.showerror("Connection Error", str(e))
        else:
            if not ip:
                messagebox.showerror("Error", "Please enter a valid IP address")
                return

            try:
                self.conn = peer.connect_to_peer(ip)
                if self.conn:
                    self.chat_handler = chat.ChatHandler(
                        is_server=False, 
                        peer_ip=ip, 
                        on_message_callback=self._append_chat
                    )
                    self._build_main_window()
            except Exception as e:
                messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")

    def _build_main_window(self):
        self._clear_window()

        main_container = ttk.Frame(self.root, padding=10)
        main_container.pack(expand=True, fill=tk.BOTH)

        status_frame = ttk.Frame(main_container)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        self.status_label = ttk.Label(status_frame, 
            text=f"🟢 Connected to: {self.peer_ip.get() or 'Peer'} ({self.mode.get().capitalize()} Mode)",
            font=("Helvetica", 10))
        self.status_label.pack(side=tk.LEFT)

        chat_frame = tk.LabelFrame(main_container, text=" 💬 Live Chat ",
                                 font=('Helvetica', 11, 'bold'),
                                 bg=self.colors['background'],
                                 fg=self.colors['secondary'],
                                 relief=tk.GROOVE,
                                 borderwidth=3)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.chat_box = scrolledtext.ScrolledText(
            chat_frame, 
            bg=self.colors['chat_bg'],
            fg=self.colors['chat_fg'],
            insertbackground=self.colors['chat_fg'],
            font=('Helvetica', 10),
            padx=10,
            pady=10,
            width=60, 
            height=15, 
            state='disabled'
        )
        self.chat_box.pack(fill=tk.BOTH, expand=True)

        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(fill=tk.X, pady=(10, 0))

        chat_entry = ttk.Entry(input_frame, textvariable=self.chat_input, width=50)
        chat_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        chat_entry.bind('<Return>', lambda e: self._send_chat())
        chat_entry.focus()

        ttk.Button(input_frame, text="Send", command=self._send_chat).pack(side=tk.RIGHT)

        if self.mode.get() == "send":
            self._build_sender_interface(main_container)
        else:
            self._build_receiver_interface(main_container)

    def _build_sender_interface(self, parent):
        transfer_frame = ttk.LabelFrame(parent, text="📁 File Transfer", padding=10)
        transfer_frame.pack(fill=tk.X, pady=10)

        btn_frame = ttk.Frame(transfer_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(btn_frame, text="📂 Choose File", 
                   command=self._choose_file).pack(side=tk.LEFT, padx=5)

        self._create_progress_bar(transfer_frame)

        self.drop_frame = tk.Label(
            transfer_frame,
            text="📁 Drag and Drop Files Here",
            relief=tk.RIDGE,
            width=50,
            height=4,
            font=('Helvetica', 10)
        )
        self.drop_frame.pack(fill=tk.X, pady=10)
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self._on_file_dropped)

    def _build_receiver_interface(self, parent):
        transfer_frame = ttk.LabelFrame(parent, text="📥 Incoming Files", padding=10)
        transfer_frame.pack(fill=tk.X, pady=10)
        ttk.Label(transfer_frame, text="⏳ Waiting for files to be sent...", 
                  font=('Helvetica', 11)).pack(pady=10)

    def _clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def _choose_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self._send_file(filepath)

    def _on_file_dropped(self, event):
        file = event.data.strip().strip('{').strip('}')
        if os.path.isfile(file):
            self._send_file(file)

    def _send_file(self, filepath):
        filename = os.path.basename(filepath)
        self._append_chat(f"📤 You: Sending file: {filename}", is_system=True)
        threading.Thread(target=self._send_file_logic, args=(filepath,), daemon=True).start()

    def _send_file_logic(self, filepath):
        self.progress.set(0)
        success, message = file_transfer.send_file(
            self.conn, 
            filepath, 
            progress_callback=self._update_progress
        )
        animator.show_animation("success" if success else "error", message)
        self._append_chat(message, is_system=True)

    def _receive_loop_logic(self):
        file_transfer.receive_loop(self.conn, callback=self._on_file_received)

    def _on_file_received(self, message):
        if message.startswith("✨"):
            animator.show_animation("transfer", message[2:])
        self._append_chat(message, is_system=True)

    def _send_chat(self):
        msg = self.chat_input.get().strip()
        if msg:
            self._append_chat(f"👤 You: {msg}")
            self.chat_input.set("")
            if self.chat_handler:
                self.chat_handler.send(msg)

    def _append_chat(self, msg, is_system=False):
        self.chat_box.configure(state='normal')
        if "You:" in msg:
            self.chat_box.tag_config('you', foreground=self.colors['secondary'])
            self.chat_box.insert(tk.END, msg + '\n', 'you')
        elif "Peer:" in msg:
            self.chat_box.tag_config('peer', foreground=self.colors['accent'])
            self.chat_box.insert(tk.END, msg + '\n', 'peer')
        elif is_system:
            self.chat_box.tag_config('system', foreground=self.colors['success'])
            self.chat_box.insert(tk.END, msg + '\n', 'system')
        else:
            self.chat_box.insert(tk.END, msg + '\n')
        self.chat_box.configure(state='disabled')
        self.chat_box.yview(tk.END)

    def _create_progress_bar(self, parent):
        self.progress_frame = ttk.Frame(parent)
        self.progress_frame.pack(fill=tk.X, pady=5)

        self.progress_label = tk.Label(self.progress_frame, 
                                        text="📊 Progress: 0%",
                                        font=('Helvetica', 9))
        self.progress_label.pack(anchor=tk.W)

        self.progress_bar = ttk.Progressbar(self.progress_frame, 
                                            length=300, 
                                            variable=self.progress, 
                                            maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)

    def _update_progress(self, sent, total):
        percent = (sent / total) * 100
        self.progress.set(percent)
        self.progress_label.config(text=f"📊 Progress: {int(percent)}%")
        if percent >= 100:
            self.progress_label.config(text="🎉 Transfer complete!", fg=self.colors['success'])

def start_gui():
    os.makedirs(config.SHARED_FOLDER, exist_ok=True)
    root = TkinterDnD.Tk()
    sv_ttk.set_theme("dark")
    gui = P2PGUI(root)
    root.mainloop()
