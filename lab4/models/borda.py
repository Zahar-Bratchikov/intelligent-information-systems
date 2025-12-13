"""
Модель Борда
"""
from typing import List, Dict, Tuple

class BordaModel:
    """Модель Борда"""
    
    def __init__(self, candidates: List[str], ranked_votes: List[List[str]]):
        """
        Инициализация модели
        
        Args:
            candidates: Список кандидатов
            ranked_votes: Список ранжированных голосов
        """
        self.candidates = candidates
        self.ranked_votes = ranked_votes
    
    def calculate_winner(self) -> Tuple[str, Dict[str, int], str]:
        """
        Расчет победителя по модели Борда
        
        Returns:
            Кортеж: (победитель, баллы, объяснение)
        """
        if not self.ranked_votes:
            return "", {}, "Нет голосов для анализа"
        
        # Инициализация баллов
        scores = {candidate: 0 for candidate in self.candidates}
        num_candidates = len(self.candidates)
        
        # Расчет баллов по системе Борда
        for vote in self.ranked_votes:
            # Создаем полную ранжировку (если голос неполный)
            complete_vote = vote.copy()
            for candidate in self.candidates:
                if candidate not in complete_vote:
                    complete_vote.append(candidate)
            
            # Начисляем баллы: первый = n-1, второй = n-2, ..., последний = 0
            for i, candidate in enumerate(complete_vote):
                if i < num_candidates:
                    scores[candidate] += (num_candidates - 1 - i)
        
        # Нахождение победителя
        winner = max(scores, key=scores.get)
        max_score = scores[winner]
        
        explanation = f"Победитель по модели Борда: '{winner}' с {max_score} баллами. "
        explanation += "Баллы начисляются по системе: 1-е место = {num_candidates-1}, 2-е место = {num_candidates-2}, и т.д."
        
        return winner, scores, explanation