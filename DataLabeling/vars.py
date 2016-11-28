import os.path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
csv_directory = ROOT_DIR + "/csvs/"
label_directory = ROOT_DIR + "/labels/"
format_directory = ROOT_DIR + "/formats/"
operators = ["+", "-", "*", "/"]
operators_regex = ' + | - | * | / '
