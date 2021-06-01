# pylint: disable=line-too-long
""" configuration interface """
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
#################################################### general ###########################################################
LAYER_ID_B = common.get_environment_variable('LAYER_ID_B', 614)
EXT_FOR_SYNC_FILE = common.get_environment_variable('EXT_FOR_SYNC_FILE', 'json')
EXEC_TYPE_FULL = 'FULL'
EXEC_TYPE_DIFF = 'DIFF'
SYNC_DATA_URL = common.get_environment_variable('SYNC_DATA_URL', 'http://10.8.1.9/full.json')
STORE_DATA_DIR = common.get_environment_variable('STORE_DATA_DIR', '/tmp')

################################################ response messeages ####################################################

USE_JIRA = common.get_environment_variable('USE_JIRA', False)

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
    "properties_list": { "action": "added tag" }
  }

DEBUG_ENTITY_FILE = common.get_environment_variable('DEBUG_ENTITY_FILE', '/home/ronenk1/dev/automation-tests-vector/geojsons/small_70k_Alaska.geojson')