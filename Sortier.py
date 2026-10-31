from pathlib import Path
import shutil
import tkinter as tk
from tkinter import messagebox
from send2trash import send2trash

ORDNER = None                  # Ordner, der sortiert wird (wird beim Start gewählt)
dateien = []
index = 0
aktueller_ordner = Path.home()  # Ordner, der gerade in der Liste angezeigt wird
ordner_inhalt = []
modus = "start"                 # "start" = Ordner zum Sortieren wählen, "swipe", "ordner" = Ziel wählen

# ---------------- Swipe-Ansicht ----------------
def zeige_datei():
    ordner_info.config(text=f"Sortiere: {ORDNER}")
    if index < len(dateien):
        name_label.config(text=dateien[index].name)
        zaehler.config(text=f"{index + 1} von {len(dateien)}")
    elif not dateien:
        name_label.config(text=f"Keine Dateien in\n{ORDNER}\n\nAlles aufgeräumt! 🎉")
        zaehler.config(text="")
    else:
        name_label.config(text="Fertig! Alles sortiert 🎉")
        zaehler.config(text="")

def links(event=None):
    global index
    if modus != "swipe" or index >= len(dateien):
        return
    try:
        send2trash(str(dateien[index]))
    except Exception as fehler:
        messagebox.showerror("Fehler", f"Konnte nicht löschen:\n{fehler}")
        return
    index += 1
    zeige_datei()

def rechts(event=None):
    if modus != "swipe" or index >= len(dateien):
        return
    zeige_ordnerwahl()

def ueberspringen(event=None):
    global index
    if modus != "swipe" or index >= len(dateien):
        return
    index += 1
    zeige_datei()

# ---------------- Ordner-Ansicht (für Start und für Ziel) ----------------
def zeige_startwahl():
    global modus
    modus = "start"
    swipe_ansicht.pack_forget()
    ordner_ansicht.pack(fill="both", expand=True, padx=10, pady=10)
    wohin_label.config(text="Welchen Ordner willst du sortieren?")
    aktions_knopf.config(text="✅ Diesen Ordner sortieren")
    abbrechen_knopf.pack_forget()
    aktualisiere_liste()

def zeige_ordnerwahl():
    global modus
    modus = "ordner"
    swipe_ansicht.pack_forget()
    ordner_ansicht.pack(fill="both", expand=True, padx=10, pady=10)
    wohin_label.config(text=f"Wohin mit: {dateien[index].name}")
    aktions_knopf.config(text="✅ In diesen Ordner verschieben")
    abbrechen_knopf.pack(side="left")
    aktualisiere_liste()

def zurueck_zum_swipe(event=None):
    global modus
    if modus == "start":
        return  # Beim Start gibt es noch nichts, wohin man zurück kann
    modus = "swipe"
    ordner_ansicht.pack_forget()
    swipe_ansicht.pack(fill="both", expand=True)
    zeige_datei()

def aktualisiere_liste():
    global ordner_inhalt
    pfad_label.config(text=str(aktueller_ordner))
    liste.delete(0, tk.END)
    try:
        ordner_inhalt = sorted(
            [o for o in aktueller_ordner.iterdir()
             if o.is_dir() and not o.name.startswith(".")],
            key=lambda o: o.name.lower())
    except PermissionError:
        ordner_inhalt = []
    for o in ordner_inhalt:
        liste.insert(tk.END, "📁  " + o.name)

def ordner_oeffnen(event=None):
    global aktueller_ordner
    auswahl = liste.curselection()
    if auswahl:
        aktueller_ordner = ordner_inhalt[auswahl[0]]
        aktualisiere_liste()

def eine_ebene_hoch():
    global aktueller_ordner
    aktueller_ordner = aktueller_ordner.parent
    aktualisiere_liste()

def neuer_ordner(event=None):
    name = eingabe.get().strip()
    if not name:
        return
    try:
        (aktueller_ordner / name).mkdir()
    except FileExistsError:
        messagebox.showwarning("Gibt es schon", f"Der Ordner „{name}“ existiert bereits.")
        return
    except Exception as fehler:
        messagebox.showerror("Fehler", f"Konnte Ordner nicht anlegen:\n{fehler}")
        return
    eingabe.delete(0, tk.END)
    aktualisiere_liste()

def bestaetigen():
    if modus == "start":
        sortier_ordner_waehlen()
    else:
        hier_ablegen()

