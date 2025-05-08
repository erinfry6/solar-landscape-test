import pandas as pd


# read specific cells in excel file
def read_excel_cells(file_path: str, sheet_name: str, cells: dict) -> dict:
    """
    Read specific cells from an Excel file and return them as a dictionary.
    
    :param file_path: Path to the Excel file.
    :param sheet_name: Name of the sheet to read from.
    :param cells: Dictionary with keys as cell names and values as cell coordinates (e.g., 'A1', 'B2').
    :return: Dictionary with cell names as keys and their values as values.
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    result = {}
    
    for name, cell in cells.items():
        # skip if cell is None
        if cell is None:
            continue
        row, col = int(cell[1:]) - 1, ord(cell[0].upper()) - ord('A')
        result[name] = df.iloc[row, col]
    
    return result

def trim_dataframe_at_string(df: pd.DataFrame, string: str = "Total") -> pd.DataFrame:
    """
    Trim the DataFrame at the first occurrence of 'Total' in any column (case insensitive).
    
    :param df: The DataFrame to be trimmed.
    :param string: The string to search for in the DataFrame.
    :return: The trimmed DataFrame.
    """
    # Convert all values in the DataFrame to strings
    df_str = df.astype(str)

    # Find the index of the first occurrence of the specified string (case insensitive) in any column
    string_index = df_str.apply(lambda row: row.str.contains(string, case=False, na=False)).any(axis=1).idxmax()
    print(f"{string} index: {string_index}")
    

    if string_index > 0:
        return df.iloc[:string_index]
    
    else:
        # if string in first row, string_index will be 0, so check if it is, and if so return empty df
        if df_str.iloc[0].str.contains(string, case=False, na=False).any():
            return pd.DataFrame(columns=df.columns)
        
        # otherwise, not found in df and return the original df
        return df

