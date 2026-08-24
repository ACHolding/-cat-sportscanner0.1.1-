#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AC Kondo's Port Scanner 0.1
Single-file Tkinter port scanner.
Blue hue on black, black buttons — educational use only.
files = OFF, all in RAM.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import socket
import time

class ACKondoPortScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("AC Kondo's Port Scanner 0.1")
        self.root.geometry("600x400")
        self.root.minsize(500, 350)
        self.root.configure(bg='black')
        self.running = False
        self.scan_thread = None

        # ===== Title =====
        title = tk.Label(
            root,
            text="AC KONDO'S PORT SCANNER 0.1",
            fg='blue',
            bg='black',
            font=('Courier', 18, 'bold')
        )
        title.pack(pady=(12, 4))

        sub = tk.Label(
            root,
            text="Network Port Discovery — Educational Only",
            fg='#4488ff',
            bg='black',
            font=('Courier', 10)
        )
        sub.pack(pady=(0, 8))

        # ===== Input Frame =====
        frame = tk.Frame(root, bg='black')
        frame.pack(pady=6)

        # Target
        tk.Label(frame, text="Target:", fg='blue', bg='black', font=('Courier', 11)).grid(row=0, column=0, padx=4, pady=4, sticky='e')
        self.target_entry = tk.Entry(frame, width=20, fg='blue', bg='black', insertbackground='blue', font=('Courier', 11))
        self.target_entry.grid(row=0, column=1, padx=4, pady=4, sticky='w')
        self.target_entry.insert(0, "127.0.0.1")

        # Start port
        tk.Label(frame, text="Start Port:", fg='blue', bg='black', font=('Courier', 11)).grid(row=0, column=2, padx=4, pady=4, sticky='e')
        self.start_port = tk.Entry(frame, width=6, fg='blue', bg='black', insertbackground='blue', font=('Courier', 11))
        self.start_port.grid(row=0, column=3, padx=4, pady=4, sticky='w')
        self.start_port.insert(0, "1")

        # End port
        tk.Label(frame, text="End Port:", fg='blue', bg='black', font=('Courier', 11)).grid(row=0, column=4, padx=4, pady=4, sticky='e')
        self.end_port = tk.Entry(frame, width=6, fg='blue', bg='black', insertbackground='blue', font=('Courier', 11))
        self.end_port.grid(row=0, column=5, padx=4, pady=4, sticky='w')
        self.end_port.insert(0, "1024")

        # Timeout
        tk.Label(frame, text="Timeout (s):", fg='blue', bg='black', font=('Courier', 11)).grid(row=1, column=0, padx=4, pady=4, sticky='e')
        self.timeout_entry = tk.Entry(frame, width=6, fg='blue', bg='black', insertbackground='blue', font=('Courier', 11))
        self.timeout_entry.grid(row=1, column=1, padx=4, pady=4, sticky='w')
        self.timeout_entry.insert(0, "0.5")

        # Threads (optional, but keep simple)
        tk.Label(frame, text="Threads:", fg='blue', bg='black', font=('Courier', 11)).grid(row=1, column=2, padx=4, pady=4, sticky='e')
        self.threads_entry = tk.Entry(frame, width=6, fg='blue', bg='black', insertbackground='blue', font=('Courier', 11))
        self.threads_entry.grid(row=1, column=3, padx=4, pady=4, sticky='w')
        self.threads_entry.insert(0, "50")

        # ===== Buttons =====
        btn_frame = tk.Frame(root, bg='black')
        btn_frame.pack(pady=10)

        self.scan_btn = tk.Button(
            btn_frame,
            text="🔍 SCAN",
            fg='blue',
            bg='black',
            activeforeground='cyan',
            activebackground='#1a1a1a',
            font=('Courier', 12, 'bold'),
            command=self.start_scan,
            relief='raised',
            bd=3,
            padx=18,
            pady=6
        )
        self.scan_btn.pack(side='left', padx=10)

        self.stop_btn = tk.Button(
            btn_frame,
            text="🛑 STOP",
            fg='blue',
            bg='black',
            activeforeground='red',
            activebackground='#1a1a1a',
            font=('Courier', 12, 'bold'),
            command=self.stop_scan,
            relief='raised',
            bd=3,
            padx=18,
            pady=6
        )
        self.stop_btn.pack(side='left', padx=10)

        self.clear_btn = tk.Button(
            btn_frame,
            text="🧹 CLEAR",
            fg='blue',
            bg='black',
            activeforeground='cyan',
            activebackground='#1a1a1a',
            font=('Courier', 12, 'bold'),
            command=self.clear_output,
            relief='raised',
            bd=3,
            padx=15,
            pady=6
        )
        self.clear_btn.pack(side='left', padx=10)

        # ===== Status =====
        self.status = tk.Label(
            root,
            text="🐱 Ready. Enter target and port range.",
            fg='#4488ff',
            bg='black',
            font=('Courier', 10)
        )
        self.status.pack(pady=5)

        # ===== Output =====
        self.output = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            width=70,
            height=12,
            fg='blue',
            bg='black',
            insertbackground='blue',
            font=('Courier', 10),
            bd=2,
            relief='sunken'
        )
        self.output.pack(padx=15, pady=8, fill=tk.BOTH, expand=True)

        # Tags
        self.output.tag_configure('header', foreground='cyan', font=('Courier', 10, 'bold'))
        self.output.tag_configure('info', foreground='#4488ff')
        self.output.tag_configure('open', foreground='lightgreen')
        self.output.tag_configure('error', foreground='red')

        # ===== Init =====
        self.log("AC Kondo's Port Scanner 0.1 — LOADED", 'header')
        self.log("=" * 55, 'header')
        self.log("Educational port scanner. Use only on your own network.", 'info')
        self.log("⚠️ Unauthorized scanning is illegal.", 'error')
        self.log("=" * 55, 'header')

    def log(self, msg, tag='info'):
        self.output.insert(tk.END, msg + "\n", tag)
        self.output.see(tk.END)
        self.root.update_idletasks()

    def clear_output(self):
        self.output.delete(1.0, tk.END)
        self.log("🧹 Output cleared.", 'header')

    def scan_port(self, ip, port, timeout):
        """Check if a TCP port is open."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False

    def worker(self, ip, port_range, timeout, thread_id):
        """Worker thread to scan a range of ports."""
        start, end = port_range
        for port in range(start, end + 1):
            if not self.running:
                break
            if self.scan_port(ip, port, timeout):
                self.log(f"OPEN  {ip}:{port}", 'open')
            # Optionally print closed ports if you want, but keep quiet

    def start_scan(self):
        if self.running:
            messagebox.showwarning("Already Running", "A scan is already in progress.")
            return

        # Validate inputs
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showerror("Error", "Please enter a target IP or hostname.")
            return

        try:
            start_port = int(self.start_port.get().strip())
            end_port = int(self.end_port.get().strip())
            if start_port < 1 or end_port > 65535 or start_port > end_port:
                raise ValueError
        except:
            messagebox.showerror("Invalid Port Range", "Ports must be 1–65535 and start <= end.")
            return

        try:
            timeout = float(self.timeout_entry.get().strip())
            if timeout <= 0:
                raise ValueError
        except:
            messagebox.showerror("Invalid Timeout", "Timeout must be a positive number.")
            return

        try:
            threads = int(self.threads_entry.get().strip())
            if threads < 1 or threads > 200:
                raise ValueError
        except:
            messagebox.showerror("Invalid Threads", "Threads must be 1–200.")
            return

        # Resolve hostname if needed
        try:
            ip = socket.gethostbyname(target)
        except:
            messagebox.showerror("Resolution Failed", f"Could not resolve {target}.")
            return

        total_ports = end_port - start_port + 1
        self.log(f"🐱 Scanning {ip} ({target}) from {start_port} to {end_port}", 'header')
        self.log(f"   Threads: {threads}  Timeout: {timeout}s", 'info')
        self.log("-" * 50, 'header')

        self.running = True
        self.scan_btn.config(state='disabled')
        self.status.config(text=f"🐱 Scanning {ip}...")

        # Split port range into chunks for threads
        chunk_size = max(1, total_ports // threads)
        port_chunks = []
        for i in range(0, total_ports, chunk_size):
            chunk_start = start_port + i
            chunk_end = min(start_port + i + chunk_size - 1, end_port)
            port_chunks.append((chunk_start, chunk_end))

        self.threads_list = []
        for idx, (p_start, p_end) in enumerate(port_chunks):
            t = threading.Thread(target=self.worker, args=(ip, (p_start, p_end), timeout, idx+1), daemon=True)
            t.start()
            self.threads_list.append(t)

        # Monitor thread to detect completion
        self.monitor = threading.Thread(target=self.monitor_scan, daemon=True)
        self.monitor.start()

    def monitor_scan(self):
        while self.running:
            all_done = True
            for t in self.threads_list:
                if t.is_alive():
                    all_done = False
                    break
            if all_done:
                self.root.after(0, self.scan_finished)
                break
            time.sleep(0.5)

    def scan_finished(self):
        self.running = False
        self.scan_btn.config(state='normal')
        self.status.config(text="🐱 Scan complete.")
        self.log("\n✅ SCAN FINISHED", 'open')
        self.log("=" * 55, 'header')

    def stop_scan(self):
        if not self.running:
            return
        self.running = False
        self.status.config(text="🐱 Stopping...")
        self.log("\n🛑 STOPPING scan...", 'error')
        self.scan_btn.config(state='normal')
        self.root.after(1000, lambda: self.log("✅ Scan stopped by user.", 'error'))

    def on_closing(self):
        self.running = False
        self.root.destroy()

# ===== MAIN =====
if __name__ == "__main__":
    root = tk.Tk()
    app = ACKondoPortScanner(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
