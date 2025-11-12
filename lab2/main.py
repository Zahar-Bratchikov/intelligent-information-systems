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

def main():
    print("=== Экспертная система для выбора места отдыха ===\n")
    
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
    # Попробуем стратегию "first" для корректной работы числовых правил
    engine.set_conflict_resolution_strategy("first")
    
    # Выполняем логический вывод
    print("Выполняем логический вывод...")
    engine.forward_chain()
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
    
    # Пример объяснения правила
    print("\nОбъяснение одного из правил (например, правило #6):")
    rule_explanation = explainer.get_rule_explanation(6)
    print(rule_explanation)

if __name__ == "__main__":
    main()