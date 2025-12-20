import tkinter as tk
from tkinter import messagebox, simpledialog
import numpy as np
import pickle
import os
from neural_network import NeuralNetwork

# Отображение римских цифр
ROMAN_DIGITS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
GRID_SIZE = 10
PIXEL_SIZE = 30

class RomanRecognizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Распознавание римских цифр")
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.drawing = False

        # Инициализация нейросети
        self.nn = NeuralNetwork()
        self.nn.load_weights()
        self.nn.print_architecture()

        # Загрузка обучающей выборки
        self.dataset = self.load_dataset()

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Холст для рисования
        self.canvas = tk.Canvas(self.root, width=GRID_SIZE*PIXEL_SIZE, height=GRID_SIZE*PIXEL_SIZE, bg='white')
        self.canvas.grid(row=0, column=0, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        # Панель управления
        control_frame = tk.Frame(self.root)
        control_frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')

        tk.Button(control_frame, text="Распознать", command=self.recognize).pack(pady=5)
        tk.Button(control_frame, text="Очистить", command=self.clear_canvas).pack(pady=5)
        tk.Button(control_frame, text="Добавить в обучение", command=self.add_to_dataset).pack(pady=5)
        tk.Button(control_frame, text="Обучить сеть", command=self.train_network).pack(pady=5)
        tk.Button(control_frame, text="Управление выборкой", command=self.manage_dataset).pack(pady=5)

        self.result_label = tk.Label(control_frame, text="Результат: —", font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.draw_grid()

    def draw_grid(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x1, y1 = j * PIXEL_SIZE, i * PIXEL_SIZE
                x2, y2 = x1 + PIXEL_SIZE, y1 + PIXEL_SIZE
                color = "black" if self.grid[i][j] else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="lightgray")

    def start_draw(self, event):
        self.drawing = True
        self.update_pixel(event)

    def draw(self, event):
        if self.drawing:
            self.update_pixel(event)

    def stop_draw(self, _):
        self.drawing = False

    def update_pixel(self, event):
        col = event.x // PIXEL_SIZE
        row = event.y // PIXEL_SIZE
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            self.grid[row][col] = 1
            self.draw_grid()

    def clear_canvas(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.draw_grid()
        self.result_label.config(text="Результат: —")

    def get_flattened_input(self):
        return np.array(self.grid, dtype=float).flatten().reshape(1, -1)

    def recognize(self):
        X = self.get_flattened_input()
        if X.sum() == 0:
            messagebox.showwarning("Предупреждение", "Нарисуйте цифру!")
            return
        pred = self.nn.predict(X)[0]
        self.result_label.config(text=f"Результат: {ROMAN_DIGITS[pred]}")

    def add_to_dataset(self):
        X = self.get_flattened_input()
        if X.sum() == 0:
            messagebox.showwarning("Ошибка", "Нарисуйте цифру для добавления!")
            return
        label = simpledialog.askstring("Метка", "Введите римскую цифру (I–VII):")
        if label not in ROMAN_DIGITS:
            messagebox.showerror("Ошибка", "Неверная метка. Допустимы: I, II, III, IV, V, VI, VII.")
            return
        y = ROMAN_DIGITS.index(label)
        self.dataset.append((X.flatten(), y))
        self.save_dataset()
        messagebox.showinfo("Успех", f"Образ добавлен как '{label}'")

    def manage_dataset(self):
        if not self.dataset:
            messagebox.showinfo("Выборка", "Обучающая выборка пуста.")
            return
        info = "\n".join([f"{i+1}. {ROMAN_DIGITS[y]}" for i, (_, y) in enumerate(self.dataset)])
        choice = simpledialog.askstring("Выборка", f"Текущие примеры:\n{info}\n\n"
                                                    "Введите номер для удаления или '0' для отмены:")
        if choice and choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.dataset):
                del self.dataset[idx]
                self.save_dataset()
                messagebox.showinfo("Успех", "Пример удалён.")
            elif idx == -1:
                pass
            else:
                messagebox.showerror("Ошибка", "Неверный номер.")

    def train_network(self):
        if len(self.dataset) < 2:
            messagebox.showwarning("Ошибка", "Недостаточно данных для обучения (минимум 2 примера).")
            return
        X = np.array([item[0] for item in self.dataset])
        y = np.array([item[1] for item in self.dataset])
        # Преобразуем метки в one-hot encoding
        Y = np.zeros((y.size, 7))
        Y[np.arange(y.size), y] = 1

        self.nn.train(X, Y, epochs=2000, lr=0.3)
        self.nn.save_weights()
        messagebox.showinfo("Готово", "Сеть обучена и веса сохранены!")

    def load_dataset(self, path='dataset.pkl'):
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return pickle.load(f)
        return []

    def save_dataset(self, path='dataset.pkl'):
        with open(path, 'wb') as f:
            pickle.dump(self.dataset, f)

if __name__ == "__main__":
    root = tk.Tk()
    app = RomanRecognizerApp(root)
    root.mainloop()