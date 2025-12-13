"""
Модель относительного большинства
"""
from typing import List, Dict, Tuple

class MajorityModel:
    """Модель относительного большинства"""
    
    def __init__(self, candidates: List[str], votes: List[str]):
        """
        Инициализация модели
        
        Args:
            candidates: Список кандидатов (мест для отдыха)
            votes: Список голосов (выбранных мест)
        """
        self.candidates = candidates
        self.votes = votes
    
    def calculate_winner(self) -> Tuple[str, Dict[str, int], str]:
        """
        Расчет победителя по модели относительного большинства
        
        Returns:
            Кортеж: (победитель, результаты голосования, объяснение)
        """
        # Подсчет голосов
        vote_counts = {candidate: 0 for candidate in self.candidates}
        for vote in self.votes:
            if vote in vote_counts:
                vote_counts[vote] += 1
        
        # Нахождение победителя
        winner = max(vote_counts, key=vote_counts.get)
        max_votes = vote_counts[winner]
        
        # Формирование объяснения
        total_votes = len(self.votes)
        explanation = f"Победитель определен по модели относительного большинства. "
        explanation += f"Место '{winner}' получило {max_votes} голосов из {total_votes} ({max_votes/total_votes*100:.1f}%)."
        
        return winner, vote_counts, explanation