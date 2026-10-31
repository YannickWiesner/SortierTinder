from pathlib import Path
import tkinter as tk

downloads = Path.home() / "Downloads"
dateien = [d for d in downloads.iterdir() if d.is_file()]
index = 0

def zeige_datei():
    if index < len(dateien):
        label.config(text=dateien[index].name)
        zaehler.config(text=f"{index + 1} von {len(dateien)}")
    else:
        label.config(text="Fertig! Keine Dateien mehr 🎉")
        zaehler.config(text="")

def links(event=None):
    global index
    if index < len(dateien):
        print("❌ Löschen:", dateien[index].name)
        index += 1
        zeige_datei()

def rechts(event=None):
    global index
    if index < len(dateien):
        print("✅ Behalten:", dateien[index].name)
        index += 1
        zeige_datei()

fenster = tk.Tk()
fenster.title("Datei-Tinder")
fenster.geometry("500x250")

zaehler = tk.Label(fenster, font=("Arial", 10))
zaehler.pack(pady=5)

label = tk.Label(fenster, font=("Arial", 14), wraplength=450)
label.pack(pady=30)

knoepfe = tk.Frame(fenster)
knoepfe.pack()
tk.Button(knoepfe, text="❌ Löschen", width=15, command=links).pack(side="left", padx=10)
tk.Button(knoepfe, text="✅ Behalten", width=15, command=rechts).pack(side="left", padx=10)

fenster.bind("<Left>", links)
fenster.bind("<Right>", rechts)

zeige_datei()
fenster.mainloop()