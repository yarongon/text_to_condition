"""
A Python module that contains classes that represent conditions for a dataframe,
and a function that uses LLM to construct a condition expression out of free text.
All the classes are subclasses of Pydantic's BaseModel.
There are two types of conditions:
1. Column conditions: These conditions are applied to a single column.
2. Column 'in' conditions: These conditions are applied to a single column and check if the column's value is in a list of values.
3. and/or conditions: consitions that are applied to two or more conditions.
"""

import json
import os
from typing import Literal

import pandas as pd
from openai import OpenAI
from pydantic import BaseModel, Field

openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


class ColumnCondition(BaseModel):
    """
    A class that represents a condition that is applied to a single column.
    """

    tag: Literal["ColumnCondition"] = "ColumnCondition"
    column_name: str = Field(
        ..., title="The name of the column to apply the condition to."
    )
    column_type: Literal["int", "float", "str", "date"] = Field(
        ..., title="The data type of the column"
    )
    operator: Literal["==", "!=", "<", ">", "<=", ">="] = Field(
        ..., title="The operator of the condition."
    )
    value: str | None = Field(None, title="The value to compare the column to.")


class ColumnInCondition(BaseModel):
    """
    A class that represents a condition that is applied to a single column and checks if the column's value is in a list of values.
    """

    tag: Literal["ColumnInCondition"] = "ColumnInCondition"
    column_name: str = Field(
        ..., title="The name of the column to apply the condition to."
    )
    column_type: Literal["int", "float", "str", "date"] = Field(
        ..., title="The data type of the column"
    )
    values: list[str] = Field(..., title="The list of values to compare the column to.")


class ColumnNotInCondition(BaseModel):
    """
    A class that represents a condition that is applied to a single column and checks if the column's value is not in a list of values.
    """

    tag: Literal["ColumnInCondition"] = "ColumnInCondition"
    column_name: str = Field(
        ..., title="The name of the column to apply the condition to."
    )
    column_type: Literal["int", "float", "str", "date"] = Field(
        ..., title="The data type of the column"
    )
    values: list[str] = Field(..., title="The list of values to compare the column to.")


class AndCondition(BaseModel):
    """
    A class that represents an 'and' condition that is applied to two or more conditions.
    """

    tag: Literal["AndCondition"] = "AndCondition"
    conditions: list["Condition"]


class OrCondition(BaseModel):
    """
    A class that represents an 'or' condition that is applied to two or more conditions.
    """

    tag: Literal["OrCondition"] = "OrCondition"
    conditions: list["Condition"]


Condition = ColumnCondition | ColumnInCondition | AndCondition | OrCondition


class ConditionModel(BaseModel):
    condition: Condition = Field(discriminator="tag")


def text_to_condition(free_text: str, columns_info: dict[str, str]) -> Condition:
    """
    Convert a free text condition into a Condition object.

    Args:
    free_text (str): A free text describing a condition.
    columns_info (dict[str, str]): A dictionary where keys are column names and values are their data types.

    Returns:
    Condition: A Condition object that represents the condition.

    Can raise the following exceptions:
    - JSONDecodeError: If the JSON string is invalid.
    - ValidationError: If the JSON does not match the schema.
    """
    columns_description = ", ".join(
        [f"{col_name} ({col_type})" for col_name, col_type in columns_info.items()]
    )

    prompt = f"""
    Given a DataFrame with the following columns: {columns_description}
    
    Convert the following free text conditions into a JSON format:
    {free_text}
 
    Instructions:
    - Column names should be the exact column names from the DataFrame.
    - Ensure that the operators are appropriate for the given column types.
    - When dealing with dates, provide absolute dates in the format "YYYY-MM-DD".
    - The current date is {pd.Timestamp.now().strftime("%Y-%m-%d")}.
    - Provide the JSON only. Do not include any code block delimiters, text, explanation or comments.
    """

    json_schema = ConditionModel.model_json_schema()
    openai_response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"Generate JSON that conforms to this schema: {json_schema}",
            },
            {"role": "user", "content": prompt},
        ],
    )

    json_str = openai_response.choices[0].message.content
    json_obj = json.loads(json_str)
    return ConditionModel.model_validate(json_obj).condition


def get_column_metadata(df: pd.DataFrame) -> dict:
    return {col: str(dtype) for col, dtype in df.dtypes.items()}
