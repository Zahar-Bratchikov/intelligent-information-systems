"""
Диалоговые окна для голосования
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QLabel, QComboBox, QListWidget, 
                             QPushButton, QMessageBox)

class VotingDialog(QDialog):
    """Диалоговое окно для голосования"""
    
    def __init__(self, candidates: list, vote_type: str):
        super().__init__()
        self.candidates = candidates
        self.vote_type = vote_type
        self.selected_vote = None
        
        self.setWindowTitle("Голосование")
        self.setGeometry(200, 200, 400, 300)
        self.init_ui()
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        if self.vote_type == "simple":
            layout.addWidget(QLabel("Выберите одно место для отдыха:"))
            self.combo = QComboBox()
            self.combo.addItems(self.candidates)
            layout.addWidget(self.combo)
        else:  # ranked
            layout.addWidget(QLabel("Ранжируйте места для отдыха (перетащите в нужном порядке):"))
            self.list_widget = QListWidget()
            self.list_widget.addItems(self.candidates)
            self.list_widget.setDragDropMode(QListWidget.InternalMove)
            layout.addWidget(self.list_widget)
        
        # Кнопки
        button_layout = QHBoxLayout()
        self.ok_btn = QPushButton("Голосовать")
        self.cancel_btn = QPushButton("Отмена")
        self.ok_btn.clicked.connect(self.accept_vote)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
    
    def accept_vote(self):
        """Подтверждение голоса"""
        if self.vote_type == "simple":
            self.selected_vote = self.combo.currentText()
        else:
            # Получаем ранжировку из списка
            items = []
            for i in range(self.list_widget.count()):
                items.append(self.list_widget.item(i).text())
            self.selected_vote = items
        
        self.accept()
    
    def get_vote(self):
        """Возвращает результат голосования"""
        return self.selected_vote