def sortier_ordner_waehlen():
    global ORDNER, dateien, index, aktueller_ordner, modus
    try:
        dateien = sorted([d for d in aktueller_ordner.iterdir() if d.is_file()],
                         key=lambda d: d.name.lower())
    except Exception as fehler:
        messagebox.showerror("Fehler", f"Ordner kann nicht gelesen werden:\n{fehler}")
        return
    ORDNER = aktueller_ordner
    index = 0
    aktueller_ordner = Path.home()  # Zielauswahl startet wieder im Benutzerordner
    modus = "ordner"                # damit zurueck_zum_swipe greift
    zurueck_zum_swipe()

def hier_ablegen():
    global index
    datei = dateien[index]
    ziel_pfad = aktueller_ordner / datei.name
    if ziel_pfad.exists():
        messagebox.showwarning("Gibt es schon", f"{datei.name} existiert dort bereits.")
        return
    try:
        shutil.move(str(datei), str(ziel_pfad))
    except Exception as fehler:
        messagebox.showerror("Fehler", f"Konnte nicht verschieben:\n{fehler}")
        return
    index += 1
    zurueck_zum_swipe()

# ---------------- Fenster aufbauen ----------------
fenster = tk.Tk()
fenster.title("Datei-Tinder")
fenster.geometry("560x460")

# Swipe-Ansicht
swipe_ansicht = tk.Frame(fenster)
oben = tk.Frame(swipe_ansicht)
oben.pack(fill="x", padx=10, pady=(10, 0))
ordner_info = tk.Label(oben, fg="gray", anchor="w")
ordner_info.pack(side="left", fill="x", expand=True)
tk.Button(oben, text="📂 Anderer Ordner", command=zeige_startwahl).pack(side="right")
zaehler = tk.Label(swipe_ansicht, font=("Arial", 10))
zaehler.pack(pady=10)
name_label = tk.Label(swipe_ansicht, font=("Arial", 14), wraplength=500)
name_label.pack(pady=50)
knoepfe = tk.Frame(swipe_ansicht)
knoepfe.pack()
tk.Button(knoepfe, text="❌ Löschen (←)", width=15, command=links).pack(side="left", padx=8)
tk.Button(knoepfe, text="⏭ Später (↓)", width=12, command=ueberspringen).pack(side="left", padx=8)
tk.Button(knoepfe, text="✅ Behalten (→)", width=15, command=rechts).pack(side="left", padx=8)

# Ordner-Ansicht
ordner_ansicht = tk.Frame(fenster)
wohin_label = tk.Label(ordner_ansicht, font=("Arial", 12, "bold"), wraplength=520)
wohin_label.pack(anchor="w")
pfad_zeile = tk.Frame(ordner_ansicht)
pfad_zeile.pack(fill="x", pady=5)
tk.Button(pfad_zeile, text="⬆ Hoch", command=eine_ebene_hoch).pack(side="left")
pfad_label = tk.Label(pfad_zeile, anchor="w", fg="gray")
pfad_label.pack(side="left", padx=8)

liste = tk.Listbox(ordner_ansicht, font=("Arial", 11), height=10)
liste.pack(fill="both", expand=True)
liste.bind("<Double-Button-1>", ordner_oeffnen)

neu_zeile = tk.Frame(ordner_ansicht)
neu_zeile.pack(fill="x", pady=5)
eingabe = tk.Entry(neu_zeile)
eingabe.pack(side="left", fill="x", expand=True)
eingabe.bind("<Return>", neuer_ordner)
tk.Button(neu_zeile, text="➕ Neuer Ordner", command=neuer_ordner).pack(side="left", padx=5)

aktion_zeile = tk.Frame(ordner_ansicht)
aktion_zeile.pack(fill="x", pady=5)
abbrechen_knopf = tk.Button(aktion_zeile, text="↩ Abbrechen (Esc)", command=zurueck_zum_swipe)
aktions_knopf = tk.Button(aktion_zeile, command=bestaetigen)
aktions_knopf.pack(side="right")

# Tasten
fenster.bind("<Left>", links)
fenster.bind("<Right>", rechts)
fenster.bind("<Down>", ueberspringen)
fenster.bind("<Escape>", zurueck_zum_swipe)

zeige_startwahl()
fenster.mainloop()
