import qrcode
from tkinter import *
from tkinter import colorchooser
from PIL import ImageTk, Image
import win32api
from pathlib import Path

# want a gui to control the settings and also display the qrcode, implement color wheels in tkinter to change color

fill_color_rgb = (0, 0, 0)
bg_color_rgb = (255, 255, 255)

downloads_path = Path.home() / "Downloads"

def qr_code_generate(version_param, error_correct_param, box_param, border_param):
    global file_name
    
    if error_correct_param == "Low":
        correction_param = qrcode.constants.ERROR_CORRECT_L
    elif error_correct_param == "Medium":
        correction_param = qrcode.constants.ERROR_CORRECT_M
    elif error_correct_param == "Strong":
        correction_param = qrcode.constants.ERROR_CORRECT_Q
    elif error_correct_param == "High":
        correction_param = qrcode.constants.ERROR_CORRECT_H
    else:
        correction_param = qrcode.constant.ERROR_CORRECT_M
    
    qr = qrcode.QRCode(
        version=version_param,
        error_correction=correction_param,
        box_size=box_param,
        border=border_param,
    )
    qr.add_data(qr_input.get())
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color_rgb, back_color=bg_color_rgb)
    file_name = file_name_input.get()
    file_path = downloads_path / "{}.png".format(file_name)
    img.save(file_path)
    display_qr()
    
    
def display_qr():
    file_path = downloads_path / "{}.png".format(file_name)
    qr_image = Image.open(file_path)
    qr_image = ImageTk.PhotoImage(qr_image)
    img_width = qr_image.width()
    img_height = qr_image.height() + 100
    popup = Toplevel()
    popup.geometry("{}x{}".format(img_width, img_height))
    popup.title("QR Code")
    
    label_for_image = Label(popup, image=qr_image)
    label_for_image.image = qr_image
    label_for_image.pack()
    
    def close():
        popup.destroy()
    
    print_button = Button(popup, text="Print", command=print_image, width=30, height=3)
    print_button.pack()
    
    close_button = Button(popup, text="Close", command=close, width=30, height=3)
    close_button.pack()

def print_image():
    file_path = downloads_path / "{}.png".format(file_name)
    win32api.ShellExecute(0, "open", str(file_path), None, ".", 1)

def choose_fill_color():
    # returns tuple of the color code (255, 255, 255)
    global fill_color_rgb
    chosen_color = colorchooser.askcolor()
    fill_color_rgb = chosen_color[0]
    fill_color_button.config(bg=chosen_color[1])

def choose_bg_color():
    global bg_color_rgb
    chosen_color = colorchooser.askcolor()
    bg_color_rgb = chosen_color[0]
    background_color_button.config(bg=chosen_color[1])

def submit():
    version_param = version_input.get()
    error_correction_param = option_clicked.get()
    box_param = box_input.get()
    border_param = border_input.get()
    qr_code_generate(version_param, error_correction_param, box_param, border_param)

def main():
    global fill_color_button, background_color_button, qr_input, option_clicked, version_input, box_input, border_input, file_name_input
    
    root = Tk()
    root.title("QR Code Generator")
    root.geometry("1200x1000")
    title_label = Label(root, text="QR Code Generator", font=("Helvetica", 24))
    title_label.pack(pady=10)
    qr_label = Label(root, text="Please enter the text / link for the qr code", font=("Helvetica", 16))
    qr_label.pack(pady=10)
    qr_input = Entry(root, width=50, font=("Helvetica", 16))
    qr_input.pack()
    version_label = Label(root, text="Enter the version you would like to use", font=("Helvetica", 16))
    version_label.pack(pady=2)
    version_description = Label(root, text="Controls how much data the QR Code can hold. Higher versions create larger QR codes", font=("Helvetica", 8))
    version_description.pack(pady=2)
    version_input = Scale(root, from_=1, to=40, orient=HORIZONTAL)
    version_input.pack(pady=2)
    version_input.set(5)
    option_clicked = StringVar()
    option_clicked.set("Medium")
    error_label = Label(root, text="Please select your error correction level", font=("Helvetica", 16))
    error_label.pack(pady=2)
    error_description = Label(root, text="Controls how much damage or distortion the QR code can tolerate. Higher levels are more reliable but produce larger QR Codes", font=("Helvetica", 8))
    error_description.pack(pady=2)
    error_input = OptionMenu(root, option_clicked, "Low", "Medium", "Strong", "High")
    error_input.pack(pady=2)
    box_label = Label(root, text="Please select your box level", font=("Helvetica", 16))
    box_label.pack(pady=2)
    box_description = Label(root, text="Controls how large each square in the QR code is. Higher values make a bigger image, but the QR code itself stays the same.", font=("Helvetica", 8))
    box_description.pack(pady=2)
    box_input = Scale(root, from_=1, to=50, orient=HORIZONTAL)
    box_input.pack(pady=2)
    box_input.set(10)
    border_label = Label(root, text="Please enter your border level", font=("Helvetica", 16))
    border_label.pack(pady=2)
    border_description = Label(root, text="Controls how much empty space surrounds the QR code.", font=("Helvetica", 8))
    border_description.pack(pady=2)
    border_input = Scale(root, from_=4, to=20, orient=HORIZONTAL)
    border_input.pack(pady=2)
    border_input.set(4)
    fill_color_label = Label(root, text="Please select your Fill Color", font=("Helvetica", 16))
    fill_color_label.pack(pady=2)
    fill_color_description = Label(root, text="Color of the QR Code Squares", font=("Helvetica", 8))
    fill_color_description.pack(pady=2)
    fill_color_button = Button(root, text="Choose the Fill Color", command=choose_fill_color, width=30, height=3)
    fill_color_button.pack(pady=2)
    background_color_label = Label(root, text="Please select your Background Color", font=("Helvetica", 16))
    background_color_label.pack(pady=2)
    background_color_description = Label(root, text="Color of the background behind the QR code", font=("Helvetica", 8))
    background_color_description.pack(pady=2)
    background_color_button = Button(root, text="Choose the Background Color", command=choose_bg_color, width=30, height=3)
    background_color_button.pack(pady=2)
    file_name_label = Label(root, text="Please Enter your desired file name", font=("Helvetica", 18))
    file_name_label.pack()
    file_name_input = Entry(root, width=50, font=("Helvetica", 16))
    file_name_input.pack()
    submit_button = Button(root, text="Generate", command=submit, font=("Helvetica", 16), width=25, height=2)
    submit_button.pack(pady=5)
    
    
    root.mainloop()

if __name__ == "__main__":
    main()