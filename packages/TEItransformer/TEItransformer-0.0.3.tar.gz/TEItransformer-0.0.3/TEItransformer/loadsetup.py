from .teiauxiliary import read_yaml, load_directories, create_file_list, DATA_DIR
from collections import defaultdict
import pkg_resources
import os


filenames = create_file_list(DATA_DIR, 'data', filenames=defaultdict(list))


TT_CFG = read_yaml(filenames['config']['tei_transformer.yaml'])
HTMLT_CFG = read_yaml(filenames['config']['html_transformer.yaml'])
DOCX_CFG = read_yaml(filenames['config']["docx_constructor.yaml"])


doc_temp = filenames['templates']['document7.html']
file_desc = filenames['xsl']['file-desc.xsl']



# SCHEMA_PATH = TT_CFG["PATHS"]["schema_dir"]
SCENARIOS = ['drama', 'plain']
