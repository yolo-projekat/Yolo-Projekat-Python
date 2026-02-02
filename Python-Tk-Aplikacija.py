import tkinter as tk
from tkinter import ttk
import websockets
import asyncio
from threading import Thread, Lock
from PIL import Image, ImageTk
import io
import requests
import cv2
import numpy as np
from ultralytics import YOLO
import queue

class RobotControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLOv8 Robot Control Pro")

        # Inicijalizacija modela
        self.model = YOLO("yolov8n.pt")
        self.conf_threshold = 0.3
        
        # Thread-safe queue za slike i lock za resurse
        self.image_queue = queue.Queue(maxsize=1)
        self.command_lock = Lock()
        
        self.ws_uri = tk.StringVar(value="ws://192.168.4.1:1606")
        self.image_url = tk.StringVar(value="http://192.168.4.1:1607/capture")
        self.active_commands = set()
        self.ws = None
        self.ws_loop = None
        self.is_tracking = False

        self.key_to_command = {
            'Up': 'napred', 'Down': 'nazad',
            'Left': 'levo', 'Right': 'desno',
            'space': 'stop'
        }

        self.create_controls()
        self.setup_key_bindings()

        # Pokretanje pozadinskih niti
        Thread(target=self.run_websocket, daemon=True).start()
        Thread(target=self.video_stream_thread, daemon=True).start()
        
        # Update UI petlja
        self.update_ui_image()

    def video_stream_thread(self):
        """Pozadinska nit za capture i YOLO detekciju (ne koči UI)"""
        while True:
            try:
                # 1. Capture slike
                url = self.image_url.get()
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    img_data = io.BytesIO(response.content)
                    image = Image.open(img_data).convert('RGB')
                    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

                    # 2. YOLO Detekcija
                    results = self.model.predict(frame, conf=self.conf_threshold, verbose=False)
                    annotated = results[0].plot()
                    
                    # 3. Logika automatskog praćenja (ako je aktivno)
                    if self.is_tracking:
                        self.process_tracking_logic(results[0], frame.shape[1])

                    # 4. Priprema za prikaz
                    rgb_frame = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
                    img_pil = Image.fromarray(rgb_frame)
                    
                    # Ubaci u queue (izbaci staru ako niko nije uzeo)
                    if self.image_queue.full():
                        try: self.image_queue.get_nowait()
                        except queue.Empty: pass
                    self.image_queue.put(img_pil)
            except Exception as e:
                print(f"Stream error: {e}")
                asyncio.run_coroutine_threadsafe(asyncio.sleep(1), self.ws_loop)

    def update_ui_image(self):
        """Čita iz queue-a i osvežava labelu (izvršava se u glavnom threadu)"""
        try:
            while not self.image_queue.empty():
                img_pil = self.image_queue.get_nowait()
                img_tk = ImageTk.PhotoImage(img_pil)
                self.image_label.config(image=img_tk)
                self.image_label.image = img_tk
        except queue.Empty:
            pass
        self.root.after(30, self.update_ui_image)

    def process_tracking_logic(self, result, width):
        """Automatsko upravljanje na osnovu pozicije banane"""
        found = False
        for box in result.boxes:
            if int(box.cls.item()) == 46: # Banana
                found = True
                x1, _, x2, _ = box.xyxy[0].tolist()
                cx = (x1 + x2) / 2
                center_screen = width / 2
                offset = cx - center_screen

                if abs(offset) < 80:
                    self.send_command('napred')
                elif offset < 0:
                    self.send_command('levo')
                else:
                    self.send_command('desno')
                break
        
        if not found:
            self.send_command('stop')

    def create_controls(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # UI za URL-ove
        grid_f = ttk.Frame(main_frame)
        grid_f.pack(fill=tk.X)
        ttk.Label(grid_f, text="WS:").grid(row=0, column=0)
        ttk.Entry(grid_f, textvariable=self.ws_uri).grid(row=0, column=1, sticky="ew")
        
        # Prikaz slike
        self.image_label = ttk.Label(main_frame)
        self.image_label.pack(pady=10)

        # Dugme za praćenje (Toggle)
        self.track_btn = ttk.Button(main_frame, text="🍌 Pokreni praćenje", command=self.toggle_tracking)
        self.track_btn.pack(pady=5)

    def toggle_tracking(self):
        self.is_tracking = not self.is_tracking
        self.track_btn.config(text="🛑 Zaustavi praćenje" if self.is_tracking else "🍌 Pokreni praćenje")
        if not self.is_tracking:
            self.send_command('stop')

    def setup_key_bindings(self):
        self.root.bind('<KeyPress>', self.handle_key)
        self.root.bind('<KeyRelease>', self.handle_key)

    def handle_key(self, event):
        if self.is_tracking: return # Isključi ručne komande dok traje tracking
        
        key = event.keysym
        cmd = self.key_to_command.get(key)
        
        if not cmd: return
        
        if event.type == tk.EventType.KeyPress:
            if cmd == 'stop':
                self.active_commands.clear()
            else:
                self.active_commands.add(cmd)
        elif event.type == tk.EventType.KeyRelease:
            if cmd in self.active_commands:
                self.active_commands.remove(cmd)
        
        # Slanje kombinovane komande
        final_cmd = "+".join(sorted(self.active_commands)) if self.active_commands else "stop"
        self.send_command(final_cmd)

    def send_command(self, cmd):
        if self.ws_loop:
            asyncio.run_coroutine_threadsafe(self.async_send(cmd), self.ws_loop)

    async def async_send(self, cmd):
        if self.ws and not self.ws.closed:
            try:
                await self.ws.send(cmd)
            except: pass

    def run_websocket(self):
        self.ws_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.ws_loop)
        self.ws_loop.run_until_complete(self.websocket_client())

    async def websocket_client(self):
        while True:
            try:
                async with websockets.connect(self.ws_uri.get()) as websocket:
                    self.ws = websocket
                    print("Konektovan na robot!")
                    while not websocket.closed:
                        await asyncio.sleep(0.1)
            except Exception as e:
                print(f"WS Reconnect: {e}")
                await asyncio.sleep(2)

if __name__ == "__main__":
    root = tk.Tk()
    app = RobotControlApp(root)
    root.mainloop()