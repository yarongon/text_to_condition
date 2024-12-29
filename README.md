# text_to_condition

## Overview
`text_to_condition` is a Python package that provides functionality to convert free text into structured conditions using a Large Language Model (LLM).
This package is designed to facilitate the parsing and interpretation of free text into a format that can be easily processed by applications.

## Background
A *condition expression* is a recursive data structure.
The basic (or atomic) conditions are:
- *Column condition*: Composed of a column, an operator, and a value.
- *Column in condition*: Composed of a column and a list of values.
- *Column not in condition*: Composed of a column and a list of values.

The compound conditions are:
- *And condition*: Composed of a list of conditions.
- *Or condition*: Composed of a list of conditions.

The [Pydantic](https://docs.pydantic.dev) package is used to define the `Condition` recursive type utilizing its *discriminative union* method. See more details about discriminative unions [here](https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions).

## Installation
You can install the `text_to_condition` package using pip. Run the following command:

```sh
pip install text_to_condition
```

## Usage
Before running, define the environment variable `OPENAI_API_KEY` and assign it the appropriate value. Currently, there is no support for other LLMs. Here is a simple example of how to use the `text_to_condition` package:

```python
from text_to_condition.core import text_to_condition

# Example usage
columns_info = {"amount": "float", "category": "str"}
free_text = "amount greater than or equal to 100 AND category is food"
result = text_to_condition(free_text, columns_info)
print(result)
```

## Contributing
We welcome contributions to the `text_to_condition` project! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your branch to your forked repository.
5. Submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.