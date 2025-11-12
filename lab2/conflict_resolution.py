from typing import List, Dict
from knowledge_base import Rule

class ConflictResolution:
    """Класс для реализации различных стратегий разрешения конфликтов"""
    
    @staticmethod
    def first_strategy(candidates: List[Rule]) -> List[Rule]:
        """
        Стратегия "первый в списке" - возвращает правило с наименьшим ID
        """
        if not candidates:
            return []
        min_id = min(rule.id for rule in candidates)
        return [rule for rule in candidates if rule.id == min_id]
    
    @staticmethod
    def recency_strategy(candidates: List[Rule], working_memory) -> List[Rule]:
        """
        Стратегия "новизна" - приоритет у правил, которые зависят от недавно добавленных фактов
        """
        # В упрощенном варианте - возвращаем все кандидаты
        # В реальной системе здесь была бы логика анализа истории изменений
        return candidates
    
    @staticmethod
    def specificity_strategy(candidates: List[Rule]) -> List[Rule]:
        """
        Стратегия "специфичность" - приоритет у правил с более сложными условиями
        """
        if not candidates:
            return []
        
        # Сортируем по количеству условий (от большего к меньшему)
        sorted_candidates = sorted(candidates, key=lambda r: len(r.condition), reverse=True)
        max_conditions = len(sorted_candidates[0].condition)
        
        # Возвращаем правила с максимальным количеством условий
        return [rule for rule in sorted_candidates if len(rule.condition) == max_conditions]
    
    @staticmethod
    def user_defined_priority(candidates: List[Rule], priorities: Dict[int, int] = None) -> List[Rule]:
        """
        Стратегия "приоритет пользователя" - пользователь сам задает приоритеты
        """
        if not candidates:
            return []
        
        if priorities is None:
            priorities = {}
        
        # Сортируем по приоритету (если не задан, приоритет 0)
        sorted_candidates = sorted(candidates, key=lambda r: priorities.get(r.id, 0), reverse=True)
        max_priority = priorities.get(sorted_candidates[0].id, 0)
        
        return [rule for rule in sorted_candidates if priorities.get(rule.id, 0) == max_priority]