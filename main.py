import tkinter as tk
from tkinter import filedialog, colorchooser, font, messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import qrcode
import io

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.root.geometry("800x600")

        self.text = ScrolledText(self.root, wrap=tk.WORD, undo=True)
        self.text.pack(fill=tk.BOTH, expand=1)

        self.create_menu()
        self.create_toolbar()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Print", command=self.print_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Copy", command=self.copy_text)
        edit_menu.add_command(label="Paste", command=self.paste_text)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        format_menu = tk.Menu(menubar, tearoff=0)
        format_menu.add_command(label="Font", command=self.choose_font)
        format_menu.add_command(label="Color", command=self.choose_color)
        format_menu.add_command(label="Underline", command=self.underline_text)
        menubar.add_cascade(label="Format", menu=format_menu)

        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Generate QR Code", command=self.generate_qr_code)
        tools_menu.add_command(label="Scan QR Code", command=self.scan_qr_code)
        menubar.add_cascade(label="Tools", menu=tools_menu)

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bg="lightgray")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        dark_mode_btn = tk.Button(toolbar, text="Dark Mode", command=self.dark_mode)
        dark_mode_btn.pack(side=tk.LEFT, padx=2, pady=2)

        light_mode_btn = tk.Button(toolbar, text="Light Mode", command=self.light_mode)
        light_mode_btn.pack(side=tk.LEFT, padx=2, pady=2)

    def new_file(self):
        self.text.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.INSERT, content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text.get(1.0, tk.END)
                file.write(content)

    def save_as_file(self):
        self.save_file()

    def print_file(self):
        # Placeholder for print functionality
        messagebox.showinfo("Print", "Printing the document...")

    def copy_text(self):
        self.text.event_generate("<<Copy>>")

    def paste_text(self):
        self.text.event_generate("<<Paste>>")

    def choose_font(self):
        font_choice = font.askfont(self.root)
        if font_choice:
            self.text.config(font=font_choice)

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text.config(fg=color)

    def underline_text(self):
        current_tags = self.text.tag_names(tk.SEL_FIRST)
        if "underline" in current_tags:
            self.text.tag_remove("underline", tk.SEL_FIRST, tk.SEL_LAST)
        else:
            self.text.tag_add("underline", tk.SEL_FIRST, tk.SEL_LAST)
            self.text.tag_configure("underline", underline=True)

    def dark_mode(self):
        self.text.config(bg="black", fg="white")

    def light_mode(self):
        self.text.config(bg="white", fg="black")

    def generate_qr_code(self):
        content = self.text.get(1.0, tk.END)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(content)
        qr.make(fit=True)
        
        img = qr.make_image(fill="black", back_color="white")
        img.show()

    def scan_qr_code(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            img = Image.open(file_path)
            qr_code = qrcode.decode(img)
            if qr_code:
                self.text.insert(tk.INSERT, qr_code.data.decode())

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()
