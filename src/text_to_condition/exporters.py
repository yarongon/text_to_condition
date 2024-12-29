from abc import ABC, abstractmethod
from typing import Union
from src.text_to_condition.core import Condition, ColumnCondition, ColumnInCondition, ColumnNotInCondition, AndCondition, OrCondition

class ConditionExporter(ABC):
    @abstractmethod
    def export(self, condition: Condition) -> str:
        pass

class DataFrameQueryExporter(ConditionExporter):
    def export(self, condition: Condition) -> str:
        if isinstance(condition, ColumnCondition):
            return f"{condition.column_name} {condition.operator} {condition.value}"
        elif isinstance(condition, ColumnInCondition):
            values = ", ".join([str(v) for v in condition.values])
            return f"{condition.column_name}.isin([{values}])"
        elif isinstance(condition, ColumnNotInCondition):
            values = ", ".join([str(v) for v in condition.values])
            return f"~{condition.column_name}.isin([{values}])"
        elif isinstance(condition, AndCondition):
            subconditions = [self.export(c) for c in condition.conditions]
            return " & ".join(f"({c})" for c in subconditions)
        elif isinstance(condition, OrCondition):
            subconditions = [self.export(c) for c in condition.conditions]
            return " | ".join(f"({c})" for c in subconditions)
        raise ValueError(f"Unknown condition type: {type(condition)}")

class HumanReadableExporter(ConditionExporter):
    OPERATOR_WORDS = {
        '>': 'greater than',
        '<': 'less than',
        '>=': 'greater than or equal to',
        '<=': 'less than or equal to',
        '=': 'is',
        '==': 'is',
        '!=': 'does not equal',
        'like': 'contains',
        'ilike': 'contains (case insensitive)'
    }

    def export(self, condition: Condition) -> str:
        if isinstance(condition, ColumnCondition):
            operator_word = self.OPERATOR_WORDS.get(condition.operator, condition.operator)
            return f"{condition.column_name} {operator_word} {condition.value}"
        elif isinstance(condition, ColumnInCondition):
            values = ", ".join([str(v) for v in condition.values])
            return f"{condition.column_name} is one of: {values}"
        elif isinstance(condition, ColumnNotInCondition):
            values = ", ".join([str(v) for v in condition.values])
            return f"{condition.column_name} is not one of: {values}"
        elif isinstance(condition, AndCondition):
            subconditions = [self.export(c) for c in condition.conditions]
            return " AND ".join(subconditions)
        elif isinstance(condition, OrCondition):
            subconditions = [self.export(c) for c in condition.conditions]
            return " OR ".join(subconditions)
        raise ValueError(f"Unknown condition type: {type(condition)}")