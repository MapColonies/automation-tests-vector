"""This module provide method to generate new full layer json data for sync to OSM"""
import os
import json
from server_automation.configuration import config
from mc_automation_tools import common

import logging
_log = logging.getLogger('server_automation.support_utilities.layer_generator')

def generate_single_full_json(layer_id, file_count=1, file_name='entities', files=[]):
    """This method create full_json file to start synchronization"""
    layer_id = str(layer_id)
    unique_id = common.generate_uuid().replace('-', '_')
    current_date = common.generate_datatime_zulu()
    file_name = "_".join([layer_id, unique_id])

    single_file = {"layer_id": config.LAYER_ID_B, 'exec_type': layer_id, 'files': files}


def generate_entity_file(layer_id, file_count=1, file_name='entities', object_count=10, output_dir = config.STORE_DATA_DIR):
    """
    This method will generate single file object for specific layer type
    :param layer_id: layer type id
    :param file_count: number of file per file entity
    :param file_name: file entity name
    :param object_count: number of objects per entity file (polygons)
    :return: dict of single file object 
    """
    output_dir = os.path.join(output_dir, str(layer_id))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def generate_entity_json(num_of_files=10, entities_per_file=10, source='small'):
    """
    This method generate json file entity with polygons
    :return: json object with entities
    """

    total_entities = num_of_files*entities_per_file
    source_data = json.load(open(source, "r"))
    polygons = source_data['features']

    for i in range(num_of_files):

        for j in range(entities_per_file):

            entity = {'exclusive_id'}
