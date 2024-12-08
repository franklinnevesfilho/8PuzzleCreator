# create a class to create a gui

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class Screen:



    def __init__(
            self,
            title="8-Puzzle Creator",
            width=500,
            height=500
    ):
        self.img = None
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(False, False)

        self.create_widgets()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        if file_path:
            self.img = file_path
            messagebox.showinfo("Success", "Image Uploaded Successfully")
            self.clear()
            self.create_widgets()
        else:
            messagebox.showerror("Error", "No Image Selected")

    def create_widgets(self):
        # create a label
        label = tk.Label(
            self.root,
            text="8-Puzzle Creator",
            font=("Arial", 24)
        )

        label.pack()

        # show image
        if self.img:
            img = tk.PhotoImage(file=self.img)
            img_label = tk.Label(
                self.root,
                image=img
            )
            img_label.image = img
            img_label.pack()

        # create an image upload btn
        upload_btn = tk.Button(
            self.root,
            text="Upload Image",
            command=self.upload_image
        )
        upload_btn.pack()



    def run(self):
        self.root.eval('tk::PlaceWindow . center')
        self.root.mainloop()


