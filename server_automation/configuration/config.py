# pylint: disable=line-too-long
""" configuration interface """
import os
from datetime import datetime
import enum
from mc_automation_tools import common


class ResponseCode(enum.Enum):
    """
    Types of server responses
    """
    Ok = 200  # server return ok status
    IngestionModelOk = 201
    ValidationErrors = 400  # bad request
    StatusNotFound = 404  # status\es not found on db
    ServerError = 500  # problem with error
    DuplicatedError = 409  # in case of requesting package with same name already exists
    GetwayTimeout = 504


##################################      Running global environment variables     #######################################
# ENVIRONMENT_NAME = common.get_environment_variable('ENVIRONMENT_NAME', 'dev')
# TMP_DIR = common.get_environment_variable('TMP_DIR', '/tmp/auto_3rd')
###################################### S3 #############################################################
# S3_TILE_LINK_SOURCE = common.get_environment_variable("S3_TILE_LINK_SOURCE", False)
# S3_DOWNLOAD_EXPIRATION_TIME = common.get_environment_variable("S3_DOWNLOAD_EXPIRED_TIME", 3600)
# S3_DOWNLOAD_DIRECTORY = common.get_environment_variable('S3_DOWNLOAD_DIR', '/tmp/')
# S3_BUCKET_NAME = common.get_environment_variable('S3_BUCKET_NAME', None)
# S3_ACCESS_KEY = common.get_environment_variable('S3_ACCESS_KEY', None)
# S3_SECRET_KEY = common.get_environment_variable('S3_SECRET_KEY', None)
# S3_END_POINT = common.get_environment_variable('S3_END_POINT', None)
################################################# postgress credits ####################################################
UPDATE_DB = common.get_environment_variable('UPDATE_DB', True)
PG_USER = common.get_environment_variable('PG_USER', None)
PG_PASS = common.get_environment_variable('PG_PASS', None)
PG_HOST = common.get_environment_variable('PG_HOST', 'localhost')
PG_DB_NAME = common.get_environment_variable('PG_DB_NAME', 'vector-automation-tests')
PG_TABLE_NAME = common.get_environment_variable('PG_TABLE_NAME', 'buildings')
#################################################### general ###########################################################
LAYER_ID_B = common.get_environment_variable('LAYER_ID_B', 614)
LAYER_ID = common.get_environment_variable('LAYER_ID', 614)
LAYER_NAME = common.get_environment_variable('LAYER_NAME', 'building')
EXT_FOR_SYNC_FILE = common.get_environment_variable('EXT_FOR_SYNC_FILE', 'json')
EXEC_TYPE_FULL = 'FULL'
EXEC_TYPE_DIFF = 'DIFF'
SYNC_DATA_URL = common.get_environment_variable('SYNC_DATA_URL', 'http://10.8.1.9/full.json')
DIFF_SAMPLES = common.get_environment_variable('DIFF_SAMPLES', 10000)
Z_TIME = datetime.now().strftime('vector_%Y%m_%d_%H_%M_%S')
DIFF_SAMPLES_PERCENTAGE = common.get_environment_variable('DIFF_SAMPLES_PERCENTAGE', 0.1)

BASE_STORAGE_DATA_DIR = common.get_environment_variable('BASE_STORAGE_DATA_DIR', '/tmp')
RELATIVE_DIR = common.get_environment_variable('RELATIVE_DIR', os.path.join('vector_data', Z_TIME))
RELATIVE_DIFF_DIR = common.get_environment_variable('RELATIVE_DIFF_DIR', os.path.join('vector_data', 'diff', Z_TIME))
STORE_DIFF_DIR = os.path.join(BASE_STORAGE_DATA_DIR, RELATIVE_DIFF_DIR)
DIFF_RANDOM_MAX = common.get_environment_variable('DIFF_RANDOM_MAX', 1)
MAX_HEIGHT_PROP = common.get_environment_variable('MAX_HEIGHT_PROP', 30)
MIN_HEIGHT_PROP = common.get_environment_variable('MIN_HEIGHT_PROP', 3)
STORE_DATA_DIR = os.path.join(BASE_STORAGE_DATA_DIR, RELATIVE_DIR)
STATIC_URL_FOR_FILES = common.get_environment_variable('STATIC_URL_FOR_FILES', 'http://10.8.1.9')
################################################ response messeages ####################################################

USE_JIRA = common.get_environment_variable('USE_JIRA', False)

SYNC_LAYER_SKELETON = {
    "files": [
        {
            "layer_id": 614,
            "exec_type": "FULL",
            "created": "2021-05-22T21:00:04Z",
            "files": [
                {
                    "file_name": "http://10.8.1.9/entities.zip",
                    "file_count": 1
                }
            ]
        }
    ]
}

ENTITY_SKELETON = {
    "exclusive_id": {
        "data_store_name": "automation",
        "name": "meow",
        "entity_id": "one"
    },
    "classification": {
        "hi": 1,
        "ho": "sh"
    },
    "date": "05/05/2019 06:58:35",
    "link": "http...",
    "geo": {
        "wkt": "POLY",
        "geo_json": {
            "type": "Polygon",
            "coordinates": [
                [
                    [35.201037526130676, 31.769924871200327],
                    [35.20086854696274, 31.769892946554663],
                    [35.201058983802795, 31.76914499456106],
                    [35.20123064517975, 31.769181480164423],
                    [35.201037526130676, 31.769924871200327]
                ]
            ]
        },
        "area": 1.123,
        "perimeter": 0.03
    },
    "properties_list": {"action": "added tag"}
}

DIFF_SKELETON = {
    "files": [
        {
            "layer_id": 614,
            "exec_type": "DIFF",
            "created": "2021-05-22T22:00:04Z",
            "files": [
                {
                    "file_name": "http://10.8.1.9/diff.zip",
                    "file_count": 1
                }
            ]
        }
    ]
}
DEBUG_ENTITY_FILE = common.get_environment_variable('DEBUG_ENTITY_FILE',
                                                    '/home/ronenk1/dev/automation-tests-vector/geojsons/DistrictofColumbia.geojson')
