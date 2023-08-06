# -*- coding: utf-8 -*-

import os
import copy
import logging

from .setup import SCHEMA_PATH, TT_CFG
from lxml import etree
from .path_validator import PathValidator

SCHEMA_ROOT = etree.XML(TT_CFG['SCHEMA']['root'])


# class PathValidator:
#
#     @staticmethod
#     def if_exists(filepath):
#         if os.path.isfile(filepath):
#             return True
#         return False
#
#     @staticmethod
#     def __check_extension(filepath, extension_type):
#         filename, extension = os.path.splitext(filepath)
#         return extension in TT_CFG['FORMATS'][extension_type]
#
#     def validate_path(self, filepath, extension_type):
#         exists = self.if_exists(filepath)
#         cor_extension = self.__check_extension(filepath, extension_type)
#         if exists and cor_extension: return True
#         raise OSError("Incorrect extension or file not found")


class SchemaValidator:

    @staticmethod
    def load_rng_schema(schema_path):
        relaxng_doc = etree.parse(schema_path)
        relaxng = etree.RelaxNG(relaxng_doc)
        return relaxng

    @staticmethod
    def load_dtd_schema(schema_path):
        dtd = etree.DTD(file=schema_path)
        return dtd

    @staticmethod
    def load_xsd_schema(schema_path):
        xmlschema_doc = etree.parse(schema_path)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        return xmlschema

    def load_schema(self, schema_path, schema_type):
        parser_func = "load_{}_schema".format(schema_type)
        schema_parser = getattr(self, parser_func)(schema_path)
        return schema_parser

    def validator_generator(self, scenario):
        schema_folder = os.path.join(SCHEMA_PATH, scenario, TT_CFG['FORMATS']['default_schema'])
        os.chdir(schema_folder)
        filename = "tei_{}.{}".format(scenario, TT_CFG['FORMATS']['default_schema'])
        schema_parser = self.load_schema(filename, TT_CFG['FORMATS']['default_schema'])
        return schema_parser

    @staticmethod
    def __get_schema_locations(tei, nsp):
        pattern = TT_CFG['SCHEMA']['loc_pattern'].format(nsp)
        schema_locs = set(tei.root.xpath(pattern, namespaces=tei.nsmap))
        return schema_locs

    @staticmethod
    def __add_schema_import(location, schema_root):
        schema_params = location.strip().split()
        xs_import = etree.Element(TT_CFG['SCHEMA']['xs_import'])
        if len(schema_params) != 2:
            raise ValueError("The namespace is required for schemaLocation")
        xs_import.attrib['namespace'] = schema_params[0]
        xs_import.attrib['schemaLocation'] = schema_params[1]
        schema_root.append(xs_import)
        return schema_root

    def __import_schema(self, schema_locs):
        schema_root = copy.deepcopy(SCHEMA_ROOT)
        for location in schema_locs:
            schema_root = self.__add_schema_import(location, schema_root)
        return schema_root

    def __check_root_by_namespace(self, tei, nsp):
        schema_locs = self.__get_schema_locations(tei, nsp)
        if schema_locs:
            schema_root = self.__import_schema(schema_locs)
            schema = etree.XMLSchema(schema_root)
            return schema
        return False

    def check_root(self, tei):
        for nsp in tei.nsmap:
            schema = self.__check_root_by_namespace(tei, nsp)
            if schema: return schema
        return False


class XMLValidator(PathValidator, SchemaValidator):

    @staticmethod
    def __validate_schema(tei, validator):
        if validator.validate(tei.dom):
            return True
        logging.warning("Invalid TEI")
        return False

    def __validate_against_schema(self, tei, schema_path):
        _, extension = os.path.splitext(schema_path)
        validator = self.load_schema(schema_path, extension[1:])
        self.__validate_schema(tei, validator)

    def __validate_default_schema(self, tei, scenario):
        cur_directory = os.getcwd()
        validator = self.validator_generator(scenario)
        self.__validate_schema(tei, validator)
        os.chdir(cur_directory)

    def validate(self, tei, schema_path=None, scenario=None):
        root_validator = self.check_root(tei)
        if schema_path:
            self.validate_path(schema_path, extension_type='schema')
            self.__validate_against_schema(tei, schema_path)
        elif root_validator:
            self.__validate_schema(tei, root_validator)
        elif scenario:
            self.__validate_default_schema(tei, scenario)
