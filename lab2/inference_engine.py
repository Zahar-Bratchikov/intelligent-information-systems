from typing import Dict, Any, List
from knowledge_base import KnowledgeBase, Rule
from working_memory import WorkingMemory
from conflict_resolution import ConflictResolution

class InferenceEngine:
    """Механизм логического вывода экспертной системы"""
    
    def __init__(self, knowledge_base: KnowledgeBase, working_memory: WorkingMemory):
        self.knowledge_base = knowledge_base
        self.working_memory = working_memory
        self.conflict_resolver = ConflictResolution()
        self.strategy = "first"  # по умолчанию
        self.priorities = {}  # для пользовательской стратегии
    
    def set_conflict_resolution_strategy(self, strategy: str, priorities: Dict[int, int] = None):
        """Устанавливает стратегию разрешения конфликтов"""
        self.strategy = strategy
        if priorities:
            self.priorities = priorities
    
    def evaluate_condition(self, condition: Dict[str, Any]) -> bool:
        """Оценивает одно условие"""
        variable = condition['variable']
        operator = condition['operator']
        value = condition['value']
        
        fact_value = self.working_memory.get_fact(variable)
        
        if fact_value is None:
            return False
        
        # Проверяем оператор
        if operator == "==":
            return fact_value == value
        elif operator == "!=":
            return fact_value != value
        elif operator in ["<", "<=", ">", ">="]:
            # Для числовых операций пробуем преобразовать в числа
            try:
                fact_num = float(fact_value)
                value_num = float(value)
                if operator == "<":
                    return fact_num < value_num
                elif operator == "<=":
                    return fact_num <= value_num
                elif operator == ">":
                    return fact_num > value_num
                elif operator == ">=":
                    return fact_num >= value_num
            except (ValueError, TypeError):
                # Если не получилось преобразовать в число, возвращаем False
                return False
        elif operator == "in":
            # Для оператора "in" значение должно быть списком
            return fact_value in value
        else:
            raise ValueError(f"Неизвестный оператор: {operator}")
    
    def evaluate_rule_conditions(self, rule: Rule) -> bool:
        """Оценивает все условия правила"""
        for condition in rule.condition:
            if not self.evaluate_condition(condition):
                return False
        return True
    
    def find_applicable_rules(self) -> List[Rule]:
        """Находит все применимые правила"""
        applicable_rules = []
        all_rules = self.knowledge_base.get_rules()
        
        for rule in all_rules:
            if self.evaluate_rule_conditions(rule):
                applicable_rules.append(rule)
        
        return applicable_rules
    
    def resolve_conflicts(self, candidates: List[Rule]) -> List[Rule]:
        """Разрешает конфликты между применимыми правилами"""
        if self.strategy == "first":
            return self.conflict_resolver.first_strategy(candidates)
        elif self.strategy == "specificity":
            return self.conflict_resolver.specificity_strategy(candidates)
        elif self.strategy == "user_defined":
            return self.conflict_resolver.user_defined_priority(candidates, self.priorities)
        else:
            # по умолчанию используем первую стратегию
            return self.conflict_resolver.first_strategy(candidates)
    
    # В inference_engine.py (из файла Pasted_Text_1762327865517.txt)
def apply_rule(self, rule: Rule) -> bool:
    conclusion = rule.conclusion
    variable = conclusion['variable']
    value = conclusion['value']

    current_value = self.working_memory.get_fact(variable)

    if current_value != value:
        self.working_memory.update_fact(variable, value, rule.id)
        return True # Изменило состояние
    else:
        # Значение не изменится. Обновляем факт для объяснений,
        # но возвращаем False, чтобы не зациклить основной цикл.
        self.working_memory.update_fact(variable, value, rule.id)
        return False # Не изменило состояние с точки зрения цикла вывода
    
    def forward_chain(self, max_iterations: int = 100) -> bool:
        """
        Выполняет прямую цепочку вывода
        :param max_iterations: максимальное количество итераций для предотвращения зацикливания
        :return: True если был сделан вывод, False иначе
        """
        iterations = 0
        new_fact_added = True
        
        while new_fact_added and iterations < max_iterations:
            new_fact_added = False
            
            # Находим применимые правила
            applicable_rules = self.find_applicable_rules()
            
            if not applicable_rules:
                print(f"На итерации {iterations + 1}: нет применимых правил. Выход из цикла.")
                break
            
            # Разрешаем конфликты
            selected_rules = self.resolve_conflicts(applicable_rules)
            
            if selected_rules:
                # Применяем первое выбранное правило
                rule_to_apply = selected_rules[0]
                # ИСПРАВЛЕНО: проверяем, изменило ли применение состояние
                rule_changed_state = self.apply_rule(rule_to_apply)
                if rule_changed_state:
                    new_fact_added = True
                    print(f"На итерации {iterations + 1}: применено правило {rule_to_apply.id}, состояние изменилось.")
                else:
                    print(f"На итерации {iterations + 1}: применено правило {rule_to_apply.id}, но состояние не изменилось.")
            else:
                print(f"На итерации {iterations + 1}: выбраны правила, но ни одно не изменило состояние.")
            
            iterations += 1
        
        print(f"Цикл вывода завершён за {iterations} итераций.")
        return iterations > 0
