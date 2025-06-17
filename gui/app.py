import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DCTCompress")
        self.geometry("400x500")

        # External container for all pages
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # Dictionary of all pages
        self.pages = {}

        # Initialize all pages
        for PageClass in (HomePage, ImageViewerPage):
            # Get class name
            page_name = PageClass.__name__
            # Create page
            frame = PageClass(parent=self.container)
            # Add page to dictionary of App's pages
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.switch_to_page("HomePage")

    def switch_to_page(self, name):
        page = self.pages[name]
        page.tkraise()


class HomePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.label = ctk.CTkLabel(
            master=self.content_frame,
            text="DCTCompress",
            width=40,
            height=28,
            fg_color="transparent",
            font=("Roboto", 30),
        )
        self.label.pack(pady=20)

        self.button = ctk.CTkButton(
            master=self.content_frame,
            text="Choose File",
            width=140,
            height=28,
            command=self.select_file,
        )
        self.button.pack(pady=10)

        self.fileLabel = ctk.CTkLabel(
            master=self.content_frame,
            width=40,
            height=28,
            text="No file selected",
            fg_color="transparent",
            wraplength=200,
            font=("Roboto", 10),
        )
        self.fileLabel.pack(pady=10)

        self.inputsFrame = ctk.CTkFrame(self.content_frame)

        self.firstRow = ctk.CTkFrame(self.inputsFrame, fg_color="transparent")
        self.firstRow.columnconfigure(0, weight=1)
        self.firstRow.columnconfigure(1, weight=1)

        self.fLabel = ctk.CTkLabel(
            master=self.firstRow,
            width=40,
            height=28,
            text="F",
            fg_color="transparent",
            font=("Roboto", 15),
        )
        self.fLabel.grid(row=0, column=0)

        fTextBox = ctk.CTkEntry(self.firstRow)
        fTextBox.grid(row=0, column=1)

        self.firstRow.pack(pady=(50, 20))

        self.secondRow = ctk.CTkFrame(self.inputsFrame, fg_color="transparent")
        self.secondRow.columnconfigure(0, weight=1)
        self.secondRow.columnconfigure(1, weight=1)

        self.dLabel = ctk.CTkLabel(
            master=self.secondRow,
            width=40,
            height=28,
            text="d",
            fg_color="transparent",
            font=("Roboto", 15),
        )
        self.dLabel.grid(row=0, column=0)

        self.dTextBox = ctk.CTkEntry(self.secondRow)
        self.dTextBox.grid(row=0, column=1)

        self.secondRow.pack(pady=(10, 50))

        self.inputsFrame.pack(pady=20)

        self.buttonCompress = ctk.CTkButton(
            self.inputsFrame, text="Compress!", width=300, height=28
        )
        self.buttonCompress.pack()

    def button_event():
        print("button pressed")

    def select_file(self):
        filename = ctk.filedialog.askopenfilename()
        print(filename)
        self.fileLabel.configure(text=filename)
        self.fileLabel.configure(font=("Roboto", 12))
        self.fileLabel.update()


class ImageViewerPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
