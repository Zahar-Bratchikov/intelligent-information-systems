import yaml
from typing import Dict, List, Any

class Rule:
    """Класс для представления продукционного правила"""
    def __init__(self, rule_id: int, condition: List[Dict], conclusion: Dict):
        self.id = rule_id
        self.condition = condition
        self.conclusion = conclusion

    def __repr__(self):
        return f"Rule({self.id}, condition={self.condition}, conclusion={self.conclusion})"

class KnowledgeBase:
    """Класс для работы с базой знаний"""
    def __init__(self, config_file: str):
        self.rules = []
        self.load_from_yaml(config_file)

    def load_from_yaml(self, config_file: str):
        """Загружает правила из YAML файла"""
        with open(config_file, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        
        for rule_data in data.get('rules', []):
            rule = Rule(
                rule_id=rule_data['id'],
                condition=rule_data['condition'],
                conclusion=rule_data['conclusion']
            )
            self.rules.append(rule)

    def get_rules(self) -> List[Rule]:
        """Возвращает список всех правил"""
        return self.rules