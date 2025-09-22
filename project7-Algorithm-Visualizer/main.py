import tkinter as tk
from tkinter import *
import time

bubble_pressed = False

def bubble_sort(array):
    if bubble_pressed == True:
        bars, labels = draw_bars(array)
        time.sleep(0.25)
        n = len(array)
        for i in range(n):
            # highlight_bar(i, bars)
            swapped = False
            for j in range(0, n-i-1):
                #highlight_bar(i, j, bars)
                highlight_bar(j, j+1, bars)
                canvas.update()
                #time.sleep(0.75)
                if array[j] > array[j+1]:
                    #swap_bars(j, j+1, bars)
                    array[j], array[j+1] = array[j+1], array[j]
                    
                    swap_bars(bars, labels, j, j+1)

                    bars[j], bars[j+1] = bars[j+1], bars[j]
                    
                    labels[j], labels[j+1] = labels[j+1], labels[j]

                    swapped = True

                reset_bar(j, j+1, bars)
                canvas.update()

            if swapped is False:
                break

        highlight_all_bars(bars)

def swap_bars(bars, labels, i, j, steps=20, delay=0.01):
    x1, _, _, _ = canvas.coords(bars[i])
    x2, _, _, _ = canvas.coords(bars[j])

    dx = x2 - x1

    step_x = dx / steps

    for _ in range(steps):


        canvas.move(bars[i], step_x, 0)
        canvas.move(labels[i], step_x, 0)

        canvas.move(bars[j], -step_x, 0)
        canvas.move(labels[j], -step_x, 0)

        canvas.update()
        time.sleep(delay)

    final_dx = x2 - canvas.coords(bars[i])[0]
    canvas.move(bars[i], final_dx, 0)
    canvas.move(labels[i], final_dx, 0)
    canvas.move(bars[j], -final_dx, 0)
    canvas.move(labels[j], -final_dx, 0)

    canvas.update()

def highlight_all_bars(bars):
    for i in bars:
        canvas.itemconfig(i, fill = "green")
    canvas.update()

# The way the rectangles are stored is that it gives them a ID that starts
# at 1 and incrememnts by 2 every id. So it goes 1, 3, 5, 7, 9
def highlight_bar(index, index2, rectangle):
    # This theoretically should match the rectangle id's to the index of the
    # element we are currently looking at in the sort. We are getting the
    # indices of the elements in rectangle
    current_rect = rectangle[index]
    next_rect = rectangle[index2]
    canvas.itemconfig(current_rect, fill="lightgreen")
    canvas.itemconfig(next_rect, fill="lightgreen")

def reset_bar(index, index2, rectangle):
    current_rect = rectangle[index]
    next_rect = rectangle[index2]

    canvas.itemconfig(current_rect, fill="red")
    canvas.itemconfig(next_rect, fill="red")

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
    else:
        font_size = 15
    
    x_gap = 20 # The gap between left canvas edge and y axis
    y_gap = 20 # The gap between lower canvas edge and x axis
    c_width = 1300
    c_height = 700
    
    bar_width = (c_width - 2 * x_gap) / n
    max_val = max(array)

    rects = []
    labels = []

    for i, val in enumerate(array):
        x0 = x_gap + i * bar_width
        x1 = x_gap + (i + 1) * bar_width
        
        bar_height = (val / max_val) * (c_height - 2 * y_gap)
        y0 = c_height - y_gap - bar_height
        y1 = c_height - y_gap
        
        rectangle = canvas.create_rectangle(x0, y0, x1, y1, fill="gray")
        rects.append(rectangle)
        label_x = (x0 + x1) / 2
        label_y = (y0 + y1) / 2
        text = canvas.create_text(label_x, label_y, text=val, font=("Helvetica", font_size))
        labels.append(text)
    canvas.update()
    return rects, labels
        
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
