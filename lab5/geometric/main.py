import tkinter as tk
from tkinter import messagebox, simpledialog
import numpy as np
from neural_network import NeuralNetwork
from dataset import DatasetManager, SHAPES

CANVAS_SIZE = 200  # ← теперь 200x200
INPUT_SIZE = CANVAS_SIZE * CANVAS_SIZE  # 40000

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Распознавание фигур (200×200)")
        self.dataset = DatasetManager(input_size=INPUT_SIZE)
        self.dataset.load()

        # Подберите скрытый слой поменьше, иначе не обучится
        self.network = NeuralNetwork(
            input_size=INPUT_SIZE,
            hidden_size=128,          # ← уменьшено (иначе слишком тяжело)
            output_size=len(SHAPES),
            learning_rate=0.01        # ← уменьшено из-за большого входа
        )

        # Кнопки
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Обучить", command=self.train_network).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Распознать", command=self.predict).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Очистить", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)

        # Холст 200x200
        self.canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg='white')
        self.canvas.pack(pady=5)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.paint)  # клик тоже рисует

        self.image_data = np.zeros((CANVAS_SIZE, CANVAS_SIZE), dtype=int)  # 200x200

        # Архитектура
        arch_label = tk.Label(root, text="Архитектура: " + self.network.get_architecture())
        arch_label.pack(pady=5)

    def paint(self, event):
        x, y = event.x, event.y
        if 0 <= x < CANVAS_SIZE and 0 <= y < CANVAS_SIZE:
            # Рисуем "кисть" 3x3 для удобства
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < CANVAS_SIZE and 0 <= ny < CANVAS_SIZE:
                        self.image_data[ny, nx] = 1
                        self.canvas.create_rectangle(nx, ny, nx+1, ny+1, fill="black", outline="")

    def clear_canvas(self):
        self.image_data.fill(0)
        self.canvas.delete("all")

    def get_input_vector(self):
        return self.image_data.flatten().astype(float)  # (40000,)

    def add_to_dataset(self):
        vec = self.get_input_vector()
        label = simpledialog.askinteger(
            "Метка",
            f"Введите номер фигуры (0–{len(SHAPES)-1}):\n" +
            "\n".join(f"{i}: {s}" for i, s in enumerate(SHAPES))
        )
        if label is not None and 0 <= label < len(SHAPES):
            self.dataset.add_sample(vec, label)
            self.dataset.save()
            messagebox.showinfo("Успех", "Образец добавлен!")
        else:
            messagebox.showwarning("Ошибка", "Неверная метка.")

    def remove_from_dataset(self):
        idx = simpledialog.askinteger("Индекс", f"Индекс (0–{len(self.dataset.samples)-1})")
        if idx is not None and 0 <= idx < len(self.dataset.samples):
            self.dataset.remove_sample(idx)
            self.dataset.save()
            messagebox.showinfo("Успех", "Удалено.")
        else:
            messagebox.showwarning("Ошибка", "Неверный индекс.")

    def edit_dataset(self):
        idx = simpledialog.askinteger("Индекс", f"Индекс (0–{len(self.dataset.samples)-1})")
        if idx is not None and 0 <= idx < len(self.dataset.samples):
            vec = self.get_input_vector()
            label = simpledialog.askinteger("Метка", f"Новая метка (0–{len(SHAPES)-1})")
            if label is not None and 0 <= label < len(SHAPES):
                self.dataset.update_sample(idx, vec, label)
                self.dataset.save()
                messagebox.showinfo("Успех", "Обновлено.")
        else:
            messagebox.showwarning("Ошибка", "Неверный индекс.")

    def train_network(self):
        X, Y = self.dataset.get_data()
        if X.size == 0:
            messagebox.showwarning("Ошибка", "Нет данных!")
            return
        # Обучаем с меньшим числом эпох за раз
        self.network.train(X, Y, epochs=200)
        messagebox.showinfo("Успех", "Эпохи 200 пройдены!")

    def predict(self):
        vec = self.get_input_vector().reshape(1, -1)
        pred = self.network.predict(vec)[0]
        messagebox.showinfo("Результат", f"Распознано: {SHAPES[pred]}")

    def run(self):
        # Добавим меню для управления выборкой
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        data_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Датасет", menu=data_menu)
        data_menu.add_command(label="Добавить текущий рисунок", command=self.add_to_dataset)
        data_menu.add_command(label="Удалить элемент", command=self.remove_from_dataset)
        data_menu.add_command(label="Редактировать элемент", command=self.edit_dataset)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.run()
    root.mainloop()