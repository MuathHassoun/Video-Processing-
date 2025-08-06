from customtkinter import *
import video_processing
import video_processing_advance
global root

def next(current):
    if current == "advance":
        video_processing.main()
    elif current == "normal":
        video_processing_advance.advance_processing()

def open_advance():
    global root
    root.withdraw()
    video_processing_advance.advance_processing()

def open_normal():
    global root
    root.withdraw()
    video_processing.main()

root = CTk()
set_appearance_mode("light")
root.geometry("350x150+100+100")
root.resizable(False, False)

title_font = CTkFont(family="Times New Roman", size=25, weight="bold", slant="italic")
button_font = CTkFont(family="Times New Roman", size=15, weight="bold")

CTkLabel(root, text=" Choose Processing Type ", font=title_font, text_color="#0000FF").pack(pady=10)
CTkButton(root, text="Normal Processing", font=button_font, command=open_normal).pack(pady=10)
CTkButton(root, text="Advance Processing", font=button_font, command=open_advance).pack(pady=10)
root.mainloop()