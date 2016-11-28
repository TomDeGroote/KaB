import os.path
import pandas
from vars import *
from user_interaction import start_interaction


# TODO convert using general labels
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
    user_input = raw_input('Give csv name (type \'all\' if you want to process all in csvs folder, or type done: ')
    print_welcome = True
    while not user_input == 'done':
        file_name = csv_directory + user_input
        # read all files in the csv directory
        if user_input == 'all':
            for f in os.listdir(csv_directory):
                print 'Result: ' + str(process_csv(csv_directory + f, print_welcome))
                print_welcome = False
        # warn about an incorrect filename
        elif not os.path.isfile(csv_directory + file_name):
            print 'incorrect filename, please try again'
        # read one file
        else:
            print 'Result: ' + str(process_csv(csv_directory + file_name, print_welcome))
        user_input = raw_input('Give csv name: ')
        print_welcome = False

    print 'Thank you for using the tool, hope you enjoyed it!'


# reads the given csv file into a pandas matrix and starts the user interaction
# When the interaction is finished, the general labels are returned.
def process_csv(f, print_welcome):
    m = pandas.read_csv(f, sep=',')
    print '\nCurrently processing: ' + f + '\n'
    result = start_interaction(m, print_welcome)
    convert(m, result)


# Searches for a possible set of labels. These labels can be in the first five rows, or in the first five columns
# If no labels are found, an error message is print, and the user is asked to manually reconfigure the csv
def transform_matrix(matrix):
    print 'not implemented yet'


# Initial labels are replaced by their general labels, if the general label is 'None' the column will be thrown away.
# Here sums etc are also calculated if the label contains an operator
def convert(matrix, result):
    # Count the number of non 'None' labels
    nr_of_labels = 0
    for label in result:
        if label is not None:
            nr_of_labels += 1

    # initialize the resulting matrix
    # TODO

    # copy data to correct columns
    # TODO
    for label in result:
        labels = label.split('operator')  # TODO generic operator
        column_result = matrix.iloc(labels[0])
        i = 1
        while i < len(labels):
            label_part = labels[i]
            operator = labels[i+1]
            if operator == '+':
                print 'not implemented yet'  # TODO
            elif operator == '-':
                print 'not implemented yet'  # TODO
            elif operator == '*':
                print 'not implemented yet'  # TODO
            elif operator == '/':
                print 'not implemented yet'  # TODO
            else:
                print 'Error during conversion: invalid operator'  # TODO hoe nu verder?
            i += 2





process_csv()
