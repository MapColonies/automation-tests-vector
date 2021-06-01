"""This module provide method to generate new full layer json data for sync to OSM"""
import os
import json
import copy
import datetime
import shutil
from server_automation.configuration import config
from mc_automation_tools import common, geometry

import logging

_log = logging.getLogger('server_automation.support_utilities.layer_generator')


def generate_single_full_json(layer_id, file_count=1, file_name='entities', files=[]):
    """This method create full_json file to start synchronization"""
    layer_id = str(layer_id)
    unique_id = common.generate_uuid().replace('-', '_')
    current_date = common.generate_datatime_zulu()
    file_name = "_".join([layer_id, unique_id])

    single_file = {"layer_id": config.LAYER_ID_B, 'exec_type': layer_id, 'files': files}


def generate_entity_file(layer_id, n_zips=10, n_files=10, n_objects=10, file_name='entities',
                         output_dir=config.STORE_DATA_DIR, source=config.DEBUG_ENTITY_FILE):
    """
    This method will generate single file object for specific layer type
    :param source: source directory to ingest polygons for entities
    :param output_dir: destination root directory to store generated data
    :param n_zips: number of zips per directory to create
    :param layer_id: layer type id
    :param n_files: number of file per zip
    :param file_name: file entity name
    :param n_objects: number of objects per entity file (polygons)
    :return: dict of single file object 
    """

    output_dir = os.path.join(output_dir, str(layer_id))
    _log.info(f'New job of generating data:\n'
              f'Destination directory storing generated data: {output_dir}\n'
              f'Number of zip files: {n_zips}\n'
              f'Number of json files per single zip: {n_files}\n'
              f'Number of object per json (polygons): {n_objects}\n'
              f'Total dataset for [FULL] to generate: {n_zips * n_files * n_objects}')

    # validating the provided source to generation include enough data to requested generation
    source_data = json.load(open(source, "r"))
    polygons = source_data['features']
    _log.info(f'Total number of features on data source: {len(polygons)}')
    if len(polygons) < (n_zips * n_files * n_objects):
        raise Exception(f"Provided data source doesn't fit to requested size of generation:\n"
                        f"Requested [{n_zips * n_files * n_objects}] > Source data polygon count [{len(polygons)}]")

    for i in range(n_zips):
        zip_id = "_".join([str(layer_id), common.generate_uuid()])
        zip_dir = os.path.join(output_dir, zip_id)
        if not os.path.exists(zip_dir):
            os.makedirs(zip_dir)
        offset = i * n_files * n_objects
        _log.info(f'Generating zip {i + 1}\\{n_zips}: {zip_id}, into: {zip_dir}')
        result_files = generate_entity_json(n_files, n_objects, start_idx=offset, source=polygons)
        for idx, file in enumerate(result_files):

            json.dump(file, open(os.path.join(zip_dir, "_".join([os.path.basename(zip_id), str(idx)])), "w"))
        shutil.make_archive(zip_dir, 'zip', zip_dir)
        shutil.rmtree(zip_dir)
    _log.info(f'Finish creating:\n'
              f'- zips: {n_zips}\n'
              f'- files per single zip: {n_files}\n'
              f'- entities on each file: {n_objects}\n'
              f'*** Total data: {n_zips*n_files*n_objects} entities ***')
    # output_final = os.path.join(output_dir, "_".join([str(layer_id), common.generate_uuid()]))
    # if not os.path.exists(output_final):
    #     os.makedirs(output_final)
    # _log.info(
    #     f'Result of new generated file will be placed on: {output_dir}, File name: {os.path.basename(output_final)}')
    # result_files = generate_entity_json(n_files, n_objects, source=polygons)
    # for idx, file in enumerate(result_files):
    #     json.dump(file, open(os.path.join(output_final, "_".join([os.path.basename(output_final), str(idx)])), "w"))
    #
    # # create entity zip file and remove temporary folder
    # shutil.make_archive(output_final, 'zip', output_final)
    # shutil.rmtree(output_final)


def generate_entity_json(num_of_files=10, entities_per_file=10, start_idx=0, source=None):
    """
    This method generate json file entity with polygons
    :return: json object with entities
    """
    entities_list = []
    total_entities = num_of_files * entities_per_file
    current_poly_idx = 0+start_idx
    # todo - refactor ingestion of new polygon to be more generic
    if not source:
        source = config.DEBUG_ENTITY_FILE
        source_data = json.load(open(source, "r"))
        polygons = source_data['features']
    else:
        polygons = source
    # _log.info(f'Total number of features on data source: {len(polygons)}')
    _log.info(f'Start generate {current_poly_idx+1}-{current_poly_idx+total_entities} entities: \n')
    for i in range(num_of_files):
        entities_file = []
        for j in range(entities_per_file):
            _log.info(
                f'Generating entity number {current_poly_idx + 1} related zip idx {(start_idx//num_of_files//entities_per_file)+1} under file: {i + 1}, number in file: {j + 1}')
            entity = config.ENTITY_SKELETON
            entity['exclusive_id']['entity_id'] = '{%s}' % common.generate_uuid()
            entity['exclusive_id']['name'] = "_".join(['Building', str(current_poly_idx)])
            entity['date'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            entity['geo']['geo_json']['coordinates'] = polygons[current_poly_idx]['geometry']['coordinates']
            entity['geo']['area'] = geometry.get_polygon_area(entity['geo']['geo_json']['coordinates'][0])
            entity['geo']['perimeter'] = geometry.get_polygon_perimeter(entity['geo']['geo_json']['coordinates'][0])
            entity['properties_list']['BUILDING'] = 'YES'

            current_poly_idx += 1
            entities_file.append(copy.deepcopy(entity))
        entities_list.append(copy.deepcopy(entities_file))
    # _log.info(f'\nCreated total {current_poly_idx} out of {total_entities} required\n'
    #           f'Number of groups: {num_of_files}\n'
    #           f'Number of entities per group: {entities_per_file}')
    _log.info(f'Finish generating entities: {current_poly_idx}-{current_poly_idx+total_entities} for group: {i+1},number in group: {j + 1}')

    return entities_list
