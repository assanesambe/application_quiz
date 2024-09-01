import tkinter as tk
from tkinter import messagebox
import json

class Quiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("500x400")

        # Charger les questions du fichier JSON
        self.load_questions()

        # Initialisation des variables
        self.score = 0
        self.current_question = 0
        self.total_questions = len(self.questions)

        # Interface graphique
        self.question_label = tk.Label(root, text="", font=("Arial", 16), wraplength=400)
        self.question_label.pack(pady=20)

        self.option_var = tk.StringVar(value="")
        self.options = [tk.Radiobutton(root, text="", variable=self.option_var, value=i, font=("Arial", 14)) for i in range(4)]
        for option in self.options:
            option.pack(anchor="w")

        self.submit_button = tk.Button(root, text="Submit", command=self.submit_answer)
        self.submit_button.pack(pady=20)

        self.next_button = tk.Button(root, text="Next", command=self.next_question)
        self.next_button.pack(pady=10)
        self.next_button.config(state=tk.DISABLED)  # Désactiver le bouton Next au départ

        self.quit_button = tk.Button(root, text="Quit", command=self.root.quit)
        self.quit_button.pack(pady=10)

        # Afficher la première question
        self.display_question()

    def load_questions(self):
        with open("questions.json", "r") as file:
            data = json.load(file)
        self.questions = data["questions"]

    def display_question(self):
        question_data = self.questions[self.current_question]
        self.question_label.config(text=question_data["question"])
        for i, option in enumerate(question_data["options"]):
            self.options[i].config(text=option)
        self.option_var.set("")  # Réinitialiser l'option sélectionnée

    def submit_answer(self):
        selected_option = self.option_var.get()
        if selected_option == "":
            messagebox.showwarning("Attention", "Veuillez sélectionner une option avant de soumettre.")
            return

        correct_answer = self.questions[self.current_question]["answer"]
        selected_text = self.questions[self.current_question]["options"][int(selected_option)]
        if selected_text == correct_answer:
            self.score += 1

        # Désactiver le bouton Submit et activer le bouton Next
        self.submit_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        # Passer à la question suivante
        self.current_question += 1
        if self.current_question < self.total_questions:
            self.display_question()
            self.submit_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.DISABLED)
        else:
            self.display_results()

    def display_results(self):
        incorrect_answers = self.total_questions - self.score
        result_message = f"Quiz terminé !\nScore: {self.score}/{self.total_questions}\nCorrect: {self.score}\nIncorrect: {incorrect_answers}"
        messagebox.showinfo("Résultats", result_message)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    quiz_app = Quiz(root)
    root.mainloop()
