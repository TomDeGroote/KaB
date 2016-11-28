import os.path
from bcolors import bcolors
from vars import label_directory, operators
from commands import *

# TODO als optie toevoegen ongekende labels toe te voegen
# TODO operators enablen

general_label_dict = {}
composed_label_dict = {}


# processes the input given by the user, at the end of the user interaction (when done is typed)
# the result of general labels is returned
def start_interaction(matrix, print_welcome):
    label_row = get_initial_matrix_labels(matrix)  # get the initial labels
    add_labels_to_dicts(label_row)  # get the general labels for the initial labels

    initial_label_row = label_row

    if print_welcome:
        # welcome the user using a welcome text
        print_welcome_text()
    # print the current labels and there general labels
    show_labels(label_row)
    print ''

    # wait for input and process it
    given_label = raw_input('> ')
    while not given_label == 'done':
        # show the help text
        if given_label == 'help':
            print_help()
        else:
            # Check if the label assignment format is used ( there is a = in it)
            l = given_label.split(' = ')
            if len(l) < 2:
                l = given_label.split(' ')

                if len(l) < 2:
                    show_invalid_command()
                elif l[0] == 'remove':
                    remove_label(l[1], l[2])
                elif l[0] == 'show':
                    if l[1] == 'initial':
                        show_labels(initial_label_row)
                    elif l[1] == 'labels':
                        show_labels(label_row)
                    elif l[1] == 'general':
                        show_general_label_dict()
                    elif l[1] == 'composed':
                        print composed_label_dict
                    else:
                        show_invalid_command()
                elif l[0] == 'format':
                    add_label_format(l[1], l[2])

            else:
                # Add the label to the general labels and to the matching label file
                # TODO checken of wel valid labels?
                general_label_dict[l[0]] = l[1]  # add the given label to general labels
                if is_composed_label(l[0]):
                    add_to_composed_labels(l[0])
                if not os.path.isfile(label_directory + l[1].lower()):
                    with open(label_directory + l[1].lower(), "a") as my_file:
                        my_file.write(l[1].upper() + "\n")
                        my_file.write(l[0].upper() + "\n")
                else:
                    with open(label_directory + l[1].lower(), "a") as my_file:
                        my_file.write(l[0].upper() + "\n")

        given_label = raw_input('> ')
    return general_label_dict


# checks if the given label contains any operators
def is_composed_label(label):
    return any(ext in operators for ext in label)


# Adds all labels used in a composed label (i.e. using operators) to the composed label dict
def add_to_composed_labels(composed_label):
    no_operator_str = composed_label
    for operator in operators:
        no_operator_str = no_operator_str.replace(operator, ',')
    separate_labels = no_operator_str.split(" , ")
    for label in separate_labels:
        composed_label_dict[label] = composed_label


# searches the known and unknown labels in the initial matrix and uses colors to identify them to the user
def get_initial_matrix_labels(matrix):
    label_row = list(matrix.columns.values)  # The labels as given in the csv
    return label_row


# prints the current label row, inclusive colors (green for known label, red for unknown label)
def show_labels(label_row):
    # Show the user if labels are known or unknown
    labels = '['
    i = 0
    for label in label_row:
        label = label.upper()
        if label not in general_label_dict and label not in composed_label_dict:
            labels += bcolors.RED + label + bcolors.ENDC + ', '
        else:
            if label in composed_label_dict:
                composed_label = composed_label_dict[label]
                general_label = general_label_dict[composed_label] + " = " + composed_label
            else:
                general_label = general_label_dict[label]
            labels += bcolors.GREEN + label + bcolors.ENDC + ' (' + general_label + ')' + ', '
        i += 1
    labels = labels[:-2]
    labels += ']'
    print labels


# shows the general label dictionary
def show_general_label_dict():
    print general_label_dict


# Check if the given label is known, if so return the general label
# TODO kan volgens mij wel efficienter
def add_labels_to_dicts(label_row):
    for label in label_row:
        add_label_to_dict(label.upper())


# searches for the label in the file and adds it to the correct dictionaries
def add_label_to_dict(label):
    for file_name in os.listdir(label_directory):
            with open(label_directory + file_name) as f:
                for line in f:
                    if label in line:
                        if label == line[:-1]:
                            general_label_dict[label] = file_name.upper()
                            return
                        else:
                            general_label_dict[line[:-1]] = file_name.upper()
                            composed_label_dict[label] = line[:-1]
                            return
