import tkinter as tk
from tkinter import *

bubble_pressed = False

def bubble_sort(array):
    if bubble_pressed == True:
        draw_bars(array)
        n = len(array)
        
        for i in range(n):
            swapped = False
            
            for j in range(0, n-i-1):
                if array[j] > array[j+1]:
                    array[j], array[j+1] = array[j+1], array[j]
                    swapped = True
            if (swapped == False):
                break
    
    
def draw_bars(array):
    canvas.delete("all")
    
    n = len(array)
    if n == 0:
        return
    
    if 35 <= n <= 50:
        font_size = 10
    elif 15 <= n <= 34:
        font_size = 20
    elif 1 <= n <= 14:
        font_size = 30
    
    x_gap = 20 # The gap between left canvas edge and y axis
    y_gap = 20 # The gap between lower canvas edge and x axis
    c_width = 1300
    c_height = 700
    
    bar_width = (c_width - 2 * x_gap) / n
    max_val = max(array)

    for i, val in enumerate(array):
        x0 = x_gap + i * bar_width
        x1 = x_gap + (i + 1) * bar_width
        
        bar_height = (val / max_val) * (c_height - 2 * y_gap)
        y0 = c_height - y_gap - bar_height
        y1 = c_height - y_gap
        
        canvas.create_rectangle(x0, y0, x1, y1, fill="gray")
        label_x = (x0 + x1) / 2
        label_y = (y0 + y1) / 2
        canvas.create_text(label_x, label_y, text=val, font=("Helvetica", font_size))
        
def bubble_button():
    global bubble_pressed
    bubble_pressed = not bubble_pressed
    
def start():
    num_inputs = num_input.get().replace(" ", "").split(",")
    num_list = [int(num) for num in num_inputs]
    bubble_sort(num_list)

def main():
    global num_input
    global canvas
    root = tk.Tk()
    root.title("Algorithm Visualizer")
    root.geometry("1400x900")
    sort_label = Label(root, text="Select a Sort", font=("Helvetica", 14))
    sort_label.pack()
    bubble_sort = Button(root, text="Bubble Sort", command=bubble_button, font=("Helvetica", 14))
    bubble_sort.pack()
    numbers_label = Label(root, text="Please enter a comma seperated list of numbers", font=("Helvetica", 14))
    numbers_label.pack()
    num_input = Entry(root, width=50, font=("Helvetica", 16))
    num_input.pack()
    start_button = Button(root, text="Start", command=start, font=("Hevletica", 14))
    start_button.pack()
    c_width = 1300
    c_height = 700
    canvas = tk.Canvas(root, width=c_width, height=c_height, bg='light gray')
    canvas.pack()
    
    
    root.mainloop()
    

if __name__ == "__main__":
    main()