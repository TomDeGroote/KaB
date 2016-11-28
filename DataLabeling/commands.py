def print_help():
    print 'Possible commands: \n' \
          '     - help :\n' \
          '         shows the help text\n' \
          '     - local_label_1 operator local_label_2 operator ... operator local_label_n = general_label : \n' \
          '         assigns the part before the = to the general label, possible operators: + - * /\n' \
          '         this can also be used to overwrite current assigned general labels\n' \
          '         operators will be executed from left to right' \
          '     - remove general_label label :\n' \
          '         removes the label from general labels\n' \
          '     - show initial :\n' \
          '         shows the initial labels\n' \
          '     - show general :\n' \
          '         shows the general labels\n' \
          '     - show composed :\n' \
          '         shows the composed labels (i.e. the labels with an operator)\n' \
          '     - show labels :\n' \
          '         shows the current labels, green labels have a known label category, red ones don\'t'


def print_welcome_text():
    print 'Welcome to this label assigment tool. We will try to automate as much as possible, but sometimes your ' \
          'input will be required.\n' \
          'Beneath this text we show the current labels we found in your matrix.\n' \
          'Green labels are known labels, the general label for this label is shown between parentheses. \n' \
          'Red labels are unknown. To identify labels please type in the following format: GENERAL = UNKNOWN_LABEL. \n'\
          'For a list of possible commands, type help.\n' \
          'Enjoy!\n'


def show_invalid_command():
    print 'Not a valid command.'


def remove_label(label, general):
    print 'not implemented yet'


def add_label_format(label, format):
    print 'not implemented yet'


