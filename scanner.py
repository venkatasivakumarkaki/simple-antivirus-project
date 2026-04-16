import os
import hashlib
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog


def get_file_hash(filepath):
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()
    except:
        return None


def load_signatures():
    try:
        with open("signatures.txt") as f:
            return set(line.strip() for line in f)
    except:
        return set()


def log_result(message):
    with open("logs.txt", "a") as log:
        log.write(f"{datetime.now()} - {message}\n")


def quarantine_file(filepath):
    os.makedirs("quarantine", exist_ok=True)
    dest = os.path.join("quarantine", os.path.basename(filepath))
    try:
        shutil.move(filepath, dest)
        log_result(f"Quarantined: {filepath}")
    except:
        log_result(f"Failed to quarantine: {filepath}")


def scan_folder(folder):
    signatures = load_signatures()

    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)

            file_hash = get_file_hash(path)

            if not file_hash:
                continue

            if file_hash in signatures:
                print(f"[⚠️] Malware: {file}")
                log_result(f"Malware detected: {file}")
                quarantine_file(path)
            else:
                print(f"[✔️] Safe: {file}")
                log_result(f"Safe: {file}")


def start_scan():
    folder = filedialog.askdirectory()
    if folder:
        scan_folder(folder)


app = tk.Tk()
app.title("Basic Antivirus Scanner")
app.geometry("300x200")

label = tk.Label(app, text="Antivirus Scanner", font=("Arial", 14))
label.pack(pady=20)

scan_btn = tk.Button(app, text="Scan Folder", command=start_scan)
scan_btn.pack(pady=10)

app.mainloop()