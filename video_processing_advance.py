from customtkinter import *
import cv2
import numpy as np
global advance_window

def on_close():
    import main_controller
    global advance_window
    advance_window.destroy()
    main_controller.root.deiconify()

def switch_to_other_option():
    import main_controller
    global advance_window
    advance_window.destroy()
    main_controller.next("advance")

def advance_processing_actions(frame, levels=4, angle=60, checked=[0,1,0,0,0,0,1,0]):
    if checked[3] == 1:
        frame = cv2.bilateralFilter(frame, 9, 75, 75)

    if checked[1] == 1:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        quantized = (gray // (256 // levels)) * (256 // levels)
        frame = cv2.cvtColor(quantized, cv2.COLOR_GRAY2BGR)

    if checked[0] == 1:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    if checked[2] == 1:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        equalized = cv2.equalizeHist(gray)
        frame = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)

    if checked[4] == 1:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 5)
        color = cv2.bilateralFilter(frame, 9, 300, 300)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        frame = cartoon

    if checked[5] == 1:
        gray, sketch = cv2.pencilSketch(frame, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
        frame = sketch

    if checked[6] == 1:
        frame = cv2.flip(frame, 1)

    if checked[7] == 1:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[..., 0] = angle
        hsv[..., 1] = 255
        hsv[..., 2] = cv2.equalizeHist(hsv[..., 2])
        frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return frame
    
def advance_processing():
    set_appearance_mode("light") 
    global advance_window
    advance_window = CTkToplevel()
    advance_window.geometry("500x600+150+150")
    advance_window.resizable(False, False)   

    title_font = CTkFont(family="Times New Roman", size=30, weight="bold", slant="italic")
    option_font = CTkFont(family="Times New Roman", size=15, weight="bold")
    note_font = CTkFont(family="Times New Roman", size=14)
    
    switch_to_normal = CTkButton(
        advance_window,
        text="Normal",
        font=option_font,
        text_color="#000000",
        border_width=0,
        width=100,
        height=30,
        fg_color="transparent",
        hover=False,
        cursor="hand2",
        command=switch_to_other_option
    )
    switch_to_normal.place(relx=0.93, rely=0.02, anchor="center")

    title = CTkLabel(advance_window, text=" Choose processing filters: ", font=title_font, text_color="#0000FF")
    title.pack(pady=20)
    note_label = CTkLabel(advance_window, text="You can select multiple filters simultaneously.", font=note_font, text_color="#000000")
    note_label.place(relx=0.5, rely=0.115, anchor="center")

    vars_funcs = [
        (IntVar()),
        (IntVar()),
        (IntVar()),
        (IntVar()),
        (IntVar()),
        (IntVar()),
        (IntVar()),
        (IntVar()),
    ]

    labels = [
        "1 - Edge Detection",
        "2 - Grayscale Quantization",
        "3 - Contrast Enhancement",
        "4 - Soft and Polished Appearance",
        "5 - Cartoon Filter",
        "6 - Pencil Sketch",
        "7 - Mirror Filter",
        "8 - Night Vision"
    ]

    mode_labels = [
        "Green",
        "Red",
        "Blue"
    ]
    combo_box = CTkComboBox(advance_window, font=option_font, text_color="#000000", values=mode_labels, state="readonly")


    for i, (var, label_text) in enumerate(zip(vars_funcs, labels)):
        checkbox = CTkCheckBox(advance_window, text=label_text, font=option_font, text_color="#000000", variable=var)
        checkbox.place(relx=0.1, rely=0.15 + i * 0.08, anchor="w")

    rely_levels = 0.8
    levels_var_advance = StringVar(value="4")
    levels_label = CTkLabel(advance_window, text="Grayscale levels:", font=option_font, text_color="#000000")
    levels_label.place(relx=0.1, rely=rely_levels, anchor="w")
    levels_entry_advance = CTkEntry(advance_window, textvariable=levels_var_advance, width=50)
    levels_entry_advance.place(relx=0.5, rely=rely_levels, anchor="center")
    levels_var_example = CTkLabel(advance_window, text="(e.g. 4, 8, 16, or 256)", font=option_font, text_color="#000000")
    levels_var_example.place(relx=0.7, rely=rely_levels, anchor="center")
    msg_text_field = CTkLabel(advance_window, text="", font=option_font, text_color="#FF0000")

    def start_processing():
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            msg_text_field.configure(text="Could not open camera.", text_color="#FF0000")
            return

        try:
            levels = int(levels_var_advance.get())
        except:
            levels = 4
            msg_text_field.configure(text="Invalid grayscale level! Using default: 4", text_color="#FF0000")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            processed = frame.copy()
            processed = cv2.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
            checked = [var.get() for var in vars_funcs]
            
            color_mode = combo_box.get()
            angle_map = {"Red": 0, "Green": 60, "Blue": 120}
            angle = angle_map.get(color_mode, 60)
            processed = advance_processing_actions(processed, levels=levels, angle=angle, checked=checked)                   

            cv2.imshow("Processed Video", processed)
            if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Processed Video", cv2.WND_PROP_VISIBLE) < 1:
                break
        cap.release()
        cv2.destroyAllWindows()

    combo_label = CTkLabel(advance_window, text="Night Vision Mode:", font=option_font, text_color="#000000")
    combo_label.place(relx=0.1, rely=0.85, anchor="w")
    combo_box.place(relx=0.45, rely=0.85, anchor="w")
    msg_text_field.place(relx=0.1, rely=0.9, anchor="w")

    start_button = CTkButton(advance_window, text="Start Camera", font=option_font, command=start_processing)
    start_button.place(relx=0.85, rely=0.97, anchor="center")
    advance_window.protocol("WM_DELETE_WINDOW", on_close)
    advance_window.mainloop()