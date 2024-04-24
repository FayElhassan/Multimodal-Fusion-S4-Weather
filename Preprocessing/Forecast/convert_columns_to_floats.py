########################## IMPORTS ##########################
# ALL
import re
import ast

# AS
import pandas as pd

########################## FUNCTIONS ##########################
# Function to convert string list to list of floats
def str_to_floatlist(s):
    try:
        return [float(i) for i in ast.literal_eval(s)]
    except ValueError as e:
        print(f"Error converting: {e}")
        return []
    
# Parse a string for numbers, including decimals and negatives
def parse_complex_string(s):
    # Find all numbers in the string, including decimals and negatives
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", s)
    # Convert found numbers to floats
    return [float(num) for num in numbers]

# Convert a list of strings to a list of floats
def convert_columns_to_floats(columns):
    return [parse_complex_string(column) for column in columns]

# Convert a dataframe to a dataframe with all columns converted to floats
def convert_columns_to_floats2(df):
    for col in df.columns:
        print(f"Processing column: {col}")
        df[col] = df[col].astype(str).apply(parse_complex_string)
        print(f"Processed column: {col}")
    return df

# Get length of list of each row in a column
def get_length_of_list(df, column_name):
    '''
    Get length of list of each row in a column
    '''
    return df[column_name].apply(lambda x: len(x))  

# Reduce each cell in each column by 96 values from the end
def reduce_cells(df, column, n=96):
    '''
    Reduce each cell in each column by 96 values from the end
    '''
    df[column] = df[column].apply(lambda x: x[:-n])
    return df[column]

# Reduce each cell in each column by 96 values from the end
def reduce_cells_for_all_columns(df, n=96):
    '''
    Reduce each cell in each column by 96 values from the end
    '''
    for cols in df.columns:
        df[cols] = df[cols].apply(lambda x: x[:-n])
    return df

# Save df as csv file
def save_df_as_csv(df, filename):
    '''
    Save df as csv file
    '''
    df.to_csv(filename, index=False)      
            