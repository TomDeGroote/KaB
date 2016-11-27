import os.path
from bcolors import bcolors
from vars import label_directory
from commands import *

# TODO als optie toevoegen ongekende labels toe te voegen
# TODO operators enablen


# processes the input given by the user, at the end of the user interaction (when done is typed)
# the result of general labels is returned
def start_interaction(matrix, print_welcome):
    label_row = get_initial_matrix_labels(matrix)  # get the initial labels
    general_labels = get_general_labels(label_row)  # get the general labels for the initial labels

    initial_label_row = label_row
    initial_general_labels = general_labels

    if print_welcome:
        # welcome the user using a welcome text
        print_welcome_text()
    # print the current labels and there general labels
    show_labels(label_row, general_labels)
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
                        show_labels(initial_label_row, initial_general_labels)
                    elif l[1] == 'labels':
                        show_labels(label_row, general_labels)
                    elif l[1] == 'general':
                        print general_labels
                    else:
                        show_invalid_command()
                elif l[0] == 'format':
                    add_label_format(l[1], l[2])

            else:
                # Add the label to the general labels and to the matching label file
                if l[0] not in label_row:
                    show_invalid_command()
                else:
                    general_labels[label_row.index(l[0])] = l[1]  # add the given label to general labels
                    if not os.path.isfile(label_directory + l[1].lower()):
                        with open(label_directory + l[1].lower(), "a") as my_file:
                            my_file.write(l[1].upper() + "\n")
                            my_file.write(l[0].upper() + "\n")
                    else:
                        with open(label_directory + l[1].lower(), "a") as my_file:
                            my_file.write(l[0].upper() + "\n")

        given_label = raw_input('> ')
    return general_labels


# searches the known and unknown labels in the initial matrix and uses colors to identify them to the user
def get_initial_matrix_labels(matrix):
    label_row = list(matrix.columns.values)  # The labels as given in the csv
    return label_row


# generates a list of general labels from the initial label list
def get_general_labels(label_row):
    general_labels = [None] * len(label_row)
    i = 0
    for label in label_row:
        general_label = check_if_known_label(label)
        if general_label:
            general_labels[i] = general_label
        i += 1
    return general_labels


# prints the current label row, inclusive colors (green for known label, red for unknown label)
def show_labels(label_row, general_labels):
    # Show the user if labels are known or unknown
    labels = '['
    i = 0
    for label in label_row:
        general_label = general_labels[i]
        if general_label is None:
            labels += bcolors.RED + label + bcolors.ENDC + ', '
        else:
            labels += bcolors.GREEN + label + bcolors.ENDC + ' (' + general_label + ')' + ', '
        i += 1
    labels = labels[:-2]
    labels += ']'
    print labels


# Check if the given label is known, if so return the general label, if not return FALSE
def check_if_known_label(label):
    label = label.upper()
    for file_name in os.listdir(label_directory):
        if label in open(label_directory + file_name).read():
            return file_name.upper()
    else:
        return False

