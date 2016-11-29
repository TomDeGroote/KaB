import os.path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
csv_directory = ROOT_DIR + "/csvs/"
label_directory = ROOT_DIR + "/labels/"
format_directory = ROOT_DIR + "/formats/"
operators = ["+", "-", "*", "/"]
operators_regex = ' + | - | * | / '
percent_to_be_float = 30
number_of_rows_to_check = 5
number_of_columns_to_check = 5
LOCATION_VAR = 'LOCATION'
