import os
import pandas as pd

def dateparser(x): return pd.to_datetime(x, format="%d/%m/%Y %H:%M:%S")

d_types = {'Contract': str, 'Operation RelNr': str}
cols = ['Created On (Contract)',
        'Contract',
        'Operation RelNr',
        'Material Number',
        'Setup Duration Actual',
        'Setup Duration Planned',
        'Processing Duration Actual',
        'Processing Duration Planned',
        'Teardown Duration Actual',
        'Teardown Duration Planned',
        'Downtime Actual',
        'Good Quantity Actual (Recording Unit)',
        'Good Quantity Planned (Recording Unit)',
        'Scrap Quantity Actual (Recording Unit)',
        'Start Date Actual',
        'Start Date Planned',
        'End Date Actual',
        'End Date Planned',
        'Availability',
        'Performance',
        'Quality']

dates = ['Created On (Contract)', 'Start Date Actual', 'End Date Actual',
         'Start Date Planned', 'End Date Planned']

def parse_data(path, file_name, cols, dates, dateparser, d_types) -> pd.DataFrame:
    """
    Parses a CSV file containing data with specific columns and date formats and returns a pandas DataFrame.

    Parameters:
        path (str): The directory path where the CSV file is located.
        file_name (str): The name of the CSV file to be parsed.
        cols (list): List of column names to be read from the CSV file.
        dates (list): List of column names to be parsed as dates.
        dateparser (function): A function to parse dates in the CSV file.
        d_types (dict): Dictionary specifying the data types for specific columns.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the parsed data.
    """
    df = pd.read_csv(os.path.join(path, file_name), sep=';', usecols=cols, parse_dates=dates, date_parser=dateparser,
                     low_memory=False, dtype=d_types)
    return df

def filter_na(df) -> pd.DataFrame:
    """
    Filters out rows with 'Operation RelNr' starting with 'UNA' (Unplanned Rework) from the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    df = df.loc[~df["Operation RelNr"].str.startswith("UNA")]
    return df

def filter_df_by_matnr(df, material_number):
    """
    Filters DataFrame rows by 'Material Number' column.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        material_number (str): Material Number to filter DataFrame rows.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    df = df.loc[df['Material Number'] == material_number]
    return df

def import_data(input_path, data_file):
    """
    Imports data from a CSV file with specific configurations.

    Parameters:
        input_path (str): The directory path where the CSV file is located.
        data_file (str): The name of the CSV file to be imported.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the imported data.
    """
    data_df = parse_data(input_path, data_file, cols, dates, dateparser, d_types)
    return data_df
