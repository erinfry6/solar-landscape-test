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