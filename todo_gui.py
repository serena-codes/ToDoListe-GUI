import tkinter as tk
from tkinter import messagebox
import json

# Aufgabenliste
tasks = []

# Prioritätssortierung
def update_listbox():
    listbox.delete(0, tk.END)
    priority_order = {"hoch": 1, "mittel": 2, "niedrig": 3}
    sorted_tasks = sorted(tasks, key=lambda x: priority_order[x['priority']])
    for i, task in enumerate(sorted_tasks, 1):
        listbox.insert(tk.END, f"{i}. {task['text']} (Priorität: {task['priority']})")

# Aufgabe hinzufügen
def add_task():
    task_text = entry.get()
    priority = priority_var.get()
    if task_text:
        tasks.append({'text': task_text, 'priority': priority})
        entry.delete(0, tk.END)
        update_listbox()

# Aufgabe löschen
def delete_task():
    try:
        selected = listbox.curselection()[0]
        del tasks[selected]
        update_listbox()
    except IndexError:
        messagebox.showwarning("Fehler", "Bitte eine Aufgabe auswählen!")

# Aufgaben speichern
def save_tasks():
    filename = filename_var.get()
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Gespeichert", f"Aufgaben wurden gespeichert in {filename}.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Speichern fehlgeschlagen: {e}")

# Aufgaben laden
def load_tasks():
    global tasks
    filename = filename_var.get()
    try:
        with open(filename, "r", encoding="utf-8") as f:
            tasks = json.load(f)
        update_listbox()
        messagebox.showinfo("Geladen", f"Aufgaben wurden geladen aus {filename}.")
    except FileNotFoundError:
        messagebox.showwarning("Nicht gefunden", f"Datei {filename} wurde nicht gefunden.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Laden fehlgeschlagen: {e}")

# GUI-Fenster
root = tk.Tk()
root.title("To-Do-Liste mit Priorität")
root.configure(bg="#f0f4f7")  # Hintergrundfarbe

# Eingabe für Aufgabe + Priorität
input_frame = tk.Frame(root)
input_frame.pack(pady=5)

entry = tk.Entry(input_frame, width=30)
entry.pack(side=tk.LEFT)
entry.configure(bg="white")

priority_label = tk.Label(input_frame, text="Priorität:")
priority_label.pack(side=tk.LEFT, padx=(10, 0))

priority_var = tk.StringVar(value="mittel")
priority_menu = tk.OptionMenu(input_frame, priority_var, "hoch", "mittel", "niedrig")
priority_menu.pack(side=tk.LEFT)

# Button: Aufgabe hinzufügen
add_button = tk.Button(root, text="Aufgabe hinzufügen", command=add_task)
add_button.pack(pady=5)
add_button.configure(bg="#d0f0c0")  # grünlich

# Eingabe für Dateiname
filename_var = tk.StringVar(value="tasks.json")

filename_frame = tk.Frame(root)
filename_frame.pack(pady=5)

tk.Label(filename_frame, text="Dateiname:").pack(side=tk.LEFT)
filename_entry = tk.Entry(filename_frame, textvariable=filename_var, width=30)
filename_entry.pack(side=tk.LEFT)
filename_entry.configure(bg="white")

# Buttons: Speichern & Laden
save_button = tk.Button(root, text="Speichern", command=save_tasks)
save_button.pack(pady=2)
save_button.configure(bg="#cfe2f3")  # hellblau

load_button = tk.Button(root, text="Laden", command=load_tasks)
load_button.pack(pady=2)
load_button.configure(bg="#fff2cc")  # gelblich

# Liste & Löschen
listbox = tk.Listbox(root, width=50)
listbox.pack(pady=10)
listbox.configure(bg="white")

delete_button = tk.Button(root, text="Ausgewählte Aufgabe löschen", command=delete_task)
delete_button.pack(pady=5)
delete_button.configure(bg="#f4cccc")  # rosa

# Start
update_listbox()
root.mainloop()