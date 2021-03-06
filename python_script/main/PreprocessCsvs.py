import pandas as pd
import re
import os

raw_csv_directory = "../raw_csv_storage"
preprocessed_csv_directory = "../preprocessed_csv_storage"


def first_time_asylum_applicants():
    filename = "firstTimeAsylumApplicants.csv"
    data = load_csv(filename)
    del data['SEX']
    del data['AGE'] # sex and age are always 'total', which makes them useless
    data['Value'] = data['Value'].apply(format_number)
    write_csv(data, filename)


def crime():
    filename = "crime.csv"
    data = load_csv(filename)
    data['Value'] = data['Value'].apply(format_number)
    write_csv(data, filename)


def general_processing():
    for file in os.listdir(raw_csv_directory):
        if file.endswith(".csv"):
            data = load_csv(file)
            if 'Value' in data:
                data['Value'] = data['Value'].apply(format_number)
            write_csv(data, file)


def format_number(numstring):
    return re.sub("[^0-9.]", "", str(numstring))


def load_csv(filename):
    slash = "/"
    if raw_csv_directory.endswith("/"):
        slash = ""
    return pd.read_csv(raw_csv_directory + slash + filename, sep=',')


def write_csv(data, filename):
    slash = "/"
    if preprocessed_csv_directory.endswith("/"):
        slash = ""
    data.to_csv(path_or_buf=preprocessed_csv_directory + slash + filename, index=False)


def perform_preprocessing():
    general_processing()
    # crime()
    # first_time_asylum_applicants()



perform_preprocessing()