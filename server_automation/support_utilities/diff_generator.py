"""This module responsible to generate diff files"""
import copy
import enum
import random
import os
import json
import shutil
from datetime import datetime

from server_automation.configuration import config
from server_automation.postgress import postgres_adapter
from mc_automation_tools import common
import logging

_log = logging.getLogger('server_automation.support_utilities.diff_generator')
num_of_generation = 0
num_of_samples = 0


class RandomDiffOpt(enum.Enum):
    add_tag = 0
    high_change = 1
    no_change = 2
    delete = 3
    insert = 4
    geometry = 5


def create_diff_json(files_output_dir, layer_id, zip_names):
    single_file = copy.deepcopy(config.DIFF_SKELETON)
    single_file = single_file['files'][0]
    creation_date = common.generate_datatime_zulu()
    exec_type = config.EXEC_TYPE_DIFF
    relative_path = files_output_dir.split(config.BASE_STORAGE_DATA_DIR)[1]
    files = []

    # todo - insert to automation kit package
    from contextlib import closing
    from zipfile import ZipFile
    import urllib.parse as p  # todo - insert to automation kit package
    output_url = p.urljoin(config.STATIC_URL_FOR_FILES, relative_path)

    for name in zip_names:
        file = {}
        file_url = os.path.join(output_url, ".".join([name, 'zip']))
        zip_location = os.path.join(files_output_dir, ".".join([name, 'zip']))
        with closing(ZipFile(zip_location)) as archive:
            count_in_zip = len(archive.infolist())
        file['file_name'] = file_url
        file['count'] = count_in_zip
        files.append(file)

    single_file['layer_id'] = layer_id
    single_file['exec_type'] = exec_type
    single_file['created'] = creation_date
    single_file['files'].clear()
    single_file['files'] = files
    return single_file





def generate_new_diff(layer_id, n_zips=10, n_files=10, n_objects=10, samples=config.DIFF_SAMPLES_PERCENTAGE,
                      output_dir=config.STORE_DIFF_DIR):
    c_time = datetime.now().strftime('%Y%m_%d_%H_%M_%S')
    # create root directory saving the diff generation
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    full_entities_id = postgres_adapter.get_all_entities_id()
    num_of_samples = int(len(full_entities_id) * samples)
    samples_ids = random.sample(full_entities_id, num_of_samples)
    # sample_per_file = len(samples_ids) // n_zips // n_files
    sample_per_zip = len(samples_ids) // n_zips
    zip_names = []
    diff_update_list = []
    for i in range(n_zips):
        _log.info(f'\n\n*** Start generate zip:{i+1} ***')
        zip_name = "_".join([str(layer_id), common.generate_uuid()])
        zip_names.append(zip_name)
        samples = samples_ids[i*sample_per_zip:i*sample_per_zip+sample_per_zip]
        zip_dir = os.path.join(output_dir, zip_name)
        create_zip_file(layer_id, n_files, samples, zip_dir, i+1, diff_update_list=diff_update_list)
        shutil.make_archive(zip_dir, 'zip', zip_dir)
        shutil.rmtree(zip_dir)
    postgres_adapter.update_diff_on_db(diff_update_list,)
    return {'zips': zip_names, 'storage': output_dir, 'layer_id': layer_id}


def create_zip_file(layer_id, n_files=10, samples_id=[], output_dir=config.STORE_DATA_DIR, zip_idx=None, diff_update_list=[]):
    """
    This method generate single zip file including entities diff json files
    :return:
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    entities_list = []
    samples_per_file = len(samples_id) // n_files

    total_updates = []
    for i in range(n_files):

        _log.info(f'Generating [{samples_per_file}] changes for file [{i+1}] out of [{n_files}] on zip [{zip_idx}]')
        file_name = "_".join([str(layer_id), common.generate_uuid()])
        samples = samples_id[i * samples_per_file:i * samples_per_file + samples_per_file]
        orig_json_objects = postgres_adapter.get_json_by_id(copy.deepcopy(samples))
        res = create_entity_file(orig_json_objects, diff_update_list=diff_update_list)
        entities_list.append(res)

        res = [(elem['exclusive_id']['entity_id'][1:-1], json.dumps(elem)) for elem in res]
        total_updates = total_updates + res
        entities = [json.loads(elem[1]) for elem in res]
        with open(os.path.join(output_dir, file_name), 'w') as fp:
            json.dump(entities, fp)

    postgres_adapter.update_json_on_db(total_updates, config.PG_TABLE_NAME)


    pass


def create_entity_file(orig_objects, diff_update_list):
    """
    This method generate json file of entities with changes
    :return:
    """
    new_objects = []
    for idx, object_json in enumerate(orig_objects):
        type_of_diff = random.randint(1, config.DIFF_RANDOM_MAX)
        if type_of_diff == RandomDiffOpt.high_change.value:
            object_json = change_building_height(object_json)
            object_json['properties_list']['diff'] = str(int(object_json['properties_list']['diff'])+1)
            new_objects.append(object_json)
            diff_update_list.append((object_json['exclusive_id']['entity_id'][1:-1], int(object_json['properties_list']['diff'])))
    # postgres_adapter.update_diff_on_db(diff_update_list)
    return new_objects


def generate_diff_zips(layer_id, n_zips=10, n_files=10, n_objects=10, sample_list=[], sample_per_file=10):

    for i in range(n_zips):
        create_zip_file()
    pass


def change_building_height(json_object, new_height=None):
    if not new_height:
        new_height = random.uniform(config.MIN_HEIGHT_PROP, config.MAX_HEIGHT_PROP)

    json_object['properties_list']['RELATIVE_HEIGHT'] = new_height
    return json_object


def add_new_tag(json_object, tag_content=[]):
    if not tag_content:
        diff_version = json_object['properties_list'].get('diff')
        if not diff_version:
            json_object['properties_list']['diff'] = '0'
        else:
            diff_version = int(json_object['properties_list'].get('diff'))
            diff_version += 1
            json_object['properties_list']['diff'] = str(diff_version)
    else:
        _log.warning('Not implement yet, other random tag dynamic addition')
        return json_object
    return json_object