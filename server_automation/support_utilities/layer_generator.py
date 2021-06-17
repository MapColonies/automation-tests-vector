"""This module provide method to generate new full layer json data for sync to OSM"""
import os
import json
import copy
import datetime
import random
import shutil
from server_automation.configuration import config
from mc_automation_tools import common, geometry
from server_automation.postgress import postgres_adapter as pa
from dataclasses import dataclass
import logging

_log = logging.getLogger('server_automation.support_utilities.layer_generator')


@dataclass(frozen=True)
class GenerationFullParam:
    """
    This class organize basic parameters for generating sync full data
    """
    layer_id: str
    unique_id: str
    current_date: str
    root_file_name: str
    n_zip: int
    n_files: int
    n_object: int
    output_dir: str
    source_dir: str


def generate_single_full_json(layer_id, n_zips=10, n_files=10, n_objects=10,
                              output_dir=config.STORE_DATA_DIR, source=config.DEBUG_ENTITY_FILE):
    """This method create full_json file to start synchronization"""

    s_layer_id = str(layer_id)
    unique_id = common.generate_uuid().replace('-', '_')
    current_date = common.generate_datatime_zulu()
    file_name = "_".join([s_layer_id, unique_id])
    # params = GenerationFullParam(layer_id=layer_id, unique_id=unique_id, current_date=current_date,
    #                              root_file_name=file_name, n_zips=n_zips, n_files=n_files, n_objects=n_objects,
    #                              output_dir=output_dir, source_dir=source)

    files_output_dir, files_names = generate_entity_file(layer_id=s_layer_id,
                                                         n_zips=n_zips,
                                                         n_files=n_files,
                                                         n_objects=n_objects,
                                                         output_dir=output_dir,
                                                         source=source)

    relative_path = files_output_dir.split(config.BASE_STORAGE_DATA_DIR)[1]
    import urllib.parse as p  # todo - insert to automation kit package
    output_url = p.urljoin(config.STATIC_URL_FOR_FILES, relative_path)

    single_file = copy.deepcopy(config.SYNC_LAYER_SKELETON)
    single_file['files'][0]['layer_id'] = layer_id
    # single_file['files'][0]['diff_version'] = 0
    single_file['files'][0]['exec_type'] = config.EXEC_TYPE_FULL
    single_file['files'][0]['created'] = current_date
    single_file['files'][0]['files'].clear()

    # todo - insert to automation kit package
    from contextlib import closing
    from zipfile import ZipFile

    for file in files_names:
        zip_location = os.path.join(files_output_dir, file)
        with closing(ZipFile(zip_location)) as archive:
            count_in_zip = len(archive.infolist())
        file_uri = output_url + '/' + file
        single_file['files'][0]['files'].append({'file_name': file_uri, 'file_count': count_in_zip})
    res_file_name = ".".join(["_".join(['full',config.Z_TIME]),'json'])
    with open(os.path.join(files_output_dir, res_file_name), 'w') as fp:
        json.dump(single_file, fp, indent=4)
    print(single_file)


def generate_entity_file(layer_id, n_zips=10, n_files=10, n_objects=10,
                         output_dir=config.STORE_DATA_DIR, source=config.DEBUG_ENTITY_FILE):
    """
    This method will generate single file object for specific layer type
    :param source: source directory to ingest polygons for entities
    :param output_dir: destination root directory to store generated data
    :param n_zips: number of zips per directory to create
    :param layer_id: layer type id
    :param n_files: number of file per zip
    :param n_objects: number of objects per entity file (polygons)
    :return: dict of single file object 
    """

    output_dir = os.path.join(output_dir, str(layer_id))
    _log.info(f'New job of generating data:\n'
              f'Destination directory storing generated data: {output_dir}\n'
              f'Number of zip files: {n_zips}\n'
              f'Number of json files per single zip: {n_files}\n'
              f'Number of object per json (polygons): {n_objects}\n'
              f'Total dataset for [FULL] to generate: {n_zips * n_files * n_objects}\n'
              f'Absolut root path for results: {output_dir}')

    # validating the provided source to generation include enough data to requested generation
    source_data = json.load(open(source, "r"))
    polygons = source_data['features']
    _log.info(f'Total number of features on data source: {len(polygons)}')
    if len(polygons) < (n_zips * n_files * n_objects):
        raise Exception(f"Provided data source doesn't fit to requested size of generation:\n"
                        f"Requested [{n_zips * n_files * n_objects}] > Source data polygon count [{len(polygons)}]")

    zip_names = []
    for i in range(n_zips):
        zip_id = "_".join([str(layer_id), common.generate_uuid()])
        zip_dir = os.path.join(output_dir, zip_id)
        zip_names.append(".".join([zip_id, 'zip']))
        if not os.path.exists(zip_dir):
            os.makedirs(zip_dir)
        offset = i * n_files * n_objects
        _log.info(f'Generating zip {i + 1}\\{n_zips}: {zip_id}, into: {zip_dir}')
        result_files = generate_entity_json(n_files, n_objects, start_idx=offset, source=polygons)
        for idx, file in enumerate(result_files):
            unique_file_id = "_".join([layer_id, common.generate_uuid()])
            json.dump(file, open(os.path.join(zip_dir, unique_file_id), "w"))
            # json.dump(file, open(os.path.join(zip_dir, "_".join([os.path.basename(zip_id), str(idx)])), "w"))
        shutil.make_archive(zip_dir, 'zip', zip_dir)
        shutil.rmtree(zip_dir)
    _log.info(f'Finish creating:\n'
              f'- zips: {n_zips}\n'
              f'- files per single zip: {n_files}\n'
              f'- entities on each file: {n_objects}\n'
              f'*** Total data: {n_zips * n_files * n_objects} entities ***')
    return output_dir, zip_names


