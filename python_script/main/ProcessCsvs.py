import os
import pandas as pd

csv_directory = "../preprocessed_csv_storage"
csv_dicts = {}

# load a .csv file and save it to a dictionary
def process_csv(file):
    matrix = pd.read_csv(csv_directory + "/" + file, sep=',')
    csv_dicts[file] = matrix

# loop over all .csv files in csv_storage
def process_csv_storage():
    for file in os.listdir(csv_directory):
        if file.endswith(".csv"):
            process_csv(file)

process_csv_storage()
