import os
import platform
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import getpass

# --- Hotspot control functions ---
def start_hotspot(ssid, password):
    system = platform.system()

    if system == "Windows":
        os.system(f'netsh wlan set hostednetwork mode=allow ssid={ssid} key={password}')
        os.system('netsh wlan start hostednetwork')
        messagebox.showinfo("Hotspot", "✅ Hotspot started on Windows!")

    elif system == "Linux":
        os.system(f"nmcli dev wifi hotspot ifname wlan0 ssid {ssid} password {password}")
        messagebox.showinfo("Hotspot", "✅ Hotspot started on Linux!")

    elif system == "Darwin":  # macOS
        os.system(f"networksetup -createNetworkService {ssid} en0")
        messagebox.showwarning("Hotspot", "⚠️ Hotspot partially created.\nEnable Internet Sharing in System Preferences.")
    else:
        messagebox.showerror("Error", "❌ Unsupported OS")

def stop_hotspot():
    system = platform.system()

    if system == "Windows":
        os.system('netsh wlan stop hostednetwork')
        messagebox.showinfo("Hotspot", "🛑 Hotspot stopped on Windows.")

    elif system == "Linux":
        os.system("nmcli connection down Hotspot")
        messagebox.showinfo("Hotspot", "🛑 Hotspot stopped on Linux.")

    elif system == "Darwin":
        messagebox.showwarning("Hotspot", "⚠️ Stop hotspot manually via System Preferences on macOS.")
    else:
        messagebox.showerror("Error", "❌ Unsupported OS")


# --- GUI ---
def start():
    ssid = ssid_var.get()
    password = password_var.get()
    if len(ssid) < 1 or len(password) < 8:
        messagebox.showerror("Error", "SSID cannot be empty and password must be at least 8 characters.")
        return
    start_hotspot(ssid, password)

def stop():
    stop_hotspot()

root = tk.Tk()
root.title("Cross-Platform Hotspot Manager")
root.geometry("400x220")
root.resizable(False, False)

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 12), padding=8)
style.configure("TLabel", font=("Segoe UI", 11))

ssid_var = tk.StringVar()
password_var = tk.StringVar()

# Widgets
ttk.Label(root, text="Hotspot SSID:").pack(pady=5)
ssid_entry = ttk.Entry(root, textvariable=ssid_var, width=30)
ssid_entry.pack(pady=5)

ttk.Label(root, text="Password:").pack(pady=5)
password_entry = ttk.Entry(root, textvariable=password_var, show="*", width=30)
password_entry.pack(pady=5)

ttk.Button(root, text="Start Hotspot", command=start).pack(pady=10)
ttk.Button(root, text="Stop Hotspot", command=stop).pack(pady=5)

root.mainloop()
