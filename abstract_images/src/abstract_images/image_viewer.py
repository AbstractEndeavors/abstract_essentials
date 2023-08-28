import os
import tkinter as tk
from tkinter import Button, Label, filedialog
from PIL import Image, ImageTk

class ImageBrowser:
    def __init__(self, root, images):
        self.root = root
        self.images = images
        self.index = 0
        self.img_label = Label(root)
        self.img_label.pack(pady=20)

        prev_button = Button(root, text="Previous", command=self.prev_image)
        prev_button.pack(side="left", padx=10)

        next_button = Button(root, text="Next", command=self.next_image)
        next_button.pack(side="right", padx=10)

        self.show_image()

    def prev_image(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.images) - 1
        self.show_image()

    def next_image(self):
        self.index += 1
        if self.index == len(self.images):
            self.index = 0
        self.show_image()

    def show_image(self):
        image_path = self.images[self.index]
        image = Image.open(image_path)
     
        image = image.resize((int(float(float(image.size[0])/float(image.size[1]))*600), 600), Image.LANCZOS) # Resize the image for demonstration purposes
        photo = ImageTk.PhotoImage(image)
        self.img_label.config(image=photo)
        self.img_label.image = photo
        self.root.title(f"Viewing {os.path.basename(image_path)}")
def resize_image(image, base_width):
    # Calculate the aspect ratio
    w_percent = base_width / float(image.size[0])
    h_size = int(float(image.size[1]) * float(w_percent))
    return image.resize((base_width, h_size), Image.LANCZOS)

def find_images(directory, extensions=("jpg", "jpeg", "png", "gif")):
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(extensions):
                yield os.path.join(dirpath, filename)

def main():
    dir_path = filedialog.askdirectory(title="Select Directory")
    if not dir_path:
        return

    images = list(find_images(dir_path))
    if not images:
        print("No images found in the selected directory!")
        return

    root = tk.Tk()
    app = ImageBrowser(root, images)
    root.mainloop()

if __name__ == "__main__":
    main()
