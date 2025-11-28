import os
from PIL import Image
import numpy as np
from dataset import DatasetManager, SHAPES

def load_image_as_vector(path):
    """Загружает PNG 200x200 → вектор из 40000 float (0.0 или 1.0)"""
    img = Image.open(path).convert('L')  # grayscale
    if img.size != (200, 200):
        raise ValueError(f"Изображение {path} не 200x200! Размер: {img.size}")
    arr = np.array(img)
    # Бинаризация: чёрное = фигура = 1.0
    binary = (arr < 128).astype(float)
    return binary.flatten()  # (40000,)

def extract_label(filename):
    basename = os.path.basename(filename)
    return basename.split('_')[0].split('.')[0]

def main(dataset_dir, save_path="dataset.pkl"):
    dataset = DatasetManager(input_size=40000)
    files = [f for f in os.listdir(dataset_dir) if f.endswith('.png')]
    print(f"Найдено {len(files)} PNG-файлов...")

    count = 0
    for i, f in enumerate(files):
        try:
            label = extract_label(f)
            if label not in SHAPES:
                continue
            vec = load_image_as_vector(os.path.join(dataset_dir, f))
            dataset.add_sample(vec, SHAPES.index(label))
            count += 1
        except Exception as e:
            print(f"Пропущен {f}: {e}")
        
        if (i + 1) % 5000 == 0:
            print(f"Обработано: {i + 1}")

    print(f"Добавлено {count} образцов.")
    dataset.save(save_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Использование: python import_dataset.py <папка>")
        sys.exit(1)
    main(sys.argv[1])