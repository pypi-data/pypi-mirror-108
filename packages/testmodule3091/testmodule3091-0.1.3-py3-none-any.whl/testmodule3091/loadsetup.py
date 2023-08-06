from .teiauxiliary import read_yaml, load_directories
import pkg_resources
import os


# TT_CFG = read_yaml("data/config/tei_transformer.yaml")
# HTMLT_CFG = read_yaml("data/config/html_transformer.yaml")


PROJECT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(PROJECT_DIR, 'data')

filenames = os.listdir(DATA_DIR)


# resource = 'testmodule3091'
# res = ['regs.txt', 'diacrit.json', 'cons.json', 'vows.json', 'ftable.json', 'index_column.json', 'rows.json']
# paths = ['/'.join(('data', i)) for i in res]
# filenames = [pkg_resources.resource_filename(resource, path) for path in paths]

# SCHEMA_PATH = TT_CFG["PATHS"]["schema_dir"]
# SCENARIOS = load_directories(SCHEMA_PATH)
