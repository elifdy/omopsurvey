import pandas as pd


def recode_missing_values(input_data):
    missing_values = [-99, -98, -97, -96, -95, -94, -93, -92, -91, -90]

    if isinstance(input_data, str):
        if input_data.endswith('.csv') or input_data.endswith('.txt'):
            return pd.read_csv(input_data, na_values=missing_values)
        elif input_data.endswith(('.xlsx', '.xls')):
            return pd.read_excel(input_data, na_values=missing_values)
        else:
            raise ValueError("Unsupported file type. Please provide a .csv, .txt, or .xlsx file.")
    elif isinstance(input_data, pd.DataFrame):
        input_data.replace(missing_values, pd.NA, inplace=True)
        return input_data
    else:
        raise ValueError("Unsupported data type. Please provide a file path or a pandas DataFrame.")
