# 🚗 YOLO Vision Rover Control (Python Edition)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Ultralytics](https://img.shields.io/badge/YOLO-v8-red.svg)](https://docs.ultralytics.com/)
[![Tkinter](https://img.shields.io/badge/UI-Tkinter-grey.svg)](https://docs.python.org/3/library/tkinter.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**YOLO Vision Rover** je sofisticirana desktop aplikacija razvijena u Python-u koja služi kao kontrolni centar za pametno vozilo bazirano na mikrokontrolerima (poput ESP32-CAM ili Raspberry Pi). Aplikacija kombinuje daljinsko upravljanje u realnom vremenu sa naprednim AI funkcijama za prepoznavanje objekata pomoću **YOLOv8** modela.



---

## ✨ Ključne Karakteristike

### 📺 Live Stream & AI Monitoring
* **Real-Time Processing:** Prikaz video signala sa kamere vozila u realnom vremenu uz sinhronu YOLOv8 detekciju.
* **YOLOv8 Integracija:** Automatsko prepoznavanje objekata (ljudi, automobili, prepreke) sa vizuelnim bounding-box prikazom.
* **Smart Banana Tracker:** Specijalizovani mod za automatsko praćenje objekta (klasa: banana). Vozilo inteligentno koriguje svoju putanju kako bi zadržalo objekt u centru kadra.
* **Multithreading Arhitektura:** Obrada slike i AI detekcija se vrše u posebnim nitima, što osigurava stabilan FPS i responzivan korisnički interfejs.

### 🎮 Kontrolni Sistem
* **Keyboard Mastery:** Potpuna kontrola kretanja putem strelica na tastaturi uz podršku za kombinovane komande (npr. napred + levo).
* **On-Screen Dashboard:** Intuitivna dugmad unutar Tkinter interfejsa za brzu kontrolu mišem.
* **WebSocket Engine:** Brz prenos komandi bez latencije putem asinhronih WebSocketa.

---

## 🛠 Tehnologije

| Segment | Tehnologija |
| :--- | :--- |
| **GUI Framework** | Tkinter (Python Native UI) |
| **AI Model** | Ultralytics YOLOv8 (Nano verzija) |
| **Networking** | WebSockets & Requests |
| **Image Handling** | OpenCV & Pillow (PIL) |
| **Backend** | Python 3.9+ |

---

## 🚀 Kako radi?

### 1. Povezivanje
Aplikacija komunicira sa vozilom putem dve adrese:
* **WebSocket:** `ws://192.168.4.1:1606` (Slanje komandi kretanja).
* **HTTP Stream:** `http://192.168.4.1:1607/capture` (Preuzimanje frejmova za analizu).

### 2. Logika Praćenja (Follow Mode)
Aplikacija analizira horizontalni offset detektovanog objekta:
* **Levo:** Ako je objekt na levoj strani, šalje se komanda `levo+nazad` (za rotaciju).
* **Centar:** Ako je objekt u sredini, šalje se komanda `napred`.
* **Desno:** Ako je objekt na desnoj strani, šalje se komanda `desno+nazad`.

### 3. Komande kretanja
Vozilo prima sledeće string komande:
* `napred`, `nazad`, `levo`, `desno`
* `stop` (automatski se šalje čim korisnik pusti taster)

---

## 📦 Instalacija i Podešavanje

1. **Klonirajte repozitorijum:**
   ```bash
   git clone https://github.com/yolo-projekat/Yolo-Projekat-Python/
   cd Yolo-Projekat-Python
Instalirajte zavisnosti:

Bash
pip install -r requirements.txt
Povežite se na WiFi vozila: Povežite svoj računar na WiFi pristupnu tačku robota (default IP: 192.168.4.1).

Pokrenite aplikaciju:

Bash
python main.py

🎨 Teme i UI
Aplikacija koristi modernu i preglednu paletu boja unutar Tkinter okruženja:

Dark Mode Stream: Crna pozadina za video prikaz radi boljeg kontrasta bounding-boxova.

Interactive Buttons: Vizuelna povratna informacija prilikom klika na kontrole.

Real-time Logs: Konzola unutar aplikacije prikazuje status konekcije i poslate komande.

Autor: Danilo Stoletovic

Licenca: MIT
