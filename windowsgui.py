import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont

# Global variable to store image
original_image = None


def upload_image():
    global original_image
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )

    if file_path:
        original_image = Image.open(file_path).convert("RGBA")
        status_label.config(text="Image uploaded successfully")


def add_watermark():
    global original_image

    if original_image is None:
        messagebox.showerror("Error", "Please upload an image first.")
        return

    watermark_text = watermark_entry.get()
    if not watermark_text:
        messagebox.showerror("Error", "Please enter watermark text.")
        return

    image = original_image.copy()
    width, height = image.size

    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", size=int(width / 20))
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Position: bottom-right corner
    x = width - text_width - 20
    y = height - text_height - 20

    draw.text((x, y), watermark_text, fill=(255, 255, 255, 128), font=font)

    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg")]
    )

    if save_path:
        image.convert("RGB").save(save_path)
        messagebox.showinfo("Success", "Watermarked image saved successfully!")

# ---------------- GUI ---------------- #
root = tk.Tk()
root.title("Image Watermark App")
root.geometry("400x250")
root.resizable(True, True)

title_label = tk.Label(root, text="Image Watermark Tool", font=("Arial", 16))
title_label.pack(pady=10)

upload_btn = tk.Button(root, text="Upload Image", command=upload_image, width=20)
upload_btn.pack(pady=5)

watermark_entry = tk.Entry(root, width=30)
watermark_entry.pack(pady=5)
watermark_entry.insert(0, "Enter watermark text")

apply_btn = tk.Button(root, text="Add Watermark & Save", command=add_watermark, width=20)
apply_btn.pack(pady=10)

status_label = tk.Label(root, text="", fg="green")
status_label.pack()

root.mainloop()
