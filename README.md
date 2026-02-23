Markdown
<div align="center">

# 🐍 YOLO Projekat Python
### *AI Engine i Multithreaded Kontrolni Terminal*

[![Python](https://img.shields.io/badge/Python-3.9%2B-38bdf8?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/AI-YOLOv8-075985?style=for-the-badge&logo=ultralytics&logoColor=white)](https://docs.ultralytics.com/)
[![OpenCV](https://img.shields.io/badge/Vision-OpenCV-38bdf8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-94a3b8?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

<p align="center">
  <b>YOLO Vozilo Python</b> predstavlja moćan desktop klijent dizajniran za real-time vizuelnu analitiku i preciznu daljinsku kontrolu. 
  <br>Aplikacija koristi <b>YOLOv8 Nano</b> model za inteligentno procesiranje video strima uz minimalno procesorsko opterećenje.
</p>



</div>

## 🚀 Ključne Karakteristike

### 🧠 Napredna AI Detekcija
* **Real-Time Inference:** Kontinuirano procesiranje frejmova sa grafičkim prikazom *bounding-box* identifikatora.
* **Smart Tracking (Follow Mode):** Napredni algoritam za praćenje specifičnih objekata (npr. klasa "banana"). Sistem dinamički koriguje kretanje vozila kako bi cilj ostao u centru vidnog polja.
* **Multithreaded Architecture:** Odvojene niti za mrežnu komunikaciju, UI renderovanje i AI inferenciju, čime se postiže stabilan FPS i maksimalna responzivnost.

### 🎮 Kontrolna Tabla
* **Keyboard Mastery:** Full-stack kontrola kretanja putem tastature uz podršku za složene vektorske komande (npr. napred + levo).
* **Asynchronous WebSockets:** Implementacija `websockets` biblioteke za ultrabrz prenos komandi kretanja ka Raspberry Pi 5 kontroleru.
* **Tkinter Dash:** Modernizovani GUI sa real-time logovanjem sistemskih događaja i mrežnog statusa.

---

## 🛠 Tehnološki Stack

| Segment | Tehnologija | Uloga |
| :--- | :--- | :--- |
| **Backend Core** | Python 3.9+ | Glavna programska logika |
| **AI Engine** | Ultralytics YOLOv26 | Computer Vision i detekcija |
| **Networking** | WebSockets & Requests | Real-time I/O komunikacija |
| **Image Processing** | OpenCV | Filtriranje i manipulacija frejmova |
| **UI Framework** | Tkinter / Pillow | Grafički interfejs i renderovanje |

---

## 🔧 Arhitektura i Rad

Sistem funkcioniše kao centralni čvor u YOLO ekosistemu:

> [!NOTE]
> Praćenje objekata koristi PID-like logiku za glatku korekciju pravca motora, sprečavajući nagle oscilacije pri kretanju.

### 🌐 Mrežni Protokoli
- **Command Stream:** `ws://192.168.4.1:1606` (Low-latency kontrola).
- **Video Capture:** `http://192.168.4.1:1607/capture` (Raw MJPEG stream).

### 📐 Logika Praćenja
Aplikacija izračunava horizontalni offset objekta u odnosu na centar frejma:
1. **Levo:** Aktivira `rot_levo` za centriranje kadra.
2. **Centar:** Održava `napred` vektor kretanja.
3. **Desno:** Aktivira `rot_desno` za centriranje kadra.

---

## 📦 Instalacija

1. **Kloniraj:**
   ```bash
   git clone [https://github.com/yolo-projekat/Yolo-Projekat-Python/](https://github.com/yolo-projekat/Yolo-Projekat-Python/)
   cd Yolo-Projekat-Python
Dependencies:

pip install -r requirements.txt
Run: Povežite se na mrežu vozila i pokrenite:

python main.py
🎨 Vizuelni Identitet
U skladu sa Glassmorphism stilom projekta:

UI Background: Deep Navy (#0f172a) kontrast za bolju vidljivost bounding-boxova.

Accent Color: #38bdf8 za aktivne niti i mrežne indikatore.

<div align="center">

Autor: Danilo Stoletović • Mentor: Dejan Batanjac

ETŠ „Nikola Tesla“ Niš • 2026

</div>
