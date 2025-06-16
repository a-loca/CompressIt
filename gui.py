import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("400x500")
root.title("DCTCompress")


content_frame = customtkinter.CTkFrame(root, fg_color="transparent")
content_frame.place(relx=0.5, rely=0.5, anchor="center")


label = customtkinter.CTkLabel(
    master=content_frame,
    text="DCTCompress",
    width=40,
    height=28,
    fg_color="transparent",
    font=("Roboto", 30),
)
label.pack(pady=20)


def select_file():
    filename = customtkinter.filedialog.askopenfilename()
    print(filename)
    fileLabel.configure(text=filename)
    fileLabel.configure(font=("Roboto", 12))
    fileLabel.update()


button = customtkinter.CTkButton(
    master=content_frame, text="Choose File", width=140, height=28, command=select_file
)
button.pack(pady=10)

fileLabel = customtkinter.CTkLabel(
    master=content_frame,
    width=40,
    height=28,
    text="No file selected",
    fg_color="transparent",
    wraplength=200,
    font=("Roboto", 10),
)
fileLabel.pack(pady=10)

inputsFrame = customtkinter.CTkFrame(content_frame)

firstRow = customtkinter.CTkFrame(inputsFrame, fg_color="transparent")
firstRow.columnconfigure(0, weight=1)
firstRow.columnconfigure(1, weight=1)

fLabel = customtkinter.CTkLabel(
    master=firstRow,
    width=40,
    height=28,
    text="F",
    fg_color="transparent",
    font=("Roboto", 15),
)
fLabel.grid(row=0, column=0)

fTextBox = customtkinter.CTkEntry(firstRow)
fTextBox.grid(row=0, column=1)

firstRow.pack(pady=(50, 20))

secondRow = customtkinter.CTkFrame(inputsFrame, fg_color="transparent")
secondRow.columnconfigure(0, weight=1)
secondRow.columnconfigure(1, weight=1)

dLabel = customtkinter.CTkLabel(
    master=secondRow,
    width=40,
    height=28,
    text="d",
    fg_color="transparent",
    font=("Roboto", 15),
)
dLabel.grid(row=0, column=0)

dTextBox = customtkinter.CTkEntry(secondRow)
dTextBox.grid(row=0, column=1)

secondRow.pack(pady=(10, 50))

inputsFrame.pack(pady=20)

def button_event():
    print("button pressed")

button = customtkinter.CTkButton(inputsFrame, text="Compress!", width=300, height=28)
button.pack()

root.mainloop()
