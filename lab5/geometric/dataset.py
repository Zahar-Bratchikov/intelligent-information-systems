import pickle
import numpy as np

# Классы фигур
SHAPES = [
    "circle", "parallelogram", "rhombus", "trapezoid",
    "kite", "rectangle", "square", "triangle"
]

class DatasetManager:
    def __init__(self, input_size=40000):  # ← 200*200
        self.input_size = input_size
        self.samples = []

    def add_sample(self, vector, label):
        """Добавить образец"""
        if len(vector) != self.input_size:
            raise ValueError(f"Вектор должен быть длиной {self.input_size}")
        if label < 0 or label >= len(SHAPES):
            raise ValueError("Некорректная метка")
        self.samples.append((np.array(vector, dtype=float), label))

    def remove_sample(self, index):
        """Удалить образец по индексу"""
        if 0 <= index < len(self.samples):
            del self.samples[index]

    def update_sample(self, index, vector, label):
        """Обновить образец"""
        if 0 <= index < len(self.samples):
            if len(vector) != self.input_size:
                raise ValueError(f"Вектор должен быть длиной {self.input_size}")
            self.samples[index] = (np.array(vector, dtype=float), label)

    def get_data(self):
        """Вернуть X и y для обучения"""
        if not self.samples:
            return np.array([]), np.array([])
        X = np.array([s[0] for s in self.samples])
        y = np.array([s[1] for s in self.samples])
        # One-hot encoding
        Y = np.zeros((y.size, len(SHAPES)))
        Y[np.arange(y.size), y] = 1
        return X, Y

    def save(self, filename="dataset.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.samples, f)

    def load(self, filename="dataset.pkl"):
        try:
            with open(filename, "rb") as f:
                self.samples = pickle.load(f)
        except FileNotFoundError:
            self.samples = []