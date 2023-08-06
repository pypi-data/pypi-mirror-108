# -*- coding: utf-8 -*-
import os
import re

import yaml
import json
import logging

import pkg_resources
from collections import defaultdict


size_pattern = re.compile("(?P<value>(?:\d|\.)+)(?P<measure>[a-z]+)")
rgb_pattern = re.compile("rgb\((?P<r>.+?), (?P<g>.+?), (?P<b>.+?)\)")
CSS_VALUE_PATTERNS = [size_pattern, rgb_pattern]

PROJECT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
RESOURCE = 'TEItransformer'


# def get_files(path):
# 	for file in os.listdir(path):
# 		if not file.startswith('.'):
# 			yield file
# 			
# 
# def create_file_list(data_dir, filenames={}):
# # 	filenames = {}
# 	for dir_ in get_files(DATA_DIR):
# 		dir_path = os.path.join(DATA_DIR, dir_)
# 		filenames[dir_] = defaultdict(list)
# 		for file in get_files(dir_path):
# 			file_path = os.path.join(dir_path, file)
# 			filenames[dir_][file] = file_path
# 	return filenames


def create_file_list(data_dir0, dirname0, filenames={}):
    for file in get_files(data_dir0):
        file_path = os.path.join(data_dir0, file)
        filenames[file] = file_path
    
    for dirname1 in get_dirs(data_dir0):
        dir_path2 = os.path.join(data_dir0, dirname1)
        filenames[dirname1] = create_file_list(dir_path2, dirname1, filenames={})
            
    return filenames

def get_files(path):
    for file in os.listdir(path):
        if not file.startswith('.') and '.' in file:
            yield file
            
def get_dirs(path):
    for file in os.listdir(path):
        if not file.startswith('.') and '.' not in file:
            yield file
    
    


def read_yaml(path):
    """
    Reads yaml file.
    :param path: str
    :return: yaml object
    """
    with open(path) as f:
        data = yaml.safe_load(f)
    return data


def read_file(path):
    """
    Reads file.
    :param path: str
    :return: str
    """
    with open(path, "r", encoding='utf-8') as f:
        data = f.read()
    return data


def write_html(path, html, full_page=False):
    """
    Writes html to file.
    :param path: str
    :param html: lxml object
    :param full_page: bool
    :return: None
    """
    if full_page:
        html.write(path, pretty_print=True)
    else:
        with open(path, 'w', encoding="utf-8") as f:
            f.write(str(html))


def write_json(path, data):
    """
    Write json to file.
    :param path: str
    :param data: dict
    :return: None
    """
    with open(path, "w") as outfile:
        json.dump(data, outfile)


def load_directories(path):
    """
    Get directory names.
    :param path: str
    :return: list
    """
    dirs = [name
        for name in os.listdir(path)
        if os.path.isdir(os.path.join(path, name))
    ]
    return dirs


def get_filename(path):
    """
    Get filename from path.
    :param path: str
    :return: str
    """
    filename = os.path.split(path)[-1]
    filename = os.path.splitext(filename)[0]
    return filename


def prepare_func_name(*args, ftype='parse'):
    """
    Prepares function name.
    :param args: []
    :param ftype: str
    :return: name
    """
    name = "_".join((ftype,) + args)
    name = re.sub("-", "_", name)
    return name


def clean_text(text):
    """
    Preprocess text name.
    :param text: str
    :return: str
    """
    return ' '.join(text.split())


def css_value_parser(line):
    """
    Parse css rule.
    :param line: str
    :return: dict
    """
    global CSS_VALUE_PATTERNS
    for pattern in CSS_VALUE_PATTERNS:
        res = pattern.search(line)
        if res: return res.groupdict()
    return {}


def check_if_rgb(value):
    """
    Checks if color value is RGB.
    :param value: str
    :return: bool
    """
    try:
        cond1 = isinstance(value, str)
        cond2 = len(value) == 3
        cond3 = all(isinstance(x, int) for x in value)
        if cond1 and cond2 and cond3: return True
        return False
    except:
        return False


def check_bool(value, name):
    """
    Checks if variable is bool
    :param value: any
    :param name: str
    :return: None
    """
    if not isinstance(value, bool):
        raise ValueError("Wrong datatype. {} should be bool".format(name))
    return None


def check_str(value, name):
    """
    Checks if variable is str
    :param value: any
    :param name: str
    :return: None
    """
    if not isinstance(value, str):
        raise ValueError("Wrong datatype. {} should be string".format(name))
    return None


def check_iterable(value, name):
    """
    Checks if variable is int
    :param value: any
    :param name: str
    :return: None
    """
    if not isinstance(value, (list, tuple, set)):
        raise ValueError(
            "Wrong datatype. {} should be list, tuple or set".format(name)
        )
    return None


def check_scenario(scenario):
    """
    Checks is scenario is valid.
    :param scenario: str
    :return: str
    """
    if not isinstance(scenario, str):
        raise ValueError("Scenario. Wrong datatype.")
    scenarios = ['drama', 'plain']
    if scenario in scenarios:
        return scenario
    logging.warning("Wrong scenario. Available options: {}".format(*scenarios))
    return 'plain'


def check_extension():
    pass
