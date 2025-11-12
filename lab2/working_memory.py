from typing import Dict, Any, List

class WorkingMemory:
    """Класс для представления рабочей памяти экспертной системы"""
    
    def __init__(self, initial_facts: Dict[str, Any] = None):
        """
        Инициализирует рабочую память с начальными фактами
        :param initial_facts: словарь начальных фактов
        """
        self.facts = initial_facts or {}
        self.derivation_trace = []  # История вывода для объяснений
    
    def add_fact(self, variable: str, value: Any):
        """Добавляет факт в рабочую память"""
        self.facts[variable] = value
        # Логируем добавление факта
        self.derivation_trace.append({
            'action': 'add_fact',
            'variable': variable,
            'value': value,
            'from_rule': None
        })
    
    def update_fact(self, variable: str, value: Any, rule_id: int = None):
        """Обновляет значение факта и записывает происхождение"""
        self.facts[variable] = value
        # Логируем обновление факта
        self.derivation_trace.append({
            'action': 'update_fact',
            'variable': variable,
            'value': value,
            'from_rule': rule_id
        })
    
    def get_fact(self, variable: str) -> Any:
        """Возвращает значение факта по имени переменной"""
        return self.facts.get(variable)
    
    def has_fact(self, variable: str, value: Any) -> bool:
        """Проверяет наличие факта с определенным значением"""
        return self.facts.get(variable) == value
    
    def get_all_facts(self) -> Dict[str, Any]:
        """Возвращает все факты в рабочей памяти"""
        return self.facts.copy()
    
    def get_derivation_trace(self) -> List[Dict]:
        """Возвращает историю вывода"""
        return self.derivation_trace