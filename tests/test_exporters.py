# tests/test_exporters.py
from text_to_condition.core import (
    AndCondition,
    ColumnCondition,
    ColumnInCondition,
    OrCondition,
)
from text_to_condition.exporters import (
    DataFrameQueryExporter,
    HumanReadableExporter,
)


def test_dataframe_query_exporter():
    exporter = DataFrameQueryExporter()

    # Test simple column condition
    condition = ColumnCondition(
        column_name="amount", column_type="float", operator=">=", value="100"
    )
    assert exporter.export(condition) == "amount >= 100"

    # Test IN condition
    in_condition = ColumnInCondition(
        column_name="category", column_type="str", values=["food", "transport"]
    )
    assert exporter.export(in_condition) == "category.isin([food, transport])"

    # Test AND condition
    and_condition = AndCondition(
        conditions=[
            ColumnCondition(
                column_name="amount", column_type="float", operator=">=", value="100"
            ),
            ColumnCondition(
                column_name="category", column_type="str", operator="==", value="food"
            ),
        ]
    )
    assert exporter.export(and_condition) == "(amount >= 100) & (category == food)"

    # Test OR condition
    or_condition = OrCondition(
        conditions=[
            ColumnCondition(
                column_name="amount", column_type="float", operator="<", value="50"
            ),
            ColumnCondition(
                column_name="category",
                column_type="str",
                operator="==",
                value="transport",
            ),
        ]
    )
    assert exporter.export(or_condition) == "(amount < 50) | (category == transport)"


def test_human_readable_exporter():
    exporter = HumanReadableExporter()

    # Test simple column condition
    condition = ColumnCondition(
        column_name="amount", column_type="float", operator=">=", value="100"
    )
    assert exporter.export(condition) == "amount greater than or equal to 100"

    # Test IN condition
    in_condition = ColumnInCondition(
        column_name="category", column_type="str", values=["food", "transport"]
    )
    assert exporter.export(in_condition) == "category is one of: food, transport"

    # Test AND condition
    and_condition = AndCondition(
        conditions=[
            ColumnCondition(
                column_name="amount", column_type="float", operator=">=", value="100"
            ),
            ColumnCondition(
                column_name="category", column_type="str", operator="==", value="food"
            ),
        ]
    )
    assert (
        exporter.export(and_condition)
        == "amount greater than or equal to 100 AND category is food"
    )

    # Test OR condition
    or_condition = OrCondition(
        conditions=[
            ColumnCondition(
                column_name="amount", column_type="float", operator="<", value="50"
            ),
            ColumnCondition(
                column_name="category",
                column_type="str",
                operator="==",
                value="transport",
            ),
        ]
    )
    assert (
        exporter.export(or_condition) == "amount less than 50 OR category is transport"
    )
    assert exporter.export(in_condition) == "category.isin([food, transport])"

    # Test AND condition
    and_condition = AndCondition(
        conditions=[
            ColumnCondition(
                column_name="amount", column_type="float", operator=">=", value="100"
            ),
            ColumnCondition(
                column_name="category", column_type="str", operator="==", value="food"
            ),
        ]
    )
    assert exporter.export(and_condition) == "(amount >= 100) & (category == food)"


def test_human_readable_exporter_2():
    exporter = HumanReadableExporter()

    # Test simple column condition
    condition = ColumnCondition(
        column_name="amount", column_type="float", operator=">=", value="100"
    )
    assert exporter.export(condition) == "amount greater than or equal to 100"

    # Test IN condition
    in_condition = ColumnInCondition(
        column_name="category", column_type="str", values=["food", "transport"]
    )
    assert exporter.export(in_condition) == "category is one of: food, transport"

    # Test AND condition
    and_condition = AndCondition(
        conditions=[
            ColumnCondition(
                column_name="amount", column_type="float", operator=">=", value="100"
            ),
            ColumnCondition(
                column_name="category", column_type="str", operator="==", value="food"
            ),
        ]
    )
    assert (
        exporter.export(and_condition)
        == "amount greater than or equal to 100 AND category is food"
    )
