from knowledge_base import KnowledgeBase
from working_memory import WorkingMemory
from inference_engine import InferenceEngine
from explanation_component import ExplanationComponent

def get_user_input(variable: str, options: list = None) -> str:
    """Функция для получения ввода от пользователя"""
    if options:
        print(f"Пожалуйста, выберите значение для '{variable}':")
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        while True:
            try:
                choice = int(input(f"Введите номер (1-{len(options)}): "))
                if 1 <= choice <= len(options):
                    return options[choice - 1]
                else:
                    print("Неверный номер. Попробуйте снова.")
            except ValueError:
                print("Пожалуйста, введите число.")
    else:
        return input(f"Введите значение для '{variable}': ")

def debug_forward_chain(engine: InferenceEngine):
    """
    Отладочная версия forward_chain, которая показывает, что происходит
    """
    max_iterations = 100
    iterations = 0
    new_fact_added = True
    
    print("=== НАЧАЛО ОТЛАДКИ ВЫВОДА ===")
    
    while new_fact_added and iterations < max_iterations:
        new_fact_added = False
        
        print(f"\n--- ИТЕРАЦИЯ {iterations + 1} ---")
        current_facts = engine.working_memory.get_all_facts()
        print(f"Текущие факты: {current_facts}")
        
        # Находим применимые правила
        applicable_rules = engine.find_applicable_rules()
        
        print(f"Найдено применимых правил: {len(applicable_rules)}")
        for rule in applicable_rules:
            print(f"  - Правило {rule.id}: {rule}")
        
        if not applicable_rules:
            print("Нет применимых правил. Завершаем.")
            break
        
        # Разрешаем конфликты
        selected_rules = engine.resolve_conflicts(applicable_rules)
        
        print(f"Выбрано правил для применения: {len(selected_rules)}")
        for rule in selected_rules:
            print(f"  - Правило {rule.id}")
        
        if selected_rules:
            # Применяем первое выбранное правило
            rule_to_apply = selected_rules[0]
            print(f"Применяем правило {rule_to_apply.id}")
            
            # Прежде чем применить, проверим, какие условия срабатывают
            for i, condition in enumerate(rule_to_apply.condition):
                eval_result = engine.evaluate_condition(condition)
                print(f"    Условие {i+1}: '{condition['variable']}' {condition['operator']} '{condition['value']}' -> {eval_result}")
            
            old_facts = engine.working_memory.get_all_facts()
            engine.apply_rule(rule_to_apply)
            new_facts = engine.working_memory.get_all_facts()
            
            print(f"    До применения: {old_facts}")
            print(f"    После применения: {new_facts}")
            
            # Найдем, что изменилось
            for var, new_val in new_facts.items():
                old_val = old_facts.get(var)
                if old_val != new_val:
                    print(f"    Изменено: {var} = {old_val} -> {new_val}")
            
            new_fact_added = True
        
        iterations += 1
    
    print(f"\n=== КОНЕЦ ОТЛАДКИ ВЫВОДА (итераций: {iterations}) ===")
    return iterations > 0

def main():
    print("=== Экспертная система для выбора места отдыха (ОТЛАДКА) ===\n")
    
    # Загружаем базу знаний
    kb = KnowledgeBase("knowledge_base.yaml")
    print(f"Загружено {len(kb.get_rules())} правил.\n")
    
    # Запрашиваем у пользователя начальные данные
    print("Ответьте на следующие вопросы:")
    
    initial_facts = {}
    
    # Бюджет - числовое значение
    budget_input = input("Введите ваш бюджет (в рублях): ")
    try:
        initial_facts["Бюджет"] = int(budget_input)
    except ValueError:
        print("Неверный формат бюджета. Установлено значение 75000.")
        initial_facts["Бюджет"] = 75000
    
    # Остальные вопросы
    initial_facts["Ограничения по здоровью"] = get_user_input("Ограничения по здоровью", ["да", "нет"])
    initial_facts["Хочу море"] = get_user_input("Хочу море", ["да", "нет"])
    initial_facts["Сезон"] = get_user_input("Сезон", ["лето", "зима"])
    initial_facts["Короткий отпуск"] = get_user_input("Короткий отпуск", ["да", "нет"])
    initial_facts["Хочу экскурсии"] = get_user_input("Хочу экскурсии", ["да", "нет"])
    initial_facts["Есть транспорт"] = get_user_input("Есть транспорт", ["да", "нет"])
    initial_facts["Хочу горы"] = get_user_input("Хочу горы", ["да", "нет"])
    
    print(f"\nВаши ответы:")
    for var, val in initial_facts.items():
        print(f"  {var}: {val}")
    print()
    
    # Создаем рабочую память с начальными фактами
    wm = WorkingMemory(initial_facts)
    
    # Создаем механизм вывода
    engine = InferenceEngine(kb, wm)
    
    # Устанавливаем стратегию разрешения конфликтов
    engine.set_conflict_resolution_strategy("first")
    
    # Выполняем логический вывод с отладкой
    print("Выполняем логический вывод...")
    debug_forward_chain(engine)
    print("Логический вывод завершен.\n")
    
    # Показываем все полученные факты
    print("Факты в рабочей памяти после вывода:")
    all_facts = wm.get_all_facts()
    for var, val in all_facts.items():
        print(f"  {var}: {val}")
    print()
    
    # Создаем компоненту объяснений
    explainer = ExplanationComponent(kb, wm)
    
    # Объясняем результат
    print("Объяснение результата:")
    explanation = explainer.explain_result()
    print(explanation)
    
    # Пример объяснения конкретного факта
    print("\nОбъяснение факта 'Результат':")
    fact_explanation = explainer.explain_fact("Результат")
    print(fact_explanation)

if __name__ == "__main__":
    main()