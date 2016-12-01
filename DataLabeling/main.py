import os.path
import pandas
from vars import *
import numpy as np
import re
from labeling_interaction import start_interaction

# TODO Ignored labels onthouden en in de toekomst ook negeren
# TODO pijlte naar boven = previous commandresult
# TODO allow spaces in file name
# TODO sum monthly data to yearly
# TODO allow folder
# TODO na drops moet je index aanpassen he slimme


# goes through the csv processing process.
# Starts by asking the csv name
# Next it will convert the csv to a matrix
# Then using the interaction of the user, but automated as much as possible, labels will be identified
def start_process():
    # ask for filename to process
    # TODO implement deze shit
    print 'Type the filename of the csv you want to process. Type all if you want to process all csvs in folder.\n' \
          'You can also add arguments after the filename: \n' \
          '     - labels= LOCATION : this tells us where the labels are\n' \
          '             example LOCATION:   column 1 (Tells us the labels are on the first column\n' \
          '                                 row 4 (Tells us the labels start on the forth row.\n' \
          '                                 multi 1 2 (Tells us you are using a multi label e.g. geo\\time, that' \
          'starts on the first row, second column\n' \
          '     - automate= add_all : no questions will be asked to you, unless no labels at all are found, all labels' \
          'that are not known general labels yet, will be added as a general label (caution, may be inaccurate)\n' \
          '     - automate= add_none : no questions will be asked to you, unless no labels at all are found, none of ' \
          'the labels will be added to the general labels\n' \
          '     - split= boolean : will split your files by location and time, the result will be a set of csvs' \
          'that contain one country per csv, the same categories in every csv, sorted by year' \
          '     - remember= boolean : remembers the labels you ignored and ignores them in the future as well'
    user_input = 'crime.csv'  # raw_input('> ')
    print_welcome = True
    while not user_input == 'done':
        split = user_input.split('.csv ')
        file_name = csv_directory + split[0]
        args = []
        if len(split) > 1:
            file_name += '.csv'
            args = split[1].split(' ')
        location, automate, split, remember = process_arguments(args)
        # read all files in the csv directory
        if user_input == 'all':
            for f in os.listdir(csv_directory):
                result = str(process_csv(csv_directory + f, print_welcome, location, automate, split, remember))
                print_welcome = False
                write_results(result)
        # warn about an incorrect filename
        elif not os.path.isfile(file_name):
            print 'incorrect filename, please try again'
        # read one file
        else:
            result = str(process_csv(file_name, print_welcome, location, automate, split, remember))
            write_results(result)
        user_input = 'done'  # raw_input('\nEnter filename and possible arguments: \n > ')
        print_welcome = False

    print 'Thank you for using the tool, hope you enjoyed it!'


# Processes a list of arguments to the location, automate, split and remember arguments needed to process the csv
def process_arguments(args):
    location = None
    automate = None
    split = False
    remember = False
    i = 0
    while i < len(args):
        # labels argument, identify the location
        if args[i] == 'labels=':
            if args[i+1] == 'multi':
                location = ['multi', int(args[i+2]), int(args[i+3])]
                i += 3
            else:
                location = [args[i+1], int(args[i+2])]
                i += 2
        # automate argument, identify type of automation
        elif args[i] == 'automate=':
            automate = args[i+1]
            i += 1
        # split argument, identify if user wants to split or not
        elif args[i] == 'split=':
            split = args[i+1].lower() == 'true'
            i += 1
        # remember argument, identify if user wants to remember ignored or not
        elif args[i] == 'remember=':
            remember = args[i+1].lower() == 'true'
            i += 1
        else:
            print 'Invalid argument ignored.'
        i += 1
    return location, automate, split, remember


def write_results(result):
    print 'Result: '
    print result
    print 'Result writing not implemented yet'
    # if LOCATION_VAR:


# reads the given csv file into a pandas matrix and starts the user interaction
# When the interaction is finished, the general labels are returned.
def process_csv(f, print_welcome, location, automate, split, remember):
    m = pandas.read_csv(f, sep=',')
    print '\nCurrently processing: ' + f + '\n'
    m = transform_matrix(m, location)
    correct_types(m)
    create_uppercase_column_labels(m)
    general_label_dict = start_interaction(m, print_welcome)
    # general_label_dict = {'Value': 'TEST', 'GEO': 'LOCATION', 'TIME': 'DATE'}
    return convert(m, general_label_dict)


