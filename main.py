import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# Константы
HISTORY_FILE = 'history.json'
MIN_LEN = 6
MAX_LEN = 32

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.history = []

        self.load_history()

        self.create_widgets()

    def create_widgets(self):
        # Длина пароля
        tk.Label(self.root, text="Длина пароля:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.length_var = tk.IntVar(value=12)
        self.length_scale = tk.Scale(self.root, from_=MIN_LEN, to=MAX_LEN, orient='horizontal',
                                     variable=self.length_var)
        self.length_scale.grid(row=0, column=1, padx=5, pady=5, sticky='we')

        # Чекбоксы
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=False)

        tk.Checkbutton(self.root, text="Цифры (0-9)", variable=self.use_digits).grid(row=1, column=0, sticky='w', padx=5)
        tk.Checkbutton(self.root, text="Буквы (a-z, A-Z)", variable=self.use_letters).grid(row=1, column=1, sticky='w', padx=5)
        tk.Checkbutton(self.root, text="Спецсимволы (!@#$...)", variable=self.use_symbols).grid(row=1, column=2, sticky='w', padx=5)

        # Генерация пароля
        self.generate_button = tk.Button(self.root, text="Генерировать", command=self.generate_password)
        self.generate_button.grid(row=2, column=0, columnspan=3, pady=10)

        # Таблица истории
        self.tree = ttk.Treeview(self.root, columns=('Password',), show='headings', height=10)
        self.tree.heading('Password', text='Сгенерированный пароль')
        self.tree.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

        # Настройка растяжения таблицы
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        # Загрузить историю в таблицу
        self.load_history_into_table()

    def generate_password(self):
        length = self.length_var.get()
        if length < MIN_LEN or length > MAX_LEN:
            messagebox.showerror("Ошибка", f"Длина должна быть между {MIN_LEN} и {MAX_LEN}")
            return

        symbols = ""
        if self.use_digits.get():
            symbols += "0123456789"
        if self.use_letters.get():
            symbols += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if self.use_symbols.get():
            symbols += "!@#$%^&*()_+-=[]{}|;:,.<>/?"

        if not symbols:
            messagebox.showwarning("Внимание", "Выберите хотя бы один тип символов")
            return

        password = ''.join(random.choice(symbols) for _ in range(length))
        self.add_to_history(password)

    def add_to_history(self, password):
        self.history.append(password)
        self.save_history()
        self.load_history_into_table()

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r') as f:
                    self.history = json.load(f)
            except json.JSONDecodeError:
                self.history = []
        else:
            self.history = []

    def save_history(self):
        with open(HISTORY_FILE, 'w') as f:
            json.dump(self.history, f)

    def load_history_into_table(self):
        # Очистить таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Добавить новую историю
        for pw in reversed(self.history):  # отображать последние сверху
            self.tree.insert('', 'end', values=(pw,))


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.geometry('600x400')
    root.mainloop()