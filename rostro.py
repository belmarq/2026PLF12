import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import json

#python -m pip install -U opencv-contrib-python
#python -m pip install -U Pillow

class FaceLandmarkMarker:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Landmark Marker")
        self.landmarks = []
        self.image = None
        self.photo = None
        self.canvas = None
        self.image_path = None
        
        # Load image button
        btn_load = tk.Button(root, text="Load Image", command=self.load_image)
        btn_load.pack()
        
        # Canvas for image
        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        
        # Info label
        self.info_label = tk.Label(root, text="Landmarks marked: 0/30")
        self.info_label.pack()
        
        # Save button
        btn_save = tk.Button(root, text="Save Landmarks", command=self.save_landmarks)
        btn_save.pack()
        
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.image_path = file_path
            self.image = cv2.imread(file_path)
            self.landmarks = []
            self.display_image()
    
    def display_image(self):
        img_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        self.photo = ImageTk.PhotoImage(img_pil)
        
        self.canvas.config(width=self.photo.width(), height=self.photo.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        
        # Draw existing landmarks
        for i, (x, y) in enumerate(self.landmarks):
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="red")
            self.canvas.create_text(x+5, y-5, text=str(i+1), fill="white")
    
    def on_click(self, event):
        if len(self.landmarks) < 30:
            self.landmarks.append((event.x, event.y))
            self.info_label.config(text=f"Landmarks marked: {len(self.landmarks)}/30")
            self.display_image()
    
    def save_landmarks(self):
        if self.landmarks:
            data = {
                "image": self.image_path,
                "landmarks": self.landmarks
            }
            with open("landmarks.json", "w") as f:
                json.dump(data, f)
            print(f"Saved {len(self.landmarks)} landmarks to landmarks.json")

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceLandmarkMarker(root)
    root.mainloop()