import os.path
import pandas
from vars import *
import numpy as np
import re
from labeling_interaction import start_interaction


# TODO wat als labels de rijen zijn en niet de kolommen => transpose, maar hoe herkennen
# (gebruiker laten identificeren) en of zelf proberen
# TODO wat als file start op een andere lijn
# TODO als gebruiker start en geen extra parameters doorstuurt en er wordt niets herkend, vraag de gebruiker dan
# TODO argumenten toelaten (label start, label kolom/rij, vraag geen labels, voeg alle ongekende labels toe)
# in meer detail over de situatie van de file

# goes through the csv processing process.
# Starts by asking the csv name
# Next it will convert the csv to a matrix
# Then using the interaction of the user, but automated as much as possible, labels will be identified
def start_process():
    # ask for filename to process
    user_input = "crime.csv"
    # user_input =  raw_input('Give csv name (type \'all\' if you want to process all in csvs folder, or type done: ')
    print_welcome = True
    while not user_input == 'done':
        file_name = csv_directory + user_input
        # read all files in the csv directory
        if user_input == 'all':
            for f in os.listdir(csv_directory):
                print 'Result: ' + str(process_csv(csv_directory + f, print_welcome))
                print_welcome = False
        # warn about an incorrect filename
        elif not os.path.isfile(file_name):
            print 'incorrect filename, please try again'
        # read one file
        else:
            result = str(process_csv(file_name, print_welcome))
            write_results(result)
        user_input = 'done'  # raw_input('Give csv name: ')
        print_welcome = False

    print 'Thank you for using the tool, hope you enjoyed it!'


def write_results(result):
    print 'not implemented yet'
    # if LOCATION_VAR:


# reads the given csv file into a pandas matrix and starts the user interaction
# When the interaction is finished, the general labels are returned.
def process_csv(f, print_welcome):
    m = pandas.read_csv(f, sep=',')
    print '\nCurrently processing: ' + f + '\n'
    # transform_matrix(m)
    correct_types(m)
    create_uppercase_column_labels(m)
    general_label_dict = start_interaction(m, print_welcome)
    # general_label_dict = {'Value': 'TEST', 'GEO': 'LOCATION', 'TIME': 'DATE'}
    return convert(m, general_label_dict)


# Makes the column labels of the given matrix all uppercase
def create_uppercase_column_labels(m):
    uppercase_columns = ['']*len(m.columns)
    for i, column in enumerate(m.columns):
        uppercase_columns[i] = column.upper()
    m.columns = uppercase_columns


# Searches for a possible set of labels. These labels can be in the first five rows, or in the first five columns
# If no labels are found, an error message is print, and the user is asked to manually reconfigure the csv
def transform_matrix(matrix):
    # Check if current column labels are labels, if so, do nothing
    possible_labels = matrix.columns

    if not are_labels(possible_labels):
        # Check if one of the first few rows is the label row
        for i, row in matrix.iterrows():
            # If the row you are checking has an index higher than the allowed, skip the rest of the rows
            if i > number_of_rows_to_check:
                break
            # if the i'th row is a label row, remove the first i rows and make the i'th row the column labels
            possible_labels = row.values
            if are_labels(possible_labels):
                matrix = matrix.drop(matrix.index[[range(i+1)]])
                matrix.columns = possible_labels
                print matrix
                return
        for i, column in enumerate(matrix.columns[:number_of_columns_to_check]):
            print matrix[column]
            # if the i'th column is a label column, transpose and
            # remove the first i rows and make the i'th row the column labels
            if are_labels(matrix[column]):
                matrix = matrix.transpose
                print matrix
                return
    else:
        print 'labels found ' + str(possible_labels)


# Checks if the given array are possible labels
# To be identified as labels, at least 10% of the given labels need to be actual labels
def are_labels(possible_labels):
    number_of_labels = len(possible_labels)
    counter = 0
    for possible_label in possible_labels:
        if is_label(possible_label):
            counter += 1
            if counter*10 > number_of_labels:
                return True


# Checks if a given possible label is an actual known general label
def is_label(possible_label):
    for file_name in os.listdir(label_directory):
        with open(label_directory + file_name) as f:
            for line in f:
                if str(possible_label) in line:
                        return True


# Makes correct types of matrix, i.e. 20,001.5 is replaced by 20001.5, ; or : become NaN, dates become dates.
def correct_types(matrix):
    print 'Starting type corrections...'
    for column in matrix:
        if matrix[column].dtype == 'object':
            count = 0
            total = len(matrix[column].values)
            for value in matrix[column].values:
                if is_float(value):
                    count += 1
            if count*100/total > percent_to_be_float:
                clean_numbers(matrix, column)


# Given a matrix and a column identifier, the column will be cleaned:
#   - , will become nothing (since it is mostly used to separate large numbers: 10,000 becomes 10000)
#   - spaces, : and ; will be removed
#   - If after the conversion the values are still not of the float type, NaN will be put instead
def clean_numbers(matrix, column):
    for i, value in enumerate(matrix[column].values):
        value = value.replace(',', '')
        value = value.replace(' ', '')
        value = value.replace(':', '')
        value = value.replace(';', '')
    matrix[column] = pandas.to_numeric(matrix[column], errors='coerce')


# Checks whether or not a given string is a float
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


# Initial labels are replaced by their general labels, if the general label is 'None' the column will be thrown away.
# Here sums etc are also calculated if the label contains an operator
def convert(matrix, general_label_dict):
    # initialize the resulting matrix
    index = matrix.index  # TODO make index the date?
    columns = sorted(general_label_dict.values())
    result = pandas.DataFrame(np.nan, index=index, columns=columns)

    # copy data to correct columns and execute operators (if included in label)
    for key in general_label_dict.keys():
        labels = re.split(operators_regex, key)
        column_result = matrix[labels[0]].copy()  # select first column of possibly composed columns
        i = 1
        while i+1 < len(labels):
            label_part = labels[i+1]
            operator = labels[i]
            if operator == '+':
                column_result += matrix[label_part]
            elif operator == '-':
                column_result -= matrix[label_part]
            elif operator == '*':
                column_result *= matrix[label_part]
            elif operator == '/':
                column_result /= matrix[label_part]
            else:
                print 'Error during conversion: invalid operator'  # TODO hoe nu verder?
            i += 2

        general_label = general_label_dict[key]
        result[general_label] = column_result

    return result


start_process()
