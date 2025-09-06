import tkinter as tk
from tkinter import *
from questionBank import questionBank
import random
from rapidfuzz import fuzz

def main():
    root = tk.Tk()
    root.title("Quiz Game")
    root.geometry("1000x700")
    l = Label(root, text="Welcome to the Quiz Game!", font=("Arial", 20, "bold underline"))
    l.pack()
    label_Category = Label(root, text="Select a category for the quiz:", font=("Arial", 16))
    label_Category.pack(pady=25)
    button_frame = Frame(root)
    button_frame.pack(pady=5)

    categories = [
        "Scuba Diving", "Fishing", "Hunting", "ELR/PRS Shooting", "Cybersecurity", "Coding",
        "Golf", "History", "Math", "Sports", "Science", "All"
    ]

    selected_category = tk.StringVar()
    selected_category.set(categories[11])
    global question_data_store
    question_data_store = []

    def select_category(category):
        global question_data_store
        selected_category.set(category)
        question_data_store = questionBank(category)

    for i, category in enumerate(categories):
        btn = Button(button_frame, text=category, width=15, height=1,
                     command=lambda c=category: select_category(c))
        btn.grid(row=i//6, column=i%6, padx=5, pady=5)
        
    label_Number = Label(root, text="Select the number of questions:", font=("Arial", 16))        
    label_Number.pack(pady=(10, 5))  # Reduce vertical padding above and below the label

    button_Answer_Frame = Frame(root)
    button_Answer_Frame.pack(pady=(0, 10))  # Reduce space above the buttons

    numbers = [5, 10, 15, 20]
    selected_number = tk.IntVar()
    selected_number.set(numbers[0])
    
    def select_number(number):
        selected_number.set(number)

    for i, number in enumerate(numbers):
        btn = Button(button_Answer_Frame, text=number, width=15, height=1,
                     command=lambda c=number: select_number(c))
        btn.grid(row=0, column=i, padx=5, pady=2)
        
    label_Start = Label(root, text="Ready to Start the Quiz?", font=("Arial", 16))
    label_Start.pack()
    
    start_selected = tk.StringVar()
    start_selected.set("None")
    
    def start_button_selected(status):
        start_selected.set(status)
        if selected_category.get() and selected_number.get():
            question_logic()
    
    start_button = Button(root, text="Start Quiz", width=20, height=2, command=lambda c="Start Quiz": start_button_selected(c))
    start_button.pack(pady=20)
    
    #if selected_category.get() != '' and selected_number.get() != 0 and start_selected.get() == "Start Quiz":
        #question_logic()
    
    question_frame = Frame(root, bd=2, relief="groove", padx=10, pady=10)
    question_frame.place(x=50, y=400, width=900, height=70)  # Shifted down and reduced height

    question_label_title = Label(question_frame, text="Question:", font=("Arial", 14, "bold"))
    question_label_title.place(x=0, y=0)

    question_text = tk.StringVar(value="Your question will appear here.")
    # Place question_display right next to the "Question:" label
    question_display = Label(question_frame, textvariable=question_text, font=("Arial", 12), wraplength=750, justify="left")
    question_display.place(x=110, y=0, height=30)  # x=110 aligns it beside the title label
    
    # Frame for displaying answers below the question box
    answer_frame = Frame(root, bd=2, relief="groove", padx=10, pady=10)
    answer_frame.place(x=50, y=480, width=900, height=150)

    def show_score_popup(score, total_questions):
        popup = Toplevel(root)
        popup.title("Quiz Result")
        popup.geometry("300x150")
        popup.transient(root)
        popup.grab_set()
        
        Label(popup, text=f"Your score: {score}/{total_questions}", font=("Arial", 14)).pack(pady=20)
        
        button_frame = Frame(popup)
        button_frame.pack()
        
        Button(button_frame, text = "Close", command=popup.destroy).pack(side=LEFT, padx=10)
        #Button(button_frame, text="Restart", command=lambda: [popup.destroy(), restart_quiz()]).pack(side=RIGHT, padx=10)

    # Store user answers
    user_answers = []
    current_question_index = [0]
    selected_questions = []

    # Function to update answer box based on answer type
    def display_answers(answer):
        # Clear previous widgets
        for widget in answer_frame.winfo_children():
            widget.destroy()

        if isinstance(answer, list):
            # Multiple choice or True/False
            display_options = [opt for opt in answer if not (isinstance(opt, str) and opt.startswith("Correct: "))]
            
            selected_option = tk.StringVar()
            for option in display_options:
                rb = Radiobutton(answer_frame, text=str(option), variable=selected_option, value=str(option), font=("Arial", 12))
                rb.pack(anchor="w", pady=2)
            answer_frame.selected_option = selected_option
            answer_frame.entry_widget = None
        else:
            # Short answer (answer is a string)
            entry = Entry(answer_frame, font=("Arial", 12), width=50)
            entry.pack(anchor="w", pady=2)
            answer_frame.entry_widget = entry
            answer_frame.selected_option = None

    def load_question(index):
        if index < len(selected_questions):
            question, answer = selected_questions[index]
            question_text.set(question)
            display_answers(answer)
        else:
            question_text.set("Quiz Complete!")
            for widget in answer_frame.winfo_children():
                widget.destroy()
        
            score = 0
            for i, (q, a) in enumerate(selected_questions):
                if isinstance(a, str):
                    correct = a
                elif isinstance(a, list):
                    if isinstance(a[-1], str) and a[-1].startswith("Correct: "):
                        correct = a[-1].replace("Correct: ", "")
                    else:
                        correct = a[0]
                else:
                    correct = a
                    
                user_response = str(user_answers[i]).strip().lower()
                correct_answer = str(correct).strip().lower()
                
                if user_response == correct_answer:
                    score += 1
                else:
                    similarity = fuzz.ratio(user_response, correct_answer)
                    if similarity >= 85:
                        score += 1

            show_score_popup(score, len(selected_questions))

    def next_question():
        # Save current answer
        idx = current_question_index[0]
        if idx < len(selected_questions):
            answer = None
            if hasattr(answer_frame, 'selected_option') and answer_frame.selected_option:
                answer = answer_frame.selected_option.get()
            elif hasattr(answer_frame, 'entry_widget') and answer_frame.entry_widget:
                answer = answer_frame.entry_widget.get()
            user_answers.append(answer)
            current_question_index[0] += 1
            load_question(current_question_index[0])

    next_btn = Button(root, text="Next", font=("Arial", 12), width=12, command=next_question)
    next_btn.place(x=830, y=650)  # Adjust x and y to position right of the answer box

    def question_logic():
        global question_data_store
        number = selected_number.get()
        # Use global selected_questions so next_question can access
        nonlocal selected_questions
        selected_questions = random.sample(list(question_data_store.items()), number)
        current_question_index[0] = 0
        user_answers.clear()
        load_question(0)
            
    root.mainloop()

if __name__ == "__main__":
    main()