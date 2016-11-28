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
            print 'Result:\n' + str(process_csv(file_name, print_welcome))
        user_input = raw_input('Give csv name: ')
        print_welcome = False

    print 'Thank you for using the tool, hope you enjoyed it!'


# reads the given csv file into a pandas matrix and starts the user interaction
# When the interaction is finished, the general labels are returned.
def process_csv(f, print_welcome):
    m = pandas.read_csv(f, sep=',')
    print '\nCurrently processing: ' + f + '\n'
    # general_label_dict = start_interaction(m, print_welcome)
    general_label_dict = {'Value': 'TEST', 'GEO': 'LOCATION', 'TIME': 'DATE'}
    return convert(m, general_label_dict)


# Searches for a possible set of labels. These labels can be in the first five rows, or in the first five columns
# If no labels are found, an error message is print, and the user is asked to manually reconfigure the csv
def transform_matrix(matrix):
    print 'not implemented yet'


# Makes correct types of matrix, i.e. 20,001.5 is replaced by 20001.5, ; or : become NaN, dates become dates.
def correct_types(matrix):
    print 'not implemented yet'


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
