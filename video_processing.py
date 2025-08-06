from customtkinter import *
import cv2
import numpy as np
global interface

def on_close():
    import main_controller
    global interface
    interface.destroy()
    main_controller.root.deiconify()

def switch_to_other_option():
    import main_controller
    global interface
    interface.destroy()
    main_controller.next("normal")

def edge_detection(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

def grayscale_quantization(frame, levels=4):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    quantized = (gray // (256 // levels)) * (256 // levels)
    return cv2.cvtColor(quantized, cv2.COLOR_GRAY2BGR)
    
def contrast_enhancement(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    equalized = cv2.equalizeHist(gray)
    return cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)

def soft_appearance(frame):
    return cv2.bilateralFilter(frame, 9, 75, 75)

def cartoon_filter(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 5)
    color = cv2.bilateralFilter(frame, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

def pencil_sketch(frame):
    gray, sketch = cv2.pencilSketch(frame, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
    return sketch

def mirror_filter(frame):
    return cv2.flip(frame, 1)

def night_vision(frame, angle=60):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv[..., 0] = angle
    hsv[..., 1] = 255
    hsv[..., 2] = cv2.equalizeHist(hsv[..., 2])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def main():
    set_appearance_mode("light")
    global interface
    interface = CTkToplevel()
    interface.geometry("500x600+150+150")
    interface.resizable(False, False)
    
    title_font = CTkFont(family="Times New Roman", size=30, weight="bold", slant="italic")
    option_font = CTkFont(family="Times New Roman", size=15, weight="bold")

    switch_to_advance = CTkButton(
        interface,
        text="Advance",
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
    switch_to_advance.place(relx=0.93, rely=0.02, anchor="center")

    title = CTkLabel(interface, text=" Choose processing filter: ", font=title_font, text_color="#0000FF")
    title.pack(pady=20)
    selected_option = StringVar(value="edge_detection");
    options = [
        "edge_detection",
        "grayscale_quantization",
        "contrast_enhancement",
        "soft_appearance",
        "cartoon_filter",
        "pencil_sketch",
        "mirror_filter",
        "night_vision"
    ]

    vars_funcs = [
        (selected_option, edge_detection),
        (selected_option, grayscale_quantization),
        (selected_option, contrast_enhancement),
        (selected_option, soft_appearance),
        (selected_option, cartoon_filter),
        (selected_option, pencil_sketch),
        (selected_option, mirror_filter),
        (selected_option, night_vision),
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
    combo_box = CTkComboBox(interface, font=option_font, text_color="#000000", values=mode_labels, state="readonly")


    for i, (var_func, label_text, option_num) in enumerate(zip(vars_funcs, labels, options)):
        var, _ = var_func
        radio_button = CTkRadioButton(interface, text=label_text, font=option_font, text_color="#000000", variable=var, value=option_num)
        radio_button.place(relx=0.1, rely=0.15 + i * 0.08, anchor="w")

    rely_levels = 0.8
    levels_var = StringVar(value="4")
    levels_label = CTkLabel(interface, text="Grayscale levels:", font=option_font, text_color="#000000")
    levels_label.place(relx=0.1, rely=rely_levels, anchor="w")
    levels_entry = CTkEntry(interface, textvariable=levels_var, width=50)
    levels_entry.place(relx=0.5, rely=rely_levels, anchor="center")
    levels_var_example = CTkLabel(interface, text="(e.g. 4, 8, 16, or 256)", font=option_font, text_color="#000000")
    levels_var_example.place(relx=0.7, rely=rely_levels, anchor="center")
    msg_text_field = CTkLabel(interface, text="", font=option_font, text_color="#FF0000")
    
    def start_processing():
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            msg_text_field.configure(text="Could not open camera.", text_color="#FF0000")
            return

        try:
            levels = int(levels_var.get())
        except:
            levels = 4
            msg_text_field.configure(text="Invalid grayscale level! Using default: 4", text_color="#FF0000")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            processed = frame.copy()
            processed = cv2.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
            global_option = ""
            for (var, func), option in zip(vars_funcs, options):
                if var.get() == option:
                    msg_text_field.configure(text=option + " is now running", text_color="#006400")
                    msg_text_field.update_idletasks()
                    if func == grayscale_quantization:
                        global_option = option
                        processed = func(processed, levels=levels)
                    elif func == night_vision:
                        global_option = option
                        color_mode = combo_box.get()
                        angle_map = {"Red": 0, "Green": 60, "Blue": 120}
                        angle = angle_map.get(color_mode, 60)
                        processed = func(processed, angle=angle)
                    else:
                        global_option = option
                        processed = func(processed)

            cv2.imshow("Processed Video", processed)
            if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Processed Video", cv2.WND_PROP_VISIBLE) < 1:
                msg_text_field.configure(text=global_option + " has finished running", text_color="#006400")
                msg_text_field.update_idletasks()
                break
        cap.release()
        cv2.destroyAllWindows()

    combo_label = CTkLabel(interface, text="Night Vision Mode:", font=option_font, text_color="#000000")
    combo_label.place(relx=0.1, rely=0.85, anchor="w")
    combo_box.place(relx=0.45, rely=0.85, anchor="w")
    msg_text_field.place(relx=0.1, rely=0.9, anchor="w")

    start_button = CTkButton(interface, text="Start Camera", font=option_font, command=start_processing)
    start_button.place(relx=0.85, rely=0.97, anchor="center")
    interface.protocol("WM_DELETE_WINDOW", on_close)
    interface.mainloop()