"""
Главное окно графического интерфейса
"""
import sys
import yaml
from typing import Dict  # Добавлен импорт Dict
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QComboBox, QTextEdit, 
                             QTabWidget, QTableWidget, QTableWidgetItem,
                             QGroupBox, QFormLayout, QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt
from models import MajorityModel, CondorcetModel, BordaModel
from gui.voting_dialog import VotingDialog

class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система поддержки принятия коллективных решений")
        self.setGeometry(100, 100, 800, 600)
        
        # Загрузка данных о местах отдыха
        self.locations = self.load_locations()
        self.candidates = [loc['name'] for loc in self.locations]
        
        # Данные для голосования
        self.simple_votes = []  # Простые голоса (выбор одного варианта)
        self.ranked_votes = []  # Ранжированные голоса
        
        self.init_ui()
    
    def load_locations(self):
        """Загружает список мест отдыха из YAML файла"""
        try:
            with open('data/locations.yaml', 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return data['locations']
        except FileNotFoundError:
            # Создаем базовый список, если файл не найден
            default_locations = [
                {"name": "Крым", "description": "Пляжный отдых в России"},
                {"name": "Турция", "description": "Пляжный отдых за границей"},
                {"name": "Сочи", "description": "Горнолыжный отдых в России"},
                {"name": "Париж", "description": "Городской тур за границей"}
            ]
            return default_locations
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Заголовок
        title_label = QLabel("Выбор совместного места для отдыха")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Кнопки голосования
        voting_layout = QHBoxLayout()
        self.simple_vote_btn = QPushButton("Простое голосование")
        self.ranked_vote_btn = QPushButton("Ранжированное голосование")
        self.simple_vote_btn.clicked.connect(self.open_simple_voting)
        self.ranked_vote_btn.clicked.connect(self.open_ranked_voting)
        voting_layout.addWidget(self.simple_vote_btn)
        voting_layout.addWidget(self.ranked_vote_btn)
        layout.addLayout(voting_layout)
        
        # Информация о текущих голосах
        self.votes_info = QLabel("Голоса: Простые - 0, Ранжированные - 0")
        layout.addWidget(self.votes_info)
        
        # Вкладки с моделями
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_majority_tab(), "Относительное большинство")
        self.tabs.addTab(self.create_condorcet_tab(), "Модель Кондорсе")
        self.tabs.addTab(self.create_borda_tab(), "Модель Борда")
        layout.addWidget(self.tabs)
        
        # Кнопка расчета
        self.calculate_btn = QPushButton("Рассчитать результаты")
        self.calculate_btn.clicked.connect(self.calculate_results)
        layout.addWidget(self.calculate_btn)
    
    def create_majority_tab(self):
        """Создает вкладку для модели относительного большинства"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.majority_result = QLabel("Результаты еще не рассчитаны")
        self.majority_result.setWordWrap(True)
        layout.addWidget(self.majority_result)
        
        self.majority_table = QTableWidget(0, 2)
        self.majority_table.setHorizontalHeaderLabels(["Место отдыха", "Голоса"])
        layout.addWidget(self.majority_table)
        
        widget.setLayout(layout)
        return widget
    
    def create_condorcet_tab(self):
        """Создает вкладку для модели Кондорсе"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Явный победитель
        condorcet_group = QGroupBox("Явный победитель Кондорсе")
        condorcet_layout = QVBoxLayout()
        self.condorcet_result = QLabel("Результаты еще не рассчитаны")
        self.condorcet_result.setWordWrap(True)
        condorcet_layout.addWidget(self.condorcet_result)
        condorcet_group.setLayout(condorcet_layout)
        layout.addWidget(condorcet_group)
        
        # Правило Копленда
        copeland_group = QGroupBox("Правило Копленда")
        copeland_layout = QVBoxLayout()
        self.copeland_result = QLabel("Результаты еще не рассчитаны")
        self.copeland_result.setWordWrap(True)
        copeland_layout.addWidget(self.copeland_result)
        self.copeland_table = QTableWidget(0, 2)
        self.copeland_table.setHorizontalHeaderLabels(["Место отдыха", "Баллы"])
        copeland_layout.addWidget(self.copeland_table)
        copeland_group.setLayout(copeland_layout)
        layout.addWidget(copeland_group)
        
        # Правило Симпсона
        simpson_group = QGroupBox("Правило Симпсона")
        simpson_layout = QVBoxLayout()
        self.simpson_result = QLabel("Результаты еще не рассчитаны")
        self.simpson_result.setWordWrap(True)
        simpson_layout.addWidget(self.simpson_result)
        self.simpson_table = QTableWidget(0, 2)
        self.simpson_table.setHorizontalHeaderLabels(["Место отдыха", "Мин. победы"])
        simpson_layout.addWidget(self.simpson_table)
        simpson_group.setLayout(simpson_layout)
        layout.addWidget(simpson_group)
        
        widget.setLayout(layout)
        return widget
    
    def create_borda_tab(self):
        """Создает вкладку для модели Борда"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.borda_result = QLabel("Результаты еще не рассчитаны")
        self.borda_result.setWordWrap(True)
        layout.addWidget(self.borda_result)
        
        self.borda_table = QTableWidget(0, 2)
        self.borda_table.setHorizontalHeaderLabels(["Место отдыха", "Баллы"])
        layout.addWidget(self.borda_table)
        
        widget.setLayout(layout)
        return widget
    
    def open_simple_voting(self):
        """Открывает диалог простого голосования"""
        dialog = VotingDialog(self.candidates, "simple")
        if dialog.exec_():
            vote = dialog.get_vote()
            if vote:
                self.simple_votes.append(vote)
                self.update_votes_info()
    
    def open_ranked_voting(self):
        """Открывает диалог ранжированного голосования"""
        dialog = VotingDialog(self.candidates, "ranked")
        if dialog.exec_():
            vote = dialog.get_vote()
            if vote:
                self.ranked_votes.append(vote)
                self.update_votes_info()
    
    def update_votes_info(self):
        """Обновляет информацию о количестве голосов"""
        self.votes_info.setText(f"Голоса: Простые - {len(self.simple_votes)}, Ранжированные - {len(self.ranked_votes)}")
    
    def calculate_results(self):
        """Рассчитывает результаты по всем моделям"""
        if not self.simple_votes and not self.ranked_votes:
            QMessageBox.warning(self, "Ошибка", "Нет голосов для анализа!")
            return
        
        # Модель относительного большинства
        if self.simple_votes:
            majority_model = MajorityModel(self.candidates, self.simple_votes)
            winner, results, explanation = majority_model.calculate_winner()
            self.majority_result.setText(explanation)
            self.update_table(self.majority_table, results)
        else:
            self.majority_result.setText("Нет простых голосов для анализа")
            self.majority_table.setRowCount(0)
        
        # Модель Кондорсе (требует ранжированные голоса)
        if self.ranked_votes:
            condorcet_model = CondorcetModel(self.candidates, self.ranked_votes)
            
            # Явный победитель
            cond_winner, cond_explanation = condorcet_model.find_condorcet_winner()
            self.condorcet_result.setText(cond_explanation)
            
            # Правило Копленда
            cop_winner, cop_scores, cop_explanation = condorcet_model.copeland_rule()
            self.copeland_result.setText(cop_explanation)
            self.update_table(self.copeland_table, cop_scores)
            
            # Правило Симпсона
            simp_winner, simp_scores, simp_explanation = condorcet_model.simpson_rule()
            self.simpson_result.setText(simp_explanation)
            self.update_table(self.simpson_table, simp_scores)
        else:
            self.condorcet_result.setText("Нет ранжированных голосов для анализа")
            self.copeland_result.setText("Нет ранжированных голосов для анализа")
            self.simpson_result.setText("Нет ранжированных голосов для анализа")
            self.copeland_table.setRowCount(0)
            self.simpson_table.setRowCount(0)
        
        # Модель Борда
        if self.ranked_votes:
            borda_model = BordaModel(self.candidates, self.ranked_votes)
            borda_winner, borda_scores, borda_explanation = borda_model.calculate_winner()
            self.borda_result.setText(borda_explanation)
            self.update_table(self.borda_table, borda_scores)
        else:
            self.borda_result.setText("Нет ранжированных голосов для анализа")
            self.borda_table.setRowCount(0)
    
    def update_table(self, table: QTableWidget, data: Dict[str, any]):
        """Обновляет таблицу с результатами"""
        table.setRowCount(len(data))
        for i, (candidate, value) in enumerate(data.items()):
            table.setItem(i, 0, QTableWidgetItem(candidate))
            table.setItem(i, 1, QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()