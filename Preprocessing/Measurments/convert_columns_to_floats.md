## Python Code Description

This Python script consists of multiple utility functions intended for data manipulation and processing, particularly with numerical data within strings and pandas DataFrames.

### Imports
- `re`: Regex module for parsing strings.
- `ast`: Abstract Syntax Trees module for safely evaluating strings containing Python literal structures.
- `pandas`: Data manipulation and analysis library.

### Functions

#### `str_to_floatlist(s)`
Converts a string representation of a list into a list of floats.

#### `parse_complex_string(s)`
Extracts all numbers (including decimals and negatives) from a string and converts them to floats.

#### `convert_columns_to_floats(columns)`
Converts a list of string representations of numbers to a list of lists of floats.

#### `convert_columns_to_floats2(df)`
Converts all columns in a DataFrame to floats. Each element is parsed to extract numerical values.

#### `get_length_of_list(df, column_name)`
Returns a pandas Series containing the lengths of lists in a specified column of a DataFrame.

#### `reduce_cells(df, column, n=96)`
Reduces the data in each cell of a specified column by removing the last `n` elements.

#### `reduce_cells_for_all_columns(df, n=96)`
Applies `reduce_cells` operation to all columns in the DataFrame.

#### `save_df_as_csv(df, filename)`
Saves the DataFrame `df` to a CSV file with the specified `filename`.

### Usage
These functions are suitable for preprocessing tasks where data needs to be extracted from strings, converted, and manipulated efficiently within pandas DataFrames.