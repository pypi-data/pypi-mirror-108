from .teiauxiliary import read_yaml, load_directories, create_file_list
import pkg_resources
import os


filenames = create_file_list()

TT_CFG = read_yaml(filenames['config']['tei_transformer.yaml'])
HTMLT_CFG = read_yaml(filenames['config']['html_transformer.yaml'])
DOCX_CFG = read_yaml(filenames['config']["docx_constructor.yaml"])

SCHEMA_PATH = TT_CFG["PATHS"]["schema_dir"]
SCENARIOS = load_directories(SCHEMA_PATH)
