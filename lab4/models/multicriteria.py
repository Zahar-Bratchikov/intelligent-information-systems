"""
Многокритериальные модели выбора (опционально)
"""
from typing import List, Dict, Tuple
import numpy as np

class MulticriteriaModel:
    """Многокритериальные модели выбора"""
    
    def __init__(self, candidates: List[str], criteria: List[str], weights: List[float]):
        """
        Инициализация модели
        
        Args:
            candidates: Список кандидатов
            criteria: Список критериев
            weights: Веса критериев
        """
        self.candidates = candidates
        self.criteria = criteria
        self.weights = weights
        self.evaluations = {}  # Оценки по критериям
    
    def set_evaluations(self, evaluations: Dict[str, List[float]]):
        """Установка оценок кандидатов по критериям"""
        self.evaluations = evaluations
    
    def linear_weighted_sum(self) -> Tuple[str, Dict[str, float], str]:
        """Линейная многокритериальная модель (метод взвешенной суммы)"""
        if not self.evaluations:
            return "", {}, "Оценки не установлены"
        
        scores = {}
        for candidate in self.candidates:
            if candidate in self.evaluations:
                # Нормализуем оценки (предполагаем шкалу 1-10)
                normalized_scores = [score / 10.0 for score in self.evaluations[candidate]]
                weighted_sum = sum(w * s for w, s in zip(self.weights, normalized_scores))
                scores[candidate] = weighted_sum
        
        if not scores:
            return "", {}, "Нет данных для расчета"
        
        winner = max(scores, key=scores.get)
        max_score = scores[winner]
        
        explanation = f"Победитель по линейной многокритериальной модели: '{winner}'. "
        explanation += f"Обобщенный показатель: {max_score:.3f} (максимальный среди всех кандидатов)."
        
        return winner, scores, explanation