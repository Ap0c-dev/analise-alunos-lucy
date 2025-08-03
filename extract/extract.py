import pandas as pd

def extract_data(path=None, sheet_name=None, header=None):
    df = pd.read_excel(
        path,
        engine='openpyxl',
        sheet_name=sheet_name,
        header=header)
    return df