from working_memory import WorkingMemory
from knowledge_base import KnowledgeBase

class ExplanationComponent:
    """Компонента объяснений экспертной системы"""
    
    def __init__(self, knowledge_base: KnowledgeBase, working_memory: WorkingMemory):
        self.knowledge_base = knowledge_base
        self.working_memory = working_memory
    
    def explain_fact(self, variable: str) -> str:
        """Объясняет, как был получен определенный факт"""
        derivation_trace = self.working_memory.get_derivation_trace()
        
        # Ищем в истории, как был добавлен или изменен этот факт
        for entry in reversed(derivation_trace):  # идем с конца
            if entry['variable'] == variable:
                if entry['from_rule'] is not None:
                    return f"Факт '{variable} = {entry['value']}' был выведен с помощью правила #{entry['from_rule']}."
                else:
                    return f"Факт '{variable} = {entry['value']}' был задан изначально."
        
        return f"Факт '{variable}' не найден в рабочей памяти."
    
    def explain_result(self, result_variable: str = "Результат") -> str:
        """Объясняет полученный результат"""
        result_value = self.working_memory.get_fact(result_variable)
        
        if result_value is None:
            return f"Результат ({result_variable}) не был вычислен."
        
        explanation = f"Результат: {result_value}\n"
        explanation += f"Как мы пришли к этому результату:\n"
        
        derivation_trace = self.working_memory.get_derivation_trace()
        
        # Показываем шаги, которые привели к результату
        for entry in derivation_trace:
            if entry['variable'] == result_variable:
                if entry['from_rule'] is not None:
                    explanation += f"  - Факт '{entry['variable']} = {entry['value']}' был выведен с помощью правила #{entry['from_rule']}\n"
        
        # Показываем все факты, участвовавшие в выводе
        explanation += "\nФакты, участвовавшие в выводе:\n"
        for entry in derivation_trace:
            if entry['from_rule'] is not None:  # только выведенные факты
                explanation += f"  - '{entry['variable']} = {entry['value']}' (правило #{entry['from_rule']})\n"
        
        return explanation
    
    def get_rule_explanation(self, rule_id: int) -> str:
        """Объясняет, что делает определенное правило"""
        rules = self.knowledge_base.get_rules()
        rule = next((r for r in rules if r.id == rule_id), None)
        
        if not rule:
            return f"Правило #{rule_id} не найдено."
        
        explanation = f"Правило #{rule.id}:\n"
        explanation += "ЕСЛИ "
        
        conditions = []
        for cond in rule.condition:
            conditions.append(f"('{cond['variable']}' {cond['operator']} '{cond['value']}')")
        
        explanation += " И ".join(conditions)
        explanation += f" ТОГДА '{rule.conclusion['variable']}' = '{rule.conclusion['value']}'"
        
        return explanation