# Makes the column labels of the given matrix all uppercase
def create_uppercase_column_labels(m):
    uppercase_columns = ['']*len(m.columns)
    for i, column in enumerate(m.columns):
        column = str(column)
        uppercase_columns[i] = column.upper()
    m.columns = uppercase_columns


# Searches for a possible set of labels. These labels can be in the first five rows, or in the first five columns
# If no labels are found, an error message is print, and the user is asked to manually reconfigure the csv
# TODO methode needs cleaning, lelijkste methode ooit :/
def transform_matrix(matrix, location):
    had_multilabel = False
    # user specified some location for the labels
    if location is not None:
        if location[0] == 'multi':
            row_index = location[1]
            column_index = location[2]
            if not row_index == 0:
                matrix.columns = list(matrix.loc[[row_index-1]].values)
                matrix = matrix.drop(matrix.index[[range(row_index)]])
            if not column_index == 0:
                for i in range(column_index):
                    del matrix[matrix.columns[0]]
            labels = is_multi_label(matrix.columns[0])
            labels_1 = matrix[matrix.columns[0]].values
            labels_2 = matrix.columns[1:]
            label_1 = labels[0]
            label_2 = labels[1]
            had_multilabel = True
        elif location[0] == 'column':
            matrix.loc[-1] = matrix.columns
            matrix.index += 1  # shifting index
            matrix = matrix.sort_index()  # sorting by index
            column_index = location[1]
            labels = matrix[matrix.columns[column_index]].values
            matrix = matrix.transpose()
            matrix.columns = labels
            index = range(len(matrix[matrix.columns[0]].values))
            matrix.index = index
            matrix = matrix.drop(matrix.index[[range(column_index+1)]])
            return matrix
        elif location[0] == 'row':
            # TODO werkt het wel?
            row_index = location[1]
            if row_index == 0:
                return matrix
            row_index -= 1
            labels = matrix.iloc[row_index].values
            matrix.columns = labels
            index = range(len(matrix[matrix.columns[0]].values))
            matrix.index = index
            matrix = matrix.drop(matrix.index[[range(row_index + 1)]])
            return matrix
    else:
        # Search if there is a single cell label
        labels = is_multi_label(matrix.columns[0])
        labels_1 = None
        labels_2 = None
        label_1 = None
        label_2 = None
        if labels:
            label_1 = labels[0]
            label_2 = labels[1]
            had_multilabel = True
        else:
            for i, label in enumerate(matrix[matrix.columns[0]]):
                labels = is_multi_label(label)
                if labels:
                    label_1 = labels[0]
                    label_2 = labels[1]
                    labels_2 = matrix.iloc[i][1:]
                    matrix = matrix.drop(matrix.index[[range(i)]])
                    had_multilabel = True
        labels_1 = matrix[matrix.columns[0]][1:]

    # if a multi-label was found, then transform the matrix
    if had_multilabel:
        clean_first_column = []
        for l in labels_1:
            clean_first_column += [l]*len(labels_2)
        clean_first_column = np.asarray(clean_first_column).transpose()

        clean_second_column = []
        for _ in labels_1:
            for l in labels_2:
                clean_second_column += [l]
        clean_second_column = np.asarray(clean_second_column).transpose()

        index = np.arange(len(clean_first_column))
        m = pandas.DataFrame(np.nan, index=index, columns=[label_1, label_2, value_label])
        m[label_1] = clean_first_column
        m[label_2] = clean_second_column
        del matrix[matrix.columns[0]]
        matrix = matrix.drop(matrix.index[[range(1)]])
        for i, row in matrix.iterrows():
            for j, element in enumerate(row.values):
                nr = (i-2)*(len(labels_2)) + j
                m.set_value(nr, value_label, convert_to_float(element))

        return m

    # Search best label row or column
    # Check if current column labels are labels, if so, do nothing
    possible_labels_row = matrix.columns
    possible_labels_row_nr = are_labels(possible_labels_row)
    i_row = 'index'

    # Search for the best row for representing labels
    for i, row in matrix.iterrows():
        # If the row you are checking has an index higher than the allowed, skip the rest of the rows
        if i > number_of_rows_to_check:
            break
        # if the i'th row is a label row, remove the first i rows and make the i'th row the column labels
        new_possible_labels = row.values
        new_nr = are_labels(new_possible_labels)

        if new_nr > possible_labels_row_nr:
            possible_labels_row = new_possible_labels
            possible_labels_row_nr = new_nr
            i_row = i
            # matrix = matrix.drop(matrix.index[[range(i+1)]])
            # matrix.columns = possible_labels

    # search for the best column to represent labels
    possible_labels_column = None
    possible_labels_column_nr = 0
    i_column = 0
    for i, column in enumerate(matrix.columns[:number_of_columns_to_check]):
        new_possible_labels = matrix[column]
        new_nr = are_labels(new_possible_labels)
        if new_nr > possible_labels_column_nr:
            possible_labels_column = new_possible_labels
            possible_labels_column_nr = new_nr
            i_column = i

    if possible_labels_column_nr > possible_labels_row_nr:
        # The given column has the most likely hood of being the label representation
        matrix = matrix.transpose()
        matrix.columns = possible_labels_column
        matrix = matrix.drop(matrix.index[[range(i_column + 1)]])
    else:
        if not i_row == 'index':
            matrix.columns = possible_labels_row
            matrix = matrix.drop(matrix.index[[range(i_row + 1)]])

    return matrix


