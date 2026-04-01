import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import cv2
import numpy as np
import os


class HSVEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("HSV Image Editor")

        self.image = None
        self.hsv_image = None
        self.tk_image = None
        self.current_image = None
        self.image_name = ""

        # =========================
        # Canvas for image display
        # =========================
        self.canvas = tk.Canvas(root, width=300, height=300, bg="gray")
        self.canvas.pack(pady=10)
        self.canvas.drop_target_register(DND_FILES)
        self.canvas.dnd_bind("<<Drop>>", self.drop_image)

        # =========================
        # Sliders container
        # =========================
        controls = tk.Frame(root)
        controls.pack(fill="x", padx=10, pady=5)

        # -------------------------
        # Helper to build one row
        # -------------------------
        def make_slider_row(label, from_, to):
            row = tk.Frame(controls)
            row.pack(fill="x", pady=4)

            minus = tk.Button(
                row, text="◀", width=2,
                command=lambda s=None: self.step_scale(scale, -1)
            )
            minus.pack(side="left")

            scale = tk.Scale(
                row,
                from_=from_,
                to=to,
                orient="horizontal",
                label=label,
                command=self.update_image
            )
            scale.pack(side="left", fill="x", expand=True)

            plus = tk.Button(
                row, text="▶", width=2,
                command=lambda s=None: self.step_scale(scale, 1)
            )
            plus.pack(side="left")

            return scale

        # =========================
        # Create sliders
        # =========================
        self.hue = make_slider_row("Hue", -180, 180)
        self.sat = make_slider_row("Saturation", -255, 255)
        self.val = make_slider_row("Value", -255, 255)

        # =========================
        # Mean HSV label
        # =========================
        self.mean_label = tk.Label(
            root,
            text="Mean H: Mean S: Mean V:",
            font=("Arial", 12)
        )
        self.mean_label.pack(pady=5)
        self.std_label = tk.Label(
            root,
            text="Std H: Std S: Std V:",
            font=("Arial", 12)
        )
        self.std_label.pack(pady=5)

        # =========================
        # Buttons
        # =========================
        self.save_btn = tk.Button(root, text="Save Image", command=self.save_image,height=3)
        self.save_btn.pack(pady=3)

        self.reset_btn = tk.Button(root, text="Reset Adjustments", command=self.reset_adjustments, height=3)
        self.reset_btn.pack(pady=3)

    # =========================
    # Slider step helper
    # =========================
    def step_scale(self, scale, step):
        scale.set(scale.get() + step)
        self.update_image()

    # =========================
    # Reset sliders
    # =========================
    def reset_adjustments(self):
        self.hue.set(0)
        self.sat.set(0)
        self.val.set(0)
        self.update_image()

    # =========================
    # Drag & drop image
    # =========================
    def drop_image(self, event):
        path = event.data.strip("{}")
        if os.path.isfile(path):
            self.load_image(path)

    def load_image(self, path):
        img = Image.open(path).convert("RGB")
        img = img.resize((300, 300))
        self.image = np.array(img)
        self.hsv_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)
        self.image_name = os.path.splitext(os.path.basename(path))[0]

        self.hue.set(0)
        self.sat.set(0)
        self.val.set(0)
        self.update_image()

    # =========================
    # Image update
    # =========================
    def update_image(self, event=None):
        if self.hsv_image is None:
            return

        hsv = self.hsv_image.copy().astype(np.int16)
        hsv[:, :, 0] = np.clip(hsv[:, :, 0] + self.hue.get(), 0, 179)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] + self.sat.get(), 0, 255)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] + self.val.get(), 0, 255)
        hsv = hsv.astype(np.uint8)

        rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

        mean_h = np.mean(hsv[:, :, 0])
        mean_s = np.mean(hsv[:, :, 1])
        mean_v = np.mean(hsv[:, :, 2])
        std_h = np.std(hsv[:, :, 0])
        std_s = np.std(hsv[:, :, 1])
        std_v = np.std(hsv[:, :, 2])

        self.mean_label.config(
            text=f"Mean H: {mean_h:.1f}\nMean S: {mean_s:.1f}\nMean V: {mean_v:.1f}"
        )

        self.std_label.config(
            text=f"Std H: {std_h:.1f}\nStd S: {std_s:.1f}\nStd V: {std_v:.1f}"
        )

        pil_img = Image.fromarray(rgb)
        self.tk_image = ImageTk.PhotoImage(pil_img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")

        self.current_image = rgb

    # =========================
    # Save image
    # =========================
    def save_image(self):
        if self.current_image is None:
            return

        path = filedialog.asksaveasfilename(
            title=f"Save {self.image_name}",
            initialfile=f"{self.image_name}_edited.png",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")]
        )
        if path:
            Image.fromarray(self.current_image).save(path)


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = HSVEditor(root)
    root.mainloop()
