from text_to_condition.core import text_to_condition
from text_to_condition.core import (
    ColumnCondition, 
    ColumnInCondition,
    AndCondition,
    OrCondition,
    ConditionModel
)

def test_column_condition_validation():
    condition = ColumnCondition(
        column_name="amount",
        column_type="float",
        operator=">=",
        value="100"
    )
    assert condition.column_name == "amount"
    assert condition.column_type == "float"
    assert condition.operator == ">="
    assert condition.value == "100"

def test_column_in_condition_validation():
    condition = ColumnInCondition(
        column_name="category",
        column_type="str",
        values=["food", "transport"]
    )
    assert condition.column_name == "category"
    assert condition.values == ["food", "transport"]

def test_and_condition_validation():
    condition = AndCondition(
        conditions=[
            ColumnCondition(
                column_name="amount",
                column_type="float",
                operator=">=",
                value="100"
            ),
            ColumnCondition(
                column_name="category",
                column_type="str",
                operator="==",
                value="food"
            )
        ]
    )
    assert len(condition.conditions) == 2

def test_condition_model_validation():
    model = ConditionModel(
        condition=AndCondition(
            conditions=[
                ColumnCondition(
                    column_name="amount",
                    column_type="float",
                    operator=">=",
                    value="100"
                ),
                ColumnInCondition(
                    column_name="category",
                    column_type="str",
                    values=["food", "transport"]
                )
            ]
        )
    )
    assert isinstance(model.condition, AndCondition)

def test_text_to_condition_column_condition():
    columns_info = {"amount": "float", "category": "str"}
    free_text = "amount greater than or equal to 100"
    condition = text_to_condition(free_text, columns_info)
    
    assert isinstance(condition, ColumnCondition)
    assert condition.column_name == "amount"
    assert condition.column_type == "float"
    assert condition.operator == ">="
    assert condition.value == "100"

def test_text_to_condition_column_in_condition():
    columns_info = {"amount": "float", "category": "str"}
    free_text = "category is one of: food, transport"
    condition = text_to_condition(free_text, columns_info)
    
    assert isinstance(condition, ColumnInCondition)
    assert condition.column_name == "category"
    assert condition.column_type == "str"
    assert condition.values == ["food", "transport"]

def test_text_to_condition_and_condition():
    columns_info = {"amount": "float", "category": "str"}
    free_text = "amount greater than or equal to 100 AND category is food"
    condition = text_to_condition(free_text, columns_info)
    
    assert isinstance(condition, AndCondition)
    assert len(condition.conditions) == 2
    assert isinstance(condition.conditions[0], ColumnCondition)
    assert isinstance(condition.conditions[1], ColumnCondition)

def test_text_to_condition_or_condition():
    columns_info = {"amount": "float", "category": "str"}
    free_text = "amount less than 50 OR category is transport"
    condition = text_to_condition(free_text, columns_info)
    
    assert isinstance(condition, OrCondition)
    assert len(condition.conditions) == 2
    assert isinstance(condition.conditions[0], ColumnCondition)
    assert isinstance(condition.conditions[1], ColumnCondition)