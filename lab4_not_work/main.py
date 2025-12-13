"""
Точка входа в систему поддержки принятия коллективных решений
"""
import sys
import os
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    """Запуск приложения"""
    # Создаем необходимые директории
    if not os.path.exists('data'):
        os.makedirs('data')
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()