# Checks if the label could be a multi label e.g. geo\time
def is_multi_label(label):
    label = str(label)
    labels = re.split(multi_label_splitters, label)
    if len(labels) == 2:
        if is_label(labels[0]) and is_label(labels[1]):
            return [labels[0], labels[1]]
    else:
        return False


# Checks if the given array are possible labels
# To be identified as labels, at least 10% of the given labels need to be actual labels
def are_labels(possible_labels):
    number_of_labels = len(possible_labels)
    counter = 0
    for possible_label in possible_labels:
        if is_label(possible_label):
            counter += 1
    return counter*100/number_of_labels


# Checks if a given possible label is an actual known general label
def is_label(possible_label):
    possible_label = str(possible_label)
    if possible_label == '':
        return False
    for file_name in os.listdir(label_directory):
        with open(label_directory + file_name) as f:
            for line in f:
                if str(possible_label.upper()) in line:
                        return True
    return False


# Makes correct types of matrix, i.e. 20,001.5 is replaced by 20001.5, ; or : become NaN, dates become dates.
def correct_types(matrix):
    for column in matrix:
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
        value = str(value)
        value = value.replace(',', '')
        value = value.replace(' ', '')
        value = value.replace(':', '')
        value = value.replace(';', '')
        matrix.set_value(i, column, value)
    matrix[column] = pandas.to_numeric(matrix[column], errors='coerce')


def convert_to_float(value):
    value = str(value)
    value = value.replace(',', '')
    value = value.replace(' ', '')
    value = value.replace(':', '')
    value = value.replace(';', '')
    if is_float(value):
        return float(value)
    else:
        return np.nan


# Checks whether or not a given string is a int
def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


# Checks whether or not a given string is a float
def is_float(string):
    try:
        float(string)
        return True
    except (ValueError, TypeError) as e:
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
        # if columns consist of numbers, all operators are possible
        if labels_represent_number(labels[1::2]):
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
        # if columns are strings, concatenate with a space in between
        else:
            i = 1
            while i + 1 < len(labels):
                spaces_column = [' ']*len(column_result)
                label_part = labels[i + 1]
                operator = labels[i]
                if operator == '+':
                    column_result += spaces_column + matrix[label_part]
                else:
                    print 'Error during conversion: invalid operator'  # TODO hoe nu verder?
                i += 2

        general_label = general_label_dict[key]
        result[general_label] = column_result

    return result


# Checks if all given labels are numbers
def labels_represent_number(labels):
    for label in labels:
        if not is_float(label) and not is_int(label):
            return False
    return True


start_process()
