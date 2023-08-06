from .teiauxiliary import read_yaml, load_directories, create_file_list
import pkg_resources
import os


# TT_CFG = read_yaml("data/config/tei_transformer.yaml")
# HTMLT_CFG = read_yaml("data/config/html_transformer.yaml")

filenames = create_file_list()

TT_CFG = read_yaml(filenames['config']['tei_transformer.yaml'])
HTMLT_CFG = read_yaml(tei_transformer.yamlfilenames['config']['html_transformer.yaml'])


# PROJECT_DIR = os.path.dirname(__file__)
# DATA_DIR = os.path.join(PROJECT_DIR, 'data')
# RESOURCE = 'testmodule3091'



		

# for dir_ in os.listdir(DATA_DIR):
# 	if not dir_.startswith('.'):
# 		dir_path = os.path.join(DATA_DIR, dir_)) 
# 		for file in os.listdir(dir_path):
# 			if not dir_.startswith('.')
		


# res = ['regs.txt', 'diacrit.json', 'cons.json', 'vows.json', 'ftable.json', 'index_column.json', 'rows.json']
# paths = ['/'.join(('data', i)) for i in res]
# filenames = [pkg_resources.resource_filename(resource, path) for path in paths]

# SCHEMA_PATH = TT_CFG["PATHS"]["schema_dir"]
# SCENARIOS = load_directories(SCHEMA_PATH)
