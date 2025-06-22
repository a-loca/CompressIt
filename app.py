import customtkinter as ctk
import os
from PIL import Image
from dct import jpg_compression
from io import BytesIO
import math

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CompressIt")

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        self.pages = {}  # collect instances of pages' class
        self.page_sizes = {
            "HomePage": "550x700",
            "ImageViewerPage": "1400x900",
        }

        for PageClass in (HomePage, ImageViewerPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.switch_to_page("HomePage")

    def switch_to_page(self, name):
        page = self.pages[name]
        page.tkraise()
        if name in self.page_sizes:
            self.geometry(self.page_sizes[name])


class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.filename = ""

        # Outer container
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Page title
        label = ctk.CTkLabel(
            master=content_frame,
            text="Compress it!",
            width=60,
            height=36,
            fg_color="transparent",
            font=("Roboto", 36),
        )
        label.pack(pady=30)

        # File browser button
        button = ctk.CTkButton(
            master=content_frame,
            text="Choose File",
            width=140,
            height=36,
            command=self.select_file,
            font=("Roboto", 16),
        )
        button.pack(pady=15)

        # Selected file name
        self.file_label = ctk.CTkLabel(
            master=content_frame,
            width=60,
            height=32,
            text="No file selected.",
            fg_color="transparent",
            wraplength=300,
            font=("Roboto", 14),
        )
        self.file_label.pack(pady=(15, 30))

        # Container for inputs section
        inputs_frame = ctk.CTkFrame(content_frame, fg_color="#2E2E2E", width=450)

        # Container for "F" and textbox
        first_row = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        first_row.columnconfigure(0, weight=1)
        first_row.columnconfigure(1, weight=1)

        # "F" label
        f_label = ctk.CTkLabel(
            master=first_row,
            width=50,
            height=32,
            text="F",
            fg_color="transparent",
            font=("Roboto", 20),
        )
        f_label.grid(row=0, column=0, padx=10, pady=10)

        # Actual input
        self.f_textbox = ctk.CTkEntry(
            first_row, height=36, width=160, font=("Roboto", 14)
        )
        self.f_textbox.grid(row=0, column=1, padx=10, pady=10)

        first_row.pack(pady=(60, 20), padx=(20, 40))

        # Container for "d" and textbox
        second_row = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        second_row.columnconfigure(0, weight=1)
        second_row.columnconfigure(1, weight=1)

        d_label = ctk.CTkLabel(
            master=second_row,
            width=50,
            height=32,
            text="d",
            fg_color="transparent",
            font=("Roboto", 20),
        )
        d_label.grid(row=0, column=0, padx=10, pady=10)

        self.d_textbox = ctk.CTkEntry(
            second_row, height=36, width=160, font=("Roboto", 14)
        )
        self.d_textbox.grid(row=0, column=1, padx=10, pady=10)

        second_row.pack(pady=(10, 50), padx=(20, 40))

        inputs_frame.pack()

        btn_compress = ctk.CTkButton(
            inputs_frame,
            text="Compress!",
            width=250,
            height=36,
            font=("Roboto", 16),
            command=self.prepare_compression,
        )
        btn_compress.pack(pady=(0, 30))

        # Error messages
        self.error_frame = ctk.CTkFrame(
            content_frame, fg_color="red", width=300, height=40
        )
        self.error_message = ctk.CTkLabel(
            self.error_frame,
            text="Error",
            text_color="white",
            font=("Roboto", 15),
        )

        self.error_frame.pack_propagate(0)

    def _show_error(self, message):
        self.error_message.configure(text=message)
        self.error_message.pack(pady=10)
        self.error_frame.pack(pady=20)

    def _hide_error(self):
        self.error_frame.pack_forget()

    def select_file(self):
        path = ctk.filedialog.askopenfilename()

        # Check that file is a .bmp image
        filename, file_extension = os.path.splitext(path)

        if file_extension != ".bmp":
            self._show_error("ERROR: choose a .bpm image.")
            self.file_label.configure(text="No file selected.")
            self.filename = ""
        else:
            self._hide_error()

            self.file_label.configure(text=path)
            self.file_label.configure(font=("Roboto", 14))
            self.file_label.update()

            self.filename = path

    def check_inputs(self):
        # Check that F is a number
        f_content = self.f_textbox.get()
        if not f_content.isnumeric() or int(f_content) < 0:
            self._show_error("ERROR: F needs to be a positive integer.")
            return False

        # Remove error if present
        self._hide_error()

        # F is a number
        self.f = int(f_content)

        # Check if d is a number
        d_content = self.d_textbox.get()
        if not d_content.isnumeric():
            self._show_error("ERROR: d needs to be a positive integer.")
            return False

        # Check that d is in [0, 2F-2]
        self.d = int(d_content)
        if not (self.d >= 0 and self.d <= 2 * self.f - 2):
            self._show_error(f"ERROR: d needs to be in [0, {2 * self.f - 2}].")
            return False

        # d is a number and in the correct range
        self._hide_error()

        return True

    def check_file(self):
        if self.filename == "":
            self._show_error("ERROR: no .bpm image selected.")
            return False

        self._hide_error()
        return True

    def prepare_compression(self):
        if self.check_inputs():
            if self.check_file():
                # Change page and compress
                self.controller.pages["ImageViewerPage"].set_image(
                    self.filename, self.f, self.d
                )
                self.controller.switch_to_page("ImageViewerPage")


class ImageViewerPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.filename = ""

        # Back to home page button
        go_back_button = ctk.CTkButton(
            self,
            text="← Go Back",
            width=140,
            height=28,
            command=lambda: controller.switch_to_page("HomePage"),
        )
        go_back_button.place(relx=0.02, rely=0.02, anchor="nw")

        # Save button
        save_button = ctk.CTkButton(
            self, text="Save JPG", width=140, height=28, command=self.save_image
        )

        save_button.place(relx=0.98, rely=0.02, anchor="ne")

        # Outer frame
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        # Show regular image
        self.original_image_label = ctk.CTkLabel(frame, text="")
        self.original_image_label.grid(row=0, column=0, padx=20, pady=10)

        # Show compressed image
        self.compressed_image_label = ctk.CTkLabel(frame, text="")
        self.compressed_image_label.grid(row=0, column=1, padx=20, pady=10)

        # Info about the image and params
        self.info_label = ctk.CTkLabel(
            self,
            fg_color="transparent",
            bg_color="transparent",
            text="",
            font=("Roboto", 15),
        )
        self.info_label.place(relx=0.5, rely=0.98, anchor="s")

    def set_image(self, image, f, d):
        # Save image path as class attribute to set default
        # name for compressed image when saving it
        self.image_path = image

        # Open image with PIL
        img = Image.open(image)
        # Some test images have 3 channels even though they are gray scale
        # forcing a conversion to gray scale removes superfluous channels
        img = img.convert("L")
        width, height = img.size

        # Compress image
        self.compressed_image = jpg_compression(img, f, d)

        # Print info on screen
        self.info_label.configure(
            text=f"Image size: {width}x{height} \t\t"
            + f"Params: F = {f}, d = {d} \t"
            + f"Original size (.bmp): {self._bytes_to_string(os.path.getsize(image))} \t\t"
            + f"Compressed size (.jpg): {self._bytes_to_string(self._get_image_size_in_bytes(self.compressed_image))}"
        )

        # Resize images
        max_img_width = 500
        scale_factor = max_img_width / width

        resized_img = img.resize(
            (math.floor(width * scale_factor), math.floor(height * scale_factor)),
            Image.NEAREST,
        )

        resized_compressed_image = self.compressed_image.resize(
            (math.floor(width * scale_factor), math.floor(height * scale_factor)),
            Image.NEAREST,
        )

        ctk_img = ctk.CTkImage(
            light_image=resized_img, dark_image=resized_img, size=resized_img.size
        )
        ctk_compressed_img = ctk.CTkImage(
            light_image=resized_compressed_image,
            dark_image=resized_compressed_image,
            size=resized_compressed_image.size,
        )

        # Display original image
        self.original_image_label.configure(image=ctk_img)

        # Display compressed image
        self.compressed_image_label.configure(image=ctk_compressed_img)

    def save_image(self):
        # Open file browser to save image
        path = ctk.filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")],
            title="Save image as...",
            initialfile=os.path.basename(self.image_path).split(".")[0] + ".jpg",
        )
        # If user selected a path to save image to
        if path:
            self.compressed_image.save(
                path, "JPEG", quality=100, subsampling=0, optimize=True
            )

    def _get_image_size_in_bytes(self, img, format="JPEG"):
        buffer = BytesIO()
        # Simulate saving file to get its size
        img.save(buffer, format=format)
        return len(buffer.getvalue())

    def _bytes_to_string(self, bytes):
        if bytes > 1e6:
            return f"{bytes / 1e6 :.2f} MB"
        elif bytes > 1e3:
            return f"{bytes / 1e3 : .2f} kB"
        else:
            return f"{bytes} B"


if __name__ == "__main__":
    app = App()
    app.mainloop()
