import pandas as pd

raw_csv_directory = "../raw_csv_storage"
preprocessed_csv_directory = "../preprocessed_csv_storage"

def first_time_asylum_applicants():
    filename = "firstTimeAsylumApplicants.csv"
    matrix = pd.read_csv(raw_csv_directory + "/" + filename, sep=',')
    #TODO perform preprocessing
    matrix.to_csv(path_or_buf=preprocessed_csv_directory + "/" + filename, index=False)

first_time_asylum_applicants()