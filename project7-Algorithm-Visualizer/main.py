import tkinter as tk
from tkinter import *

bubble_pressed = False

def bubble_sort(array):
    if bubble_pressed == True:
        n = len(array)
        bar_height(array)
        
        for i in range(n):
            swapped = False
            
            for j in range(0, n-i-1):
                if array[j] > array[j+1]:
                    array[j], array[j+1] = array[j+1], array[j]
                    swapped = True
            if (swapped == False):
                break
        print(array)
    
def bar_height(array):
    max_val = max(array) # bar fills entire canvas, rest of the values get scaled dynamically
    for val in array:
        if val != max_val:
            bar_height = val
            
        

def bubble_button():
    global bubble_pressed
    bubble_pressed = not bubble_pressed
    
def start():
    num_inputs = num_input.get().replace(" ", "").split(",")
    num_list = [int(num) for num in num_inputs]
    bubble_sort(num_list)

def main():
    global num_input
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
    
    
    root.mainloop()
    

if __name__ == "__main__":
    main()