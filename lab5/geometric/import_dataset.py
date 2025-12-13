import os
from PIL import Image
import numpy as np
from dataset import DatasetManager, SHAPES

# Параметр: размер, до которого уменьшать изображения (рекомендуется 28 или 64)
RESIZE_TO = 28  # ← можно изменить на 64, 16 и т.д.

def load_and_resize_image(path, size=28):
    """
    Загружает изображение (RGB или RGBA), удаляет белый фон,
    возвращает бинарный вектор (0.0 = фон, 1.0 = фигура).
    """
    img = Image.open(path).convert('RGB')  # приводим к RGB
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    arr = np.array(img)  # shape: (H, W, 3)

    # Белый фон: RGB ≈ (255, 255, 255)
    # Считаем пиксель "фоном", если все каналы >= 250
    is_background = (arr[:, :, 0] >= 250) & (arr[:, :, 1] >= 250) & (arr[:, :, 2] >= 250)
    # Фигура = НЕ фон
    binary = (~is_background).astype(float)  # True → 1.0, False → 0.0

    return binary.flatten()

def main(dataset_dir, save_path="dataset.pkl"):
    dataset = DatasetManager(input_size=RESIZE_TO * RESIZE_TO)
    total_added = 0

    print(f"Сканирование папок в: {dataset_dir}")
    for label_name in sorted(os.listdir(dataset_dir)):
        label_path = os.path.join(dataset_dir, label_name)
        if not os.path.isdir(label_path):
            continue

        # Проверяем, что папка соответствует известной фигуре
        if label_name not in SHAPES:
            print(f"Пропущена неизвестная папка: {label_name}")
            continue

        label_idx = SHAPES.index(label_name)
        files = [f for f in os.listdir(label_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        print(f"Обработка папки '{label_name}' ({len(files)} файлов)...")
        for filename in files:
            try:
                img_path = os.path.join(label_path, filename)
                vector = load_and_resize_image(img_path, size=RESIZE_TO)
                dataset.add_sample(vector, label_idx)
                total_added += 1
            except Exception as e:
                print(f"Ошибка при обработке {img_path}: {e}")

    print(f"\n✅ Всего добавлено: {total_added} образцов")
    dataset.save(save_path)
    print(f"Датасет сохранён в: {save_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Использование: python import_dataset.py <папка_с_подпапками>")
        print("Пример: python import_dataset.py ./dataset/")
        sys.exit(1)
    main(sys.argv[1])