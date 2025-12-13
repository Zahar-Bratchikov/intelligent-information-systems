"""
Модели Кондорсе: явный победитель, правило Копленда, правило Симпсона
"""
from typing import List, Dict, Tuple, Optional
import itertools

class CondorcetModel:
    """Модели Кондорсе"""
    
    def __init__(self, candidates: List[str], ranked_votes: List[List[str]]):
        """
        Инициализация модели
        
        Args:
            candidates: Список кандидатов
            ranked_votes: Список ранжированных голосов (полные ранжировки)
        """
        self.candidates = candidates
        self.ranked_votes = ranked_votes
    
    def _create_pairwise_matrix(self) -> Dict[Tuple[str, str], int]:
        """Создает матрицу попарных сравнений"""
        pairwise = {}
        for candidate1, candidate2 in itertools.permutations(self.candidates, 2):
            pairwise[(candidate1, candidate2)] = 0
        
        # Подсчет побед в парных сравнениях
        for vote in self.ranked_votes:
            for i, candidate1 in enumerate(vote):
                for candidate2 in vote[i+1:]:
                    if (candidate1, candidate2) in pairwise:
                        pairwise[(candidate1, candidate2)] += 1
        
        return pairwise
    
    def find_condorcet_winner(self) -> Tuple[Optional[str], str]:
        """Находит явного победителя Кондорсе"""
        if not self.ranked_votes:
            return None, "Нет голосов для анализа"
        
        pairwise = self._create_pairwise_matrix()
        total_voters = len(self.ranked_votes)
        
        for candidate in self.candidates:
            is_winner = True
            wins_count = 0
            
            for opponent in self.candidates:
                if candidate == opponent:
                    continue
                
                wins = pairwise.get((candidate, opponent), 0)
                losses = pairwise.get((opponent, candidate), 0)
                
                if wins <= losses:
                    is_winner = False
                    break
                wins_count += 1
            
            if is_winner:
                explanation = f"Найден явный победитель Кондорсе: '{candidate}'. "
                explanation += f"Он побеждает всех остальных кандидатов в парных сравнениях."
                return candidate, explanation
        
        return None, "Явный победитель Кондорсе не найден"
    
    def copeland_rule(self) -> Tuple[str, Dict[str, float], str]:
        """Правило Копленда"""
        if not self.ranked_votes:
            return "", {}, "Нет голосов для анализа"
        
        pairwise = self._create_pairwise_matrix()
        total_voters = len(self.ranked_votes)
        scores = {candidate: 0.0 for candidate in self.candidates}
        
        # Расчет баллов по правилу Копленда
        for candidate in self.candidates:
            for opponent in self.candidates:
                if candidate == opponent:
                    continue
                
                wins = pairwise.get((candidate, opponent), 0)
                losses = pairwise.get((opponent, candidate), 0)
                
                if wins > losses:
                    scores[candidate] += 1
                elif wins == losses:
                    scores[candidate] += 0.5
        
        # Нахождение победителя
        winner = max(scores, key=scores.get)
        max_score = scores[winner]
        
        explanation = f"Победитель по правилу Копленда: '{winner}' с {max_score} баллами. "
        explanation += "Баллы рассчитываются как количество побед (+1) и ничьих (+0.5) в парных сравнениях."
        
        return winner, scores, explanation
    
    def simpson_rule(self) -> Tuple[str, Dict[str, int], str]:
        """Правило Симпсона (максимин)"""
        if not self.ranked_votes:
            return "", {}, "Нет голосов для анализа"
        
        pairwise = self._create_pairwise_matrix()
        min_wins = {candidate: float('inf') for candidate in self.candidates}
        
        # Находим минимальное количество побед для каждого кандидата
        for candidate in self.candidates:
            for opponent in self.candidates:
                if candidate == opponent:
                    continue
                
                wins = pairwise.get((candidate, opponent), 0)
                min_wins[candidate] = min(min_wins[candidate], wins)
        
        # Нахождение победителя (максимум из минимумов)
        winner = max(min_wins, key=min_wins.get)
        max_min_wins = min_wins[winner]
        
        explanation = f"Победитель по правилу Симпсона: '{winner}'. "
        explanation += f"У этого кандидата максимальное значение минимального числа побед в парных сравнениях ({max_min_wins})."
        
        return winner, min_wins, explanation