def generate_entity_json(num_of_files=10, entities_per_file=10, start_idx=0, source=None):
    """
    This method generate json file entity with polygons
    :return: json object with entities
    """

    try:
        pa.create_full_table(config.PG_TABLE_NAME)
    except Exception as e:
        _log.warning(f'Table {config.PG_TABLE_NAME} already exists, will insert values to exists!')
        _log.warning(f'{str(e)}')

    entities_list = []
    total_entities = num_of_files * entities_per_file
    current_poly_idx = 0 + start_idx
    # todo - refactor ingestion of new polygon to be more generic
    if not source:
        source = config.DEBUG_ENTITY_FILE
        source_data = json.load(open(source, "r"))
        polygons = source_data['features']
    else:
        polygons = source
    _log.info(f'Start generate {current_poly_idx + 1}-{current_poly_idx + total_entities} entities: \n')
    for i in range(num_of_files):
        entities_file = []
        entities_params = []
        for j in range(entities_per_file):
            _log.info(
                f'Generating entity number {current_poly_idx + 1} related zip idx {(start_idx // num_of_files // entities_per_file) + 1} under file: {i + 1}, number in file: {j + 1}')
            entity = config.ENTITY_SKELETON
            entity['exclusive_id']['entity_id'] = '{%s}' % common.generate_uuid()
            entity['exclusive_id']['name'] = "_".join([config.LAYER_NAME, str(current_poly_idx)])
            entity['date'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            entity['geo']['geo_json']['coordinates'] = polygons[current_poly_idx]['geometry']['coordinates']
            entity['geo']['area'] = geometry.get_polygon_area(entity['geo']['geo_json']['coordinates'][0])
            entity['geo']['perimeter'] = geometry.get_polygon_perimeter(entity['geo']['geo_json']['coordinates'][0])
            entity['properties_list']['BUILDING'] = 'YES'
            entity['properties_list']['diff'] ='0'
            entity['properties_list']['RELATIVE_HEIGHT'] = random.uniform(config.MIN_HEIGHT_PROP, config.MAX_HEIGHT_PROP)

            current_poly_idx += 1
            db_params = {
                'uuid': entity['exclusive_id']['entity_id'],
                'layer_id': config.LAYER_ID,
                'name': entity['exclusive_id']['name'],
                'layer_type': config.LAYER_NAME,
                'cdatetime': str(datetime.datetime.now()),
                'udatatime': str(datetime.datetime.now()),
                'geo_json': json.dumps(entity['geo']['geo_json']),
                'entity_json': json.dumps(entity),
                'diff' : 0
            }
            entities_params.append(db_params)
            # insert_entity_to_db(db_params)
            entities_file.append(copy.deepcopy(entity))
        pa.insert_entity_to_db(entities_params, config.PG_TABLE_NAME)
        entities_list.append(copy.deepcopy(entities_file))

    _log.info(
        f'Finish generating entities: {current_poly_idx}-{current_poly_idx + total_entities} for group: {i + 1}, '
        f'number in group: {j + 1}')

    return entities_list
